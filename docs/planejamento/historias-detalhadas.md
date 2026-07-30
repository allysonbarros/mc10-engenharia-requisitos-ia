# Histórias de Usuário — Detalhamento

> Cards completos das histórias dos primeiros sprints (fundação, identidade, eventos) + destaques críticos.
> Template aplicável a todas as histórias do `backlog-e-roadmap.md`.
> Critérios de aceite em Gherkin (Dado/Quando/Então) derivados dos `WHEN…THEN…SHALL` das SPECs.
> Data: 2026-07-30 · Camila (PM) + Caio (aceite).

## Como ler um card

- **Rastreabilidade:** cada card cita a SPEC e o requisito de origem — a história não inventa, deriva.
- **Critérios de aceite:** são o teste da história; o `/kairos-forge:validar` os cobra.
- **DoD:** só "pronto" com gate rodado (`verificado:`), não com "deve funcionar".

---

## Épico E0 — Fundação Técnica & Qualidade

### E0-01 — Scaffold do backend Rails API
- **Épico:** E0 · **Fonte:** ADR-0001 · **MoSCoW:** Must · **SP:** 5 · **Dep:** —
- **História:** Como time de desenvolvimento, quero o scaffold do backend Rails API com PostgreSQL, para ter a base do servidor sobre a qual as features serão construídas.
- **Critérios de aceite:**
  - Dado o repositório, Quando rodo o scaffold, Então existe uma app Rails em `api/` em modo `--api` com PostgreSQL configurado.
  - Dado o app, Quando rodo `bin/rails db:create db:migrate`, Então o banco é criado sem erro.
  - Dado o app, Quando rodo `bin/rails runner 'puts 1'`, Então ele boota e imprime `1`.
- **DoD:** app boota · `database.yml` aponta para o Postgres local · RuboCop (omakase) e Brakeman presentes · commit Conventional Commits · gate `bin/rails runner` verde.
- **Agentes:** Carlos (DBA) + Lucas (Backend).

### E0-02 — Scaffold do frontend Next.js com BFF
- **Épico:** E0 · **Fonte:** ADR-0001, ADR-0002 · **MoSCoW:** Must · **SP:** 5 · **Dep:** —
- **História:** Como time, quero o scaffold do frontend Next.js (TypeScript, App Router) com o padrão BFF, para ter a base do cliente e a ponte segura com a API.
- **Critérios de aceite:**
  - Dado o repositório, Quando rodo o scaffold, Então existe uma app Next em `web/` com TypeScript e ESLint.
  - Dado o app, Quando rodo `npm run build`, Então o build passa sem erro.
  - Dada uma rota de API do Next (BFF), Quando ela recebe uma chamada, Então faz proxy para a API Rails preservando o cookie de sessão (base para SPEC-009).
- **DoD:** `npm run build` verde · `npm run lint` verde · `npm run typecheck` verde · estrutura de BFF documentada · commit.
- **Agentes:** Marina (Frontend) + Pablo (UI).

### E0-03 — CI (GitHub Actions) com os gates
- **Épico:** E0 · **Fonte:** `contextos/testes.md` · **MoSCoW:** Must · **SP:** 5 · **Dep:** E0-01, E0-02
- **História:** Como time, quero CI rodando os gates a cada push/PR, para travar a qualidade desde o primeiro commit de código (fecha a lacuna de Guardrails da auditoria).
- **Critérios de aceite:**
  - Dado um push/PR, Quando o CI roda, Então executa backend (`bin/rubocop`, `bin/brakeman`, `bin/rails test`) e frontend (`npm run lint`, `npm run typecheck`, `npm run build`).
  - Dado um gate que falha, Quando o CI termina, Então o status do PR fica vermelho e o merge é bloqueado.
  - Dado um serviço Postgres, Quando os testes de integração rodam, Então há um Postgres disponível no job.
- **DoD:** workflow em `.github/workflows/` · CI verde no primeiro run · badge no README · commit.
- **Agentes:** Marcos (DevOps).

