# Backlog, Épicos e Roadmap de Sprints — Eventus

> Conduzido por Camila (PM), com Hugo (priorização), Caio (critérios de aceite) e Iara (planejamento).
> **Fonte:** derivado das SPECs em `docs/specs/` — cada história aponta para um requisito rastreável (ID da SPEC).
> **Data:** 2026-07-30.

## Premissas de planejamento

| Parâmetro | Valor | Observação |
|---|---|---|
| Cadência de sprint | **1 semana** | Definido com o time |
| Capacidade | **Fábrica kairos-forge** (agentes especialistas em paralelo) | Vazão limitada por dependências e ciclos de gate/validação/revisão, não por "mãos" |
| Escala de estimativa | **Story points (Fibonacci)** — 1,2,3,5,8,13 | Complexidade relativa |
| Velocidade inicial | **~20 SP/sprint** (premissa) | Calibrar empiricamente após o Sprint 1 |
| Priorização | **MoSCoW** derivado de P1→Must, P2→Should, P3→Could | Ver mapa por história |

> Estimativas e velocidade são **planejamento**, não fato. São premissas a calibrar — não confundir com os requisitos das SPECs, que são o contrato.

## Épicos

| Épico | Nome | SPEC(s) de origem | Objetivo |
|---|---|---|---|
| **E0** | Fundação Técnica & Qualidade | ADR-0001/0002/0003, RNF-001, DESIGN-002 | Esqueleto Rails+Next, CI, design system, gates de qualidade |
| **E1** | Identidade e Acesso | SPEC-009 + AMEACAS-auth | Autenticação, RBAC, isolamento, hardening de segurança |
| **E2** | Gestão de Eventos | SPEC-002 | Organizador cria, configura e publica eventos e atividades |
| **E3** | Descoberta de Eventos | SPEC-003 | Catálogo público de eventos disponíveis |
| **E4** | Jornada de Inscrição | SPEC-001 + SPEC-004 | Inscrição, controle de vagas, lista de espera, cancelamento e promoção |
| **E5** | Pagamentos e Financeiro | SPEC-005 + AMEACAS-pagamento | Pagamento (Pix/cartão), confirmação, reembolso |
| **E6** | Certificação | SPEC-006 | Liberação e emissão de certificados |
| **E7** | Comunicação e Notificações | SPEC-007 | Comprovantes e avisos transacionais (canal desacoplado) |
| **E8** | Experiência do Palestrante | SPEC-008 | Painel do palestrante com dados mínimos (LGPD) |

Dependências entre épicos (do grafo de conhecimento): **E0 → E1 → E2 → {E3, E4, E6, E8}**; **E4 → E5**; **E7** é transversal (consome eventos de E4/E5).

## Backlog priorizado

Legenda: **MoSCoW** (Must/Should/Could) · **SP** (story points) · **Dep** (depende de) · **Req** (requisito rastreável na SPEC).

### E0 — Fundação Técnica & Qualidade

| ID | História | MoSCoW | SP | Dep | Req/Fonte |
|---|---|---|---|---|---|
| E0-01 | Como time, quero o scaffold do backend Rails API com Postgres, para ter a base do servidor. | Must | 5 | — | ADR-0001 |
| E0-02 | Como time, quero o scaffold do frontend Next.js com BFF, para ter a base do cliente. | Must | 5 | — | ADR-0001/0002 |
| E0-03 | Como time, quero CI (GitHub Actions) rodando os gates, para travar qualidade desde o commit 0. | Must | 5 | E0-01, E0-02 | `contextos/testes.md` |
| E0-04 | Como time, quero tokens + componentes base (design system), para não espalhar estilo solto. | Must | 13 | E0-02 | DESIGN-002 |
| E0-05 | Como time, quero logs estruturados com correlation ID, para observabilidade dos fluxos. | Should | 5 | E0-01 | RNF-OBS-01 |

