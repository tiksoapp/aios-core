# Story TL-08: Brand Token Migration — Orange para Teal (Pulse Mark)

**Epic:** Tikso Launch (TL)
**Story ID:** TL-08
**Priority:** P2 — Sprint 2, identidade visual
**Points:** 3
**Effort:** ~1 dia
**Status:** Ready for Dev
**Type:** Feature — Frontend (Design System)
**Sprint:** Sprint 2 — Tikso Launch Growth
**Lead:** @dev (Dex)
**Depends On:** —
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [visual-review, manual-review]
```

---

## User Story

**Como** produto Tikso,
**Quero** migrar a cor primária da interface de Brand Orange (#FA6810) para Teal (#0D9488) alinhado com o conceito "Pulse Mark",
**Para que** a identidade visual reflita a marca moderna e as novas cores tenham melhor contraste WCAG (4.53:1 vs 3.2:1 do orange atual).

---

## Acceptance Criteria

1. **AC1 — Token `--primary` migrado para Teal:** Em `src/app/globals.css`, o token `--primary` é atualizado de Brand Orange (`#FA6810`) para Teal Pulse (`#0D9488`). O token `--primary-foreground` permanece `#FFFFFF`. O token `--primary-hover` é adicionado com valor `#0F766E` (Deep Teal).

