# Story TL-04: No-Show Recovery Agent — Recuperação Automática de Faltas

**Epic:** Tikso Launch (TL)
**Story ID:** TL-04
**Priority:** P1 — Sprint 1, alto impacto direto em receita
**Points:** 8
**Effort:** ~2 dias
**Status:** Ready for Dev
**Type:** Feature — Backend (Agente + Cron)
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** ELI-01, ELI-02
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit-test, integration-test, manual-review]
```

---

## User Story

**Como** dono de barbearia,
**Quero** que a Eli detecte automaticamente quando um cliente não apareceu no horário agendado e envie uma mensagem de reagendamento,
**Para que** eu possa recuperar 30-40% das faltas sem precisar fazer isso manualmente — gerando R$1.600-3.200/mês extras por barbearia.

---

## Acceptance Criteria

1. **AC1 — Detecção de no-show:** Um job cron verifica agendamentos a cada 15 minutos. Para cada agendamento com `status = 'CONFIRMED'` e `scheduledAt < now() - 30min`, se o status ainda não foi atualizado para `COMPLETED` ou `CANCELLED`, o agendamento é marcado como `NO_SHOW` automaticamente.

2. **AC2 — Mensagem de recuperação enviada pela Eli:** Após detectar um no-show, a Eli envia uma mensagem para o cliente via WhatsApp em até 5 minutos. Formato da mensagem: `"Oi [nome]! Vi que você não conseguiu vir hoje no horário das [hora]. Acontece! Quer reagendar? Tenho horários disponíveis [hoje às Xh] e [amanhã às Yh]. É só me falar!"` — O nome, horário original, e próximas disponibilidades são preenchidos dinamicamente.

3. **AC3 — A mensagem de recuperação respeita o antiban:** A mensagem é enviada pela fila BullMQ existente com os mesmos controles antiban (rate limiting, typing simulation, jitter gaussiano). Não envia mais de 1 mensagem de no-show por agendamento. Não envia se cliente estiver com opt-out.

4. **AC4 — Registro de tentativa de recuperação:** O model `Appointment` registra: `noShowDetectedAt: DateTime?`, `recoveryMessageSentAt: DateTime?`, `recoveryOutcome: String?` (valores: `null`, `'rescheduled'`, `'declined'`, `'no_response'`). Quando o cliente reagenda após uma mensagem de no-show, o `recoveryOutcome` é atualizado para `'rescheduled'`.

5. **AC5 — Dashboard mostra "No-shows recuperados":** O `EliSummaryCard` (TL-02) ou um card separado exibe a métrica "No-shows recuperados" com valor em Reais. O cálculo: `Appointment.count({ recoveryOutcome: 'rescheduled' })` × preço médio do serviço.

6. **AC6 — Configurável por organização:** O dono pode desativar ou configurar o no-show recovery nas configurações da organização: (a) tempo de espera antes de marcar como no-show (padrão: 30 min), (b) mensagem customizada (usa o template padrão se vazio), (c) toggle on/off.

7. **AC7 — Testes:** Mínimo 5 testes cobrindo: detecção correta de no-show (horário passou + 30min), não detecta se status já foi atualizado, mensagem enviada via fila (mock da fila), não envia segunda mensagem no mesmo no-show, recoveryOutcome atualizado ao reagendar.

---

## Tasks / Subtasks

- [ ] **Task 1: Schema Prisma — campos de recovery** [AC: 4]
  - [ ] Adicionar ao model `Appointment`: `noShowDetectedAt DateTime?`, `recoveryMessageSentAt DateTime?`, `recoveryOutcome String?`
  - [ ] Adicionar ao model `OrgConfig` (ou `Organization`): `noShowRecoveryEnabled Boolean @default(true)`, `noShowGracePeriodMinutes Int @default(30)`, `noShowRecoveryMessage String?`
  - [ ] Migration: `npx prisma migrate dev --name add-no-show-recovery`

- [ ] **Task 2: Cron job de detecção de no-show** [AC: 1]
  - [ ] Criar `/src/lib/cron/no-show-detector.ts` (seguir padrão de `antiban-cron.ts` já existente)
  - [ ] Query: `Appointment.findMany({ where: { status: 'CONFIRMED', scheduledAt: { lt: subMinutes(now, gracePeriod) }, noShowDetectedAt: null } })`
  - [ ] Para cada resultado: atualizar `status = 'NO_SHOW'`, salvar `noShowDetectedAt = now()`
  - [ ] Disparar job de envio de mensagem de recovery via BullMQ
  - [ ] Registrar cron no scheduler existente com intervalo de 15 minutos

- [ ] **Task 3: Job de mensagem de recovery** [AC: 2, 3]
  - [ ] Criar job handler `noShowRecoveryJob` em BullMQ
  - [ ] Buscar próximas 2 disponibilidades do profissional do agendamento original via `getAvailability()`
  - [ ] Montar mensagem com template: `buildNoShowRecoveryMessage(appointment, nextSlots)`
  - [ ] Enviar via fila antiban existente (mesma usada pelo PULSE agent)
  - [ ] Salvar `recoveryMessageSentAt = now()` no appointment

- [ ] **Task 4: Detecção de reagendamento pós-recovery** [AC: 4]
  - [ ] No handler de `create_appointment` tool: verificar se o cliente tem appointment com `recoveryMessageSentAt != null` e `recoveryOutcome = null` nas últimas 48h
  - [ ] Se sim: ao criar novo agendamento, atualizar o anterior com `recoveryOutcome = 'rescheduled'`
  - [ ] Adicionar evento no `AnalyticsEvent` (se model existir): `eventType: 'no_show_recovered'`

- [ ] **Task 5: Configurações no dashboard** [AC: 6]
  - [ ] Localizar página de configurações da organização (`src/app/(dashboard)/settings/`)
  - [ ] Adicionar seção "Recuperação de No-Show" com: toggle on/off, campo de texto para mensagem customizada, número de minutos de grace period
  - [ ] Salvar via API existente de update de OrgConfig

- [ ] **Task 6: Métrica no EliSummaryCard** [AC: 5]
  - [ ] Atualizar API `/api/dashboard/eli-summary` para incluir `noShowsRecovered` e `noShowRecoveryRevenue`
  - [ ] Atualizar `EliSummaryCard` para exibir "X faltas recuperadas" quando > 0

- [ ] **Task 7: Testes** [AC: 7]
  - [ ] `tests/unit/no-show-detector.test.ts`
  - [ ] Mock do Prisma e BullMQ
  - [ ] Mínimo 5 casos de teste conforme AC7

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, BullMQ, Redis
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos de referência para o padrão de cron existente

```
src/lib/cron/antiban-cron.ts      — padrão de cron a seguir
src/lib/cron/pulse-cron.ts        — padrão de cron com BullMQ
src/lib/agents/pulse-agent.ts     — padrão de agente proativo
```

### Template de mensagem de recovery

```typescript
function buildNoShowRecoveryMessage(
  appointment: Appointment & { contact: Contact; service: Service; professional: Professional },
  nextSlots: { date: string; time: string }[]
): string {
  const slots = nextSlots
    .slice(0, 2)
    .map(s => `${s.date} às ${s.time}`)
    .join(' ou ');

  return (
    `Oi, ${appointment.contact.name?.split(' ')[0] ?? 'tudo bem'}! ` +
    `Vi que você não conseguiu vir hoje no horário das ${formatTime(appointment.scheduledAt)}. ` +
    `Acontece! Quer reagendar? ` +
    `Tenho horários disponíveis ${slots}. ` +
    `É só me falar! 😊`
  );
}
```

### Cálculo de impacto de receita

```typescript
// No endpoint /api/dashboard/revenue-attribution
const recoveredAppointments = await prisma.appointment.count({
  where: {
    organizationId,
    recoveryOutcome: 'rescheduled',
    noShowDetectedAt: { gte: periodStart },
  },
});

