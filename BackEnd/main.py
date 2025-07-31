import os
import fitz  # PyMuPDF
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


def carregar_normas_diretorio(diretorio: str):
    normas = []
    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.lower().endswith(".pdf"):
            caminho = os.path.join(diretorio, nome_arquivo)
            with fitz.open(caminho) as doc:
                texto = ""
                for pagina in doc:
                    texto += pagina.get_text()
                normas.append(texto)
    return normas


normas_padrao = carregar_normas_diretorio("normas")

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
