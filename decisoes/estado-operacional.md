# Estado operacional

Memória leve da fábrica neste projeto. Atualize quando uma execução revelar decisão, bloqueio, aprendizado ou follow-up recorrente.

## Decisões recentes

- 2026-07-29 — Backlog de SPECs escrito: SPEC-001 a 008 (inscrição, gestão de eventos, catálogo, cancelamento+promoção, pagamento, certificado, notificações, painel do palestrante). Decisões de negócio registradas em `decisoes/log.md`.

## Bloqueios ativos

- ~~**T0 (stack + banco)**~~ ✅ **RESOLVIDO 2026-07-29** — Rails 8 + Next.js + PostgreSQL (ADR-0001). Gates concretos em `contextos/testes.md`.
- ~~**Identidade/auth**~~ ✅ **RESOLVIDO 2026-07-29** — auth própria Rails nativo (ADR-0002). Destrava SPEC-002/005/008.
- ~~**Provedor de pagamento**~~ ✅ **RESOLVIDO 2026-07-29** — Mercado Pago, Pix + cartão (ADR-0003).
- ~~**Fórmula de reembolso**~~ ✅ **RESOLVIDO 2026-07-29** — "total até prazo" (SPEC-005/P-01).
- **Canal de notificação**: bloqueia entrega externa da SPEC-007 (in-app funciona sem).
- **Política de senha (P-01) e MFA (Q-02)**: detalhes de auth pendentes; não bloqueiam o início da SPEC-009.
- ~~**Threat models**~~ ✅ **FEITOS 2026-07-29** — `docs/seguranca/AMEACAS-pagamento-*` e `AMEACAS-autenticacao-*`. Mitigações P1 (M1–M5 pagamento, M1–M6 auth) devem virar tarefas na implementação das SPEC-005/009.

## Ordem de implementação sugerida

1. Resolver T0 (ADR de stack + banco) e ADR de identidade (SPEC-009/Q-01).
2. SPEC-009 (auth/papéis) — base de autorização das demais. RNF-001 vira gate transversal desde já.
3. SPEC-002 (gestão de eventos) → SPEC-001 (inscrição) → SPEC-003 (catálogo).
4. SPEC-004 (cancelamento + promoção) → SPEC-007 (notificações, interface).
5. SPEC-005 (pagamento — rodar /analisar-ameacas antes) → SPEC-006 (certificado) → SPEC-008 (palestrante).

- Nove questões em aberto na elicitação bloqueiam a especificação de features de negócio (ver `contextos/restricoes.md`). Requisitos não-funcionais ainda não levantados.

## Design

- 2026-07-29 — DESIGN-002 (gestão de eventos) concluído: 4 views com 5 estados cada, responsivo, acessibilidade e V-01..V-10. **Achado:** projeto sem design system → tokens + componentes base são tarefa fundacional da primeira implementação de UI.

## Aprendizados

## Ideias adiadas
