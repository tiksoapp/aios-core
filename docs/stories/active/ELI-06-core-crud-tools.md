# Story ELI-06: Core CRUD Tools (remove_tag, update_contact, list_pipeline_stages)

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-06
**Priority:** Must Have
**Points:** 5
**Effort:** ~4 horas
**Status:** Ready for Dev
**Type:** Feature — Backend
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** ELI-01 (mesma base de arquivos: aria-tools.ts)
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
**Quero** poder remover tags incorretas, atualizar dados de contato e listar os estágios do pipeline disponíveis,
**Para que** eu possa manter as informações do cliente corretas sem precisar acionar um humano para correções triviais.

---

## Acceptance Criteria

1. **AC1 — remove_tag implementada:** A tool `remove_tag` está disponível no tool-calling loop de Eli, com parâmetro `tag_name: string` obrigatório. Remove a tag do contato atual (identificado via `orgId` + `contactId` do contexto da requisição). Se a tag não existir, retorna `{ success: true, message: "Tag nao encontrada (noop)" }` — idempotente.
2. **AC2 — remove_tag definida em aria-tools.ts:** A definição da tool segue exatamente o mesmo padrão de `add_tag` (mesma estrutura de schema, mesmo estilo de implementação inline). O campo `description` instrui claramente: "Remove uma tag do contato. Use quando uma tag foi aplicada incorretamente."
3. **AC3 — update_contact implementada:** A tool `update_contact` está disponível, com parâmetros opcionais `name?: string` e `email?: string`. Atualiza apenas os campos informados via `db.contact.update()`. Campos nunca permitidos (phone, orgId, etc.) são rejeitados na definição do schema — não aceitos como parâmetro.
4. **AC4 — update_contact com validação:** Se nem `name` nem `email` forem informados, retorna `{ error: "Informe ao menos um campo para atualizar (name ou email)." }`. Se o `email` informado for inválido (sem `@`), retorna erro de validação.
5. **AC5 — list_pipeline_stages implementada:** A tool `list_pipeline_stages` está disponível, sem parâmetros. Retorna `{ stages: [{ id, name, pipelineName, position }], count }` consultando `db.pipelineStage.findMany({ where: { pipeline: { orgId } } })`.
6. **AC6 — Todas as 3 tools registradas em getToolsForOrg:** As tools aparecem no array de `CORE_TOOL_DEFINITIONS` e são retornadas por `getToolsForOrg()` para qualquer org.
7. **AC7 — Testes:** Mínimo 8 testes: remove_tag (encontrou e removeu, não encontrou noop), update_contact (nome OK, email OK, ambos OK, nenhum campo → erro, email inválido → erro), list_pipeline_stages (retorna lista, sem stages retorna array vazio).

---

## Tasks / Subtasks

- [ ] **Task 1: Implementar remove_tag** [AC: 1, 2, 6]
  - [ ] Adicionar definição de tool `remove_tag` em `aria-tools.ts` no array `CORE_TOOL_DEFINITIONS`
  - [ ] Schema: `{ name: "remove_tag", description: "...", parameters: { tag_name: { type: "string", description: "Nome exato da tag a remover" } }, required: ["tag_name"] }`
  - [ ] Implementar execução inline em `executeToolCall()`: buscar tag por `contactId` + `tag_name`, deletar com `db.contactTag.deleteMany()` (idempotente)
  - [ ] Retornar `{ success: true, message: "Tag '{tag_name}' removida." }` ou `{ success: true, message: "Tag nao encontrada (noop)." }`

- [ ] **Task 2: Implementar update_contact** [AC: 3, 4, 6]
  - [ ] Adicionar definição de tool `update_contact` em `aria-tools.ts` no array `CORE_TOOL_DEFINITIONS`
  - [ ] Schema: parâmetros `name` (string, opcional) e `email` (string, opcional) — nenhum required
  - [ ] Validação: se nenhum campo informado → erro; se email sem `@` → erro de validação
  - [ ] Implementar `db.contact.update({ where: { id: contactId }, data: { ...name && { name }, ...email && { email } } })`
  - [ ] Retornar `{ success: true, updated: { name?, email? }, message: "Contato atualizado." }`

