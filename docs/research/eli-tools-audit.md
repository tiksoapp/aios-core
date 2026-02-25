# Eli Tools Audit -- Complete Analysis

**Date:** 2026-02-25
**Auditor:** Aria (Architect Agent)
**Scope:** All tools available to Eli (ARIA autonomous agent) in Tikso CRM
**Server:** Vultr (`ssh vultr`), project at `/home/tikso/tikso/`

---

## 1. Tool Inventory

### 1.1 Core Tools (always available, defined in `aria-tools.ts`)

| # | Tool Name | Parameters | Required Params | Returns (success) | Returns (error) |
|---|-----------|-----------|-----------------|-------------------|-----------------|
| 1 | `get_contact_info` | (none) | (none) | `{ id, name, phone, email, tags[], pipeline_stages[] }` | `{ error }` |
| 2 | `add_tag` | `tag_name: string` | `tag_name` | `{ success, message, already_existed? }` | `{ error }` |
| 3 | `move_pipeline_stage` | `stage_name: string` | `stage_name` | `{ success, message, action: "updated"\|"created" }` | `{ error }` with available stages |
| 4 | `add_internal_note` | `content: string` | `content` | `{ success, message }` | `{ error }` |
| 5 | `transfer_to_human` | `reason: string` | `reason` | `{ success, assigned_to, reason, message }` | `{ error }` |
| 6 | `search_knowledge_base` | `query: string` | `query` | `{ results[{ title, content, category }], count }` | `{ error }` |

### 1.2 BestBarbers Integration Tools (loaded dynamically per org, defined in `tools.ts`)

| # | Tool Name | Parameters | Required Params | Returns (success) | Returns (error) |
|---|-----------|-----------|-----------------|-------------------|-----------------|
| 7 | `get_services` | (none) | (none) | `{ services[{ id, name, price, duration_minutes, duration_display }], barbers[{ name, restrictions }], total_services, total_barbers }` | `{ error }` |
| 8 | `check_availability` | `date: string`, `barber_name?: string`, `service_name?: string`, `duration_minutes?: number` | `date` | `{ date, duration_minutes, available, total_free_slots, results[{ barber, available_slots[] }] }` | `{ error, _internal? }` |
| 9 | `get_subscriber_status` | `phone?: string` | (none -- uses contact phone if omitted) | `{ found, client_name, phone, is_subscriber, active_plans?, active_count?, due_date?, message }` | `{ error, _internal? }` |
| 10 | `get_appointment_history` | (none) | (none) | `{ found, client_name, total_visits, upcoming_count, upcoming[], preferred_barber, last_5[], message }` | `{ error, _internal? }` |
| 11 | `create_appointment` | `barber_name: string`, `date: string`, `start_hour: string`, `service_name?: string`, `service_id?: number` | `barber_name`, `date`, `start_hour` | `{ success, appointment_id, barber, date, start_hour, finish_hour, service, type, is_subscriber, plan_name, message }` | `{ error, _internal? }` |
| 12 | `cancel_appointment` | `appointment_id?: number` | (none -- auto-resolves next upcoming if omitted) | `{ success, appointment_id, message }` | `{ error, _internal? }` |
| 13 | `reschedule_appointment` | `new_date: string`, `new_start_hour: string`, `barber_name?: string`, `service_id?: number`, `appointment_id?: number` | `new_date`, `new_start_hour` | `{ success, old_appointment_cancelled, new_appointment{}, message }` | `{ error, _internal?, available_slots? }` |

**Total: 13 tools (6 core + 7 BestBarbers integration)**

---

## 2. Tool Loading and Execution Architecture

### 2.1 Registration Flow

```
autonomous-agent.ts
  |
  +--> getToolsForOrg(orgId)  [aria-tools.ts]
        |
        +--> CORE_TOOL_DEFINITIONS (6 tools, always included)
        |
        +--> db.integration.findMany({isActive: true})
              |
              +--> type="bestbarbers" --> BB_TOOL_DEFINITIONS (7 tools)
              |
              +--> (future: listenplay, nexaas -- commented placeholder)
```

### 2.2 Execution Flow

