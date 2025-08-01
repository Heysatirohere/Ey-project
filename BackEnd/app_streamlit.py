import streamlit as st
import fitz  # PyMuPDF
import requests

# Configuração da página
st.set_page_config(
    page_title="Chat ESG - Análise GRC",
    layout="centered",
    page_icon="💬"
)

# Título com estilo
st.markdown("<h1 style='text-align: center;'>💬 Chat ESG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Análise de Relatórios com OCPC-09, GRI, IFRS S1 e S2</p>", unsafe_allow_html=True)
st.divider()

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "content": "👋 Olá! Sou o assistente ESG. Envie um relatório em PDF ou me pergunte algo sobre GRI, OCPC-09, IFRS S1 e S2."
        }
    ]

# Mostrar mensagens anteriores com estilo
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Função para extrair texto do PDF
def extrair_texto_pdf(file):
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            texto = "".join([page.get_text() for page in doc])
        return texto.strip()
    except Exception as e:
        return f"Erro ao ler PDF: {e}"

# Bloco de upload
with st.expander("📁 Enviar relatório em PDF para análise"):
    uploaded_file = st.file_uploader("Selecione o arquivo PDF", type=["pdf"])

# Campo de entrada de mensagem
user_input = st.chat_input("Digite sua pergunta ou envie um PDF para análise...")

# Se o usuário enviou mensagem ou PDF
if user_input or uploaded_file:

    # PDF enviado
    if uploaded_file:
        user_msg = "📎 Enviado relatório para análise."
        st.chat_message("user").markdown(user_msg)
        st.session_state.messages.append({"role": "user", "content": user_msg})

        with st.chat_message("ai"):
            with st.spinner("🧠 Analisando seu relatório..."):
                texto_pdf = extrair_texto_pdf(uploaded_file)

                if not texto_pdf:
                    resposta = "❌ Não consegui extrair o texto do PDF. Verifique se ele está legível."
                else:
                    try:
                        response = requests.post("http://localhost:8000/analisar", json={"report": texto_pdf})
                        if response.status_code == 200:
                            registros = response.json().get("registros", [])
                            if registros:
                                resposta = "✅ **Análise do relatório:**\n\n"
                                for item in registros:
                                    resposta += f"""
🔍 **{item['titulo']}**  
- 🟠 Grau de Risco: **{item['risco']}**  
- 📄 {item['descricao']}\n\n"""
                            else:
                                resposta = "✅ Nenhum risco relevante foi identificado no relatório enviado. 🎯"
                        else:
                            resposta = f"❌ Erro na API: {response.status_code} - {response.text}"
                    except Exception as e:
                        resposta = f"❌ Erro ao conectar com a API: {e}"

            st.markdown(resposta)
            st.session_state.messages.append({"role": "ai", "content": resposta})

    # Entrada de texto (mensagem do usuário)
    elif user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Aqui é onde você integra com sua IA (por enquanto, resposta estática)
        resposta = "🤖 No momento, só consigo analisar PDFs. Mas em breve poderei responder suas perguntas diretamente!"
        st.chat_message("ai").markdown(resposta)
        st.session_state.messages.append({"role": "ai", "content": resposta})
