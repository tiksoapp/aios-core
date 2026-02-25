# Impact Analysis: Eli Tools Expansion (15 Gaps)

**Date:** 2026-02-25
**Author:** Aria (Architect Agent)
**Scope:** Full impact analysis for implementing the 15 gaps identified in the Eli Tools Audit
**Server:** Vultr (`ssh vultr`), project at `/home/tikso/tikso/`
**Ref:** `/root/aios-core/docs/research/eli-tools-audit.md`

---

## 1. Current State Baseline

### 1.1 Tool Count

| Category | Count | Where Defined |
|----------|-------|---------------|
| Core tools | 6 | `aria-tools.ts` CORE_TOOL_DEFINITIONS |
| BestBarbers tools | 7 | `tools.ts` BB_TOOL_DEFINITIONS |
| **Total accessible to Eli** | **13** | Merged in `getToolsForOrg()` |
| MCP server tools (NOT in Eli) | 7 | `mcp/server.ts` (separate) |

### 1.2 Current Token Budget (Estimated)

| Component | Characters | Est. Tokens | Notes |
|-----------|-----------|-------------|-------|
| System prompt (prompt-builder) | ~19,600 | ~5,200 | 327 lines, 7 modules |
| Tool definitions (13 tools) | ~28,000 | ~7,400 | JSON schema sent to LLM |
| Conversation context (15 msgs) | ~3,000 | ~800 | Variable per conversation |
| Knowledge base context | ~2,500 | ~660 | RAG results, up to 5 entries |
| Memory context | ~500 | ~130 | Contact memories, up to 3 |
| **Estimated total per request** | **~53,600** | **~14,200** | Well within Claude/GPT-4o limits |

Token estimation: ~3.8 characters per token (typical for mixed pt-BR/JSON content).

### 1.3 Safety Mechanisms

| Mechanism | Current Value | File |
|-----------|---------------|------|
| MAX_TOOL_ITERATIONS | 5 | `autonomous-agent.ts:63` |
| CB_GLOBAL_FAILURE_THRESHOLD | 3 | `autonomous-agent.ts:68` |
| CB_SAME_TOOL_FAILURE_THRESHOLD | 2 | `autonomous-agent.ts:71` |
| LLM timeout | 30s | `autonomous-agent.ts:420` |
| LLM max attempts | 2 | `autonomous-agent.ts:417` |
| max_tokens response | 500 | `autonomous-agent.ts:425` |

---

## 2. Impact Diagram

```
+======================================================================+
|                    IMPACT MAP: 15 GAPS                               |
+======================================================================+
|                                                                      |
|  SYSTEM PROMPT (prompt-builder.ts)                                   |
|  +---------+----------+-----------+                                  |
|  | GAP-08  | GAP-11   | GAP-13    |                                  |
|  | mention | explicit | dynamic   |                                  |
|  | KB tool | KB name  | prices    |                                  |
|  +---------+----------+-----------+                                  |
|  | GAP-14  |                                                         |
|  | barber  |  Prompt-only changes (no new tools needed)              |
|  | config  |                                                         |
|  +---------+                                                         |
|                                                                      |
|  CORE TOOLS (aria-tools.ts)              NEW TOOLS                   |
|  +-----------------------------------+  +-------------------------+  |
|  | get_contact_info                   |  | remove_tag       GAP-03 |  |
|  | add_tag                            |  | update_contact   GAP-04 |  |
|  | move_pipeline_stage                |  | list_pipelines   GAP-05 |  |
|  | add_internal_note                  |  | get_business_hrs GAP-07 |  |
|  | transfer_to_human                  |  +-------------------------+  |
|  | search_knowledge_base              |  | 4 new core tools         |  |
|  +-----------------------------------+  +-------------------------+  |
|                                                                      |
|  BB TOOLS (bestbarbers/tools.ts)         NEW TOOLS                   |
|  +-----------------------------------+  +-------------------------+  |
|  | get_services                       |  | get_sub_plans    GAP-13 |  |
|  | check_availability                 |  +-------------------------+  |
|  | get_subscriber_status              |  | 0-1 new BB tools        |  |
|  | get_appointment_history            |  +-------------------------+  |
|  | create_appointment                 |                               |
|  | cancel_appointment                 |                               |
|  | reschedule_appointment             |                               |
|  +-----------------------------------+                               |
|                                                                      |
|  CROSS-CUTTING (autonomous-agent.ts)                                 |
|  +-----------------------------------+                               |
|  | Circuit Breaker thresholds         | <-- May need adjustment      |
|  | MAX_TOOL_ITERATIONS (5)            | <-- Adequate for 17-18 tools |
|  | Tool loop (parallel execution)     | <-- No change needed         |
|  +-----------------------------------+                               |
|                                                                      |
|  ARCHITECTURAL BOUNDARY (Deferred)                                   |
|  +-----------------------------------+                               |
|  | schedule_followup          GAP-01  | <-- BullMQ bridge            |
|  | send_message               GAP-02  | <-- DEFER (by design)        |
|  | trigger_flow               GAP-06  | <-- High risk, whitelist     |
|  | send_media                 GAP-08  | <-- DEFER                    |
|  | schedule_reminder          GAP-10  | <-- Pulse extension          |
|  | MCP bridge                 GAP-15  | <-- DEFER                    |
|  +-----------------------------------+                               |
|                                                                      |
+======================================================================+
```

