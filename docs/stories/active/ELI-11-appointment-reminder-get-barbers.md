# Story ELI-11: Appointment Reminder + Get Barbers Standalone

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-11
**Priority:** Should Have
**Points:** 5
**Effort:** ~4 horas
**Status:** Ready for Dev
**Type:** Feature — Backend
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** ELI-07 (padrão BullMQ estabelecido)
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

**Como** Eli (agente autônomo da barbearia),
**Quero** poder listar barbeiros disponíveis sem precisar carregar todos os serviços e agendar lembretes de compromisso para o cliente,
**Para que** eu responda perguntas sobre "quem trabalha hoje" de forma eficiente e ofereça confirmação de lembrete após criar um agendamento.

---

## Acceptance Criteria

1. **AC1 — Tool get_barbers implementada:** A tool `get_barbers` está disponível no loop de tool-calling de Eli, sem parâmetros obrigatórios. Aceita `date?: string` (formato YYYY-MM-DD) opcional para filtrar barbeiros disponíveis em uma data específica.
2. **AC2 — Retorno de get_barbers:** Retorna `{ barbers: [{ name, restrictions?: string[] }], total_barbers, date_checked?: string }`. A lista de barbeiros vem da integração BestBarbers (mesmo fonte que `get_services` usa) mas sem carregar serviços.
3. **AC3 — get_barbers é mais leve que get_services:** A implementação de `get_barbers` chama apenas a API de barbeiros (não a de serviços). Se a API BestBarbers não tiver endpoint dedicado para barbeiros, pode usar `get_services` internamente mas retornar APENAS os campos de barbeiros (não expor serviços na resposta para o LLM).
4. **AC4 — Prompt atualizado para get_barbers:** Em `buildFlows()`, substituir a instrução "QUEM TRABALHA HOJE: chame get_services (retorna barbeiros ativos)" por "QUEM TRABALHA HOJE: chame get_barbers."
5. **AC5 — Tool schedule_appointment_reminder implementada:** A tool `schedule_appointment_reminder` está disponível, com parâmetros `appointment_id: number` (obrigatório), `remind_before_minutes: number` (obrigatório, deve ser 30, 60 ou 120), `contact_phone?: string` (opcional, usa phone do contexto se omitido).
6. **AC6 — Validação de remind_before_minutes:** Apenas os valores 30, 60 ou 120 são aceitos. Outros valores retornam `{ error: "remind_before_minutes deve ser 30, 60 ou 120." }`.
7. **AC7 — Job de lembrete enfileirado:** Após validação, cria job no BullMQ com `{ contactId, orgId, phone, appointment_id, remind_before_minutes, type: "appointment_reminder" }` e delay calculado: se `appointment_time` disponível via consulta ao DB, `delay = appointment_time - remind_before_minutes*60*1000 - now`. Se appointment não encontrado no DB, retorna erro.
8. **AC8 — Retorno de schedule_appointment_reminder:** `{ success: true, job_id, appointment_id, remind_before_minutes, message: "Lembrete agendado. Avisarei X minutos antes do seu compromisso." }`.
9. **AC9 — Prompt sugere lembrete após create_appointment:** Em `buildFlows()`, após o fluxo de criação de agendamento, adicionar: "Após criar agendamento com sucesso, OFEREÇA ao cliente agendar um lembrete: 'Deseja que eu te avise 1 hora antes do seu compromisso?'"
10. **AC10 — Testes:** Mínimo 7 testes: get_barbers retorna apenas barbeiros (não serviços), get_barbers com date filtra corretamente, schedule_appointment_reminder com remind=30 (sucesso), remind valor inválido (erro), appointment_id não encontrado (erro), job enfileirado com delay correto.

---

## Tasks / Subtasks

- [ ] **Task 1: Implementar get_barbers em tools.ts (BB integration)** [AC: 1, 2, 3]
  - [ ] Verificar se a API BestBarbers tem endpoint dedicado para barbeiros: `grep -rn "barber\|getBarbers" /home/tikso/tikso/src/lib/integrations/providers/bestbarbers/ | head -20`
  - [ ] Adicionar `get_barbers` em `BB_TOOL_DEFINITIONS` de `tools.ts`
  - [ ] Implementar em `tool-implementations.ts` (ou `executeBBTool` dispatcher)
  - [ ] Se não há endpoint dedicado: chamar `getServices()` internamente e retornar apenas o campo `barbers` da resposta

- [ ] **Task 2: Atualizar prompt para get_barbers** [AC: 4]
  - [ ] Em `buildFlows()` de `prompt-builder.ts`: substituir instrução de get_services para barbeiros por get_barbers
  - [ ] Remover ambiguidade: deixar claro que `get_services` é para serviços/preços, `get_barbers` é para profissionais

