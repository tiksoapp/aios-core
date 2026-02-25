# Story TL-06: Pipeline Visual de Vendas — Kanban de Leads

**Epic:** Tikso Launch (TL)
**Story ID:** TL-06
**Priority:** P1 — Sprint 1, feature core de CRM
**Points:** 8
**Effort:** ~2 dias
**Status:** Ready for Dev
**Type:** Feature — Frontend + Backend
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** —
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit-test, manual-review, visual-review]
```

---

## User Story

**Como** dono de barbearia ou salão usando Tikso,
**Quero** ver todos os meus leads e oportunidades em um pipeline visual estilo Kanban,
**Para que** eu saiba exatamente onde cada cliente potencial está na jornada e quais oportunidades estão quentes ou travadas.

---

## Acceptance Criteria

1. **AC1 — Página de Pipeline acessível:** Existe uma rota `/pipeline` no dashboard com um board Kanban que exibe colunas representando estágios do funil de vendas. Colunas padrão para o vertical de barbearia/beleza: "Novo Lead", "Interessado", "Orçamento Enviado", "Agendamento Marcado", "Cliente Ativo", "Perdido". O dono pode renomear as colunas nas configurações.

2. **AC2 — Cards de contato arrastáveis:** Cada card no pipeline exibe: nome do contato, foto de avatar (iniciais se sem foto), serviço de interesse (se conhecido), data da última interação, e badge de origem ("Via WhatsApp", "Via Indicação", etc.). Os cards podem ser arrastados de uma coluna para outra via drag-and-drop. A posição é persistida no banco via API.

3. **AC3 — A Eli move leads automaticamente:** Quando a Eli confirma um agendamento para um lead que estava na coluna "Interessado" ou "Orçamento Enviado", o sistema automaticamente move o card do lead para a coluna "Agendamento Marcado". Quando o agendamento é concluído (`status = COMPLETED`), o card vai para "Cliente Ativo".

4. **AC4 — Resumo de valor do pipeline:** No topo da página de Pipeline, exibir: (a) total de leads ativos (cards não em "Perdido"), (b) total de leads em "Agendamento Marcado" (receita potencial na semana), (c) taxa de conversão do pipeline (leads que chegaram a "Cliente Ativo" / total de leads que entraram, mês atual).

5. **AC5 — Adicionar lead manualmente:** Botão `[+ Novo Lead]` abre um modal/drawer com campos: nome, telefone WhatsApp, serviço de interesse (dropdown dos serviços cadastrados), e coluna inicial. Ao salvar, o contato é criado na tabela `Contact` (se não existir) e um `PipelineCard` é criado na coluna selecionada.

6. **AC6 — Performance:** O board com até 200 cards carrega em menos de 2 segundos. Usar virtualização se necessário. O drag-and-drop é suave (sem lag) em dispositivos mobile.

7. **AC7 — Persistência:** A posição dos cards (coluna + ordem dentro da coluna) persiste no banco. O model `PipelineCard` já existe no schema Prisma — usar os campos existentes (`stageId`, `position`).

---

## Tasks / Subtasks

- [ ] **Task 1: Verificar schema Prisma existente** [AC: 7]
  - [ ] Inspecionar o model `PipelineCard` e `PipelineStage` existentes no schema
  - [ ] Verificar se `PipelineStage` já tem estágios padrão ou se precisam ser criados via seed
  - [ ] Se necessário, adicionar `position Int @default(0)` ao `PipelineCard` e criar migration
  - [ ] Criar seed para estágios padrão de barbearia se não existirem

- [ ] **Task 2: API — buscar pipeline** [AC: 1, 2]
  - [ ] Criar ou verificar endpoint `GET /api/pipeline` retornando estágios com cards agrupados
  - [ ] Resposta: `{ stages: [{ id, name, position, cards: [{ id, contactId, contactName, serviceInterest, lastInteractionAt, source }] }] }`
  - [ ] Ordenar cards por `position` dentro de cada coluna

- [ ] **Task 3: API — mover card** [AC: 2, 3]
  - [ ] Criar ou verificar endpoint `PATCH /api/pipeline/cards/:id` para atualizar `stageId` e `position`
  - [ ] Usar transação Prisma para atualizar posições de múltiplos cards (quando um é inserido no meio da coluna)

- [ ] **Task 4: Automação — Eli move cards** [AC: 3]
  - [ ] No handler de `create_appointment` tool: verificar se o contato tem `PipelineCard` ativo
  - [ ] Se tem card e `appointment.status = 'CONFIRMED'`: mover card para o estágio "Agendamento Marcado" automaticamente
  - [ ] Quando `appointment.status` atualizado para `'COMPLETED'`: mover para "Cliente Ativo"
  - [ ] Criar função `movePipelineCard(contactId, targetStageName)` reutilizável

- [ ] **Task 5: Componente KanbanBoard** [AC: 1, 2, 6]
  - [ ] Criar `/src/components/pipeline/kanban-board.tsx`
  - [ ] Usar biblioteca de drag-and-drop: `@dnd-kit/core` + `@dnd-kit/sortable` (já instalada? verificar `package.json`)
  - [ ] Se não instalada: `npm install @dnd-kit/core @dnd-kit/sortable`
  - [ ] Implementar `KanbanColumn` e `KanbanCard` como sub-componentes
  - [ ] `KanbanCard` exibe: avatar com iniciais (shadcn/ui `Avatar`), nome, serviço, badge de origem, data de interação
  - [ ] On drag end: chamar API `PATCH /api/pipeline/cards/:id` com nova posição/coluna

- [ ] **Task 6: Resumo do pipeline** [AC: 4]
  - [ ] Criar `/src/components/pipeline/pipeline-summary.tsx`
  - [ ] Buscar métricas de `/api/pipeline/summary`: `{ totalActive, scheduledThisWeek, conversionRate }`
  - [ ] Exibir como 3 KPI cards acima do Kanban board

- [ ] **Task 7: Modal "Novo Lead"** [AC: 5]
  - [ ] Criar `/src/components/pipeline/new-lead-modal.tsx`
  - [ ] Formulário com validação: nome (obrigatório), telefone WhatsApp (obrigatório, formato BR), serviço de interesse (opcional, dropdown), coluna inicial (select)
  - [ ] Submit: `POST /api/contacts` (criar/buscar contato) + `POST /api/pipeline/cards` (criar card)

- [ ] **Task 8: Página do Pipeline** [AC: 1]
  - [ ] Criar `/src/app/(dashboard)/pipeline/page.tsx`
  - [ ] Compor `PipelineSummary` + `KanbanBoard` + botão `[+ Novo Lead]`

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, React 19, Prisma 7.4, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos existentes relevantes

```
prisma/schema.prisma                              — verificar PipelineCard + PipelineStage
src/app/(dashboard)/pipeline/                     — pode já existir (verificar)
src/components/pipeline/                          — pode já existir (verificar)
```

### Verificar antes de começar

```bash
# Na máquina de dev (ou via SSH vultr)
ls /home/tikso/tikso/src/app/\(dashboard\)/pipeline/
ls /home/tikso/tikso/src/components/pipeline/
grep -r "PipelineCard\|PipelineStage" /home/tikso/tikso/prisma/schema.prisma
grep -r "@dnd-kit" /home/tikso/tikso/package.json
```

### Padrão de drag-and-drop com @dnd-kit

```typescript
import { DndContext, DragEndEvent } from '@dnd-kit/core';
import { SortableContext, arrayMove } from '@dnd-kit/sortable';

