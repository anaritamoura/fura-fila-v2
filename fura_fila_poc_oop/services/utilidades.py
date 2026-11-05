def converter_id(valor):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None


def formatar_moeda(valor):
    return f"R$ {valor:.2f}".replace(".", ",")
