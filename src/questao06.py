import streamlit as st


# =========================
# CLASSES (OO)
# =========================

class Item:
    def __init__(self, produto, quantidade, preco_unitario):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def subtotal(self):
        return self.quantidade * self.preco_unitario


class Comanda:
    def __init__(self, numero):
        self.numero = numero
        self.itens = []
        self.finalizada = False

    def adicionar_item(self, item):
        if not self.finalizada:
            self.itens.append(item)

    def total(self):
        return sum(i.subtotal() for i in self.itens)

    def fechar(self):
        self.finalizada = True


# =========================
# ESTADO
# =========================

if "comandas" not in st.session_state:
    st.session_state.comandas = []

if "comanda_atual" not in st.session_state:
    st.session_state.comanda_atual = Comanda(1)


# =========================
# UI
# =========================

st.set_page_config(page_title="PDV - Comanda", layout="wide")

st.title("Sistema PDV - Comanda Eletrônica")

comanda = st.session_state.comanda_atual


# =========================
# CADASTRO DE ITENS
# =========================

st.sidebar.header("Adicionar Item")

produto = st.sidebar.text_input("Produto")
quantidade = st.sidebar.number_input("Quantidade", min_value=1)
preco = st.sidebar.number_input("Preço unitário", min_value=0.0)


if st.sidebar.button("Adicionar na comanda"):
    item = Item(produto, quantidade, preco)
    comanda.adicionar_item(item)
    st.success("Item adicionado!")


# =========================
# EXIBIÇÃO DA COMANDA
# =========================

st.subheader(f"Comanda Nº {comanda.numero}")

if comanda.itens:

    for i in comanda.itens:
        st.write(f"{i.produto} | Qtd: {i.quantidade} | Unit: R$ {i.preco_unitario:.2f} | Subtotal: R$ {i.subtotal():.2f}")

    st.markdown("---")
    st.metric("TOTAL", f"R$ {comanda.total():.2f}")

else:
    st.info("Nenhum item na comanda.")


# =========================
# FINALIZAR COMPRA
# =========================

st.subheader("Ações")

if st.button("Fechar comanda"):

    comanda.fechar()
    st.session_state.comandas.append(comanda)

    st.success(f"Comanda {comanda.numero} finalizada!")

    # cria nova comanda automaticamente
    st.session_state.comanda_atual = Comanda(comanda.numero + 1)


# =========================
# HISTÓRICO
# =========================

st.subheader("Histórico de Comandas")

for c in st.session_state.comandas:
    st.write(f"Comanda {c.numero} - Total: R$ {c.total():.2f} - Finalizada: {c.finalizada}")