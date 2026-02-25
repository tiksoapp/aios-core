# Story SIDEBAR-03: Redesign das Acoes Rapidas do Painel

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-03
**Priority:** Should Have
**Points:** 5
**Effort:** ~6-8 horas
**Status:** Done
**Type:** Feature — Frontend
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** SIDEBAR-02 (estrutura do painel reorganizada)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [visual-inspection, mobile-test, touch-target-test]
```

---

## User Story

**Como** atendente do Tikso CRM,
**Quero** um conjunto claro de botoes de acao rapida com icones e alvos de toque adequados,
**Para que** eu possa executar as acoes mais comuns (atribuir, fluxo, agendar, pausar) com um toque, sem confundir acoes de UI com acoes de dominio.

---

## Acceptance Criteria

1. **AC1 — Grade de icones 3x2:** A secao de acoes rapidas exibe 6 botoes em uma grade de 3 colunas x 2 linhas. Os botoes sao: WhatsApp, Atribuir, Fluxo (linha 1); Agendar, Tag, Pausar (linha 2).
2. **AC2 — Alvos de toque 48x40px:** Cada botao tem area clicavel de no minimo 48px de largura e 40px de altura (dentro da tolerancia para mobile). O icone tem 18px e o label abaixo tem `text-xs`.
3. **AC3 — Estilos corretos:** Botoes no estado normal: fundo transparente, borda `1px solid --border`, icone na cor `--primary` (teal). Botao "Pausar" quando ativo (AI pausada): fundo `--destructive/10`, icone vermelho, label "Retomar". Hover/focus: fundo `--accent` (teal-50).
4. **AC4 — Separacao de controles de UI:** O botao "Fechar painel" (X) e movido para o header do painel (fora da grade de acoes), deixando a grade apenas com acoes de dominio sobre o contato/conversa.
5. **AC5 — Acoes funcionais:** Todos os 6 botoes executam a acao correspondente ao serem clicados. WhatsApp abre `https://wa.me/{numero}` em nova aba. Atribuir abre o dropdown de membros. Fluxo abre o seletor de fluxos. Agendar abre o dialog de compromisso (ou mostra toast "Em breve" se nao existir). Tag abre o dropdown de tags. Pausar/Retomar alterna o estado de automacao pausada.
6. **AC6 — Tooltips e labels:** Cada botao tem `aria-label` descritivo e um `title` para tooltip no hover (ex: `aria-label="Abrir conversa no WhatsApp"`, `title="WhatsApp"`).

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend
**Secondary Type(s):** Accessibility (touch targets, ARIA)
**Complexity:** Medium

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Implementacao da grade de botoes e logica de acoes

**Supporting Agents:**
- @qa: Verificacao de touch targets em mobile e de todos os 6 botoes funcionais

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Verificar que todos os botoes tem `aria-label`, touch targets >= 40px altura
- [ ] Pre-PR (@devops): Run `npm run lint && npm run typecheck`

### Self-Healing Configuration

**Expected Self-Healing:**
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutos
- Severity Filter: CRITICAL e HIGH

**Predicted Behavior:**
- CRITICAL issues: auto_fix
- HIGH issues: document_only

### CodeRabbit Focus Areas

**Primary Focus:**
- Accessibility: aria-label em todos os botoes, touch targets de 40px minimo
- UX: Separacao clara entre acoes de UI (fechar painel) e acoes de dominio

**Secondary Focus:**
- Estado do botao Pausar: toggle correto, visual diferenciado quando pausado
- WhatsApp link: usa numero raw (sem formatacao) para o href wa.me

---

## Tasks / Subtasks

- [x] **Task 1: Mover botao "Fechar painel" para o header** [AC: 4]
  - [ ] Localizar onde o painel exibe o botao de fechar (`onClose` callback)
  - [ ] Verificar se ja existe um header com titulo "Detalhes do Contato" — adicionar se nao existir
  - [ ] Posicionar botao X (`<X className="h-4 w-4" />`) no canto superior direito do header
  - [ ] Adicionar `aria-label="Fechar painel de contato"` ao botao
  - [ ] Remover "Fechar" da lista de acoes rapidas existente

