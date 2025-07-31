import os
import fitz 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gemini import gerar_prompt, analisar_com_gemini

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReportRequest(BaseModel):
    report: str
    norm: str = None  



@app.post("/analisar")
def analisar_relatorio(request: ReportRequest):
    try:
        # Se nenhuma norma for enviada, usa as carregadas da pasta
        norm_text = request.norm or "\n\n".join(normas_padrao)
        prompt = gerar_prompt(request.report, norm_text)
        registros = analisar_com_gemini(prompt)
        return {"registros": registros}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
