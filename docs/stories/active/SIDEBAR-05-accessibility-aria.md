# Story SIDEBAR-05: Acessibilidade e ARIA no Painel de Contato

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-05
**Priority:** Should Have
**Points:** 3
**Effort:** ~4-5 horas
**Status:** Ready for Dev
**Type:** Feature — Frontend (Accessibility)
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** SIDEBAR-03 (grade de botoes criada), SIDEBAR-04 (secoes colapsaveis ajustadas)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [accessibility-review, aria-validation, keyboard-navigation-test]
```

---

## User Story

**Como** atendente do Tikso CRM que usa teclado ou leitor de tela,
**Quero** que o painel de contato tenha labels de acessibilidade, estados ARIA corretos e foco gerenciado ao abrir,
**Para que** eu possa navegar e operar todas as funcoes do painel sem depender exclusivamente do mouse ou touch.

---

## Acceptance Criteria

1. **AC1 — ARIA labels em todos os elementos interativos:** Todos os botoes, links e inputs do painel que nao tem texto visivel suficiente possuem `aria-label` descritivo. Elementos que ja tem texto visivel claro nao precisam de `aria-label` redundante.
2. **AC2 — `aria-expanded` em secoes colapsaveis:** O botao de colapso de cada `SectionHeader` tem `aria-expanded={isOpen}` e `aria-controls` apontando para o id do conteudo da secao.
3. **AC3 — Touch targets minimos de 44px:** Todos os elementos interativos tem area de toque de pelo menos 44x44px (WCAG 2.5.5 AA). Elementos menores usam padding para atingir o minimo sem alterar o visual.
4. **AC4 — Roles de landmark:** O container principal do painel tem `role="complementary"` e `aria-label="Detalhes do contato"`. Cada secao principal usa elemento `<section>` com `aria-label` ou `aria-labelledby`.
5. **AC5 — Gerenciamento de foco ao abrir:** Quando o painel abre (transicao de `isOpen: false` para `true`), o foco e movido para o botao de fechar no header do painel (ou para o primeiro elemento interativo do painel).
6. **AC6 — Labels em textareas:** O textarea de observacao pessoal tem `aria-label="Observacao pessoal sobre o contato"`. O textarea de nova nota de equipe tem `aria-label="Nova nota de equipe"`.

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend (Accessibility)
**Secondary Type(s):** —
**Complexity:** Low-Medium

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Implementacao de todos os atributos ARIA e gerenciamento de foco

**Supporting Agents:**
- @qa: Validacao com navegacao por teclado (Tab, Enter, Escape) e inspecao de aria-expanded

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Verificar que nenhum elemento interativo novo foi adicionado sem aria-label
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
- ARIA: aria-label em elementos sem texto visivel, aria-expanded em colapsaveis
- Focus management: useEffect para mover foco quando painel abre

**Secondary Focus:**
- Touch targets: min-h-[44px] ou padding equivalente em todos os botoes de acao
- Landmarks: role="complementary" no container do painel

---

## Tasks / Subtasks

- [ ] **Task 1: Adicionar role de landmark ao painel** [AC: 4]
  - [ ] Abrir `src/components/inbox/contact-panel.tsx`
  - [ ] No elemento raiz do painel (o `<div>` com `w-full sm:w-[320px]`), adicionar:
    ```tsx
    <div
      role="complementary"
      aria-label="Detalhes do contato"
      className="flex h-full w-full shrink-0 flex-col border-l bg-card sm:w-[320px]"
    >
    ```
  - [ ] Nos containers de cada secao principal, substituir `<div>` por `<section>` com `aria-labelledby` apontando para o id do `SectionHeader` correspondente (ou `aria-label` direto se nao houver heading)

- [ ] **Task 2: Gerenciamento de foco ao abrir o painel** [AC: 5]
  - [ ] Adicionar `ref` ao botao de fechar no header do painel (`closeButtonRef`)
  - [ ] Adicionar `useEffect` que monitora a prop `isOpen`:
    ```typescript
    const closeButtonRef = React.useRef<HTMLButtonElement>(null);

    React.useEffect(() => {
      if (isOpen && closeButtonRef.current) {
        // Pequeno delay para garantir que o painel terminou de montar
        const timer = setTimeout(() => {
          closeButtonRef.current?.focus();
        }, 50);
        return () => clearTimeout(timer);
      }
    }, [isOpen]);
    ```
  - [ ] Aplicar o `ref` ao botao X no header: `<button ref={closeButtonRef} aria-label="Fechar painel de contato" ...>`

- [ ] **Task 3: `aria-expanded` e `aria-controls` no SectionHeader** [AC: 2]
  - [ ] Abrir `src/components/contacts/shared/section-header.tsx`
  - [ ] Gerar um id estavel para o conteudo da secao (usar prop `id` ou derivar do `title`):
    ```typescript
    const contentId = id ?? `section-${title.toLowerCase().replace(/\s+/g, "-")}`;
    ```
  - [ ] Adicionar ao botao de toggle:
    ```tsx
    <button
      aria-expanded={isOpen}
      aria-controls={contentId}
      onClick={() => setIsOpen((prev) => !prev)}
    >
      {title}
    </button>
    ```
  - [ ] Adicionar `id={contentId}` ao container do conteudo da secao
  - [ ] Propagar prop `id` ao componente `SectionHeader` se necessario

- [ ] **Task 4: `aria-label` nos elementos interativos sem texto visivel** [AC: 1]
  - [ ] Percorrer `contact-panel.tsx` e identificar botoes sem texto visivel adequado
  - [ ] Lista minima de elementos que precisam de `aria-label`:
    - Botao de remover tag X: `aria-label={`Remover tag ${tag.name}`}`
    - Botao de excluir nota: `aria-label="Excluir nota"`
    - Botao de copiar telefone: `aria-label="Copiar numero de telefone"`
    - Botao de editar nome (icone de lapis): `aria-label="Editar nome do contato"`
    - Botoes de status de compromisso: `aria-label="Marcar como cumprido"`, `aria-label="Marcar como quebrado"`
    - Botao de adicao de tag (`+`): `aria-label="Adicionar tag"`
  - [ ] Verificar que o botao de fechar painel tem `aria-label="Fechar painel de contato"` (pode ja ter de SIDEBAR-03)
  - [ ] NÃO adicionar aria-label redundante em botoes que ja tem texto visivel claro (ex: "Atribuir", "Fluxo")

- [ ] **Task 5: `aria-label` nos textareas** [AC: 6]
  - [ ] Abrir `src/components/contacts/shared/notes-section.tsx`
  - [ ] Localizar o textarea de observacao pessoal — adicionar `aria-label="Observacao pessoal sobre o contato"`
  - [ ] Localizar o textarea de nova nota de equipe — adicionar `aria-label="Nova nota de equipe"`
  - [ ] Verificar se existem outros inputs no painel sem label visivel ou aria-label

- [ ] **Task 6: Ajustar touch targets para 44x44px** [AC: 3]
  - [ ] Identificar elementos com area menor que 44x44px:
    - Botao X de remover tag: atualmente `h-4 w-4` — adicionar `p-2` ou wrapper com `min-h-[44px] min-w-[44px]`
    - Botao de excluir nota (trash): similar
    - Botao de status de compromisso: adicionar `p-2`
    - Botao "Alterar" jornada: verificar altura
  - [ ] Usar padding para aumentar a area clicavel sem alterar o visual: `className="... p-2 -m-2"` (adiciona padding e compensa com margin negativa para manter alinhamento)
  - [ ] Verificar que a grade de quick actions (SIDEBAR-03) tem `min-h-[44px]` (AC desta story ajusta para 44px, SIDEBAR-03 usou 40px como minimo — corrigir aqui para 44px)

- [ ] **Task 7: Verificacao de acessibilidade por teclado** [AC: 1-6]
  - [ ] Navegar por todo o painel usando apenas Tab e Shift+Tab
  - [ ] Verificar que todos os elementos interativos sao alcanciveis por teclado
  - [ ] Verificar que Enter e Space ativam botoes
  - [ ] Verificar que Escape cancela edicao inline de nome
  - [ ] Verificar que aria-expanded muda quando secao e aberta/fechada (inspecionar no devtools > accessibility tree)
  - [ ] Verificar que ao abrir o painel, o foco vai para o botao X do header

---

## Dev Notes

### WCAG 2.1 AA — Requisitos Relevantes

Esta story implementa os seguintes criterios WCAG 2.1 AA identificados no UX audit:

| WCAG | Criterio | Implementacao |
|------|----------|---------------|
| 1.3.1 | Info and Relationships | `role="complementary"`, `<section>` com labels |
| 2.4.3 | Focus Order | Focus management ao abrir painel |
| 2.5.3 | Label in Name | aria-label descritivo em todos os controles |
| 2.5.5 | Target Size | Touch targets >= 44x44px |
| 4.1.2 | Name, Role, Value | aria-expanded em colapsaveis, aria-label em inputs |

### Padrao de Touch Target com Padding Negativo

Para aumentar area clicavel sem alterar visual:

```tsx
// Botao visualmente pequeno, area de toque adequada
<button
  type="button"
  aria-label="Remover tag Barba"
  className="rounded-full p-2 -m-2 text-muted-foreground hover:text-destructive transition-colors"