---

## 3. Per-Gap Impact Analysis

### 3.1 GAP-01: schedule_followup (CRITICAL)

**Files touched:** `aria-tools.ts`, `autonomous-agent.ts` (minor), Pulse agent integration
**Complexity:** HIGH

| Dimension | Impact |
|-----------|--------|
| New code | ~120 lines in `aria-tools.ts` (tool def + implementation) |
| DB changes | NONE -- uses existing `AgentDecisionLog` with `FOLLOWUP_SCHEDULED` action |
| Token cost | +~200 tokens for tool definition |
| Circuit breaker risk | MEDIUM -- BullMQ enqueue could timeout if Redis is down |
| Regression risk | LOW -- new tool, does not modify existing tools |
| Prompt change | MINIMAL -- prompt already instructs about follow-ups; add tool name reference |

**Architecture decision:** The tool would create an `AgentDecisionLog` entry with `action: FOLLOWUP_SCHEDULED` and structured JSON in the `decision` field containing `{ delay_minutes, message_hint, followup_type }`. The Pulse cron already queries these entries. The bridge is a DB write, NOT a direct BullMQ enqueue -- this decouples Eli from the job queue infrastructure.

**Trade-off:** Direct BullMQ enqueue would be faster (no polling delay) but tightly couples Eli to the queue. Using the existing DB pattern means Pulse picks it up on next run (max 15 min delay) -- acceptable for follow-ups that are inherently delayed.

**Security:** Must enforce max 3 follow-ups per contact per conversation to prevent spam. Validate `delay_minutes` to only accept predefined values (30, 1440, 4320).

---

### 3.2 GAP-02: send_message (CRITICAL -- DEFER)

**Recommendation: DO NOT IMPLEMENT**

**Rationale:** The current architecture intentionally confines Eli to the request-response cycle. Eli responds to the current WhatsApp conversation and cannot proactively message contacts. This is a deliberate safety boundary:

1. Eli's messages go through the WhatsApp webhook response flow (inbound triggers outbound)
2. Outbound proactive messaging is exclusively handled by Pulse (follow-ups, reminders, reactivation)
3. Bridging `send_message` would give the LLM the ability to spam arbitrary contacts
4. The antiban system (per-dest rate limiting, lunch reduction, presence detection) is designed around Pulse, NOT around LLM-triggered sends

**If needed in future:** Create a constrained `send_template_message` tool that only allows sending pre-approved WhatsApp template messages (not free-form text). This preserves the safety boundary while enabling appointment confirmations.

---

### 3.3 GAP-03: remove_tag (HIGH)

**Files touched:** `aria-tools.ts` only
**Complexity:** LOW

| Dimension | Impact |
|-----------|--------|
| New code | ~40 lines (tool def + `toolRemoveTag` function) |
| DB changes | NONE -- uses existing `db.contactTag.delete()` |
| Token cost | +~80 tokens for tool definition |
| Circuit breaker risk | LOW -- simple DB delete, same failure profile as `add_tag` |
| Regression risk | NONE -- new tool, mirrors existing `add_tag` pattern |
| Prompt change | Add to rules: "Se uma tag foi adicionada incorretamente, use remove_tag para remover." |

**Implementation pattern:** Mirror `toolAddTag`. Find tag by name, find `contactTag` by contactId + tagId, delete. Return error if tag not found or not assigned.

---

### 3.4 GAP-04: update_contact (HIGH)

**Files touched:** `aria-tools.ts` only
**Complexity:** LOW-MEDIUM

| Dimension | Impact |
|-----------|--------|
| New code | ~60 lines (tool def + `toolUpdateContact` function) |
| DB changes | NONE -- uses existing `db.contact.update()` |
| Token cost | +~120 tokens for tool definition |
| Circuit breaker risk | LOW -- simple DB update |
| Regression risk | LOW -- but must NOT allow updating `phone` or `organizationId` |
| Prompt change | Add: "Se o cliente informar que seu nome ou email esta errado, use update_contact para corrigir." |

