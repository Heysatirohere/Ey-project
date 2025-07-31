import streamlit as st
import fitz  # PyMuPDF
import requests

st.title("Análise de Relatórios GRC com Gemini")

# Upload do PDF
uploaded_file = st.file_uploader("Faça upload do relatório em PDF", type="pdf")
norm = st.text_area("Cole aqui normas ou diretrizes relevantes (opcional)", height=200)

def extrair_texto_pdf(file):
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        return texto.strip()
    except Exception as e:
        st.error(f"Erro ao ler o PDF: {e}")
        return ""

if st.button("Analisar"):
    if not uploaded_file:
        st.warning("Por favor, envie um PDF.")
    else:
        report_text = extrair_texto_pdf(uploaded_file)

        if not report_text:
            st.warning("Não foi possível extrair texto do PDF.")
        else:
            with st.spinner("Enviando para análise..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/analisar",  # ajuste se precisar
                        json={"report": report_text, "norm": norm}
                    )
                    if response.status_code == 200:
                        resultado = response.json().get("resultado", "")
                        st.subheader("Resultado da Análise:")
                        st.write(resultado)
                    else:
                        st.error(f"Erro: {response.status_code}\n{response.text}")
                except Exception as e:
                    st.error(f"Falha na requisição: {e}")
