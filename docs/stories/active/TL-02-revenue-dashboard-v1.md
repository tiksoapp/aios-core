# Story TL-02: Revenue Dashboard v1 — "Quanto a Eli gerou hoje?"

**Epic:** Tikso Launch (TL)
**Story ID:** TL-02
**Priority:** P0 — Killer feature, diferenciador central
**Points:** 8
**Effort:** ~2 dias
**Status:** Ready for Dev
**Type:** Feature — Backend + Frontend
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** ELI-01 (service resolution fix)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit-test, integration-test, manual-review, visual-review]
```

---

## User Story

**Como** dono de barbearia usando Tikso,
**Quero** ver no dashboard quanto dinheiro a Eli gerou para o meu negócio,
**Para que** eu possa medir o ROI real da ferramenta em Reais e justificar o custo da assinatura — e para que eu nunca queira cancelar.

---

## Acceptance Criteria

1. **AC1 — KPI Card "Receita Gerada pela Eli":** O dashboard exibe um card de destaque com o valor total de receita atribuída à Eli na semana atual, com comparação percentual em relação à semana anterior (ex: `R$ 4.850,00 +18% vs semana passada`). O card usa a cor primária (teal) e é visualmente maior que os outros cards.

2. **AC2 — Card "Resumo da Eli — Últimas 24h":** Exibe: (a) total de conversas atendidas pela Eli, (b) agendamentos feitos pela Eli, (c) taxa de resolução sem escalar para humano (%), e (d) número de conversas que precisam de atenção do dono. O componente usa o nome "Eli" e ícone de bot, apresentando a IA como funcionária.

3. **AC3 — API endpoint `/api/dashboard/eli-summary`:** Retorna JSON com: `{ conversationsHandled, appointmentsBooked, resolutionRate, needsAttentionCount, periodStart, periodEnd }`. Período padrão: últimas 24 horas. Suporta query param `?period=24h|7d|30d`.

4. **AC4 — API endpoint `/api/dashboard/revenue-attribution`:** Retorna JSON com: `{ totalRevenue, aiRevenue, humanRevenue, comparisonPct, breakdown: { appointments, noShowsRecovered, upsells } }`. `aiRevenue` é calculado como: agendamentos com `bookedBy = 'ai'` × preço médio do serviço. Período padrão: semana atual vs semana anterior.

5. **AC5 — Agendamentos com flag de origem:** O model `Appointment` possui campo `bookedBy: String?` (valores: `'ai'`, `'human'`, `'external'`). Quando a Eli cria um agendamento via tool `create_appointment`, salva `bookedBy = 'ai'`. Migration Prisma incluída.

6. **AC6 — Cache Redis com TTL:** Os endpoints de dashboard usam cache Redis com TTL de 5 minutos para as métricas agregadas. Cache invalidado quando um novo agendamento é criado. Dashboard carrega em < 500ms.

7. **AC7 — Cards visíveis no dashboard existente:** Os dois novos cards (`RevenueHeroCard` e `EliSummaryCard`) são adicionados ao dashboard atual, acima dos KPI cards existentes, sem quebrar o layout atual.

---

## Tasks / Subtasks

- [ ] **Task 1: Schema Prisma — campo bookedBy** [AC: 5]
  - [ ] Adicionar `bookedBy String?` ao model `Appointment` em `prisma/schema.prisma`
  - [ ] Adicionar `bookedBy String?` ao model `Message` (para rastrear mensagens geradas por IA)
  - [ ] Criar e rodar migration: `npx prisma migrate dev --name add-booked-by-attribution`
  - [ ] Atualizar `toolCreateAppointment` em `tool-implementations.ts` para salvar `bookedBy: 'ai'`

- [ ] **Task 2: API — eli-summary** [AC: 3]
  - [ ] Criar `/src/app/api/dashboard/eli-summary/route.ts`
  - [ ] Query: contar conversas onde agente AI foi `lastAgentType = 'ai'` no período
  - [ ] Query: contar `Appointment` onde `bookedBy = 'ai'` no período
  - [ ] Calcular `resolutionRate`: conversas resolvidas pela Eli / total conversas com Eli
  - [ ] Calcular `needsAttentionCount`: conversas com status `ESCALATED` ou aguardando resposta humana > 30min
  - [ ] Implementar cache Redis: `dashboard:eli-summary:{orgId}:{period}` com TTL 300s

- [ ] **Task 3: API — revenue-attribution** [AC: 4]
  - [ ] Criar `/src/app/api/dashboard/revenue-attribution/route.ts`
  - [ ] Query: `SUM(service.price)` para `Appointment` onde `bookedBy = 'ai'` AND `status = 'COMPLETED'` no período atual
  - [ ] Query idêntica para período anterior (comparação)
  - [ ] Calcular `comparisonPct`: `(atual - anterior) / anterior * 100`
  - [ ] Implementar cache Redis: `dashboard:revenue:{orgId}:{period}` com TTL 300s
  - [ ] Invalidar cache ao criar/atualizar appointment: adicionar `redis.del(cacheKey)` no handler

- [ ] **Task 4: Componente RevenueHeroCard** [AC: 1]
  - [ ] Criar `/src/components/dashboard/revenue-hero-card.tsx`
  - [ ] Exibir: valor total com formatação `Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })`
  - [ ] Exibir: badge de comparação com seta para cima/baixo e cor semântica (verde/vermelho)
  - [ ] Estado de loading: skeleton com `animate-pulse`
  - [ ] Largura 2x nos breakpoints `md` e acima (usando `col-span-2`)

- [ ] **Task 5: Componente EliSummaryCard** [AC: 2]
  - [ ] Criar `/src/components/dashboard/eli-summary-card.tsx`
  - [ ] Layout: ícone Bot + título "Resumo da Eli — Últimas 24h"
  - [ ] 3 métricas em linha: "conversas atendidas", "agendamentos feitos", "taxa de resolução"
  - [ ] Alerta em destaque se `needsAttentionCount > 0`: `"[!] N conversas precisam da sua atenção"` com link para Inbox filtrado
  - [ ] Usar token `--ai-accent` para bordas/ícones do card

- [ ] **Task 6: Integrar no dashboard** [AC: 7]
  - [ ] Localizar `/src/app/(dashboard)/dashboard/page.tsx` ou equivalente
  - [ ] Adicionar os dois novos cards no topo, antes dos KPI cards existentes
  - [ ] Grid: `RevenueHeroCard` (col-span-2) + `EliSummaryCard` (col-span-2) no desktop; full-width no mobile
  - [ ] Testar layout em 1280px, 768px, e 375px

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Redis, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos-chave

```
src/app/api/dashboard/eli-summary/route.ts         — CRIAR
src/app/api/dashboard/revenue-attribution/route.ts — CRIAR
src/components/dashboard/revenue-hero-card.tsx     — CRIAR
src/components/dashboard/eli-summary-card.tsx      — CRIAR
src/app/(dashboard)/dashboard/page.tsx             — MODIFICAR
src/lib/integrations/providers/bestbarbers/tool-implementations.ts — MODIFICAR
prisma/schema.prisma                               — MODIFICAR
```

### Modelo de dados existente relevante

```typescript
// O model Appointment já existe — adicionar apenas bookedBy
model Appointment {
  // ... campos existentes ...
  bookedBy  String?  // 'ai' | 'human' | 'external'
}