```
AutonomousAgent.generateResponse()
  |
  +--> callLLM() with tools=[...toolDefs]
  |
  +--> Tool loop (max 5 iterations)
        |
        +--> Circuit Breaker filter (blocked tools removed)
        |
        +--> executeToolCall() [aria-tools.ts]
              |
              +--> Core tools: inline implementation
              +--> BB tools: executeBBToolWithConfig() --> executeBBTool() [tools.ts]
        |
        +--> Circuit Breaker tracking (failure counters)
        |
        +--> ELI-03 error wrapping (_internal stripped, _context added)
```

### 2.3 Safety Mechanisms

| Mechanism | Source | Behavior |
|-----------|--------|----------|
| **MAX_TOOL_ITERATIONS** | `autonomous-agent.ts` | Hard limit of 5 tool-calling rounds per response |
| **Circuit Breaker (global)** | `autonomous-agent.ts` (ELI-02) | After 3 consecutive global failures, force handoff to human |
| **Circuit Breaker (per-tool)** | `autonomous-agent.ts` (ELI-02) | After 2 consecutive failures of same tool, block it for the session |
| **Error sanitization** | `autonomous-agent.ts` (ELI-03) | `_internal` field stripped, `_context` guidance injected |
| **Response sanitization** | `autonomous-agent.ts` | 14-pass regex cleaning of leaked tool calls, JSON, code blocks, technical identifiers |
| **LLM timeout** | `autonomous-agent.ts` | 30s per LLM call, 2 attempts max |
| **Appointment ID validation** | `tool-implementations.ts` | INT4 range check (1 to 2,147,483,647) |

---

## 3. Prompt-to-Tool Coverage Matrix

This matrix maps every tool reference in the prompt-builder (`/home/tikso/tikso/src/lib/ai/prompt-builder.ts`) to actual tool implementations.

| Prompt Instruction | Tool Referenced | Tool Exists | Accessible to LLM | Status |
|-------------------|----------------|-------------|-------------------|--------|
| "Chame get_appointment_history" (verify booking) | `get_appointment_history` | YES | YES | OK |
| "Chame get_subscriber_status" (start of booking flow) | `get_subscriber_status` | YES | YES | OK |
| "check_availability com service_name" | `check_availability` | YES | YES | OK |
| "NAO precisa chamar get_services antes de check_availability" | `get_services` | YES | YES | OK |
| "create_appointment com barber_name, date, start_hour e service_name" | `create_appointment` | YES | YES | OK |
| "Se falhar 2x: transfer_to_human" | `transfer_to_human` | YES | YES | OK |
| "get_appointment_history -> confirme -> cancel_appointment" | `cancel_appointment` | YES | YES | OK |
| "Use SEMPRE reschedule_appointment" | `reschedule_appointment` | YES | YES | OK |
| "add_internal_note" (subscription cancellation retention) | `add_internal_note` | YES | YES | OK |
| "Chame get_services" (services/prices/professionals) | `get_services` | YES | YES | OK |
| "Chame transfer_to_human" (explicit human request) | `transfer_to_human` | YES | YES | OK |
| "SEMPRE chame get_services" (rule 18) | `get_services` | YES | YES | OK |
| "get_subscriber_status: Se assinante..." (rule 20) | `get_subscriber_status` | YES | YES | OK |
| Follow-up logic (T+30min, T+24h, T+72h) | **NO TOOL** | N/A | N/A | **GAP** |
| "Use a base de conhecimento" (general info) | `search_knowledge_base` | YES | YES | OK (implicit) |

---

## 4. GAP Analysis

### 4.1 CRITICAL Gaps

| ID | Gap | Severity | Description | Impact |
|----|-----|----------|-------------|--------|
| GAP-01 | **No follow-up tool** | **CRITICAL** | The prompt instructs Eli about follow-up behavior at T+30min, T+24h, T+72h intervals, but there is NO tool that Eli can call to schedule a delayed/future message. The prompt says "APENAS quando o sistema de follow-up automatico disparar" -- but this system is implemented via `pulse-agent.ts` (a BullMQ cron job), NOT via a tool Eli can invoke. Eli has no mechanism to trigger or influence follow-ups from within a conversation. | Follow-ups happen independently via Pulse cron; Eli cannot proactively schedule one if the conversation flow suggests it would be beneficial. However, the prompt explicitly says "Voce NAO inicia follow-ups por conta propria" which means this is BY DESIGN -- not a bug. The gap is purely architectural: no bridge between Eli's conversation context and Pulse's scheduling. |
| GAP-02 | **No send_message / outbound messaging tool** | **CRITICAL** | Eli can ONLY respond within the current conversation turn. There is no tool to proactively send a message to a contact outside the current request-response cycle. The MCP server has `send_message` but it is NOT exposed to Eli's LLM tool calls. | Eli cannot send confirmation reminders, cannot message other contacts, cannot send media/templates. All outbound beyond the current response must go through Pulse or manual action. |

