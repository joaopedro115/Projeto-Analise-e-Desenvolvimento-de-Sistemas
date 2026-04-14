import streamlit as st


# =========================
# CLASSES (OO)
# =========================

class Sala:
    def __init__(self, nome, capacidade):
        self.nome = nome
        self.capacidade = capacidade


class Reuniao:
    def __init__(self, sala, data, horario, assunto, funcionario):
        self.sala = sala
        self.data = data
        self.horario = horario
        self.assunto = assunto
        self.funcionario = funcionario


class Agenda:
    def __init__(self):
        self.salas = []
        self.reunioes = []

    def adicionar_sala(self, sala):
        self.salas.append(sala)

    def conflito(self, sala, data, horario):
        for r in self.reunioes:
            if r.sala.nome == sala.nome and r.data == data and r.horario == horario:
                return True
        return False

    def agendar(self, reuniao):
        if not self.conflito(reuniao.sala, reuniao.data, reuniao.horario):
            self.reunioes.append(reuniao)
            return True
        return False

    def por_sala(self, nome_sala):
        return [r for r in self.reunioes if r.sala.nome == nome_sala]

    def disponiveis(self, salas, data, horario):
        livres = []
        for s in salas:
            if not self.conflito(s, data, horario):
                livres.append(s)
        return livres


# =========================
# ESTADO
# =========================

if "agenda" not in st.session_state:
    st.session_state.agenda = Agenda()

agenda = st.session_state.agenda


# salas iniciais
if not agenda.salas:
    agenda.adicionar_sala(Sala("101", 10))
    agenda.adicionar_sala(Sala("105", 20))
    agenda.adicionar_sala(Sala("201", 15))


# =========================
# UI
# =========================

st.set_page_config(page_title="Sala de Reunião", layout="wide")

st.title("Sistema - Agenda de Salas de Reunião")


# =========================
# CADASTRO
# =========================

st.sidebar.header("Agendar Reunião")

sala_escolhida = st.sidebar.selectbox(
    "Sala",
    agenda.salas,
    format_func=lambda s: f"{s.nome} ({s.capacidade} lugares)"
)

data = st.sidebar.date_input("Data")
horario = st.sidebar.time_input("Horário")

assunto = st.sidebar.text_input("Assunto")
funcionario = st.sidebar.text_input("Funcionário")


if st.sidebar.button("Agendar"):

    reuniao = Reuniao(
        sala_escolhida,
        str(data),
        str(horario),
        assunto,
        funcionario
    )

    if agenda.agendar(reuniao):
        st.success("Reunião agendada com sucesso!")
    else:
        st.error("Conflito de horário! Sala já ocupada.")


# =========================
# CONSULTA
# =========================

st.subheader("Reuniões Agendadas")

if agenda.reunioes:

    for r in agenda.reunioes:
        st.markdown(f"### Sala {r.sala.nome}")
        st.write(f"Data: {r.data}")
        st.write(f"Horário: {r.horario}")
        st.write(f"Assunto: {r.assunto}")
        st.write(f"Funcionário: {r.funcionario}")
        st.divider()

else:
    st.info("Nenhuma reunião agendada.")


# =========================
# DISPONIBILIDADE
# =========================

st.subheader("Verificar Disponibilidade")

data_consulta = st.date_input("Data consulta", key="d2")
horario_consulta = st.time_input("Horário consulta", key="t2")

if st.button("Verificar salas livres"):

    livres = agenda.disponiveis(
        agenda.salas,
        str(data_consulta),
        str(horario_consulta)
    )

    if livres:
        st.success("Salas disponíveis:")

        for s in livres:
            st.write(f"{s.nome} ({s.capacidade})")
    else:
        st.warning("Nenhuma sala disponível nesse horário.")