// Agendamentos criados pela tool já têm conversationId
// Usar para cruzar com serviço e preço
```

### Padrão de cache Redis

```typescript
const CACHE_TTL = 300; // 5 minutos
const cacheKey = `dashboard:eli-summary:${orgId}:${period}`;

const cached = await redis.get(cacheKey);
if (cached) return JSON.parse(cached);

const data = await computeMetrics(orgId, period);
await redis.setex(cacheKey, CACHE_TTL, JSON.stringify(data));
return data;
```

### Formatação de moeda BR

```typescript
const formatBRL = (value: number) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
// Output: "R$ 4.850,00"
```

### Cálculo de receita atribuída à Eli

```typescript
// Query Prisma
const aiRevenue = await prisma.appointment.findMany({
  where: {
    organizationId,
    bookedBy: 'ai',
    status: 'COMPLETED',
    completedAt: { gte: periodStart, lte: periodEnd },
  },
  include: { service: { select: { price: true } } },
});

const totalAiRevenue = aiRevenue.reduce(
  (acc, apt) => acc + (apt.service?.price?.toNumber() ?? 0),
  0
);
```

### Gotchas Relevantes
- Nunca usar `sed -i` com regex global em `.ts` — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Após migration Prisma: `su - tikso -c 'cd /home/tikso/tikso && npx prisma generate'`
- `Decimal` do Prisma não é Number: usar `.toNumber()` ao somar preços

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-product-strategy-roadmap.md` — Seção 4.6 "Relatórios de Receita por Canal" + Seção 3 Feature F6 "Dashboard de receita v1"
- `docs/research/tikso-ux-redesign-proposal.md` — Seção 4 "Dashboard do Dono", Seção 4.4 "Revenue Attribution Model", Seção 10.3 "New Components to Create"
- `docs/research/tikso-analytics-system-design.md` — Seção 2 "Existing Schema Analysis" + Seção 3 "New Models"

**Impacto estratégico (do roadmap PM):** "Não gera receita direta, mas RETÉM o cliente. Com ROI visível, churn cai de 8% para <4%"

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir dos relatórios de PM Strategy, UX Redesign e Analytics System Design | @sm (River) |

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
| `src/app/api/dashboard/eli-summary/route.ts` | CREATE |
| `src/app/api/dashboard/revenue-attribution/route.ts` | CREATE |
| `src/components/dashboard/revenue-hero-card.tsx` | CREATE |
| `src/components/dashboard/eli-summary-card.tsx` | CREATE |
| `src/app/(dashboard)/dashboard/page.tsx` | MODIFY — adicionar novos cards |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — salvar bookedBy = 'ai' |
| `prisma/schema.prisma` | MODIFY — campo bookedBy em Appointment |
| `prisma/migrations/...` | CREATE — migration add-booked-by-attribution |

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
      - Campo bookedBy salvo como 'ai' ao criar agendamento via Eli
      - Endpoints /api/dashboard/eli-summary e /api/dashboard/revenue-attribution retornam 200
      - Cache Redis com TTL 300s funcionando (verificar via redis-cli TTL)
      - RevenueHeroCard e EliSummaryCard renderizam sem erros
      - Dashboard carrega em < 500ms (medir com network tab)

  pre_pr:
    agent: "@github-devops"
    checks:
      - Migration Prisma aplicada sem erros
      - Decimal.toNumber() usado em todos os cálculos de preço

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Precisão do cálculo de receita atribuída (não sobre-contar)
  - Performance da query de atribuição (índice em bookedBy + status + completedAt)
  - Formatação de moeda PT-BR em todos os contextos
  - Invalidação de cache ao criar agendamento
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
