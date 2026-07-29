# Modelo de ameaças — Autenticação e papéis — 2026-07-29

**Coordenado por:** Helena (Segurança), com Carlos (Banco/RLS) e Marcos (sessão/infra)
**SPEC relacionada:** SPEC-009 · **ADR:** ADR-0002 (auth própria Rails nativo, cookie httpOnly + BFF)
**Escopo:** login, registro, reset de senha, sessão por cookie e autorização RBAC dos cinco papéis.

## Resumo executivo

- **Ameaça principal:** **tomada de conta** (via força bruta/credential stuffing ou reset de senha frágil) e **escalada de privilégio** (usuário comum virando organizador/financeiro/admin).
- **3 mitigações de maior alavancagem:**
  1. Autorização **server-side por policy** com `role` **não atribuível pelo usuário** (proteção de mass-assignment).
  2. Token de reset de senha **aleatório forte, single-use, com expiração** e link com host validado.
  3. Cookie de sessão **httpOnly + Secure + SameSite** com **rotação no login** + rate limit/lockout no login.
- **Custo de não mitigar:** contas comprometidas, acesso a dados de todos os participantes, e um usuário comum operando pagamentos/eventos alheios.

## Ativos

| Ativo | Por que importa | Acesso atual |
|---|---|---|
| Cookie/sessão de usuário | Impersonação direta | Browser do usuário |
| Hash de senha | Base para crackeamento offline | Banco |
| Capacidade de assumir papel | Escalada para organizador/financeiro/admin | Backend (RBAC) |
| Fluxo de reset de senha | Vetor de account takeover | Público (request) |
| PII dos usuários | Privacidade/LGPD | Backend, papéis autorizados |

## Trust boundaries

| Boundary | O que cruza | Formato | Validação atual (a implementar) |
|---|---|---|---|
| Browser → BFF Next.js → Rails | Credenciais, sessão | HTTPS + cookie | Rate limit, CSRF, rotação de sessão |
| Usuário comum ↔ organizador/financeiro/admin | Autorização de operação | request autenticada | Policy server-side (least privilege) |
| Organizador A ↔ Organizador B | Acesso a recursos | request autenticada | Escopo por dono + RLS |
| Rails ↔ PostgreSQL | Usuários, sessões, papéis | conexão interna | RLS, hash de senha |

## Entrypoints

| Entrypoint | Caller esperado | Auth | Rate limit | Validação |
|---|---|---|---|---|
| Login | Público | Não (estabelece) | **Sim** | Mensagem genérica, lockout |
| Registro | Público | Não | Sim | Dados mínimos + consentimento |
| Reset de senha (request/confirm) | Público | Não | **Sim** | Token forte, single-use, expira |
| Endpoints autenticados | Usuário | Sim (sessão) | Conforme | Policy + escopo por dono |

## Perfis de atacante considerados

| Perfil | Por que entra neste modelo |
|---|---|
| Atacante oportunista | Credential stuffing / brute force com listas vazadas |
| Usuário comum curioso | IDOR e tentativa de escalada de privilégio |
| Atacante motivado | Account takeover direcionado via reset |
| Insider | Abuso do que o papel dele permite |

## Abuse paths

### AP-01: Escalada de privilégio via papel
**Perfil:** usuário comum · **Objetivo:** virar organizador/financeiro/admin
**Caminho:**
1. No registro/edição de perfil, injeta `role=admin` no corpo da request (mass-assignment).
2. Ou chama diretamente endpoint de papel superior contando com checagem só no front.
**Ativos atingidos:** capacidade de assumir papel, todos os dados/ações do papel.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação — `role` nunca em strong params do usuário; toda operação passa por **policy server-side** (SPEC-009/I2). UI escondida não conta.
**Severidade:** Crítica.

### AP-02: Account takeover via reset de senha
**Perfil:** atacante motivado · **Objetivo:** assumir conta alvo
**Caminho:** token de reset previsível, sem expiração, reutilizável, ou link montado por **host header injection** apontando para domínio do atacante.
**Ativos atingidos:** conta, PII, papéis associados.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação — token aleatório forte, **single-use**, com expiração curta; host do link fixado/validado; invalidar sessões ativas ao trocar a senha.
**Severidade:** Crítica.

### AP-03: Credential stuffing / brute force no login
**Perfil:** oportunista · **Objetivo:** tomar contas com senhas vazadas
**Caminho:** automatiza tentativas de login com listas de e-mail/senha.
**Ativos atingidos:** contas.
**Controle atual:** inexistente.
**Mitigação proposta:** borda/aplicação — `rate_limit` do Action Controller (Rails 8), lockout progressivo, política de senha (RNF-SEG / SPEC-009 P-01); MFA para papéis sensíveis como follow-up.
**Severidade:** Alta.

