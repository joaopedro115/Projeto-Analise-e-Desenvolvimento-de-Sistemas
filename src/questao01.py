import streamlit as st
from datetime import date


# =========================
# MODELO (OO)
# =========================

class LeituraConta:
    def __init__(self, data, kw, valor):
        self.data = data
        self.kw = kw
        self.valor = valor


class RelatorioConsumo:
    def __init__(self, leituras):
        self.leituras = leituras

    def maior_consumo(self):
        return max(self.leituras, key=lambda x: x.kw)

    def menor_consumo(self):
        return min(self.leituras, key=lambda x: x.kw)

    def consumo_total(self):
        return sum(l.kw for l in self.leituras)

    def valor_total(self):
        return sum(l.valor for l in self.leituras)


# =========================
# BANCO EM MEMÓRIA
# =========================

if "leituras" not in st.session_state:
    st.session_state.leituras = []


# =========================
# UI
# =========================

st.set_page_config(page_title="Conta de Luz", layout="wide")

st.title("Controle de Conta de Luz")

menu = st.sidebar.selectbox(
    "Menu",
    ["Nova Leitura", "Histórico", "Relatório"]
)


# =========================
# CADASTRO
# =========================
if menu == "Nova Leitura":
    st.header("Registrar Leitura")

    data = st.date_input("Data da leitura")
    kw = st.number_input("Consumo (KW)", min_value=0.0)
    valor = st.number_input("Valor da conta", min_value=0.0)

    if st.button("Salvar leitura"):
        leitura = LeituraConta(data, kw, valor)
        st.session_state.leituras.append(leitura)
        st.success("Leitura registrada com sucesso!")


# =========================
# HISTÓRICO
# =========================
elif menu == "Histórico":
    st.header("Histórico de Leituras")

    if not st.session_state.leituras:
        st.warning("Nenhuma leitura cadastrada.")
    else:
        for l in st.session_state.leituras:
            st.write(f"Data: {l.data} | KW: {l.kw} | Valor: R$ {l.valor}")


# =========================
# RELATÓRIO
# =========================
elif menu == "Relatório":
    st.header("Relatório de Consumo")

    if len(st.session_state.leituras) < 1:
        st.warning("Cadastre leituras primeiro.")
    else:
        rel = RelatorioConsumo(st.session_state.leituras)

        maior = rel.maior_consumo()
        menor = rel.menor_consumo()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Maior consumo", f"{maior.kw} KW")

        with col2:
            st.metric("Menor consumo", f"{menor.kw} KW")

        with col3:
            st.metric("Total gasto", f"R$ {rel.valor_total():.2f}")

        st.subheader("Detalhes")
        st.write("Maior consumo em:", maior.data)
        st.write("Menor consumo em:", menor.data)