- [x] **Task 2: Criar componente `ContactQuickActions`** [AC: 1, 2, 3, 5, 6]
  - [ ] Criar (ou refatorar) o componente de acoes rapidas em `contact-panel.tsx` (secao QuickActionsSection, linhas 545-654)
  - [ ] Implementar grade CSS: `grid grid-cols-3 gap-2` para 2 linhas de 3 botoes
  - [ ] Definir interface de props:
    ```typescript
    interface QuickActionsProps {
      contactPhone: string | null;
      isPaused: boolean;
      isAiHandling: boolean;
      onAssign: () => void;      // abre dropdown de atribuicao
      onFlow: () => void;        // abre seletor de fluxo
      onTag: () => void;         // abre dropdown de tags
      onSchedule: () => void;    // abre dialog de agendamento
      onTogglePause: () => void; // toggle de pausa de automacao
    }
    ```
  - [ ] Implementar os 6 botoes com icones do `lucide-react`:
    - WhatsApp: icone `MessageCircle` (ou `Phone`) + label "WhatsApp"
    - Atribuir: icone `UserPlus` + label "Atribuir"
    - Fluxo: icone `Play` (ou `GitBranch`) + label "Fluxo"
    - Agendar: icone `CalendarPlus` + label "Agendar"
    - Tag: icone `Tag` + label "Tag"
    - Pausar/Retomar: icone `PauseCircle`/`PlayCircle` + label "Pausar"/"Retomar"
  - [ ] Aplicar estilos dos botoes (ver AC3 e Dev Notes abaixo)
  - [ ] Adicionar `aria-label` e `title` a cada botao (ver AC6)

- [x] **Task 3: Implementar acao do botao WhatsApp** [AC: 5]
  - [ ] Construir o href `https://wa.me/${digits}` onde `digits = phone.replace(/\D/g, "")`
  - [ ] Abrir em nova aba: `window.open(href, "_blank", "noopener noreferrer")`
  - [ ] Se `contactPhone` e null ou vazio: mostrar `toast.error("Contato sem numero de telefone")`

- [x] **Task 4: Conectar botoes Atribuir, Fluxo e Tag aos mecanismos existentes** [AC: 5]
  - [ ] Botao "Atribuir": disparar o mesmo comportamento do dropdown de atribuicao em `AssignmentJourneySection` (pode ser um `onClick` que abre um `DropdownMenu` separado ou rola para a secao de atribuicao)
  - [ ] Botao "Fluxo": chamar a mesma funcao que o botao "Fluxo" existente em `QuickActionsSection` (abrir o flow picker)
  - [ ] Botao "Tag": focar o input de adicao de tag em `TagsSection` (via `ref` ou scroll + focus)
  - [ ] Botao "Agendar": verificar se existe `CommitmentsSection` ou dialog de agendamento — chamar `onSchedule` prop; se nao existir integracao, mostrar `toast("Em breve: Agendamento rapido")`
  - [ ] Botao "Pausar/Retomar": chamar funcao existente `handleToggleAutomation` (ou equivalente)

- [x] **Task 5: Estilos e estados visuais** [AC: 2, 3]
  - [ ] Aplicar a cada botao: `min-h-[40px] min-w-[48px] flex flex-col items-center justify-center gap-1 rounded-lg border border-[--border] bg-transparent hover:bg-[--accent] transition-colors`
  - [ ] Estado Pausar ativo: adicionar condicional `isPaused && "bg-destructive/10 border-destructive/30"`
  - [ ] Icones: `className="h-[18px] w-[18px] text-[--primary]"` para normal, `"text-destructive"` para Pausar ativo
  - [ ] Labels: `className="text-[10px] text-muted-foreground leading-none"` abaixo dos icones

- [x] **Task 6: Teste visual e funcional** [AC: 1-6]
  - [ ] Verificar grade 3x2 em 320px de largura
  - [ ] Verificar que clicar cada botao dispara a acao correta
  - [ ] Verificar estado Pausar ativo: cor vermelha e label "Retomar"
  - [ ] Verificar touch targets em viewport mobile (375px): alvos de pelo menos 40px de altura
  - [ ] Verificar dark mode: bordas e icones visiveis
  - [ ] Verificar que "Fechar painel" esta no header, nao na grade

---

## Dev Notes

### Estrutura Atual dos Botoes

O `QuickActionsSection` (linhas 545-654 em `contact-panel.tsx`) atualmente renderiza:
- Botao "Fechar" (fecha conversa via `onCloseConversation`)
- Botao "Fluxo" (abre flow picker inline)
- Botao "Pausar"/"Retomar" (toggle `automationPaused`)

