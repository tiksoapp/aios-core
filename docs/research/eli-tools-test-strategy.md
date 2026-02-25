# Eli Tools -- Test Strategy & Quality Assessment

**Date:** 2026-02-25
**Author:** Quinn (QA Agent)
**Input:** `eli-tools-audit.md` by Aria (Architect Agent)
**Server:** Vultr (`ssh vultr`), project at `/home/tikso/tikso/`

---

## 1. Current Test Inventory

### 1.1 Overall Numbers

| Metric | Count |
|--------|-------|
| Total test files | 23 |
| Total test cases (passing) | 407 |
| Test framework | Vitest |
| All tests passing | YES (as of 2026-02-25) |

### 1.2 Test Files Relevant to Eli Tools

| File | Path | Test Cases | Coverage Area |
|------|------|------------|---------------|
| `circuit-breaker.test.ts` | `src/__tests__/agents/` | 9 | ELI-02: Circuit breaker global/per-tool thresholds, handoff, reset |
| `eli03-error-classification.test.ts` | `src/__tests__/ai/` | 18 | ELI-03: Error sanitization, _internal stripping, anti-jargon, sanitizeResponse |
| `tool-implementations.test.ts` | `src/__tests__/integrations/bestbarbers/` | 12 | ELI-01: service_name resolution in check_availability & create_appointment |
| `eli05-subscriber-check.test.ts` | `src/__tests__/integrations/bestbarbers/` | 7 | ELI-05: Proactive subscriber check in create_appointment |
| `prompt-builder.test.ts` | `src/__tests__/agents/` | 19 | Prompt structure, rules, flows |
| `agent-pipeline.test.ts` | `src/__tests__/agents/` | 5 | Agent pipeline priority gates, step independence |
| `server.test.ts` | `src/__tests__/mcp/` | 21 | MCP server: 7 tool registrations, tenant isolation |
| `pulse-agent.test.ts` | `src/__tests__/agents/` | 6 | Rate limiting, action types, inactive client detection |

**Subtotal: 97 test cases directly related to Eli/tools architecture.**

### 1.3 Tools With Tests vs Without Tests

| Tool | Has Unit Tests | Has Integration Tests | Notes |
|------|:-:|:-:|-------|
| `get_contact_info` | NO | NO | Only tested as circuit breaker target (mock). No functional test of the actual implementation. |
| `add_tag` | NO | NO | Only tested as circuit breaker target (mock). Implementation in aria-tools.ts untested. |
| `move_pipeline_stage` | NO | NO | Implementation in aria-tools.ts untested. MCP `move_pipeline` tested separately. |
| `add_internal_note` | NO | NO | Implementation in aria-tools.ts untested. Used in circuit breaker tests only as side effect. |
| `transfer_to_human` | NO | NO | Implementation in aria-tools.ts untested (659 lines total, zero direct coverage). |
| `search_knowledge_base` | NO | NO | Implementation in aria-tools.ts untested. |
| `get_services` | NO | NO | Only indirectly tested (mocked in ELI-01 tests for service resolution). |
| `check_availability` | YES | NO | 6 tests via ELI-01 (service_name resolution focus). |
| `get_subscriber_status` | PARTIAL | NO | 1 test for HTTP failure case (ELI-03). 0 happy path tests as standalone. |
| `get_appointment_history` | NO | NO | Zero tests. |
| `create_appointment` | YES | NO | 9 tests across ELI-01 + ELI-05 (service_name, subscriber enrichment). |
| `cancel_appointment` | NO | NO | Zero tests. |
| `reschedule_appointment` | NO | NO | Zero tests. |
| `getToolsForOrg` | PARTIAL | NO | Mocked in circuit breaker tests. Dynamic loading logic untested. |
| `executeToolCall` (dispatcher) | PARTIAL | NO | Tested through circuit breaker flow. Routing logic for all tools untested. |

