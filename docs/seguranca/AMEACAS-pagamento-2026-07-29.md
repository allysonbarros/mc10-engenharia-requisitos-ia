# Modelo de ameaças — Pagamento e reembolso — 2026-07-29

**Coordenado por:** Helena (Segurança), com Thiago (Integrações — Mercado Pago) e Carlos (Banco/RLS)
**SPEC relacionada:** SPEC-005 · **ADR:** ADR-0003 (Mercado Pago, Pix + cartão)
**Escopo:** fluxo de pagamento de eventos pagos via Mercado Pago, confirmação por webhook, reserva de vaga de 15min e reembolso "total até prazo".

## Resumo executivo

- **Ameaça principal:** confirmar uma inscrição **sem pagar** (ou obter reembolso indevido) forjando/reproduzindo a confirmação do gateway — dinheiro e vagas perdidos.
- **3 mitigações de maior alavancagem:**
  1. Validar assinatura do webhook **e reconsultar o status via API do Mercado Pago** (server-to-server) antes de confirmar — nunca confiar no corpo do webhook.
  2. **Idempotência** por `payment_id`/`event_id` em confirmação e reembolso.
  3. **Valor e regra de reembolso sempre server-side** — derivados do evento e do relógio do servidor, nunca de input do cliente.
- **Custo de não mitigar:** fraude direta (inscrições grátis, reembolsos forjados), esgotamento malicioso de vagas e exposição de dado financeiro — perda financeira e reputacional imediata.

## Ativos

| Ativo | Por que importa | Acesso atual |
|---|---|---|
| Capacidade de marcar inscrição como PAGA | Fraude: entrar sem pagar | Backend (via confirmação) |
| Registro/execução de reembolso | Desvio de dinheiro | Backend + financeiro |
| Vaga reservada (15min) | Esgotar inventário legítimo | Qualquer autenticado que inicia pagamento |
| Credencial da API do Mercado Pago | Controle total da integração de pagamento | Backend (env/cofre) |
| PII + dado financeiro do participante | Privacidade/LGPD; fraude | Backend, financeiro, Mercado Pago |

## Trust boundaries

| Boundary | O que cruza | Formato | Validação atual (a implementar) |
|---|---|---|---|
| Browser → BFF Next.js → Rails | Início de pagamento, cancelamento | HTTPS + cookie de sessão | Auth + authz de propriedade |
| Rails ↔ Mercado Pago (API) | Criação de cobrança, consulta de status | HTTPS + credencial | TLS + credencial fora do código |
| Mercado Pago → Rails (**webhook**) | Notificação de pagamento | HTTPS POST | **Assinatura + reconsulta server-to-server** |
| Rails ↔ PostgreSQL | Pagamento, reserva, reembolso | conexão interna | Transação + RLS/constraint |

## Entrypoints

| Entrypoint | Caller esperado | Auth | Rate limit | Validação |
|---|---|---|---|---|
| Iniciar pagamento | Participante | Sim (sessão) | Sim (por usuário) | Valor derivado do evento no server |
| **Webhook de confirmação** | Mercado Pago | **Assinatura** (não sessão) | Sim | Assinatura + reconsulta + idempotência |
| Consultar pagamentos | Financeiro | Sim + papel | — | Escopo por papel |
| Cancelar → reembolso | Participante | Sim | Sim | Regra e valor server-side |

## Perfis de atacante considerados

| Perfil | Por que entra neste modelo |
|---|---|
| Usuário comum fraudador | Quer inscrição grátis ou reembolso indevido |
| Atacante oportunista | Forja/reproduz webhook, testa a URL pública |
| Insider (financeiro) | Pode forjar confirmação/reembolso com login válido |

## Abuse paths

### AP-01: Webhook de pagamento forjado
**Perfil:** oportunista · **Objetivo:** confirmar inscrição sem pagar
**Caminho:**
1. Descobre a URL pública do webhook (previsível ou vazada).
2. Envia `POST` "payment approved" com um `payment_id` arbitrário.
3. Backend confirma a inscrição confiando no corpo recebido.
**Ativos atingidos:** confirmação de pagamento, vaga, receita.
**Controle atual:** inexistente (feature não implementada).
**Mitigação proposta:** aplicação — validar assinatura do webhook **e** reconsultar o status na API do Mercado Pago (server-to-server) por `payment_id` antes de confirmar. Corpo do webhook é só um gatilho, nunca a fonte da verdade.
**Severidade:** Crítica.

