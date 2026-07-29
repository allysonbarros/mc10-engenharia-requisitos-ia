# Stack técnica

Definida em **ADR-0001** (2026-07-29). Resolve o T0 que bloqueava as SPECs.

| Camada | Escolha | Justificativa |
|---|---|---|
| Linguagem backend | **Ruby** | Base do Rails; produtividade e convenções fortes. |
| Framework backend | **Ruby on Rails 8 (`--api`)** | CRUD e transações maduras (eventos, pagamento, cancelamento); RuboCop/Brakeman/CI no scaffold. |
| Linguagem/framework frontend | **Next.js (React, TypeScript)** | Catálogo, fluxos de inscrição (5 estados) e painéis; consome a API via REST. |
| Banco de dados | **PostgreSQL** | `UPDATE` condicional atômico contra overbooking (SPEC-001/I1); transações fortes (SPEC-005); RLS para isolamento (SPEC-008/009). |
| Empacotamento | **Docker** | Imagens separadas para API e frontend; portabilidade. |
| Autenticação | **Rails nativo** (has_secure_password + Session) | Auth própria, sem lock-in; ADR-0002. |
| Hospedagem | `<a definir>` | ADR de hospedagem futuro (PaaS gerenciado vs. cloud maior). |

## Padrões técnicos ratificados

- **Concorrência de vagas (SPEC-001):** UPDATE condicional atômico —
  `Evento.where(id: id).where('ocupadas < capacidade').update_all('ocupadas = ocupadas + 1')`
  e checar linhas afetadas (0 = lotado). Nada de contador em memória.
- **Contrato de API:** REST documentado em OpenAPI (Thiago) — o front Next.js depende dele.
- **Autorização:** server-side no Rails; RLS no Postgres onde couber (SPEC-009).

## Pendências de stack

- ADR de identidade/auth (SPEC-009/Q-01).
- Provedor de pagamento (SPEC-005/Q-01).
- Hospedagem (ADR-0002).
