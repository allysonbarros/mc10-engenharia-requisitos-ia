# PROMPT B — casos a partir das invariantes e da máquina de estados

Você gera casos de teste de INTEGRAÇÃO que tentam FURAR as invariantes
abaixo. Seu objetivo não é confirmar que o sistema funciona; é encontrar
a sequência de chamadas que o quebra.

## Invariantes (o sistema não pode violar, em nenhuma ordem de eventos)
- SPEC-001/I1: inscrições confirmadas nunca excedem a capacidade.
- I2: um pagamento aprovado produz exatamente um recebimento.
- I3: webhook de pagamento desconhecido não muda estado.

## Máquina de estados
aguardando_pagamento -> confirmada | recusada | expirada
(expirada não tem transição de saída declarada)

## Regras
- Para cada invariante, escreva pelo menos um caso de CORRIDA ou de
  ORDEM INVERTIDA, não só o caminho feliz: evento duplicado, evento fora
  de ordem, evento que chega depois do job de expiração, duas requisições
  simultâneas pela mesma vaga.
- A asserção é sobre a invariante, nunca sobre o passo a passo interno.
  `confirmadas <= capacidade`, não `status == 'confirmada'`.
- Toda transição não declarada na máquina de estados é uma LACUNA: liste
  a pergunta de negócio correspondente e escreva o teste com o
  comportamento que a invariante exige, mesmo que o sistema hoje falhe.
- Um teste que falha é resultado válido. Não ajuste a asserção para
  passar e não conserte a implementação.

## Saída
Arquivo pytest + uma tabela: caso | invariante | sequência de eventos |
resultado observado.