function KanbanBoard({ stages, cards }: KanbanBoardProps) {
  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    // Atualizar estado local otimisticamente
    // Chamar API para persistir
    await fetch(`/api/pipeline/cards/${active.id}`, {
      method: 'PATCH',
      body: JSON.stringify({ stageId: over.data.current?.stageId, position: over.data.current?.position }),
    });
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      {stages.map(stage => (
        <KanbanColumn key={stage.id} stage={stage} cards={cards[stage.id]} />
      ))}
    </DndContext>
  );
}
```

### Estágios padrão para seed

```typescript
const defaultStages = [
  { name: 'Novo Lead', position: 0, color: '#94A3B8' },
  { name: 'Interessado', position: 1, color: '#3B82F6' },
  { name: 'Orçamento Enviado', position: 2, color: '#F59E0B' },
  { name: 'Agendamento Marcado', position: 3, color: '#10B981' },
  { name: 'Cliente Ativo', position: 4, color: '#0D9488' },  // teal primário
  { name: 'Perdido', position: 5, color: '#EF4444' },
];
```

### Referência de UX

Conforme `docs/research/tikso-ux-redesign-proposal.md` Seção 3.1:
> "Pipeline — Tier 2 — Every Week (visible, but de-emphasized)"
> O Pipeline está na sidebar, visível mas não na navegação primária.

Conforme `docs/research/tikso-world-best-crms-analysis.md`:
> "Pipedrive: O pipeline visual drag-and-drop MAIS intuitivo do mercado... Pipeline visual é NÃO-NEGOCIÁVEL para qualquer CRM de vendas."

### Gotchas Relevantes
- Verificar se a rota `/pipeline` já existe antes de criar do zero (pode haver implementação parcial)
- @dnd-kit não funciona bem com `Strict Mode` do React em dev — comportamento é correto em produção
- Nunca usar `sed -i` com regex em `.ts`
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-world-best-crms-analysis.md` — Seção 1.2 "Pipedrive: Pipeline Perfeito" + Gap Analysis
  - "Pipeline visual de vendas" listado como uma das 5 capacidades urgentes para competir
