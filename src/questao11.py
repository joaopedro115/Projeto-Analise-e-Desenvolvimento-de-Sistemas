import streamlit as st
from datetime import date


# =========================
# CLASSE BASE (HERANÇA)
# =========================

class Pessoa:
    def __init__(self, nome, data_nascimento, endereco, telefones=None):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefones = telefones if telefones else []

    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) <
            (self.data_nascimento.month, self.data_nascimento.day)
        )


# =========================
# CLASSES AUXILIARES
# =========================

class Endereco:
    def __init__(self, rua, bairro, cidade):
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade


class Telefone:
    def __init__(self, numero):
        self.numero = numero


class Cargo:
    def __init__(self, nome, salario_base):
        self.nome = nome
        self.salario_base = salario_base


class Profissao:
    def __init__(self, nome):
        self.nome = nome


# =========================
# HERANÇA
# =========================

class Cliente(Pessoa):
    def __init__(self, nome, data_nascimento, endereco, profissao):
        super().__init__(nome, data_nascimento, endereco)
        self.profissao = profissao


class Funcionario(Pessoa):
    def __init__(self, nome, data_nascimento, endereco, cargo):
        super().__init__(nome, data_nascimento, endereco)
        self.cargo = cargo
        self.salario = cargo.salario_base

    def reajustar(self, percentual):
        self.salario += self.salario * (percentual / 100)

    def promover(self, novo_cargo):
        self.cargo = novo_cargo
        self.salario = novo_cargo.salario_base


# =========================
# ESTADO
# =========================

if "clientes" not in st.session_state:
    st.session_state.clientes = []

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = []


# =========================
# UI
# =========================

st.set_page_config(page_title="Sistema Herança", layout="wide")

st.title("Sistema - Herança (Pessoa, Cliente e Funcionário)")


menu = st.sidebar.selectbox(
    "Menu",
    ["Cadastrar Cliente", "Cadastrar Funcionário", "Listar Pessoas"]
)


# =========================
# CLIENTE
# =========================
if menu == "Cadastrar Cliente":

    st.header("Cadastro de Cliente")

    nome = st.text_input("Nome")
    nascimento = st.date_input("Data de nascimento")

    rua = st.text_input("Rua")
    bairro = st.text_input("Bairro")
    cidade = st.text_input("Cidade")

    profissao = st.text_input("Profissão")

    if st.button("Salvar Cliente"):

        endereco = Endereco(rua, bairro, cidade)
        prof = Profissao(profissao)

        cliente = Cliente(nome, nascimento, endereco, prof)

        st.session_state.clientes.append(cliente)

        st.success("Cliente cadastrado!")


# =========================
# FUNCIONÁRIO
# =========================
elif menu == "Cadastrar Funcionário":

    st.header("Cadastro de Funcionário")

    nome = st.text_input("Nome")
    nascimento = st.date_input("Data de nascimento")

    rua = st.text_input("Rua")
    bairro = st.text_input("Bairro")
    cidade = st.text_input("Cidade")

    cargo_nome = st.text_input("Cargo")
    salario = st.number_input("Salário base", min_value=0.0)

    if st.button("Salvar Funcionário"):

        endereco = Endereco(rua, bairro, cidade)
        cargo = Cargo(cargo_nome, salario)

        funcionario = Funcionario(nome, nascimento, endereco, cargo)

        st.session_state.funcionarios.append(funcionario)

        st.success("Funcionário cadastrado!")


# =========================
# LISTAGEM
# =========================
elif menu == "Listar Pessoas":

    st.subheader("Clientes")

    if st.session_state.clientes:
        for c in st.session_state.clientes:
            st.write(f"{c.nome} - {c.profissao.nome} - {c.idade()} anos")
    else:
        st.info("Nenhum cliente cadastrado.")

    st.subheader("Funcionários")

    if st.session_state.funcionarios:
        for f in st.session_state.funcionarios:
            st.write(
                f"{f.nome} - {f.cargo.nome} - "
                f"R$ {f.salario:.2f} - {f.idade()} anos"
            )
    else:
        st.info("Nenhum funcionário cadastrado.")