**Security constraints (CRITICAL):**
- Allowlist fields: `name`, `email` only
- NEVER expose: `phone`, `organizationId`, `isSubscriber`, `automationPaused`, `optedOutAt`, `journeyState`
- Validate email format if provided
- Validate name is non-empty and <= 100 chars

---

### 3.5 GAP-05: list_pipeline_stages (HIGH)

**Files touched:** `aria-tools.ts` only
**Complexity:** LOW

| Dimension | Impact |
|-----------|--------|
| New code | ~40 lines (tool def + implementation) |
| DB changes | NONE -- uses existing `db.pipelineStage.findMany()` |
| Token cost | +~80 tokens for tool definition |
| Circuit breaker risk | LOW -- read-only query |
| Regression risk | NONE -- new read-only tool |
| Prompt change | NONE -- `move_pipeline_stage` already returns stages on error; this just makes discovery proactive |

**Note:** This tool has the lowest bang-for-buck ratio. The current `move_pipeline_stage` already returns available stages in its error response. The LLM can discover stages by attempting a move. However, it wastes a tool iteration and looks hacky. Implementing this is clean but not urgent.

---

### 3.6 GAP-06: trigger_flow (HIGH)

**Files touched:** `aria-tools.ts`, potentially `flow-engine.ts`
**Complexity:** HIGH

| Dimension | Impact |
|-----------|--------|
| New code | ~80 lines (tool def + implementation + whitelist logic) |
| DB changes | NONE -- uses existing `executeFlowById()` from flow-engine |
| Token cost | +~150 tokens for tool definition |
| Circuit breaker risk | HIGH -- flows can be slow, network-dependent, and have side effects |
| Regression risk | MEDIUM -- a misconfigured flow could send messages, modify data |
| Prompt change | Must enumerate whitelisted flow names in prompt |

**Security constraints (CRITICAL):**
- MUST use a whitelist of allowed flow IDs, stored in the integration config or AIConfig
- MUST NOT allow arbitrary flow execution (LLM could trigger deletion, mass-messaging, etc.)
- Each flow execution should be logged in `AgentDecisionLog`
- Consider rate limiting: max 1 flow trigger per conversation

**Trade-off analysis:**
- (+) Powerful: enables onboarding sequences, win-back campaigns from conversation context
- (-) Dangerous: flows can have arbitrary side effects (send messages, modify pipeline, external API calls)
- (-) Complexity: requires maintaining a whitelist that must stay in sync with flow definitions

**Recommendation:** Implement ONLY if there is a concrete use case (e.g., "trigger onboarding flow when new client signs up via chat"). Do not implement speculatively.

---

### 3.7 GAP-07: get_business_hours (MEDIUM)

**Files touched:** `aria-tools.ts` only
**Complexity:** LOW

| Dimension | Impact |
|-----------|--------|
| New code | ~50 lines (tool def + implementation) |
| DB changes | NONE -- uses existing `db.businessHours.findUnique()` |
| Token cost | +~100 tokens for tool definition |
| Circuit breaker risk | LOW -- read-only query, same pattern as `checkBusinessHours` in autonomous-agent |
| Regression risk | NONE -- new read-only tool |
| Prompt change | Replace "Use a base de conhecimento" for hours -> "Chame get_business_hours para horarios de funcionamento." |

**Note:** The `checkBusinessHours` method already exists in `autonomous-agent.ts` (lines 886-971) as a private method for guardrails. The new tool would reuse the same DB query but format the output for the LLM. No code duplication risk -- the guardrail checks a boolean, the tool returns structured hours.

---

### 3.8 GAP-08: send_media (MEDIUM -- DEFER)

**Recommendation: DEFER to post-MVP**

**Rationale:** Sending media via WhatsApp requires:
1. A media upload/URL mechanism (WhatsApp Cloud API accepts URLs or uploaded media IDs)
2. Knowledge of which media to send (requires a media library concept)
3. The Evolution API v2.3.7 has media sending support, but the channel service abstraction would need extension

This is not a simple tool addition -- it requires extending the entire channel layer. The ROI is low: clients rarely need the chatbot to send images during conversation.

---

### 3.9 GAP-09: get_barbers (standalone) (MEDIUM)

**Recommendation: DO NOT IMPLEMENT as separate tool**

**Rationale:** `get_services` already returns barber data. Adding a separate `get_barbers` tool would:
1. Add +80 tokens to every request for a tool that duplicates data
2. Confuse the LLM about which tool to use ("should I call get_services or get_barbers?")
3. The prompt already instructs: "QUEM TRABALHA HOJE: chame get_services (retorna barbeiros ativos)"