**Finding: 6 of 6 core tools in `aria-tools.ts` have ZERO direct functional tests. 4 of 7 BestBarbers tools have ZERO tests. This is the single biggest coverage gap.**

### 1.4 Tests That Need Updates When New Tools Are Added

| Test File | Required Updates | Reason |
|-----------|-----------------|--------|
| `circuit-breaker.test.ts` | Add new tool names to `getToolsForOrg` mock | New tools must participate in circuit breaker tracking |
| `eli03-error-classification.test.ts` | Add error format tests for each new tool | Verify _internal/_context pattern for new tools |
| `prompt-builder.test.ts` | Add prompt references for new tools | Verify prompt mentions new tools by name |
| `server.test.ts` | Update tool count assertion (line: `expect(Object.keys(toolHandlers)).toHaveLength(7)`) | If any MCP tools are bridged to Eli |

---

## 2. Test Scenarios per New Tool

### 2.1 `schedule_followup` (GAP-01 -- CRITICAL)

**Risk Level: HIGH** -- This tool bridges Eli conversations to BullMQ job queue. Incorrect scheduling could spam contacts or create orphaned jobs.

#### Unit Tests (8 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: schedule 30min followup | happy | Enqueue BullMQ job with correct delay, message_hint, followup_type="curiosity" |
| 2 | Happy path: schedule 24h followup | happy | delay_minutes=1440, verify job data |
| 3 | Happy path: schedule 72h followup | happy | delay_minutes=4320, type="farewell" |
| 4 | Error: exceed max followups per contact | error | Contact already has 3 pending followups, reject with user-friendly error |
| 5 | Error: invalid delay_minutes | error | Negative number, zero, or >10080 (1 week) should be rejected |
| 6 | Error: BullMQ connection failure | error | Queue.add() throws, return error with _internal detail |
| 7 | Edge: duplicate prevention | edge | Same contact + same followup_type within 1h window should deduplicate |
| 8 | Edge: contact opted out | edge | If contact has opted out of messaging, reject followup |

#### Mock Requirements
- BullMQ `Queue` class (add, getJobs, obliterate)
- DB client for contact opt-out status lookup
- DB client for counting existing pending followups

#### Integration Test (1 test)
- Verify job appears in BullMQ queue with correct delay and is picked up by Pulse processor

#### ELI-03 Compliance (2 tests)
- Error returns `_internal` field with technical details
- Error message is user-friendly (no queue IDs, no BullMQ references)

**Total: 11 tests**

---

### 2.2 `remove_tag` (GAP-03 -- HIGH)

**Risk Level: LOW** -- Mirror of `add_tag`. Simple DB operation.

#### Unit Tests (5 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: remove existing tag | happy | Tag exists on contact, remove it, return success |
| 2 | Error: tag not found on contact | error | Tag exists but not assigned to this contact |
| 3 | Error: tag name does not exist | error | No tag with that name in the org |
| 4 | Error: contactId is null | error | Return "Contato nao identificado" |
| 5 | Edge: empty tag_name | edge | Reject empty/whitespace-only input |

#### Mock Requirements
- `db.tag.findUnique` / `db.contactTag.findUnique` / `db.contactTag.delete`

#### ELI-03 Compliance (1 test)
- Verify error format consistency

**Total: 6 tests**

---

### 2.3 `update_contact` (GAP-04 -- HIGH)

**Risk Level: MEDIUM** -- Must restrict updatable fields (only name, email). Incorrect implementation could corrupt phone numbers or org membership.

#### Unit Tests (8 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: update name | happy | Update contact name, return success with old/new values |
| 2 | Happy path: update email | happy | Update contact email |
| 3 | Happy path: update both name and email | happy | Both fields in one call |
| 4 | Error: attempt to update phone | error | Reject with "campo nao permitido" |
| 5 | Error: attempt to update organizationId | error | Reject forbidden field |
| 6 | Error: contactId is null | error | Standard contact guard |
| 7 | Edge: empty name | edge | Reject empty/whitespace name |
| 8 | Edge: invalid email format | edge | Basic email validation |