>
  <X className="h-3 w-3" />
</button>
```

O `p-2 -m-2` adiciona 8px de padding em todas as direcoes e compensa com -8px de margin, mantendo o elemento no mesmo lugar visualmente mas com area clicavel maior.

### SectionHeader — Estado Atual

O componente `SectionHeader` em `src/components/contacts/shared/section-header.tsx` provavelmente usa `useState` para `isOpen` internamente. Verificar se ele ja tem `aria-expanded` — se tiver, confirmar que esta sendo atualizado corretamente. Se nao tiver, adicionar conforme descrito na Task 3.

A adicao de `id` prop e necessaria para o `aria-controls`. Verificar como o componente e chamado em `contact-panel.tsx` e adicionar ids unicos para cada secao:

```tsx
<SectionHeader id="tags" title="Tags" defaultOpen={tags.length > 0}>
  ...
</SectionHeader>

<SectionHeader id="notes" title="Notas" defaultOpen={false}>
  ...
</SectionHeader>
```

### Gerenciamento de Foco — Timing

O delay de 50ms no `setTimeout` e necessario porque o painel pode ter uma animacao de entrada (CSS transition). Se o painel usa `transition` ou `animate` via Tailwind/Framer Motion, o foco precisa esperar a animacao terminar. Se nao houver animacao, o delay pode ser reduzido ou removido.

### Gotcha: aria-label vs. aria-labelledby

- Use `aria-label="texto"` quando o label nao existe no DOM
- Use `aria-labelledby="id-do-elemento"` quando o texto do label ja existe visivel no DOM

Para as `<section>` do painel, o titulo ja existe no `SectionHeader` — usar `aria-labelledby` apontando para o `id` do elemento de titulo e mais semantico.

### Testing

- **Tipo:** Teste de acessibilidade manual + inspecao do devtools
- **Ferramentas:** Chrome DevTools > Accessibility tab, navegacao por Tab
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios de teste:**
  - [ ] Tab pelo painel completo: todos os botoes e inputs alcancados em ordem logica
  - [ ] Inspecionar accessibility tree no Chrome: role="complementary" no container
  - [ ] Inspecionar botao de colapso de secao: aria-expanded=false inicialmente, muda para true ao clicar
  - [ ] Inspecionar botao X de tag: aria-label contem o nome da tag
  - [ ] Clicar fora do painel e reabrir: foco vai para o botao X do header
  - [ ] Medir touch targets com Chrome DevTools > Elements > computed styles: min-height >= 44px

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada baseada no UX Audit WCAG 2.1 AA do sidebar | @sm (River) |

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
| `src/components/inbox/contact-panel.tsx` | MODIFY — role/aria-label no container, focus management, aria-label em elementos interativos, touch targets |
| `src/components/contacts/shared/section-header.tsx` | MODIFY — adicionar aria-expanded, aria-controls, id prop |
| `src/components/contacts/shared/notes-section.tsx` | MODIFY — adicionar aria-label nos textareas |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
