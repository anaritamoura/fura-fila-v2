import os
import webbrowser
from http.server import HTTPServer

from config import HOST, PORTA_PADRAO
from routes.handler import Handler


def main():
    porta = int(os.environ.get("PORTA", PORTA_PADRAO))
    servidor = HTTPServer((HOST, porta), Handler)
    endereco = f"http://{HOST}:{porta}"

    print("=== FURA-FILA · Cantina CESAR ===")
    print(f"App rodando em {endereco} (Ctrl+C para parar)")

    if os.environ.get("SEM_NAVEGADOR") is None:
        webbrowser.open(endereco)

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\\nBom lanche!")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
