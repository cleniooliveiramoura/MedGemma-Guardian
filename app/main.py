import os
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
try:
    from .engine import clinical_engine
except ImportError:
    from engine import clinical_engine

app = FastAPI(title="MedGemma Guardian API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClinicalAnalysisRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"status": "online", "model": clinical_engine.model_type}

@app.post("/analyze")
async def analyze_text(request: ClinicalAnalysisRequest):
    return await clinical_engine.analyze(request.text)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Somente arquivos PDF são permitidos.")
    
    try:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")
            
        return await clinical_engine.analyze(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
