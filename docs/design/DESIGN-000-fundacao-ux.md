# DESIGN-000 — Fundação de UX & Design System

> Conduzido por Pablo (UI), Isabela (UX) e Ada (Acessibilidade).
> **Base compartilhada** referenciada por todos os DESIGN-NNN. Par de design da história **E0-04**.
> Regra: um DESIGN de feature **não repete** o que está aqui — só referencia e adiciona o que é único.
> Stack: Next.js (React + TS), tokens em CSS variables + Tailwind (ADR-0001). Data: 2026-07-30.

## Princípios inegociáveis

1. **Cinco estados por view, sem exceção** (ver definição abaixo).
2. **Sem spinner genérico** — cada carregamento usa skeleton com a forma do conteúdo.
3. **Todo estado vazio tem CTA de saída** — o usuário nunca fica num beco.
4. **Mobile-first** — desenha-se do menor breakpoint para cima.
5. **Acessibilidade é critério, não intenção** — tudo aqui é verificável (WCAG 2.1 AA).
6. **Microcopy real é da Celina** — placeholder marcado `[texto: Celina]`, nunca inventado.

## A regra dos cinco estados

| Estado | O que é | Exigência |
|---|---|---|
| **Carregando** | Dados a caminho | Skeleton específico da estrutura (não spinner) |
| **Vazio** | Sem dados a exibir | Mensagem + **CTA de saída** |
| **Erro** | Falha ao carregar/enviar | Mensagem clara + ação de recuperação (tentar de novo) |
| **Sucesso** | Caminho feliz | Conteúdo/confirmação |
| **Parcial** | Carregando incremento / enviando | Feedback sem travar a tela (botão em loading, skeleton de trecho) |

## Tokens (placeholders neutros — trocar pela marca depois)

**Cores semânticas** (light / dark):

| Token | Uso | Light | Dark |
|---|---|---|---|
| `--cor-primaria` | Ações primárias, links | `#2563eb` | `#60a5fa` |
| `--cor-sucesso` | Confirmação, publicado | `#16a34a` | `#4ade80` |
| `--cor-erro` | Erro, perigo, destrutivo | `#dc2626` | `#f87171` |
| `--cor-aviso` | Atenção, pendência | `#d97706` | `#fbbf24` |
| `--cor-texto` | Texto padrão | `#1f2937` | `#f3f4f6` |
| `--cor-texto-suave` | Texto secundário | `#6b7280` | `#9ca3af` |
| `--cor-superficie` | Fundo de cards | `#ffffff` | `#1f2937` |
| `--cor-fundo` | Fundo da página | `#f9fafb` | `#111827` |
| `--cor-borda` | Bordas, divisores | `#e5e7eb` | `#374151` |

> Todo par texto/fundo aqui atinge contraste ≥ 4,5:1 (validar no build). Cores são placeholders — a identidade da Eventus entra depois sem mudar a estrutura.

**Tipografia:** escala 12 / 14 / 16 (base) / 20 / 24 / 32. Peso 400 (corpo), 600 (títulos). Fonte de sistema por ora.
**Espaçamento:** escala de 4px — 4, 8, 12, 16, 24, 32, 48.
**Raio:** 4px (campos), 8px (cards), 12px (modais). **Sombra:** 1 nível para cards, 1 para modais/overlay.
**Movimento:** transições ≤ 200ms; respeitar `prefers-reduced-motion` (desligar animações).

## Breakpoints

| Nome | Largura | Regra geral |
|---|---|---|
| Mobile | < 640px | 1 coluna; tabelas viram cards; ações primárias fixas no rodapé; modal em tela cheia |
| Tablet | 640–1023px | Layout intermediário; tabelas compactas; ações secundárias em menu "…" |
| Desktop | ≥ 1024px | Multi-coluna; tabelas completas |

## Componentes base

Cada componente já entrega os estados relevantes (default / hover / focus / disabled / error / loading) e a acessibilidade abaixo.

