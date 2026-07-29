# Sistema de Gestão de Eventos — Eventus

> Projeto onboardado na fábrica **kairos-forge**. Este arquivo é a fonte de instruções do projeto para agentes.
> Se o time usar Codex/Cursor/OpenCode, manter `AGENTS.md` em sincronia com este arquivo.

## O que é este projeto

A **Eventus** organiza congressos, workshops e eventos corporativos. Hoje o gerenciamento de inscrições é feito com formulários on-line e planilhas eletrônicas, o que dificulta o controle de vagas, pagamentos, cancelamentos e emissão de certificados.

Com o crescimento do número de eventos, a empresa decidiu desenvolver um **sistema para centralizar essas atividades**, oferecendo melhor experiência aos participantes e maior controle aos organizadores.

O usuário final se divide em cinco perfis (stakeholders):

- **Participantes** — inscrevem-se em eventos, acompanham inscrições, cancelam participação e emitem certificados.
- **Organizadores** — criam eventos, controlam vagas, acompanham inscrições e gerenciam participantes.
- **Equipe Financeira** — confirma pagamentos e controla reembolsos.
- **Palestrantes** — consultam a programação e informações dos participantes de suas atividades.
- **Equipe de TI** — desenvolve e mantém o sistema.

> Contexto atual: este é um projeto em fase de **engenharia de requisitos** (disciplina MC10). O artefato de origem é `elicitacao.txt`. Ainda **não há decisão de implementação** — stack, arquitetura e código serão definidos nas próximas etapas.

Detalhes em `contextos/sobre-o-projeto.md`.

## Stack técnica

`<a preencher>` — ainda não definida. O projeto está na fase de requisitos; nenhuma linguagem, framework, banco ou hospedagem foi escolhido. Quando a decisão for tomada, registrar em `docs/adr/` (via arquiteto) e atualizar `contextos/stack.md`.

## Estrutura de pastas

```
.
├── elicitacao.txt              # Documento de elicitação (fonte de requisitos)
├── CLAUDE.md                   # Este arquivo
├── contextos/                  # Contexto persistente do projeto
├── decisoes/                   # Log de decisões + estado operacional da fábrica
├── docs/
│   ├── specs/                  # SPECs rastreáveis (via /kairos-forge:especificar)
│   │   └── validacoes/         # Relatórios de validação SPEC (via /validar)
│   └── adr/                    # Architecture Decision Records
└── .agents/
    ├── memory/                 # Memórias de incidente
    └── grafo/                  # Grafo de conhecimento do projeto
```

O que **não** deveria morar aqui: código de implementação ainda não tem lugar definido (será decidido junto com a stack). Detalhes em `contextos/stack.md` quando houver.

## Convenções não-óbvias

`<a preencher>` — sem base de código ainda. Definir estilo de commit, nomenclatura, padrões de erro e regras de dependência quando a implementação começar. Ver `contextos/convencoes.md`.

## O que está em andamento

Fase de **elicitação e especificação de requisitos**. O documento `elicitacao.txt` já levantou stakeholders, entrevistas e — importante — uma lista de **pontos em aberto** que precisam de definição antes de especificar (ver `contextos/restricoes.md`, seção "Questões em aberto").

Decisões pendentes destravadas pelo negócio (da seção "Observações" da elicitação):

1. Prazo-limite para cancelamento de inscrição.
2. Regras de reembolso (quando há direito, quando não).
3. Funcionamento da lista de espera.
4. Emissão de certificado: automática ou condicionada à confirmação de presença.
5. Canal e formato de envio de comprovantes/notificações.
6. Momento da reserva da vaga: no início do pagamento ou só após confirmação.
7. Tratamento de inscrições em atividades com horários conflitantes.
8. Quais dados do participante são visíveis ao palestrante.
9. Requisitos não-funcionais (segurança, desempenho, disponibilidade, acessibilidade, privacidade) — **não levantados**.

## Restrições e o que evitar

- **Privacidade de dados de participantes (LGPD)** — o sistema trata dados pessoais; a visibilidade para palestrantes precisa ser explicitamente definida (ponto em aberto #8). Tratar como restrição desde o desenho.
- **Requisitos não-funcionais ausentes** — segurança, desempenho, disponibilidade, acessibilidade e privacidade **ainda não foram levantados** (observação da elicitação). Não assumir que estão cobertos.
- **Regras de negócio ainda indefinidas** — não implementar cancelamento, reembolso, lista de espera ou emissão de certificado sem antes fechar as decisões pendentes; caso contrário, o código nasce sobre premissa inventada.

Detalhes em `contextos/restricoes.md`.

## Como a fábrica deve trabalhar

`<a preencher>` — política de gates e comandos de teste/lint/build serão definidos quando a stack for escolhida. Ver `contextos/testes.md`.

Enquanto o projeto está na fase de requisitos, o fluxo recomendado é:

1. Fechar os pontos em aberto → `/kairos-forge:especificar <feature>` (Laura classifica e registra requisitos rastreáveis).
2. Implementar a SPEC → `/kairos-forge:rodar` ou `/kairos-forge:mobilizar`.
3. Validar contra a SPEC → `/kairos-forge:validar SPEC-NNN`.
4. Revisar o diff → `/kairos-forge:revisar`.
5. Auditar o setup semanalmente → `/kairos-forge:auditar`.
