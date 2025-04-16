# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("banco.db")
    c = conn.cursor()
    # Tabela de processos
    c.execute("""
        CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            empresa TEXT,
            setor TEXT,
            estado TEXT,
            criado_por TEXT,
            responsavel TEXT,
            data_criacao TEXT
        )
    """)
    # Tabela de etapas
    c.execute("""
        CREATE TABLE IF NOT EXISTS etapas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processo_id INTEGER,
            nome_etapa TEXT,
            responsavel TEXT,
            data_inicio TEXT,
            data_fim TEXT,
            FOREIGN KEY (processo_id) REFERENCES processos(id)
        )
    """)
    conn.commit()
    conn.close()

def inserir_processo(processo, etapas):
    conn = sqlite3.connect("banco.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO processos (nome, empresa, setor, estado, criado_por, responsavel, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (processo["nome"], processo["empresa"], processo["setor"], processo["estado"],
          processo["criado_por"], processo["responsavel"], processo["data_criacao"]))
    processo_id = c.lastrowid

    for etapa in etapas:
        c.execute("""
            INSERT INTO etapas (processo_id, nome_etapa, responsavel, data_inicio, data_fim)
            VALUES (?, ?, ?, NULL, NULL)
        """, (processo_id, etapa["nome_etapa"], etapa["responsavel"]))
    conn.commit()
    conn.close()

def obter_processos_com_etapas():
    conn = sqlite3.connect("banco.db")
    c = conn.cursor()

    c.execute("SELECT * FROM processos")
    processos = c.fetchall()

    resultado = []
    for processo in processos:
        processo_id = processo[0]
        c.execute("SELECT nome_etapa, responsavel, data_inicio, data_fim FROM etapas WHERE processo_id = ?", (processo_id,))
        etapas = [{"nome_etapa": et[0], "responsavel": et[1], "data_inicio": et[2], "data_fim": et[3]} for et in c.fetchall()]
        resultado.append({
            "id": processo_id,
            "nome": processo[1],
            "empresa": processo[2],
            "setor": processo[3],
            "estado": processo[4],
            "criado_por": processo[5],
            "responsavel": processo[6],
            "data_criacao": processo[7],
            "etapas": etapas
        })

    conn.close()
    return resultado
