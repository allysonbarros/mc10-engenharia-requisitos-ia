# Atividade Prática — Fórum de Discussão

> Pós-graduação em Engenharia de Software com IA — UFG.
> Resposta à atividade prática de especificação de requisitos apoiada por IA Generativa.

Olá, pessoal! 👋

Compartilho minha atividade prática. Parti do documento de elicitação de um **Sistema de Gestão de Eventos** (empresa fictícia "Eventus" — inscrições em congressos/workshops, controle de vagas, pagamentos, cancelamentos e certificados) e usei IA Generativa como apoio para transformar aquele texto solto em um conjunto de artefatos de especificação rastreáveis.

**🔗 Repositório:** https://github.com/allysonbarros/mc10-engenharia-requisitos-ia

## Artefatos que decidi produzir

Em vez de um único artefato, montei um **encadeamento rastreável** (cada peça aponta para a anterior):

- **Requisitos especificados (SPECs)** — 10 documentos (9 features + 1 de requisitos não-funcionais), com IDs estáveis e **critérios de aceitação verificáveis** no formato `WHEN … THEN … SHALL …`.
- **Requisitos não-funcionais (RNF)** — segurança, desempenho, disponibilidade, acessibilidade e privacidade/LGPD, que a elicitação explicitamente **não** havia levantado.
- **Histórias de usuário + backlog ágil** — 9 épicos, ~63 histórias com priorização MoSCoW, story points e roadmap de sprints.
- **Critérios de aceitação visuais** e **protótipos de design (handoff)** — fluxos de tela, os 5 estados de cada view, responsivo e acessibilidade.
- **ADRs (registros de decisão arquitetural)** e **modelos de ameaça (threat models)** para as áreas sensíveis (pagamento e autenticação).
- **Grafo de conhecimento** ligando SPECs, decisões e dependências.
- Por fim, materializei o backlog como **63 issues + 10 milestones + um Project board (Kanban)** no próprio GitHub.

## Por que considerei esses artefatos os mais adequados

O documento de elicitação tinha **lacunas e ambiguidades reais** (9 pontos em aberto: prazo de cancelamento, regras de reembolso, funcionamento da lista de espera etc.) e **omitia os requisitos não-funcionais**. Então eu não precisava de um artefato que só *descrevesse* — precisava de artefatos que **expusessem e resolvessem** essas lacunas:

- **História de usuário + critério de aceitação** (`WHEN/THEN/SHALL`) tornam cada requisito **testável** e evitam o "requisito vago".
- **ADRs** registram o *porquê* das decisões (stack, autenticação, gateway de pagamento) de forma permanente.
- **Threat models** anteciparam riscos onde eles doem (fraude no pagamento, tomada de conta) **antes** de implementar.
- **Protótipos/design handoff** deram forma às telas com critérios verificáveis, não intenções.
- A **rastreabilidade ponta a ponta** (requisito → história → issue → sprint) é o que torna o conjunto auditável — algo muito valorizado em engenharia de requisitos.

## Como a Inteligência Artificial Generativa apoiou

Usei uma abordagem de **desenvolvimento guiado por especificação (spec-driven)**, com a IA atuando como uma "fábrica" de agentes especialistas (papéis de tech lead, arquiteto, segurança, UX, PM). A IA ajudou a:

- **Identificar** requisitos funcionais, regras de negócio e RNFs a partir do texto de elicitação;
- **Apontar as ambiguidades** e transformá-las em perguntas objetivas de decisão;
- **Gerar rascunhos** dos artefatos (SPECs, ADRs, backlog, designs) com estrutura consistente;
- **Propor alternativas com trade-offs** (ex.: estratégias de controle de concorrência de vagas) e recomendar uma.

O ponto que mais me marcou foi a **disciplina de não inventar**: sempre que faltava uma informação de negócio, a IA **parava e perguntava** em vez de preencher com achismo.

## O que foi aproveitado, modificado e descartado

- **Aproveitei:** a estrutura de critérios de aceitação `WHEN/THEN/SHALL`; a recomendação técnica de garantir o não-overbooking por *UPDATE condicional atômico* no banco; as mitigações dos threat models; e a ideia de **extrair uma fundação de design compartilhada** em vez de repetir componentes em cada tela.
- **Modifiquei:** a IA sugeriu criar artefato de design para **todas** as SPECs — reduzi isso apenas às que têm interface real e criei um documento-base único; também ajustei o dimensionamento dos sprints, que estavam otimistas demais.
- **Descartei / decidi eu mesmo:** as **regras de negócio inventáveis** (fórmula de reembolso, prazo de cancelamento, política da lista de espera) — a IA se recusou a chutá-las e **eu** as defini; os **números de RNF** ficaram marcados como *premissa a confirmar*, não como fato; a **escolha da stack** (Ruby on Rails + Next.js) foi minha decisão explícita, não o padrão sugerido; e removi o **boleto** do escopo de pagamento por ser incompatível com a reserva curta de vaga.

No fim, o maior aprendizado foi perceber que a IA Generativa é excelente para **acelerar e estruturar**, mas as **decisões irreversíveis e as regras de negócio** continuam sendo responsabilidade humana — e um bom processo é justamente o que separa uma coisa da outra.

Abraços! 🚀
