# Esquema do grafo de conhecimento

**Versão:** 2
**Última alteração:** 2026-07-29 — adicionado predicado `restringe` no primeiro `construir` do grafo

## Tipos de entidade

| Tipo | O que é | Exemplos |
|---|---|---|
| COMPONENTE | Módulo, serviço, pacote ou camada do sistema | API de inscrições, worker de notificações |
| FEATURE | Capacidade voltada ao usuário | Inscrição em evento, lista de espera, emissão de certificado |
| SPEC | SPEC rastreável em docs/specs/ | SPEC-001 |
| ADR | Decisão arquitetural registrada | ADR-0003 |
| DECISÃO | Decisão técnica fora de ADR (decisoes/log.md) | "Adotar pnpm" |
| TECNOLOGIA | Linguagem, framework, banco, serviço externo | PostgreSQL, React |
| PESSOA | Pessoa real do time ou stakeholder | Allyson, Organizador, Participante |
| AGENTE | Persona da fábrica | Laura, Helena |
| INCIDENTE | Memória de incidente (.agents/memory/) | "Timeout no deploy de sexta" |
| AMBIENTE | Ambiente ou infraestrutura | produção, staging |

## Predicados aceitos

Verbos curtos, em PT-BR, no presente: `implementa`, `depende de`, `expõe`, `consome`,
`decidiu usar`, `substitui`, `bloqueia`, `cobre`, `valida`, `causou`, `mitiga`,
`pertence a`, `responsável por`, `documenta`, `restringe`.

- `restringe` — um requisito não-funcional/transversal impõe condição sobre uma SPEC (ex.: RNF-001 restringe SPEC-001).

Predicado novo é permitido se for verbo curto e raciocinável — registre-o aqui na
próxima revisão. Predicado vago ("está relacionado a", "envolve") é proibido.

## Histórico de versões

| Versão | Data | Mudança |
|---|---|---|
| 1 | 2026-07-29 | Esquema inicial |
| 2 | 2026-07-29 | Adicionado predicado `restringe` (RNF transversal → SPEC) |
