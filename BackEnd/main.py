import pandas as pd
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

@app.post("/analisar")
def analisar_relatorio(request: ReportRequest):
    try:
        prompt = gerar_prompt(request.report)
        registros = analisar_com_gemini(prompt)
        return {"registros": registros}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def carregar_planilha(path="dados/esg_base.xlsx"):
    try: 
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    except Exception as e:
        return None
    