const avgServicePrice = await prisma.service.aggregate({
  where: { organizationId },
  _avg: { price: true },
});

const noShowRecoveryRevenue =
  recoveredAppointments * (avgServicePrice._avg.price?.toNumber() ?? 0);
```

### Gotchas Relevantes
- BullMQ jobs devem ser idempotentes — usar `appointmentId` como `jobId` para evitar envios duplicados
- Nunca usar `sed -i` com regex global em `.ts`
- PM2 roda como user `tikso`
- Testar com Vitest: `npx vitest run --reporter=verbose tests/unit/no-show-detector.test.ts`
- O cron precisa ser registrado no processo que inicia com o servidor (verificar `src/server.ts` ou similar)

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-product-strategy-roadmap.md` — Seção 4.1 "Recuperação de No-Show" + Feature G1 Q2
  - "Impacto estimado: Recuperação de 30-40% dos no-shows = 1-2 agendamentos extras/dia = R$1.600-3.200/mês"
- `docs/research/tikso-multi-agent-architecture.md` — Seção 3 "Agentes Especializados" (RETAIN agent pattern)

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do roadmap PM (Feature G1) e arquitetura multi-agent | @sm (River) |

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
| `src/lib/cron/no-show-detector.ts` | CREATE |
| `src/lib/jobs/no-show-recovery-job.ts` | CREATE |
| `src/app/(dashboard)/settings/no-show-recovery/page.tsx` | CREATE |
| `src/app/api/dashboard/eli-summary/route.ts` | MODIFY — adicionar noShowsRecovered |
| `src/components/dashboard/eli-summary-card.tsx` | MODIFY — exibir métrica |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — detectar recovery ao criar appointment |
| `prisma/schema.prisma` | MODIFY — campos de recovery |
| `tests/unit/no-show-detector.test.ts` | CREATE |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Backend
  secondary: [Database]
  complexity: High

specialized_agents:
  primary: "@dev"
  secondary: ["@db-sage"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Cron job detecta no-shows corretamente (5+ testes passando)
      - Mensagem NÃO enviada para mesmo agendamento duas vezes (idempotência via jobId)
      - Mensagem NÃO enviada para contatos com opt-out
      - gracePeriodMinutes configurável por org
      - noShowDetectedAt salvo no banco ao detectar

  pre_pr:
    agent: "@github-devops"
    checks:
      - Migration Prisma aplicada sem conflitos
      - Cron registrado no processo principal (não "esquecido")

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Idempotência do job (não enviar duplicatas)
  - Respeito ao opt-out antes de qualquer envio
  - Cálculo correto de grace period com timezone
  - Integração com fila antiban existente (não criar fila nova)
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
