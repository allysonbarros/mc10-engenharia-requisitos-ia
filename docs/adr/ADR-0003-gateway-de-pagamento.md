# ADR-0003 — Gateway de pagamento

- **Status:** Aceito
- **Data:** 2026-07-29
- **Decisores:** Thiago (Integrações), Rafael (Staff), Helena (Segurança), com aprovação do usuário e da Equipe Financeira
- **Resolve:** SPEC-005/Q-01 (provedor) e Q-02 (métodos) — parte do bloqueio da SPEC-005

## Contexto

A SPEC-005 (pagamento, confirmação e reembolso) especificou o fluxo, mas o provedor de pagamento e os métodos aceitos estavam em aberto — sem eles a integração externa não fecha. A Eventus é brasileira, então o **Pix** é praticamente obrigatório (confirmação quase imediata, custo baixo). A reserva de vaga é curta (15min, ADR/SPEC-005 P-02), o que exige métodos de **confirmação rápida**.

## Decisão

| Aspecto | Escolha |
|---|---|
| **Gateway** | **Mercado Pago** |
| **Métodos** | **Pix** e **cartão de crédito** |
| **Boleto** | **Fora do MVP** — confirmação de 1–2 dias úteis é incompatível com a reserva de 15min |
| **Confirmação** | Via **webhook** do Mercado Pago, com validação de assinatura e idempotência |
| **Isolamento** | Integração atrás de uma **camada de pagamento** (porta/adaptador) para não acoplar a regra ao SDK do provedor |

### Por que Mercado Pago

- Pix, cartão e checkout nativos, com boa documentação em PT-BR — adequado ao contexto brasileiro.
- Confirmação de Pix quase imediata, compatível com a reserva curta de vaga (SPEC-005/I2, I3).
- Ampla adoção reduz risco de integração e facilita suporte.

## Alternativas consideradas

| Alternativa | Por que não (agora) |
|---|---|
| Stripe | Excelente DX e suporta Pix no BR, mas o time optou por Mercado Pago pela familiaridade/contexto BR. |
| Pagar.me / PagBank | Boas opções nacionais; preteridas pela escolha do Mercado Pago. |
| Incluir boleto | Confirmação lenta conflita com a reserva de 15min; reintroduzir só se a política de reserva mudar. |

## Consequências

**Positivas**
- Pix cobre o método preferido no Brasil, com liberação rápida da vaga.
- Camada de pagamento isolada permite trocar de provedor no futuro com impacto contido.

**Negativas / trade-offs**
- **Lock-in parcial** no SDK/checkout do Mercado Pago — mitigado pela porta/adaptador.
- **Webhook é superfície de ataque** (forja, replay) — exige validação de assinatura e idempotência (Helena; threat model obrigatório antes de implementar).
- **Taxa do gateway** afeta a conta do reembolso (ver SPEC-005/Q-04).

## Premissas e pendências

- **Reembolso** segue a regra "total até prazo" (SPEC-005/P-01); resta confirmar se os 100% incluem a taxa do Mercado Pago (SPEC-005/Q-04) e o `prazo_reembolso` default (Q-05).
- **Ambiente sandbox** do Mercado Pago para testes de integração (gate de `bin/rails test` com webhooks simulados).
- Credenciais do gateway **fora do código** (RNF-SEG-04), em variáveis de ambiente/cofre.

## Impacto no backlog

- Resolve o "Provedor de pagamento" que bloqueava a SPEC-005.
- A SPEC-005 fica destravada para `/kairos-forge:analisar-ameacas` e, depois, implementação. Restam apenas as questões menores Q-04/Q-05 (não bloqueantes).