#### Mock Requirements
- `db.contact.update` with field-level validation

#### Guardrail Tests (2 tests)
- Verify field whitelist enforcement (only `name`, `email` accepted)
- Verify audit trail (internal note created on contact update)

**Total: 10 tests**

---

### 2.4 `list_pipeline_stages` (GAP-05 -- HIGH)

**Risk Level: LOW** -- Read-only query. No side effects.

#### Unit Tests (4 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: return stages grouped by pipeline | happy | Returns `[{ name, pipeline_name }]` |
| 2 | Happy path: multiple pipelines | happy | Org has 2+ pipelines, all stages returned |
| 3 | Error: no pipelines configured | error | Return empty array with informative message |
| 4 | Error: DB failure | error | Graceful error with _internal |

#### Mock Requirements
- `db.pipelineStage.findMany` with pipeline include

**Total: 4 tests**

---

### 2.5 `trigger_flow` (GAP-06 -- HIGH)

**Risk Level: CRITICAL** -- Can trigger expensive automation flows. LLM misuse could fire onboarding or billing flows on wrong contacts.

#### Unit Tests (8 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: trigger whitelisted flow | happy | Flow is PUBLISHED and in whitelist, trigger succeeds |
| 2 | Error: flow not in whitelist | error | Reject with list of allowed flows |
| 3 | Error: flow not published | error | DRAFT flow rejected |
| 4 | Error: flow not found | error | Return "fluxo nao encontrado" |
| 5 | Error: contact has no phone | error | Cannot trigger flow without phone |
| 6 | Error: no WhatsApp channel | error | Cannot trigger flow without active channel |
| 7 | Edge: rate limit | edge | Same flow for same contact within 24h should be blocked |
| 8 | Edge: concurrent trigger prevention | edge | Two simultaneous triggers for same contact should only execute once |

#### Mock Requirements
- `db.flow.findUnique` (status, name)
- `db.contact.findUnique` (phone)
- `db.channel.findFirst` (WhatsApp channel)
- `executeFlowById` function
- Flow whitelist configuration

#### Guardrail Tests (3 tests)
- Whitelist enforcement (only pre-approved flow IDs accepted)
- Rate limiting (max 1 trigger per flow per contact per 24h)
- Audit trail (internal note created when flow triggered)

**Total: 11 tests**

---

### 2.6 `get_business_hours` (GAP-07 -- MEDIUM)

**Risk Level: LOW** -- Read-only. Already a table in the DB (`businessHours`).

#### Unit Tests (4 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: return business hours for each day | happy | Returns structured hours per weekday |
| 2 | Happy path: handle closed days | happy | Some days have no hours (closed), return `closed: true` |
| 3 | Error: no business hours configured | error | Return default message |
| 4 | Edge: timezone handling | edge | Hours should be returned in org timezone |

**Total: 4 tests**

---

### 2.7 `get_subscription_plans` (GAP-13 -- LOW, but recommended)

**Risk Level: LOW** -- Read-only. Eliminates hardcoded prices in prompt.

#### Unit Tests (4 tests)

| # | Scenario | Type | Description |
|---|----------|------|-------------|
| 1 | Happy path: return all active plans with prices | happy | Fetch from BestBarbers API, return `[{ name, price, features }]` |
| 2 | Error: API unavailable | error | Graceful fallback (return cached or empty) |
| 3 | Edge: caching | edge | Second call within TTL returns cached data |
| 4 | Edge: empty plan list | edge | Org has no subscription plans configured |

**Total: 4 tests**

---

## 3. Tests Required for Existing Untested Tools

Before adding new tools, the following existing tool implementations in `aria-tools.ts` (659 lines) have ZERO direct test coverage and should be addressed:

