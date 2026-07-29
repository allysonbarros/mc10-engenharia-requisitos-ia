# SPEC-008 — Painel do palestrante

> Autores: **Helena (Segurança)** obrigatória (PII) · **Diego (Sistemas)** · Laura classificou.
> Tamanho: **Médio** · Sensível — expõe dados de participantes.

## Contexto e problema

Palestrantes querem consultar a lista de participantes inscritos em suas atividades e a programação delas. A elicitação deixou em aberto **quais dados** ficam visíveis (#8). A decisão desta sessão, por minimização de dados (LGPD), foi: o palestrante vê **apenas nome do participante e a atividade** — nada de e-mail, telefone ou outros dados pessoais.

## Objetivo

Dar ao palestrante uma visão das suas atividades e dos participantes nelas inscritos, expondo o mínimo de dado pessoal.

## Não-objetivos

- Contato direto com participantes (envio de e-mail/mensagem) — fora do escopo; exigiria mais dados e base legal.
- Edição de qualquer dado de participante — o painel é somente leitura.
- Atribuição de palestrantes a atividades — assume-se feito na gestão de eventos (SPEC-002) ou por auth/papéis (pré-requisito).

## Invariantes

- **I1 (minimização):** o palestrante vê **somente** nome do participante e a atividade; nunca e-mail, telefone ou outros dados (decisão LGPD).
- **I2 (isolamento):** o palestrante vê apenas participantes das **suas** atividades — nunca de atividades de terceiros.
- **I3:** o painel é somente leitura.

## Requisitos rastreáveis

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| PAL-01 | Como palestrante, quero ver minhas atividades e sua programação, para me organizar. | P1 | WHEN o palestrante acessa o painel THEN o sistema SHALL listar as atividades atribuídas a ele com horários. | Pendente | — |
| PAL-02 | Como palestrante, quero ver os participantes inscritos nas minhas atividades, para conhecer o público. | P1 | WHEN o palestrante abre uma atividade sua THEN o sistema SHALL listar os participantes confirmados exibindo **apenas nome** e a atividade (I1). | Pendente | — |
| PAL-03 | Como responsável por LGPD, quero que o palestrante não veja dados além do nome, para minimizar exposição. | P1 | WHEN a lista de participantes é exibida THEN o sistema SHALL NÃO retornar e-mail, telefone ou outros dados pessoais (I1). | Pendente | — |
| PAL-04 | Como responsável por segurança, quero que o palestrante só veja participantes das suas atividades, para evitar vazamento. | P1 | WHEN o palestrante tenta acessar participantes de atividade que não é dele THEN o sistema SHALL negar o acesso (I2). | Pendente | — |

## Plano de implementação

> Bloqueio: T0 (stack) **e** auth/papéis (pré-requisito) precedem implementação. Gates `<a definir>`.

| Tarefa | Agente | Requisito(s) | Arquivos/áreas | Depende de | Done when | Gate |
|---|---|---|---|---|---|---|
| T1 | [Thiago] → [Lucas] | PAL-01, PAL-02 | endpoint do painel (projeção mínima) | SPEC-002, auth | Retorna atividades do palestrante e participantes só com nome (I1). | `<a definir>` |
| T2 | [Helena] | PAL-03, PAL-04 | auditoria de acesso/PII | T1 | Confirma que resposta não vaza dados extras (I1) e valida isolamento (I2). | auditoria |
| T3 | [Isabela] → [Marina] + [Ada] | PAL-01, PAL-02 | UI do painel (leitura) | T1 | Painel acessível, somente leitura (I3). | `<a definir>` |
| T4 | [Ricardo] | PAL-01..04 | testes | T1–T2 | Escopo mínimo e isolamento cobertos, inclusive tentativa de acesso indevido. | `<a definir>` |

## Matriz de testes

| Requisito | Tipo | Responsável | Comando/gate | Evidência esperada |
|---|---|---|---|---|
| PAL-01 | integration | [Ricardo] | `<a definir>` | Atividades do palestrante listadas. |
| PAL-02/03 | integration | [Ricardo] | `<a definir>` | Lista traz só nome; sem e-mail/telefone no payload. |
| PAL-04 | integration (authz) | [Ricardo] | `<a definir>` | Acesso a atividade de terceiro negado. |

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Vazamento de PII na resposta da API | Projeção mínima no backend (não filtrar só no front); auditoria Helena (I1). |
| Palestrante acessa dados de outra atividade | Checagem de propriedade por atividade (I2); teste de authz negativo. |
| Ausência de auth trava o painel | Registrar auth/papéis como pré-requisito (herda SPEC-002/Q-01). |

## Perguntas abertas

- **Q-01:** Palestrante deve ver participantes em lista de espera ou só confirmados? (adotado: só confirmados — confirmar.)
- **Q-02:** Auth/papéis (pré-requisito compartilhado) — precisa de SPEC própria.

## Validação

`/kairos-forge:validar SPEC-008`

## Próximo passo

`/kairos-forge:mobilizar SPEC-008` (após auth e SPEC-002).