### 4.2 HIGH Gaps

| ID | Gap | Severity | Description | Impact |
|----|-----|----------|-------------|--------|
| GAP-03 | **No remove_tag tool** | **HIGH** | `add_tag` exists but there is no `remove_tag`. If a tag was incorrectly applied or a contact's status changes, Eli cannot remove it. | Tags accumulate without cleanup ability. Human intervention required to remove wrong tags. |
| GAP-04 | **No update_contact tool** | **HIGH** | Eli can read contact info (`get_contact_info`) and add tags, but cannot update the contact's name, email, or custom fields. If a client says "my name is actually X" or "my email is Y", Eli cannot act on it. | Missed data enrichment opportunities. Contact corrections require human action. |
| GAP-05 | **No list_pipelines / get_pipeline_stages tool** | **HIGH** | `move_pipeline_stage` accepts a `stage_name` string and returns available stages on error, but there is no proactive tool to LIST pipeline stages before attempting a move. Eli must guess or fail first to discover available stages. | Wastes a tool call iteration on failure. Prompt never instructs Eli to move pipeline stages proactively, so this is mitigated. But if the LLM decides to use it autonomously, it has no way to discover valid stage names first. |
| GAP-06 | **No trigger_flow tool (Eli-accessible)** | **HIGH** | The MCP server has `trigger_flow` (execute automation flows), but this is NOT available to Eli's LLM tool calls. If a conversation reaches a state where a flow should be triggered (e.g., onboarding, reactivation campaign), Eli cannot do it. | Automation flows can only be triggered by the MCP server (external callers), not by the autonomous agent during conversation. |

### 4.3 MEDIUM Gaps

| ID | Gap | Severity | Description | Impact |
|----|-----|----------|-------------|--------|
| GAP-07 | **No get_business_hours tool** | **MEDIUM** | The prompt tells Eli to inform operating hours ("FORA DO HORARIO: informe horarios"), but Eli must rely on the knowledge base to know the hours. There is no dedicated tool to fetch structured business hours from the DB (`businessHours` table exists and is used in guardrails). | Eli might hallucinate hours if the KB entry is missing or outdated. The DB has the authoritative data. |
| GAP-08 | **No send_media tool** | **MEDIUM** | Eli can only send text responses. There is no tool to send images, documents, audio, or location pins via WhatsApp. | Cannot share location map, price list images, or promotional materials during conversation. |
| GAP-09 | **No get_barbers tool (standalone)** | **MEDIUM** | Barber list is returned as a side effect of `get_services`. There is no dedicated tool to just list available barbers. The prompt says "QUEM TRABALHA HOJE: chame get_services (retorna barbeiros ativos)" -- this works but is semantically wrong (calling a services tool to get barber info). | Minor inefficiency. The workaround (get_services) works, but the tool call is heavier than needed (fetches all services + all barber restrictions). |
| GAP-10 | **No schedule_appointment_reminder tool** | **MEDIUM** | After creating an appointment, Eli cannot schedule a reminder (e.g., "lembrete 1h antes"). This must be handled externally by Pulse or the BestBarbers system. | No in-conversation confirmation that a reminder will be sent. Client may miss the appointment. |
| GAP-11 | **search_knowledge_base is never explicitly named in prompt** | **MEDIUM** | The prompt says "Use a base de conhecimento" and "SEMPRE informe endereco completo" but never names the `search_knowledge_base` tool explicitly. The LLM must infer from the tool description that this is how to access the KB. | Works in practice (LLM reads tool descriptions), but inconsistent with other tools which ARE explicitly named. Could lead to the LLM trying to answer from the inline KB entries instead of calling the tool. |
| GAP-12 | **get_contact_info never explicitly referenced in prompt flows** | **MEDIUM** | The `get_contact_info` tool exists and works, but the prompt never instructs Eli to call it. Contact data (name, phone, email) is pre-loaded into the system prompt context. The tool is redundant for the current flow but useful if the LLM needs to refresh or verify data mid-conversation. | Mostly harmless. The tool exists as a safety net but is effectively unused by the prompt's design. |

