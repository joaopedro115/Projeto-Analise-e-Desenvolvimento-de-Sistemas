import streamlit as st


# =========================
# CLASSE (OO)
# =========================

class Gasto:
    def __init__(self, tipo, valor, forma_pagamento):
        self.tipo = tipo
        self.valor = valor
        self.forma_pagamento = forma_pagamento


class RelatorioGastos:
    def __init__(self, gastos):
        self.gastos = gastos

    def total_geral(self):
        return sum(g.valor for g in self.gastos)

    def total_por_tipo(self):
        totais = {}
        for g in self.gastos:
            totais[g.tipo] = totais.get(g.tipo, 0) + g.valor
        return totais

    def total_por_pagamento(self):
        totais = {}
        for g in self.gastos:
            totais[g.forma_pagamento] = totais.get(g.forma_pagamento, 0) + g.valor
        return totais


# =========================
# ESTADO
# =========================

if "gastos" not in st.session_state:
    st.session_state.gastos = []


# =========================
# UI
# =========================

st.set_page_config(page_title="Gastos Diários", layout="wide")

st.title("Sistema - Controle de Gastos Diários")

st.sidebar.header("Novo Gasto")

tipo = st.sidebar.selectbox(
    "Tipo de gasto",
    ["Remédio", "Roupa", "Refeição", "Transporte", "Outros"]
)

valor = st.sidebar.number_input("Valor", min_value=0.0)

forma_pagamento = st.sidebar.selectbox(
    "Forma de pagamento",
    ["Dinheiro", "Cartão Crédito", "Cartão Débito", "Ticket Alimentação"]
)


# =========================
# CADASTRO
# =========================

if st.sidebar.button("Adicionar gasto"):
    gasto = Gasto(tipo, valor, forma_pagamento)
    st.session_state.gastos.append(gasto)
    st.success("Gasto adicionado!")


# =========================
# RELATÓRIO
# =========================

st.subheader("Resumo Financeiro")

rel = RelatorioGastos(st.session_state.gastos)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Geral", f"R$ {rel.total_geral():.2f}")

with col2:
    st.metric("Quantidade de registros", len(st.session_state.gastos))


# =========================
# DETALHES POR TIPO
# =========================

st.subheader("Total por Tipo de Gasto")

totais_tipo = rel.total_por_tipo()

if totais_tipo:
    for tipo, valor in totais_tipo.items():
        st.write(f"{tipo}: R$ {valor:.2f}")
else:
    st.info("Nenhum gasto registrado.")


# =========================
# DETALHES POR PAGAMENTO
# =========================

st.subheader("Total por Forma de Pagamento")

totais_pagamento = rel.total_por_pagamento()

if totais_pagamento:
    for forma, valor in totais_pagamento.items():
        st.write(f"{forma}: R$ {valor:.2f}")
else:
    st.info("Nenhum gasto registrado.")