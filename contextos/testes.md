# Testes e gates

Stack definida em **ADR-0001**: Rails 8 (API) + Next.js + PostgreSQL. Comandos concretos abaixo.

## Comandos — Backend (Rails 8)

| Gate | Comando | Quando usar |
|---|---|---|
| Lint | `bin/rubocop` | Antes de PR (regras rubocop-rails-omakase) |
| Segurança | `bin/brakeman` | Antes de PR (SAST — RNF-SEG) |
| Unit/Integration | `bin/rails test` | Regra de negócio, models, requests |
| E2E/System | `bin/rails test:system` | Fluxo de tela server-rendered, se houver |
| Build/Boot | `bundle install && bin/rails db:prepare && bin/rails zeitwerk:check` | Antes de release/PR |

## Comandos — Frontend (Next.js)

| Gate | Comando | Quando usar |
|---|---|---|
| Lint | `npm run lint` | Antes de PR (ESLint) |
| Typecheck | `npm run typecheck` (`tsc --noEmit`) | Antes de PR |
| Unit | `npm test` (Vitest/Jest) | Componentes, hooks, lógica de UI |
| E2E | `npx playwright test` | Fluxo crítico de usuário (catálogo → inscrição → comprovante) |
| Build | `npm run build` | Antes de release/PR |

## Mapeamento por tipo de teste das SPECs

- **INSCR-02 (concorrência / sem overbooking):** teste de integração Rails que dispara inscrições paralelas nas últimas vagas e assere `ocupadas <= capacidade`. Gate: `bin/rails test`.
- **AUTH/PAL (autorização e isolamento):** testes de request negativos (acesso indevido → 403). Gate: `bin/rails test`.
- **Fluxos de UI (catálogo, inscrição, certificado):** Playwright. Gate: `npx playwright test`.
- **Segurança (RNF-SEG):** `bin/brakeman` + auditoria da Helena.
- **Acessibilidade (RNF-ACE):** axe nos testes Playwright + validação da Ada.

## Política

- Toda tarefa com código de produção deve ter caminho feliz e pelo menos 1 erro coberto.
- Requisito P1 sem gate precisa de justificativa na SPEC.
- `/kairos-forge:validar` roda os gates relevantes antes de `/kairos-forge:revisar`.
