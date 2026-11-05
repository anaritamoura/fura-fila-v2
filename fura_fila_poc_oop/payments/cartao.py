from payments.base import MeioPagamento
from services.utilidades import formatar_moeda


class PagamentoCartao(MeioPagamento):
    def processar(self, pedido, dados):
        valor = pedido["total"]

        return {
            "ok": True,
            "mensagem": f"Cartão aprovado: {formatar_moeda(valor)}.",
            "pagamento": "Cartão",
            "valor_pago": valor,
            "troco": None
        }
