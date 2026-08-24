# Unidade III — Fórum: Diagrams as Code

> Pós-graduação em Engenharia de Software com IA — UFG.
> Resposta à atividade prática de documentação com diagramas como código (Unidade III).

Olá, pessoal! 👋

Segui com o mesmo sistema das atividades anteriores — o **Sistema de Gestão de Eventos da Eventus** (inscrições em congressos e workshops, controle de vagas, pagamentos, cancelamentos e certificados) — e conduzi a fase de discovery de documentação com *diagrams as code*.

**🔗 Repositório:** https://github.com/allysonbarros/mc10-engenharia-requisitos-ia

Tudo está na seção **"📐 Documentação do sistema — diagrams as code"** do README:

- a **descrição do sistema em linguagem natural** (escopo, nível da visão, limites e responsabilidades, integrações, restrições e lacunas);
- um **diagrama estrutural** — visão de containers inspirada no C4 (Next.js como BFF, API Rails 8, PostgreSQL, jobs assíncronos, Mercado Pago);
- um **diagrama comportamental** — sequência da jornada crítica: inscrição em evento pago com Pix, do `UPDATE` atômico que reserva a vaga até o webhook do gateway;
- e um bônus: a **máquina de estados** do ciclo de vida de uma inscrição.

Tudo em Mermaid, renderizando direto no GitHub. O que mais me convenceu da abordagem na prática: como o diagrama é texto, ele entrou **no mesmo commit e na mesma revisão** que as SPECs e ADRs que ele referencia — documentação visual e requisitos evoluem juntos, sem ferramenta externa nem imagem desatualizada.

## O que o modelo inferiu corretamente

Como o repositório já tinha SPECs, ADRs e modelos de ameaça das unidades anteriores, o modelo teve contexto rico — e usou bem:

- A arquitetura **Web/BFF (Next.js) ↔ API (Rails 8) ↔ PostgreSQL** com sessão em cookie httpOnly, fiel ao nosso ADR de autenticação — não caiu no clichê de "JWT no localStorage";
- O **UPDATE condicional atômico** como mecanismo anti-overbooking e a **reserva de vaga com timeout de 15 min** contando como vaga ocupada;
- O trio de segurança do webhook de pagamento (**assinatura + reconsulta + idempotência**), extraído do threat model;
- A escolha da **jornada crítica**: apontou o fluxo de evento *pago* (e não o gratuito) como o que concentra mais risco e decisões.

## O que precisei ajustar

1. **Sintaxe:** o modelo gerou primeiro em `C4Container` nativo do Mermaid; converti para `flowchart` com subgraph e classes de cor, porque o suporte C4 do Mermaid é experimental e renderiza mal no GitHub. Mantive a semântica C4 (pessoas / containers / sistemas externos) por convenção visual.
2. **Removi um Redis** que ele inventou "para o contador de inscritos em tempo real" — nenhum ADR decidiu isso; diagrama não é lugar de tomar decisão nova.
3. **Rebaixei o serviço de e-mail** de fato consumado para container **tracejado "a definir"** — o canal de notificações é ponto em aberto da elicitação, e o diagrama precisa ser honesto sobre isso.
4. **Tirei o boleto** da sequência de pagamento — está fora do MVP por decisão registrada em ADR (a confirmação em 1–2 dias briga com a reserva de 15 min).
5. **Rotulei os jobs assíncronos como premissa sem ADR** — a expiração de reserva implica um executor, mas ele ainda não foi decidido.
6. **Amarrei cada elemento a um ID rastreável** (SPEC, invariante, ADR) nos próprios rótulos, para o diagrama ser auditável contra a documentação.

O padrão que emergiu: o modelo acerta o que está **escrito e decidido**, e erra por **excesso de completude** — preenche lacunas com o "default da indústria" (Redis, e-mail transacional, boleto). O trabalho humano foi menos corrigir e mais **rebaixar inferência a premissa** e devolver lacuna a lacuna.

## O que faltaria para um agente construir sem inventar decisões

- **ADR de hospedagem/deploy** — hoje a topologia de produção teria que ser inventada;
- **Contrato OpenAPI** da API — o diagrama de sequência insinua rotas e códigos de erro, mas não os especifica;
- **ADR do executor de jobs** e da estratégia do contador em tempo real (polling vs. push);
- As **decisões de negócio pendentes**: canal e formato das notificações, quais dados do participante o palestrante enxerga (LGPD!), taxa do gateway no reembolso e prazo default de reembolso;
- **Números de RNF confirmados** (latência, disponibilidade, acessibilidade) — hoje são premissas;
- Um **ERD** como próximo diagrama estrutural, um nível abaixo da visão de containers.

Ou seja: os diagramas fecham a visão macro, mas um agente honesto ainda teria que **parar e perguntar** essas seis coisas — e é exatamente esse o comportamento que a documentação deve induzir, em vez de deixar o agente decidir por mim. 😄

Vou passar no repositório de um colega para deixar uma sugestão. Abraços! 🚀
