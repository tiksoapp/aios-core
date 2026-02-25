# Story ELI-07: Schedule Followup Bridge (Eli → Pulse)

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-07
**Priority:** Must Have
**Points:** 8
**Effort:** ~6 horas
**Status:** Ready for Dev
**Type:** Feature — Backend
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** —
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
**Quero** poder enfileirar um job de follow-up no BullMQ quando uma conversa indicar necessidade,
**Para que** o Pulse Agent execute a mensagem de acompanhamento no momento certo sem que eu precise permanecer ativo.

---

## Acceptance Criteria

1. **AC1 — Tool schedule_followup disponível:** A tool `schedule_followup` está registrada no array `CORE_TOOL_DEFINITIONS` de `aria-tools.ts` e é retornada por `getToolsForOrg()` para qualquer org.
2. **AC2 — Parâmetros corretos:** A tool aceita: `delay_minutes: number` (obrigatório, deve ser 30, 1440 ou 4320), `message_hint: string` (obrigatório, contexto para o Pulse gerar a mensagem certa), `followup_type: "curiosity" | "value" | "farewell"` (obrigatório).
3. **AC3 — Validação de delay_minutes:** Se `delay_minutes` não for um dos valores permitidos (30, 1440, 4320), retorna `{ error: "delay_minutes deve ser 30 (30min), 1440 (24h) ou 4320 (72h)." }`.
4. **AC4 — Limite de follow-ups por contato:** Antes de enfileirar, verificar se já existem 3 ou mais jobs pendentes de follow-up para o mesmo `contactId` na fila BullMQ. Se sim, retorna `{ error: "Limite de 3 follow-ups por contato atingido.", existing_count: N }`.
5. **AC5 — Job enfileirado no BullMQ:** Quando válido, cria um job na fila `pulse-followup` (mesma fila que o Pulse Agent já monitora) com `{ contactId, orgId, phone, message_hint, followup_type, delay_minutes }` e delay de `delay_minutes * 60 * 1000` ms.
6. **AC6 — Retorno de sucesso:** Retorna `{ success: true, job_id, scheduled_for_minutes: delay_minutes, followup_type, message: "Follow-up agendado com sucesso." }`.
7. **AC7 — Prompt atualizado:** Em `prompt-builder.ts`, adicionar instrução em `buildFlows()` para os cenários em que Eli deve considerar agendar follow-up: após criar agendamento sem confirmação do cliente, após apresentar planos de assinatura sem fechamento, após despedida de cliente interessado mas indeciso.
8. **AC8 — Testes:** Mínimo 6 testes: delay_minutes válido (30, 1440, 4320), delay_minutes inválido → erro, limite de 3 atingido → erro, job enfileirado com delay correto (em ms), job_id retornado, payload do job contém todos os campos necessários.

---

## Tasks / Subtasks

- [ ] **Task 1: Definir tool schedule_followup em aria-tools.ts** [AC: 1, 2]
  - [ ] Adicionar entrada em `CORE_TOOL_DEFINITIONS` com schema completo
  - [ ] Descrição clara: "Agenda um follow-up futuro para este contato via Pulse Agent. Use SOMENTE quando a conversa indica interesse não concretizado. Tipos: curiosity (cliente curioso mas indeciso), value (após apresentar planos), farewell (despedida com interesse)."
  - [ ] Enum `followup_type`: `["curiosity", "value", "farewell"]`
  - [ ] Enum `delay_minutes`: descrição explicando os 3 valores permitidos

- [ ] **Task 2: Implementar execução em executeToolCall()** [AC: 3, 4, 5, 6]
  - [ ] Validar `delay_minutes` contra `[30, 1440, 4320]`
  - [ ] Consultar BullMQ queue `pulse-followup` para contar jobs pendentes do `contactId` — usar `queue.getJobs(['waiting', 'delayed'])` e filtrar por `contactId`
  - [ ] Se count >= 3: retornar erro com `existing_count`
  - [ ] Enfileirar job com `queue.add('followup', payload, { delay: delay_minutes * 60 * 1000 })`
  - [ ] Retornar sucesso com `job.id`

- [ ] **Task 3: Verificar compatibilidade com pulse-agent.ts** [AC: 5]
  - [ ] Confirmar nome da fila BullMQ usada pelo Pulse Agent em `pulse-agent.ts`
  - [ ] Confirmar estrutura de payload esperada pelo Pulse (campos obrigatórios)
  - [ ] Ajustar nomes de campos se necessário para compatibilidade total

