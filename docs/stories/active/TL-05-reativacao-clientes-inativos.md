# Story TL-05: Reativação de Clientes Inativos — "Faz tempo que você não aparece!"

**Epic:** Tikso Launch (TL)
**Story ID:** TL-05
**Priority:** P1 — Sprint 1, alto impacto em receita e retenção
**Points:** 5
**Effort:** ~1.5 dias
**Status:** Ready for Dev
**Type:** Feature — Backend (Cron + Agente proativo)
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** ELI-01, TL-04 (padrão de cron proativo)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit-test, manual-review]
```

---

## User Story

**Como** dono de barbearia,
**Quero** que a Eli identifique automaticamente clientes que não aparecem há 30+ dias e envie uma mensagem personalizada de reativação,
**Para que** eu recupere 15-25% dos clientes inativos sem esforço manual — gerando R$400-800/mês extras por barbearia.

---

## Acceptance Criteria

1. **AC1 — Detecção de clientes inativos:** Um job cron diário (rodando às 09:00 no horário configurado da organização) identifica todos os contatos com: (a) pelo menos 1 agendamento `COMPLETED` no histórico, (b) último agendamento `COMPLETED` ou `NO_SHOW` há mais de `inactivityThresholdDays` dias (padrão: 30), (c) status de contato diferente de `churned` (opt-out permanente), (d) que ainda não receberam mensagem de reativação nos últimos `inactivityThresholdDays` dias.

2. **AC2 — Mensagem de reativação enviada com personalização:** A Eli envia uma mensagem personalizada por contato inativo. A mensagem referencia o barbeiro preferido do cliente (baseado no profissional do último agendamento completado) e oferece disponibilidade. Formato: `"Oi [nome]! Faz um tempinho que você não aparece por aqui. O [barbeiro] sentiu sua falta! Tem um horário disponível [próximo dia disponível]. Bora marcar?"`. Se não houver barbeiro preferido identificado, omite essa parte.

3. **AC3 — Limite de envios por cron run:** O job não envia mais de `maxReactivationsPerDay` mensagens por organização por dia (padrão: 20, configurável). Prioriza os clientes com maior tempo de inatividade. Respeita integralmente o sistema antiban (fila BullMQ, rate limiting, jitter).

4. **AC4 — Registro de tentativa de reativação:** O model `Contact` ou uma tabela `ReactivationAttempt` registra: `sentAt`, `appointmentId` (se reagendou), `outcome` (`null`, `'rescheduled'`, `'declined'`, `'no_response'`). Uma mensagem de reativação não é re-enviada para o mesmo contato antes de 30 dias, independentemente do outcome.

5. **AC5 — Detecção de reativação bem-sucedida:** Quando um cliente que recebeu mensagem de reativação nos últimos 7 dias agenda um horário, o `outcome` da tentativa é automaticamente atualizado para `'rescheduled'`.

6. **AC6 — Configurável por organização:** Nas configurações da organização, o dono pode: (a) ativar/desativar reativação automática, (b) definir limiar de inatividade em dias (padrão: 30), (c) definir máximo de mensagens por dia, (d) customizar o texto da mensagem.

7. **AC7 — Testes:** Mínimo 4 testes cobrindo: seleção correta de inativos (respeita threshold + exclusão de recém-contatados), limite diário respeitado, não re-envia para contato contatado recentemente, registro de outcome ao reagendar.

---

## Tasks / Subtasks

- [ ] **Task 1: Schema Prisma** [AC: 4]
  - [ ] Criar model `ReactivationAttempt` com campos: `id`, `organizationId`, `contactId`, `sentAt`, `outcome String?`, `appointmentId String?`
  - [ ] Adicionar ao model `OrgConfig`: `reactivationEnabled Boolean @default(true)`, `inactivityThresholdDays Int @default(30)`, `maxReactivationsPerDay Int @default(20)`, `reactivationMessage String?`
  - [ ] Migration: `npx prisma migrate dev --name add-reactivation-system`

- [ ] **Task 2: Cron job de identificação de inativos** [AC: 1, 3]
  - [ ] Criar `/src/lib/cron/reactivation-cron.ts` (seguir padrão de `antiban-cron.ts`)
  - [ ] Agendar para rodar diariamente às 09:00 no timezone da org
  - [ ] Query de inativos:
    ```sql
    SELECT DISTINCT c.id, c.name, c.phone,
      MAX(a.scheduledAt) as lastAppointment,
      MAX(a.professionalId) as preferredProfessional
    FROM Contact c
    JOIN Appointment a ON a.contactId = c.id
    WHERE a.status IN ('COMPLETED', 'NO_SHOW')
      AND c.optOut = false
      AND NOT EXISTS (
        SELECT 1 FROM ReactivationAttempt ra
        WHERE ra.contactId = c.id
        AND ra.sentAt > NOW() - INTERVAL '30 days'
      )
    GROUP BY c.id
    HAVING MAX(a.scheduledAt) < NOW() - INTERVAL '{threshold} days'
    ORDER BY MAX(a.scheduledAt) ASC
    LIMIT {maxPerDay}
    ```
  - [ ] Disparar jobs de envio via BullMQ (um job por contato)

- [ ] **Task 3: Job de mensagem de reativação** [AC: 2]
  - [ ] Criar job handler `reactivationMessageJob` no BullMQ
  - [ ] Buscar próxima disponibilidade do profissional preferido via `getAvailability()`
  - [ ] Montar mensagem com `buildReactivationMessage(contact, professional, nextSlot)`
  - [ ] Enviar via fila antiban existente
  - [ ] Salvar `ReactivationAttempt` com `sentAt = now()`

- [ ] **Task 4: Detecção de reativação bem-sucedida** [AC: 5]
  - [ ] No handler de `create_appointment` tool: verificar se o contato tem `ReactivationAttempt` com `sentAt > now - 7 days` e `outcome = null`
  - [ ] Se sim: atualizar o attempt com `outcome = 'rescheduled'` e `appointmentId`
  - [ ] Emitir evento de analytics `contact_reactivated`

- [ ] **Task 5: Configurações no dashboard** [AC: 6]
  - [ ] Adicionar seção "Reativação Automática" nas configurações da organização
  - [ ] Campos: toggle on/off, threshold em dias, max/dia, mensagem customizada

- [ ] **Task 6: Testes** [AC: 7]
  - [ ] `tests/unit/reactivation-cron.test.ts`
  - [ ] Mínimo 4 casos de teste conforme AC7

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, BullMQ, Redis
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos de referência

```
src/lib/cron/antiban-cron.ts        — padrão de cron
src/lib/cron/no-show-detector.ts    — padrão criado na TL-04
src/lib/agents/pulse-agent.ts       — padrão de agente proativo
```

### Template de mensagem de reativação

```typescript
function buildReactivationMessage(
  contact: Contact,
  professional: Professional | null,
  nextSlot: { date: string; time: string } | null
): string {
  const firstName = contact.name?.split(' ')[0] ?? 'tudo bem';
  const profPart = professional
    ? `O ${professional.name} sentiu sua falta! `
    : '';
  const slotPart = nextSlot
    ? `Tenho um horário disponível ${nextSlot.date} às ${nextSlot.time}. `
    : '';

  return (
    `Oi, ${firstName}! Faz um tempinho que você não aparece por aqui. ` +
    profPart +
    slotPart +
    `Bora marcar? 😊`
  );
}
```

### Lógica de "profissional preferido"

```typescript
// Profissional preferido = profissional do último agendamento COMPLETED
const lastCompletedAppointment = await prisma.appointment.findFirst({
  where: {
    contactId: contact.id,
    status: 'COMPLETED',
  },
  orderBy: { scheduledAt: 'desc' },
  include: { professional: true },
});
const preferredProfessional = lastCompletedAppointment?.professional ?? null;
```

### Gotchas Relevantes
- BullMQ jobs devem usar `contactId + date` como `jobId` para idempotência
- Cuidado com timezone: usar o timezone da org para calcular "09:00" de envio
- Nunca usar `sed -i` com regex em `.ts`
- PM2 roda como user `tikso`
- Diferença de TL-04: TL-04 é reativo (no-show detectado), TL-05 é proativo (verificação agendada)

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-product-strategy-roadmap.md` — Seção 4.2 "Reativação de Clientes Inativos" + Feature G2
  - "Impacto estimado: Reativação de 15-25% dos inativos = 5-10 clientes/mês = R$400-800/mês"
