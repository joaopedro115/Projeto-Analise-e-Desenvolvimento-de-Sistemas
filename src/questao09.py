import streamlit as st


# =========================
# CLASSES (OO)
# =========================

class Musico:
    def __init__(self, nome):
        self.nome = nome


class Musica:
    def __init__(self, nome, duracao):
        self.nome = nome
        self.duracao = duracao


class CD:
    def __init__(self, titulo, is_coletanea=False, is_duplo=False):
        self.titulo = titulo
        self.is_coletanea = is_coletanea
        self.is_duplo = is_duplo
        self.musicos = []
        self.musicas = []

    def adicionar_musico(self, musico):
        self.musicos.append(musico)

    def adicionar_musica(self, musica):
        self.musicas.append(musica)


class Catalogo:
    def __init__(self):
        self.cds = []
        self.musicos = []

    def adicionar_cd(self, cd):
        self.cds.append(cd)

    def adicionar_musico(self, musico):
        self.musicos.append(musico)

    def cds_por_musico(self, nome):
        return [
            cd for cd in self.cds
            if any(m.nome.lower() == nome.lower() for m in cd.musicos)
        ]

    def cds_por_musica(self, nome_musica):
        return [
            cd for cd in self.cds
            if any(m.nome.lower() == nome_musica.lower() for m in cd.musicas)
        ]


# =========================
# ESTADO
# =========================

if "catalogo" not in st.session_state:
    st.session_state.catalogo = Catalogo()


# =========================
# UI
# =========================

st.set_page_config(page_title="CDs Avançado", layout="wide")

st.title("Sistema - Coleção de CDs Avançado")


catalogo = st.session_state.catalogo


# =========================
# CADASTRO
# =========================

st.sidebar.header("Cadastro")

opcao = st.sidebar.selectbox(
    "O que cadastrar?",
    ["CD", "Músico", "Música em CD"]
)


# -------------------------
# CD
# -------------------------
if opcao == "CD":

    titulo = st.sidebar.text_input("Título do CD")
    coletanea = st.sidebar.checkbox("É coletânea?")
    duplo = st.sidebar.checkbox("É duplo?")

    if st.sidebar.button("Adicionar CD"):
        cd = CD(titulo, coletanea, duplo)
        catalogo.adicionar_cd(cd)
        st.success("CD cadastrado!")


# -------------------------
# MÚSICO
# -------------------------
elif opcao == "Músico":

    nome = st.sidebar.text_input("Nome do músico")

    if st.sidebar.button("Adicionar músico"):
        musico = Musico(nome)
        catalogo.adicionar_musico(musico)
        st.success("Músico cadastrado!")


# -------------------------
# MÚSICA EM CD
# -------------------------
elif opcao == "Música em CD":

    if catalogo.cds:

        cd_escolhido = st.sidebar.selectbox(
            "Escolha o CD",
            catalogo.cds,
            format_func=lambda c: c.titulo
        )

        nome_musica = st.sidebar.text_input("Nome da música")
        duracao = st.sidebar.number_input("Duração (min)", min_value=1)

        if st.sidebar.button("Adicionar música"):
            musica = Musica(nome_musica, duracao)
            cd_escolhido.adicionar_musica(musica)
            st.success("Música adicionada ao CD!")
    else:
        st.warning("Cadastre CDs primeiro.")


# =========================
# CONSULTAS
# =========================

st.subheader("Consultas")

consulta = st.selectbox(
    "Tipo de consulta",
    ["Todos os CDs", "CDs por músico", "CDs por música"]
)


# -------------------------
# TODOS
# -------------------------
if consulta == "Todos os CDs":

    if catalogo.cds:

        for cd in catalogo.cds:
            st.markdown(f"### {cd.titulo}")

            st.write("Coletânea:", cd.is_coletanea)
            st.write("Duplo:", cd.is_duplo)

            if cd.musicos:
                st.write("Músicos:", ", ".join(m.nome for m in cd.musicos))

            if cd.musicas:
                for m in cd.musicas:
                    st.write(f"- {m.nome} ({m.duracao} min)")

            st.divider()

    else:
        st.info("Nenhum CD cadastrado.")


# -------------------------
# POR MÚSICO
# -------------------------
elif consulta == "CDs por músico":

    nome = st.text_input("Nome do músico")

    if nome:
        resultados = catalogo.cds_por_musico(nome)

        if resultados:
            for cd in resultados:
                st.write(cd.titulo)
        else:
            st.warning("Nenhum CD encontrado.")


# -------------------------
# POR MÚSICA
# -------------------------
elif consulta == "CDs por música":

    musica = st.text_input("Nome da música")

    if musica:
        resultados = catalogo.cds_por_musica(musica)

        if resultados:
            for cd in resultados:
                st.write(cd.titulo)
        else:
            st.warning("Nenhum CD encontrado.")