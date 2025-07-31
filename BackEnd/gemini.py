import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI")
if not API_KEY:
    raise RuntimeError("Variável de ambiente GEMINI não definida!")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def gerar_prompt(report: str, norm: str = None) -> str:
    return f"""
Leia atentamente o seguinte relatório de uma empresa:

{report}

Compare com as normas da área de GRC (Governança, Riscos e Compliance){f' e com a norma abaixo:\n{norm}' if norm else ''}.

Aponte todos os erros, falhas ou pontos críticos do relatório, e gere uma lista estruturada com os seguintes campos por item:

- Título do problema identificado
- Grau de risco: Alto (Danoso e Irreversível à natureza), Médio (Danoso mas Reversível à natureza), ou Baixo (Outros)
- Justificativa técnica: explique claramente por que esse erro foi detectado

❗ A saída deve seguir exatamente este formato (um item por linha):

TÍTULO ||| RISCO ||| DESCRIÇÃO

Não escreva nada fora desse padrão.
"""

def analisar_com_gemini(prompt: str):
    response = requests.post(
        GEMINI_URL,
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )

    if response.status_code != 200:
        raise Exception(f"Erro da API Gemini (status): {response.status_code}\nResposta: {response.text}")

    data = response.json()
    try:
        texto_ia = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise Exception("Resposta da API em formato inesperado")

    registros = []
    for linha in texto_ia.strip().split('\n'):
        partes = linha.split(' ||| ')
        if len(partes) == 3:
            titulo, risco, descricao = partes
            registros.append({
                "titulo": titulo.strip(),
                "risco": risco.strip(),
                "descricao": descricao.strip()
            })

    return registros
