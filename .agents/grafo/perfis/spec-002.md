# Perfil — SPEC-002

**Tipo:** SPEC · **Grau:** 14 · **Intervalo temporal:** 2026-07-29

SPEC-002 é a SPEC **fundacional** de gestão de eventos: o organizador cria eventos, define capacidade e tipo (gratuito/pago), cadastra atividades com horários e configura as políticas de cancelamento e reembolso. Sem ela, nada em SPEC-001 (inscrição) funciona — daí ser pré-requisito direto.

Ela `implementa` a feature Gestão de eventos e `decidiu usar` a **Política configurável por evento** — a decisão de que cada evento define suas próprias regras de cancelamento e reembolso, em vez de uma regra global. Essa decisão é depois consumida por SPEC-004 (cancelamento) e SPEC-005 (reembolso), que `dependem de` a política.

SPEC-002 `depende de` SPEC-009, porque distinguir organizador de participante exige autenticação e papéis. É classificada por Laura, documentada por Fernanda e Diego, testada por Ricardo, restringida por RNF-001 e bloqueada por Escolha de stack e banco.

**Fatos-chave (rastreáveis):**
- (SPEC-002) --[implementa]--> (Gestão de eventos) [SPEC-002]
- (SPEC-002) --[decidiu usar]--> (Política configurável por evento) [SPEC-002]
- (SPEC-002) --[depende de]--> (SPEC-009) [SPEC-002]
- (SPEC-001/003/004/006/008) --[depende de]--> (SPEC-002) [respectivas SPECs]