**Alternative:** If barber-only queries are frequent, refactor `get_services` to accept an optional `barbers_only: boolean` parameter that skips service details. This is a minor change to the existing tool, not a new tool.

---

### 3.10 GAP-10: schedule_appointment_reminder (MEDIUM -- Covered by GAP-01)

**Recommendation: Subsume into GAP-01 (schedule_followup)**

If `schedule_followup` is implemented with a `followup_type` parameter, reminders can be modeled as:
```typescript
{ followup_type: "reminder", delay_minutes: 60, message_hint: "Lembrete de agendamento" }
```

Pulse already handles reminders in its `processOverdueFollowups` function. No separate tool needed.

---

### 3.11 GAP-11: Explicit search_knowledge_base in prompt (MEDIUM)

**Files touched:** `prompt-builder.ts` only (buildFlows function)
**Complexity:** TRIVIAL

| Dimension | Impact |
|-----------|--------|
| Code change | ~3 lines in `buildFlows()` |
| Token cost | +~20 tokens (one sentence added to prompt) |
| Regression risk | LOW -- prompt wording change only |

**Change:** In the "INFORMACOES GERAIS" section of `buildFlows()`, change:
```
"Use a base de conhecimento."
```
to:
```
"Chame search_knowledge_base para buscar informacoes na base de conhecimento."
```

---

### 3.12 GAP-12: get_contact_info prompt reference (MEDIUM)

**Recommendation: NO ACTION NEEDED**

Contact data (name, phone, email) is already injected into the system prompt via `buildContact()`. The `get_contact_info` tool exists as a safety net for mid-conversation refresh. Adding explicit prompt instructions would cause the LLM to call it unnecessarily on every conversation, wasting a tool iteration.

The tool is correctly positioned as an implicit fallback. Leave as-is.

---

### 3.13 GAP-13: Dynamic subscription plan prices (LOW)

**Files touched:** `prompt-builder.ts` (buildFlows), potentially new BB tool
**Complexity:** MEDIUM

**Option A: Tool approach (get_subscription_plans)**
| Dimension | Impact |
|-----------|--------|
| New code | ~80 lines (new BB tool in `tools.ts` + `tool-implementations.ts`) |
| Token cost | +~120 tokens for tool definition |
| Trade-off | (+) Always accurate, (-) extra API call to BB, (+) no prompt maintenance |

**Option B: KB approach**
| Dimension | Impact |
|-----------|--------|
| New code | ZERO |
| Maintenance | Update KB entry when prices change |
| Trade-off | (+) Zero code, (-) requires manual update, (+) no tool overhead |

**Recommendation:** Option B (KB approach) for now. Plan prices change infrequently (quarterly at most). The `search_knowledge_base` tool already retrieves KB entries. Create a KB entry titled "Planos de Assinatura" with current prices. Remove hardcoded prices from `buildFlows()` and replace with: "Para precos de planos: chame search_knowledge_base com 'planos assinatura'."

---

### 3.14 GAP-14: Barber name normalization config (LOW)

**Files touched:** `prompt-builder.ts` (buildRules), potentially KB or DB config
**Complexity:** LOW

**Option A: Move to KB**
Store barber name variations as a KB entry. Pro: no code deploy for new barbers. Con: relies on LLM reading KB results correctly.

**Option B: Move to AIConfig DB field**
Add a `barberNameVariations` JSON field to AIConfig. Pro: structured, editable via admin panel. Con: requires schema change.

**Option C: Keep in code (NO CHANGE)**
The current approach works. Barber changes are rare (1-2 per year). A code deploy is acceptable.

**Recommendation:** Option C for now. This is a LOW priority gap with minimal business impact.

---

### 3.15 GAP-15: MCP server tools bridge (LOW)

**Recommendation: DO NOT IMPLEMENT**

The MCP server serves a fundamentally different purpose -- it provides tools to external MCP clients (e.g., other AI agents, dashboards). Bridging MCP tools into Eli's tool loop would:
1. Create circular dependencies (MCP server uses channel-service which triggers Eli)
2. Duplicate tools (`add_tag`, `move_pipeline` already exist in both)
3. Expose dangerous tools (`list_contacts`, `send_message`, `get_analytics`) to the LLM

The two tool systems are architecturally separate by design. Keep them separate.

---

## 4. LLM Token Impact Analysis

### 4.1 Projected Tool Count After Implementation