### 3.1 Core Tools Coverage Gap (Backlog)

| Tool | Tests Needed | Priority |
|------|-------------|----------|
| `get_contact_info` | 4 (happy, no contactId, contact not found, DB error) | HIGH |
| `add_tag` | 5 (happy, already exists, create new tag, no contactId, empty name) | HIGH |
| `move_pipeline_stage` | 5 (happy move, happy create, stage not found, no contactId, empty name) | MEDIUM |
| `add_internal_note` | 3 (happy, empty content, no conversationId) | MEDIUM |
| `transfer_to_human` | 4 (happy with online agent, happy without agent, empty reason, DB error) | HIGH |
| `search_knowledge_base` | 4 (happy with results, no results, empty query, DB error) | MEDIUM |
| `executeToolCall` dispatch | 3 (core tool routing, BB tool routing, unknown tool) | HIGH |
| `getToolsForOrg` dynamic load | 3 (core only, core+BB, DB error fallback) | MEDIUM |

**Total backlog: 31 tests for existing untested tools.**

### 3.2 BestBarbers Tools Coverage Gap

| Tool | Tests Needed | Priority |
|------|-------------|----------|
| `get_services` | 3 (happy, empty services, API error) | MEDIUM |
| `get_appointment_history` | 4 (happy with visits, no visits, contact not found, API error) | HIGH |
| `cancel_appointment` | 5 (happy with ID, happy auto-resolve, no upcoming, invalid ID, API error) | HIGH |
| `reschedule_appointment` | 6 (happy, slot unavailable, invalid date, old appt not found, API error, available_slots in error) | HIGH |
| `get_subscriber_status` | 3 (happy subscriber, non-subscriber, phone normalization) | MEDIUM |

**Total backlog: 21 tests for existing untested BB tools.**

---

## 4. Risk Matrix

### 4.1 New Tools Risk Assessment

| Tool | Probability of Failure | Impact if Failure | Risk Score | Risk Level | Primary Risk |
|------|:---:|:---:|:---:|:---:|------|
| `schedule_followup` | HIGH | HIGH | 9 | **CRITICAL** | BullMQ integration failures, spam if guardrails fail, orphaned jobs |
| `trigger_flow` | MEDIUM | CRITICAL | 9 | **CRITICAL** | Wrong flow triggered, costly automations, billing side-effects |
| `update_contact` | MEDIUM | HIGH | 6 | **HIGH** | Field restriction bypass could corrupt contact data |
| `remove_tag` | LOW | LOW | 1 | **LOW** | Simple CRUD, mirror of tested add_tag |
| `list_pipeline_stages` | LOW | LOW | 1 | **LOW** | Read-only, no side effects |
| `get_business_hours` | LOW | MEDIUM | 2 | **LOW** | Read-only, but wrong hours could mislead clients |
| `get_subscription_plans` | LOW | MEDIUM | 2 | **LOW** | Read-only, API dependency |

### 4.2 Side Effect Analysis (Dangerous Tools)

| Tool | Side Effects | Danger Level | Mitigation |
|------|-------------|:---:|------------|
| `schedule_followup` | Creates BullMQ job that sends WhatsApp message after delay | CRITICAL | Max 3 followups per contact, dedup window, opt-out check |
| `trigger_flow` | Executes full automation flow (multi-step, may send messages, update data) | CRITICAL | Flow whitelist, rate limit per contact, PUBLISHED-only gate |
| `update_contact` | Modifies contact record permanently | HIGH | Field whitelist (name/email only), audit trail via internal note |
| `remove_tag` | Deletes tag association | LOW | None needed beyond basic validation |

---

## 5. Guardrail Recommendations

### 5.1 `schedule_followup` Guardrails

