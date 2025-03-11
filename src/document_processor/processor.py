from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
import os
import asyncio
import uuid

from src.database import Document, DocumentChunk, DocumentStatus, DocumentType, DocumentSource
from src.llm_connector.factory import get_embedding_model


async def process_document(
    document_id: str,
    db: Session,
) -> bool:
    """
    Process a document and create chunks.
    
    Args:
        document_id: The ID of the document to process
        db: Database session
        
    Returns:
        True if processing was successful, False otherwise
    """
    # Get the document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        return False
    
    try:
        # Update document status to processing
        document.status = DocumentStatus.PROCESSING
        db.commit()
        
        # Extract text based on document type
        text = await extract_text(document)
        
        # Chunk the text
        chunks = chunk_text(text)
        
        # Get embedding model
        embedding_model = get_embedding_model(db)
        
        # Process each chunk
        for i, chunk_text in enumerate(chunks):
            # Create chunk
            chunk = DocumentChunk(
                document_id=document_id,
                content=chunk_text,
                chunk_index=i,
                metadata={"position": i, "total_chunks": len(chunks)},
            )
            db.add(chunk)
            db.commit()
            db.refresh(chunk)
            
            # Generate embedding
            embedding = await embedding_model.get_embedding(chunk_text)
            
            # Save embedding to file
            embedding_dir = os.path.join("data", "embeddings", document_id)
            os.makedirs(embedding_dir, exist_ok=True)
            embedding_file = os.path.join(embedding_dir, f"{chunk.id}.npy")
            
            # In a real implementation, we would save the embedding to a file
            # For now, just update the embedding_file field
            chunk.embedding_file = embedding_file
            db.commit()
        
        # Update document status to completed
        document.status = DocumentStatus.COMPLETED
        db.commit()
        
        return True
    
    except Exception as e:
        # Update document status to failed
        document.status = DocumentStatus.FAILED
        document.metadata = document.metadata or {}
        document.metadata["error"] = str(e)
        db.commit()
        
        return False


async def extract_text(document: Document) -> str:
    """
    Extract text from a document.
    
    Args:
        document: The document to extract text from
        
    Returns:
        The extracted text
    """
    # For development, return mock text
    # In production, this will be replaced with actual text extraction
    
    # Simulate processing time
    await asyncio.sleep(0.5)
    
    if document.doc_type == DocumentType.PDF:
        return f"This is mock text extracted from a PDF document titled '{document.title}'.\n\n" + \
               f"It contains multiple paragraphs of information about {document.title}.\n\n" + \
               f"The document discusses various aspects of the topic and provides detailed explanations.\n\n" + \
               f"This is the end of the mock PDF content."
    
    elif document.doc_type == DocumentType.DOCX:
        return f"This is mock text extracted from a DOCX document titled '{document.title}'.\n\n" + \
               f"It contains formatted text, possibly with headings, lists, and tables.\n\n" + \
               f"The document covers {document.title} in detail with various sections.\n\n" + \
               f"This is the end of the mock DOCX content."
    
    elif document.doc_type == DocumentType.MARKDOWN:
        return f"# {document.title}\n\n" + \
               f"This is mock text extracted from a Markdown document.\n\n" + \
               f"## Section 1\n\n" + \
               f"It contains markdown formatting with headers, lists, and code blocks.\n\n" + \
               f"## Section 2\n\n" + \
               f"The document explains {document.title} with examples and references.\n\n" + \
               f"This is the end of the mock Markdown content."
    
    elif document.doc_type == DocumentType.RST:
        return f"{document.title}\n{'=' * len(document.title)}\n\n" + \
               f"This is mock text extracted from an RST document.\n\n" + \
               f"Section 1\n--------\n\n" + \
               f"It contains RST formatting with headers, directives, and references.\n\n" + \
               f"Section 2\n--------\n\n" + \
               f"The document covers {document.title} with detailed explanations.\n\n" + \
               f"This is the end of the mock RST content."
    
    elif document.doc_type == DocumentType.TEXT:
        return f"This is mock text extracted from a plain text document titled '{document.title}'.\n\n" + \
               f"It contains unformatted text with paragraphs separated by line breaks.\n\n" + \
               f"The document discusses {document.title} in a straightforward manner.\n\n" + \
               f"This is the end of the mock text content."
    
    elif document.doc_type == DocumentType.HTML:
        return f"This is mock text extracted from an HTML document titled '{document.title}'.\n\n" + \
               f"It contains content extracted from HTML tags, with formatting removed.\n\n" + \
               f"The document presents information about {document.title} in a web format.\n\n" + \
               f"This is the end of the mock HTML content."
    
    elif document.doc_type == DocumentType.FORM:
        return f"This is mock text from a form entry titled '{document.title}'.\n\n" + \
               f"It contains structured information entered through a form.\n\n" + \
               f"The form data includes details about {document.title}.\n\n" + \
               f"This is the end of the mock form content."
    
    else:
        return f"Unknown document type: {document.doc_type}. Unable to extract text."


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Chunk text into smaller pieces.
    
    Args:
        text: The text to chunk
        chunk_size: The maximum size of each chunk
        overlap: The overlap between chunks
        
    Returns:
        A list of text chunks
    """
    # For development, use a simple chunking strategy
    # In production, this will be replaced with more sophisticated chunking
    
    # If text is shorter than chunk_size, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]
    
    # Split text into paragraphs
    paragraphs = text.split("\n\n")
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed chunk_size, save the current chunk and start a new one
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(current_chunk)
            
            # Start new chunk with overlap
            words = current_chunk.split()
            overlap_words = min(len(words), overlap // 5)  # Approximate words in overlap
            current_chunk = " ".join(words[-overlap_words:]) if overlap_words > 0 else ""
            
            # Add a separator if there's overlap
            if current_chunk:
                current_chunk += "\n\n"
        
        # Add paragraph to current chunk
        if current_chunk and not current_chunk.endswith("\n\n"):
            current_chunk += "\n\n"
        current_chunk += paragraph
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


async def create_document(
    title: str,
    description: Optional[str],
    doc_type: DocumentType,
    source: DocumentSource,
    user_id: str,
    file_path: Optional[str] = None,
    url: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    db: Session = None,
) -> Tuple[bool, str]:
    """
    Create a new document.
    
    Args:
        title: Document title
        description: Document description
        doc_type: Document type
        source: Document source
        user_id: ID of the user creating the document
        file_path: Path to the document file (if applicable)
        url: URL of the document (if applicable)
        metadata: Additional metadata
        db: Database session
        
    Returns:
        A tuple of (success, document_id or error message)
    """
    try:
        # Create document
        document = Document(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            doc_type=doc_type,
            source=source,
            file_path=file_path,
            url=url,
            metadata=metadata or {},
            created_by=user_id,
            status=DocumentStatus.PENDING,
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Start processing in the background
        # In a real implementation, this would be a background task
        # For now, we'll just process it directly
        asyncio.create_task(process_document(document.id, db))
        
        return True, document.id
    
    except Exception as e:
        return False, str(e)