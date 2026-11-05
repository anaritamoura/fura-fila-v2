from payments.base import MeioPagamento
from services.utilidades import formatar_moeda


class PagamentoDinheiro(MeioPagamento):
    def processar(self, pedido, dados):
        try:
            entregue = float(
                str(dados.get("entregue", "")).replace(",", ".")
            )
        except (ValueError, TypeError):
            return {"erro": "Valor inválido."}

        if entregue < pedido["total"]:
            return {"erro": "Dinheiro insuficiente."}

        troco = round(entregue - pedido["total"], 2)

        return {
            "ok": True,
            "mensagem": f"Pago em dinheiro. Troco: {formatar_moeda(troco)}.",
            "pagamento": "Dinheiro",
            "valor_pago": round(entregue, 2),
            "troco": troco
        }
