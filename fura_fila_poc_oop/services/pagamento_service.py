from config import (
    STATUS_AGUARDANDO_PAGAMENTO,
    STATUS_EM_PREPARO,
    STATUS_PRONTO
)
from data import pedidos as armazenamento
from payments.factory import obter_meio_pagamento
from services.pedido_service import buscar_pedido
from services.utilidades import converter_id


def pagar(dados):
    """Coordena o pagamento sem conhecer as regras de cada modalidade."""
    pedido_id = converter_id(dados.get("id"))
    pedido = buscar_pedido(pedido_id)

    if pedido is None:
        return {"erro": "Pedido não encontrado."}

    if pedido["status"] != STATUS_AGUARDANDO_PAGAMENTO:
        return {"erro": "Esse pedido já foi pago."}

    meio_pagamento = obter_meio_pagamento(dados.get("forma"))
    if meio_pagamento is None:
        return {"erro": "Forma de pagamento inválida."}

    resultado = meio_pagamento.processar(pedido, dados)
    if "erro" in resultado:
        return resultado

    pedido["pagamento"] = resultado["pagamento"]
    pedido["valor_pago"] = resultado["valor_pago"]
    pedido["troco"] = resultado["troco"]
    pedido["status"] = STATUS_EM_PREPARO

    return {
        "ok": True,
        "mensagem": resultado["mensagem"],
        "pedido": pedido
    }


def marcar_pronto(dados):
    pedido_id = converter_id(dados.get("id"))
    pedido = buscar_pedido(pedido_id)

    if pedido is None:
        return {"erro": "Pedido não encontrado."}

    if pedido["status"] != STATUS_EM_PREPARO:
        return {"erro": "Esse pedido não está em preparo."}

    pedido["status"] = STATUS_PRONTO
    return {"ok": True, "pedido": pedido}
