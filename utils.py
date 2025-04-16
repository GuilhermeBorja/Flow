def pode_visualizar(usuario, processo):
    nivel = usuario["level"]
    if nivel in [7, 8]:  # Todos
        return True
    if nivel in [5, 6] and usuario["empresa"] == processo["empresa"]:
        return True
    if nivel in [3, 4] and usuario["estado"] == processo["estado"]:
        return True
    if nivel in [1, 2] and usuario["username"] == processo["criado_por"]:
        return True
    return False

def pode_editar(usuario, processo):
    return usuario["username"] == processo["criado_por"] or usuario["level"] >= 7
