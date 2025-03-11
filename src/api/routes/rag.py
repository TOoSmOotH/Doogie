from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db, User
from src.api.schemas.documents import SearchQuery, SearchResult
from src.api.routes.auth import get_current_active_user
from src.rag.retriever import retrieve_context, hybrid_search, graph_search, neural_rerank

# Router
router = APIRouter()


@router.post("/search", response_model=List[SearchResult])
async def search(
    query: SearchQuery,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Search for documents using the RAG system.
    
    This endpoint performs a search using the specified query and retrieval options.
    """
    try:
        # Perform search based on options
        if query.use_hybrid:
            # Use hybrid search (BM25 + vector)
            results = await hybrid_search(query.query, db, limit=query.limit * 2)
            
            # Add graph results if requested
            if query.use_graph:
                graph_results = await graph_search(query.query, db, limit=query.limit)
                
                # Combine results
                result_ids = {r["id"] for r in results}
                for result in graph_results:
                    if result["id"] not in result_ids:
                        results.append(result)
                        result_ids.add(result["id"])
            
            # Rerank if requested
            if query.use_reranker and len(results) > 0:
                results = await neural_rerank(query.query, results, db, limit=query.limit)
            else:
                # Sort by relevance and limit
                results.sort(key=lambda x: x["relevance"], reverse=True)
                results = results[:query.limit]
        else:
            # Use simple retrieval
            results = await retrieve_context(query.query, db, limit=query.limit)
        
        return results
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


@router.get("/status", response_model=dict)
async def rag_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get the status of the RAG system.
    
    This endpoint returns information about the RAG system, such as the number of documents,
    chunks, and other relevant statistics.
    """
    try:
        # In a real implementation, this would query the database for statistics
        # For now, return mock data
        return {
            "status": "operational",
            "documents": {
                "total": 0,
                "by_type": {},
                "by_status": {},
            },
            "chunks": {
                "total": 0,
            },
            "graph": {
                "nodes": 0,
                "edges": 0,
            },
            "last_updated": "2025-03-11T12:00:00Z",
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get RAG status: {str(e)}",
        )