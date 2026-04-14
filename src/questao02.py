import streamlit as st
from enum import Enum


# =========================
# ENUMS (TIPO E CORES)
# =========================

class TipoComponente(Enum):
    LABEL = "Label"
    EDIT = "Edit"
    MEMO = "Memo"


class CorFonte(Enum):
    PRETO = "black"
    BRANCO = "white"
    AZUL = "blue"
    AMARELO = "yellow"
    CINZA = "gray"


class CorFundo(Enum):
    PRETO = "black"
    BRANCO = "white"
    AZUL = "blue"
    AMARELO = "yellow"
    CINZA = "gray"


# =========================
# CLASSE PRINCIPAL
# =========================

class TextoSaida:
    def __init__(self, texto, tipo, cor_fonte, cor_fundo, tamanho):
        self.texto = texto
        self.tipo = tipo
        self.cor_fonte = cor_fonte
        self.cor_fundo = cor_fundo
        self.tamanho = tamanho

    def renderizar(self):
        return f"""
        <div style="
            background-color:{self.cor_fundo.value};
            color:{self.cor_fonte.value};
            padding:15px;
            font-size:{self.tamanho}px;
            border-radius:10px;
        ">
            {self.texto} ({self.tipo.value})
        </div>
        """


# =========================
# UI
# =========================

st.set_page_config(page_title="TextoSaída", layout="centered")

st.title("Sistema - Texto Saída")

st.sidebar.header("Configuração do Texto")


texto = st.sidebar.text_input("Texto")

tipo = st.sidebar.selectbox(
    "Tipo de componente",
    list(TipoComponente)
)

cor_fonte = st.sidebar.selectbox(
    "Cor da fonte",
    list(CorFonte)
)

cor_fundo = st.sidebar.selectbox(
    "Cor do fundo",
    list(CorFundo)
)

tamanho = st.sidebar.slider("Tamanho da fonte", 12, 40, 18)


# =========================
# GERAR COMPONENTE
# =========================

if st.sidebar.button("Gerar Texto"):

    componente = TextoSaida(
        texto,
        tipo,
        cor_fonte,
        cor_fundo,
        tamanho
    )

    st.subheader("Preview")

    st.markdown(componente.renderizar(), unsafe_allow_html=True)