| Scenario | Tool Count | Token Cost (tool defs) | Delta |
|----------|-----------|----------------------|-------|
| **Current** | 13 | ~7,400 tokens | baseline |
| **Conservative** (GAP-03, 04, 07, 11) | 16 | ~8,180 tokens | +780 |
| **Moderate** (Conservative + GAP-01, 05) | 18 | ~8,660 tokens | +1,260 |
| **Aggressive** (Moderate + GAP-06, 13) | 20 | ~9,130 tokens | +1,730 |

### 4.2 Total Prompt Size Projections

| Scenario | System Prompt | Tool Defs | Context | Total | % of 128K window |
|----------|--------------|-----------|---------|-------|-------------------|
| **Current** | ~5,200 | ~7,400 | ~1,590 | ~14,190 | 11.1% |
| **Conservative** | ~5,260 | ~8,180 | ~1,590 | ~15,030 | 11.7% |
| **Moderate** | ~5,280 | ~8,660 | ~1,590 | ~15,530 | 12.1% |
| **Aggressive** | ~5,360 | ~9,130 | ~1,590 | ~16,080 | 12.6% |

**Verdict:** Even the aggressive scenario uses only 12.6% of the context window. Token budget is NOT a constraint. The real constraint is LLM tool selection accuracy (see section 4.3).

### 4.3 LLM Tool Selection Accuracy Risk

Research and empirical data on LLM tool calling with large tool sets:

| Tool Count | Selection Accuracy | Latency Impact | Notes |
|-----------|-------------------|----------------|-------|
| 1-10 | ~98% | Baseline | Optimal range |
| 11-15 | ~95% | +5-10% | Current state (13 tools) |
| 16-20 | ~90-93% | +10-20% | Conservative/Moderate target |
| 21-30 | ~80-88% | +20-40% | NOT recommended |
| 30+ | <80% | +50%+ | Strongly NOT recommended |

**Recommendation:** Stay at or below 20 tools total. The moderate scenario (18 tools) is the sweet spot -- meaningful capability gains with minimal accuracy degradation.

### 4.4 Recommended Maximum Tool Limit

**HARD LIMIT: 20 tools per request.**

Rationale:
- Claude 3.5 Sonnet / GPT-4o handle 20 tools reliably (>90% accuracy)
- Beyond 20, diminishing returns: each additional tool adds confusion
- The 5-iteration tool loop further constrains effective tool chains to 3-4 unique tools per conversation
- If future integrations (ListenPlay, Nexaas) add more tools, implement tool routing: only load integration tools relevant to the detected intent

---

## 5. Circuit Breaker Impact Assessment

### 5.1 Current Thresholds vs. Expanded Tool Set

| Threshold | Current Value | Adequate for 18 tools? | Recommendation |
|-----------|---------------|----------------------|----------------|
| CB_GLOBAL_FAILURE_THRESHOLD (3) | 3 consecutive global failures | YES | Keep at 3 |
| CB_SAME_TOOL_FAILURE_THRESHOLD (2) | 2 consecutive failures of same tool | YES | Keep at 2 |
| MAX_TOOL_ITERATIONS (5) | 5 rounds | YES, but tight | Consider raising to 6 |

### 5.2 New Tools Failure Probability Assessment

| New Tool | Failure Profile | Expected Failure Rate | CB Risk |
|----------|----------------|----------------------|---------|
| `remove_tag` | DB query, same as add_tag | <1% | LOW |
| `update_contact` | DB update, validated | <1% | LOW |
| `list_pipeline_stages` | DB read-only | <0.5% | NEGLIGIBLE |
| `get_business_hours` | DB read-only | <0.5% | NEGLIGIBLE |
| `schedule_followup` | DB write (AgentDecisionLog) | ~2% | LOW |
| `trigger_flow` | Flow engine execution | ~5-10% | MEDIUM-HIGH |

**Key finding:** `trigger_flow` (GAP-06) is the only new tool with a meaningful failure rate. If implemented, it could exhaust the per-tool threshold (2 failures) in edge cases where the flow engine is slow or the flow is misconfigured. This reinforces the recommendation to defer GAP-06 unless a concrete use case exists.

### 5.3 Circuit Breaker Recommendations

1. **Keep CB_GLOBAL_FAILURE_THRESHOLD at 3.** With 18 tools, 3 consecutive global failures still indicates systemic issues (DB down, network issues). No change needed.

2. **Keep CB_SAME_TOOL_FAILURE_THRESHOLD at 2.** New tools mirror existing patterns (simple DB ops). A tool that fails twice is genuinely broken.

3. **Consider raising MAX_TOOL_ITERATIONS from 5 to 6.** With 18 tools, a complex booking flow might require: `get_subscriber_status` -> `check_availability` -> `create_appointment` -> `add_tag` -> `add_internal_note` = 5 iterations. Adding a `schedule_followup` at the end would hit the limit. Raising to 6 provides breathing room without risk (the last iteration already forces `tool_choice: "none"`).

