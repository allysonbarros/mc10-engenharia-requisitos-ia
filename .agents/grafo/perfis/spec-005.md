# Perfil — SPEC-005

**Tipo:** SPEC · **Grau:** 14 · **Intervalo temporal:** 2026-07-29

SPEC-005 cobre pagamento, confirmação e reembolso para eventos pagos — a SPEC mais **complexa** do backlog, por lidar com integração externa, dado financeiro e PII, com reversibilidade baixa. Ela `implementa` as features Pagamento e Reembolso.

Suas dependências revelam o encadeamento crítico: `depende de` SPEC-001 (reserva de vaga durante o pagamento), `depende de` SPEC-009 (papéis, sobretudo a Equipe Financeira que confirma pagamentos) e `depende de` a Política configurável por evento (regra de reembolso). SPEC-007 `consome` seus eventos para notificar a confirmação de pagamento.

Está bloqueada por dois pontos: a **Escolha de stack e banco** (como todas) e, especificamente, o **Provedor de pagamento** — decisão em aberto sem a qual o fluxo de integração não fecha. Por ser sensível, exige rodar `/kairos-forge:analisar-ameacas` antes de implementar. É documentada por Thiago, Fernanda e Helena (segurança obrigatória), classificada por Laura e testada por Ricardo.

**Fatos-chave (rastreáveis):**
- (SPEC-005) --[implementa]--> (Pagamento) / (Reembolso) [SPEC-005]
- (SPEC-005) --[depende de]--> (SPEC-001) / (SPEC-009) [SPEC-005]
- (Provedor de pagamento) --[bloqueia]--> (SPEC-005) [SPEC-005]
- (Helena) --[documenta]--> (SPEC-005) [SPEC-005]