- `docs/research/tikso-multi-agent-architecture.md` — Seção 3 "RETAIN Agent" (padrão de agente de retenção)

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do roadmap PM (Feature G2) e arquitetura multi-agent | @sm (River) |

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
| `src/lib/cron/reactivation-cron.ts` | CREATE |
| `src/lib/jobs/reactivation-message-job.ts` | CREATE |
| `src/app/(dashboard)/settings/reactivation/page.tsx` | CREATE |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — detectar reativação bem-sucedida |
| `prisma/schema.prisma` | MODIFY — ReactivationAttempt model + OrgConfig fields |
| `tests/unit/reactivation-cron.test.ts` | CREATE |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Backend
  secondary: [Database]
  complexity: Medium

specialized_agents:
  primary: "@dev"
  secondary: ["@db-sage"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Query de inativos exclui contatos com opt-out e contatos sem agendamentos anteriores
      - Não re-envia para mesmo contato em menos de 30 dias (4+ testes passando)
      - Limite maxReactivationsPerDay respeitado
      - recoveryOutcome atualizado ao reagendar

  pre_pr:
    agent: "@github-devops"
    checks:
      - Migration Prisma sem conflitos com TL-04
      - Cron agendado para 09:00 timezone da org (não UTC hardcoded)

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Idempotência: não re-enviar para contatos contatados recentemente
  - Timezone correto para horário de envio
  - Query performática com índices em lastAppointmentAt
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
