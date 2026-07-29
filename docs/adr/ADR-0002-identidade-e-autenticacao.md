# ADR-0002 — Identidade e autenticação

- **Status:** Aceito
- **Data:** 2026-07-29
- **Decisores:** Rafael (Staff), Helena (Segurança), com aprovação do usuário
- **Resolve:** SPEC-009/Q-01 (provedor de identidade) — parte do bloqueio de SPEC-002, SPEC-005 e SPEC-008

## Contexto

A SPEC-009 especificou o comportamento de autenticação e RBAC (cinco papéis, autorização server-side, isolamento), mas deixou em aberto a estratégia de identidade. Com a stack já em Rails 8 (ADR-0001), a decisão ficou tratável: o Rails 8 traz um **gerador de autenticação nativo** (modelo `User` com `has_secure_password`/bcrypt, modelo `Session`, controllers de sessão e reset de senha, objeto `Current`), o que torna auth própria viável sem dependência externa.

> Nota: a documentação atual do gerador não pôde ser buscada via ctx7 nesta sessão (falha de fetch transitória). Os comandos exatos (`bin/rails generate authentication` e afins) devem ser reconfirmados contra a doc do Rails 8 no início da implementação (T1).

## Decisão

**Autenticação própria com o Rails nativo**, sem provedor de identidade externo:

| Aspecto | Escolha |
|---|---|
| Identidade | `User` com `has_secure_password` (bcrypt) — gerador nativo do Rails 8 |
| Sessão | Modelo `Session` + **cookie httpOnly, Secure, SameSite** |
| Frontend ↔ API | Padrão **BFF**: rotas do Next.js fazem proxy à API Rails, mantendo o cookie *same-site* (evita guardar token em JS — proteção contra XSS, RNF-SEG) |
| RBAC | Atributo `role` no `User` (enum) para os 5 papéis: participante, organizador, financeiro, palestrante, admin (TI) |
| Autorização | **Policy objects server-side** (Pundit ou POROs) — nunca no front (SPEC-009/I2) |
| Isolamento | Consultas escopadas por dono + política (organizador → seus eventos; palestrante → suas atividades) (SPEC-009/I3) |
| Proteção de login | `rate_limit` do Action Controller + mensagens genéricas (anti-enumeração, RNF-SEG-06) |
| Consentimento/LGPD | Registrar consentimento e coletar dados mínimos no cadastro (AUTH-07, RNF-PRI) |

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Devise (gem clássica) | Madura, mas o gerador nativo do Rails 8 já cobre o necessário com menos peso e dependência. Reavaliar só se surgir necessidade específica (confirmable, lockable etc.). |
| Provedor externo (Auth0/Clerk/Cognito/Keycloak via OIDC) | Traz login social/SSO/MFA prontos, mas adiciona lock-in, custo e integração externa. Descartado para este porte; OmniAuth/OIDC fica como extensão futura se SSO virar requisito. |
| Token JWT em `localStorage` | Simples para SPA, mas expõe o token a XSS. Preterido pelo cookie httpOnly + BFF. |

## Consequências

**Positivas**
- Zero dependência externa e zero lock-in; controle total sobre o fluxo de auth.
- Cobre 100% da SPEC-009 sem serviço de terceiros.
- Cookie httpOnly + BFF reduz superfície de XSS — alinhado ao RNF-SEG.

**Negativas / trade-offs**
- **Responsabilidade de segurança é nossa** — reset de senha, expiração, rate limiting e proteção de sessão precisam ser bem-feitos e auditados (Helena, gate `bin/brakeman`).
- Cookie *cross-origin* exige cuidado com CORS/CSRF; o padrão BFF mitiga ao manter same-site.
- Sem MFA/SSO nativos — se virarem requisito, exigem trabalho adicional (ver pendências).

## Premissas e pendências

- **P-01 (política de senha, SPEC-009/P-02):** comprimento mínimo e complexidade a confirmar com o negócio; default recomendado: mínimo 8–12 caracteres + verificação contra senhas comuns.
- **Q-02 (MFA):** MFA não entra na primeira versão. Recomendação: oferecê-lo como opcional para os papéis sensíveis (financeiro, admin) em follow-up.
- Estratégia de sessão (duração, *sliding expiration*, revogação) a detalhar na implementação (SPEC-009/AUTH-05).

## Impacto no backlog

- Resolve o "Provedor de identidade" que bloqueava a SPEC-009 → destrava também SPEC-002, SPEC-005 e SPEC-008 (que dependem de auth).
- Segue pendente apenas o **provedor de pagamento** (SPEC-005) entre os bloqueios de integração externa.