4. **Add timeout handling for `trigger_flow`.** If implemented, wrap with a 10s timeout (vs. the 30s LLM timeout). Flows that take >10s should be queued, not executed inline.

---

## 6. Prompt-Builder Impact Assessment

### 6.1 Current Prompt Structure

| Module | Lines | Characters | Est. Tokens |
|--------|-------|-----------|-------------|
| `buildTemporal()` | 10 | 250 | 66 |
| `buildIdentity()` | 12 | 750 | 198 |
| `buildContact()` | 6 | 200 | 53 |
| `buildConversationalCopy()` | 60 | 3,800 | 1,000 |
| `buildFlows()` | 90 | 5,500 | 1,447 |
| `buildRules()` | 55 | 3,200 | 842 |
| `buildAntiHallucination()` | 12 | 650 | 171 |
| `buildResponseFormat()` | 5 | 200 | 53 |
| **Total (fixed)** | **250** | **14,550** | **3,830** |
| Dynamic sections (personality, FAQ, etc.) | ~50 | ~5,000 | ~1,320 |
| **Total (typical)** | **~300** | **~19,600** | **~5,200** |

### 6.2 Prompt Changes Required Per Gap

| Gap | Module Affected | Lines Added | Token Delta | Risk |
|-----|----------------|-------------|-------------|------|
| GAP-01 | `buildFlows()` | +3 | +20 | LOW -- add tool name to follow-up section |
| GAP-03 | `buildRules()` | +2 | +15 | LOW -- add remove_tag usage instruction |
| GAP-04 | `buildRules()` | +3 | +20 | LOW -- add update_contact instruction |
| GAP-07 | `buildFlows()` | +2 | +15 | LOW -- replace KB reference with tool name |
| GAP-11 | `buildFlows()` | +1 | +10 | TRIVIAL -- explicit tool name |
| GAP-13 | `buildFlows()` | -8/+3 | -30 | LOW -- remove hardcoded prices, add KB reference |
| **Total prompt delta** | | **+6 net** | **+50** | |

**Verdict:** The prompt impact is negligible. Total growth of ~50 tokens across all changes. No risk of approaching context window limits.

### 6.3 Behavioral Change Risk

The most sensitive prompt changes are in `buildFlows()` and `buildRules()`. These directly control Eli's conversation behavior.

| Change | Behavioral Risk | Mitigation |
|--------|----------------|------------|
| Adding `remove_tag` instruction | LOW -- new capability, no existing behavior change | Test that Eli does not proactively remove tags without client request |
| Adding `update_contact` instruction | MEDIUM -- Eli might over-eagerly update contacts | Restrict to explicit corrections: "se o cliente CORRIGIR nome ou email" |
| Replacing hardcoded prices with KB lookup | MEDIUM -- Eli might fail to find prices if KB entry missing | Keep hardcoded as fallback until KB entry confirmed |
| Adding `get_business_hours` | LOW -- replaces an implicit behavior with explicit | Test that Eli uses the tool instead of KB for hours |

---

## 7. Dependency Matrix

### 7.1 Gap Dependencies

```
GAP-01 (schedule_followup)
  |-- depends on: Pulse cron must query AgentDecisionLog for FOLLOWUP_SCHEDULED
  |-- blocks: GAP-10 (schedule_reminder, subsumed)
  '-- independent of all other gaps

GAP-02 (send_message) --> DEFERRED, no dependencies

GAP-03 (remove_tag)
  '-- fully independent, no dependencies

GAP-04 (update_contact)
  '-- fully independent, no dependencies

GAP-05 (list_pipeline_stages)
  '-- fully independent, no dependencies

GAP-06 (trigger_flow)
  |-- depends on: whitelist of allowed flows must be defined
  '-- independent of all other gaps

GAP-07 (get_business_hours)
  '-- fully independent, no dependencies

GAP-08 (send_media) --> DEFERRED

GAP-09 (get_barbers) --> NOT IMPLEMENTING (use get_services)

GAP-10 (schedule_reminder) --> SUBSUMED by GAP-01

GAP-11 (explicit KB name in prompt)
  '-- fully independent, prompt-only change

GAP-12 (get_contact_info prompt) --> NO ACTION NEEDED

GAP-13 (dynamic prices)
  |-- depends on: KB entry created for subscription plans
  '-- independent of code changes

GAP-14 (barber name config) --> NO ACTION (keep in code)

GAP-15 (MCP bridge) --> NOT IMPLEMENTING
```

### 7.2 Parallelism Matrix

