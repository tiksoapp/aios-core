# Story ELI-05: Verificação Proativa de Assinante

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-05
**Priority:** Medium
**Points:** 3
**Effort:** ~2 horas
**Status:** Ready for Dev
**Type:** Feature — Backend
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** ELI-01
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

**Como** cliente assinante da barbearia,
**Quero** que a IA reconheça automaticamente que sou assinante ao iniciar um agendamento,
**Para que** eu receba tratamento prioritário e a experiência personalizada que meu plano oferece.

---

## Acceptance Criteria

1. **AC1 — Check proativo no fluxo de agendamento:** Quando o fluxo de agendamento inicia (antes de oferecer horários), a IA verifica automaticamente o status de assinatura do cliente via `get_subscriber_status`, sem o cliente precisar mencionar "assinatura" ou "plano".
2. **AC2 — Informação surfada para o LLM:** O resultado do check de assinatura é incluído no contexto do LLM para que possa personalizar a resposta (ex: "E aí Kelmer, o de sempre com o Natan?" para assinantes recorrentes).
3. **AC3 — create_appointment inclui info de assinatura na resposta:** Quando `create_appointment` executa com sucesso, a resposta inclui `is_subscriber: true/false` e `plan_name` (se aplicável), para que o LLM possa mencionar na confirmação.
4. **AC4 — Prompt atualizado:** `buildFlows()` instrui: "No início do fluxo de agendamento, chame get_subscriber_status. Se assinante, personalize: mencione o plano e sugira 'o de sempre' se houver histórico."
5. **AC5 — Testes:** Mínimo 3 testes: assinante detectado e surfado, não-assinante sem erro, create_appointment inclui subscriber info.

---

## Tasks / Subtasks

- [ ] **Task 1: Atualizar prompt para check proativo** [AC: 1, 4]
  - [ ] Em `prompt-builder.ts` `buildFlows()`: adicionar step no fluxo de agendamento: "Chame get_subscriber_status antes de check_availability"
  - [ ] Adicionar instrução de personalização para assinantes
  - [ ] Atualizar regra 20 em `buildRules()`: além do caso negativo, incluir caso positivo ("Se assinante, mencione o plano e personalize")

- [ ] **Task 2: Enriquecer resposta do create_appointment** [AC: 3]
  - [ ] Em `tool-implementations.ts` `toolCreateAppointment`: incluir `is_subscriber` e `plan_name` na resposta de sucesso (linhas 694-704)
  - [ ] O check interno de subscriber (linhas 631-642) já existe — apenas surfar o resultado

- [ ] **Task 3: Testes** [AC: 5]
  - [ ] Teste: `create_appointment` retorna `is_subscriber: true` e `plan_name` para assinante
  - [ ] Teste: `create_appointment` retorna `is_subscriber: false` para não-assinante
  - [ ] Teste: verificar que prompt contém instrução de check proativo

---

## Dev Notes

### Stack e Contexto
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — `buildFlows()`, `buildRules()` regra 20
  - `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tool-implementations.ts` — `toolCreateAppointment` (linhas 631-642 check interno, 694-704 resposta)

### Código Existente
O `create_appointment` JÁ faz check de subscriber internamente (linhas 631-642):
```typescript
let appointmentType = "fit";
try {
  const subStatus = await toolGetSubscriberStatus(orgId, config, contactId);
  if (subStatus?.is_subscriber === true) {
    appointmentType = "signature";
  }
} catch { /* default to "fit" */ }
```
O resultado NÃO é incluído na resposta. Basta surfar `is_subscriber` e `plan_name`.

### Impacto na Experiência
- **Assinante recorrente:** "E aí Kelmer, o de sempre com o Natan? Corte + barba às 16h?"
- **Assinante novo fluxo:** "Vi que você tem o plano Corte + Barba Ilimitado. Bora agendar?"
- **Não assinante:** Fluxo normal, sem menção a plano

### Gotchas Relevantes
- `get_subscriber_status` faz 1 API call extra — aceitável pois a informação tem alto valor
- Se a API falhar, o fluxo continua normalmente (não-assinante por default)
- Depende de ELI-01 para o novo fluxo de `service_name` funcionar corretamente

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-24 | 1.0 | Story criada a partir dos audits Dev (Bug #3), Architect (Falha #3), Copy Chief (regra "o de sempre?"), e Analyst (RICE #5) | @sm (River) |

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
| `src/lib/ai/prompt-builder.ts` | MODIFY — adicionar step de subscriber check no fluxo, atualizar regra 20 |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — surfar is_subscriber e plan_name na resposta do create_appointment |
| `tests/unit/subscriber-check.test.ts` | CREATE — testes de verificação proativa |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
