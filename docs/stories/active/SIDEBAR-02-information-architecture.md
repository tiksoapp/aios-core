# Story SIDEBAR-02: Reestruturacao da Arquitetura de Informacao do Painel

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-02
**Priority:** Must Have
**Points:** 5
**Effort:** ~6-8 horas
**Status:** Ready for Dev
**Type:** Feature — Frontend
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** SIDEBAR-01 (correcao da mutacao de nome antes de reorganizar)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [visual-inspection, mobile-test, dark-mode-test]
```

---

## User Story

**Como** atendente do Tikso CRM,
**Quero** ver as informacoes mais relevantes do contato (ultima mensagem, score, status da conversa) imediatamente ao abrir o painel lateral,
**Para que** eu possa tomar decisoes de atendimento em menos de 3 segundos sem precisar rolar a pagina.

---

## Acceptance Criteria

1. **AC1 — StatsBar na posicao 2:** A barra de stats (tempo desde ultima mensagem + lead score) aparece imediatamente abaixo do `ProfileHeader`, antes de qualquer outra secao. O usuario ve essa informacao sem rolar.
2. **AC2 — Telefone formatado:** O numero de telefone exibido no `ContactInfoCard` usa o formato brasileiro `+55 (79) 99981-1988` para numeros com DDI 55. O numero raw continua sendo usado para o clipboard e para links `wa.me`.
3. **AC3 — Badge de status da conversa:** O painel exibe um badge compacto indicando o estado atual da conversa: "Aberta" (verde), "Fechada" (cinza), "Atendida por Eli" (roxo com icone Bot). O badge usa os tokens de cor do design system.
4. **AC4 — Secao de identidade compacta:** O `ProfileHeader` usa layout horizontal (avatar 40px a esquerda, nome + telefone empilhados a direita) ao inves do layout centralizado atual. O avatar e reduzido para 40px. O espaco vertical da secao de identidade cabe em no maximo 3 linhas de texto.
5. **AC5 — Sem regressoes:** Todas as funcionalidades existentes do `ProfileHeader` (edicao de nome inline, badge de inscrito, badge de lead score) continuam funcionando apos a reorganizacao do layout.

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend
**Secondary Type(s):** Design System (tokens, layout)
**Complexity:** Medium

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Refatoracao do layout e adicao do badge de status

**Supporting Agents:**
- @qa: Verificacao visual em mobile, dark mode e com dados reais

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Confirmar que nenhuma classe de cor hardcoded foi adicionada (apenas tokens)
- [ ] Pre-PR (@devops): Verificar que `npm run typecheck` passa sem erros

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
- Accessibility: Badge de status tem `aria-label` descritivo
- Design tokens: Uso exclusivo de tokens semanticos para as cores do badge

**Secondary Focus:**
- Responsividade: Layout horizontal de identidade nao quebra em 320px
- Phone formatting: Funcao `formatBrazilianPhone` trata numeros sem DDI 55 graciosamente

---

## Tasks / Subtasks

- [ ] **Task 1: Reposicionar StatsBar** [AC: 1]
  - [ ] Abrir `src/components/inbox/contact-panel.tsx`
  - [ ] Localizar o componente `StatsBar` (atualmente linha ~1293, no final do componente)
  - [ ] Mover a renderizacao do `StatsBar` para logo apos o `ProfileHeader` (antes do `ContactInfoCard`)
  - [ ] Verificar que todas as props necessarias para `StatsBar` estao disponiveis nessa nova posicao (props vindas do `contact` passado ao `ContactPanel`)
  - [ ] Confirmar que o `StatsBar` ainda e visivel sem scroll no viewport padrao (altura > 800px)

- [ ] **Task 2: Implementar formatacao de telefone brasileiro** [AC: 2]
  - [ ] Criar funcao utilitaria `formatBrazilianPhone(raw: string): string` em `src/lib/utils.ts` (ou em novo arquivo `src/lib/phone.ts`):
    ```typescript
    export function formatBrazilianPhone(raw: string): string {
      // Remove tudo exceto digitos
      const digits = raw.replace(/\D/g, "");
      // Formato com DDI: +55 (XX) XXXXX-XXXX (13 digitos) ou +55 (XX) XXXX-XXXX (12 digitos)
      if (digits.startsWith("55") && digits.length === 13) {
        return `+55 (${digits.slice(2, 4)}) ${digits.slice(4, 9)}-${digits.slice(9)}`;
      }
      if (digits.startsWith("55") && digits.length === 12) {
        return `+55 (${digits.slice(2, 4)}) ${digits.slice(4, 8)}-${digits.slice(8)}`;
      }
      // Fallback: retornar raw sem formatacao
      return raw;
    }
    ```
  - [ ] Aplicar `formatBrazilianPhone` no `ContactInfoCard` (`src/components/contacts/shared/contact-info-card.tsx`) apenas para exibicao
  - [ ] Garantir que o valor copiado para clipboard via botao de copia ainda usa o numero raw (sem formatacao)
  - [ ] Garantir que o `whatsAppHref` (se existente) usa o numero sem formatacao

- [ ] **Task 3: Adicionar badge de status da conversa** [AC: 3]
  - [ ] Identificar onde o status da conversa (`status`, `caseStatus`, `isBusy`, `busyByName`) e passado para `ContactPanel` — verificar `src/components/inbox/types.ts` e props de `ContactPanel`
  - [ ] Se o status da conversa nao e uma prop existente, adiciona-lo: passar `conversationStatus: ConversationListItem["status"]` e `isAiHandling: boolean` como novas props
  - [ ] Criar componente inline `ConversationStatusBadge` (ou usar `Badge` do shadcn/ui com variante adequada):
    ```typescript
    // Logica de exibicao:
    // status === "OPEN" && !isAiHandling  -> "Aberta"      variant: success (verde)
    // status === "OPEN" && isAiHandling   -> "Eli atendendo" variant: ai-accent (roxo)
    // status === "CLOSED"                 -> "Fechada"     variant: secondary (cinza)
    ```
  - [ ] Posicionar o badge no `ProfileHeader`, na mesma linha do nome ou abaixo dele
  - [ ] Adicionar `aria-label` descritivo ao badge (ex: `aria-label="Status: Conversa aberta"`)
  - [ ] Verificar tokens de cor disponiveis em `src/app/globals.css` — usar `--success`, `--ai-accent`, `--secondary` ou equivalentes

- [ ] **Task 4: Refatorar layout horizontal do ProfileHeader** [AC: 4, 5]
  - [ ] Localizar a secao `ProfileHeader` em `contact-panel.tsx` (linhas 391-543)
  - [ ] Substituir layout centralizado (flex-col items-center) por layout horizontal (flex-row):
    - Avatar 40px (`h-10 w-10`) a esquerda (`shrink-0`)
    - `div` de texto a direita: nome em `text-base font-semibold`, telefone em `text-xs text-muted-foreground`
  - [ ] Manter a funcao de edicao inline do nome (click to edit) — apenas o layout muda, nao a logica
  - [ ] Manter badges existentes (inscrito, lead score) em linha ou abaixo do nome
  - [ ] Verificar que o layout funciona em 320px de largura (sem overflow ou truncamento indesejado)

- [ ] **Task 5: Teste visual** [AC: 1, 2, 3, 4, 5]
  - [ ] Verificar posicao da StatsBar (visivel sem scroll)
  - [ ] Verificar telefone formatado: `5579999811988` -> `+55 (79) 99981-1988`
  - [ ] Verificar telefone com DDI diferente: nao formata, mostra raw
  - [ ] Verificar badge "Eli atendendo" quando `isBusy=true` (conversa com AI ativa)
  - [ ] Verificar badge "Aberta" e "Fechada" nos estados corretos
  - [ ] Verificar layout horizontal do avatar em dark mode e light mode
  - [ ] Verificar que edicao de nome ainda funciona no novo layout

---

## Dev Notes

### Mapeamento de Componentes

```
src/components/inbox/contact-panel.tsx (1433 linhas)
  |-- ProfileHeader (inline, linhas 391-543)
  |-- ContactInfoCard (src/components/contacts/shared/contact-info-card.tsx)
  |-- StatsBar (inline, atualmente linhas 1293-1314 — MOVER para posicao 2)
