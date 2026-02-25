# Story ELI-02: Circuit Breaker com Auto-Handoff

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-02
**Priority:** High
**Points:** 5
**Effort:** ~4 horas
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
quality_gate_tools: [unit-test, manual-review]
```

---

## User Story

**Como** cliente da barbearia usando WhatsApp,
**Quero** que quando a IA não conseguir resolver meu problema, um humano seja acionado automaticamente,
**Para que** eu não fique preso num loop de erros sem solução.

---

## Acceptance Criteria

1. **AC1 — Contagem de falhas:** O `AutonomousAgent` mantém um contador de tool failures por conversa (in-memory Map). Cada tool que retorna `{ error: ... }` incrementa o contador. Um sucesso reseta o contador.
2. **AC2 — Threshold de handoff:** Quando o contador atinge 3 falhas consecutivas de tool, o sistema força handoff automático via `transfer_to_human` — sem depender do LLM decidir.
3. **AC3 — Mesma tool falhando:** Se a mesma tool falha 2x consecutivas, o sistema para de chamar essa tool e informa limitação ao LLM no contexto.
4. **AC4 — Mensagem padronizada:** A mensagem enviada ao cliente no handoff automático é: "Estou com dificuldade para concluir essa ação no momento. Vou encaminhar para nossa equipe te ajudar diretamente!" (configurável via AgentConfig).
5. **AC5 — Alerta para staff:** No handoff automático, uma nota interna é criada com contexto completo: nome do cliente, serviço solicitado, horário desejado, barbeiro, número de tentativas, e erro interno (só para staff).
6. **AC6 — Testes:** Mínimo 5 testes: 3 falhas → handoff, 2 falhas mesma tool → stop, sucesso reseta contador, handoff envia mensagem correta, alerta interno contém contexto.

---

## Tasks / Subtasks

- [ ] **Task 1: Implementar CircuitBreaker** [AC: 1, 2, 3]
  - [ ] Criar lógica de circuit breaker dentro de `autonomous-agent.ts` (não precisa de arquivo separado)
  - [ ] `Map<string, { toolFailures: number, sameToolFailures: Map<string, number>, lastSuccess: Date }>`
  - [ ] No tool loop (~linha 430): após cada `executeToolCall`, verificar se resultado contém `error`
  - [ ] Se `toolFailures >= 3`: sair do loop, retornar decisão de handoff
  - [ ] Se `sameToolFailures.get(toolName) >= 2`: marcar tool como bloqueada nesta sessão

- [ ] **Task 2: Handoff automático** [AC: 4, 5]
  - [ ] Quando circuit breaker dispara: chamar `transfer_to_human` programaticamente (não via LLM)
  - [ ] Enviar mensagem padronizada ao cliente (AC4)
  - [ ] Criar nota interna via `add_internal_note` com contexto da falha (AC5)
  - [ ] Mensagem configurável via campo `fallbackMessage` no AgentConfig (com default hardcoded)

- [ ] **Task 3: Integração com guardrails existentes** [AC: 1]
  - [ ] Circuit breaker complementa (não substitui) `checkGuardrails`
  - [ ] Garantir que o post-response pipeline (CHAIN-1) NÃO é acionado em handoff por falha

- [ ] **Task 4: Testes** [AC: 6]
  - [ ] Mock de `executeToolCall` retornando erros consecutivos
  - [ ] Verificar que handoff é chamado após threshold
  - [ ] Verificar que sucesso reseta contadores
  - [ ] Verificar conteúdo da nota interna

---

## Dev Notes

### Stack e Contexto
- **Arquivo principal:** `/home/tikso/tikso/src/lib/ai/autonomous-agent.ts`
- **Tool loop:** Linhas ~420-460, `MAX_TOOL_ITERATIONS = 5`
- **Guardrails existentes:** `checkGuardrails()` — verifica human assigned, forbidden topic, max messages, hot lead, business hours
- **Core tools:** `transfer_to_human` e `add_internal_note` em `aria-tools.ts`

### Design Decision
**In-memory Map é suficiente.** O estado é efêmero por conversa. Se PM2 reiniciar, contadores zeram — aceitável porque restart resolve maioria dos problemas transientes.

### Padrão de Estados do Circuit Breaker
```
CLOSED (normal) ──(3 failures)──> OPEN (handoff)
```
Não precisa de HALF_OPEN para v1. Simplificar: contador + threshold + reset on success.

### Gotchas Relevantes
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- O `transfer_to_human` já existe como core tool — reusar a implementação existente
- Post-response pipeline (agent-pipeline.ts) não deve rodar quando circuit breaker dispara

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-24 | 1.0 | Story criada a partir do audit arquitetural (Falha #5) e análise do Analyst (RICE #2) | @sm (River) |

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
| `src/lib/ai/autonomous-agent.ts` | MODIFY — adicionar circuit breaker no tool loop + handoff automático |
| `tests/unit/circuit-breaker.test.ts` | CREATE — testes do circuit breaker |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
