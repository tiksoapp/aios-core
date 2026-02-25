# Story ELI-10: Trigger Flow + Send Media Tools

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-10
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
**Quero** poder disparar automações pré-aprovadas e enviar mídia (imagens, documentos) durante uma conversa,
**Para que** eu possa executar fluxos de onboarding/reativação e compartilhar materiais visuais com o cliente.

---

## Acceptance Criteria

1. **AC1 — Tool trigger_flow disponível para Eli:** A tool `trigger_flow` está registrada em `CORE_TOOL_DEFINITIONS` de `aria-tools.ts` e acessível no loop de tool-calling de Eli.
2. **AC2 — Whitelist de flows:** A tool aceita `flow_id: string` e `reason?: string`. Antes de executar, valida que `flow_id` está na lista de flows permitidos definida em `eli-config.ts` (constante `ALLOWED_FLOW_IDS: string[]`). Se não estiver na whitelist, retorna `{ error: "Flow nao autorizado. Flows permitidos: [lista]" }`.
3. **AC3 — Execução de trigger_flow:** Para flows autorizados, chama a API de automação (Evolution API ou chamada interna equivalente ao que o MCP server faz em `src/lib/mcp/server.ts`). Retorna `{ success: true, flow_id, triggered_at, message: "Flow disparado com sucesso." }`.
4. **AC4 — Prompt instrui uso de trigger_flow:** Em `buildFlows()`, adicionar seção "AUTOMACOES": listar os flows permitidos por nome/ID com a descrição do momento certo para usá-los (ex: "flow_onboarding — use quando cliente nunca agendou antes").
5. **AC5 — Tool send_media disponível para Eli:** A tool `send_media` está registrada em `CORE_TOOL_DEFINITIONS` e acessível no loop de tool-calling de Eli.
6. **AC6 — Parâmetros de send_media:** A tool aceita `media_url: string` (URL da mídia, obrigatório), `media_type: "image" | "document" | "audio"` (obrigatório), e `caption?: string` (legenda opcional para imagens/documentos).
7. **AC7 — Execução de send_media:** Chama a Evolution API para envio de mídia para o `phone` do contato atual (disponível no contexto). Retorna `{ success: true, media_type, message: "Midia enviada." }`.
8. **AC8 — Validação de URL em send_media:** Se `media_url` não iniciar com `https://`, retorna `{ error: "media_url deve ser HTTPS." }`.
9. **AC9 — Whitelist de domínios para send_media:** `media_url` deve pertencer a domínios pré-aprovados definidos em `eli-config.ts` (constante `ALLOWED_MEDIA_DOMAINS: string[]`). Domínios sugeridos: o próprio domínio do tikso, S3/CDN próprio. Se domínio não autorizado: `{ error: "Dominio nao autorizado para envio de midia." }`.
10. **AC10 — Testes:** Mínimo 8 testes: trigger_flow com flow autorizado (sucesso), flow não autorizado (erro), send_media com URL HTTPS válida, URL HTTP (erro), domínio não autorizado (erro), tipos de mídia válidos (image, document, audio).

---

## Tasks / Subtasks

- [ ] **Task 1: Adicionar ALLOWED_FLOW_IDS e ALLOWED_MEDIA_DOMAINS em eli-config.ts** [AC: 2, 9]
  - [ ] Se `eli-config.ts` já existe (ELI-09), adicionar nele; caso contrário, criar
  - [ ] Exportar `ALLOWED_FLOW_IDS: string[]` — inicialmente vazio `[]` (dev deve preencher com IDs reais do ambiente)
  - [ ] Exportar `ALLOWED_MEDIA_DOMAINS: string[]` — ex: `["tikso.com.br", "cdn.tikso.com.br"]`
  - [ ] Adicionar comentário: `// Preencher com IDs reais antes de ativar em produção`

- [ ] **Task 2: Implementar trigger_flow** [AC: 1, 2, 3]
  - [ ] Adicionar definição em `CORE_TOOL_DEFINITIONS`
  - [ ] Schema: `flow_id` (string, required), `reason` (string, opcional)
  - [ ] Verificar `ALLOWED_FLOW_IDS` antes de executar
  - [ ] Verificar como o MCP server executa flows: `grep -n "trigger_flow\|triggerFlow" /home/tikso/tikso/src/lib/mcp/server.ts`
  - [ ] Reutilizar a mesma implementação (extrair função compartilhada ou chamar diretamente)
  - [ ] Registrar em `executeToolCall()`

