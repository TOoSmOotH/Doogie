from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import random
import asyncio

from src.database import Document, DocumentChunk, GraphNode, GraphEdge
from src.llm_connector.factory import get_embedding_model
from src.rag.bm25_indexer import get_bm25_indexer
from src.rag.vector_search import get_vector_search
from src.rag.graph_rag import get_graph_rag
from src.rag.neural_reranker import get_neural_reranker


async def retrieve_context(
    query: str,
    db: Session,
    limit: int = 5,
    use_hybrid: bool = True,
    use_graph: bool = True,
    use_reranking: bool = True,
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant context for a query using hybrid RAG.
    
    Args:
        query: The query to retrieve context for
        db: Database session
        limit: Maximum number of results to return
        use_hybrid: Whether to use hybrid search (BM25 + vector)
        use_graph: Whether to include graph search results
        use_reranking: Whether to apply neural reranking
        
    Returns:
        A list of relevant document chunks with metadata
    """
    # Check if we have any documents in the database
    doc_count = db.query(Document).count()
    if doc_count == 0:
        # If no documents, return mock results
        return await _mock_retrieve(query, db, limit)
    
    # Get results from hybrid search
    results = []
    
    if use_hybrid:
        # Get hybrid search results (BM25 + vector)
        hybrid_results = await hybrid_search(query, db, limit=limit * 2)  # Get more results for reranking
        results.extend(hybrid_results)
    
    if use_graph:
        # Get graph search results
        graph_results = await graph_search(query, db, limit=limit)
        
        # Add graph results, avoiding duplicates
        existing_ids = {r["id"] for r in results}
        for result in graph_results:
            if result["id"] not in existing_ids:
                results.append(result)
                existing_ids.add(result["id"])
    
    # If no results from either method, fall back to mock results
    if not results:
        return await _mock_retrieve(query, db, limit)
    
    # Apply neural reranking if requested
    if use_reranking and results:
        results = await neural_rerank(query, results, db, limit=limit)
    else:
        # Sort by relevance and limit results
        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        results = results[:limit]
    
    return results


async def _mock_retrieve(
    query: str,
    db: Session,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Mock retrieval for development."""
    # Simulate processing time
    await asyncio.sleep(0.5)
    
    # Get some random document chunks from the database if available
    chunks = db.query(DocumentChunk).limit(limit).all()
    
    if chunks:
        # Return actual chunks from the database
        return [
            {
                "id": chunk.id,
                "content": chunk.content,
                "document_id": chunk.document_id,
                "title": chunk.document.title if hasattr(chunk, "document") else "Unknown Document",
                "relevance": random.uniform(0.7, 0.95),
                "source": "database",
            }
            for chunk in chunks
        ]
    else:
        # Return mock chunks
        return [
            {
                "id": f"mock-chunk-{i}",
                "content": f"This is mock content related to {query}. It contains information about {query.split()[0] if query.split() else 'topics'} and other related concepts.",
                "document_id": f"mock-doc-{i}",
                "title": f"Mock Document {i}",
                "relevance": random.uniform(0.7, 0.95),
                "source": "mock",
            }
            for i in range(limit)
        ]


async def hybrid_search(
    query: str,
    db: Session,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Perform hybrid search using BM25 and vector search.
    
    Args:
        query: The query to search for
        db: Database session
        limit: Maximum number of results to return
        
    Returns:
        A list of relevant document chunks with metadata
    """
    # Get results from BM25
    bm25_results = await bm25_search(query, db, limit=limit)
    
    # Get results from vector search
    vector_results = await vector_search(query, db, limit=limit)
    
    # Combine and deduplicate results
    combined_results = {}
    
    # Add BM25 results
    for result in bm25_results:
        combined_results[result["id"]] = result
    
    # Add vector results, updating relevance if already exists
    for result in vector_results:
        if result["id"] in combined_results:
            # Average the relevance scores
            combined_results[result["id"]]["relevance"] = (
                combined_results[result["id"]]["relevance"] + result["relevance"]
            ) / 2
            combined_results[result["id"]]["sources"] = "hybrid"
        else:
            combined_results[result["id"]] = result
    
    # Convert back to list and sort by relevance
    results = list(combined_results.values())
    results.sort(key=lambda x: x["relevance"], reverse=True)
    
    # Limit results
    return results[:limit]


async def bm25_search(
    query: str,
    db: Session,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Perform BM25 search.
    
    Args:
        query: The query to search for
        db: Database session
        limit: Maximum number of results to return
        
    Returns:
        A list of relevant document chunks with metadata
    """
    # Get BM25 indexer
    bm25_indexer = get_bm25_indexer()
    
    # Search using BM25
    results = await bm25_indexer.search(query, limit=limit)
    
    # If no results, check if we need to index documents
    if not results:
        # Check if we have any documents that need indexing
        doc_count = db.query(Document).count()
        if doc_count > 0:
            print(f"No BM25 results found. Indexing {doc_count} documents...")
            await bm25_indexer.index_all_documents(db)
            
            # Try search again
            results = await bm25_indexer.search(query, limit=limit)
    
    # If still no results, return mock results
    if not results:
        # Mock BM25 results
        return [
            {
                "id": f"mock-chunk-bm25-{i}",
                "content": f"This is a BM25 result for {query}. It contains keywords like {query.split()[0] if query.split() else 'example'} and other related terms.",
                "document_id": f"mock-doc-{i}",
                "title": f"Mock BM25 Document {i}",
                "relevance": random.uniform(0.6, 0.9),
                "source": "bm25",
            }
            for i in range(limit)
        ]
    
    return results


async def vector_search(
    query: str,
    db: Session,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Perform vector search.
    
    Args:
        query: The query to search for
        db: Database session
        limit: Maximum number of results to return
        
    Returns:
        A list of relevant document chunks with metadata
    """
    # Get embedding model
    embedding_model = get_embedding_model(db)
    
    # Get query embedding
    query_embedding = await embedding_model.get_embedding(query)
    
    # Get vector search instance
    vector_search_instance = get_vector_search()
    
    # Search using vector search
    results = await vector_search_instance.search(query_embedding, limit=limit, db=db)
    
    # If no results, check if we need to index documents
    if not results:
        # Check if we have any documents that need indexing
        doc_count = db.query(Document).count()
        if doc_count > 0:
            print(f"No vector search results found. Indexing {doc_count} documents...")
            await vector_search_instance.index_all_documents(db)
            
            # Try search again
            results = await vector_search_instance.search(query_embedding, limit=limit, db=db)
    
    # If still no results, return mock results
    if not results:
        # Mock vector search results
        return [
            {
                "id": f"mock-chunk-vector-{i}",
                "content": f"This is a vector search result for {query}. It is semantically similar to the query and discusses {query.split()[0] if query.split() else 'concepts'} in depth.",
                "document_id": f"mock-doc-{i}",
                "title": f"Mock Vector Document {i}",
                "relevance": random.uniform(0.7, 0.95),
                "source": "vector",
            }
            for i in range(limit)
        ]
    
    return results


async def graph_search(
    query: str,
    db: Session,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Perform graph-based search.
    
    Args:
        query: The query to search for
        db: Database session
        limit: Maximum number of results to return
        
    Returns:
        A list of relevant document chunks with metadata
    """
    # Get graph RAG instance
    graph_rag = get_graph_rag()
    
    # Search using graph RAG
    results = await graph_rag.search(query, limit=limit, db=db)
    
    # If no results, check if we need to build the graph
    if not results:
        # Check if we have any documents that need graph building
        doc_count = db.query(Document).count()
        if doc_count > 0:
            print(f"No graph search results found. Building graph for {doc_count} documents...")
            
            # Get all documents
            documents = db.query(Document).all()
            
            # Build graph for each document
            for document in documents:
                await graph_rag.build_graph_for_document(document.id, db)
            
            # Try search again
            results = await graph_rag.search(query, limit=limit, db=db)
    
    # If still no results, return mock results
    if not results:
        # Mock graph search results
        return [
            {
                "id": f"mock-chunk-graph-{i}",
                "content": f"This is a graph search result for {query}. It is connected to concepts related to {query.split()[0] if query.split() else 'topics'} through the knowledge graph.",
                "document_id": f"mock-doc-{i}",
                "title": f"Mock Graph Document {i}",
                "relevance": random.uniform(0.75, 0.98),
                "source": "graph",
            }
            for i in range(limit)
        ]
    
    return results


async def neural_rerank(
    query: str,
    results: List[Dict[str, Any]],
    db: Session,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Rerank results using a neural reranker.
    
    Args:
        query: The original query
        results: The results to rerank
        db: Database session
        limit: Maximum number of results to return
        
    Returns:
        Reranked results
    """
    # Get neural reranker
    reranker = get_neural_reranker()
    
    # Rerank results
    reranked_results = await reranker.rerank(query, results, limit=limit)
    
    # If no results from reranker, fall back to original results
    if not reranked_results:
        # Copy results to avoid modifying the original
        reranked = results.copy()
        
        # Sort by relevance and limit
        reranked.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        return reranked[:limit]
    
    return reranked_results