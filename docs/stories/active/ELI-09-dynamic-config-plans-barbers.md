# Story ELI-09: Dynamic Config (Subscription Plans + Barber Names)

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-09
**Priority:** Could Have
**Points:** 3
**Effort:** ~3 horas
**Status:** Ready for Dev
**Type:** Refactor — Backend
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

**Como** operador do Tikso CRM,
**Quero** que os preços dos planos de assinatura e as normalizações de nomes de barbeiros sejam configuráveis sem redeployar código,
**Para que** uma mudança de preço ou a adição de um novo barbeiro não exija alteração manual no código da IA.

---

## Acceptance Criteria

1. **AC1 — Preços de planos removidos do código:** A função `buildFlows()` em `prompt-builder.ts` não contém mais valores hardcoded de preço (R$79,90, R$99,90, R$129,90, etc.). Os preços são carregados dinamicamente.
2. **AC2 — Preços via Knowledge Base:** Uma entrada na Knowledge Base (tabela `knowledgeBase` ou equivalente) com `category: "subscription_plans"` contém os preços atualizados. O `buildFlows()` busca esta entrada via `db.knowledgeBase.findFirst({ where: { orgId, category: "subscription_plans" } })` e injeta o conteúdo no prompt. Se não encontrar, usa um fallback genérico: "Consulte nossos planos disponíveis."
3. **AC3 — Fallback gracioso para preços:** Se a entrada da KB não existir ou a query falhar, o sistema não quebra — usa o texto de fallback e loga um warning. Eli ainda funciona normalmente.
4. **AC4 — Normalização de nomes de barbeiros configurável:** A lista de alias de nomes em `prompt-builder.ts` (ex: "Wanderson=Vanderson, Stefane=Stephane, Nathan/Nattan=Natan") é movida para uma constante exportável `BARBER_NAME_ALIASES` em um novo arquivo de configuração `src/lib/ai/eli-config.ts`.
5. **AC5 — eli-config.ts como fonte única:** O arquivo `eli-config.ts` exporta: `BARBER_NAME_ALIASES: Record<string, string[]>` (chave = nome canônico, valor = array de aliases). O `prompt-builder.ts` importa e usa este objeto para gerar a regra de normalização dinamicamente.
6. **AC6 — Adicionar novo alias não exige mudança no prompt-builder.ts:** Para adicionar "Joao=João=Joãozinho", basta editar `BARBER_NAME_ALIASES` em `eli-config.ts`. O `buildRules()` gera a instrução textual automaticamente a partir do objeto.
7. **AC7 — Testes:** Mínimo 4 testes: preços carregados da KB e injetados no prompt, fallback quando KB vazia, BARBER_NAME_ALIASES importado corretamente em buildRules, geração dinâmica de regra de normalização a partir do config.

---

## Tasks / Subtasks

- [ ] **Task 1: Criar eli-config.ts** [AC: 4, 5, 6]
  - [ ] Criar `/home/tikso/tikso/src/lib/ai/eli-config.ts`
  - [ ] Exportar `BARBER_NAME_ALIASES: Record<string, string[]>` com os valores atuais extraídos do prompt
  - [ ] Exportar função helper `generateBarbersAliasRule(): string` que formata os aliases como instrução legível para o LLM

- [ ] **Task 2: Refatorar buildRules() para usar eli-config.ts** [AC: 4, 5, 6]
  - [ ] Importar `generateBarbersAliasRule` em `prompt-builder.ts`
  - [ ] Substituir a string hardcoded da regra de normalização pela chamada à função
  - [ ] Verificar que o output da função é equivalente ao texto atual (sem regressão)

- [ ] **Task 3: Tornar preços de planos dinâmicos** [AC: 1, 2, 3]
  - [ ] Verificar schema da tabela Knowledge Base: `grep -n "knowledgeBase\|KnowledgeBase" /home/tikso/tikso/prisma/schema.prisma`
  - [ ] Em `buildFlows()` (ou função chamada por ela): adicionar query para buscar entrada `category: "subscription_plans"`
  - [ ] Se encontrada: usar `content` da entrada no lugar dos preços hardcoded
  - [ ] Se não encontrada: usar texto de fallback e emitir `console.warn`
  - [ ] Remover valores R$79,90, R$99,90, R$129,90 do código

- [ ] **Task 4: Testes** [AC: 7]
  - [ ] Criar arquivo `tests/unit/eli-config.test.ts`
  - [ ] Testar `generateBarbersAliasRule()` com aliases de exemplo
  - [ ] Testar `buildFlows()` com mock da KB retornando preços e com KB vazia (fallback)

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — Refatorar buildFlows e buildRules
  - `/home/tikso/tikso/src/lib/ai/eli-config.ts` — CRIAR (novo arquivo de configuração)

### Aliases atuais a migrar para eli-config.ts

Do audit (GAP-14), os aliases hardcoded no prompt são:
```
Wanderson = Vanderson
Stefane = Stephane
Nathan/Nattan = Natan
```

Estrutura proposta para `eli-config.ts`:

```typescript
// src/lib/ai/eli-config.ts

export const BARBER_NAME_ALIASES: Record<string, string[]> = {
  "Natan":      ["Nathan", "Nattan"],
  "Vanderson":  ["Wanderson"],
  "Stephane":   ["Stefane", "Stephanie"],
};

export function generateBarbersAliasRule(): string {
  const lines = Object.entries(BARBER_NAME_ALIASES).map(([canonical, aliases]) => {
    return `${aliases.join("/")}=${canonical}`;
  });
  return `Normalizacao de nomes: ${lines.join(", ")}.`;
}
```

### Estrutura de preços no prompt atual

Localizar com:
```bash
grep -n "79\|99\|129\|SMART\|FLEX\|BLACK\|plano\|assinatura" /home/tikso/tikso/src/lib/ai/prompt-builder.ts | head -30
```

### Abordagem para preços dinâmicos

```typescript
// Em buildFlows() — novo helper:
async function getSubscriptionPlansText(orgId: string): Promise<string> {
  try {
    const entry = await db.knowledgeBase.findFirst({
      where: { orgId, category: "subscription_plans" }
    });
    if (entry?.content) return entry.content;
  } catch (err) {
    console.warn("[prompt-builder] Falha ao carregar subscription_plans da KB:", err);
  }
  return "Consulte nossos planos disponíveis com a equipe da barbearia.";
}
```

**IMPORTANTE:** `buildFlows()` é chamado por `buildSystemPrompt()`. Se o buildFlows for síncrono atualmente, tornar assíncrono e ajustar todos os callers. Verificar assinatura antes de alterar:

```bash
grep -n "buildFlows\|buildSystemPrompt\|async\|await" /home/tikso/tikso/src/lib/ai/prompt-builder.ts | head -30
```

### Verificar nome da categoria na KB

A tabela `knowledgeBase` pode ter um campo `category` ou `type`. Verificar:
```bash
grep -n "category\|type\|KnowledgeBase" /home/tikso/tikso/prisma/schema.prisma
```

### Gotchas Relevantes
- Se `buildFlows()` for síncrono, torná-lo async pode exigir mudanças em cascata — verificar todos os callers
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Testar com Vitest: `npx vitest run --reporter=verbose`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-13, GAP-14) | @sm (River) |

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
| `src/lib/ai/eli-config.ts` | CREATE — BARBER_NAME_ALIASES e generateBarbersAliasRule() |
| `src/lib/ai/prompt-builder.ts` | MODIFY — usar eli-config.ts para aliases, carregar preços da KB dinamicamente |
| `tests/unit/eli-config.test.ts` | CREATE — testes para eli-config e buildFlows dinâmico |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