| Componente | Papel | A11y-chave |
|---|---|---|
| **Button** (primário/secundário/perigo) | Ação | Foco visível; estado loading desabilita e anuncia; alvo ≥44px |
| **FormField** | label + controle + erro | `<label>` associado; erro por `aria-describedby`; `aria-invalid` |
| **Input / Textarea / Select** | Entrada | Rótulo sempre presente; erro anunciado |
| **DateTimePicker** | Data/hora | Navegável por teclado; formato anunciado; não depende só do mouse |
| **Toggle / Checkbox / Radio** | Binário/opção | `role`/estado corretos; rótulo clicável |
| **Card** | Agrupamento | Título como heading; ação com nome acessível |
| **DataTable / DataList** | Listagem | Cabeçalhos `<th scope>`; no mobile, vira lista de cards |
| **Badge de status** | Rascunho/Publicado/Lotado | Rótulo textual (nunca só cor); contraste ≥4,5:1 |
| **Modal / Dialog** | Sobreposição | `role="dialog"` `aria-modal`; **foco preso**; `Esc` fecha; foco **retorna** ao gatilho |
| **Toast** | Feedback efêmero | `aria-live="polite"`; não some rápido demais; dismissível |
| **EmptyState** | Vazio | Ilustração + CTA focável |
| **Skeleton** | Carregando | `aria-busy`; forma do conteúdo real |
| **Pagination / "carregar mais"** | Paginação | Foco preservado ao carregar mais |
| **Contador ao vivo** | Números em tempo real | `aria-live` para atualização sem recarregar |

## Critérios globais de acessibilidade (WCAG 2.1 AA)

Aplicam-se a **todas** as telas:

- **Foco visível** (contraste do indicador ≥ 3:1) em todo interativo.
- **Ordem de tabulação** = ordem visual; nenhum foco preso fora de modal.
- **Todo campo** tem rótulo; erro ligado por `aria-describedby`; resumo de erro recebe foco no submit falho.
- **Contraste** de texto/ícone essencial ≥ 4,5:1; estado nunca comunicado só por cor.
- **Alvo de toque** ≥ 44×44px em ações primárias.
- **Teclado**: todo fluxo crítico é 100% operável sem mouse.
- **Leitor de tela**: fluxos críticos testados; toasts e contadores usam `aria-live`.
- **Modais**: foco preso + retorno ao fechar.
- **Movimento**: respeita `prefers-reduced-motion`.

## Critérios visuais globais (VG-xx)

Cobrados pelo `/kairos-forge:desenhar verificar` em qualquer feature:

| ID | Critério | Como verificar |
|---|---|---|
| VG-01 | Nenhum carregamento usa spinner genérico (é skeleton) | Throttle de rede em cada view |
| VG-02 | Todo estado vazio tem CTA de saída focável | Abrir a view sem dados |
| VG-03 | Contraste AA (≥4,5:1) em texto e badges | Medir com ferramenta de contraste |
| VG-04 | Fluxo crítico 100% navegável por teclado | Percorrer sem mouse |
| VG-05 | Modais prendem e devolvem o foco | Abrir/fechar modal por teclado |
| VG-06 | Toasts e contadores anunciam via `aria-live` | Leitor de tela na ação |
| VG-07 | Status nunca comunicado só por cor (tem rótulo) | Inspecionar badges |
| VG-08 | Layout responde nos 3 breakpoints sem quebra | Redimensionar |

## Convenções

- **Microcopy:** todo texto de interface a definir é `[texto: Celina]` — não inventar.
- **Idioma:** PT-BR único nesta versão (sem i18n; Ingrid não acionada), mas componentes não hardcodam texto fora de arquivos de string — preparados para i18n futura.
- **Fuso horário:** datas/horas exibidas no fuso do evento (herda Q-02 da SPEC-001, a confirmar).

## Como os DESIGN de feature usam esta fundação

Cada `DESIGN-NNN` referencia este documento e adiciona só: **fluxos** próprios, a tabela de **5 estados das suas views**, **componentes novos** (além dos base) e seus **critérios `V-xx`**. Os `VG-xx` e a a11y global valem sem repetição.