| # | Guardrail | Implementation | Priority |
|---|-----------|---------------|:---:|
| G1 | Max 3 pending followups per contact | Check `queue.getJobs('delayed')` filtered by contactId before enqueue | MUST |
| G2 | Deduplication window (1h) | If same contactId + followup_type exists within last 60min, reject | MUST |
| G3 | Opt-out check | Query contact opt-out status before scheduling | MUST |
| G4 | Valid delay_minutes range | Accept only: 30, 1440, 4320 (or configurable whitelist) | SHOULD |
| G5 | Anti-ban coordination | New followup jobs must go through antiban pipeline (rate limits, presence) | MUST |
| G6 | Audit trail | Log scheduled followup in conversation internal notes | SHOULD |

### 5.2 `trigger_flow` Guardrails

| # | Guardrail | Implementation | Priority |
|---|-----------|---------------|:---:|
| G7 | Flow whitelist | Only pre-approved flow IDs accepted (config/DB driven, not hardcoded) | MUST |
| G8 | PUBLISHED-only gate | Reject DRAFT/ARCHIVED flows | MUST |
| G9 | Rate limit: 1 trigger per flow per contact per 24h | Check recent flow execution log | MUST |
| G10 | Contact phone validation | Contact must have valid phone to receive flow messages | MUST |
| G11 | Channel availability | Active WhatsApp channel must exist | MUST |
| G12 | Audit trail | Internal note + decision log for every flow trigger | MUST |

### 5.3 `update_contact` Guardrails

| # | Guardrail | Implementation | Priority |
|---|-----------|---------------|:---:|
| G13 | Field whitelist | ONLY `name` and `email` accepted. Reject any other field. | MUST |
| G14 | Validation: name | Non-empty, max 200 chars, no script injection | MUST |
| G15 | Validation: email | Basic format check (contains @, valid domain) | SHOULD |
| G16 | Audit trail | Internal note with old/new values on every update | MUST |

---

## 6. Test Estimation Summary

### 6.1 New Tools

| Tool | Unit | Integration | ELI-03 | Guardrail | Total |
|------|:---:|:---:|:---:|:---:|:---:|
| `schedule_followup` | 8 | 1 | 2 | (included in unit) | **11** |
| `remove_tag` | 5 | 0 | 1 | 0 | **6** |
| `update_contact` | 8 | 0 | 0 | 2 | **10** |
| `list_pipeline_stages` | 4 | 0 | 0 | 0 | **4** |
| `trigger_flow` | 8 | 0 | 0 | 3 | **11** |
| `get_business_hours` | 4 | 0 | 0 | 0 | **4** |
| `get_subscription_plans` | 4 | 0 | 0 | 0 | **4** |
| **Subtotal** | **41** | **1** | **3** | **5** | **50** |

### 6.2 Existing Coverage Backlog

| Area | Tests Needed |
|------|:---:|
| Core tools (aria-tools.ts) | 31 |
| BestBarbers untested tools | 21 |
| **Subtotal** | **52** |

### 6.3 Regression / Update Existing Tests

| Area | Tests to Update |
|------|:---:|
| circuit-breaker.test.ts (mock updates) | 2-3 adjustments |
| eli03-error-classification.test.ts (new tool errors) | 3-4 new cases |
| prompt-builder.test.ts (new tool references) | 3-4 new cases |
| server.test.ts (if MCP bridging) | 1-2 adjustments |
| **Subtotal** | **~10** |

### 6.4 Grand Total

| Category | Test Count |
|----------|:---------:|
| New tool tests | 50 |
| Existing coverage backlog | 52 |
| Regression updates | ~10 |
| **GRAND TOTAL** | **~112** |

Current test count: 407. After full implementation: **~519 tests**.

---

## 7. Testing Pattern Reference

All new tests MUST follow the established patterns observed in the codebase:

### 7.1 File Structure

```
src/__tests__/
  ai/                          # Core AI tests (error classification, etc.)
  agents/                      # Agent-level tests (circuit breaker, pipeline)
  integrations/bestbarbers/    # BestBarbers tool tests
  mcp/                         # MCP server tests
```

