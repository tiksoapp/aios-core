# Story ELI-08: Business Hours Tool + Knowledge Base Prompt Fix

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-08
**Priority:** Should Have
**Points:** 3
**Effort:** ~3 horas
**Status:** Ready for Dev
**Type:** Feature + Prompt Fix — Backend
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** —
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

**Como** Eli (agente autônomo da barbearia),
**Quero** ter acesso direto aos horários de funcionamento do DB e receber instruções claras no prompt para usar `search_knowledge_base` e `get_contact_info`,
**Para que** eu não alucinei horários e use as tools disponíveis de forma consistente.

---

## Acceptance Criteria

1. **AC1 — Tool get_business_hours implementada:** A tool `get_business_hours` está disponível no loop de Eli, sem parâmetros. Retorna os horários de funcionamento da org atual consultando a tabela `businessHours` do DB.
2. **AC2 — Retorno estruturado:** A tool retorna `{ business_hours: [{ day_of_week: string, opens_at: string, closes_at: string, is_closed: boolean }], timezone, is_open_now: boolean }`. O campo `is_open_now` é calculado com base no horário atual (UTC vs timezone da org).
3. **AC3 — Integração correta com schema Prisma:** A implementação usa o modelo `businessHours` existente (o mesmo já usado nas guardrails do autonomous-agent.ts). Verificar campos exatos do modelo antes de implementar.
4. **AC4 — Prompt menciona search_knowledge_base explicitamente:** Em `buildFlows()` do `prompt-builder.ts`, adicionar instrução explícita: "Para informações gerais (localização, formas de pagamento, políticas da barbearia): chame `search_knowledge_base` com a query relevante." Remover dependência implícita do modelo inferir pelo nome da tool.
5. **AC5 — Prompt menciona get_contact_info explicitamente:** Em `buildFlows()`, adicionar instrução: "Se precisar verificar ou atualizar dados do cliente durante a conversa (nome, email, tags atuais): chame `get_contact_info`." Isso alinha a tool com o fluxo de update_contact (ELI-06).
6. **AC6 — Prompt menciona get_business_hours:** Em `buildFlows()`, substituir a instrução genérica "informe horários" por: "Para informar horários de funcionamento: chame `get_business_hours`. Use `is_open_now` para confirmar se estamos abertos agora."
7. **AC7 — Testes:** Mínimo 4 testes: get_business_hours retorna estrutura correta, is_open_now calculado corretamente para horário dentro e fora do expediente, org sem businessHours retorna array vazio com is_open_now=false.

---

## Tasks / Subtasks

- [ ] **Task 1: Implementar get_business_hours** [AC: 1, 2, 3]
  - [ ] Verificar schema Prisma: `grep -n "businessHours\|BusinessHours" /home/tikso/tikso/prisma/schema.prisma`
  - [ ] Adicionar definição da tool em `CORE_TOOL_DEFINITIONS` em `aria-tools.ts`
  - [ ] Implementar consulta: `db.businessHours.findMany({ where: { orgId: context.orgId } })`
  - [ ] Calcular `is_open_now` com base no `dayOfWeek` atual e horário atual vs `opensAt`/`closesAt`
  - [ ] Registrar em `executeToolCall()`

- [ ] **Task 2: Atualizar prompt — search_knowledge_base** [AC: 4]
  - [ ] Em `prompt-builder.ts` `buildFlows()`: adicionar instrução explícita citando o nome da tool
  - [ ] Localizar a menção atual implícita "Use a base de conhecimento" e substituir por menção explícita

- [ ] **Task 3: Atualizar prompt — get_contact_info** [AC: 5]
  - [ ] Em `buildFlows()`: adicionar instrução explícita para uso de `get_contact_info`
  - [ ] Conectar com o fluxo de correção de dados do cliente (ELI-06 update_contact)

