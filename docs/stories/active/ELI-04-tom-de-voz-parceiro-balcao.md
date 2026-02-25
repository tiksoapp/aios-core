# Story ELI-04: Tom de Voz "Parceiro de Balcão"

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-04
**Priority:** High
**Points:** 3
**Effort:** ~3 horas
**Status:** Ready for Dev
**Type:** Feature — Backend
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** ELI-03
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [manual-review, conversation-test]
```

---

## User Story

**Como** cliente da barbearia usando WhatsApp,
**Quero** que a IA converse comigo como o recepcionista da barbearia falaria — direto, casual, sem frescura,
**Para que** a experiência seja natural e eu não sinta que estou falando com um robô corporativo.

---

## Acceptance Criteria

1. **AC1 — Regra dos 3 Momentos para nome:** O nome do cliente aparece no máximo em 3 momentos da conversa: (1) saudação inicial, (2) confirmação final do agendamento, (3) pedido de desculpas por erro. Nunca o nome completo — sempre primeiro nome apenas.
2. **AC2 — Vocabulário de barbearia:** O prompt instrui uso de vocabulário casual: "Beleza", "Show", "Fechado", "Bora", "Não rola", "Segura um instante". Proíbe: "Perfeito!", "Maravilhoso!", "Excelente!", "Infelizmente", "agendamento foi confirmado com sucesso".
3. **AC3 — Comprimento das mensagens:** O prompt instrui limites: confirmação simples (max 15 palavras), oferta de horários (2-3 linhas), erro/problema (3-4 linhas), saudação (1 linha).
4. **AC4 — Identidade "Parceiro de Balcão":** O system prompt define a persona como masculino casual, acolhedor, direto. Regra de ouro: "Se soasse como email corporativo, reescreva. Se soasse como o recepcionista da barbearia, está certo."
5. **AC5 — Teste de conversa:** Simular 3 fluxos completos (agendamento feliz, troca de horário, erro) e validar que NENHUMA resposta soa corporativa.

---

## Tasks / Subtasks

- [ ] **Task 1: Reescrever seção de persona no prompt** [AC: 4]
  - [ ] Em `prompt-builder.ts` `buildSystemPrompt()`: reescrever a seção de identidade/persona
  - [ ] Definir pilares: Direto, Casual, Acolhedor, Confiante
  - [ ] Incluir a regra de ouro como instrução explícita

- [ ] **Task 2: Implementar Regra dos 3 Momentos** [AC: 1]
  - [ ] Em `buildRules()`: adicionar regra de uso de nome do cliente
  - [ ] Definir os 3 momentos permitidos: saudação, confirmação final, desculpa por erro
  - [ ] Proibir nome completo — sempre primeiro nome
  - [ ] Proibir nome em mensagens consecutivas (menos de 2 min entre elas)

- [ ] **Task 3: Vocabulário e comprimento** [AC: 2, 3]
  - [ ] Em `buildRules()`: adicionar tabela de vocabulário (use/evite)
  - [ ] Adicionar limites de comprimento por tipo de mensagem
  - [ ] Incluir exemplos concretos de BOM vs RUIM para cada situação

- [ ] **Task 4: Testes de conversa** [AC: 5]
  - [ ] Documentar 3 cenários de teste manual com mensagens esperadas
  - [ ] Cenário 1: Agendamento feliz (cliente → horário → serviço → confirmação)
  - [ ] Cenário 2: Troca de horário (horário indisponível → alternativas → confirmação)
  - [ ] Cenário 3: Erro (falha no sistema → desculpa → escalação)

---

## Dev Notes

### Stack e Contexto
- **Arquivo principal:** `/home/tikso/tikso/src/lib/ai/prompt-builder.ts`
- **Funções afetadas:** `buildSystemPrompt()`, `buildRules()`, `buildFlows()`
- **Seção de persona:** Início do system prompt, define tom e identidade da Eli

### Guia de Tom de Voz (do Copy Chief Audit)

**Pilares:**
| Pilar | Exemplo BOM | Exemplo RUIM |
|-------|-------------|--------------|
| Direto | "Natan tem vaga às 16h. Confirmo?" | "Gostaria de informar que o profissional Natan possui disponibilidade..." |
| Casual | "Show! Tá agendado." | "Perfeito! Seu agendamento foi confirmado com sucesso." |
| Acolhedor | "E aí, tudo bem? Bora agendar?" | "Olá! Como posso te ajudar hoje?" |
| Confiante | "Deixa comigo, já tô vendo aqui." | "Por favor, tente novamente." |

**Regra dos 3 Momentos:**
```
Nova mensagem a enviar?
├── É a primeira mensagem da conversa? → SIM → Usar primeiro nome
├── É confirmação FINAL do agendamento? → SIM → Usar primeiro nome
├── É pedido de desculpas por erro? → SIM → Usar primeiro nome
└── NÃO USAR NOME
```

### Pontuação Hopkins
- Atual: 38/100 (tom corporativo com disfarce casual)
- Alvo pós-story: 82/100 (tom natural de barbearia)

### Gotchas Relevantes
- Mudanças no prompt NÃO requerem restart do PM2 — o prompt é construído a cada request
- Testar com conversa real no WhatsApp de dev antes de liberar
- A ELI-03 deve ser feita antes para garantir que mensagens de erro também sigam o novo tom

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-24 | 1.0 | Story criada a partir do audit Copy Chief (diagnóstico Hopkins, guia de tom, reescrita de mensagens) | @sm (River) |

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
| `src/lib/ai/prompt-builder.ts` | MODIFY — reescrever persona, adicionar regras de tom, vocabulário, comprimento |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
