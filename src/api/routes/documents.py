from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil

from src.database import get_db, User, Document, DocumentStatus, DocumentType, DocumentSource
from src.api.schemas.documents import (
    DocumentCreate, DocumentResponse, DocumentUpdate, 
    DocumentUploadResponse, DocumentProcessResponse
)
from src.api.routes.auth import get_current_active_user, get_current_admin_user
from src.document_processor.processor import process_document, create_document

# Router
router = APIRouter()


@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all documents."""
    query = db.query(Document)
    
    # Filter by status if provided
    if status:
        query = query.filter(Document.status == DocumentStatus(status))
    
    # Get documents
    documents = query.offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document_api(
    document_data: DocumentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new document (for manual entry or URL)."""
    # Validate document type
    if document_data.doc_type not in [
        DocumentType.FORM.value, 
        DocumentType.HTML.value,
        DocumentType.TEXT.value,
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document type for direct creation: {document_data.doc_type}",
        )
    
    # Validate source
    if document_data.source not in [
        DocumentSource.MANUAL.value, 
        DocumentSource.WEBSITE.value,
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document source for direct creation: {document_data.source}",
        )
    
    # Create document
    success, result = await create_document(
        title=document_data.title,
        description=document_data.description,
        doc_type=DocumentType(document_data.doc_type),
        source=DocumentSource(document_data.source),
        user_id=current_user.id,
        url=document_data.url,
        meta_data=document_data.metadata,
        db=db,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create document: {result}",
        )
    
    # Get the created document
    document = db.query(Document).filter(Document.id == result).first()
    return document


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Upload a document file."""
    # Determine document type from file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    doc_type = None
    if file_ext == ".pdf":
        doc_type = DocumentType.PDF
    elif file_ext == ".docx":
        doc_type = DocumentType.DOCX
    elif file_ext == ".md":
        doc_type = DocumentType.MARKDOWN
    elif file_ext == ".rst":
        doc_type = DocumentType.RST
    elif file_ext in [".txt", ".text"]:
        doc_type = DocumentType.TEXT
    elif file_ext in [".html", ".htm"]:
        doc_type = DocumentType.HTML
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_ext}",
        )
    
    # Create directory for uploaded files if it doesn't exist
    upload_dir = os.path.join("data", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save the uploaded file
    try:
        # Create a file in the upload directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    finally:
        file.file.close()
    
    # Create document in database
    success, result = await create_document(
        title=title,
        description=description,
        doc_type=doc_type,
        source=DocumentSource.UPLOAD,
        user_id=current_user.id,
        file_path=file_path,
        meta_data={"original_filename": file.filename},
        db=db,
    )
    
    if not success:
        # Clean up the file if document creation failed
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create document: {result}",
        )
    
    return {
        "id": result,
        "title": title,
        "file_name": file.filename,
        "doc_type": doc_type.value,
        "status": DocumentStatus.PENDING.value,
    }


@router.post("/{document_id}/process", response_model=DocumentProcessResponse)
async def process_document_api(
    document_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Process or reprocess a document (admin only)."""
    # Get the document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Start processing
    success = await process_document(document_id, db)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process document",
        )
    
    return {
        "id": document_id,
        "status": document.status.value,
        "message": "Document processing started",
    }


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    document_data: DocumentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a document."""
    # Get the document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Update fields
    if document_data.title is not None:
        document.title = document_data.title
    
    if document_data.description is not None:
        document.description = document_data.description
    
    if document_data.metadata is not None:
        document.meta_data = document_data.metadata
    
    db.commit()
    db.refresh(document)
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a document (admin only)."""
    # Get the document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Delete the file if it exists
    if document.file_path and os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            # Log the error but continue with deletion
            print(f"Error deleting file {document.file_path}: {str(e)}")
    
    # Delete embedding files if they exist
    embedding_dir = os.path.join("data", "embeddings", document_id)
    if os.path.exists(embedding_dir):
        try:
            shutil.rmtree(embedding_dir)
        except Exception as e:
            # Log the error but continue with deletion
            print(f"Error deleting embedding directory {embedding_dir}: {str(e)}")
    
    # Delete the document from the database
    db.delete(document)
    db.commit()
    
    return None


@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset_rag(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Reset the entire RAG system (admin only)."""
    # Get all documents
    documents = db.query(Document).all()
    
    # Delete all documents
    for document in documents:
        # Delete the file if it exists
        if document.file_path and os.path.exists(document.file_path):
            try:
                os.remove(document.file_path)
            except Exception as e:
                # Log the error but continue with deletion
                print(f"Error deleting file {document.file_path}: {str(e)}")
    
    # Delete all embedding files
    embedding_dir = os.path.join("data", "embeddings")
    if os.path.exists(embedding_dir):
        try:
            shutil.rmtree(embedding_dir)
            os.makedirs(embedding_dir, exist_ok=True)
        except Exception as e:
            # Log the error but continue with deletion
            print(f"Error resetting embedding directory {embedding_dir}: {str(e)}")
    
    # Delete all documents from the database
    db.query(Document).delete()
    db.commit()
    
    return {"message": "RAG system reset successfully"}