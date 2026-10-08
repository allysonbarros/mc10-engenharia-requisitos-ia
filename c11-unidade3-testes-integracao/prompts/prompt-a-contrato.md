# PROMPT A — casos a partir do contrato

Você gera casos de teste de INTEGRAÇÃO a partir do contrato abaixo. Não
gera testes de unidade e não sugere mudanças na implementação.

## Contrato (fonte da verdade)
<colar aqui o trecho do OpenAPI: rotas, schemas, códigos de resposta,
cabeçalhos obrigatórios>

## Regras
- Um caso por par (rota, código de resposta) declarado no contrato. Se um
  código está no contrato e você não consegue escrever o caso que o
  produz, isso é uma LACUNA DE CONTRATO: liste e não invente o caso.
- Nunca invente campo, código de erro, cabeçalho ou mensagem que não
  esteja no contrato. Campo ausente é lacuna, não liberdade.
- O teste exercita a borda HTTP real (cliente de teste da aplicação),
  nunca chama a função interna direto.
- Dados fictícios com prefixo `fake-`; nenhum segredo real.
- Nome do teste = rota + código. Uma asserção principal por caso.
- Proibido afirmar comportamento de dependência externa sem ter rodado:
  se o caso depende de como o gateway assina o corpo, diga qual comando
  executar para conferir.

## Saída
Arquivo pytest + uma tabela: caso | rota | código | o que prova.
