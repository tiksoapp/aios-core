# Story TL-09: Dashboard Redesign — Revenue-First Layout

**Epic:** Tikso Launch (TL)
**Story ID:** TL-09
**Priority:** P2 — Sprint 2, retenção e daily engagement
**Points:** 5
**Effort:** ~1.5 dias
**Status:** Ready for Dev
**Type:** Feature — Frontend
**Sprint:** Sprint 2 — Tikso Launch Growth
**Lead:** @dev (Dex)
**Depends On:** TL-02 (Revenue Dashboard v1), TL-08 (Brand Tokens)
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

**Como** dono de barbearia abrindo o Tikso de manhã,
**Quero** ver em 5 segundos as três coisas que importam: quanto dinheiro entrou, o que a Eli fez por mim, e o que tenho hoje na agenda,
**Para que** o Tikso seja o primeiro app que abro todo dia — e o último que cancelo.

---

## Acceptance Criteria

1. **AC1 — Layout reorganizado: revenue primeiro:** O dashboard existente é reorganizado para mostrar, nesta ordem de cima para baixo: (a) saudação personalizada com data, (b) grid de KPI cards com RevenueHeroCard ocupando destaque, (c) card EliSummaryCard ao lado de ChannelHealthWidget, (d) agenda do dia, (e) ações rápidas. Nenhum elemento atual é removido, apenas reorganizado e aprimorado.

2. **AC2 — Saudação personalizada:** Exibir `"Bom dia, [primeiro nome]!"` com a data no formato `"Ter, 25 de Fevereiro"`. O texto de saudação muda conforme o horário: "Bom dia" (05:00-12:00), "Boa tarde" (12:00-18:00), "Boa noite" (18:00-05:00). Nome vem do perfil do usuário logado.

3. **AC3 — Grid de KPIs com hierarquia visual:** No desktop (≥768px), exibir 4 KPI cards em grid: `RevenueHeroCard` com col-span-2 (destaque de largura dupla em teal), e 3 cards menores: "Agendamentos Hoje", "Conversas Ativas", "Novos Clientes". No mobile, todos em coluna completa, receita primeiro.

4. **AC4 — Componente "Agenda de Hoje":** Um novo card `DailyScheduleCard` exibe os agendamentos do dia atual em formato de timeline vertical. Cada linha: hora, nome do cliente, serviço, status badge (Confirmado/Pendente/Cancelado). Mostra no máximo 6 agendamentos (restante: "Ver agenda completa →"). Horários livres são visíveis como linhas cinzas com "disponível" em texto muted.

5. **AC5 — Barra de ações rápidas:** Abaixo da agenda, exibir 4 botões de ação rápida em linha: `[+ Agendar]`, `[Enviar campanha]`, `[Ver relatório]`, `[Configurações]`. No mobile, em grid 2×2. Cada botão usa ícone + label, estilo ghost/outline.

6. **AC6 — Navegação sidebar atualizada:** A sidebar é reorganizada por frequência de uso em 3 grupos: (a) "Principal": Dashboard, Inbox (badge de não lidos), Agendamentos (badge de hoje); (b) "Gestão": Contatos, Pipeline, Eli (badge de saúde); (c) "Marketing + Avançado": restante, colapsado por padrão. O item "Agente IA" é renomeado para "Eli" com ícone de bot.

7. **AC7 — API para agenda do dia:** Endpoint `GET /api/dashboard/daily-schedule` retorna agendamentos do dia atual da organização: `{ appointments: [{ time, clientName, serviceName, status, isPending }], freeSlots: [...] }`. Usa cache Redis TTL 60s.

---

## Tasks / Subtasks

- [ ] **Task 1: Componente DailyScheduleCard** [AC: 4]
  - [ ] Criar `/src/components/dashboard/daily-schedule-card.tsx`
  - [ ] Timeline vertical: cada item usa `time | [bar] | clientName — serviceName | [StatusBadge]`
  - [ ] Status badges: "Confirmado" (verde), "Pendente" (amarelo), "Cancelado" (vermelho tachado)
  - [ ] Horários livres como linha com background striped e texto "disponível" em muted
  - [ ] Rodapé: "X confirmados | Y pendentes | Z livres" + link "Ver agenda completa →"
  - [ ] Skeleton loading

- [ ] **Task 2: API daily-schedule** [AC: 7]
  - [ ] Criar `/src/app/api/dashboard/daily-schedule/route.ts`
  - [ ] Query: `Appointment.findMany({ where: { organizationId, scheduledAt: { gte: startOfDay, lte: endOfDay } } })`
  - [ ] Ordenar por `scheduledAt ASC`
  - [ ] Cache Redis: `dashboard:schedule:{orgId}:{date}` TTL 60s
  - [ ] Invalidar cache ao criar/atualizar agendamento

- [ ] **Task 3: Saudação personalizada** [AC: 2]
  - [ ] Criar helper `getGreeting(hour: number, firstName: string): string`
  - [ ] Formatar data em PT-BR: `new Intl.DateTimeFormat('pt-BR', { weekday: 'short', day: 'numeric', month: 'long' }).format(new Date())`
  - [ ] Adicionar no topo do componente de dashboard (server component ou client com hidratação)

- [ ] **Task 4: Grid de KPIs reorganizado** [AC: 3]
  - [ ] Reestruturar o grid do dashboard existente
  - [ ] Usar CSS Grid: `grid-cols-4` no desktop, `grid-cols-1` no mobile
  - [ ] `RevenueHeroCard` com `col-span-2`
  - [ ] Cards secundários com `col-span-1`
  - [ ] Verificar que `RevenueHeroCard` e `EliSummaryCard` (de TL-02) são corretamente posicionados

