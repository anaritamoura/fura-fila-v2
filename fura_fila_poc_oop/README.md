# FURA-FILA — PoC com orientação a objetos

## Executar

Mantenha o `index.html` na mesma pasta de `main.py` e execute:

```bash
python main.py
```

A aplicação abre em `http://localhost:8000`.

## Organização

- `main.py`: inicialização do servidor.
- `config.py`: configurações e estados.
- `data/`: cardápio e armazenamento temporário.
- `services/`: regras de negócio de pedidos e coordenação do pagamento.
- `payments/`: contrato e implementações de cada meio de pagamento.
- `routes/`: endpoints HTTP.

## Princípios aplicados

### Responsabilidade Única (SRP)

Cada classe/módulo tem uma responsabilidade delimitada. `Handler` trata HTTP;
`PedidoService` gerencia pedidos; `PagamentoService` coordena o fluxo de
pagamento; cada classe em `payments/` implementa uma modalidade.

### Aberto/Fechado (OCP)

`PagamentoService.pagar()` trabalha com a abstração `MeioPagamento` e não
precisa conter um `if/elif` para cada modalidade. Cada modalidade implementa
`processar()`.

Para incluir uma modalidade, crie uma classe que herde de `MeioPagamento`
e registre a classe em `payments/factory.py`. Não é necessário alterar as
classes Pix, Cartão ou Dinheiro.

### Vale-refeição

`PagamentoValeRefeicao` é uma simulação para demonstrar extensibilidade.
Ele aprova o valor total do pedido, sem consultar saldo nem integrar com
operadora real. O frontend deve enviar `forma: "vale_refeicao"` para usar
essa modalidade.

## Observações

- Os pedidos ficam em memória e são perdidos ao encerrar o servidor.
- O pagamento é simulado; não há integração real com adquirentes, Pix ou
  operadoras de vale-refeição.
- A API mantém os endpoints existentes: `/api/pedido`, `/api/pagar`,
  `/api/pronto`, `/api/cardapio`, `/api/pedidos` e `/api/pedido?id=...`.
- Para exibir a nova opção na interface, o `index.html` também precisa
  oferecer Vale-refeição e enviar `vale_refeicao` no campo `forma`.

## Complexidade ciclomática

Não declare uma redução numérica sem medir as duas versões com a mesma
ferramenta e configuração. Uma opção é instalar Radon (`pip install radon`)
e executar sobre uma cópia do código antigo e sobre esta versão:

```bash
radon cc -s -a caminho/para/versao_antiga.py
radon cc -s -a services/pagamento_service.py
radon cc -s -a payments/
```

Compare especificamente a função antiga `pagar()` com a nova
`services.pagamento_service.pagar()`. Na versão nova, as decisões próprias
de cada modalidade ficam nas classes concretas, portanto a complexidade
deve ser analisada por método e também no conjunto do fluxo.
