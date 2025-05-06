from fastapi import FastAPI, UploadFile, File, Query, Depends
import tempfile
from . import extractor
from auth import credits_guard

app = FastAPI(title="PDF-to-JSON Service")

@app.post("/convert",
          dependencies=[Depends(credits_guard)])
async def convert(
    file: UploadFile = File(...),
    ocr: bool = Query(False, description="Enable OCR fallback")
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp.flush()
        result = extractor.pdf_to_json(tmp.name, use_ocr=ocr)
    return result
