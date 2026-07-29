# SPEC-009 — Autenticação e papéis (RBAC)

> Autores: **Helena (Segurança)** obrigatória · **Diego (Sistemas)** · **Rafael (Staff)** na decisão de identidade · Laura classificou.
> Tamanho: **Complexo** — auth + autorização + PII. Pré-requisito de SPEC-002, 005 e 008.

## Contexto e problema

A elicitação não levantou autenticação nem papéis (parte da observação #9), mas os cinco stakeholders têm permissões distintas: participante se inscreve, organizador gerencia seus eventos, equipe financeira confirma pagamentos, palestrante consulta suas atividades, e a equipe de TI administra. Sem controle de acesso por papel, invariantes de outras SPECs (organizador só mexe nos seus eventos, palestrante só vê suas atividades) não têm como ser garantidas. Esta SPEC define **identidade, papéis e autorização** em nível de comportamento — o provedor concreto de identidade é decisão de ADR à parte.

## Objetivo

Autenticar usuários e autorizar cada operação conforme o papel, com menor privilégio, garantindo os isolamentos exigidos pelas demais SPECs.

## Não-objetivos

- Escolha do provedor/tecnologia de identidade (auth próprio vs. OAuth vs. SSO) — **decisão em aberto** (ADR).
- Gestão de organização/multi-tenant avançada — nesta versão, papéis simples por usuário.
- Fluxos sociais (login com Google etc.) — follow-up, se o provedor permitir.

## Invariantes

- **I1 (least privilege):** cada papel só acessa o que sua função exige (ver matriz).
- **I2 (server-side):** toda autorização é verificada no backend; o front nunca é a fonte da verdade.
- **I3 (isolamento):** organizador acessa só seus eventos; palestrante só suas atividades; financeiro só dados de pagamento.
- **I4 (credencial protegida):** senha nunca trafega/armazena em texto claro (ver RNF-SEG).

## Papéis e permissões

| Papel | Pode | Não pode |
|---|---|---|
| **Participante** | Ver catálogo, inscrever-se, cancelar, emitir certificado liberado, ver seus dados | Ver dados de outros participantes; gerenciar eventos |
| **Organizador** | Criar/gerenciar **seus** eventos, ver inscritos dos seus eventos, liberar certificados | Acessar eventos de outros organizadores; confirmar pagamentos |
| **Equipe Financeira** | Ver/confirmar pagamentos, registrar reembolsos | Gerenciar eventos; ver dados além do necessário ao pagamento |
| **Palestrante** | Ver **suas** atividades e participantes (só nome — SPEC-008) | Ver e-mail/telefone; ver atividades de terceiros |
| **Equipe de TI (admin)** | Administrar o sistema | Uso indevido fora de trilha de auditoria |

## Requisitos rastreáveis

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| AUTH-01 | Como usuário, quero me autenticar, para acessar o sistema com minha identidade. | P1 | WHEN um usuário fornece credenciais válidas THEN o sistema SHALL estabelecer uma sessão autenticada; credenciais inválidas SHALL ser rejeitadas sem vazar qual campo falhou. | Pendente | — |
| AUTH-02 | Como admin, quero atribuir papéis a usuários, para definir o que cada um acessa. | P1 | WHEN um papel é atribuído a um usuário THEN o sistema SHALL passar a aplicar as permissões desse papel. | Pendente | — |
| AUTH-03 | Como responsável por segurança, quero que cada operação sensível verifique a permissão do papel, para impedir acesso indevido. | P1 | WHEN um usuário tenta uma operação fora das permissões do seu papel THEN o sistema SHALL negar no backend (I1,I2). | Pendente | — |
| AUTH-04 | Como organizador/palestrante, quero acessar só os meus recursos, para respeitar o isolamento. | P1 | WHEN um organizador acessa evento que não é seu OU palestrante acessa atividade que não é sua THEN o sistema SHALL negar (I3). | Pendente | — |
| AUTH-05 | Como usuário, quero uma sessão segura com expiração e logout, para proteger minha conta. | P1 | WHEN a sessão expira OU o usuário faz logout THEN o sistema SHALL exigir nova autenticação. | Pendente | — |
| AUTH-06 | Como responsável por segurança, quero política de credenciais forte, para reduzir risco de conta comprometida. | P2 | WHEN um usuário define senha THEN o sistema SHALL exigir a política mínima (P-02) e armazenar apenas hash forte (I4). | Pendente | — |
| AUTH-07 | Como titular de dados, quero consentir e fornecer o mínimo no cadastro, para respeitar a LGPD. | P1 | WHEN um usuário se cadastra THEN o sistema SHALL coletar apenas dados necessários e registrar consentimento (liga a RNF-PRI). | Pendente | — |

## Plano de implementação

> Bloqueio: T0 (stack) + escolha do provedor de identidade (Q-01) precedem implementação. Gates `<a definir>`.

| Tarefa | Agente | Requisito(s) | Arquivos/áreas | Depende de | Done when | Gate |
|---|---|---|---|---|---|---|
| T0c | [Rafael] + [Elisa] | — | ADR de identidade | SPEC-001/T0 | Provedor/estratégia de auth escolhido e registrado. | ADR revisado |
| T1 | [Fernanda] → [Carlos] | AUTH-01,02,07 | `migrations/` (usuário, papel, consentimento) | T0c | Modelo de usuário/papel; senha só como hash. | `<a definir>` |
| T2 | [Lucas] | AUTH-01, AUTH-05 | autenticação + sessão | T1 | Login/logout/expiração funcionam; credencial protegida (I4). | `<a definir>` |
| T3 | [Lucas] | AUTH-02..04 | autorização por papel (middleware) | T1 | Checagem de permissão e isolamento no backend (I1,I2,I3). | `<a definir>` |
| T4 | [Helena] | AUTH-01..07 | auditoria de segurança | T2,T3 | Sem bypass de authz; sem enumerar usuários; sem secret em código. | auditoria |
| T5 | [Lucas] | AUTH-06 | política de senha/credencial | T2 | Política mínima aplicada. | `<a definir>` |
| T6 | [Ricardo] | AUTH-01..07 | testes (incl. authz negativo) | T2–T5 | Acesso indevido negado; isolamento provado. | `<a definir>` |

## Matriz de testes

| Requisito | Tipo | Responsável | Comando/gate | Evidência esperada |
|---|---|---|---|---|
| AUTH-01/05 | integration | [Ricardo] | `<a definir>` | Login válido cria sessão; expiração/logout exigem re-login. |
| AUTH-03/04 | integration (authz) | [Ricardo] | `<a definir>` | Operação fora do papel e acesso a recurso alheio negados. |
| AUTH-06 | unit | [Ricardo] | `<a definir>` | Senha fraca rejeitada; hash forte armazenado. |
| AUTH-07 | integration | [Ricardo] | `<a definir>` | Cadastro coleta só o mínimo e registra consentimento. |

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Autorização só no front (bypass) | Verificação server-side obrigatória (I2); auditoria Helena. |
| Vazamento por enumeração de usuário/senha | Mensagens de erro genéricas; rate limiting (liga a RNF-SEG). |
| Escolha de provedor tardia trava as SPECs dependentes | T0c explícito; comportamento especificado agnóstico do provedor. |

## Premissas

- **P-01:** papéis simples por usuário (sem hierarquia de organização) nesta versão.
- **P-02:** política mínima de senha (comprimento/complexidade) e eventual MFA — **a confirmar com o negócio**.

## Perguntas abertas

- ~~Q-01 (provedor/estratégia de identidade)~~ ✅ Resolvido: auth própria Rails nativo (ADR-0002).
- **Q-02:** MFA nesta versão? Para quais papéis (ex.: financeiro, admin)? — recomendado como follow-up.

## Segurança

Threat model concluído: `docs/seguranca/AMEACAS-autenticacao-2026-07-29.md`. As mitigações **M1–M6 são P1** e viram tarefas: policy server-side + `role` fora de strong params, token de reset forte/single-use, rate limit/lockout, escopo+RLS, cookie httpOnly+rotação, CSRF.

## Validação

`/kairos-forge:validar SPEC-009`

## Próximo passo

✅ Threat model feito · Q-01 resolvido (ADR-0002). Depois de aprovada: `/kairos-forge:mobilizar SPEC-009` (incorporando M1–M6).
