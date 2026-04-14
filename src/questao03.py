import streamlit as st
from enum import Enum


# =========================
# ENUM (DIREÇÃO)
# =========================

class Direcao(Enum):
    CIMA = "Cima"
    BAIXO = "Baixo"
    DIREITA = "Direita"
    ESQUERDA = "Esquerda"


# =========================
# CLASSE DO BONECO
# =========================

class Boneco:
    def __init__(self, nome, x=0, y=0):
        self.nome = nome
        self.x = x
        self.y = y
        self.direcao = Direcao.DIREITA

    def mover(self, direcao: Direcao):
        self.direcao = direcao

        if direcao == Direcao.CIMA:
            self.y += 1
        elif direcao == Direcao.BAIXO:
            self.y -= 1
        elif direcao == Direcao.DIREITA:
            self.x += 1
        elif direcao == Direcao.ESQUERDA:
            self.x -= 1

    def posicao(self):
        return self.x, self.y


# =========================
# ESTADO DA APLICAÇÃO
# =========================

if "boneco" not in st.session_state:
    st.session_state.boneco = Boneco("Heroi")


# =========================
# UI
# =========================

st.set_page_config(page_title="Boneco em Movimento", layout="centered")

st.title("Sistema - Boneco em Movimento")

boneco = st.session_state.boneco

st.subheader(f"Boneco: {boneco.nome}")

st.write(f"Posição atual: X = {boneco.x} | Y = {boneco.y}")
st.write(f"Direção atual: {boneco.direcao.value}")


# =========================
# CONTROLES
# =========================

st.subheader("Controles")

col1, col2, col3, col4 = st.columns(4)

if col1.button("⬆ Cima"):
    boneco.mover(Direcao.CIMA)

if col2.button("⬇ Baixo"):
    boneco.mover(Direcao.BAIXO)

if col3.button("➡ Direita"):
    boneco.mover(Direcao.DIREITA)

if col4.button("⬅ Esquerda"):
    boneco.mover(Direcao.ESQUERDA)


# =========================
# VISUALIZAÇÃO SIMPLES
# =========================

st.subheader("Mapa (Simples)")

grid_size = 10
grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

x = min(max(boneco.x + 5, 0), grid_size - 1)
y = min(max(5 - boneco.y, 0), grid_size - 1)

grid[y][x] = "B"

for row in grid:
    st.write(" ".join(row))