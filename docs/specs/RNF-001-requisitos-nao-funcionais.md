# RNF-001 — Requisitos não-funcionais

> Autores: **Norma (NFR)** coordena · **Helena (Segurança)** · **Ada (Acessibilidade)** · **Vinícius (Performance)** · **Renata (Observabilidade)**.
> Escopo: **transversal** — restringe todas as SPECs. `/kairos-forge:validar` e `/kairos-forge:revisar` devem checar estes gates.

## Contexto

A observação #9 da elicitação registra que "não foram levantados requisitos relacionados à segurança, desempenho, disponibilidade, acessibilidade e privacidade dos dados". Este documento cobre essa lacuna com requisitos não-funcionais rastreáveis. **Metas numéricas estão marcadas como premissa "(a confirmar)"** — são pontos de partida razoáveis, não fatos elicitados; ajuste com o negócio.

## Segurança

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| RNF-SEG-01 | Credenciais protegidas | P1 | Senhas SHALL ser armazenadas só como hash forte (ex.: bcrypt/argon2); nunca em texto claro ou log. | Pendente | — |
| RNF-SEG-02 | Transporte cifrado | P1 | Todo tráfego SHALL usar TLS; sem endpoints em texto claro em produção. | Pendente | — |
| RNF-SEG-03 | OWASP Top 10 | P1 | Entradas SHALL ser validadas/escapadas; injeção, XSS e CSRF mitigados. Auditoria Helena antes de PR. | Pendente | — |
| RNF-SEG-04 | Sem secrets no código | P1 | Nenhum secret/credencial SHALL estar versionado; uso de cofre/variáveis de ambiente. | Pendente | — |
| RNF-SEG-05 | Autorização server-side | P1 | Toda decisão de acesso SHALL ocorrer no backend, com menor privilégio (liga a SPEC-009/I2). | Pendente | — |
| RNF-SEG-06 | Proteção contra abuso | P2 | Endpoints sensíveis (login, pagamento) SHALL ter rate limiting e proteção contra enumeração. | Pendente | — |

## Desempenho

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| RNF-DES-01 | Latência do catálogo | P2 | Listagem/detalhe de eventos SHALL responder em < 500ms p95 sob carga nominal (premissa — a confirmar). | Pendente | — |
| RNF-DES-02 | Latência da inscrição | P2 | Confirmação de inscrição SHALL responder em < 1s p95, inclusive sob concorrência (premissa — a confirmar). | Pendente | — |
| RNF-DES-03 | Pico de concorrência | P2 | O sistema SHALL sustentar o pico de inscrições simultâneas na abertura de um evento popular sem overbooking nem degradação grave (alvo de vazão a confirmar). | Pendente | — |

## Disponibilidade e confiabilidade

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| RNF-DIS-01 | Disponibilidade | P2 | O sistema SHALL ter disponibilidade-alvo de 99,5%/mês (premissa — a confirmar). | Pendente | — |
| RNF-DIS-02 | Consistência de vagas sob falha | P1 | Em falha parcial, o sistema SHALL priorizar não permitir overbooking (consistência sobre disponibilidade nesse ponto — liga a SPEC-001/I1). | Pendente | — |
| RNF-DIS-03 | Backup e recuperação | P1 | Dados SHALL ter backup periódico; RPO/RTO definidos (premissa — a confirmar). | Pendente | — |

## Acessibilidade

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| RNF-ACE-01 | Conformidade WCAG | P1 | Telas voltadas ao usuário SHALL atender WCAG 2.1 nível AA (validação Ada). | Pendente | — |
| RNF-ACE-02 | Teclado e leitor de tela | P1 | Fluxos críticos (catálogo, inscrição, certificado) SHALL ser navegáveis por teclado e compatíveis com leitor de tela; contraste adequado. | Pendente | — |

## Privacidade e LGPD

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| RNF-PRI-01 | Minimização de dados | P1 | O sistema SHALL coletar e expor apenas dados necessários (ex.: palestrante vê só nome — SPEC-008/I1). | Pendente | — |
| RNF-PRI-02 | Base legal/consentimento | P1 | O cadastro SHALL registrar consentimento e a finalidade do tratamento (liga a SPEC-009/AUTH-07). | Pendente | — |
| RNF-PRI-03 | Direitos do titular | P1 | O titular SHALL poder acessar e solicitar exclusão dos seus dados. | Pendente | — |
| RNF-PRI-04 | Retenção e descarte | P2 | Dados pessoais SHALL ter prazo de retenção e descarte definidos (premissa — a confirmar). | Pendente | — |
| RNF-PRI-05 | Trilha de auditoria | P2 | Acessos a dados pessoais sensíveis SHALL ser auditáveis. | Pendente | — |

## Observabilidade (habilitadora dos NFRs acima)

| ID | Requisito | Prioridade | Critério de aceite | Status | Verificação |
|---|---|---|---|---|---|
| RNF-OBS-01 | Logs estruturados + correlação | P2 | Fluxos cross-componente (inscrição, pagamento, promoção) SHALL ter logs estruturados com correlation ID (Renata). | Pendente | — |
| RNF-OBS-02 | Métricas e alertas | P2 | Métricas de latência, erro e vazão SHALL ser expostas, com alertas nos limiares dos RNF-DES/DIS. | Pendente | — |

## Como estes RNFs entram no fluxo

- **Por SPEC:** cada SPEC de feature deve referenciar os RNFs aplicáveis nos seus gates (ex.: toda UI → RNF-ACE-01/02; todo endpoint → RNF-SEG-03/05).
- **Na validação:** `/kairos-forge:validar` trata RNF P1 sem evidência como bloqueio, igual a requisito funcional.
- **Na revisão:** Helena (segurança), Vinícius (performance), Ada (acessibilidade) verificam seus RNFs em `/kairos-forge:revisar`.

## Perguntas abertas (metas a confirmar com o negócio)

- Volume esperado: nº de eventos/mês, participantes/evento, pico de inscrições na abertura.
- SLA de disponibilidade real exigido (99,5%? 99,9%?).
- RPO/RTO aceitáveis para recuperação.
- Prazo de retenção de dados pessoais.
- MFA obrigatório para papéis sensíveis? (herda SPEC-009/Q-02.)

## Validação

`/kairos-forge:validar RNF-001`