### E0-04 — Design system base (tokens + componentes)
- **Épico:** E0 · **Fonte:** DESIGN-002 · **MoSCoW:** Must · **SP:** 13 · **Dep:** E0-02
- **História:** Como time, quero tokens (cores, tipografia, espaçamento) e os componentes base, para as telas nascerem consistentes e acessíveis, sem estilo solto.
- **Critérios de aceite:**
  - Dado o design system, Quando um componente é usado, Então ele vem do conjunto base: Button, FormField, Input, Select, DateTimePicker, Toggle, Card, DataTable, Badge, Modal, Toast, EmptyState, Skeleton.
  - Dado o Modal, Quando aberto, Então prende o foco e o devolve ao fechar (DESIGN-002/V-07).
  - Dado qualquer componente, Quando avaliado, Então contraste ≥ 4,5:1 e alvo de toque ≥ 44px (V-08, V-09).
- **DoD:** componentes com estados e variantes · testes de componente (Vitest) · axe sem violações · Storybook ou catálogo mínimo · commit.
- **Agentes:** Pablo (UI) + Ada (Acessibilidade).

---

## Épico E1 — Identidade e Acesso

### E1-01 — Autenticação (login/sessão)
- **Épico:** E1 · **Fonte:** SPEC-009/AUTH-01 · **MoSCoW:** Must · **SP:** 8 · **Dep:** E0-01, E0-02
- **História:** Como usuário, quero me autenticar com credenciais válidas, para acessar o sistema com minha identidade.
- **Critérios de aceite:**
  - Dado um usuário com credenciais válidas, Quando faz login, Então o sistema estabelece uma sessão autenticada (cookie httpOnly).
  - Dado um usuário com credenciais inválidas, Quando tenta login, Então é rejeitado **sem revelar** qual campo falhou (anti-enumeração — AMEACAS-auth/AP-07).
  - Dada uma senha, Quando armazenada, Então é apenas hash forte (bcrypt), nunca texto claro (AUTH/I4).
- **DoD:** gerador de auth do Rails 8 aplicado · teste de request (login ok + login inválido) · `bin/brakeman` sem alta · commit.
- **Agentes:** Lucas (Backend) + Helena (Segurança, parecer).

### E1-02 — Cadastro com dados mínimos e consentimento (LGPD)
- **Épico:** E1 · **Fonte:** SPEC-009/AUTH-07, RNF-PRI-02 · **MoSCoW:** Must · **SP:** 5 · **Dep:** E1-01
- **História:** Como titular de dados, quero me cadastrar fornecendo apenas o necessário e registrando meu consentimento, para respeitar a LGPD.
- **Critérios de aceite:**
  - Dado o cadastro, Quando submetido, Então coleta apenas dados necessários e registra o consentimento com finalidade.
  - Dado um campo não essencial, Quando ausente, Então o cadastro ainda é aceito (minimização).
- **DoD:** modelo com campo de consentimento · teste (cadastro mínimo aceito) · registro auditável · commit.
- **Agentes:** Lucas (Backend) + Carlos (DBA, schema).

### E1-03 — Sessão segura (httpOnly, expiração, logout)
- **Épico:** E1 · **Fonte:** SPEC-009/AUTH-05, AMEACAS-auth/M5 · **MoSCoW:** Must · **SP:** 5 · **Dep:** E1-01
- **História:** Como usuário, quero uma sessão segura com expiração e logout, para proteger minha conta.
- **Critérios de aceite:**
  - Dado o login, Quando a sessão é criada, Então o cookie é `httpOnly`, `Secure`, `SameSite` e a sessão é **rotacionada** (anti-fixation).
  - Dada a expiração ou logout, Quando ocorre, Então nova autenticação é exigida.
- **DoD:** teste de expiração e logout · verificação dos atributos do cookie · commit.
- **Agentes:** Lucas (Backend) + Marcos (sessão/infra, parecer).

### E1-05 — Autorização por policy server-side (RBAC)
- **Épico:** E1 · **Fonte:** SPEC-009/AUTH-03, AMEACAS-auth/M1 · **MoSCoW:** Must · **SP:** 8 · **Dep:** E1-04
- **História:** Como responsável por segurança, quero que cada operação sensível verifique a permissão do papel no backend, para impedir escalada de privilégio.
- **Critérios de aceite:**
  - Dado um usuário fora do papel exigido, Quando tenta a operação, Então o backend nega (não o front).
  - Dado o campo `role`, Quando enviado pelo usuário no payload, Então é **ignorado** (fora dos strong params — anti mass-assignment, AP-01).
  - Dada cada rota sensível, Quando testada sem permissão, Então retorna 403.
