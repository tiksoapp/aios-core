# Story ELI-12: MCP-to-Eli Bridge Architecture (Spike + Documentação)

**Epic:** Eli AI Agent Reliability & UX (ELI)
**Story ID:** ELI-12
**Priority:** Could Have
**Points:** 3
**Effort:** ~3 horas
**Status:** Ready for Dev
**Type:** Spike — Arquitetura + Documentação
**Sprint:** Audit Sprint - Eli Reliability
**Lead:** @dev (Dex)
**Depends On:** ELI-06, ELI-07, ELI-10, ELI-11 (contexto completo das tools implementadas)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [manual-review]
```

---

## User Story

**Como** arquiteto do sistema Tikso CRM,
**Quero** um documento de arquitetura claro sobre a separação entre MCP server e Eli tools, com um plano evolutivo documentado,
**Para que** a equipe tome decisões informadas sobre quando (e se) expor mais tools do MCP para Eli, evitando riscos de segurança e over-engineering.

---

## Acceptance Criteria

1. **AC1 — Decisão de DEFER para send_message documentada:** O documento registra formalmente a decisão de NÃO expor `send_message` do MCP para Eli neste sprint, com justificativa arquitetural: "Eli opera dentro do ciclo request-response. Mensagens proativas são responsabilidade do Pulse Agent. Expor send_message criaria risco de spam e viola o princípio de responsabilidade única."
2. **AC2 — Mapa de tools MCP vs Eli tools atualizado:** O documento contém uma tabela comparando as 7 tools do MCP server com as tools equivalentes de Eli (se houver), indicando: "em Eli", "diferente em Eli", "apenas no MCP (intencional)", "apenas no MCP (candidato a bridge futuro)".
3. **AC3 — Plano de bridge futuro documentado:** Para cada tool do MCP marcada como "candidato a bridge futuro", o documento descreve: pré-requisitos técnicos, guardrails necessários, e quando (marco do produto) faz sentido implementar.
4. **AC4 — Arquivo ARCHITECTURE.md criado:** O documento é salvo em `/home/tikso/tikso/docs/eli-mcp-architecture.md` (criar o diretório `docs/` se não existir). Conteúdo em português, formato Markdown.
5. **AC5 — Diagrama ASCII atualizado:** O documento inclui versão atualizada do diagrama ASCII do audit (`## 5. Architecture Diagram`) refletindo todas as tools adicionadas nas stories ELI-06 a ELI-11.
6. **AC6 — GAP-15 fechado no documento:** A seção sobre GAP-15 ("MCP server tools not bridged to Eli") é explicitamente fechada com status: tools que foram bridged, tools que foram explicitamente DEFER'd, e próximos passos.

---

## Tasks / Subtasks

- [ ] **Task 1: Levantar estado atual após ELI-06 a ELI-11** [AC: 2, 5]
  - [ ] Listar todas as tools de Eli após as implementações das stories anteriores
  - [ ] Listar as 7 tools do MCP server: `grep -n "name:\|tool_name" /home/tikso/tikso/src/lib/mcp/server.ts`
  - [ ] Criar tabela de comparação MCP vs Eli

- [ ] **Task 2: Documentar decisão de DEFER — send_message** [AC: 1]
  - [ ] Escrever seção formal com: decisão, justificativa, data, alternativa (Pulse Agent), revisão em qual marco do produto

- [ ] **Task 3: Documentar plano de bridge futuro** [AC: 3]
  - [ ] Para cada candidato (get_analytics, list_contacts): descrever pré-requisitos e quando fazer
  - [ ] Para trigger_flow: já foi bridged em ELI-10 (documentar como concluído)

- [ ] **Task 4: Criar eli-mcp-architecture.md no servidor** [AC: 4, 5, 6]
  - [ ] Criar `/home/tikso/tikso/docs/` se não existir
  - [ ] Criar `/home/tikso/tikso/docs/eli-mcp-architecture.md` com todo o conteúdo
  - [ ] Diagrama ASCII atualizado com todas as tools novas

- [ ] **Task 5: Sem testes** — Este é um spike de documentação. Nenhum teste automatizado necessário.
  - [ ] QA faz revisão manual do documento (clareza, completude, precisão técnica)

---

## Dev Notes

### Stack e Contexto
- **Este é um spike de documentação e arquitetura — não há código de produção a implementar**
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **Arquivos de referência:**
  - `/home/tikso/tikso/src/lib/mcp/server.ts` — 7 tools do MCP
  - `/home/tikso/tikso/src/lib/ai/aria-tools.ts` — Tools de Eli (estado final após ELI-06 a ELI-11)
  - Audit original: `/root/aios-core/docs/research/eli-tools-audit.md`

