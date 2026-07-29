# ADR-0001 — Stack de aplicação e banco de dados

- **Status:** Aceito
- **Data:** 2026-07-29
- **Decisores:** Rafael (Staff), Elisa (Cloud), com aprovação do usuário
- **Resolve:** T0 — o bloqueio que travava as 9 SPECs de feature (ver grafo: `Escolha de stack e banco --bloqueia--> SPEC-001..009`)

## Contexto

O projeto tinha stack indefinida (`<a preencher>`), o que bloqueava toda implementação e mantinha todos os gates de teste como `<a definir>`. Quatro forças do backlog pesam na escolha:

1. **Concorrência de vagas sem overbooking** (SPEC-001/I1) — exige banco com transações fortes e `UPDATE` condicional atômico.
2. **Transações de pagamento e reembolso** (SPEC-005) — consistência forte, dado financeiro.
3. **Privacidade/LGPD e autorização por papel** (SPEC-008, SPEC-009, RNF-PRI) — precisa de isolamento confiável (RLS) e controle server-side.
4. **CRUD rico + UI de organizador/participante/palestrante** — produtividade de framework e uma camada de UI moderna.

## Decisão

Adotar:

| Camada | Escolha |
|---|---|
| **Backend / API** | **Ruby on Rails 8** (modo `--api`) |
| **Frontend** | **Next.js** (React) |
| **Banco de dados** | **PostgreSQL** |
| **Empacotamento** | Docker (imagens separadas para API e frontend) |

### Por que atende os requisitos

- **Rails 8** traz convenções fortes, Active Record e geradores que aceleram o CRUD de eventos, inscrições e o painel do organizador; transações e *migrations* maduras cobrem pagamento e cancelamento. Já vem com RuboCop (omakase), Brakeman (segurança) e CI padrão — alinhado ao RNF-SEG.
- **PostgreSQL** atende diretamente a invariante anti-overbooking com `UPDATE evento SET ocupadas = ocupadas + 1 WHERE id = ? AND ocupadas < capacidade` (0 linhas afetadas = lotado), **ratificando a abordagem A da SPEC-001** (premissa P-02). Suporta transações serializáveis para pagamento e **RLS** para os isolamentos de SPEC-008/SPEC-009.
- **Next.js** entrega o catálogo, os fluxos de inscrição (com os cinco estados de UI) e os painéis, consumindo a API Rails via REST.

## Alternativas consideradas

| Alternativa | Por que não (nesta decisão) |
|---|---|
| Node.js + TypeScript full-stack | Um idioma só no full-stack é atraente, mas o time optou por Rails pela produtividade de backend e convenções. |
| Python + Django | Forte candidato (admin/ORM/auth prontos); preterido pela preferência explícita por Rails. |
| Java/Kotlin + Spring Boot | Robusto para transações, mas mais cerimônia inicial; desnecessário para o porte atual. |

A escolha de **Rails + Next.js** foi definida pelo usuário; PostgreSQL foi recomendado por Rafael/Elisa e aceito.

## Consequências

**Positivas**
- Backend produtivo e convencional; segurança e lint já no scaffold do Rails 8.
- Banco robusto que satisfaz a invariante mais crítica (I1) sem gambiarra.
- Frontend desacoplado, moderno e testável de ponta a ponta.

**Negativas / trade-offs**
- **Dois ecossistemas** (Ruby e JS/TS) = duas *toolchains*, dois *deploys*, dois conjuntos de dependências. Mitigação: Docker para ambos e contrato de API claro (Thiago documenta OpenAPI).
- Overhead de CORS/auth entre front e API. Mitigação: definido na SPEC-009.
- **Hospedagem ainda não decidida** — ver premissa abaixo.

## Premissas e follow-ups

- **Hospedagem:** não decidida nesta ADR. Premissa: apps containerizados (Docker), portáveis; a escolha entre PaaS gerenciado (com Postgres gerenciado) e cloud maior vira **um ADR de hospedagem futuro** quando a natureza de produção estiver definida.
- **Natureza do projeto** (protótipo acadêmico vs. produção real) não confirmada; o ADR mantém a stack enxuta o suficiente para os dois cenários.
- **Concorrência:** a estratégia de UPDATE condicional atômico da SPEC-001 fica **ratificada** por esta escolha de banco.

## Impacto no backlog

- Desbloqueia as 9 SPECs (o `bloqueia` do T0 deixa de valer).
- Os gates de teste, antes `<a definir>`, passam a ter comandos concretos — ver `contextos/testes.md`.
- Segue pendente o **ADR de identidade** (SPEC-009/Q-01) e o **provedor de pagamento** (SPEC-005/Q-01).
