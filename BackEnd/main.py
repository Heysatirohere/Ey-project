import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Utilitários
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("GEMINI")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Função para carregar normas base salvas em arquivos
BASE_DOCS_DIR = "docs"

def carregar_norma(nome_arquivo):
    caminho = Path(BASE_DOCS_DIR) / nome_arquivo
    if not caminho.exists():
        raise FileNotFoundError(f"Norma '{nome_arquivo}' não encontrada.")
    return caminho.read_text(encoding="utf-8")

# Inicializa o app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReportRequest(BaseModel):
    report: str
    norm_file: str = ""  # nome do arquivo da norma (ex: norma_ABNT.txt)

@app.post("/analisar")
def analisar_relatorio(request: ReportRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key não definida.")

    try:
        norma = carregar_norma(request.norm_file) if request.norm_file else ""
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    prompt = f"""
Você é um especialista em GRC (Governança, Riscos e Compliance). Analise o relatório abaixo com base na norma técnica fornecida.

Norma técnica:
{norma}

Relatório da empresa:
{request.report}

Com base nisso, aponte falhas, inconsistências ou riscos. Dê sugestões de melhoria ou adequações.
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_URL, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Erro da API Gemini (status): {response.status_code}\nResposta: {response.text}")

    data = response.json()
    try:
        output = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"resultado": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar resposta da API: {e}")