- [ ] **Task 3: Implementar list_pipeline_stages** [AC: 5, 6]
  - [ ] Adicionar definição de tool `list_pipeline_stages` em `aria-tools.ts` no array `CORE_TOOL_DEFINITIONS`
  - [ ] Schema: sem parâmetros — `parameters: {}`, `required: []`
  - [ ] Implementar: `db.pipelineStage.findMany({ where: { pipeline: { orgId } }, include: { pipeline: { select: { name: true } } }, orderBy: { position: 'asc' } })`
  - [ ] Mapear retorno para `{ stages: [{ id, name, pipelineName: stage.pipeline.name, position }], count: stages.length }`

- [ ] **Task 4: Testes** [AC: 7]
  - [ ] Criar arquivo de testes `tests/unit/eli-crud-tools.test.ts`
  - [ ] Mock `db.contactTag.deleteMany`, `db.contact.update`, `db.pipelineStage.findMany`
  - [ ] Cobrir todos os cenários listados no AC7

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivo principal:** `/home/tikso/tikso/src/lib/ai/aria-tools.ts`

### Padrão de Referência — add_tag (copiar estrutura)

A tool `add_tag` já existente em `aria-tools.ts` é o template exato para `remove_tag`. Seguir o mesmo padrão:

```typescript
// CORE_TOOL_DEFINITIONS (fragmento - add_tag como referência)
{
  name: "add_tag",
  description: "Adiciona uma tag ao contato atual.",
  input_schema: {
    type: "object",
    properties: {
      tag_name: {
        type: "string",
        description: "Nome da tag a adicionar"
      }
    },
    required: ["tag_name"]
  }
}

// Execução inline em executeToolCall() para add_tag:
case "add_tag": {
  const { tag_name } = toolInput as { tag_name: string };
  const existing = await db.contactTag.findFirst({
    where: { contactId: context.contactId, name: tag_name }
  });
  if (existing) return { success: true, message: `Tag '${tag_name}' ja existe.`, already_existed: true };
  await db.contactTag.create({ data: { contactId: context.contactId, name: tag_name, orgId: context.orgId } });
  return { success: true, message: `Tag '${tag_name}' adicionada.` };
}

// NOVA — remove_tag:
case "remove_tag": {
  const { tag_name } = toolInput as { tag_name: string };
  const result = await db.contactTag.deleteMany({
    where: { contactId: context.contactId, name: tag_name }
  });
  if (result.count === 0) return { success: true, message: `Tag '${tag_name}' nao encontrada (noop).` };
  return { success: true, message: `Tag '${tag_name}' removida com sucesso.` };
}
```

### Padrão update_contact

```typescript
case "update_contact": {
  const { name, email } = toolInput as { name?: string; email?: string };
  if (!name && !email) return { error: "Informe ao menos um campo para atualizar (name ou email)." };
  if (email && !email.includes("@")) return { error: "Email invalido." };
  const updated = await db.contact.update({
    where: { id: context.contactId },
    data: { ...(name && { name }), ...(email && { email }) }
  });
  return { success: true, updated: { name: updated.name, email: updated.email }, message: "Contato atualizado." };
}
```

### Padrão list_pipeline_stages

```typescript
case "list_pipeline_stages": {
  const stages = await db.pipelineStage.findMany({
    where: { pipeline: { orgId: context.orgId } },
    include: { pipeline: { select: { name: true } } },
    orderBy: { position: "asc" }
  });
  return {
    stages: stages.map(s => ({ id: s.id, name: s.name, pipelineName: s.pipeline.name, position: s.position })),
    count: stages.length
  };
}
```

### Contexto disponível em executeToolCall

As tools core têm acesso ao `context` que inclui `orgId`, `contactId`, `phone`. Verificar a assinatura exata da função em `aria-tools.ts` para confirmar o nome do parâmetro de contexto.

### Gotchas Relevantes
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Testar com Vitest: `npx vitest run --reporter=verbose`
- `db.contactTag.deleteMany` é idempotente — não lança erro se não encontrar registros (retorna `count: 0`)

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-03, GAP-04, GAP-05) | @sm (River) |

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
| `src/lib/ai/aria-tools.ts` | MODIFY — adicionar remove_tag, update_contact, list_pipeline_stages em CORE_TOOL_DEFINITIONS e executeToolCall() |
| `tests/unit/eli-crud-tools.test.ts` | CREATE — testes unitários para as 3 novas tools |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