- `docs/research/tikso-ux-redesign-proposal.md` — Seção 3.2 "Proposed Navigation Hierarchy" (Pipeline em Tier 2)
- `docs/research/tikso-product-strategy-roadmap.md` — Feature roadmap (Pipeline como feature core estabilizada até Fev/2027)

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir da gap analysis de CRMs mundiais e UX redesign proposal | @sm (River) |

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
| `src/app/(dashboard)/pipeline/page.tsx` | CREATE (ou MODIFY se existir) |
| `src/components/pipeline/kanban-board.tsx` | CREATE |
| `src/components/pipeline/kanban-column.tsx` | CREATE |
| `src/components/pipeline/kanban-card.tsx` | CREATE |
| `src/components/pipeline/pipeline-summary.tsx` | CREATE |
| `src/components/pipeline/new-lead-modal.tsx` | CREATE |
| `src/app/api/pipeline/route.ts` | CREATE (ou MODIFY) |
| `src/app/api/pipeline/cards/[id]/route.ts` | CREATE (ou MODIFY) |
| `src/app/api/pipeline/summary/route.ts` | CREATE |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — auto-move card |
| `prisma/schema.prisma` | MODIFY se precisar de campos extras |
| `prisma/seed.ts` | MODIFY — adicionar estágios padrão |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Frontend
  secondary: [Backend, Database]
  complexity: High

specialized_agents:
  primary: "@dev"
  secondary: ["@ux-expert", "@db-sage"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Drag-and-drop funciona em desktop e mobile (touch events)
      - Posição dos cards persiste após refresh (API salva corretamente)
      - Eli move card automaticamente ao confirmar agendamento
      - Board com 200 cards carrega em < 2s
      - Seed de estágios padrão criado

  pre_pr:
    agent: "@github-devops"
    checks:
      - Não duplicar PipelineCard se já existir para o contato
      - Verificar se pipeline page já existe antes de criar

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Acessibilidade do drag-and-drop (keyboard navigation)
  - Performance com 200+ cards (virtualização se necessário)
  - Transação Prisma ao atualizar posições múltiplas
  - Touch events para drag no mobile
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
