# Story SIDEBAR-07: Polimento Visual e Hierarquia Tipografica

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-07
**Priority:** Could Have
**Points:** 3
**Effort:** ~4-6 horas
**Status:** Ready for Dev
**Type:** Feature — Frontend (Design System)
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** SIDEBAR-02 (estrutura reorganizada), SIDEBAR-03 (grade de acoes)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [visual-inspection, dark-mode-test, design-token-audit]
```

---

## User Story

**Como** atendente do Tikso CRM,
**Quero** que o painel de contato tenha secoes visualmente distintas, hierarquia tipografica clara e indicadores de cor semanticos para tempo de ultima mensagem e estagio de jornada,
**Para que** eu consiga identificar o status e proxima acao do contato em menos de 3 segundos com um simples olhar.

---

## Acceptance Criteria

1. **AC1 — Secoes com fundo card:** As secoes de Status (jornada + atribuicao + metricas) e Identidade usam fundo `--surface-sunken` (ou equivalente: `bg-slate-50 dark:bg-slate-900/50`) para criar separacao visual em relacao ao fundo branco do painel. O border radius e `rounded-xl` (12px). O padding interno e `p-4`.
2. **AC2 — Hierarquia tipografica de 4 niveis:** O painel usa exatamente 4 niveis tipograficos: (a) Headings — nome do contato em `font-sans font-semibold text-base`; (b) Body — valores de campos em `font-sans text-sm`; (c) Labels — labels de campos em `font-sans text-xs font-medium text-muted-foreground uppercase tracking-wide`; (d) Micro — timestamps e contagens em `font-sans text-[11px] text-muted-foreground`. Nenhum texto abaixo de 11px.
3. **AC3 — Tempo de ultima mensagem com cor semantica:** O valor de ultima mensagem na StatsBar usa cor baseada no tempo decorrido: verde (`text-green-600`) para menos de 1 hora, ambar (`text-amber-600`) para 1-24 horas, vermelho (`text-red-500`) para mais de 24 horas. Em dark mode, usar variacoes mais claras (`text-green-400`, `text-amber-400`, `text-red-400`).
4. **AC4 — Badges de estagio de jornada com cores semanticas:** O estagio de jornada e exibido como um badge colorido baseado no estagio. O mapeamento de cores usa tokens do design system Tikso (ver Dev Notes). Minimo: estagio desconhecido e cinza, estAgios ativos sao teal/primary, convertido e verde.
5. **AC5 — Labels de campos em uppercase tracking:** As labels de campos de dados (ex: "TELEFONE", "E-MAIL", "CLIENTE DESDE") usam `text-xs font-medium uppercase tracking-wide text-muted-foreground`, enquanto os valores usam `text-sm text-foreground`. Os dois elementos nao competem visualmente.
6. **AC6 — Zero classes de cor hardcoded:** Nenhum valor de cor hexadecimal ou classe Tailwind de cor especifica (ex: `text-slate-500`) e adicionado diretamente. Apenas tokens CSS semanticos (ex: `text-muted-foreground`, `text-primary`, `bg-surface-sunken`) ou as classes de cor semantica definidas (verde/ambar/vermelho para urgencia de ultima mensagem). Um grep por `text-slate-`, `text-gray-`, `text-zinc-` no `contact-panel.tsx` nao retorna novas adicoes desta story.

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend (Design System)
**Secondary Type(s):** Accessibility (contraste de cor)
**Complexity:** Low

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Implementacao dos tokens visuais e hierarquia tipografica

**Supporting Agents:**
- @qa: Verificacao em dark mode, validacao de contraste das cores semanticas

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Grep em `contact-panel.tsx` por `text-slate-`, `text-gray-`, `bg-white` — confirmar zero novas ocorrencias adicionadas por esta story
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
- Design tokens: Apenas tokens semanticos para cores, sem hardcode
- Contraste: Cores de urgencia (verde/ambar/vermelho) devem passar WCAG AA (4.5:1 em fundos brancos)

**Secondary Focus:**
- Dark mode: Variacoes das cores de urgencia funcionam em fundo escuro
- Consistencia tipografica: 4 niveis exatos, sem tamanhos intermediarios nao padronizados

---

## Tasks / Subtasks

- [ ] **Task 1: Verificar e adicionar token `--surface-sunken` no globals.css** [AC: 1]
  - [ ] Abrir `src/app/globals.css`
  - [ ] Verificar se existe `--surface-sunken` ou equivalente (pode ser `--muted`, `--secondary`, ou uma variavel customizada do projeto)
  - [ ] Se nao existir, adicionar:
    ```css
    @layer base {
      :root {
        --surface-sunken: hsl(210 20% 97%);   /* slate-50 equivalente */
      }
      .dark {
        --surface-sunken: hsl(215 20% 10%);   /* slate-900/50 equivalente */
      }
    }
    ```
  - [ ] Adicionar classe Tailwind usando o token: verificar se o projeto usa `bg-[--surface-sunken]` ou se precisa de mapeamento em `tailwind.config`

- [ ] **Task 2: Aplicar fundo card nas secoes de Status e Identidade** [AC: 1]
  - [ ] Abrir `contact-panel.tsx`
  - [ ] Localizar a secao de Status (jornada + atribuicao — `AssignmentJourneySection`, linhas 656-888)
  - [ ] Envolver o conteudo da secao em um card com fundo sunken:
    ```tsx
    <div className="mx-4 rounded-xl bg-[--surface-sunken] p-4">
      {/* Conteudo da secao de status */}
    </div>
    ```
  - [ ] Aplicar o mesmo tratamento a StatsBar (metricas de ultima mensagem e score)
  - [ ] Verificar que o card nao tem `border` explicito — o fundo diferenciado ja cria separacao visual suficiente

- [ ] **Task 3: Implementar hierarquia tipografica de 4 niveis** [AC: 2, 5]
  - [ ] Definir as 4 classes de tipografia como constantes ou comentarios de referencia no topo do componente:
    ```typescript
    // Hierarquia tipografica do painel (SIDEBAR-07)
    // Level A - Heading:  font-sans font-semibold text-base text-foreground
    // Level B - Body:     font-sans text-sm text-foreground
    // Level C - Label:    font-sans text-xs font-medium uppercase tracking-wide text-muted-foreground
    // Level D - Micro:    font-sans text-[11px] text-muted-foreground
    ```
  - [ ] Aplicar Level A ao nome do contato no `ProfileHeader`
  - [ ] Aplicar Level C aos labels de campos em `ContactInfoCard` e `AssignmentJourneySection`:
    - "TELEFONE", "E-MAIL", "CLIENTE DESDE", "ATRIBUIDO A", "JORNADA"
  - [ ] Aplicar Level B aos valores de campos correspondentes
  - [ ] Aplicar Level D aos timestamps ("ha 2 dias", "16h", datas de notas)
  - [ ] Remover qualquer `text-[9px]` ou `text-[8px]` — minimo e `text-[11px]`

- [ ] **Task 4: Cor semantica para tempo de ultima mensagem** [AC: 3]
  - [ ] Localizar a `StatsBar` (linhas 1293-1314 ou nova posicao apos SIDEBAR-02)
  - [ ] Identificar o campo de ultima mensagem (`lastSeenAt` ou equivalente) e como o tempo relativo e calculado
  - [ ] Criar funcao helper `getLastMessageColor(lastSeenAt: Date | null)`:
    ```typescript
    function getLastMessageColor(lastSeenAt: Date | null): string {
      if (!lastSeenAt) return "text-muted-foreground";
      const hoursAgo = (Date.now() - lastSeenAt.getTime()) / (1000 * 60 * 60);
      if (hoursAgo < 1) return "text-green-600 dark:text-green-400";
      if (hoursAgo < 24) return "text-amber-600 dark:text-amber-400";
      return "text-red-500 dark:text-red-400";
    }
    ```
  - [ ] Aplicar a classe retornada ao elemento de valor na StatsBar
  - [ ] Verificar que o formato de exibicao do tempo (ex: "16h", "2d", "30m") permanece o mesmo

- [ ] **Task 5: Implementar badges de jornada com cores semanticas** [AC: 4]
  - [ ] Localizar onde o estagio de jornada e exibido em `AssignmentJourneySection`
  - [ ] Verificar o enum `JourneyState` em `src/lib/journey/types.ts` — listar todos os valores possiveis
  - [ ] Criar mapeamento de cores baseado nos tokens disponiveis:
    ```typescript
    // Verificar tokens em src/app/globals.css e adaptar
    const JOURNEY_BADGE_STYLES: Record<JourneyState, string> = {
      UNKNOWN:        "bg-secondary text-secondary-foreground border border-dashed",
      NEW_LEAD:       "bg-primary/10 text-primary border border-primary/20",
      IN_CONVERSATION:"bg-blue-50 text-blue-700 dark:bg-blue-950/30 dark:text-blue-300",
      PROPOSAL:       "bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-300",
      SCHEDULED:      "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-300",
      CONVERTED:      "bg-green-500 text-white",
      INACTIVE:       "bg-secondary text-muted-foreground",
      // ... adicionar outros estados conforme o enum real
    };
    ```
  - [ ] Aplicar `JOURNEY_BADGE_STYLES[journeyState]` ao elemento badge no painel
  - [ ] Adicionar `aria-label` descritivo ao badge (ex: `aria-label={`Estagio de jornada: ${JOURNEY_STATE_CONFIG[state].label}`}`)

- [ ] **Task 6: Auditoria de cores hardcoded** [AC: 6]
  - [ ] Executar grep no arquivo modificado:
    ```bash
    grep -n "text-slate-\|text-gray-\|text-zinc-\|bg-white\|#[0-9a-fA-F]\{3,6\}" src/components/inbox/contact-panel.tsx
    ```
  - [ ] Para cada ocorrencia encontrada que seja uma NOVA adicao desta story: substituir por token semantico equivalente
  - [ ] Ocorrencias pre-existentes de outras stories nao precisam ser migradas nesta story (escopo limitado)

- [ ] **Task 7: Verificacao visual em light e dark mode** [AC: 1-6]
  - [ ] Verificar em light mode: secoes com fundo sunken visiveis, labels uppercase legíveis, cores de urgencia corretas
  - [ ] Verificar em dark mode: `dark:text-green-400`, `dark:text-amber-400`, `dark:text-red-400` usam variacoes mais claras
  - [ ] Verificar badges de jornada em dark mode: fundos `dark:bg-*-950/30` com texto claro
  - [ ] Verificar contraste de cor AA: cores de urgencia contra fundo card (`--surface-sunken`)

---

## Dev Notes

### Design System Tikso — Tokens Relevantes

Baseado no design audit (tikso-sidebar-design-audit.md, secao 7.2), verificar os seguintes tokens em `src/app/globals.css`:

```css
/* Tokens que devem existir no projeto Tikso */
--primary          /* teal-600 */
--primary-foreground
--secondary        /* slate-100 */
--secondary-foreground
--muted-foreground /* slate-500 */
--accent           /* teal-50 */
--border           /* slate-200 */
--card             /* branco */
--ai-accent        /* violet — adicionado em INB-01 ou SIDEBAR-01 */
```

O token `--surface-sunken` pode nao existir — verificar se o projeto usa `--muted` para o mesmo proposito. Se `--muted` for equivalente a `slate-100`, usar `bg-muted` ao inves de criar novo token.

### Enum JourneyState — Valores Reais

Verificar `src/lib/journey/types.ts` para os valores exatos do enum. O design audit menciona:

- Novo Lead, Em Conversa, Proposta, Agendado, Convertido, Inativo, Desconhecido

Mas os valores do TypeScript enum podem usar diferentes strings. Ler o arquivo antes de implementar o mapeamento de cores.

### Hierarquia Tipografica — Referencia

```
| Nivel | Uso                              | Classes Tailwind                                      |
|-------|----------------------------------|-------------------------------------------------------|
| A     | Nome do contato                  | font-semibold text-base text-foreground               |
| B     | Valores (telefone, email, notas) | text-sm text-foreground                               |
| C     | Labels (TELEFONE, JORNADA, etc.) | text-xs font-medium uppercase tracking-wide           |
|       |                                  | text-muted-foreground                                 |
| D     | Micro (timestamps, contagens)    | text-[11px] text-muted-foreground                     |
```

A font do projeto provavelmente e Inter ou similar via `font-sans`. Verificar `tailwind.config.ts` ou `globals.css` para confirmar qual font e mapeada para `font-sans`.

### Cor de Urgencia — Verificacao de Contraste

As classes de urgencia devem ter contraste AA (4.5:1) em fundos brancos e em `--surface-sunken`:

- `text-green-600` em fundo branco: ~4.54:1 (PASSA AA)
- `text-amber-600` em fundo branco: ~3.22:1 (FALHA AA — usar `text-amber-700` se necessario)
- `text-red-500` em fundo branco: ~4.0:1 (BORDERLINE — verificar)

Ajustar as shades se necessario para garantir WCAG AA. Em dark mode, usar shades `*-400` que sao mais claras (melhor contraste em fundos escuros).

### Gotcha: Tailwind v4 e Classes Dinamicas

O projeto usa Tailwind v4. Classes como `text-green-600 dark:text-green-400` funcionam normalmente. Mas classes geradas dinamicamente via template literal podem nao ser incluidas no bundle (Tailwind precisa "ver" a classe no codigo). Ao usar `getLastMessageColor()`, certifique-se de retornar a string completa da classe, nao parcialmente:

```typescript
// ERRADO — Tailwind nao ve a classe completa
return `text-${color}-600`;

