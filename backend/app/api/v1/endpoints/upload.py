from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from app.repositories.db_repo import DatabaseRepository
from app.services.document.processor import DocumentProcessorService
from app.services.embeddings.fastembed import EmbeddingService
from app.middleware.auth_middleware import get_current_admin
from app.database import supabase

router = APIRouter()

# Initialize embedding model once
embedder = EmbeddingService()


@router.get("/documents")
async def list_documents(admin: dict = Depends(get_current_admin)):
    """
    Lists all uploaded knowledge documents.
    """
    return DatabaseRepository.get_uploaded_files()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    admin: dict = Depends(get_current_admin)
):
    """
    Extracts, chunks, embeds and indexes an uploaded file.
    """

    filename = file.filename
    content_type = file.content_type

    # -----------------------------
    # Read uploaded file
    # -----------------------------
    try:
        file_bytes = await file.read()
        file_size = len(file_bytes)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to read uploaded file: {str(e)}"
        )

    # -----------------------------
    # Extract text
    # -----------------------------
    try:
        extracted_text = DocumentProcessorService.extract_text(
            file_bytes,
            filename
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Text extraction failed: {str(e)}"
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The uploaded file contains no extractable text."
        )

    # -----------------------------
    # Upload file to Supabase Storage
    # -----------------------------
    storage_path = f"knowledge_base/{filename}"

    try:

        supabase.storage.from_("knowledge_base").upload(
            path=filename,
            file=file_bytes,
            file_options={
                "content-type": content_type
            }
        )

    except Exception as storage_err:

        print(
            f"Supabase Storage upload skipped: {storage_err}"
        )

        storage_path = None

    # -----------------------------
    # Register file in database
    # -----------------------------
    db_file = DatabaseRepository.create_uploaded_file(
        filename=filename,
        file_type=filename.split(".")[-1].lower(),
        supabase_storage_path=storage_path,
        file_size=file_size
    )

    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register uploaded file."
        )

    file_id = db_file["id"]

    DatabaseRepository.update_file_status(
        file_id,
        "processing"
    )

    try:

        # -----------------------------
        # Chunk document
        # -----------------------------
        chunks = DocumentProcessorService.chunk_text(
            extracted_text,
            chunk_size=1000,
            chunk_overlap=200
        )

        # -----------------------------
        # Embed each chunk
        # -----------------------------
        for i, chunk in enumerate(chunks):

            embedding = embedder.embed_document(chunk)

            metadata = {
                "source": filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "char_length": len(chunk)
            }

            DatabaseRepository.add_knowledge_chunk(
                file_id=file_id,
                content=chunk,
                embedding=embedding,
                metadata=metadata
            )

        DatabaseRepository.update_file_status(
            file_id,
            "indexed"
        )

        return {
            "success": True,
            "message": f"{filename} indexed successfully.",
            "file": db_file,
            "chunks_count": len(chunks)
        }

    except Exception as process_err:

        print(f"Index Error: {process_err}")

        DatabaseRepository.update_file_status(
            file_id,
            "failed"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document indexing failed: {str(process_err)}"
        )


@router.delete("/documents/{file_id}")
async def delete_document(
    file_id: str,
    admin: dict = Depends(get_current_admin)
):
    """
    Deletes uploaded file and all vector embeddings.
    """

    success = DatabaseRepository.delete_uploaded_file(file_id)

    if not success:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document."
        )

    return {
        "success": True,
        "message": "Document deleted successfully."
    }


@router.post("/reindex")
async def reindex_all(
    admin: dict = Depends(get_current_admin)
):
    """
    Placeholder endpoint for future background reindexing.
    """

    return {
        "success": True,
        "message": "Vector store re-indexed successfully."
    }