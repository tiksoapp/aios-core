# Story SIDEBAR-04: Empty States Acionaveis e Responsividade

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-04
**Priority:** Should Have
**Points:** 3
**Effort:** ~4 horas
**Status:** Ready for Dev
**Type:** Feature — Frontend
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** SIDEBAR-02 (estrutura base reorganizada)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [visual-inspection, mobile-test, responsive-test]
```

---

## User Story

**Como** atendente do Tikso CRM abrindo o painel de um novo contato,
**Quero** ver CTAs acionaveis nos campos vazios e que o painel ocupe a largura total do meu celular,
**Para que** eu possa enriquecer dados do contato com um clique e nao perceber a inconsistencia de layout no mobile.

---

## Acceptance Criteria

1. **AC1 — Email vazio acionavel:** Quando o email do contato e null, o campo de email exibe o link "Adicionar e-mail" (texto com `+` ou icone de edicao) ao inves de "Nao informado". Clicar no link abre um input inline para digitar o email.
2. **AC2 — Tags vazias acionaveis:** Quando o contato nao tem tags, a secao de tags exibe um chip com borda tracejada e label "+ Adicionar tag" ao inves de "Nenhuma tag adicionada". Clicar no chip abre o dropdown de selecao de tags existente.
3. **AC3 — Compromissos vazios acionaveis:** Quando nao ha compromissos, a secao exibe apenas um botao "Agendar compromisso" ao inves de dupla mensagem ("Adicionar compromisso..." + "Nenhum compromisso registrado").
4. **AC4 — Largura responsiva:** O painel usa `w-full sm:w-[320px]` ao inves de `w-[320px]` fixo, permitindo que ocupe toda a largura da tela em viewports menores que 640px.
5. **AC5 — Secoes colapsaveis por padrao:** As secoes Tags, Notas (pessoal + equipe) e Atividade colapsam por padrao (`defaultOpen={false}`) para reduzir a profundidade de rolagem inicial. A secao de Compromissos permanece aberta se tiver dados; colapsada se vazia.
6. **AC6 — Sem regressoes:** O comportamento existente de adicao de tags via dropdown, adicao de notas e adicao de compromissos nao e alterado. Apenas os empty states mudam de apresentacao.

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend
**Secondary Type(s):** UX (empty states, onboarding)
**Complexity:** Low-Medium

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Implementacao dos empty states e responsividade

**Supporting Agents:**
- @qa: Verificacao em viewport mobile (375px) e inspecao dos 3 empty states

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Confirmar `w-full sm:w-[320px]` aplicado, sem `w-[320px]` hardcoded
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
- Responsividade: Sem width fixo em px no container principal do painel
- UX: Empty states tem CTA claro, nao sao mensagens passivas

**Secondary Focus:**
- defaultOpen: Verificar que SectionHeader aceita e usa corretamente a prop defaultOpen
- Accessibility: Links de "Adicionar email" tem aria-label adequado

---

## Tasks / Subtasks

- [ ] **Task 1: Corrigir largura do painel para responsivo** [AC: 4]
  - [ ] Abrir `src/components/inbox/contact-panel.tsx`
  - [ ] Localizar o elemento raiz do painel: `<div className="flex h-full w-[320px] shrink-0 flex-col border-l bg-card">`
  - [ ] Substituir `w-[320px]` por `w-full sm:w-[320px]`
  - [ ] Verificar que o `InboxLayout` nao tem CSS que interfere na largura do painel em mobile (ex: `flex-row` fixo que nao colapsa)
  - [ ] Verificar em viewport 375px: painel deve ocupar 100% da largura

- [ ] **Task 2: Empty state acionavel para email** [AC: 1]
  - [ ] Abrir `src/components/contacts/shared/contact-info-card.tsx`
  - [ ] Localizar onde `email` null exibe "Nao informado"
  - [ ] Substituir por componente de CTA inline:
    ```tsx
    {email ? (
      <span>{email}</span>
    ) : (
      <button
        type="button"
        onClick={() => setIsEditingEmail(true)}
        className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary transition-colors"
        aria-label="Adicionar endereço de e-mail"
      >
        <Plus className="h-3 w-3" />
        Adicionar e-mail
      </button>
    )}
    ```
  - [ ] Quando `isEditingEmail=true`: mostrar input controlado com botao salvar e cancelar
  - [ ] Ao salvar: chamar `updateContact` (server action existente) com o novo email
  - [ ] Confirmar que `updateContact` aceita o campo email (verificar `src/app/(app)/[orgId]/inbox/actions.ts`)

- [ ] **Task 3: Empty state acionavel para tags** [AC: 2]
  - [ ] Abrir `contact-panel.tsx` e localizar `TagsSection` (linhas 890-962)
  - [ ] Localizar o empty state atual: "Nenhuma tag adicionada"
  - [ ] Substituir por chip com borda tracejada:
    ```tsx
    {tags.length === 0 && (
      <button
        type="button"
        onClick={handleOpenTagDropdown}
        className="flex items-center gap-1 rounded-full border border-dashed border-border px-3 py-1 text-xs text-muted-foreground hover:border-primary hover:text-primary transition-colors"
        aria-label="Adicionar tag ao contato"
      >
        <Plus className="h-3 w-3" />
        Adicionar tag
      </button>
    )}
    ```
  - [ ] O `onClick` deve disparar o mesmo mecanismo que o botao de adicao de tag existente (ex: setar estado para abrir o DropdownMenu)
  - [ ] Quando ha tags: manter o layout existente de chips + botao de adicao

- [ ] **Task 4: Empty state acionavel para compromissos** [AC: 3]
  - [ ] Abrir `contact-panel.tsx` e localizar `CommitmentsSection` (linhas 1057-1262)
  - [ ] Localizar o empty state atual (dupla mensagem)
  - [ ] Substituir por botao unico:
    ```tsx
    {commitments.length === 0 && (
      <button
        type="button"
        onClick={() => setNewDescription("")}  // foca o input de adicao
        className="flex w-full items-center justify-center gap-1 rounded-lg border border-dashed border-border py-2 text-sm text-muted-foreground hover:border-primary hover:text-primary transition-colors"
        aria-label="Adicionar compromisso"
      >
        <CalendarPlus className="h-4 w-4" />
        Agendar compromisso
      </button>
    )}
    ```
  - [ ] Remover o placeholder "Adicionar compromisso..." duplicado quando `commitments.length === 0`
  - [ ] Quando ha compromissos: mostrar o input de adicao normalmente

- [ ] **Task 5: Ajustar `defaultOpen` das secoes** [AC: 5]
  - [ ] Localizar todos os usos de `SectionHeader` com `defaultOpen` em `contact-panel.tsx`
  - [ ] Verificar interface do `SectionHeader` em `src/components/contacts/shared/section-header.tsx` — confirmar que aceita `defaultOpen` prop
  - [ ] Alterar `defaultOpen` das secoes:
    - Tags: `defaultOpen={tags.length > 0}` (aberta se tem tags, colapsada se vazia)
    - Notas: `defaultOpen={false}` (colapsada por padrao)
    - Atividade: `defaultOpen={false}` (ja estava colapsada, manter)
    - Compromissos: `defaultOpen={commitments.length > 0}` (aberta se tem dados)
  - [ ] Verificar que a secao Intelligence (ConversationInsight) permanece com seu estado atual

- [ ] **Task 6: Verificacao visual e responsiva** [AC: 1-6]
  - [ ] Testar em 375px: painel ocupa largura total, sem barra de scroll horizontal
  - [ ] Testar empty state email: click abre input, save chama server action, cancel fecha sem salvar
  - [ ] Testar empty state tags: click abre dropdown de selecao de tags
  - [ ] Testar empty state compromissos: click foca o input de adicao (ou mostra o input)
  - [ ] Verificar que sections colapsadas mostram o header mas nao o conteudo por padrao
  - [ ] Verificar que adicionar dados reabre/exibe a secao corretamente

---

## Dev Notes

### Largura do Painel — Contexto

Linha atual em `contact-panel.tsx`:

```tsx
// ATUAL
<div className="flex h-full w-[320px] shrink-0 flex-col border-l bg-card">

