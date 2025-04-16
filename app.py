import streamlit as st
import yaml
from yaml.loader import SafeLoader
from database import init_db, inserir_registro, obter_registros, apagar_registro
from utils import pode_visualizar, pode_editar

# Inicializar banco
init_db()

# Carregar config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Criar lista de nomes de usuários a partir dos dados do config.yaml
usuarios = list(config["credentials"]["usernames"].keys())  # Lista de todos os usernames cadastrados

# Seletor de usuário
usuario_selecionado = st.selectbox("Selecione um usuário", usuarios)

if usuario_selecionado:
    st.sidebar.success(f"Bem-vindo, {config['credentials']['usernames'][usuario_selecionado]['name']}")

    # Obtendo os dados do usuário selecionado
    user_data = config["credentials"]["usernames"][usuario_selecionado]
    user = {
        "username": usuario_selecionado,
        "level": user_data["level"],
        "estado": user_data["estado"],
        "empresa": user_data["empresa"]
    }

    # Formulário para criar um novo processo
    st.header("📋 Criar novo Processo")
    with st.form("formulario"):
        # Campos separados
        nome_processo = st.text_input("Nome do Processo:")
        qtd_etapas = st.number_input("Quantidade de Etapas", min_value=1, step=1)
        empresa = st.text_input("Empresa:", value=user["empresa"])  # Preenche com a empresa do usuário
        setor = st.text_input("Setor:")
        responsavel = st.text_input("Nome do Responsável pelo processo:")

        enviado = st.form_submit_button("Salvar")
        if enviado:
            # Salvar o novo processo no banco
            dado = f"Nome: {nome_processo}, Etapas: {qtd_etapas}, Empresa: {empresa}, Setor: {setor}, Responsável: {responsavel}"
            inserir_registro(user, dado)
            st.success("Processo salvo com sucesso!")

    # Exibição dos dados permitidos
    st.header("📄 Processos disponíveis")
    registros = obter_registros()
    for r in registros:
        if pode_visualizar(user, r):
            st.write(f"ID: {r['id']} | Criado por: {r['criado_por']} | Estado: {r['estado']} | Empresa: {r['empresa']}")
            st.write(f"Dado: {r['dado']}")

            if pode_editar(user, r):
                novo_dado = st.text_input(f"Editar dado {r['id']}", value=r['dado'], key=r['id'])
                if st.button(f"Salvar", key=f"save_{r['id']}"):  # Removido número da numeração
                    st.warning("Função de edição ainda não implementada.")

                # Adicionando o botão de "Apagar" ao lado do "Salvar"
                if st.button(f"Apagar", key=f"delete_{r['id']}"):
                    apagar_registro(r['id'])
                    st.success(f"Processo {r['id']} apagado com sucesso.")

            st.markdown("---")
else:
    st.warning("Por favor, selecione um usuário.")