- **DoD:** policies (Pundit/POROs) · testes de authz negativos (403) · `bin/brakeman` · parecer Helena · commit.
- **Agentes:** Lucas (Backend) + Helena (Segurança).

### E1-06 — Isolamento por dono (organizador/palestrante)
- **Épico:** E1 · **Fonte:** SPEC-009/AUTH-04, AMEACAS-auth/M4 · **MoSCoW:** Must · **SP:** 5 · **Dep:** E1-05
- **História:** Como organizador/palestrante, quero acessar somente os meus recursos, para respeitar o isolamento entre contas.
- **Critérios de aceite:**
  - Dado um organizador, Quando acessa evento de outro organizador, Então é negado.
  - Dado um palestrante, Quando acessa atividade que não é sua, Então é negado.
  - Dado o banco, Quando aplicável, Então RLS reforça o isolamento além da aplicação.
- **DoD:** escopo por dono nas queries + RLS · testes de IDOR horizontal (negados) · commit.
- **Agentes:** Lucas (Backend) + Carlos (RLS).

### E1-07 — Recuperação de senha segura
- **Épico:** E1 · **Fonte:** AMEACAS-auth/AP-02, M2 · **MoSCoW:** Must · **SP:** 5 · **Dep:** E1-01
- **História:** Como usuário, quero recuperar minha senha com segurança, para não perder acesso sem abrir brecha de tomada de conta.
- **Critérios de aceite:**
  - Dado um pedido de reset, Quando gerado, Então o token é aleatório forte, **single-use** e com expiração curta.
  - Dado o link de reset, Quando montado, Então o host é fixado/validado (anti host-header injection).
  - Dada a troca de senha, Quando concluída, Então as sessões ativas são invalidadas.
  - Dado um e-mail inexistente, Quando pede reset, Então a resposta é genérica (anti-enumeração).
- **DoD:** teste de token expirado/reutilizado (negado) · teste de invalidação de sessão · parecer Helena · commit.
- **Agentes:** Lucas (Backend) + Helena (Segurança).

---

## Épico E2 — Gestão de Eventos

### E2-01 — Criar evento
- **Épico:** E2 · **Fonte:** SPEC-002/EVT-01, EVT-08 · **MoSCoW:** Must · **SP:** 5 · **Dep:** E1-05
- **História:** Como organizador, quero criar um evento com nome, descrição, período e capacidade, para abrir inscrições.
- **Critérios de aceite:**
  - Dado um evento válido (capacidade > 0, período coerente), Quando submetido, Então é persistido em rascunho.
  - Dada capacidade ≤ 0 ou período inválido, Quando submetido, Então é rejeitado com mensagem clara ligada ao campo (DESIGN-002/V-02).
- **DoD:** migration + endpoint + validação · testes (feliz + erro) · gate `bin/rails test` · commit.
- **Agentes:** Fernanda (modelo) → Carlos (migration) + Lucas (endpoint).

### E2-03 — Cadastrar atividades com horário
- **Épico:** E2 · **Fonte:** SPEC-002/EVT-03 · **MoSCoW:** Must · **SP:** 5 · **Dep:** E2-01
- **História:** Como organizador, quero cadastrar atividades com início e fim, para montar a programação e permitir a detecção de conflito de horário (base do INSCR-04).
- **Critérios de aceite:**
  - Dada uma atividade com `inicio < fim` dentro do período do evento, Quando salva, Então é persistida.
  - Dada `fim ≤ inicio` ou atividade fora do período, Quando salva, Então é rejeitada com erro inline (DESIGN-002/V-03).
- **DoD:** modelo de atividade com fuso definido · testes de validação · commit.
- **Agentes:** Carlos (migration) + Lucas (endpoint).

