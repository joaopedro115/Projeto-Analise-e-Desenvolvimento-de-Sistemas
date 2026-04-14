import streamlit as st
from datetime import datetime, timedelta


# =========================
# CLASSE PRINCIPAL
# =========================

class Tratamento:
    def __init__(self, nome_paciente, nome_remedio, dias, vezes_dia, data_inicio):
        self.nome_paciente = nome_paciente
        self.nome_remedio = nome_remedio
        self.dias = dias
        self.vezes_dia = vezes_dia
        self.data_inicio = data_inicio

    def gerar_horarios_dia(self):
        agora = datetime.now()
        intervalo = 24 // self.vezes_dia

        return [
            (agora + timedelta(hours=i * intervalo)).strftime("%H:%M")
            for i in range(self.vezes_dia)
        ]

    def data_fim_tratamento(self):
        return self.data_inicio + timedelta(days=self.dias)


# =========================
# ESTADO
# =========================

if "tratamentos" not in st.session_state:
    st.session_state.tratamentos = []


# =========================
# UI
# =========================

st.set_page_config(page_title="Remédios", layout="centered")

st.title("Sistema - Controle de Remédios")

st.sidebar.header("Cadastrar Tratamento")

nome_paciente = st.sidebar.text_input("Paciente")
nome_remedio = st.sidebar.text_input("Remédio")
dias = st.sidebar.number_input("Duração (dias)", min_value=1)
vezes = st.sidebar.number_input("Vezes ao dia", min_value=1)
data_inicio = st.sidebar.date_input("Data de início")


# =========================
# CADASTRO
# =========================

if st.sidebar.button("Salvar Tratamento"):

    tratamento = Tratamento(
        nome_paciente,
        nome_remedio,
        int(dias),
        int(vezes),
        data_inicio
    )

    st.session_state.tratamentos.append(tratamento)
    st.success("Tratamento cadastrado com sucesso!")


# =========================
# LISTAGEM
# =========================

st.subheader("Tratamentos cadastrados")

for t in st.session_state.tratamentos:

    st.markdown(f"### Paciente: {t.nome_paciente}")
    st.write(f"Remédio: {t.nome_remedio}")
    st.write(f"Duração: {t.dias} dias")
    st.write(f"Início: {t.data_inicio}")
    st.write(f"Término: {t.data_fim_tratamento().date()}")

    st.write("Horários sugeridos (hoje):")
    st.write(t.gerar_horarios_dia())

    st.divider()