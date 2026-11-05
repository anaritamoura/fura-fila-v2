from payments.base import MeioPagamento
from services.utilidades import formatar_moeda


class PagamentoValeRefeicao(MeioPagamento):
    """
    Simulação de pagamento com vale-refeição.
    Nesta PoC, o vale cobre o valor total do pedido; não há integração
    com operadora nem consulta real de saldo.
    """

    def processar(self, pedido, dados):
        valor = pedido["total"]

        return {
            "ok": True,
            "mensagem": (
                f"Vale-refeição aprovado: {formatar_moeda(valor)}."
            ),
            "pagamento": "Vale-refeição",
            "valor_pago": valor,
            "troco": None
        }