### E1 — Identidade e Acesso

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E1-01 | Como usuário, quero me autenticar, para acessar o sistema com minha identidade. | Must | 8 | E0-01,02 | AUTH-01 |
| E1-02 | Como titular, quero me cadastrar fornecendo o mínimo e consentindo, para respeitar a LGPD. | Must | 5 | E1-01 | AUTH-07, RNF-PRI-02 |
| E1-03 | Como usuário, quero sessão segura (httpOnly, expiração, logout), para proteger minha conta. | Must | 5 | E1-01 | AUTH-05, AMEACAS-auth/M5 |
| E1-04 | Como admin, quero atribuir papéis a usuários, para definir o que cada um acessa. | Must | 3 | E1-01 | AUTH-02 |
| E1-05 | Como responsável por segurança, quero autorização por policy server-side, para impedir escalada de privilégio. | Must | 8 | E1-04 | AUTH-03, AMEACAS-auth/M1 |
| E1-06 | Como organizador/palestrante, quero acessar só meus recursos, para respeitar o isolamento. | Must | 5 | E1-05 | AUTH-04, AMEACAS-auth/M4 |
| E1-07 | Como usuário, quero recuperar minha senha com segurança, para não perder acesso. | Must | 5 | E1-01 | AMEACAS-auth/AP-02/M2 |
| E1-08 | Como responsável por segurança, quero rate limit e lockout no login, para barrar força bruta. | Should | 3 | E1-01 | AMEACAS-auth/M3, RNF-SEG-06 |
| E1-09 | Como usuário, quero política mínima de senha, para reduzir risco de conta fraca. | Should | 3 | E1-01 | AUTH-06 |
| E1-10 | Como responsável por segurança, quero proteção CSRF nas ações state-changing, para evitar requests forjadas. | Should | 2 | E1-03 | AMEACAS-auth/M6 |

### E2 — Gestão de Eventos

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E2-01 | Como organizador, quero criar um evento (nome, período, capacidade), para abrir inscrições. | Must | 5 | E1-05 | EVT-01, EVT-08 |
| E2-02 | Como organizador, quero marcar o evento como gratuito ou pago, para definir se exige pagamento. | Must | 2 | E2-01 | EVT-02 |
| E2-03 | Como organizador, quero cadastrar atividades com início e fim, para montar a programação. | Must | 5 | E2-01 | EVT-03 |
| E2-04 | Como organizador, quero definir a política de cancelamento, para controlar desistências. | Must | 3 | E2-01 | EVT-04 |
| E2-05 | Como organizador, quero definir a política de reembolso do evento pago, para deixar claro o direito. | Should | 3 | E2-02 | EVT-05 |
| E2-06 | Como organizador, quero publicar/despublicar um evento, para controlar sua visibilidade. | Must | 3 | E2-01 | EVT-06 |
| E2-07 | Como organizador, quero ver a lista dos meus eventos com status, para gerenciá-los. | Should | 3 | E2-01 | EVT-07 |
| E2-08 | Como organizador, quero as telas de gestão (5 estados, acessíveis), para operar sem fricção. | Must | 8 | E0-04, E2-01 | DESIGN-002 V-01..10 |

### E3 — Descoberta de Eventos

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E3-01 | Como participante, quero ver todos os eventos disponíveis num só lugar, para escolher. | Must | 3 | E2-06 | CAT-01, CAT-05 |
| E3-02 | Como participante, quero ver o detalhe de um evento, para decidir me inscrever. | Must | 3 | E3-01 | CAT-02 |
| E3-03 | Como participante, quero saber quando um evento está lotado, para não perder tempo. | Must | 2 | E3-01 | CAT-03 |
| E3-04 | Como participante, quero filtrar/buscar eventos, para achar mais rápido. | Could | 5 | E3-01 | CAT-04 |
| E3-05 | Como participante, quero a vitrine acessível (5 estados), para navegar bem. | Must | 5 | E0-04, E3-01 | CAT-01..04 |