- [ ] **Task 3: Implementar schedule_appointment_reminder** [AC: 5, 6, 7, 8]
  - [ ] Adicionar definição em `CORE_TOOL_DEFINITIONS` de `aria-tools.ts`
  - [ ] Validar `remind_before_minutes` contra `[30, 60, 120]`
  - [ ] Consultar DB para obter `appointment.startTime` pelo `appointment_id`
  - [ ] Calcular delay em ms: `Math.max(0, appointment.startTime.getTime() - (remind_before_minutes * 60 * 1000) - Date.now())`
  - [ ] Enfileirar job na fila BullMQ (mesma usada pelo Pulse para follow-ups, ou fila dedicada `appointment-reminders`)
  - [ ] Retornar sucesso com `job_id`

- [ ] **Task 4: Atualizar prompt para lembrete após agendamento** [AC: 9]
  - [ ] Em `buildFlows()`: após confirmação de `create_appointment`, adicionar sugestão de lembrete

- [ ] **Task 5: Testes** [AC: 10]
  - [ ] Criar `tests/unit/eli-barbers-reminder.test.ts`
  - [ ] Mock da API BestBarbers para get_barbers
  - [ ] Mock BullMQ e `db.appointment.findUnique` para schedule_appointment_reminder
  - [ ] Cobrir todos os cenários do AC10

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, BullMQ, Prisma 7.4, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tools.ts` — BB tool definitions
  - `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tool-implementations.ts` — BB implementações
  - `/home/tikso/tikso/src/lib/ai/aria-tools.ts` — Core tools (schedule_appointment_reminder aqui)
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — buildFlows

### Investigar API BestBarbers para get_barbers

```bash
# Ver como get_services busca barbeiros atualmente:
grep -n "barber\|getBarbers\|getServices" /home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tool-implementations.ts | head -30
```

Se `getServices()` já retorna `barbers` como parte da resposta, a implementação de `get_barbers` pode ser simplesmente:

```typescript
// Em tool-implementations.ts:
async function toolGetBarbers(config: BestBarbersConfig, args: { date?: string }) {
  // Opção 1: Endpoint dedicado (verificar se existe)
  // Opção 2: Usar getServices() e filtrar
  const result = await getServices(config);
  if ("error" in result) return result;
  return {
    barbers: result.barbers,
    total_barbers: result.total_barbers,
    ...(args.date && { date_checked: args.date })
  };
}
```

### Cálculo de delay para lembrete

```typescript
case "schedule_appointment_reminder": {
  const { appointment_id, remind_before_minutes, contact_phone } = toolInput as {
    appointment_id: number;
    remind_before_minutes: number;
    contact_phone?: string;
  };

  const ALLOWED = [30, 60, 120];
  if (!ALLOWED.includes(remind_before_minutes)) {
    return { error: "remind_before_minutes deve ser 30, 60 ou 120." };
  }

  // Buscar appointment no DB
  const appt = await db.appointment.findUnique({
    where: { id: appointment_id },
    select: { startTime: true, orgId: true }
  });
  if (!appt) return { error: `Agendamento ${appointment_id} nao encontrado.` };

  const reminderTime = appt.startTime.getTime() - (remind_before_minutes * 60 * 1000);
  const delayMs = Math.max(0, reminderTime - Date.now());

  if (delayMs === 0) {
    return { error: "Agendamento ja passou ou esta muito proximo para agendar lembrete." };
  }

  const phone = contact_phone ?? context.phone;
  const queue = getPulseQueue();
  const job = await queue.add("appointment_reminder", {
    contactId: context.contactId,
    orgId: context.orgId,
    phone,
    appointment_id,
    remind_before_minutes,
    type: "appointment_reminder"
  }, { delay: delayMs });

  return {
    success: true,
    job_id: job.id,
    appointment_id,
    remind_before_minutes,
    message: `Lembrete agendado. Avisarei ${remind_before_minutes} minutos antes do seu compromisso.`
  };
}
```

### Verificar modelo Appointment no Prisma

```bash
grep -n "model Appointment\|startTime\|start_time" /home/tikso/tikso/prisma/schema.prisma | head -10
```

### Gotchas Relevantes
- BullMQ delay em ms: `remind_before_minutes * 60 * 1000`
- `Math.max(0, ...)` evita delay negativo se o agendamento já passou
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-09, GAP-10) | @sm (River) |

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
| `src/lib/integrations/providers/bestbarbers/tools.ts` | MODIFY — adicionar get_barbers em BB_TOOL_DEFINITIONS |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — implementar toolGetBarbers |
| `src/lib/ai/aria-tools.ts` | MODIFY — adicionar schedule_appointment_reminder em CORE_TOOL_DEFINITIONS e executeToolCall() |
| `src/lib/ai/prompt-builder.ts` | MODIFY — substituir get_services por get_barbers na instrução de "quem trabalha", adicionar sugestão de lembrete |
| `tests/unit/eli-barbers-reminder.test.ts` | CREATE — testes unitários |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
