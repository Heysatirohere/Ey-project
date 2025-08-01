import streamlit as st
import fitz
import requests

st.title("Análise de Relatórios GRC com Normas")

uploaded_file = st.file_uploader("Envie o relatório para análise", type="pdf")

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
        st.warning("Envie um relatório PDF para análise.")
    else:
        report_text = extrair_texto_pdf(uploaded_file)

        with st.spinner("Analisando..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analisar",
                    json={"report": report_text}
                )
                if response.status_code == 200:
                    resultado = response.json().get("registros", [])
                    st.subheader("Resultado da Análise:")

                    for item in resultado:
                        st.markdown(f"### 🔍 {item['titulo']}")
                        st.markdown(f"**Grau de Risco:** {item['risco']}")
                        st.markdown(f"**Explicação:** {item['descricao']}")
                        st.markdown("---")
                else:
                    st.error(f"Erro: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erro ao se comunicar com o servidor: {e}")
