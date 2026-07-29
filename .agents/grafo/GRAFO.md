# Grafo de conhecimento

Modelo de mundo persistente da fábrica neste projeto: entidades e relações com
proveniência, extraídas de SPECs, ADRs, decisões e memórias. A memória de cada
agente morre com a janela de contexto — o grafo não.

Construa/atualize com `/kairos-forge:mapear-conhecimento` (Olívia coordena).
O grafo alimenta `/mobilizar` (memória compartilhada entre teammates),
`/validar` (checagem de afirmações contra arestas) e consultas multi-hop.

## Estado

- **Última construção:** 2026-07-29 (construir do zero)
- **Última atualização:** 2026-07-29 (`atualizar` — ingestão do ADR-0001, reconciliação do T0)
- **Versão do esquema:** 2 (adicionado predicado `restringe`)
- **Nós:** 64 · **Arestas:** 160 · **Aliases:** 6
- **Componentes conexos:** 1 (grafo íntegro, sem ilhas)
- **Densidade:** 2,50 arestas/nó (alta, mas legítima — grafo de dependências entre SPECs)
- **Taxa de compressão:** 1,09 (nomenclatura consistente no corpus)
- **Corpus:** 18 documentos (10 SPECs/RNF + 1 ADR + 2 decisões + 5 contextos) — abaixo do cap de 30.

### Delta da última atualização (ADR-0001)

- **+5 entidades:** ADR-0001 (ADR) e as tecnologias Ruby on Rails, Next.js, PostgreSQL, Docker.
- **−9 arestas `bloqueia`:** o T0 (`Escolha de stack e banco`) foi resolvido e não bloqueia mais as SPECs. Substituídas por `ADR-0001 --substitui--> Escolha de stack e banco`.
- **+8 arestas:** `decidiu usar` das tecnologias e `UPDATE condicional atômico --depende de--> PostgreSQL`.
- Nó `Escolha de stack e banco` remarcado como **RESOLVIDA** (perfil atualizado).

### Entidades por tipo

| Tipo | Qtd |
|---|---|
| AGENTE | 18 |
| FEATURE | 15 |
| SPEC | 10 |
| DECISÃO | 10 |
| PESSOA (stakeholder) | 5 |
| COMPONENTE | 1 |

### Top hubs (com perfil em `perfis/`)

| Nó | Grau | Papel |
|---|---|---|
| Sistema de Gestão de Eventos | 19 | Raiz do domínio; agrega features e a stack |
| SPEC-001 | 16 | Feature-âncora (inscrição + vagas) |
| RNF-001 | 14 | Requisitos não-funcionais (restringe todas) |
| SPEC-002 | 13 | Fundacional (gestão de eventos) |
| SPEC-005 | 13 | Pagamento (Complexa) |
| SPEC-009 | 11 | Auth/RBAC; pré-requisito de 002/005/008 |
| Laura | 9 | Tech Lead; classifica todas as SPECs |
| ADR-0001 | 5 | Resolveu o T0; fixou Rails + Next.js + PostgreSQL |
| Escolha de stack e banco | 3 | T0 **resolvido** por ADR-0001 |

## Onde o grafo já pode ser usado

- **`consultar`** — perguntas multi-hop: "o que bloqueia a SPEC-005?", "quais SPECs dependem de autenticação?", "quem é responsável pelo T0?".
- **`/mobilizar`** — semear teammates com o subgrafo da SPEC em vez do contexto inteiro.
- **`/validar`** — checar afirmações contra arestas com proveniência.

## Amostras humanas

| Data | Nó amostrado | Veredito |
|---|---|---|
| 2026-07-29 | Bloqueio de conflito de horário (FEATURE) | ✅ 3/3 arestas conferem. Nota: arestas `FEATURE --pertence a--> Sistema` usam `contextos/sobre-o-projeto.md` como fonte de escopo do sistema (proveniência estrutural, não menção textual da feature). |
| 2026-07-29 | ADR-0001 (ADR) — pós-atualização | ✅ 5/5 arestas conferem contra `docs/adr/ADR-0001-stack-e-banco.md` (substitui o T0 + decidiu usar Rails/Next.js/PostgreSQL/Docker). Multi-hop SPEC-001→UPDATE→PostgreSQL validado. |
