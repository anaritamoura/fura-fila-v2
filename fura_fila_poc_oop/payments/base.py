from abc import ABC, abstractmethod


class MeioPagamento(ABC):
    """Contrato comum para todos os meios de pagamento."""

    @abstractmethod
    def processar(self, pedido, dados):
        """
        Processa o pagamento e retorna:
        {"ok": True, "mensagem": "...", "pagamento": "...",
         "valor_pago": float, "troco": float | None}
        ou {"erro": "..."}.
        """
        raise NotImplementedError