### 4.4 LOW / Informational

| ID | Gap | Severity | Description |
|----|-----|----------|-------------|
| GAP-13 | **Subscription plan prices hardcoded in prompt** | LOW | The prompt hardcodes plan prices (SMART R$79,90, FLEX R$99,90, BLACK R$129,90 etc.) in the `buildFlows` function. These are not fetched dynamically from any tool or DB. If prices change, the prompt must be redeployed. |
| GAP-14 | **Barber name normalization hardcoded** | LOW | Rule 8 hardcodes name variations ("Wanderson=Vanderson, Stefane=Stephane, Nathan/Nattan=Natan"). Adding a new barber or fixing a name requires a code change, not a config change. |
| GAP-15 | **MCP server tools not bridged to Eli** | LOW | The MCP server (`/home/tikso/tikso/src/lib/mcp/server.ts`) exposes 7 tools (`list_contacts`, `send_message`, `get_conversation`, `move_pipeline`, `add_tag`, `trigger_flow`, `get_analytics`) intended for external MCP clients. None of these are available to Eli's LLM tool-calling loop. Some overlap with core tools (`add_tag`, `move_pipeline_stage`); others are unique (`send_message`, `trigger_flow`, `list_contacts`, `get_analytics`). |

---

## 5. Architecture Diagram: Tool Accessibility

```
+-------------------------------------------+
|         Eli (AutonomousAgent)             |
|  LLM Tool Calling Loop (max 5 iter)      |
|                                           |
|  ACCESSIBLE TOOLS:                        |
|  +-- Core (6) --+  +-- BB (7) ----------+|
|  | get_contact   |  | get_services       ||
|  | add_tag       |  | check_availability ||
|  | move_pipeline |  | get_subscriber     ||
|  | add_note      |  | get_history        ||
|  | transfer_human|  | create_appointment ||
|  | search_kb     |  | cancel_appointment ||
|  +---------------+  | reschedule_appt    ||
|                      +--------------------+|
+-------------------------------------------+
          |
          | (NOT connected)
          v
+-------------------------------------------+
|         MCP Server (External)             |
|  SEPARATE TOOLS (not in Eli):             |
|  - list_contacts                          |
|  - send_message        <-- CRITICAL GAP   |
|  - get_conversation                       |
|  - move_pipeline (duplicate)              |
|  - add_tag (duplicate)                    |
|  - trigger_flow        <-- HIGH GAP       |
|  - get_analytics                          |
+-------------------------------------------+
          |
          v
+-------------------------------------------+
|         Pulse Agent (Cron)                |
|  BACKGROUND JOBS (not tools):             |
|  - Follow-up messages   <-- CRITICAL GAP  |
|  - Reactivation campaigns                 |
|  - Reminder scheduling                    |
+-------------------------------------------+
```

---

## 6. Recommendations

### Priority 1: Address Critical Gaps

#### R1: Create `schedule_followup` tool (addresses GAP-01)

**Trade-offs:**
- (+) Eli can contextually trigger follow-ups ("this client seems interested but didn't confirm")
- (+) Follows the "copy conversational" philosophy -- Eli knows when a follow-up is needed
- (-) Risk of over-follow-up if LLM judgment is poor -- needs guardrails (max 3 per contact)
- (-) Requires integration with BullMQ/Pulse job queue

**Recommendation:** Create a tool that enqueues a delayed job in BullMQ with the follow-up message template and delay interval. The Pulse agent already processes these jobs. The bridge is straightforward.

```typescript
// Proposed interface:
{
  name: "schedule_followup",
  parameters: {
    delay_minutes: number,  // 30, 1440 (24h), 4320 (72h)
    message_hint: string,   // Context for Pulse to generate the right message
    followup_type: "curiosity" | "value" | "farewell"
  }
}
```

#### R2: Bridge `send_message` from MCP to Eli (addresses GAP-02)

**Trade-offs:**
- (+) Eli could send media, templates, proactive messages
- (-) Security risk: Eli could spam contacts if misused
- (-) Current architecture intentionally limits Eli to the response cycle for safety

**Recommendation:** DEFER. The current design is intentional -- Eli responds within the conversation turn only. Proactive messaging is delegated to Pulse. This is architecturally sound. If needed, create a limited `send_template_message` tool instead (pre-approved templates only).