```

### Layout Atual vs. Desejado

**Atual (posicao vertical das secoes):**
1. ProfileHeader (avatar centrado, 72px, nome centralizado)
2. ContactInfoCard (telefone, email, data)
3. QuickActionsSection
4. AssignmentJourneySection
5. TagsSection
6. UnifiedNotesSection
7. ConversationInsight
8. CommitmentsSection
9. ActivitySubSections
10. StatsBar (ultima mensagem + score) ← ERRADO: informacao mais importante por ultimo

**Desejado (apos esta story):**
1. ProfileHeader (layout horizontal, avatar 40px, nome + status badge)
2. StatsBar (ultima mensagem + score) ← MOVIDO para cima
3. ContactInfoCard (telefone formatado, email, data)
4. QuickActionsSection
5. AssignmentJourneySection
6. TagsSection
7. UnifiedNotesSection
8. ConversationInsight
9. CommitmentsSection
10. ActivitySubSections

### Formato de Telefone Brasileiro

Tikso CRM e voltado para o Brasil. O formato de exibicao deve ser `+55 (XX) XXXXX-XXXX` (celular) ou `+55 (XX) XXXX-XXXX` (fixo). O numero armazenado no banco e `5579999811988` (DDI + DDD + numero).

Logica de formatacao:
- 13 digitos com prefixo 55: celular com 9 — `+55 (79) 99981-1988`
- 12 digitos com prefixo 55: fixo — `+55 (79) 9998-1988`
- Outros formatos: retornar sem alteracao (fallback seguro)

### Props do ContactPanel Necessarias para Badge de Status

O `InboxLayout` tem acesso a `selectedConversation` (do array `conversations`). As props relevantes sao:

```typescript
// De ConversationListItem (src/components/inbox/types.ts)
status: "OPEN" | "CLOSED"  // status principal
isBusy: boolean             // true quando Eli esta atendendo
busyByName: string | null   // nome de quem esta atendendo (pode ser "Eli")
```

Se essas props nao chegam ao `ContactPanel`, adicionar como novas props opcionais e passar do `InboxLayout`. O `ContactPanel` ja recebe 16 props — adicionar com cuidado, usando tipos opcionais `?` para nao quebrar usos existentes.

### Tokens de Design Disponiveis

Verificar em `src/app/globals.css` — tokens esperados baseados no design system Tikso (Pulse Mark):

```css
--success: /* verde */
--success-foreground: /* branco */
--ai-accent: /* roxo -- pode ter sido adicionado em SIDEBAR-01 ou INB-01 */
--ai-accent-foreground: /* branco */
--secondary: /* cinza */
--secondary-foreground: /* texto cinza escuro */
```

### Testing

- **Tipo:** Inspecao visual manual
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios de teste:**
  - [ ] Contato com numero brasileiro (13 digitos): exibe formatado
  - [ ] Contato sem numero: nao exibe nada (null/undefined seguro)
  - [ ] Conversa ativa com Eli: badge roxo "Eli atendendo" visivel
  - [ ] Conversa fechada: badge cinza "Fechada"
  - [ ] StatsBar visivel na viewport inicial sem scroll (testar em 1024x768)
  - [ ] Edicao de nome ainda funciona (click para editar, Enter para salvar, Esc para cancelar)

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada baseada nos audits de UX e Design do sidebar | @sm (River) |

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
| `src/components/inbox/contact-panel.tsx` | MODIFY — reposicionar StatsBar, refatorar layout ProfileHeader, adicionar badge de status |
| `src/components/contacts/shared/contact-info-card.tsx` | MODIFY — aplicar formatBrazilianPhone para exibicao |
| `src/lib/utils.ts` (ou `src/lib/phone.ts`) | MODIFY/CREATE — adicionar funcao `formatBrazilianPhone` |
| `src/components/inbox/inbox-layout.tsx` | MODIFY — passar props de status da conversa para ContactPanel (se nao existirem) |
| `src/components/inbox/types.ts` | MODIFY — adicionar props de status ao tipo de ContactPanel (se necessario) |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
