import streamlit as st
import pandas as pd

import plotly.express as px
from random import choice, randint
from datetime import datetime, timedelta
from collections import Counter
from PIL import Image
import google.generativeai as genai
import os


# Dados

titulos = [
    "Descarte irregular de resíduos químicos",
    "Ausência de plano de contingência",
    "Falta de treinamento sobre ESG",
    "Uso indevido de recursos hídricos",
    "Emissão de gases sem controle",
    "Documentação ambiental vencida",
    "Instalações fora das normas ISO",
    "Falta de licenciamento adequado",
    "Depósito de materiais inflamáveis sem sinalização",
    "Manutenção preventiva negligenciada",
    "Armazenamento incorreto de resíduos",
    "Ruído excessivo nas operações",
    "Iluminação ineficiente em áreas críticas",
    "Transporte de resíduos sem rastreio",
    "Monitoramento ambiental ineficaz",
    "Falta de coleta seletiva no setor A",
    "Uso de substâncias tóxicas não permitidas",
    "EPI em falta para equipe noturna",
    "Sistema de exaustão com falha técnica",
    "Risco de contaminação do solo"
]

relatorios = ["Ponte São Valentim", "Praça São Luiz", "Shopping Campo Limpo"]

estados = ['Pendente', 'Em Processo', 'Concluído']

graus_risco = ["Alto", "Médio", "Baixo"]
encarregados = ["Ana Silva", "Bruno Costa", "Carlos Souza", "Diana Lopes", "Eduardo Lima", "Fernanda Rocha", " "]

explicacoes = {
    "Descarte irregular de resíduos químicos": 
        "Este problema é citado nas seções 3.2 e 5.1 do relatório de inspeção ambiental, "
        "onde se observa o descarte de solventes diretamente em rede pluvial. A prática infringe "
        "os artigos 54 e 60 da Lei nº 9.605/98 (Lei de Crimes Ambientais), além da resolução CONAMA nº 430/2011.",
    
    "Ausência de plano de contingência": 
        "Relatada na seção 4.3 do relatório. A ausência de plano para incidentes ambientais viola "
        "o Art. 225 da Constituição Federal e as exigências da Política Nacional de Segurança de Barragens (Lei nº 12.334/2010).",

    "Falta de treinamento sobre ESG": 
        "Mencionada na seção 2.1 e 6.4 do relatório de auditoria interna. Descumpre princípios da ISO 14001 "
        "e das diretrizes da GRI (Global Reporting Initiative), comprometendo a formação de equipes responsáveis.",

    "Uso indevido de recursos hídricos": 
        "Detectado nas seções 3.5 e 7.2 do relatório técnico. Viola a Resolução CONAMA nº 357/2005 e o Art. 12 da Lei nº 9.433/97 (Política Nacional de Recursos Hídricos).",

    "Emissão de gases sem controle": 
        "Citado na seção 5.3. Falta de filtros e medições em chaminés contraria a Resolução CONAMA nº 382/2006 e o licenciamento vigente.",

    "Documentação ambiental vencida": 
        "Consta nas seções 1.4 e 4.1 do relatório. Infringe o Art. 10 da Lei nº 6.938/81 por operar sem licença válida, "
        "podendo ser penalizado conforme o Decreto nº 6.514/2008.",

    "Instalações fora das normas ISO": 
        "Registrado na seção 2.5. Ambientes de armazenamento não seguem padrões da ISO 14001 e 45001, impactando segurança e meio ambiente.",

    "Falta de licenciamento adequado": 
        "Citado na seção 1.1. Empreendimento em operação sem licença ambiental prévia, infringe o Art. 60 da Lei nº 9.605/98 e o Art. 10 da Lei nº 6.938/81.",

    "Depósito de materiais inflamáveis sem sinalização": 
        "Seção 3.3 relata o depósito sem rótulos de risco ou sinalização visível. Contraria normas da NR 20 e da ABNT NBR 7500.",

    "Manutenção preventiva negligenciada": 
        "Relatada na seção 6.1. Falta de cronograma e execução de manutenções em equipamentos críticos. Pode violar a ISO 45001 e gerar risco operacional.",

    "Armazenamento incorreto de resíduos": 
        "Seções 2.3 e 4.6 indicam mistura de resíduos perigosos com comuns. Descumpre a NBR 10004 e a Resolução CONAMA nº 275.",

    "Ruído excessivo nas operações": 
        "Apontado na seção 5.6. Emissões sonoras acima de 85 dB, desrespeitando a NBR 10151 e normas da OMS.",

    "Iluminação ineficiente em áreas críticas": 
        "Seção 3.8 evidencia áreas operacionais com iluminação abaixo dos 100 lux recomendados. Infringe a NR 17 e compromete segurança do trabalho.",

    "Transporte de resíduos sem rastreio": 
        "Relatório (seção 4.9) mostra ausência de MTR (Manifesto de Transporte de Resíduos). Fere a Resolução CONAMA nº 452/2012.",

    "Monitoramento ambiental ineficaz": 
        "Seção 7.1 indica ausência de medições periódicas de efluentes. Descumpre condicionantes do licenciamento ambiental e da ISO 14001.",

    "Falta de coleta seletiva no setor A": 
        "Seção 2.7 relata descarte único de todos resíduos. Não atende à Política Nacional de Resíduos Sólidos (Lei nº 12.305/10).",

    "Uso de substâncias tóxicas não permitidas": 
        "Apontado na seção 6.3. Utilização de solventes proibidos pela ANVISA e que não constam no PPRA.",

    "EPI em falta para equipe noturna": 
        "Relatada na seção 3.6. Colaboradores sem óculos e luvas de proteção. Viola a NR 6 e pode configurar negligência da CIPA.",

    "Sistema de exaustão com falha técnica": 
        "Detectado na seção 5.5. Vazamentos e entupimentos nos dutos de exaustão. Infringe padrões da NBR 14518 e NR 15.",

    "Risco de contaminação do solo": 
        "Seções 3.1 e 6.8 apontam vazamentos contínuos de óleo e solventes próximos ao solo exposto. Viola a Resolução CONAMA nº 420/2009."
}