### E4 — Jornada de Inscrição

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E4-01 | Como participante, quero me inscrever em evento gratuito com vaga, para garantir participação. | Must | 5 | E2-06 | INSCR-01 |
| E4-02 | Como organizador, quero que o sistema nunca exceda a capacidade (concorrência), para não vender vaga a mais. | Must | 13 | E4-01 | INSCR-02 |
| E4-03 | Como participante, quero entrar na lista de espera quando lotado, para ser considerado. | Must | 5 | E4-02 | INSCR-03 |
| E4-04 | Como participante, quero ser impedido de me inscrever em atividade com horário conflitante. | Must | 5 | E4-01 | INSCR-04 |
| E4-05 | Como participante, quero me inscrever em várias atividades no mesmo dia sem conflito. | Should | 2 | E4-04 | INSCR-05 |
| E4-06 | Como organizador, quero acompanhar inscritos em tempo real, para gerir o evento. | Must | 5 | E4-01 | INSCR-06 |
| E4-07 | Como participante, quero ver uma confirmação/comprovante após me inscrever. | Must | 3 | E4-01 | INSCR-07 |
| E4-08 | Como participante, quero ver quantas vagas restam, para decidir. | Should | 2 | E4-01 | INSCR-08 |
| E4-09 | Como organizador, quero impedir inscrição duplicada, para manter a integridade das vagas. | Must | 3 | E4-01 | INSCR-09 |
| E4-10 | Como participante, quero cancelar minha inscrição, para liberar minha vaga. | Must | 3 | E4-01, E2-04 | CANC-01, CANC-02 |
| E4-11 | Como participante em espera, quero ser promovido quando abrir vaga (aviso + prazo 24h). | Must | 8 | E4-03, E4-10 | CANC-03 |
| E4-12 | Como organizador, quero que a vaga passe ao próximo se o promovido não confirmar. | Should | 5 | E4-11 | CANC-04 |
| E4-13 | Como participante, quero poder sair da lista de espera, para não ser promovido se desistir. | Should | 2 | E4-03 | CANC-05 |
| E4-14 | Como participante, quero as telas de inscrição (5 estados, acessíveis). | Must | 8 | E0-04, E4-01 | INSCR-07, INSCR-08 |

### E5 — Pagamentos e Financeiro

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E5-01 | Como participante, quero pagar via Pix ou cartão para confirmar inscrição em evento pago. | Must | 8 | E4-01, E1-05 | PAG-01, PAG-07 |
| E5-02 | Como organizador, quero a vaga reservada durante o pagamento (timeout 15min), para não vender duas vezes. | Must | 8 | E5-01, E4-02 | PAG-02 |
| E5-03 | Como organizador, quero liberar a vaga se o pagamento não se concretizar, para não travá-la. | Must | 5 | E5-02 | PAG-03 |
| E5-04 | Como responsável por segurança, quero confirmação por webhook validado e idempotente, para não confirmar fraude. | Must | 8 | E5-01 | AMEACAS-pagamento/M1,M2 |
| E5-05 | Como equipe financeira, quero confirmar e acompanhar pagamentos, para liberar inscrições corretamente. | Must | 5 | E5-01 | PAG-04 |
| E5-06 | Como participante, quero reembolso conforme a regra (total até prazo), para reaver o valor. | Should | 5 | E4-10, E5-01 | PAG-05, CANC-06 |
| E5-07 | Como participante de evento gratuito, quero me inscrever sem pagar, para não haver fricção. | Must | 2 | E4-01 | PAG-06 |
| E5-08 | Como participante, quero as telas de pagamento (5 estados, acessíveis). | Must | 5 | E0-04, E5-01 | SPEC-005 |

### E6 — Certificação

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E6-01 | Como organizador, quero liberar os certificados de um evento, para controlar quem recebe. | Must | 3 | E4-01, E2-01 | CERT-01, CERT-04 |
| E6-02 | Como participante, quero emitir meu certificado após o evento, para comprovar participação. | Must | 5 | E6-01 | CERT-02, CERT-03 |
| E6-03 | Como terceiro, quero verificar a autenticidade de um certificado, para confiar nele. | Could | 5 | E6-02 | CERT-05 |
| E6-04 | Como usuário, quero as telas de liberação e emissão (acessíveis). | Should | 5 | E0-04, E6-01 | SPEC-006 |

### E7 — Comunicação e Notificações

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E7-01 | Como time, quero uma interface de canal de notificação desacoplada, para trocar de provedor sem mexer na regra. | Must | 5 | E0-01 | NOT-05 |
| E7-02 | Como time, quero disparo idempotente (outbox), para não enviar notificação duplicada. | Must | 8 | E7-01 | NOT-06 |
| E7-03 | Como participante, quero um comprovante ao me inscrever. | Must | 3 | E7-01, E4-01 | NOT-01 |
| E7-04 | Como participante, quero ser avisado ao entrar e ao ser promovido na lista de espera. | Must | 3 | E7-02, E4-11 | NOT-02 |
| E7-05 | Como participante, quero ser avisado do cancelamento e da confirmação de pagamento. | Should | 3 | E7-02 | NOT-03, NOT-04 |

### E8 — Experiência do Palestrante