### AP-04: IDOR horizontal entre organizadores/palestrantes
**Perfil:** usuário curioso · **Objetivo:** ver/editar recursos de outro
**Caminho:** troca `evento_id`/`atividade_id` e acessa evento de outro organizador ou participantes de atividade alheia (liga a SPEC-008).
**Ativos atingidos:** dados de eventos, PII de participantes.
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação + banco — escopo por dono na query + policy + RLS no Postgres (SPEC-009/I3).
**Severidade:** Alta.

### AP-05: Sequestro/fixação de sessão
**Perfil:** oportunista · **Objetivo:** reutilizar sessão da vítima
**Caminho:** cookie sem httpOnly/Secure/SameSite, ou sessão não rotacionada no login (fixation).
**Ativos atingidos:** sessão.
**Controle atual:** definido no ADR-0002 (httpOnly+Secure+SameSite), a implementar.
**Mitigação proposta:** aplicação — cookie httpOnly+Secure+SameSite, **rotação de sessão no login**, expiração e revogação.
**Severidade:** Alta.

### AP-06: CSRF em ações state-changing
**Perfil:** oportunista · **Objetivo:** executar ação em nome da vítima logada
**Caminho:** como a auth é por cookie, um site malicioso induz request autenticada (inscrição, cancelamento, mudança de dados).
**Ativos atingidos:** integridade de ações.
**Controle atual:** parcial (SameSite ajuda).
**Mitigação proposta:** aplicação — token CSRF do Rails + verificação de origem no BFF; SameSite como defesa em profundidade.
**Severidade:** Alta.

### AP-07: Enumeração de usuários
**Perfil:** oportunista · **Objetivo:** descobrir e-mails válidos
**Caminho:** login/reset respondem diferente para "e-mail existe" vs "não existe".
**Ativos atingidos:** lista de usuários (insumo p/ AP-02/03).
**Controle atual:** inexistente.
**Mitigação proposta:** aplicação — mensagens genéricas e resposta em tempo ~constante (RNF-SEG-06).
**Severidade:** Média.

### AP-08: Roubo de sessão via XSS
**Perfil:** oportunista · **Objetivo:** exfiltrar sessão
**Caminho:** injeta script; tenta ler o cookie/token.
**Ativos atingidos:** sessão.
**Controle atual:** mitigado por design (cookie httpOnly não é acessível a JS — ADR-0002).
**Mitigação proposta:** aplicação — manter httpOnly + CSP + escape de output (defesa em profundidade).
**Severidade:** Média.

## Mitigações priorizadas

| ID | Mitigação | Camada | Custo | Alavancagem | Cobre |
|---|---|---|---|---|---|
| M1 | Policy server-side + `role` fora de strong params | Aplicação | Médio | Muito alta | AP-01 |
| M2 | Token de reset forte/single-use/expira + host fixado + invalida sessões | Aplicação | Médio | Muito alta | AP-02 |
| M3 | Rate limit + lockout + política de senha no login | Borda/App | Baixo | Alta | AP-03 |
| M4 | Escopo por dono + RLS | App/Banco | Médio | Alta | AP-04 |
| M5 | Cookie httpOnly+Secure+SameSite + rotação de sessão | Aplicação | Baixo | Alta | AP-05, AP-08 |
| M6 | CSRF token + verificação de origem | Aplicação | Baixo | Alta | AP-06 |
| M7 | Mensagens genéricas + tempo constante | Aplicação | Baixo | Média | AP-07 |

## Detecção e resposta

| Sinal | Onde monitorar | Quem responde |
|---|---|---|
| Pico de falhas de login por IP/conta | Log de auth | Helena / Sérgio |
| Uso de token de reset expirado/repetido | Log de reset | Helena |
| Tentativa de acesso negada por policy (403) em volume | Log de authz | Renata |
| Mudança de papel fora do fluxo de admin | Audit log | Helena |

## Decisões aceitas

- **MFA fora da primeira versão** (SPEC-009/Q-02): aceito; recomendado como opcional para financeiro/admin em follow-up — reavaliar antes de operar dinheiro real.

## Próximo passo

- Mitigações **M1–M6 viram tarefas P1** na SPEC-009 (auth é P1).
- M7 entra como ressalva em `/kairos-forge:revisar`.
- Reavaliar este modelo se: adicionar SSO/OAuth, MFA, ou multi-tenant real.
