# Perfil — SPEC-001

**Tipo:** SPEC · **Grau:** 17 (maior hub do grafo) · **Intervalo temporal:** 2026-07-29

SPEC-001 é a **feature-âncora** do sistema Eventus: a inscrição de participante em evento gratuito com controle de vagas. Ela implementa quatro capacidades — Inscrição em evento, Controle de vagas, Lista de espera e Bloqueio de conflito de horário — e é o nó mais conectado do grafo, o que reflete seu papel central: quase toda outra SPEC depende dela ou consome seus eventos.

Do lado das dependências de saída, SPEC-001 `depende de` SPEC-002 (os eventos precisam existir antes de alguém se inscrever) e registrou duas decisões próprias via `decidiu usar`: o **Escopo só eventos gratuitos** (pagamento foi empurrado para SPEC-005) e o **UPDATE condicional atômico** como estratégia de concorrência para nunca estourar vagas. Do lado das dependências de entrada, SPEC-004, SPEC-005 e SPEC-006 `dependem de` SPEC-001, e SPEC-007 `consome` seus eventos de domínio para notificar.

Como toda SPEC de feature, é classificada por Laura (`responsável por`), documentada por Diego e Fernanda, testada por Ricardo (`valida`) e restringida por RNF-001. Está bloqueada, junto de todas as demais, pela decisão pendente **Escolha de stack e banco**.

**Fatos-chave (rastreáveis):**
- (SPEC-001) --[implementa]--> (Controle de vagas) [SPEC-001]
- (SPEC-001) --[decidiu usar]--> (UPDATE condicional atômico) [SPEC-001]
- (SPEC-001) --[depende de]--> (SPEC-002) [SPEC-002]
- (SPEC-004/005/006) --[depende de]--> (SPEC-001) [respectivas SPECs]
- (Escolha de stack e banco) --[bloqueia]--> (SPEC-001) [contextos/stack.md]
