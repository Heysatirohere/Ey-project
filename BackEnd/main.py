import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

API_KEY = "AIzaSyD6FyfbYgr2IxVNec2RCx7DmJX5AMPm_Os"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

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
    norm: str = ""  

@app.post("/analisar")
def analisar_relatorio(request: ReportRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key não definida.")

    prompt = f"Leia atentamente o seguinte relatório de uma empresa:\n\n{request.report}\n\nCompare com as normas da área de GRC (Governança, Riscos e Compliance) e diga se há pontos de risco ou falhas. Cite os principais pontos que devem ser corrigidos."

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
