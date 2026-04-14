import streamlit as st


# =========================
# CLASSE (OO)
# =========================

class ItemCompra:
    def __init__(self, produto, unidade, qtd_planejada, qtd_comprada, preco):
        self.produto = produto
        self.unidade = unidade
        self.qtd_planejada = qtd_planejada
        self.qtd_comprada = qtd_comprada
        self.preco = preco

    def valor_planejado(self):
        return self.qtd_planejada * self.preco

    def valor_real(self):
        return self.qtd_comprada * self.preco

    def diferenca(self):
        return self.qtd_comprada - self.qtd_planejada


class ListaCompras:
    def __init__(self):
        self.itens = []

    def adicionar(self, item):
        self.itens.append(item)

    def total_planejado(self):
        return sum(i.valor_planejado() for i in self.itens)

    def total_real(self):
        return sum(i.valor_real() for i in self.itens)

    def saldo(self):
        return self.total_planejado() - self.total_real()


# =========================
# ESTADO
# =========================

if "lista" not in st.session_state:
    st.session_state.lista = ListaCompras()


# =========================
# UI
# =========================

st.set_page_config(page_title="Lista de Compras", layout="wide")

st.title("Sistema - Lista de Compras Mensal")


# =========================
# CADASTRO
# =========================

st.sidebar.header("Adicionar Produto")

produto = st.sidebar.text_input("Produto")

unidade = st.sidebar.selectbox(
    "Unidade",
    ["Kg", "L", "Unidade", "Pacote"]
)

qtd_planejada = st.sidebar.number_input("Qtd Planejada", min_value=0.0)
qtd_comprada = st.sidebar.number_input("Qtd Comprada", min_value=0.0)
preco = st.sidebar.number_input("Preço unitário", min_value=0.0)


if st.sidebar.button("Adicionar"):
    item = ItemCompra(produto, unidade, qtd_planejada, qtd_comprada, preco)
    st.session_state.lista.adicionar(item)
    st.success("Produto adicionado!")


# =========================
# LISTAGEM
# =========================

st.subheader("Itens da Lista")

if st.session_state.lista.itens:

    for i in st.session_state.lista.itens:
        st.write(
            f"{i.produto} | "
            f"Planejado: {i.qtd_planejada} | "
            f"Comprado: {i.qtd_comprada} | "
            f"Preço: R$ {i.preco:.2f}"
        )

        diff = i.diferenca()

        if diff > 0:
            st.write(f"Comprou a mais: +{diff}")
        elif diff < 0:
            st.write(f"Comprou a menos: {diff}")
        else:
            st.write("Compra exata")

        st.markdown("---")

else:
    st.info("Nenhum item cadastrado.")


# =========================
# RELATÓRIO
# =========================

st.subheader("Relatório Mensal")

lista = st.session_state.lista

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Planejado", f"R$ {lista.total_planejado():.2f}")

with col2:
    st.metric("Total Real", f"R$ {lista.total_real():.2f}")

with col3:
    saldo = lista.saldo()

    if saldo >= 0:
        st.metric("Economia", f"R$ {saldo:.2f}")
    else:
        st.metric("Excesso", f"R$ {abs(saldo):.2f}")