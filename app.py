# app.py
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from database import init_db, inserir_processo, obter_processos_com_etapas
from datetime import datetime

# Inicializar banco de dados
init_db()

# Carregar configurações de usuários
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

usuarios = list(config["credentials"]["usernames"].keys())
usuario_selecionado = st.sidebar.selectbox("Selecione um usuário", usuarios)

if usuario_selecionado:
    user_data = config["credentials"]["usernames"][usuario_selecionado]
    user = {
        "username": usuario_selecionado,
        "level": user_data["level"],
        "estado": user_data["estado"],
        "empresa": user_data["empresa"]
    }

    st.sidebar.success(f"Bem-vindo, {user_data['name']}")

    st.title("📊 Visualização de Processos")

    with st.expander("➕ Criar novo processo"):
        with st.form("novo_processo"):
            nome_processo = st.text_input("Nome do Processo")
            qtd_etapas = st.number_input("Número de Etapas", min_value=1, step=1)
            empresa = st.text_input("Empresa", value=user["empresa"])
            setor = st.text_input("Setor")
            estado = st.text_input("Estado", value=user["estado"])
            criado_por = st.text_input("Criado por", value=user["username"])
            responsavel_processo = st.text_input("Responsável pelo Processo")
            data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.markdown("---")
            etapas = []
            for i in range(int(qtd_etapas)):
                col1, col2 = st.columns(2)
                with col1:
                    nome_etapa = st.text_input(f"Nome da Etapa {i+1}", key=f"nome_etapa_{i}")
                with col2:
                    responsavel = st.text_input(f"Responsável da Etapa {i+1}", key=f"responsavel_etapa_{i}")
                etapas.append({"nome_etapa": nome_etapa, "responsavel": responsavel})

            submitted = st.form_submit_button("Salvar")
            if submitted:
                dados_processo = {
                    "nome": nome_processo,
                    "empresa": empresa,
                    "setor": setor,
                    "estado": estado,
                    "criado_por": criado_por,
                    "responsavel": responsavel_processo,
                    "data_criacao": data_criacao
                }
                inserir_processo(dados_processo, etapas)
                st.success("✅ Processo salvo com sucesso!")

    st.markdown("---")
    st.subheader("🔍 Filtros")

    processos = obter_processos_com_etapas()
    nomes = sorted(set(p["nome"] for p in processos))
    empresas = sorted(set(p["empresa"] for p in processos))
    setores = sorted(set(p["setor"] for p in processos))
    estados = sorted(set(p["estado"] for p in processos))
    criadores = sorted(set(p["criado_por"] for p in processos))
    responsaveis = sorted(set(p["responsavel"] for p in processos))
    responsaveis_etapas = sorted(set(etapa["responsavel"] for p in processos for etapa in p["etapas"]))

    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_nome = st.selectbox("Nome do Processo", ["Todos"] + nomes)
    with col2:
        filtro_empresa = st.selectbox("Empresa", ["Todos"] + empresas)
    with col3:
        filtro_setor = st.selectbox("Setor", ["Todos"] + setores)

    col4, col5, col6 = st.columns(3)
    with col4:
        filtro_estado = st.selectbox("Estado", ["Todos"] + estados)
    with col5:
        filtro_criado_por = st.selectbox("Criado por", ["Todos"] + criadores)
    with col6:
        filtro_responsavel_processo = st.selectbox("Responsável pelo Processo", ["Todos"] + responsaveis)

    filtro_responsavel_etapa = st.selectbox("Responsável por Etapa", ["Todos"] + responsaveis_etapas)

    st.markdown("---")
    st.subheader("📌 Processos")

    for processo in processos:
        if (filtro_nome != "Todos" and processo["nome"] != filtro_nome): continue
        if (filtro_empresa != "Todos" and processo["empresa"] != filtro_empresa): continue
        if (filtro_setor != "Todos" and processo["setor"] != filtro_setor): continue
        if (filtro_estado != "Todos" and processo["estado"] != filtro_estado): continue
        if (filtro_criado_por != "Todos" and processo["criado_por"] != filtro_criado_por): continue
        if (filtro_responsavel_processo != "Todos" and processo["responsavel"] != filtro_responsavel_processo): continue
        if (filtro_responsavel_etapa != "Todos" and filtro_responsavel_etapa not in [et["responsavel"] for et in processo["etapas"]]): continue

        st.markdown(f"### 📝 {processo['nome']}")
        st.markdown(f"**Empresa:** {processo['empresa']} | **Setor:** {processo['setor']} | **Estado:** {processo['estado']} | **Criado por:** {processo['criado_por']} | **Responsável:** {processo['responsavel']}")

        etapa_cols = st.columns(len(processo["etapas"]))
        for i, etapa in enumerate(processo["etapas"]):
            cor = "#ffffff"  # Branco
            if etapa["data_fim"]:
                cor = "#32CD32"  # Verde
            elif etapa["data_inicio"]:
                cor = "#FFD700"  # Amarelo

            with etapa_cols[i]:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <div style='width:60px;height:60px;border-radius:30px;background-color:{cor};margin:auto;'></div>
                        <strong>{etapa['nome_etapa']}</strong><br>
                        <small>{etapa['responsavel']}</small>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
else:
    st.warning("Por favor, selecione um usuário.")