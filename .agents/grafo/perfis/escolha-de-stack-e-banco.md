# Perfil — Escolha de stack e banco

**Tipo:** DECISÃO (T0) · **Status: RESOLVIDA** · **Grau:** 3 · **Intervalo temporal:** 2026-07-29

"Escolha de stack e banco" foi a decisão pendente mais impactante do projeto (o **T0**) — enquanto aberta, `bloqueava` as nove SPECs de feature e mantinha todos os gates de teste indefinidos. Em 2026-07-29 foi **resolvida por ADR-0001** (`ADR-0001 --substitui--> Escolha de stack e banco`): Ruby on Rails 8 + Next.js + PostgreSQL.

As arestas `bloqueia` foram removidas na atualização do grafo porque o bloqueio deixou de existir — a implementação está destravada. Permanecem as arestas de autoria: Rafael (Staff) e Elisa (Cloud) foram `responsáveis por` conduzir a decisão.

Nota de proveniência: este nó era o gargalo estrutural do grafo; após a resolução, o novo hub agregador é o próprio ADR-0001 e as tecnologias que ele fixou.

**Fatos-chave (rastreáveis):**
- (ADR-0001) --[substitui]--> (Escolha de stack e banco) [ADR-0001]
- (Rafael) --[responsável por]--> (Escolha de stack e banco) [SPEC-001]
- (Elisa) --[responsável por]--> (Escolha de stack e banco) [SPEC-001]
