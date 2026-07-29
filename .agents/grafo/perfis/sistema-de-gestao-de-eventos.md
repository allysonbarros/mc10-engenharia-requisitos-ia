# Perfil — Sistema de Gestão de Eventos

**Tipo:** COMPONENTE · **Grau:** 19 · **Intervalo temporal:** 2026-07-29

O Sistema de Gestão de Eventos é o produto que a **Eventus** decidiu construir para centralizar inscrições, vagas, pagamentos e certificados — hoje espalhados em formulários e planilhas. No grafo, é o nó agregador para o qual convergem todas as 15 features (`pertence a`), o que o torna a raiz conceitual do domínio.

Os cinco stakeholders orbitam este sistema: Participante, Organizador, Equipe Financeira e Palestrante o usam por meio de features específicas, e a Equipe de TI é `responsável por` ele. A **Adoção da fábrica kairos-forge** também `pertence a` este sistema — foi a decisão que iniciou o ciclo spec-driven do projeto.

Desde o ADR-0001, o sistema também `decidiu usar` Ruby on Rails e Next.js (a stack fixada no T0). Fora isso, é um nó estrutural (agrega features e stakeholders); as demais decisões técnicas e bloqueios moram nas SPECs individuais.

**Fatos-chave (rastreáveis):**
- (Inscrição em evento … Autorização RBAC, 15 features) --[pertence a]--> (Sistema de Gestão de Eventos) [contextos/sobre-o-projeto.md]
- (Equipe de TI) --[responsável por]--> (Sistema de Gestão de Eventos) [contextos/sobre-o-projeto.md]
- (Adoção da fábrica kairos-forge) --[pertence a]--> (Sistema de Gestão de Eventos) [decisoes/log.md]
