def pode_visualizar(usuario, registro):
    nivel = usuario["level"]
    if nivel in [7, 8]:  # Todos
        return True
    if nivel in [5, 6] and usuario["empresa"] == registro["empresa"]:
        return True
    if nivel in [3, 4] and usuario["estado"] == registro["estado"]:
        return True
    if nivel in [1, 2] and usuario["username"] == registro["criado_por"]:
        return True
    return False

def pode_editar(usuario, registro):
    return usuario["level"] in [2, 4, 6, 8] and pode_visualizar(usuario, registro)