# SPEC-003 — Catálogo de eventos

> Autores: **Diego (Sistemas)** · **Isabela (UX)** no fluxo · Laura classificou.
> Tamanho: **Médio**.

## Contexto e problema

Participantes pediram "visualizar todos os eventos disponíveis em um único lugar". Hoje isso está espalhado. O catálogo é a porta de entrada: lista os eventos **publicados**, mostra vagas restantes e leva ao detalhe de onde se parte para a inscrição (SPEC-001).

## Objetivo

Oferecer ao participante uma vitrine dos eventos publicados, com detalhe de cada evento e disponibilidade de vagas.

## Não-objetivos

- Inscrição (SPEC-001) — o catálogo apenas encaminha.
- Gestão de eventos (SPEC-002).
- Recomendação/personalização — vitrine simples nesta versão.

## Invariantes

- **I1:** só eventos **publicados** aparecem no catálogo (respeita SPEC-002/I4).
- **I2:** vagas restantes exibidas = `capacidade - ocupadas` (ou "lotado" quando 0).

## Requisitos rastreáveis

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| CAT-01 | Como participante, quero ver todos os eventos disponíveis num só lugar, para escolher onde me inscrever. | P1 | WHEN o participante acessa o catálogo THEN o sistema SHALL listar todos os eventos publicados com título, período e vagas restantes. | Pendente | — |
| CAT-02 | Como participante, quero ver o detalhe de um evento, para decidir me inscrever. | P1 | WHEN o participante abre um evento THEN o sistema SHALL exibir descrição, atividades com horários, tipo (gratuito/pago) e vagas. | Pendente | — |
| CAT-03 | Como participante, quero saber quando um evento está lotado, para não perder tempo. | P1 | WHEN `ocupadas = capacidade` THEN o catálogo SHALL exibir "lotado" (com opção de lista de espera via SPEC-001). | Pendente | — |
| CAT-04 | Como participante, quero filtrar/buscar eventos por data ou tipo, para achar mais rápido. | P2 | WHEN o participante aplica um filtro (data/tipo) THEN o sistema SHALL retornar apenas eventos correspondentes. | Pendente | — |
| CAT-05 | Como organizador, quero que só eventos publicados apareçam, para não expor rascunhos. | P1 | WHEN um evento está em rascunho THEN ele SHALL NÃO aparecer no catálogo (I1). | Pendente | — |

## Plano de implementação

> Bloqueio: T0 (stack) precede implementação. Gates `<a definir>`.

| Tarefa | Agente | Requisito(s) | Arquivos/áreas | Depende de | Done when | Gate |
|---|---|---|---|---|---|---|
| T1 | [Thiago] → [Lucas] | CAT-01, CAT-02, CAT-05 | endpoint de listagem/detalhe | SPEC-002 | Lista só publicados; detalhe traz atividades e vagas. | `<a definir>` |
| T2 | [Lucas] | CAT-03 | cálculo de disponibilidade | T1 | "lotado" quando sem vaga (I2). | `<a definir>` |
| T3 | [André] | CAT-04 | busca/filtro | T1 | Filtro por data/tipo com recall verificado. | `<a definir>` |
| T4 | [Isabela] → [Marina] + [Pablo] + [Ada] | CAT-01..04 | UI da vitrine + detalhe | T1 | Vitrine e detalhe acessíveis, com estado vazio/lotado. | `<a definir>` |
| T5 | [Ricardo] | CAT-01..05 | testes | T1–T4 | Publicados listados, rascunho oculto, lotado sinalizado. | `<a definir>` |

## Matriz de testes

| Requisito | Tipo | Responsável | Comando/gate | Evidência esperada |
|---|---|---|---|---|
| CAT-01/02 | integration | [Ricardo] | `<a definir>` | Lista e detalhe corretos. |
| CAT-03 | integration | [Ricardo] | `<a definir>` | Evento cheio marcado "lotado". |
| CAT-04 | integration | [Ricardo] | `<a definir>` | Filtro retorna subconjunto correto. |
| CAT-05 | integration | [Ricardo] | `<a definir>` | Rascunho nunca aparece. |

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Contagem de vagas desatualizada no catálogo | Ler `ocupadas` da fonte única (SPEC-001); alinhar com contador em tempo real (INSCR-06). |
| Busca cara com muitos eventos | André mede precision/recall e custo antes de aprovar; começar simples. |

## Perguntas abertas

- **Q-01:** Catálogo é público (sem login) ou só para usuários autenticados? (herda auth — SPEC-002/Q-01.)

## Validação

`/kairos-forge:validar SPEC-003`

## Próximo passo

`/kairos-forge:desenhar SPEC-003` → `/kairos-forge:mobilizar SPEC-003`.