// CORRETO — Tailwind ve a string literal completa
return "text-green-600 dark:text-green-400";
```

### Testing

- **Tipo:** Inspecao visual manual em light e dark mode
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios de teste:**
  - [ ] Ultima mensagem ha 30 minutos: valor em verde
  - [ ] Ultima mensagem ha 5 horas: valor em ambar
  - [ ] Ultima mensagem ha 2 dias: valor em vermelho
  - [ ] Toggle dark mode: todas as cores de urgencia mudam para variante clara
  - [ ] Badge de jornada "Convertido": verde preenchido com texto branco
  - [ ] Badge de jornada "Desconhecido": cinza com borda tracejada
  - [ ] Grep AC6: zero classes hardcoded adicionadas por esta story

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada baseada nos audits de Design e UX do sidebar | @sm (River) |

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
| `src/app/globals.css` | MODIFY — adicionar token `--surface-sunken` (se nao existir) |
| `src/components/inbox/contact-panel.tsx` | MODIFY — tipografia 4 niveis, fundos card, cor de urgencia, badges de jornada |
| `src/components/contacts/shared/contact-info-card.tsx` | MODIFY — labels uppercase tracking nos campos |
| `src/lib/journey/types.ts` | READ ONLY — consultar enum para mapeamento de cores |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
