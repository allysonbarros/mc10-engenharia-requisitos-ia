# Log de decisões

Append-only. Toda decisão técnica significativa entra aqui com data, contexto e justificativa.

## 2026-07-29 — Adoção da fábrica kairos-forge

Iniciado o uso do plugin kairos-forge neste projeto via /kairos-forge:onboardar.

## 2026-07-29 — Decisões de negócio para o backlog de SPECs

Fechadas com o usuário via /kairos-forge:especificar (SPEC-001 a 008):

- **Escopo MVP da inscrição:** só eventos gratuitos; pagamento é SPEC própria (SPEC-005).
- **Lista de espera:** participante entra na fila (SPEC-001); promoção = notifica o 1º e dá prazo de 24h (premissa, a confirmar); promoção implementada na SPEC-004 (depende de cancelamento).
- **Conflito de horário:** o sistema **bloqueia** inscrição em atividades sobrepostas.
- **Concorrência de vagas:** UPDATE condicional atômico (abordagem A) — ratificar em ADR no T0.
- **Cancelamento:** configurável por evento (permite? prazo?); default 24h antes do início (premissa).
- **Reembolso:** configurável por evento; fórmula exata a definir com o negócio (não inventar).
- **Certificado:** o **organizador libera** manualmente (não automático, não por presença).
- **Palestrante vê participantes:** só **nome + atividade** (minimização LGPD).

Pendências que viram pré-requisito: escolha de stack + banco (T0), provedor de pagamento, canal de notificação, e **auth/papéis** (não elicitado, precisa de SPEC própria).

## 2026-07-29 — Fechamento da lacuna da observação #9 (auth + NFRs)

- **SPEC-009 (Autenticação e papéis / RBAC)** criada: 5 papéis (participante, organizador, financeiro, palestrante, TI/admin) com matriz de permissões, autorização server-side e isolamento. Provedor de identidade fica como decisão de ADR (Q-01, bloqueante).
- **RNF-001 (Requisitos não-funcionais)** criado cobrindo os 5 temas da observação #9 (segurança, desempenho, disponibilidade, acessibilidade, privacidade/LGPD) + observabilidade. Metas numéricas registradas como **premissa "a confirmar"**, não como fato elicitado.

## 2026-07-29 — T0 resolvido: stack + banco (ADR-0001)

Decisão do usuário + Rafael/Elisa: **Ruby on Rails 8 (API) + Next.js + PostgreSQL**, containerizado com Docker. Registrada em `docs/adr/ADR-0001-stack-e-banco.md`. Desbloqueia as 9 SPECs. Gates de teste concretos definidos em `contextos/testes.md` (Rails: rubocop/brakeman/rails test; Next.js: lint/typecheck/vitest/playwright/build). Concorrência de vagas (UPDATE condicional atômico da SPEC-001) fica ratificada pelo Postgres. Hospedagem fica para um ADR futuro.

## 2026-07-29 — Identidade/auth (ADR-0002)

Decisão do usuário + Rafael/Helena: **autenticação própria com o Rails nativo** (has_secure_password/bcrypt + Session), sem provedor externo. Cookie httpOnly/Secure/SameSite com padrão BFF no Next.js; RBAC por `role` (5 papéis) e autorização por policy objects server-side. Registrada em `docs/adr/ADR-0002-identidade-e-autenticacao.md`. Resolve SPEC-009/Q-01 e destrava SPEC-002/005/008. Pendentes: política de senha (P-01), MFA (Q-02, follow-up para financeiro/admin). Comando exato do gerador do Rails 8 a reconfirmar na implementação (ctx7 falhou nesta sessão).

## 2026-07-29 — Pagamento e reembolso (ADR-0003 + SPEC-005 atualizada)

Elicitação com o usuário (Thiago/Joana/Financeiro):
- **Gateway:** Mercado Pago (ADR-0003). **Métodos:** Pix + cartão de crédito; **boleto fora** (confirmação lenta briga com reserva de 15min).
- **Reembolso:** regra "total até prazo" — 100% se cancelar até `prazo_reembolso` (default 7d, configurável por evento), 0% depois. Sem arredondamento fracionário.
- **Reserva de vaga:** timeout de 15min confirmado.
- Confirmação via webhook (validação de assinatura + idempotência). SPEC-005 atualizada: Q-01/Q-02/Q-03 resolvidas; restam Q-04 (taxa do gateway no reembolso) e Q-05 (prazo default) — não bloqueantes.

## 2026-07-30 — Backlog, épicos e roadmap de sprints (Camila)

Derivado das SPECs: 9 épicos (E0 fundação → E8 palestrante), ~48 histórias rastreáveis a requisitos, backlog priorizado (MoSCoW) e roadmap de ~10-14 sprints de 1 semana. Premissas: cadência 1 semana; capacidade = fábrica kairos-forge (agentes paralelos); estimativa em story points Fibonacci; velocidade inicial ~20 SP/sprint (a calibrar). Documentos em `docs/planejamento/` (backlog-e-roadmap.md + historias-detalhadas.md). Cada história aponta para o ID do requisito da SPEC — rastreabilidade ponta a ponta. Detalhamento completo (Gherkin + DoD + agentes) dos sprints de fundação/identidade/eventos + destaques críticos (concorrência de vagas, webhook de pagamento).

## 2026-07-30 — Projeto publicado no GitHub (público)

Repositório público criado em `github.com/allysonbarros/mc10-engenharia-requisitos-ia` (branch padrão `main`), para uso como trabalho da pós em Engenharia de Software com IA (UFG). git init + .gitignore (Rails/Node/.env) + README adicionados. Verificação de segurança pré-publicação: nenhum segredo versionado. Baseline = artefatos de requisitos (10 SPECs, 3 ADRs, 2 threat models, DESIGN-002, grafo, auditoria). Implementação da SPEC-002 (scaffold Rails+Next) estava em andamento e foi **pausada** para a publicação; será retomada com commits por incremento.

## 2026-07-29 — Threat models de pagamento e auth (Helena)

Modelos de ameaças concluídos em `docs/seguranca/`: `AMEACAS-pagamento-2026-07-29.md` (SPEC-005) e `AMEACAS-autenticacao-2026-07-29.md` (SPEC-009). Ameaças principais: forja/replay de webhook e reembolso indevido (pagamento); tomada de conta e escalada de privilégio (auth). Mitigações P1 identificadas (M1–M5 pagamento; M1–M6 auth) e referenciadas nas respectivas SPECs para virarem tarefas na implementação. Preenche a dimensão Estrutura da auditoria (threat model em área sensível).