### Priority 2: Address High Gaps

#### R3: Create `remove_tag` tool (addresses GAP-03)

**Implementation:** Mirror `add_tag` in `aria-tools.ts`. Simple DB query: `db.contactTag.delete()`. Low risk.

#### R4: Create `update_contact` tool (addresses GAP-04)

**Trade-offs:**
- (+) Eli can update name corrections and email addresses
- (-) Must restrict which fields can be updated (never phone, never org membership)
- Recommended: allow only `name`, `email` fields

#### R5: Create `list_pipeline_stages` tool (addresses GAP-05)

**Implementation:** Simple `db.pipelineStage.findMany()` returning `[{ name, pipeline_name }]`. Low risk.

#### R6: Create `trigger_flow` tool for Eli (addresses GAP-06)

**Trade-offs:**
- (+) Powerful automation capability (onboarding flows, win-back campaigns)
- (-) High risk: LLM could trigger expensive/disruptive flows
- Recommended: whitelist specific flow IDs in the prompt, not open-ended

### Priority 3: Address Medium Gaps

#### R7: Create `get_business_hours` tool (addresses GAP-07)

**Implementation:** Query `db.businessHours` and return structured hours per day. Eliminates hallucination risk for operating hours.

#### R8: Add `search_knowledge_base` to prompt flow instructions (addresses GAP-11)

**Implementation:** In `buildFlows()`, add explicit mention: "Para informacoes gerais (horarios, localizacao, pagamento): chame search_knowledge_base."

#### R9: Make subscription plan prices dynamic (addresses GAP-13)

**Implementation:** Create a `get_subscription_plans` tool that queries the BestBarbers API for current plans, or add a KB entry that is kept in sync. Remove hardcoded prices from the prompt.

---

## 7. Files Analyzed

| File | Path | Purpose |
|------|------|---------|
| BestBarbers tools definitions | `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tools.ts` | 7 BB tool definitions + executeBBTool dispatcher |
| BestBarbers tool implementations | `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/tool-implementations.ts` | Full implementation of all 7 BB tools |
| BestBarbers types | `/home/tikso/tikso/src/lib/integrations/providers/bestbarbers/types.ts` | BestBarbersConfig, BBService, BBBarber interfaces |
| Core tools (ARIA) | `/home/tikso/tikso/src/lib/ai/aria-tools.ts` | 6 core tool definitions + implementations + dynamic loading |
| Autonomous agent | `/home/tikso/tikso/src/lib/ai/autonomous-agent.ts` | Tool calling loop, circuit breaker, response parsing, guardrails |
| Prompt builder | `/home/tikso/tikso/src/lib/ai/prompt-builder.ts` | Modular system prompt (identity, flows, rules, anti-hallucination) |
| ARIA streaming | `/home/tikso/tikso/src/lib/ai/aria-streaming.ts` | Streaming response generation (no tool-related logic) |
| MCP server | `/home/tikso/tikso/src/lib/mcp/server.ts` | 7 MCP tools for external clients (NOT accessible to Eli) |
| Pulse agent | `/home/tikso/tikso/src/lib/agents/pulse-agent.ts` | Cron-based follow-ups and reactivation (background, not tools) |

---

## 8. Summary

| Metric | Count |
|--------|-------|
| Total tools accessible to Eli | **13** (6 core + 7 BB) |
| Tools referenced in prompt | **11** (all core + 5 BB) |
| Tools in prompt but NOT in code | **0** |
| Tools in code but NOT in prompt | **2** (`get_contact_info`, `search_knowledge_base` -- both implicit) |
| CRITICAL gaps | **2** (follow-up scheduling, outbound messaging) |
| HIGH gaps | **4** (remove_tag, update_contact, list_pipelines, trigger_flow) |
| MEDIUM gaps | **6** |
| LOW/Info gaps | **3** |

**Overall Assessment:** The tool system is well-implemented and well-integrated. All tools mentioned in the prompt exist and are accessible. The circuit breaker (ELI-02) and error sanitization (ELI-03) provide robust safety nets. The CRITICAL gaps around follow-up scheduling are mitigated by the architectural decision to handle follow-ups via the Pulse background agent. The most actionable improvements are the HIGH-priority gaps (remove_tag, update_contact) which are low-risk, high-value additions.

--- Aria, arquitetando o futuro
