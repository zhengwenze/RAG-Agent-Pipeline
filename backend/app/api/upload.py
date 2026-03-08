from fastapi import APIRouter, UploadFile

from app.services.ingestion.doc_loader import split_text
from app.services.embedding.embeddings import embed_chunks
from app.services.vectorstore.vector_db import insert_vectors


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()
    chunks = split_text([content.decode()])
    vectors = embed_chunks(chunks)
    insert_vectors(vectors, [{"text": c} for c in chunks])
    return {"status": "success", "chunks": len(chunks)}

