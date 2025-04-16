import sqlite3

def init_db():
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            criado_por TEXT,
            estado TEXT,
            empresa TEXT,
            dado TEXT
        )
    """)
    conn.commit()
    conn.close()

def inserir_registro(usuario, dado):
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()
    c.execute("INSERT INTO registros (criado_por, estado, empresa, dado) VALUES (?, ?, ?, ?)",
              (usuario["username"], usuario["estado"], usuario["empresa"], dado))
    conn.commit()
    conn.close()

def apagar_registro(registro_id):
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()
    c.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
    conn.commit()
    conn.close()
def obter_registros():
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()
    c.execute("SELECT * FROM registros")
    data = c.fetchall()
    conn.close()
    return [{"id": row[0], "criado_por": row[1], "estado": row[2], "empresa": row[3], "dado": row[4]} for row in data]