2. **AC2 — Token Coral adicionado:** Os tokens `--coral`, `--coral-foreground`, e `--coral-light` são adicionados para uso como acento de notificação/CTA. Valores: `--coral: 3 91% 62%` (#F97066), `--coral-foreground: 0 0% 100%`, `--coral-light: 3 91% 94%`.

3. **AC3 — Dark mode atualizado:** No seletor `.dark`, o `--primary` é atualizado para `172 66% 50%` (#2DD4BF — teal mais brilhante para dark mode). O `--ring` (focus ring) é atualizado para seguir o primary em ambos os modos.

4. **AC4 — Tailwind v4 theme inline atualizado:** No bloco `@theme inline` existente, são adicionados os mapeamentos: `--color-primary-hover`, `--color-coral`, `--color-coral-foreground`, `--color-coral-light`.

5. **AC5 — Tipografia: DM Sans para headings:** A fonte DM Sans é adicionada para `h1`, `h2`, `h3` do dashboard. `Inter` permanece para corpo de texto. Carregamento via `next/font/google`. O token `--font-heading` é adicionado ao globals.css.

6. **AC6 — Nenhum componente quebrado:** Todos os componentes que usam `text-primary`, `bg-primary`, `border-primary`, `ring-primary`, `fill-primary` continuam funcionando com a nova cor. Verificação visual nos componentes principais: Button, Badge, KpiCard, ChannelHealthWidget, Input (focus), Switch, Progress.

7. **AC7 — Verificação de contraste:** A cor teal (#0D9488) sobre fundo branco (#FFFFFF) tem contraste 4.53:1, passando WCAG AA para texto normal. Confirmado com ferramenta de contraste. **A cor coral (#F97066) NÃO deve ser usada como cor de texto sobre fundo branco** — apenas como decoração/bordas/ícones.

---

## Tasks / Subtasks

- [ ] **Task 1: Atualizar globals.css — light mode** [AC: 1, 2]
  - [ ] Localizar `/home/tikso/tikso/src/app/globals.css`
  - [ ] Atualizar `--primary: 174 83% 32%` (era o valor do orange)
  - [ ] Atualizar `--primary-foreground: 0 0% 100%` (manter)
  - [ ] Adicionar `--primary-hover: 174 83% 27%`
  - [ ] Atualizar `--ring: 174 83% 32%` (focus rings vão para teal)
  - [ ] Adicionar bloco de tokens coral: `--coral`, `--coral-foreground`, `--coral-light`
  - [ ] Atualizar `--avatar-default: 174 40% 60%` (avatar teal-tinted)

- [ ] **Task 2: Atualizar globals.css — dark mode** [AC: 3]
  - [ ] No seletor `.dark`: atualizar `--primary: 172 66% 50%`
  - [ ] Atualizar `--primary-hover: 174 83% 32%`
  - [ ] Atualizar `--ring: 172 66% 50%`
  - [ ] Adicionar `--coral-light: 3 50% 20%` (versão dark do coral)

- [ ] **Task 3: Atualizar @theme inline** [AC: 4]
  - [ ] Adicionar ao bloco `@theme inline`:
    ```css
    --color-primary-hover: hsl(var(--primary-hover));
    --color-coral: hsl(var(--coral));
    --color-coral-foreground: hsl(var(--coral-foreground));
    --color-coral-light: hsl(var(--coral-light));
    ```

- [ ] **Task 4: Adicionar DM Sans** [AC: 5]
  - [ ] Em `src/app/layout.tsx`: adicionar `DM_Sans` do `next/font/google` com subsets `['latin']`, weights `['600', '700']`, variável `--font-dm-sans`
  - [ ] Em `globals.css`: adicionar `--font-heading: 'DM Sans', var(--font-inter), ui-sans-serif, system-ui, sans-serif`
  - [ ] Aplicar em `globals.css`: `h1, h2, h3 { font-family: var(--font-heading); }`

- [ ] **Task 5: Verificação visual de componentes** [AC: 6, 7]
  - [ ] Abrir o dashboard e verificar visualmente: buttons primários (teal), focus rings (teal), KPI cards, switches
  - [ ] Verificar no mobile (375px)
  - [ ] Verificar dark mode
  - [ ] Confirmar que nenhum texto usa coral sobre fundo branco
  - [ ] Documentar: `grep -r "text-secondary\|text-coral" src/components/` — se houver, verificar se estão em contextos adequados

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivo principal a modificar

```
/home/tikso/tikso/src/app/globals.css              — MODIFICAR (tokens)
/home/tikso/tikso/src/app/layout.tsx               — MODIFICAR (DM Sans)
```

### Tokens completos para substituição (light mode)

```css
:root {
  /* Substituir os valores dos tokens existentes */
  --primary: 174 83% 32%;             /* Teal #0D9488 (era orange #FA6810) */
  --primary-foreground: 0 0% 100%;    /* manter */
  --primary-hover: 174 83% 27%;       /* Deep Teal #0F766E — NOVO */
  --ring: 174 83% 32%;                /* Teal focus ring */
  --avatar-default: 174 40% 60%;      /* Teal-tinted */

  /* NOVOS tokens coral */
  --coral: 3 91% 62%;                 /* #F97066 */
  --coral-foreground: 0 0% 100%;
  --coral-light: 3 91% 94%;           /* Soft coral background */
}
```

### Tokens dark mode

```css
.dark {
  --primary: 172 66% 50%;             /* Bright Teal #2DD4BF */
  --primary-hover: 174 83% 32%;       /* #0D9488 */
  --ring: 172 66% 50%;
  --coral-light: 3 50% 20%;           /* Dark coral bg */
}
```

### Carregamento de DM Sans

```typescript
// src/app/layout.tsx
import { DM_Sans, Inter } from 'next/font/google';

const dmSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-dm-sans',
  weight: ['600', '700'],
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

// No elemento html:
// className={`${dmSans.variable} ${inter.variable}`}
```

### Contraste WCAG

| Combinação | Ratio | WCAG AA |
|-----------|-------|---------|
| Teal #0D9488 / Branco #FFF | 4.53:1 | PASS |
| Coral #F97066 / Branco #FFF | 3.13:1 | FAIL — não usar como texto |
| Coral #F97066 / Charcoal #1E293B | 4.52:1 | PASS — ok em dark mode |

### Gotchas Relevantes
- Tailwind v4 usa `@theme inline` — não usar `tailwind.config.ts` para adicionar novas cores
- Verificar se o projeto usa `shadcn/ui` com variáveis CSS (deve usar, pois globals.css define os tokens)
- DM Sans tem excelente suporte para glyphs em português (ç, ã, etc.)
- Esta story NÃO atualiza logos ou assets SVG — apenas tokens CSS

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-ux-redesign-proposal.md` — Seção 8 "Design Tokens — Pulse Mark Brand"
  - Seção 8.2: Token migration completa (light + dark mode)
  - Seção 8.3: Tailwind v4 theme inline additions
  - Seção 8.4: Typography tokens (DM Sans)
  - Seção 8.6: WCAG compliance check
  - Seção 9 Phase 0: "Brand Token Migration (1-2 days)" — confirmação de esforço

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do UX Redesign Proposal (Seção 8) | @sm (River) |

---

## Dev Agent Record

### Agent Model Used
_A ser preenchido pelo agente de desenvolvimento_

### Debug Log References
_A ser preenchido pelo agente de desenvolvimento_

### Completion Notes List
_A ser preenchido pelo agente de desenvolvimento_

### File List

| Arquivo | Acao |
|---------|------|
| `src/app/globals.css` | MODIFY — tokens primary→teal, adicionar coral, ring, primary-hover, dark mode |
| `src/app/layout.tsx` | MODIFY — adicionar DM Sans |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Frontend
  secondary: []
  complexity: Low

specialized_agents:
  primary: "@dev"
  secondary: ["@ux-expert"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Button primário usa teal (#0D9488) no light mode
      - Button primário usa bright teal (#2DD4BF) no dark mode
      - Focus rings (input, select, button) usam teal
      - Coral NOT usado como cor de texto sobre fundo branco
      - DM Sans carregando em h1/h2/h3

  pre_pr:
    agent: "@github-devops"
    checks:
      - Nenhum componente existente quebrado (verificação visual de 6 componentes no AC6)
      - Contraste teal/branco >= 4.5:1 confirmado

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - WCAG AA compliance para teal sobre branco
  - Uso correto do coral (decoração apenas, não texto sobre branco)
  - Dark mode: teal mais brilhante para manter contraste
  - Nenhum hardcode de cor hexadecimal — apenas tokens CSS
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
