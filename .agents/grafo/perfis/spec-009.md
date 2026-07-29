# Perfil — SPEC-009

**Tipo:** SPEC · **Grau:** 11 · **Intervalo temporal:** 2026-07-29

SPEC-009 define autenticação e papéis (RBAC) para os cinco stakeholders, preenchendo a parte de controle de acesso da observação #9 (que não fora elicitada). Ela `implementa` as features Autenticação e Autorização RBAC, com menor privilégio e verificação server-side.

É um pré-requisito silencioso de várias features: os stakeholders Participante, Organizador, Equipe Financeira e Palestrante `dependem de` Autenticação (que SPEC-009 implementa), e as SPEC-002, SPEC-005 e SPEC-008 `dependem de` SPEC-009 para garantir seus isolamentos (organizador só mexe nos seus eventos; palestrante só vê suas atividades; financeiro só pagamentos).

Está bloqueada pela **Escolha de stack e banco** e, especificamente, pelo **Provedor de identidade** (decisão em aberto). Por ser sensível, pede `/analisar-ameacas` antes de implementar. Documentada por Helena, Diego e Rafael; classificada por Laura; testada por Ricardo.

**Fatos-chave (rastreáveis):**
- (SPEC-009) --[implementa]--> (Autenticação) / (Autorização RBAC) [SPEC-009]
- (SPEC-002/005/008) --[depende de]--> (SPEC-009) [respectivas SPECs]
- (Provedor de identidade) --[bloqueia]--> (SPEC-009) [SPEC-009]
- (Participante/Organizador/Equipe Financeira/Palestrante) --[depende de]--> (Autenticação) [SPEC-009]