# Função para gerar datas
def gerar_datas():
    data_registro = datetime(2023, randint(1,12), randint(1,28))
    data_inicio = data_registro + timedelta(days=randint(1, 10))
    data_final = data_inicio + timedelta(days=randint(5, 30))
    return data_registro.date(), data_inicio.date(), data_final.date()
dados = []

for i in range(20):
    titulo = titulos[i % len(titulos)]
    estado = choice(estados)
    relatorio = choice(relatorios)
    risco = choice(graus_risco)
    encarregado = choice(encarregados)
    registro, inicio, final = gerar_datas()
    a, inicio_prev, final_prev = gerar_datas()
    dados.append({
        "Relatório" : relatorio,
        "Título": titulo,
        "Grau de Risco": risco,
        "Estado Atual": estado,
        "Encarregado": encarregado,
        "Data de Registro": registro,
        "Data de Início Prevista": inicio_prev,
        "Data de Finalização Prevista": final_prev,
        "Data de Início": inicio,
        "Data de Finalização": final
    })

# ---------------------------------

contagem = Counter(item["Grau de Risco"] for item in dados)


riscoAlto = contagem.get("Alto", 0)
riscoMedio = contagem.get("Médio", 0)
riscoBaixo= contagem.get("Baixo", 0)

contagem = Counter(item["Encarregado"] for item in dados)

ocioso = contagem.get(" ", 0)

contagem = Counter(item["Data de Finalização"] for item in dados)

emProcesso = 0
concluido = 0

for item in dados:
    if item["Data de Finalização"]: 
        concluido += 1
    else:
        emProcesso += 1


with open("resources\GRAUDERISCO.html", "r", encoding="utf-8") as f:
    html_content = f.read()

html_content = html_content.replace("{{riscoAlto}}", str(riscoAlto))
html_content = html_content.replace("{{riscoMedio}}", str(riscoMedio))
html_content = html_content.replace("{{riscoBaixo}}", str(riscoBaixo))
html_content = html_content.replace("{{ocioso}}", str(ocioso))
html_content = html_content.replace("{{emProcesso}}", str(emProcesso))
html_content = html_content.replace("{{concluido}}", str(concluido))

st.markdown(html_content, unsafe_allow_html=True)

data2 = {
    'Grau de Risco' : ['Alto','Médio', 'Baixo'],
    'Total' : [riscoAlto,riscoMedio, riscoBaixo]
}

data3 = {
    'Estado' : ['Pendente', 'Em Processo', 'Concluído'],
    'Total' : [ocioso, emProcesso, concluido]
}

col1, col2 = st.columns(2)

cores_personalizadas = {
    "Alto": "red",
    "Médio": "orange",
    "Baixo": "green"
}