**New tool test locations:**
- `remove_tag`, `update_contact`, `list_pipeline_stages` --> `src/__tests__/ai/core-tools.test.ts` (NEW)
- `schedule_followup` --> `src/__tests__/agents/schedule-followup.test.ts` (NEW)
- `trigger_flow` (Eli-side) --> `src/__tests__/ai/trigger-flow.test.ts` (NEW)
- `get_business_hours` --> `src/__tests__/integrations/bestbarbers/get-business-hours.test.ts` (NEW)
- `get_subscription_plans` --> `src/__tests__/integrations/bestbarbers/get-subscription-plans.test.ts` (NEW)

### 7.2 Mock Pattern (from circuit-breaker.test.ts)

```typescript
// 1. Mock all heavy dependencies BEFORE imports
vi.mock("@/lib/db", () => ({
  createTenantClient: vi.fn(() => mockDbClient),
}));

// 2. Define mock DB client with all methods
const mockDbClient = {
  contact: { findUnique: vi.fn(), update: vi.fn() },
  tag: { findUnique: vi.fn(), create: vi.fn() },
  contactTag: { findUnique: vi.fn(), create: vi.fn(), delete: vi.fn() },
  // ... etc
};

// 3. Import AFTER mocks
import { executeToolCall } from "@/lib/ai/aria-tools";

// 4. Reset mocks in beforeEach
beforeEach(() => {
  vi.clearAllMocks();
});
```

### 7.3 ELI-03 Error Format Pattern

Every tool error MUST be tested for:
```typescript
// Error is user-friendly
expect(data.error).toBeDefined();
expect(data.error).not.toMatch(/HTTP/i);
expect(data.error).not.toMatch(/\bID\b/);
expect(data.error).not.toMatch(/status code/i);

// Technical details in _internal
expect(data._internal).toBeDefined();
```

### 7.4 Circuit Breaker Integration Pattern

New tools must be added to the `getToolsForOrg` mock in `circuit-breaker.test.ts`:
```typescript
vi.mock("@/lib/ai/aria-tools", () => ({
  getToolsForOrg: vi.fn().mockResolvedValue([
    // ... existing tools ...
    { type: "function", function: { name: "remove_tag", ... } },
    { type: "function", function: { name: "update_contact", ... } },
  ]),
}));
```

---

## 8. Implementation Priority

| Phase | Tools | Tests | Rationale |
|:---:|-------|:---:|-----------|
| **Phase 0** | Backlog: core tools (aria-tools.ts) | 31 | Must establish coverage before adding new tools |
| **Phase 1** | `remove_tag`, `update_contact`, `list_pipeline_stages` | 20 | Low risk, high value, no external dependencies |
| **Phase 2** | `get_business_hours`, `get_subscription_plans` | 8 | Medium priority, read-only |
| **Phase 3** | `schedule_followup` | 11 | High risk, requires BullMQ integration |
| **Phase 4** | `trigger_flow` | 11 | Highest risk, requires flow whitelist infrastructure |
| **Phase 5** | Backlog: BB untested tools | 21 | Fill remaining coverage gaps |

---

## 9. Quality Gate Criteria for New Tool Stories

Each new tool story MUST meet these criteria before QA approval:

1. **All unit tests passing** -- zero failures, zero skips
2. **ELI-03 compliance** -- every error path returns `_internal` field, user-facing error is jargon-free
3. **Circuit breaker integration** -- tool participates in per-tool and global failure tracking
4. **Guardrails implemented** -- all MUST-priority guardrails for that tool are coded and tested
5. **Prompt updated** -- `prompt-builder.ts` explicitly names the new tool in relevant flow sections
6. **Response sanitization** -- `sanitizeResponse` regex patterns updated if tool introduces new technical identifiers
7. **No regression** -- all 407 existing tests still pass

---

*-- Quinn, guardiao da qualidade*
