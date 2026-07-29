# SPEC-006 — Emissão de certificado

> Autores: **Diego (Sistemas)** · **Fernanda (Dados)** no modelo · Laura classificou.
> Tamanho: **Médio**.

## Contexto e problema

Participantes querem emitir o certificado depois do evento. A elicitação deixou em aberto se a emissão é automática ou depende de presença; **a decisão desta sessão foi: o organizador libera** os certificados manualmente. Assim o organizador controla quem recebe (podendo considerar presença por fora nesta versão), e o participante emite o seu quando liberado.

## Objetivo

Permitir que o organizador libere certificados de um evento e que o participante emita o seu após a liberação.

## Não-objetivos

- Confirmação automática de presença (check-in) — pode ser follow-up; aqui a liberação é decisão do organizador.
- Envio do certificado por e-mail — depende do canal (SPEC-007); aqui cobrimos a emissão/download.

## Invariantes

- **I1:** certificado só é emitido para inscrição **confirmada** e após o **término** do evento.
- **I2:** participante só emite se o organizador **liberou** o certificado para ele.
- **I3:** o certificado contém dados verídicos do sistema (nome do participante, evento, data, carga horária) — nada inventado.

## Requisitos rastreáveis

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| CERT-01 | Como organizador, quero liberar os certificados de um evento, para controlar quem recebe. | P1 | WHEN o organizador libera certificados após o término THEN o sistema SHALL habilitar a emissão para os inscritos confirmados selecionados (I1,I2). | Pendente | — |
| CERT-02 | Como participante, quero emitir meu certificado após o evento, para comprovar participação. | P1 | WHEN o certificado foi liberado para o participante THEN o sistema SHALL permitir emitir/baixar o certificado. | Pendente | — |
| CERT-03 | Como participante, quero que o certificado tenha meus dados corretos, para ter validade. | P1 | WHEN o certificado é gerado THEN ele SHALL conter nome do participante, título do evento, data e carga horária vindos do sistema (I3). | Pendente | — |
| CERT-04 | Como organizador, quero impedir emissão sem liberação, para evitar certificado indevido. | P1 | WHEN o certificado não foi liberado para o participante THEN o sistema SHALL negar a emissão (I2). | Pendente | — |
| CERT-05 | Como terceiro, quero verificar a autenticidade de um certificado, para confiar nele. | P3 | WHEN um certificado é emitido THEN o sistema SHALL incluir um código de verificação consultável. | Pendente | — |

## Plano de implementação

> Bloqueio: T0 (stack) precede implementação. Gates `<a definir>`.

| Tarefa | Agente | Requisito(s) | Arquivos/áreas | Depende de | Done when | Gate |
|---|---|---|---|---|---|---|
| T1 | [Fernanda] → [Carlos] | CERT-01..05 | `migrations/` (liberação, certificado) | SPEC-001, SPEC-002 | Modelo de liberação e emissão; rollback. | `<a definir>` |
| T2 | [Lucas] | CERT-01, CERT-04 | liberação pelo organizador | T1 | Liberação habilita emissão só a confirmados após término (I1,I2). | `<a definir>` |
| T3 | [Lucas] | CERT-02, CERT-03 | geração do certificado | T2 | Documento com dados corretos gerado/baixável (I3). | `<a definir>` |
| T4 | [Lucas] | CERT-05 | código de verificação | T3 | Código consultável valida autenticidade. | `<a definir>` |
| T5 | [Isabela] → [Marina] + [Ada] | CERT-01, CERT-02 | UI de liberação e emissão | T2 | Telas acessíveis para organizador e participante. | `<a definir>` |
| T6 | [Ricardo] | CERT-01..05 | testes | T2–T4 | Liberação, emissão e bloqueio sem liberação cobertos. | `<a definir>` |

## Matriz de testes

| Requisito | Tipo | Responsável | Comando/gate | Evidência esperada |
|---|---|---|---|---|
| CERT-01 | integration | [Ricardo] | `<a definir>` | Liberação habilita emissão a confirmados. |
| CERT-02/03 | e2e | [Ricardo] | `<a definir>` | Participante liberado emite com dados corretos. |
| CERT-04 | integration | [Ricardo] | `<a definir>` | Sem liberação → emissão negada. |
| CERT-05 | integration | [Ricardo] | `<a definir>` | Código de verificação confere. |

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Certificado com dado incorreto (carga horária) | Derivar carga horária das atividades do evento (SPEC-002); nunca digitar à mão (I3). |
| Emissão antes do término do evento | Checar data de término na liberação (I1). |
| Falsificação de certificado | Código de verificação (CERT-05) e, se necessário, assinatura. |

## Perguntas abertas

- **Q-01:** Formato do certificado (PDF? carga horária calculada ou informada?) — definir com a stack/UI.
- **Q-02:** Haverá check-in de presença em versão futura que automatize a liberação? (follow-up.)

## Validação

`/kairos-forge:validar SPEC-006`

## Próximo passo

`/kairos-forge:desenhar SPEC-006` → `/kairos-forge:mobilizar SPEC-006`.
