import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from data.cardapio import CARDAPIO
from data import pedidos as armazenamento
from services.pedido_service import buscar_pedido, criar_pedido
from services.pagamento_service import pagar, marcar_pronto
from services.utilidades import converter_id


class Handler(BaseHTTPRequestHandler):
    def responder(self, dados, codigo=200, tipo="application/json"):
        if isinstance(dados, bytes):
            corpo = dados
        else:
            corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")

        self.send_response(codigo)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def ler_json(self):
        tamanho = int(self.headers.get("Content-Length", 0))

        try:
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

        return dados if isinstance(dados, dict) else None

    def do_GET(self):
        url = urlparse(self.path)
        caminho = url.path

        if caminho in ("/", "/index.html"):
            pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_html = os.path.join(pasta_raiz, "index.html")

            try:
                with open(caminho_html, "rb") as arquivo:
                    self.responder(arquivo.read(), tipo="text/html")
            except FileNotFoundError:
                self.responder({"erro": "Arquivo index.html não encontrado."}, 404)

        elif caminho == "/api/cardapio":
            self.responder(CARDAPIO)

        elif caminho == "/api/pedidos":
            self.responder(armazenamento.PEDIDOS)

        elif caminho == "/api/pedido":
            parametros = parse_qs(url.query)
            pedido_id = converter_id(parametros.get("id", [None])[0])
            pedido = buscar_pedido(pedido_id)

            if pedido is None:
                self.responder({"erro": "Pedido não encontrado."}, 404)
            else:
                self.responder(pedido)

        else:
            self.responder({"erro": "Página não encontrada."}, 404)

    def do_POST(self):
        dados = self.ler_json()

        if dados is None:
            self.responder({"erro": "Dados inválidos."}, 400)
            return

        rotas = {
            "/api/pedido": criar_pedido,
            "/api/pagar": pagar,
            "/api/pronto": marcar_pronto
        }

        caminho = urlparse(self.path).path
        funcao = rotas.get(caminho)

        if funcao is None:
            self.responder({"erro": "Página não encontrada."}, 404)
            return

        resultado = funcao(dados)
        codigo = 400 if "erro" in resultado else 200
        self.responder(resultado, codigo)

    def log_message(self, *args):
        pass
