# Story ELI-03: Error Classification e Sanitização de Respostas

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-03
**Priority:** High
**Points:** 3
**Effort:** ~3 horas
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
quality_gate_tools: [unit-test, manual-review]
```

---

## User Story

**Como** cliente da barbearia usando WhatsApp,
**Quero** que a IA nunca me mostre códigos de erro, IDs internos ou jargão técnico,
**Para que** eu tenha uma experiência natural e não perceba que estou falando com um sistema.

---

## Acceptance Criteria

1. **AC1 — Tool errors user-friendly:** Todas as mensagens de erro retornadas pelas tools BestBarbers são reescritas para linguagem amigável. Nenhuma contém "HTTP", "ID", "service_id", "status code", ou referências técnicas.
2. **AC2 — Wrapper de erro no LLM context:** Antes de adicionar resultado de tool com erro ao `messages[]`, envolver em contexto: `"[INTERNO - NAO COMPARTILHAR COM CLIENTE] Erro: {erro_tecnico}. Responda ao cliente dizendo apenas: {mensagem_amigavel}"`
3. **AC3 — Regra explícita no prompt:** Adicionar regra no `buildRules`: "NUNCA compartilhe detalhes técnicos (HTTP, ID, erro de sistema, nomes de ferramentas) com o cliente. Se uma ferramenta falhar, diga apenas que está tendo dificuldade e tente novamente."
4. **AC4 — sanitizeResponse melhorado:** `sanitizeResponse()` em `autonomous-agent.ts` detecta e remove padrões técnicos em texto plain: `ID \d+`, `HTTP \d{3}`, `service_id`, `error code`, `API`, `timeout`.
5. **AC5 — Testes:** Mínimo 5 testes: tool error reescrito, wrapper de contexto aplicado, sanitizer remove "ID 456", sanitizer remove "HTTP 400", prompt contém regra anti-jargão.

---

## Tasks / Subtasks

- [ ] **Task 1: Reescrever mensagens de erro das tools** [AC: 1]
  - [ ] Em `tool-implementations.ts`: reescrever todos os `return { error: ... }` para linguagem amigável
  - [ ] Linha 687: `"Nao foi possivel criar o agendamento (HTTP ${res.status})"` → `"Nao consegui concluir o agendamento. Vou tentar de novo."`
  - [ ] Linha 583: `"Servico com ID ${serviceId} nao encontrado"` → `"Nao encontrei esse servico. Pode me dizer o nome do servico que voce quer?"`
  - [ ] Auditar todas as outras mensagens de erro no arquivo

- [ ] **Task 2: Wrapper de contexto para erros** [AC: 2]
  - [ ] Em `autonomous-agent.ts`, no tool loop: quando tool retorna `{ error }`, envolver antes de adicionar ao messages[]
  - [ ] Template: `"[INTERNO] {erro_original}. Acao: {retry|handoff|pedir_info}. Responda ao cliente de forma amigavel sem detalhes tecnicos."`

- [ ] **Task 3: Regra no prompt** [AC: 3]
  - [ ] Em `prompt-builder.ts` `buildRules()`: adicionar regra explícita proibindo jargão técnico
  - [ ] Posição: logo após regra 7 (que trata de erros)

- [ ] **Task 4: Melhorar sanitizeResponse** [AC: 4]
  - [ ] Em `autonomous-agent.ts` `sanitizeResponse()` (linhas 579-634): adicionar regex patterns para texto plain
  - [ ] Patterns: `/ID\s*\d+/gi`, `/HTTP\s*\d{3}/gi`, `/service_id/gi`, `/error\s*code/gi`, `/API\s/gi`, `/timeout/gi`
  - [ ] Substituir matches por string vazia ou equivalente amigável

- [ ] **Task 5: Testes** [AC: 5]
  - [ ] Testes unitários para cada mensagem de erro reescrita
  - [ ] Teste do sanitizer com strings contendo jargão
  - [ ] Teste do wrapper de contexto

---

## Dev Notes

### Stack e Contexto
- **Arquivos principais:**
  - `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tool-implementations.ts` — Mensagens de erro (linhas 583, 687, e outras)
  - `/home/tikso/tikso/src/lib/ai/autonomous-agent.ts` — `sanitizeResponse()` (linhas 579-634), tool loop (~430)
  - `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` — `buildRules()` regra 7

### Evidência do Audit
Na conversa com Kelmer Palma, a IA enviou: "sistema não está reconhecendo o ID do serviço 'Corte + Barba' corretamente. Vou tentar novamente com um ID diferente." Isso é uma **alucinação do LLM** baseada no erro genérico da tool. O LLM recebeu `"HTTP 400"` e inventou uma explicação técnica.

### Inventário de Erros a Reescrever
Auditar todas as ocorrências de `return { error:` em `tool-implementations.ts`. Cada uma deve ser reescrita para linguagem de barbearia casual.

### Gotchas Relevantes
- O sanitizer atual (linhas 579-634) foca em JSON, XML, code blocks — não pega texto plain
- A regra 7 do prompt diz "tente novamente 1x, depois transfer_to_human" mas não proíbe expor detalhes técnicos
- Cuidado para não sanitizar mensagens legítimas que contenham números (ex: "horário às 16:00")

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-24 | 1.0 | Story criada a partir do audit Dev (Bug #4) e Architect (Falha #4) | @sm (River) |

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
| `src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | MODIFY — reescrever mensagens de erro |
| `src/lib/ai/autonomous-agent.ts` | MODIFY — wrapper de contexto + melhorar sanitizeResponse |
| `src/lib/ai/prompt-builder.ts` | MODIFY — adicionar regra anti-jargão |
| `tests/unit/error-sanitization.test.ts` | CREATE — testes de sanitização |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