- [ ] **Task 5: Barra de ações rápidas** [AC: 5]
  - [ ] Criar `/src/components/dashboard/quick-actions-bar.tsx`
  - [ ] 4 botões com ícones lucide-react: `Calendar` (agendar), `Megaphone` (campanha), `BarChart2` (relatório), `Settings` (config)
  - [ ] Links de navegação: `/agendamentos/novo`, `/campanhas/nova`, `/analytics`, `/configuracoes`

- [ ] **Task 6: Reorganização do layout do dashboard** [AC: 1]
  - [ ] Editar `/src/app/(dashboard)/dashboard/page.tsx`
  - [ ] Ordem dos elementos conforme AC1
  - [ ] Garantir que elementos existentes (ChannelHealthWidget, etc.) continuam funcionando

- [ ] **Task 7: Sidebar — grupos e renomear Eli** [AC: 6]
  - [ ] Editar `/src/components/layout/sidebar.tsx`
  - [ ] Adicionar `<SidebarGroup label="Principal">`, `<SidebarGroup label="Gestão">`, `<SidebarGroup label="Mais" collapsible>`
  - [ ] Renomear item "Agente IA" para "Eli" com ícone `Bot` do lucide-react
  - [ ] Badge no item "Agendamentos": contar agendamentos do dia via `GET /api/dashboard/today-count` (endpoint simples, pode ser adicionado ao daily-schedule response)
  - [ ] Seção "Marketing + Avançado" começa colapsada (`defaultOpen={false}`)

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, React 19, Prisma 7.4, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos a modificar

```
src/app/(dashboard)/dashboard/page.tsx              — MODIFICAR (reorganizar layout)
src/components/layout/sidebar.tsx                   — MODIFICAR (grupos + rename Eli)
src/components/dashboard/                           — CRIAR novos componentes
src/app/api/dashboard/daily-schedule/route.ts       — CRIAR
```

### Helper de saudação

```typescript
export function getGreeting(hour: number, firstName: string): string {
  const greeting =
    hour >= 5 && hour < 12 ? 'Bom dia' :
    hour >= 12 && hour < 18 ? 'Boa tarde' :
    'Boa noite';
  return `${greeting}, ${firstName}!`;
}
```

### Formatação de data PT-BR

```typescript
const formatDate = (date: Date) =>
  new Intl.DateTimeFormat('pt-BR', {
    weekday: 'short',
    day: 'numeric',
    month: 'long',
  }).format(date);
// Output: "ter., 25 de fevereiro"
// Capitalizar primeira letra: formatDate(date).replace(/^\w/, c => c.toUpperCase())
```

### Layout do dashboard (wireframe de referência)

Do `docs/research/tikso-ux-redesign-proposal.md` Seção 4.3:
```
Bom dia, Carlos!                    Ter, 25 Fev 2026
[RECEITA PELA ELI 2x] [AGENDA] [CONVERSAS] [NOVOS]
[EliSummaryCard              ] [ChannelHealthWidget]
[Agenda de Hoje timeline                          ]
[Acoes Rapidas: Agendar | Campanha | Relatorio | Config]
```

### Sidebar grupos

Do `docs/research/tikso-ux-redesign-proposal.md` Seção 3.3:
```
PRINCIPAL: Dashboard, Inbox [badge], Agendamentos [badge]
GESTÃO: Contatos, Pipeline, Eli (IA) [health badge]
MARKETING: Campanhas, Templates, Broadcasts
AVANÇADO [colapsado]: Catálogo, Pedidos, Automação, Analytics, Supervisão
```

### Gotchas Relevantes
- Esta story depende de TL-02 (componentes `RevenueHeroCard` e `EliSummaryCard` devem existir)
- Sidebar usa RBAC — verificar que os badges não aparecem para usuários sem permissão de visualizar agendamentos
- A renomeação de "Agente IA" para "Eli" é apenas visual (label + ícone), não muda a rota

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-ux-redesign-proposal.md` — Seção 4 "Dashboard do Dono" completa
  - Seção 4.1: "Revenue-First Dashboard" como princípio de design #1
  - Seção 4.2: Seções A (Hero Metrics), B (Eli Summary), D (Agenda), E (Quick Actions)
  - Seção 4.3: Full desktop wireframe
  - Seção 3.3: Proposed sidebar structure (grupos)
  - Seção 9 Phase 1: "Dashboard Redesign (3-5 days)"

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do UX Redesign Proposal (Seções 3 e 4) | @sm (River) |

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
| `src/app/(dashboard)/dashboard/page.tsx` | MODIFY — reorganizar layout |
| `src/components/layout/sidebar.tsx` | MODIFY — grupos + rename Eli |
| `src/components/dashboard/daily-schedule-card.tsx` | CREATE |
| `src/components/dashboard/quick-actions-bar.tsx` | CREATE |
| `src/app/api/dashboard/daily-schedule/route.ts` | CREATE |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Frontend
  secondary: [Backend]
  complexity: Medium

specialized_agents:
  primary: "@dev"
  secondary: ["@ux-expert"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Saudação personalizada com nome correto e horário correto (bom dia/tarde/noite)
      - RevenueHeroCard com col-span-2 no desktop, full-width no mobile
      - DailyScheduleCard mostra máx 6 agendamentos com link "Ver mais"
      - Sidebar renomeou "Agente IA" para "Eli" com ícone Bot
      - Seção Avançado colapsada por padrão

  pre_pr:
    agent: "@github-devops"
    checks:
      - Depende de TL-02 (RevenueHeroCard e EliSummaryCard devem existir)
      - Layout verificado em 1280px, 768px e 375px

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Hierarquia visual (receita deve ser o elemento mais proeminente)
  - Responsividade em todos os breakpoints
  - Sidebar: RBAC — badges não vazam dados para usuários sem permissão
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