- [ ] **Task 4: Atualizar prompt — get_business_hours** [AC: 6]
  - [ ] Substituir instrução genérica de horários pela chamada explícita à tool
  - [ ] Incluir instrução sobre o campo `is_open_now`

- [ ] **Task 5: Testes** [AC: 7]
  - [ ] Criar arquivo `tests/unit/eli-business-hours.test.ts`
  - [ ] Mock `db.businessHours.findMany`
  - [ ] Testar cálculo de `is_open_now` com timezone fixo para evitar dependência de hora atual

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/ai/aria-tools.ts` — Tool a adicionar
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — Prompt fixes (buildFlows)
  - `/home/tikso/tikso/prisma/schema.prisma` — Verificar schema BusinessHours

### Como verificar o modelo businessHours no DB

```bash
grep -n "businessHours\|BusinessHours\|business_hours" /home/tikso/tikso/prisma/schema.prisma
```

O modelo já é usado em `autonomous-agent.ts` para guardrails de horário. Reutilizar a mesma query como referência:

```bash
grep -n "businessHours" /home/tikso/tikso/src/lib/ai/autonomous-agent.ts | head -20
```

### Implementação esperada de get_business_hours

```typescript
case "get_business_hours": {
  const hours = await db.businessHours.findMany({
    where: { orgId: context.orgId },
    orderBy: { dayOfWeek: "asc" }
  });

  const DAY_NAMES = ["Domingo", "Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"];
  const now = new Date();
  const currentDay = now.getDay(); // 0=Sun, 1=Mon...
  const todayHours = hours.find(h => h.dayOfWeek === currentDay);

  let isOpenNow = false;
  if (todayHours && !todayHours.isClosed) {
    const [openH, openM] = todayHours.opensAt.split(":").map(Number);
    const [closeH, closeM] = todayHours.closesAt.split(":").map(Number);
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    const openMinutes = openH * 60 + openM;
    const closeMinutes = closeH * 60 + closeM;
    isOpenNow = currentMinutes >= openMinutes && currentMinutes < closeMinutes;
  }

  return {
    business_hours: hours.map(h => ({
      day_of_week: DAY_NAMES[h.dayOfWeek],
      opens_at: h.opensAt,
      closes_at: h.closesAt,
      is_closed: h.isClosed
    })),
    is_open_now: isOpenNow,
    count: hours.length
  };
}
```

### Mudanças no prompt (buildFlows)

**Antes (GAP-11):** Eli precisa inferir que "base de conhecimento" = `search_knowledge_base`.

**Depois:** Instrução explícita como as demais tools:
```
Para informações gerais (endereço, formas de pagamento, políticas): chame search_knowledge_base.
Para horários de funcionamento: chame get_business_hours. Use o campo is_open_now para saber se estamos abertos agora.
Para verificar/confirmar dados do cliente durante a conversa: chame get_contact_info.
```

### Contexto do GAP-07 (do audit)
A tabela `businessHours` já existe no DB e é consultada no `autonomous-agent.ts` como guardrail de horário de funcionamento. A tool apenas expõe essa mesma query para o loop de tool-calling da LLM, eliminando o risco de alucinação de horários.

### Gotchas Relevantes
- Verificar campos exatos do model `BusinessHours` antes de implementar (pode ser camelCase ou snake_case no Prisma)
- O cálculo de `is_open_now` usa horário do servidor (UTC). Se a org tiver timezone diferente, ajustar usando a timezone da org (verificar se há campo `timezone` na tabela `Organization`)
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-07, GAP-11, GAP-12) | @sm (River) |

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
| `src/lib/ai/aria-tools.ts` | MODIFY — adicionar get_business_hours em CORE_TOOL_DEFINITIONS e executeToolCall() |
| `src/lib/ai/prompt-builder.ts` | MODIFY — mencionar explicitamente search_knowledge_base, get_contact_info e get_business_hours em buildFlows() |
| `tests/unit/eli-business-hours.test.ts` | CREATE — testes unitários para get_business_hours |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