fig_date = px.bar(data2, x = "Grau de Risco", y = "Total",color="Grau de Risco", title="Classificação de Risco Total", color_discrete_map=cores_personalizadas,category_orders={"Grau de Risco": ["Alto", "Médio", "Baixo"]})
col1.plotly_chart(fig_date)

image = Image.open("resources/Legenda.png")
col2.image(image, caption="Legenda", use_container_width=True)

df = pd.DataFrame(dados)

fig = px.bar(
    df, 
    x="Relatório", 
    color="Grau de Risco",
    title="Classificação de Riscos por Relatório",
    color_discrete_map=cores_personalizadas,
    category_orders={"Grau de Risco": ["Alto", "Médio", "Baixo"]},
    barmode="group"
)

st.plotly_chart(fig)

with open("resources\RESOLUCAO.html", "r", encoding="utf-8") as f:
    html_content2 = f.read()

html_content2 = html_content2.replace("{{ocioso}}", str(ocioso))
html_content2 = html_content2.replace("{{emProcesso}}", str(emProcesso))
html_content2 = html_content2.replace("{{concluido}}", str(concluido))

st.markdown(html_content2, unsafe_allow_html=True)

cores_personalizadas2 = {
    "Pendente": "blue",
    "Em Processo": "yellow",
    "Concluído": "green"
}
col3, col4 = st.columns(2)

fig_date2 = px.pie(data3, names = "Estado", color="Estado",values = "Total", color_discrete_map=cores_personalizadas2, title="Processo de Resolução das Falhas")

col3.plotly_chart(fig_date2)

fig2 = px.bar(
    df, 
    x="Estado Atual", 
    color="Grau de Risco",
    title="Classificação de Riscos por Estado Atual de Resolução de Falhas",
    color_discrete_map=cores_personalizadas,
    category_orders={"Grau de Risco": ["Alto", "Médio", "Baixo"]},
    barmode="group"
)

col4.plotly_chart(fig2)

# Suponha que você já tenha o df
df["Data de Registro"] = pd.to_datetime(df["Data de Registro"])
df["Data de Início Prevista"] = pd.to_datetime(df["Data de Início Prevista"])
df["Data de Finalização Prevista"] = pd.to_datetime(df["Data de Finalização Prevista"])
df["Data de Início"] = pd.to_datetime(df["Data de Início"])
df["Data de Finalização"] = pd.to_datetime(df["Data de Finalização"])

# Cria um novo DataFrame no formato longo
df_gantt = pd.concat([
    pd.DataFrame({
        "Título": df["Título"],
        "Encarregado": df["Encarregado"],
        "Início": df["Data de Início Prevista"],
        "Fim": df["Data de Finalização Prevista"],
        "Tipo": "Previsão",
        "Grau de Risco": df["Grau de Risco"]
    }),
    pd.DataFrame({
        "Título": df["Título"],
        "Encarregado": df["Encarregado"],
        "Início": df["Data de Início"],
        "Fim": df["Data de Finalização"],
        "Tipo": "Execução Real",
        "Grau de Risco": df["Grau de Risco"]
    })
])

# Remove tarefas incompletas (sem início ou fim)
df_gantt = df_gantt.dropna(subset=["Início", "Fim"])

# Gantt com barras separadas por tipo
figa = px.timeline(
    df_gantt,
    x_start="Início",
    x_end="Fim",
    y="Título",
    color="Tipo",
    title="Linha do Tempo: Previsão vs Execução",
    hover_data=["Grau de Risco"],
    color_discrete_map={
        "Previsão": "yellow",
        "Execução Real": "blue"
    }

)

figa.update_yaxes(autorange="reversed")

st.plotly_chart(figa, use_container_width=True)

st.dataframe(df) 

opcao = st.selectbox("Selecione um título", df["Título"])



if(opcao):
    # Configure sua API key
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY"))
    with st.expander("💬 Abrir Chat com a IA"):

        # Inicializa o modelo de chat
        model = genai.GenerativeModel("models/gemini-pro")

        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])

        # Título do app
        st.title("💬 Chat com GAIA")
        
        for msg in st.session_state.chat.history:
            with st.chat_message(msg.role):
                st.markdown(msg.parts[0].text)

        prompt = st.chat_input("Digite sua mensagem...")

        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            # with st.chat_message("assistant"):
                # response = st.session_state.chat.send_message(prompt)
                # st.markdown(response.text)