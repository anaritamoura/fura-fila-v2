from config import DESCONTO_PIX
from payments.base import MeioPagamento
from services.utilidades import formatar_moeda


class PagamentoPix(MeioPagamento):
    def processar(self, pedido, dados):
        valor = round(pedido["total"] * (1 - DESCONTO_PIX), 2)

        return {
            "ok": True,
            "mensagem": (
                f"Pix de {formatar_moeda(valor)} recebido "
                "(5% de desconto)."
            ),
            "pagamento": "Pix",
            "valor_pago": valor,
            "troco": None
        }