- [ ] **Task 4: Atualizar prompt** [AC: 7]
  - [ ] Em `prompt-builder.ts` `buildFlows()`: adicionar seção "FOLLOW-UP PROATIVO" com as 3 situações em que Eli deve chamar `schedule_followup`
  - [ ] Incluir exemplos de `message_hint` adequados para cada `followup_type`

- [ ] **Task 5: Testes** [AC: 8]
  - [ ] Criar arquivo `tests/unit/eli-schedule-followup.test.ts`
  - [ ] Mock BullMQ Queue: `queue.add()` e `queue.getJobs()`
  - [ ] Cobrir todos os cenários do AC8

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, BullMQ, Prisma 7.4, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/ai/aria-tools.ts` — Onde a tool será adicionada
  - `/home/tikso/tikso/src/lib/agents/pulse-agent.ts` — Pulse que já processa a fila
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — Prompt de Eli (buildFlows)

### Interface da Tool (do audit)

```typescript
// Proposta exata do audit (Aria):
{
  name: "schedule_followup",
  parameters: {
    delay_minutes: number,  // 30, 1440 (24h), 4320 (72h)
    message_hint: string,   // Context para Pulse gerar a mensagem certa
    followup_type: "curiosity" | "value" | "farewell"
  }
}
```

### Exemplo de implementação

```typescript
case "schedule_followup": {
  const { delay_minutes, message_hint, followup_type } = toolInput as {
    delay_minutes: number;
    message_hint: string;
    followup_type: "curiosity" | "value" | "farewell";
  };

  const ALLOWED_DELAYS = [30, 1440, 4320];
  if (!ALLOWED_DELAYS.includes(delay_minutes)) {
    return { error: "delay_minutes deve ser 30 (30min), 1440 (24h) ou 4320 (72h)." };
  }

  // Verificar limite de 3 follow-ups por contato
  const queue = getPulseQueue(); // helper que retorna a BullMQ Queue instance
  const pendingJobs = await queue.getJobs(["waiting", "delayed"]);
  const contactJobs = pendingJobs.filter(j => j.data.contactId === context.contactId);
  if (contactJobs.length >= 3) {
    return { error: "Limite de 3 follow-ups por contato atingido.", existing_count: contactJobs.length };
  }

  const job = await queue.add("followup", {
    contactId: context.contactId,
    orgId: context.orgId,
    phone: context.phone,
    message_hint,
    followup_type,
    delay_minutes,
    scheduledBy: "eli"
  }, {
    delay: delay_minutes * 60 * 1000
  });

  return {
    success: true,
    job_id: job.id,
    scheduled_for_minutes: delay_minutes,
    followup_type,
    message: "Follow-up agendado com sucesso."
  };
}
```

### Verificar no pulse-agent.ts

Antes de implementar, confirmar:
1. Nome exato da fila BullMQ: `grep -n "new Queue\|QueueName\|pulse" /home/tikso/tikso/src/lib/agents/pulse-agent.ts | head -20`
2. Estrutura do payload esperado pelo processor do Pulse
3. Como instanciar a Queue para enfileirar (pode haver um singleton ou factory)

### Segurança e Guardrails
- O prompt deve instruir Eli a usar `schedule_followup` SOMENTE quando o cliente demonstrou interesse mas não agendou/assinou
- Nunca chamar para clientes que explicitamente recusaram ou pediram para não ser contatados
- O limite de 3 por contato é um hard guardrail no código (não só no prompt)

### Gotchas Relevantes
- BullMQ: `queue.getJobs(['waiting', 'delayed'])` retorna Promise — sempre await
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Testar com Vitest: `npx vitest run --reporter=verbose`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-01 — Critical) | @sm (River) |

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
| `src/lib/ai/aria-tools.ts` | MODIFY — adicionar schedule_followup em CORE_TOOL_DEFINITIONS e executeToolCall() |
| `src/lib/agents/pulse-agent.ts` | READ-ONLY — verificar nome da fila e estrutura de payload (não modificar) |
| `src/lib/ai/prompt-builder.ts` | MODIFY — adicionar seção FOLLOW-UP PROATIVO em buildFlows() |
| `tests/unit/eli-schedule-followup.test.ts` | CREATE — testes unitários para schedule_followup |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