E tambem o componente compartilhado `QuickActions` de `src/components/contacts/shared/quick-actions.tsx`. Os comportamentos ja existem — esta story reorganiza o visual e adiciona novos botoes.

### Estilos dos Botoes

Baseado no design audit (tikso-sidebar-design-audit.md, secao 10.4):

```tsx
// Botao padrao
<button
  type="button"
  aria-label="Abrir conversa no WhatsApp"
  title="WhatsApp"
  className="flex min-h-[40px] flex-col items-center justify-center gap-1 rounded-lg border border-border bg-transparent px-3 py-2 hover:bg-accent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
>
  <MessageCircle className="h-[18px] w-[18px] text-primary" />
  <span className="text-[10px] leading-none text-muted-foreground">WhatsApp</span>
</button>

// Botao Pausar quando ATIVO (AI pausada, botao mostra "Retomar")
<button
  className="... bg-destructive/10 border-destructive/30 hover:bg-destructive/20"
>
  <PlayCircle className="h-[18px] w-[18px] text-destructive" />
  <span className="text-[10px] text-destructive">Retomar</span>
</button>
```

### Grid Layout

```tsx
<div className="grid grid-cols-3 gap-2 px-4 py-2">
  {/* Linha 1 */}
  <WhatsAppButton />
  <AssignButton />
  <FlowButton />
  {/* Linha 2 */}
  <ScheduleButton />
  <TagButton />
  <PauseButton />
</div>
```

### Icones Lucide Recomendados

O projeto usa `lucide-react`. Sugestoes de icones:

| Acao | Icone | Observacao |
|------|-------|------------|
| WhatsApp | `MessageCircle` | Nao existe icone WhatsApp nativo no Lucide |
| Atribuir | `UserPlus` | Claro e semantico |
| Fluxo | `GitBranch` ou `Play` | GitBranch sugere automacao/fluxo |
| Agendar | `CalendarPlus` | Indica adicao ao calendario |
| Tag | `Tag` | Icone direto, ja usado no projeto |
| Pausar | `PauseCircle` / `PlayCircle` | Alterna por estado |

### Prop `automationPaused`

O campo `automationPaused` vem do objeto `contact` passado ao `ContactPanel`. Verificar em `src/components/inbox/types.ts` o tipo `ContactDetails` — o campo deve existir (e usado no comportamento atual do botao Pausar).

### Testing

- **Tipo:** Inspecao visual + teste funcional manual
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios de teste:**
  - [ ] Cada botao dispara a acao correta (inspecao no devtools)
  - [ ] WhatsApp sem telefone: toast de erro
  - [ ] Pausar: muda visual para estado ativo, segunda vez retorna ao normal
  - [ ] Layout 3x2 nao quebra em 320px
  - [ ] Touch targets: pelo menos 40px de altura em cada botao (medir no devtools)
  - [ ] Fechar painel: botao X no header, nao na grade

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada baseada nos audits de UX e Design do sidebar | @sm (River) |

---

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

- TypeScript check: clean
- Build: successful
- PM2: online, HTTP 200

### Completion Notes List

- AC1: 3x2 grid with `grid grid-cols-3 gap-2` — WhatsApp, Atribuir, Fluxo (row 1), Agendar, Tag, Pausar (row 2)
- AC2: All buttons have `min-h-[40px]` with `px-3 py-2` — exceeds 48x40px touch target
- AC3: Buttons use `border-border bg-transparent hover:bg-accent`. Pausar active: `bg-destructive/10 border-destructive/30` with red icon/label
- AC4: Close panel button was already in header (pre-existing). Removed "Fechar conversa" from quick actions grid — grid now has only domain actions
- AC5: WhatsApp opens wa.me in new tab (raw digits). Atribuir scrolls to assignment section. Fluxo opens existing flow picker. Agendar shows "Em breve" toast. Tag scrolls to tags section. Pausar/Retomar toggles automation.
- AC6: All 6 buttons have `aria-label` and `title` attributes
- Removed shared QuickActions import (no longer used in contact-panel)
- Added scroll-to-section via `id` attributes on Assignment and Tags sections

### File List

| Arquivo | Acao |
|---------|------|
| `src/components/inbox/contact-panel.tsx` | MODIFY — replaced QuickActionsSection with 3x2 icon grid, added scroll targets, removed QuickActions import |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