### AP-02: Replay de webhook válido
**Perfil:** oportunista · **Objetivo:** multiplicar confirmações/reembolsos
**Caminho:** captura ou reenvia uma notificação legítima várias vezes → múltiplas confirmações ou reembolsos duplicados.
**Ativos atingidos:** receita, reembolso.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação/banco — idempotência por `payment_id`/`event_id` (constraint de unicidade); processar cada evento uma única vez.
**Severidade:** Alta.

### AP-03: Reembolso indevido (manipulação de regra/prazo)
**Perfil:** usuário fraudador · **Objetivo:** 100% após o prazo
**Caminho:** cancela após `prazo_reembolso` mas adultera parâmetros (data, percentual, valor) na request para obter reembolso integral.
**Ativos atingidos:** dinheiro.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação — cálculo do reembolso 100% server-side, com base no **relógio do servidor** e na política do evento; ignorar qualquer valor/percentual/data vindos do cliente.
**Severidade:** Alta.

### AP-04: Confirmar/ver pagamento de terceiro (IDOR)
**Perfil:** usuário curioso · **Objetivo:** acessar ou confirmar pagamento alheio
**Caminho:** troca `inscricao_id`/`payment_id` na request e acessa/aciona pagamento de outro participante.
**Ativos atingidos:** PII financeira, integridade de pagamento.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação + banco — authz de propriedade (o pagamento pertence ao usuário/evento) e RLS no Postgres.
**Severidade:** Alta.

### AP-05: Adulterar valor a pagar
**Perfil:** usuário fraudador · **Objetivo:** pagar menos
**Caminho:** envia o preço no corpo da request e informa valor menor.
**Ativos atingidos:** receita.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação — o valor **sempre** é derivado do evento no servidor; o cliente nunca envia preço.
**Severidade:** Alta.

### AP-06: Esgotamento malicioso de vagas via reservas (DoS de inventário)
**Perfil:** oportunista · **Objetivo:** negar vagas a usuários legítimos
**Caminho:** abre muitas reservas de 15min sem concluir o pagamento, esgotando o pool.
**Ativos atingidos:** disponibilidade de vagas.
**Controle atual:** parcial (expiração de 15min ajuda).
**Mitigação proposta:** aplicação — limite de reservas ativas por usuário + rate limit; expiração rápida já prevista (SPEC-005/I3).
**Severidade:** Média.

### AP-07: Vazamento da credencial do Mercado Pago
**Perfil:** oportunista/insider · **Objetivo:** controlar a integração
**Caminho:** credencial commitada no código ou impressa em log.
**Ativos atingidos:** integração de pagamento inteira.
**Controle atual:** inexistente.
**Mitigação proposta:** infra — credencial em variável de ambiente/cofre (RNF-SEG-04); nunca logar; `bin/brakeman` como gate.
**Severidade:** Alta.

## Mitigações priorizadas

| ID | Mitigação | Camada | Custo | Alavancagem | Cobre |
|---|---|---|---|---|---|
| M1 | Assinatura do webhook + reconsulta server-to-server antes de confirmar | Aplicação | Médio | Muito alta | AP-01 |
| M2 | Idempotência por payment_id/event_id (constraint) | App/Banco | Baixo | Alta | AP-02 |
| M3 | Reembolso e valor 100% server-side (relógio + política do server) | Aplicação | Baixo | Alta | AP-03, AP-05 |
| M4 | AuthZ de propriedade + RLS em pagamento | App/Banco | Médio | Alta | AP-04 |
| M5 | Credencial em cofre, nunca em log; brakeman gate | Infra | Baixo | Alta | AP-07 |
| M6 | Limite de reservas ativas por usuário + rate limit | Aplicação | Baixo | Média | AP-06 |

## Detecção e resposta

| Sinal | Onde monitorar | Quem responde |
|---|---|---|
| Webhook com assinatura inválida | Log do endpoint de webhook | Helena / Sérgio |
| Divergência valor pago × esperado | Reconciliação de pagamento | Financeiro / Renata |
| Pico de reservas expiradas por usuário | Métrica de reserva | Renata |
| Reembolsos acima do esperado | Painel financeiro | Financeiro |

## Decisões aceitas

- **Boleto fora do MVP** (ADR-0003): reduz superfície (sem confirmação lenta/assíncrona longa) — risco de exclusão de método aceito conscientemente.
- **MFA para financeiro não nesta versão** (SPEC-009/Q-02): aceito temporariamente; recomendável antes de operar dinheiro real.

## Próximo passo

- Mitigações **M1–M5 viram tarefas P1** na SPEC-005 (segurança de pagamento é P1, não opcional).
- M6 entra como ressalva em `/kairos-forge:revisar`.
- Reavaliar este modelo se: mudar de gateway, incluir boleto, ou abrir a API de pagamento a terceiros.