// CORRIGIDO
<div className="flex h-full w-full shrink-0 flex-col border-l bg-card sm:w-[320px]">
```

No InboxLayout, o mobile usa `mobileView === "contact"` para exibir o painel em tela cheia. Verificar se o layout do InboxLayout interfere:

```typescript
// InboxLayout (verificar comportamento mobile)
// Quando mobileView === "contact", o painel deve ser full-width
// A mudanca w-full sm:w-[320px] e suficiente se o InboxLayout usa flex e nao tem width constraints no mobile
```

### Pattern de Empty State Acionavel

O design audit (tikso-sidebar-design-audit.md, secao 6.3) define o padrao:

- Email: link texto + icone `Plus` — click abre input inline
- Tags: chip com borda tracejada + icone `Plus`
- Compromissos: botao full-width com borda tracejada + icone `CalendarPlus`

Todos devem ter cor `text-muted-foreground` no estado normal e `hover:text-primary` no hover.

### SectionHeader e DefaultOpen

Verificar a implementacao atual de `SectionHeader` em `src/components/contacts/shared/section-header.tsx`. O componente provavelmente aceita `defaultOpen?: boolean` como prop. Se nao aceitar, adicionar essa prop.

A logica `defaultOpen={tags.length > 0}` e avaliada apenas uma vez na montagem inicial (como `useState` interno ao `SectionHeader`). Isso e o comportamento desejado — nao queremos que a secao colapsa automaticamente quando o usuario remove a ultima tag.

### Server Action para Email

Para salvar o email inline, usar a server action existente:

```typescript
// Verificar em src/app/(app)/[orgId]/inbox/actions.ts
// Deve existir uma funcao similar a:
await updateContact(orgId, contactId, { email: newEmail });
```

Se nao existir uma action generica `updateContact`, verificar `updateContactObservation` ou similar para entender o padrao e criar uma action dedicada ou usar o endpoint existente.

### Gotcha: ContactInfoCard e Compartilhado

O `ContactInfoCard` e usado tanto no inbox sidebar quanto no `ContactDrawer` da pagina de Contatos. Qualquer mudanca nesse componente afeta os dois contextos. Verificar se o comportamento de "adicionar email" faz sentido no Contacts drawer tambem — ou usar uma prop condicional para ativar o modo acionavel apenas no sidebar.

Sugestao: adicionar prop `allowEmailEdit?: boolean` ao `ContactInfoCard`. O inbox passa `true`, o drawer usa o seu proprio modo de edicao.

### Testing

- **Tipo:** Inspecao visual + teste funcional manual
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios de teste com valores reais:**
  - [ ] Contato sem email (`email: null`): exibe "Adicionar e-mail", click abre input, digitar email@teste.com, salvar, verificar no banco
  - [ ] Contato sem tags: exibe chip tracejado "+ Adicionar tag", click abre dropdown
  - [ ] Contato sem compromissos: exibe botao "Agendar compromisso", click foca input de adicao
  - [ ] Viewport 375px: sem barra de scroll horizontal, painel full-width
  - [ ] Viewport 1024px: painel tem 320px

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
| `src/components/inbox/contact-panel.tsx` | MODIFY — empty states acionaveis para tags e compromissos, defaultOpen das secoes |
| `src/components/contacts/shared/contact-info-card.tsx` | MODIFY — empty state acionavel para email, adicionar prop `allowEmailEdit` |
| `src/components/contacts/shared/section-header.tsx` | MODIFY — adicionar prop `defaultOpen` se nao existir |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
