from fastapi import APIRouter, UploadFile, File
from backend.config import UPLOAD_DIR
import shutil, os

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    from backend.pipeline.rag_pipeline import ingest_document
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    chunks = ingest_document(file_path)
    return {"filename": file.filename, "chunks_ingested": chunks}