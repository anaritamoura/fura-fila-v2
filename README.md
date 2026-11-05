# Fura-Fila (PoC final)

<p align="center">
  <img src="./assets/images/logo-fura-fila.png" alt="Logo do Fura-Fila" width="300">
</p>

**O app da cantina do CESAR para o aluno não perder o intervalo na fila.**

Hackathon Relâmpago #1 de FDS 2026.2 (CESAR School), Entrega 2.

## O que é o app

O Fura-Fila é um app para a cantina do CESAR. O aluno faz o pedido e paga pelo app antes do intervalo. A cantina marca o pedido como pronto, e o aluno só vai ao balcão para retirar o lanche, sem pegar fila.

Telas:
- **Cardápio:** o aluno escolhe os itens e as quantidades e vê o total.
- **Pagamento:** Pix (5% de desconto), cartão, dinheiro (com cálculo de troco) ou vale-refeição.
- **Meu pedido:** acompanha o status (pedido feito → em preparo → pronto) e recebe o aviso com a senha.
- **Cantina:** painel com os pedidos pagos, onde a cantina marca o pedido como pronto.

É uma prova de conceito: os dados ficam em memória, sem banco de dados. Os pagamentos também são simulados, sem integração com instituições financeiras ou operadoras de vale-refeição.

## Como rodar

Precisa só de Python 3. Não tem nada para instalar.

```bash
python main.py
```

O app abre sozinho no navegador em `http://localhost:8000`. Se não abrir, acesse esse endereço manualmente.

Para testar o fluxo inteiro: faça um pedido na aba **Cardápio**, escolha uma forma de pagamento, vá na aba **Cantina** e clique em **Pronto ✓**. Depois volte em **Meu pedido** para ver o aviso.

Para testar o vale-refeição, selecione essa modalidade na interface. O backend recebe a opção `vale_refeicao`.

## Decisões da stack

- **Python (só biblioteca padrão):** a equipe já teve contato com a linguagem, e ela oferece classes abstratas para representar o contrato comum dos meios de pagamento. O servidor usa `http.server`, então ninguém precisa instalar nada.
- **Tela em HTML, CSS e JavaScript (`index.html`):** visual de app de celular, que roda em qualquer navegador.
- **Dados em memória:** listas e dicionários bastam para a prova de conceito.

## Organização do código

fura_fila_poc_oop/
│
├── main.py
├── config.py
├── index.html
│
├── assets/
│   └── images/
│       └── logo-fura-fila.png
│
├── data/
│   ├── __init__.py
│   ├── cardapio.py
│   └── pedidos.py
│
├── services/
│   ├── __init__.py
│   ├── pedido_service.py
│   ├── pagamento_service.py
│   └── utilidades.py
│
├── payments/
│   ├── __init__.py
│   ├── base.py
│   ├── pix.py
│   ├── cartao.py
│   ├── dinheiro.py
│   ├── vale_refeicao.py
│   └── factory.py
│
└── routes/
    ├── __init__.py
    └── handler.py

- **`main.py`:** inicializa o servidor HTTP.
- **`config.py`:** reúne configurações, desconto e status dos pedidos.
- **`assets/`:** armazena os recursos visuais do projeto, incluindo a logo em assets/images/.
- **`data/`:** contém o cardápio e o armazenamento temporário dos pedidos.
- **`services/`:** concentra as regras de negócio de pedidos e a coordenação dos pagamentos.
- **`payments/`:** contém a classe abstrata `MeioPagamento` e as implementações de Pix, cartão, dinheiro e vale-refeição.
- **`routes/`:** recebe as requisições HTTP e direciona cada rota para o serviço correspondente.

## Papel dos integrantes

| Integrante | Papel |
|---|---|
| Aline | Código: servidor e integração |
| Luiz Mário | Código: pagamento |
| Ana Rita | README e mapeamento dos princípios |
| Juliana | Roteiro do vídeo |
| Vitória | Gravação e narração do vídeo |

## Onde estão os princípios no código

Nesta versão, a estrutura foi refatorada para aplicar princípios de projeto orientado a objetos:

- **Responsabilidade Única (SRP):** as responsabilidades foram distribuídas entre módulos e classes. `Handler` trata as requisições HTTP, `pedido_service.py` gerencia a criação e a busca de pedidos, `pagamento_service.py` coordena o fluxo de pagamento e cada classe em `payments/` implementa uma modalidade específica.
- **Aberto/Fechado (OCP):** `pagamento_service.py` trabalha com a abstração `MeioPagamento`, sem concentrar condicionais para cada forma de pagamento. Para adicionar uma modalidade, criamos uma nova classe que implementa o contrato e a registramos em `payments/factory.py`, sem modificar as implementações existentes.
- **Abstração e polimorfismo:** as classes `PagamentoPix`, `PagamentoCartao`, `PagamentoDinheiro` e `PagamentoValeRefeicao` implementam o método `processar()` definido em `MeioPagamento`. O serviço de pagamento utiliza a mesma interface para acionar qualquer modalidade.
- **Separação de responsabilidades:** dados, regras de negócio, implementações de pagamento e comunicação HTTP ficam organizados em diretórios distintos.

### Complexidade ciclomática

A função `pagar()` foi simplificada: ela valida o pedido, seleciona a implementação de pagamento e aplica o resultado. As regras específicas de cada modalidade ficam nos respectivos métodos `processar()`.

A comparação numérica da complexidade ciclomática entre a versão inicial e esta PoC deve ser feita com a mesma ferramenta e configuração nas duas versões. Assim, é possível demonstrar a distribuição dos pontos de decisão sem afirmar uma redução numérica que ainda não tenha sido medida.
