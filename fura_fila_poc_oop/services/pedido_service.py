from config import STATUS_AGUARDANDO_PAGAMENTO
from data.cardapio import CARDAPIO
from data import pedidos as armazenamento
from services.utilidades import converter_id


def buscar_pedido(pedido_id):
    return next(
        (pedido for pedido in armazenamento.PEDIDOS
         if pedido["id"] == pedido_id),
        None
    )


def buscar_item(item_id):
    return next(
        (item for item in CARDAPIO if item["id"] == item_id),
        None
    )


def criar_pedido(dados):
    nome_cliente = str(dados.get("cliente", "")).strip()

    if not nome_cliente:
        return {"erro": "Digite seu nome."}

    itens_escolhidos = dados.get("itens", [])
    if not isinstance(itens_escolhidos, list):
        return {"erro": "Lista de itens inválida."}

    itens_pedido = []
    total = 0

    for escolhido in itens_escolhidos:
        if not isinstance(escolhido, dict):
            return {"erro": "Dados dos itens inválidos."}

        item = buscar_item(converter_id(escolhido.get("id")))
        if item is None:
            return {"erro": "Item não existe."}

        try:
            quantidade = int(escolhido.get("qtd", 0))
        except (ValueError, TypeError):
            return {"erro": "Quantidade inválida."}

        if quantidade < 0:
            return {"erro": "A quantidade não pode ser negativa."}
        if quantidade == 0:
            continue

        itens_pedido.append({
            "nome": item["nome"],
            "preco": item["preco"],
            "qtd": quantidade
        })
        total += item["preco"] * quantidade

    if not itens_pedido:
        return {"erro": "Seu pedido está vazio."}

    pedido = {
        "id": armazenamento.PROXIMO_ID,
        "cliente": nome_cliente,
        "itens": itens_pedido,
        "total": round(total, 2),
        "status": STATUS_AGUARDANDO_PAGAMENTO,
        "pagamento": None,
        "valor_pago": None,
        "troco": None
    }

    armazenamento.PEDIDOS.append(pedido)
    armazenamento.PROXIMO_ID += 1
    return pedido
