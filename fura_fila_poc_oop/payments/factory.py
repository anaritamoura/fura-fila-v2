from payments.pix import PagamentoPix
from payments.cartao import PagamentoCartao
from payments.dinheiro import PagamentoDinheiro
from payments.vale_refeicao import PagamentoValeRefeicao


# Associação entre o identificador recebido pela API e sua implementação.
# Para adicionar outro meio, crie uma classe e registre-a aqui.
MEIOS_PAGAMENTO = {
    "pix": PagamentoPix,
    "cartao": PagamentoCartao,
    "dinheiro": PagamentoDinheiro,
    "vale_refeicao": PagamentoValeRefeicao,
}


def obter_meio_pagamento(forma):
    classe_pagamento = MEIOS_PAGAMENTO.get(forma)

    if classe_pagamento is None:
        return None

    return classe_pagamento()
