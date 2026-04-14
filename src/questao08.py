import streamlit as st


# =========================
# CLASSES (OO)
# =========================

class CD:
    def __init__(self, titulo, artista, ano):
        self.titulo = titulo
        self.artista = artista
        self.ano = ano


class ColecaoCD:
    def __init__(self):
        self.cds = []

    def adicionar(self, cd):
        self.cds.append(cd)

    def listar_por_artista(self, artista):
        return [cd for cd in self.cds if cd.artista.lower() == artista.lower()]

    def listar_por_ano(self, ano):
        return [cd for cd in self.cds if cd.ano == ano]


# =========================
# ESTADO
# =========================

if "colecao" not in st.session_state:
    st.session_state.colecao = ColecaoCD()


# =========================
# UI
# =========================

st.set_page_config(page_title="Coleção de CDs", layout="wide")

st.title("Sistema - Coleção de CDs")


# =========================
# CADASTRO
# =========================

st.sidebar.header("Adicionar CD")

titulo = st.sidebar.text_input("Título do CD")
artista = st.sidebar.text_input("Artista")
ano = st.sidebar.number_input("Ano de lançamento", min_value=1900, max_value=2100)


if st.sidebar.button("Adicionar CD"):
    cd = CD(titulo, artista, ano)
    st.session_state.colecao.adicionar(cd)
    st.success("CD adicionado!")


# =========================
# CONSULTA
# =========================

st.subheader("Consulta")

filtro = st.selectbox(
    "Filtrar por",
    ["Todos", "Artista", "Ano"]
)

colecao = st.session_state.colecao


if filtro == "Todos":

    if colecao.cds:
        for cd in colecao.cds:
            st.write(f"{cd.titulo} - {cd.artista} ({cd.ano})")
    else:
        st.info("Nenhum CD cadastrado.")


elif filtro == "Artista":

    artista_busca = st.text_input("Nome do artista")

    if artista_busca:
        resultados = colecao.listar_por_artista(artista_busca)

        if resultados:
            for cd in resultados:
                st.write(f"{cd.titulo} - {cd.artista} ({cd.ano})")
        else:
            st.warning("Nenhum CD encontrado para este artista.")


elif filtro == "Ano":

    ano_busca = st.number_input("Ano", min_value=1900, max_value=2100)

    if ano_busca:
        resultados = colecao.listar_por_ano(int(ano_busca))

        if resultados:
            for cd in resultados:
                st.write(f"{cd.titulo} - {cd.artista} ({cd.ano})")
        else:
            st.warning("Nenhum CD encontrado nesse ano.")