- [ ] **Task 3: Implementar send_media** [AC: 5, 6, 7, 8, 9]
  - [ ] Adicionar definição em `CORE_TOOL_DEFINITIONS`
  - [ ] Schema: `media_url` (string, required), `media_type` (enum, required), `caption` (string, opcional)
  - [ ] Validar `https://` prefix e domínio contra `ALLOWED_MEDIA_DOMAINS`
  - [ ] Verificar como Evolution API recebe envio de mídia — padrão usual: `POST /message/sendMedia/{instance}` com `{ number, mediatype, mimetype, media, caption }`
  - [ ] Registrar em `executeToolCall()`

- [ ] **Task 4: Atualizar prompt** [AC: 4]
  - [ ] Em `buildFlows()` de `prompt-builder.ts`: adicionar seção "AUTOMACOES" com instrução de uso de `trigger_flow`
  - [ ] Instrução para `send_media`: "Para compartilhar materiais (cardápio de preços, localização em imagem): use send_media com media_url do CDN."

- [ ] **Task 5: Testes** [AC: 10]
  - [ ] Criar `tests/unit/eli-trigger-send-media.test.ts`
  - [ ] Mock da Evolution API (HTTP client)
  - [ ] Cobrir todos os cenários do AC10

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Evolution API v2.3.7, Vitest
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/ai/aria-tools.ts` — Tools a adicionar
  - `/home/tikso/tikso/src/lib/mcp/server.ts` — Referência de implementação de trigger_flow
  - `/home/tikso/tikso/src/lib/ai/eli-config.ts` — Adicionar ALLOWED_FLOW_IDS, ALLOWED_MEDIA_DOMAINS
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — Seção AUTOMACOES

### Como o MCP server implementa trigger_flow

```bash
# Verificar implementação atual:
grep -n "trigger_flow\|triggerFlow\|flow" /home/tikso/tikso/src/lib/mcp/server.ts | head -30
```

A ideia é reutilizar a mesma lógica de chamada de API. Se o MCP usa uma função interna, extrair para um arquivo compartilhado (ex: `src/lib/ai/automation-helpers.ts`).

### Padrão Evolution API para envio de mídia

```typescript
// Padrão usual Evolution API v2:
const evolutionApiUrl = process.env.EVOLUTION_API_URL;
const evolutionApiKey = process.env.EVOLUTION_API_KEY;

// POST /message/sendMedia/{instanceName}
const response = await fetch(`${evolutionApiUrl}/message/sendMedia/${instanceName}`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "apikey": evolutionApiKey
  },
  body: JSON.stringify({
    number: context.phone,
    mediatype: media_type,  // "image" | "document" | "audio"
    media: media_url,       // URL da mídia
    caption: caption ?? ""
  })
});
```

Verificar a implementação existente de envio de mensagem no projeto para confirmar padrão:
```bash
grep -rn "sendMedia\|sendMessage\|EVOLUTION" /home/tikso/tikso/src/lib/ | grep -v ".test." | head -20
```

### Whitelist de flows (IMPORTANTE)

Os `ALLOWED_FLOW_IDS` devem ser preenchidos com IDs reais ANTES de ir para produção. Em dev, pode-se deixar a lista vazia (toda chamada retorna erro "não autorizado") para não disparar flows acidentalmente.

```typescript
// eli-config.ts (adição)
export const ALLOWED_FLOW_IDS: string[] = [
  // Preencher com IDs reais antes de ativar em produção
  // Ex: "flow_onboarding_v1", "flow_reativacao_90d"
];

export const ALLOWED_MEDIA_DOMAINS: string[] = [
  "tikso.com.br",
  "cdn.tikso.com.br",
  // Adicionar CDN/S3 quando configurado
];
```

### Segurança — trigger_flow

O audit (GAP-06) alerta: "alto risco: LLM poderia disparar flows caros/disruptivos." A whitelist é o guardrail principal. O prompt deve instruir Eli a usar `trigger_flow` SOMENTE em contextos específicos e NUNCA de forma especulativa.

### Gotchas Relevantes
- Evolution API v2.3.7 (patched) — verificar padrão exato de envio de mídia no código existente
- Nunca usar `sed -i` com regex global em .ts — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Variáveis de ambiente: `EVOLUTION_API_URL`, `EVOLUTION_API_KEY` — verificar `.env`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-06, GAP-08) | @sm (River) |

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
| `src/lib/ai/aria-tools.ts` | MODIFY — adicionar trigger_flow e send_media em CORE_TOOL_DEFINITIONS e executeToolCall() |
| `src/lib/ai/eli-config.ts` | MODIFY (ou CREATE se ELI-09 não executado antes) — adicionar ALLOWED_FLOW_IDS, ALLOWED_MEDIA_DOMAINS |
| `src/lib/ai/prompt-builder.ts` | MODIFY — seção AUTOMACOES em buildFlows() |
| `src/lib/mcp/server.ts` | READ-ONLY — referência para implementação de trigger_flow |
| `tests/unit/eli-trigger-send-media.test.ts` | CREATE — testes unitários |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
