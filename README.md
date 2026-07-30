# Sistema de Gestão de Eventos — Eventus

> Trabalho prático da pós-graduação em **Engenharia de Software com IA — UFG**.
> Projeto conduzido com a fábrica de agentes **[kairos-forge](https://github.com/vilelaAI/kairos-forge)** (spec-driven development assistido por IA).

A **Eventus** organiza congressos, workshops e eventos corporativos. Hoje o gerenciamento de inscrições é feito com formulários on-line e planilhas, o que dificulta o controle de vagas, pagamentos, cancelamentos e emissão de certificados. Este projeto centraliza essas atividades em um sistema próprio.

Este repositório documenta o ciclo completo de **engenharia de requisitos → arquitetura → segurança → design → início de implementação**, com todos os artefatos rastreáveis.

## Status atual

| Etapa | Estado |
|---|---|
| Elicitação de requisitos | ✅ (`elicitacao.txt`) |
| Especificação (10 SPECs + RNF) | ✅ `docs/specs/` |
| Decisões arquiteturais (3 ADRs) | ✅ `docs/adr/` |
| Modelos de ameaças (pagamento, auth) | ✅ `docs/seguranca/` |
| Handoff de design (SPEC-002) | ✅ `docs/design/` |
| Grafo de conhecimento | ✅ `.agents/grafo/` |
| Implementação | 🚧 iniciando pela SPEC-002 (fundacional) |

## Stakeholders

- **Participantes** — inscrevem-se, acompanham inscrições, cancelam e emitem certificados.
- **Organizadores** — criam eventos, controlam vagas e gerenciam participantes.
- **Equipe Financeira** — confirma pagamentos e controla reembolsos.
- **Palestrantes** — consultam programação e participantes de suas atividades.
- **Equipe de TI** — desenvolve e mantém o sistema.

## Stack (ADR-0001, ADR-0002, ADR-0003)

| Camada | Escolha |
|---|---|
| Backend / API | Ruby on Rails 8 (`--api`) |
| Frontend | Next.js (React + TypeScript) |
| Banco | PostgreSQL |
| Autenticação | Rails nativo (`has_secure_password` + Session), cookie httpOnly + BFF |
| Pagamento | Mercado Pago (Pix + cartão) |
| Empacotamento | Docker |

## Estrutura do repositório

```
.
├── elicitacao.txt          # Documento de elicitação (fonte de requisitos)
├── CLAUDE.md               # Instruções do projeto para agentes de IA
├── contextos/              # Contexto persistente (sobre, stack, convenções, restrições, testes)
├── decisoes/               # Log de decisões, estado operacional e auditorias
├── docs/
│   ├── specs/              # SPECs rastreáveis (SPEC-001..009 + RNF-001)
│   ├── adr/                # Architecture Decision Records
│   ├── design/             # Handoff de design (DESIGN-NNN)
│   └── seguranca/          # Modelos de ameaças (AMEACAS-*)
├── .agents/grafo/          # Grafo de conhecimento do projeto (entidades + relações)
├── api/                    # Backend Rails (em construção)
└── web/                    # Frontend Next.js (em construção)
```

## Requisitos e rastreabilidade

As SPECs usam requisitos com ID estável, prioridade e critério de aceite verificável no formato `WHEN … THEN … SHALL …`. Cada feature nasce de uma SPEC, é desenhada (quando tem UI), tem suas ameaças modeladas (quando é sensível) e é validada contra a SPEC antes da revisão.

| SPEC | Feature |
|---|---|
| SPEC-001 | Inscrição em evento com controle de vagas e lista de espera |
| SPEC-002 | Gestão de eventos pelo organizador (fundacional) |
| SPEC-003 | Catálogo de eventos |
| SPEC-004 | Cancelamento de inscrição e promoção da lista de espera |
| SPEC-005 | Pagamento, confirmação e reembolso |
| SPEC-006 | Emissão de certificado |
| SPEC-007 | Notificações e comprovantes |
| SPEC-008 | Painel do palestrante |
| SPEC-009 | Autenticação e papéis (RBAC) |
| RNF-001 | Requisitos não-funcionais (segurança, desempenho, disponibilidade, acessibilidade, privacidade/LGPD) |

## Como rodar (quando a implementação estiver disponível)

```bash
# Backend
cd api && bundle install && bin/rails db:prepare && bin/rails server

# Frontend
cd web && npm install && npm run dev
```

Gates de qualidade em `contextos/testes.md`.

## Licença

Projeto acadêmico — UFG, pós-graduação em Engenharia de Software com IA.