### E2-06 — Publicar/despublicar evento
- **Épico:** E2 · **Fonte:** SPEC-002/EVT-06 · **MoSCoW:** Must · **SP:** 3 · **Dep:** E2-01
- **História:** Como organizador, quero publicar/despublicar um evento, para controlar sua visibilidade no catálogo.
- **Critérios de aceite:**
  - Dado um evento válido, Quando publicado, Então fica visível no catálogo (base de E3).
  - Dado um evento pago sem política de reembolso, Quando tento publicar, Então é bloqueado com a pendência listada (DESIGN-002/V-04).
  - Dado um evento publicado, Quando despublicado, Então some da vitrine.
- **DoD:** transição de status controlando visibilidade · testes · commit.
- **Agentes:** Lucas (Backend).

---

## Destaques críticos (histórias de maior risco)

### E4-02 — Sem overbooking sob concorrência ⭐
- **Épico:** E4 · **Fonte:** SPEC-001/INSCR-02 (invariante I1) · **MoSCoW:** Must · **SP:** 13 · **Dep:** E4-01
- **História:** Como organizador, quero que o sistema nunca exceda a capacidade mesmo sob inscrições simultâneas, para nunca vender mais vagas do que existem.
- **Contexto:** a invariante mais crítica do sistema. Estratégia ratificada no ADR-0001: `UPDATE evento SET ocupadas = ocupadas + 1 WHERE id = ? AND ocupadas < capacidade` — 0 linhas afetadas = lotado.
- **Critérios de aceite:**
  - Dadas N inscrições concorrentes disputando as últimas M vagas (N > M), Quando processadas, Então exatamente M confirmam e `ocupadas` nunca ultrapassa `capacidade`.
  - Dado o teste de concorrência, Quando executado, Então prova a ausência de overbooking (não é opcional).
- **DoD:** UPDATE condicional atômico em transação · **teste de concorrência** (threads paralelas) verde · commit · fato pro grafo.
- **Agentes:** Lucas (Backend) + Carlos (transação/índice) + Ricardo (teste de concorrência).

### E5-04 — Webhook de pagamento validado e idempotente ⭐
- **Épico:** E5 · **Fonte:** AMEACAS-pagamento/M1, M2 (AP-01, AP-02) · **MoSCoW:** Must · **SP:** 8 · **Dep:** E5-01
- **História:** Como responsável por segurança, quero confirmar pagamentos só por webhook validado e idempotente, para não confirmar inscrição sem pagamento real.
- **Contexto:** ameaça principal da SPEC-005 — forja/replay de webhook. O corpo do webhook é gatilho, nunca fonte da verdade.
- **Critérios de aceite:**
  - Dado um webhook recebido, Quando processado, Então a assinatura é validada **e** o status é reconsultado na API do Mercado Pago (server-to-server) antes de confirmar.
  - Dado o mesmo `payment_id`/`event_id`, Quando recebido mais de uma vez, Então gera no máximo uma confirmação/reembolso (idempotência via constraint).
  - Dado um webhook forjado (assinatura inválida), Quando recebido, Então é rejeitado e registrado.
- **DoD:** validação de assinatura + reconsulta + idempotência · testes (forjado rejeitado, replay não duplica) · parecer Helena · commit.
- **Agentes:** Thiago (Integrações) + Lucas (Backend) + Helena (Segurança).

---

## Definition of Ready (para uma história entrar no sprint)

1. Aponta para um requisito rastreável da SPEC (coluna Req).
2. Critérios de aceite verificáveis (Gherkin/`WHEN…THEN…SHALL`).
3. Sem pergunta aberta bloqueante na SPEC de origem.
4. Estimada em story points.
5. Dependências mapeadas e satisfeitas (ou no mesmo sprint, na ordem certa).

## Definition of Done (global)

1. Implementação conforme os critérios de aceite.
2. Teste mínimo: caminho feliz + ≥1 erro (concorrência/segurança quando aplicável).
3. Gate relevante rodado e verde (`contextos/testes.md`).
4. Sem regressão de RNF aplicável (segurança/acessibilidade).
5. Commit Conventional Commits PT-BR; história marcada como concluída com evidência.
6. Fatos novos registrados para o grafo de conhecimento.