### MCP Server — 7 Tools existentes (do audit)

```
MCP server (src/lib/mcp/server.ts) expõe:
1. list_contacts     — Listar contatos da org
2. send_message      — Enviar mensagem WhatsApp (proativa)  [DEFER]
3. get_conversation  — Buscar histórico de conversa
4. move_pipeline     — Mover contato de stage (duplicata de move_pipeline_stage de Eli)
5. add_tag           — Adicionar tag (duplicata da core tool de Eli)
6. trigger_flow      — Disparar automação  [bridged em ELI-10]
7. get_analytics     — Métricas da org
```

### Tabela comparativa para o documento

| MCP Tool | Eli Tool | Status |
|----------|----------|--------|
| `list_contacts` | Não tem equivalente | Candidato futuro (com filtros e paginação) |
| `send_message` | Não tem equivalente | DEFER — intencional (Pulse é responsável) |
| `get_conversation` | Não tem equivalente | Baixa prioridade (histórico já está no contexto) |
| `move_pipeline` | `move_pipeline_stage` | Em Eli (diferente: Eli usa nome, MCP usa ID) |
| `add_tag` | `add_tag` + `remove_tag` (ELI-06) | Em Eli (mais completo) |
| `trigger_flow` | `trigger_flow` (ELI-10) | Bridged com whitelist de segurança |
| `get_analytics` | Não tem equivalente | Fora de escopo para Eli (dado para dashboards) |

### Diagrama ASCII atualizado (base para o documento)

```
+-------------------------------------------+
|         Eli (AutonomousAgent)             |
|  LLM Tool Calling Loop (max 5 iter)      |
|                                           |
|  CORE TOOLS (aria-tools.ts):             |
|  get_contact_info    search_kb            |
|  add_tag             remove_tag (ELI-06)  |
|  move_pipeline_stage update_contact (06)  |
|  add_internal_note   list_pipeline (06)   |
|  transfer_to_human   schedule_followup (07) |
|  get_business_hours (08)                  |
|  trigger_flow (10)   send_media (10)      |
|  schedule_reminder (11)                   |
|                                           |
|  BB INTEGRATION TOOLS (tools.ts):        |
|  get_services        check_availability   |
|  get_subscriber      get_history          |
|  create_appointment  cancel_appointment   |
|  reschedule_appt     get_barbers (11)     |
+-------------------------------------------+
          |
          | (separação intencional)
          v
+-------------------------------------------+
|         MCP Server (Clientes Externos)    |
|  Ferramentas para integrações externas:   |
|  - list_contacts (futuro bridge)          |
|  - send_message  [DEFER — Pulse faz]      |
|  - get_conversation                       |
|  - move_pipeline (duplicata, OK)          |
|  - add_tag (duplicata, OK)                |
|  - trigger_flow [bridged com whitelist]   |
|  - get_analytics [dashboards, não Eli]    |
+-------------------------------------------+
          |
          v
+-------------------------------------------+
|         Pulse Agent (BullMQ Cron)        |
|  Mensagens proativas:                     |
|  - Follow-ups (T+30min/24h/72h)          |
|  - Reativação de contatos inativos       |
|  - Lembretes de compromisso (ELI-11)     |
|  - Jobs agendados por Eli (ELI-07)       |
+-------------------------------------------+
```

### Princípio arquitetural a documentar

> Eli responde, não inicia. Mensagens proativas pertencem ao Pulse Agent.
> O MCP expõe capacidades para integrações externas (n8n, webhooks, etc.).
> Eli é uma camada de inteligência conversacional — não uma plataforma de outbound.

### Gotchas Relevantes
- Este spike depende das stories ELI-06 a ELI-11 estarem completas para o diagrama ser preciso
- Se executado antes, usar o estado planejado (não o atual) e marcar o documento como "estado pós-ELI-06..11"
- Criar o diretório `/home/tikso/tikso/docs/` se não existir: `mkdir -p /home/tikso/tikso/docs/`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do audit de tools da Eli (GAP-02, GAP-15) | @sm (River) |

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
| `/home/tikso/tikso/docs/eli-mcp-architecture.md` | CREATE — documento de arquitetura MCP vs Eli tools |
| `src/lib/mcp/server.ts` | READ-ONLY — inventário das 7 tools MCP |
| `src/lib/ai/aria-tools.ts` | READ-ONLY — inventário das tools de Eli (estado final) |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