| ID | História | MoSCoW | SP | Dep | Req |
|---|---|---|---|---|---|
| E8-01 | Como palestrante, quero ver minhas atividades e programação, para me organizar. | Must | 3 | E1-06, E2-03 | PAL-01 |
| E8-02 | Como palestrante, quero ver os participantes das minhas atividades (só nome), para conhecer o público. | Must | 3 | E8-01, E4-01 | PAL-02, PAL-03 |
| E8-03 | Como responsável por LGPD/segurança, quero garantir minimização e isolamento no painel. | Must | 3 | E8-02 | PAL-03, PAL-04 |
| E8-04 | Como palestrante, quero o painel acessível (somente leitura). | Should | 3 | E0-04, E8-01 | SPEC-008 |

**Total aproximado:** ~285 SP.

## Roadmap de sprints (1 semana cada)

> Sequenciado pelas dependências do grafo. Cada sprint tem um **objetivo demonstrável** (Working Backwards). Velocidade-alvo ~20 SP (premissa).

| Sprint | Objetivo (o que fica demonstrável) | Histórias | ~SP |
|---|---|---|---|
| **S1** | Esqueleto rodando: Rails+Next sobem, CI verde, design system base. | E0-01, E0-02, E0-03, E0-04 (início) | 20 |
| **S2** | Login e cadastro seguros: usuário autentica, sessão protegida, reset de senha. | E0-04 (fim), E1-01, E1-02, E1-03, E1-07 | 21 |
| **S3** | RBAC completo: papéis, autorização server-side, isolamento; começa criação de evento. | E1-04, E1-05, E1-06, E1-08, E1-09, E1-10 | 24 |
| **S4** | Organizador cria, configura e publica eventos com atividades. | E2-01..E2-08 | 32 → *dividir se velocidade < 25* |
| **S5** | Participante descobre e se inscreve sem overbooking. | E3-01,02,03,05, E4-01, E4-02, E4-09 | 29 |
| **S6** | Inscrição completa: lista de espera, conflito de horário, tempo real, comprovante. | E4-03,04,05,06,07,08, E4-14, E7-01 | 35 → *dividir* |
| **S7** | Cancelamento libera vaga e promove a fila com aviso. | E4-10,11,12,13, E7-02,03,04,05 | 30 |
| **S8** | Eventos pagos: Pix/cartão, reserva, webhook seguro, reembolso, painel financeiro. | E5-01..E5-08 | 46 → *provável 2 sprints* |
| **S9** | Certificação e painel do palestrante. | E6-01..04, E8-01..04 | 33 |
| **S10** | Hardening & lançamento: RNF completos, a11y/perf, PR final, `/lancar`. | E0-05, E3-04, E6-03, backlog residual + gates | ~20 |

> **Nota de realismo:** vários sprints (S4, S6, S8) passam de 30 SP — provável que, com velocidade real de ~20, virem 1,5–2 sprints cada. O total sugere **~12–14 semanas** de execução. Isso será ajustado após medir a velocidade do Sprint 1 (a fábrica pode entregar mais por paralelismo, ou menos por ciclos de revisão — só medindo).

## MoSCoW — visão executiva

- **Must (MVP demonstrável):** E0 completo, E1 (auth/RBAC), E2 (eventos), E3 núcleo, E4 (inscrição+cancelamento), E5 núcleo (Pix/cartão), E6 emissão, E7 comprovante/promoção, E8 painel mínimo.
- **Should (V1.1):** filtros de busca, expiração de promoção, reembolso, política de reembolso, notificações de cancelamento/pagamento.
- **Could (V2):** verificação de autenticidade de certificado, busca avançada.
- **Won't (fora do escopo agora):** boleto, MFA, SSO/OAuth, multi-idioma — registrados como não-objetivos nas SPECs.

## Como este backlog se conecta à fábrica

- **Cada história → um requisito rastreável** da SPEC (coluna Req). Rastreabilidade auditável.
- **Execução:** cada história vira tarefas em `/kairos-forge:mobilizar SPEC-NNN`, com os agentes já nomeados nas SPECs (Carlos, Lucas, Marina, Pablo, Ada, Ricardo…).
- **Aceite:** os critérios `WHEN…THEN…SHALL` das SPECs são o teste da história; `/kairos-forge:validar` cobra.
- **Detalhamento:** ver `docs/planejamento/historias-detalhadas.md` para os cards completos (descrição, critérios de aceite, DoD, agentes, pontos) das histórias dos primeiros sprints.