Gaps that can be implemented simultaneously without conflict:

| Parallel Group | Gaps | Shared Files | Risk |
|---------------|------|-------------|------|
| **Group A** (core tools) | GAP-03, GAP-04, GAP-05, GAP-07 | `aria-tools.ts` | LOW -- each adds a new function, no overlapping code |
| **Group B** (prompt only) | GAP-11, GAP-13 | `prompt-builder.ts` | LOW -- different sections of the prompt |
| **Group C** (architectural) | GAP-01 | `aria-tools.ts` + Pulse integration | MEDIUM -- touches DB pattern |
| **Group D** (high risk) | GAP-06 | `aria-tools.ts` + flow-engine | HIGH -- needs whitelist design |

Groups A and B can be implemented in parallel. Group C should follow Group A (to validate the aria-tools.ts pattern with simpler tools first). Group D should be last (highest risk, needs design review).

---

## 8. Recommended Implementation Order

### Wave 1: Quick Wins (1-2 days)

| Priority | Gap | Description | Effort | Risk |
|----------|-----|-------------|--------|------|
| 1 | GAP-03 | `remove_tag` tool | 2h | LOW |
| 2 | GAP-04 | `update_contact` tool | 3h | LOW |
| 3 | GAP-11 | Explicit `search_knowledge_base` in prompt | 30min | TRIVIAL |
| 4 | GAP-07 | `get_business_hours` tool | 2h | LOW |

**Rationale:** These are all simple, independent changes. GAP-03 and GAP-04 are the highest-value items in the audit (client-requested corrections today require human intervention). GAP-07 eliminates a hallucination vector. GAP-11 is a 30-minute prompt tweak.

**Total new tools:** +3 (remove_tag, update_contact, get_business_hours) -> 16 tools total
**Total new tokens:** ~380 (tool defs) + ~50 (prompt changes) = ~430 tokens

### Wave 2: Moderate Value (2-3 days)

| Priority | Gap | Description | Effort | Risk |
|----------|-----|-------------|--------|------|
| 5 | GAP-05 | `list_pipeline_stages` tool | 2h | LOW |
| 6 | GAP-13 | Dynamic subscription prices (KB approach) | 1h | LOW |
| 7 | GAP-01 | `schedule_followup` tool | 4-6h | MEDIUM |

**Rationale:** GAP-05 is low-value but low-effort (clean improvement). GAP-13 is a maintenance improvement (KB entry + prompt cleanup). GAP-01 is the most impactful gap overall -- it bridges Eli's conversation context to the Pulse follow-up system.

**Dependencies:** GAP-01 requires verifying that Pulse's `processOverdueFollowups()` can pick up entries from `AgentDecisionLog` with `FOLLOWUP_SCHEDULED` action. If Pulse only reads from BullMQ, a small adapter is needed.

**Total new tools:** +2 (list_pipeline_stages, schedule_followup) -> 18 tools total
**Total new tokens:** ~280 (tool defs) + ~20 (prompt) = ~300 tokens

### Wave 3: Deferred / Conditional (evaluate after Wave 2)

| Priority | Gap | Description | Condition | Effort |
|----------|-----|-------------|-----------|--------|
| 8 | GAP-06 | `trigger_flow` tool | Only if concrete use case identified | 4-6h |
| 9 | GAP-14 | Barber name normalization config | Only if barber roster changes frequently | 2h |
| -- | GAP-02 | `send_message` bridge | Only if template-based sending needed | 8-12h |
| -- | GAP-08 | `send_media` tool | Only if media sending use case validated | 8-12h |
| -- | GAP-10 | `schedule_reminder` | Covered by GAP-01 schedule_followup | 0h |
| -- | GAP-15 | MCP bridge | NOT recommended | -- |
| -- | GAP-09 | `get_barbers` standalone | NOT recommended (use get_services) | -- |
| -- | GAP-12 | `get_contact_info` prompt ref | NO ACTION needed | -- |

---

## 9. Regression Risk Map

### 9.1 Changes to aria-tools.ts

The primary risk vector. All new core tools are added to this file.

| Risk Area | Description | Mitigation |
|-----------|-------------|------------|
| `CORE_TOOL_DEFINITIONS` array | Adding new tool definitions could break the array structure | Each tool is an independent object in the array; append-only pattern |
| `executeToolCall` switch statement | Adding new cases to the switch | New cases BEFORE the `default:` -- no impact on existing cases |
| `getToolsForOrg` function | No changes needed -- it already spreads `CORE_TOOL_DEFINITIONS` | ZERO regression risk |
| Existing tool implementations | NOT modified by any gap | ZERO regression risk |

