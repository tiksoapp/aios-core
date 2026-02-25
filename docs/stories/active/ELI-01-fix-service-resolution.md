# Story ELI-01: Fix Service Resolution nas Tools BestBarbers

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-01
**Priority:** Must Have
**Points:** 5
**Effort:** ~4 horas
**Status:** Ready for Dev
**Type:** Bug Fix — Backend
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

**Como** cliente da barbearia usando WhatsApp,
**Quero** que a IA me ofereça apenas horários que realmente cabem no serviço que eu escolhi,
**Para que** eu não perca tempo escolhendo um horário que depois será recusado.

---

## Acceptance Criteria

1. **AC1 — check_availability aceita service_name:** A tool `check_availability` aceita um parâmetro opcional `service_name` (string). Quando informado, a tool internamente resolve a duração via `getServices()` e usa o valor correto no algoritmo de slots.
2. **AC2 — check_availability rejeita chamada sem contexto de duração:** Se nem `service_name` nem `duration_minutes` forem informados, a tool retorna erro com hint: `"Informe service_name ou duration_minutes. Chame get_services para obter as opcoes."` — NÃO usa default de 30min.
3. **AC3 — create_appointment aceita service_name:** A tool `create_appointment` aceita `service_name` como alternativa a `service_id`. A resolução interna segue o mesmo padrão já usado para `barber_name` (fuzzy match via `getServices()`).
4. **AC4 — Prompt atualizado:** A regra 14 do `buildRules` é atualizada para refletir o novo fluxo: "Sempre informe service_name em check_availability e create_appointment."
5. **AC5 — Backward compatibility:** Se `service_id` ou `duration_minutes` forem passados diretamente, continuam funcionando como antes (nenhuma breaking change).
6. **AC6 — Testes:** Mínimo 6 testes cobrindo: service_name resolve corretamente, chamada sem parâmetros retorna erro, service_id ainda funciona, duration_minutes ainda funciona, fuzzy match com nome parcial, serviço não encontrado retorna erro claro.

---

## Tasks / Subtasks

- [ ] **Task 1: Modificar check_availability** [AC: 1, 2]
  - [ ] Adicionar parâmetro `service_name` (string, opcional) na definição da tool em `tools.ts`
  - [ ] Em `tool-implementations.ts` `toolCheckAvailability`: quando `service_name` informado, chamar `getServices()` e resolver duração
  - [ ] Remover default de 30min na linha 101: `const serviceDuration = Math.max(30, durationMinutes ?? 30)`
  - [ ] Se nem `service_name` nem `duration_minutes`: retornar `{ error: "...", hint: "call_get_services_first" }`
  - [ ] Manter `duration_minutes` como fallback funcional

- [ ] **Task 2: Modificar create_appointment** [AC: 3]
  - [ ] Adicionar parâmetro `service_name` (string, opcional) na definição da tool em `tools.ts`
  - [ ] Em `tool-implementations.ts` `toolCreateAppointment`: quando `service_name` informado e `service_id` ausente, resolver via `getServices()` + fuzzy match (mesmo padrão de `barber_name`)
  - [ ] Se ambos `service_name` e `service_id` informados, `service_id` tem precedência

- [ ] **Task 3: Atualizar prompt** [AC: 4]
  - [ ] Em `prompt-builder.ts` `buildRules()`: atualizar regra 14 para mencionar `service_name`
  - [ ] Em `buildFlows()`: atualizar fluxo de agendamento para instruir uso de `service_name`

- [ ] **Task 4: Testes** [AC: 6]
  - [ ] Testes unitários para `toolCheckAvailability` com/sem `service_name`
  - [ ] Testes unitários para `toolCreateAppointment` com `service_name`
  - [ ] Teste de regressão: chamadas existentes com `service_id`/`duration_minutes` continuam funcionando

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tools.ts` — Schemas das tools
  - `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tool-implementations.ts` — Implementações (linhas 101, 306-319, 631-668)
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — System prompt (regra 14, buildFlows)

### Padrão de Referência
A tool `create_appointment` já aceita `barber_name` (string) e resolve internamente para `barber_id` via `getBarbers()` + fuzzy match. Seguir exatamente o mesmo padrão para `service_name`.

### Root Cause (do Audit)
- **Bug Horários Fantasma:** `check_availability` chamada sem `duration_minutes` usa default 30min. IA ofereceu 18:00 para Kelmer, mas "Corte+Barba" (60min) não cabia pois Natan tinha compromisso às 18:30.
- **Bug Falha de Agendamento:** HTTP 400 "Informe a data atual" — possivelmente causado por `service_id` incorreto ou formato de data. Com `service_name` resolução interna, elimina-se o risco de ID errado.

### Gotchas Relevantes
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Testar com Vitest: `npx vitest run --reporter=verbose`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-24 | 1.0 | Story criada a partir do audit de 4 agentes (Copy Chief, Analyst, Dev, Architect) sobre conversa Kelmer Palma | @sm (River) |

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
| `src/lib/integrations/providers/bestbarbers/tools.ts` | MODIFY — adicionar service_name em check_availability e create_appointment |
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — resolver service_name internamente, remover default 30min |
| `src/lib/ai/prompt-builder.ts` | MODIFY — atualizar regra 14 e fluxo de agendamento |
| `tests/unit/bestbarbers-tools.test.ts` | CREATE — testes de service resolution |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