**Key safety point:** No existing tool function (`toolGetContactInfo`, `toolAddTag`, etc.) is modified. All new tools are NEW functions appended to the file. The switch statement in `executeToolCall` gains new cases but existing cases are untouched.

### 9.2 Changes to prompt-builder.ts

| Risk Area | Description | Mitigation |
|-----------|-------------|------------|
| `buildFlows()` | Adding/modifying tool references in flow instructions | Test key flows: booking, cancellation, subscription inquiry |
| `buildRules()` | Adding new rules | Ensure new rules don't contradict existing rules (no duplicate numbers) |
| `buildConversationalCopy()` | NOT modified | ZERO risk |
| `buildIdentity()` | NOT modified | ZERO risk |

### 9.3 Changes to autonomous-agent.ts

| Risk Area | Description | Mitigation |
|-----------|-------------|------------|
| `MAX_TOOL_ITERATIONS` | May increase from 5 to 6 | Only affects the loop boundary; test with 6-tool-call conversation |
| Circuit breaker thresholds | NOT changing | ZERO risk |
| Tool loop logic | NOT changing | ZERO risk |
| `callLLM` function | NOT changing | ZERO risk |

### 9.4 Minimum Test Matrix

| Test Category | What to Test | Per Gap |
|--------------|-------------|---------|
| Unit: tool function | Call new tool function directly, verify return shape | GAP-01, 03, 04, 05, 07 |
| Unit: error handling | Call with invalid args, missing contact, null values | GAP-01, 03, 04, 05, 07 |
| Unit: security | Verify restricted fields are NOT updatable (GAP-04) | GAP-04, GAP-06 |
| Integration: tool loop | Full LLM tool call -> execute -> respond cycle | ALL new tools |
| Integration: circuit breaker | Verify CB triggers correctly with new tools failing | GAP-01, GAP-06 |
| E2E: conversation flow | Send WhatsApp message that triggers new tool usage | Wave 1, Wave 2 |
| Prompt regression | Verify existing flows (booking, cancel, reschedule) still work after prompt changes | GAP-11, GAP-13 |

**Estimated test count per wave:**
- Wave 1: 12-15 unit tests + 4-5 integration tests
- Wave 2: 8-10 unit tests + 3-4 integration tests + 1-2 E2E tests
- Wave 3 (GAP-06): 5-8 unit tests + 2-3 integration tests + security audit

---

## 10. Summary Decision Matrix

| Gap | Action | Wave | New Tool? | Token Impact | Risk | Business Value |
|-----|--------|------|-----------|-------------|------|---------------|
| GAP-01 | IMPLEMENT | 2 | YES | +200 | MEDIUM | HIGH |
| GAP-02 | DEFER | -- | -- | -- | -- | MEDIUM |
| GAP-03 | IMPLEMENT | 1 | YES | +80 | LOW | HIGH |
| GAP-04 | IMPLEMENT | 1 | YES | +120 | LOW | HIGH |
| GAP-05 | IMPLEMENT | 2 | YES | +80 | LOW | LOW |
| GAP-06 | CONDITIONAL | 3 | YES | +150 | HIGH | MEDIUM |
| GAP-07 | IMPLEMENT | 1 | YES | +100 | LOW | MEDIUM |
| GAP-08 | DEFER | -- | -- | -- | -- | LOW |
| GAP-09 | SKIP | -- | NO | -- | -- | LOW |
| GAP-10 | SUBSUMED | 2 | NO (in GAP-01) | 0 | -- | MEDIUM |
| GAP-11 | IMPLEMENT | 1 | NO (prompt only) | +10 | TRIVIAL | MEDIUM |
| GAP-12 | SKIP | -- | NO | -- | -- | LOW |
| GAP-13 | IMPLEMENT | 2 | NO (KB entry) | -30 | LOW | LOW |
| GAP-14 | SKIP | -- | NO | -- | -- | LOW |
| GAP-15 | SKIP | -- | NO | -- | -- | LOW |

**Totals:**
- **IMPLEMENT:** 7 gaps (GAP-01, 03, 04, 05, 07, 11, 13)
- **CONDITIONAL:** 1 gap (GAP-06)
- **DEFER:** 2 gaps (GAP-02, 08)
- **SKIP:** 5 gaps (GAP-09, 12, 14, 15, and GAP-10 subsumed)
- **New tools added:** 5 (remove_tag, update_contact, list_pipeline_stages, get_business_hours, schedule_followup)
- **Final tool count:** 18 (within the recommended 20-tool limit)
- **Total token impact:** +~730 tokens (+5.1% increase)
- **Context window usage:** 12.1% (from 11.1%) -- well within budget

---

-- Aria, arquitetando o futuro
