# Tikso CRM - Contact Detail Sidebar QA Audit

**Date:** 2026-02-25
**Auditor:** Quinn (Guardian) - QA Agent
**Scope:** Inbox contact detail sidebar panel (`ContactPanel` component and all sub-components)
**Server:** Vultr (`/home/tikso/tikso/`)
**Verdict:** NEEDS_WORK (7 issues found, 1 CRITICAL, 2 HIGH, 4 MEDIUM)

---

## 1. Component Architecture

The sidebar is composed of a parent component and 9 sub-sections:

| # | Section | Component | File |
|---|---------|-----------|------|
| 1 | Profile Header | `ProfileHeader` | `src/components/inbox/contact-panel.tsx` (inline) |
| 2 | Contact Info | `ContactInfoCard` | `src/components/contacts/shared/contact-info-card.tsx` |
| 3 | Quick Actions | `QuickActions` + `QuickActionsSection` | `src/components/contacts/shared/quick-actions.tsx` + inline |
| 4 | Assignment + Journey | `AssignmentJourneySection` | inline |
| 5 | Tags | `TagsSection` | inline, delegates to `TagList` |
| 6 | Notes | `UnifiedNotesSection` -> `NotesSection` | `src/components/contacts/shared/notes-section.tsx` |
| 7 | AI Insights | `ConversationInsight` | `src/components/inbox/conversation-insight.tsx` |
| 8 | Commitments | `CommitmentsSection` | inline |
| 9 | Activity + Stats | `ActivitySubSection` + `StatsBar` | inline |

**Parent orchestration:** `InboxLayout` (`src/components/inbox/inbox-layout.tsx`) manages state and passes callbacks. ContactPanel is a presentational component with ~1433 lines.

**Server actions:** `src/app/(app)/[orgId]/inbox/actions.ts` (primary), `src/app/(app)/[orgId]/ai/actions.ts` (journey), `src/app/api/inbox/notes/route.ts` (note CRUD via REST).

---

## 2. Functional Completeness Assessment

### FULLY FUNCTIONAL (working with proper error handling)

| Feature | Verdict | Evidence |
|---------|---------|----------|
| **Profile display** (avatar, initials, name, badges) | PASS | Correctly computes initials via `.split(" ").map(n => n[0]).join("").slice(0, 2)`. Handles avatarUrl null. |
| **Inline name editing** | PASS | Full flow: click to edit, Enter to save, Escape to cancel. Validates trimmed value. Shows loader during save. Reverts on error with `toast.error`. |
| **Contact info display** (phone, email, date) | PASS | Handles null phone/email with "Nao informado" text. Date formatted via `date-fns` with `ptBR` locale. Copy-to-clipboard with visual feedback (Check icon for 2s). |
| **Close conversation** | PASS | Delegates to `InboxLayout.handleCloseConversation`. Updates conversation status optimistically. Fires default close flow non-blocking. |
| **Trigger flow** | PASS | Lazy-loads published flows on first click. Validates flow exists, is published, has nodes, channel is connected, phone exists. Fire-and-forget execution. Per-flow loading indicator. |
| **Toggle automation (Pause/Resume)** | PASS | Toggles `automationPaused` via `updateContact`. Updates local state on success. Button text changes between "Pausar" and "Retomar". |
| **Assignment dropdown** | PASS | Shows all team members with avatars and presence indicators. Supports unassign (null). Checkmark on current assignee. Separate "Remover" button when assigned. |
| **Journey state display + change** | PASS | Loads asynchronously with proper `cancelled` flag in useEffect cleanup. Dropdown to change state. Shows mini timeline of last 3 transitions with relative dates. Loading skeleton during fetch. |
| **Tags display + add/remove** | PASS | Optimistic add with rollback on failure. Remove via `TagList` editable mode. Dropdown filters out already-assigned tags. Shows "Nenhuma tag disponivel" when all tags assigned. |
| **Personal notes (observation)** | PASS | Auto-save with 1-second debounce. Saves on blur. Loading indicator during save. Error toast on failure. |
| **Team notes (internal notes)** | PARTIAL | Add works (server action). Display works. **Delete is BROKEN** (see BUG-001). Ctrl/Cmd+Enter shortcut to submit. |
| **AI Insights (DNA)** | PASS | Fetches insight on mount with cleanup. Real-time updates via Centrifugo subscription. Gracefully hides when no data or default values. Displays sentiment, intent, urgency, topics, buying signals, suggested action. |
| **Commitments** | PASS | CRUD via handoff service. Add with Enter key. Status transitions (pending/fulfilled/broken) with per-item loading state. Due date display. Visual styling per status. |
| **Activity section** | PASS | Collapsible (defaultOpen=false). Shows sequences, campaigns, custom fields, pipeline cards. Each with empty state. |
| **Stats bar** | PASS | Last message time with relative formatting (m/h/d/dd-MM). Lead score with fallback to 0. |
| **Loading skeleton** | PASS | Full skeleton layout matching real content structure. |

---

## 3. CONFIRMED BUGS

### BUG-001 [CRITICAL]: Note Deletion Endpoint Missing

**Location:** `src/app/api/inbox/notes/route.ts`

The `UnifiedNotesSection` component calls `DELETE /api/inbox/notes?noteId={id}` to delete internal notes:

```typescript
// contact-panel.tsx line ~1040
const handleDeleteNote = React.useCallback(async (noteId: string) => {
  try {
    const res = await fetch(`/api/inbox/notes?noteId=${noteId}`, { method: "DELETE" });
    if (res.ok) {
      setInternalNotes((prev) => prev.filter((n) => n.id !== noteId));
    } else {
      throw new Error("Failed");
    }
  } catch {
    toast.error("Erro ao excluir nota");
  }
}, []);
```

However, the API route at `src/app/api/inbox/notes/route.ts` only exports `POST` and `GET` handlers. There is **no `DELETE` export**. This means:

- Every delete attempt returns **405 Method Not Allowed**
- The catch block shows "Erro ao excluir nota" toast
- The note remains in the database but appears to be removed from UI briefly (no -- it checks `res.ok` which is false, so the note stays in the list)
- Actually, the note is NOT removed from the list because the `res.ok` check prevents the optimistic removal

**Impact:** Users cannot delete any internal notes. The delete button (trash icon) is visible on hover but always fails silently with a toast error.

**Fix required:** Add a `DELETE` handler to `src/app/api/inbox/notes/route.ts` with proper auth, org access verification, and authorization check (only note author or admin should delete).

---

### BUG-002 [HIGH]: Direct Mutation of Contact Object

**Location:** `src/components/inbox/contact-panel.tsx`, `ProfileHeader` callback

```typescript
<ProfileHeader
  contact={contact}
  orgId={orgId}
  onNameUpdated={(newName) => {
    if (contact) contact.name = newName;  // DIRECT MUTATION
  }}
/>
```

This directly mutates the `contact` prop object instead of using React state updates. Because the `contact` object reference does not change, child components that depend on `contact.name` will not re-render. The name appears to update in the `ProfileHeader` only because it manages its own `editName` state, but:

1. The `ContactInfoCard` further down the sidebar will display the OLD name until the panel is re-opened
2. This violates React's immutability principle
3. The `InboxLayout` parent's `contact` state object is mutated in place, which could cause stale closures in other callbacks

**Fix required:** The `onNameUpdated` callback should call a proper state setter in `InboxLayout`, similar to how `handleUpdateNotes` works:

```typescript
onNameUpdated={(newName) => {
  setContact((prev) => prev ? { ...prev, name: newName } : null);
}}
```

---

### BUG-003 [HIGH]: Journey State Update Permission Mismatch

**Location:** `src/app/(app)/[orgId]/ai/actions.ts`, line ~351

The `updateJourneyState` server action requires `"integrations"` permission:

```typescript
assertMemberPermission(member, "integrations");
```

However, the sidebar is used by live chat agents who have `"liveChat"` permission. A regular agent who can view the sidebar, assign conversations, close them, and manage tags will get a **403 error** when trying to change a contact's journey state because they lack the `"integrations"` permission.

This creates a confusing UX where the "Alterar" button is visible and clickable, but the action fails with "Erro ao atualizar estado" for most users.

**Fix required:** Either:
- Change the permission to `"liveChat"` (if agents should be able to change journey state)
- Or hide the "Alterar" button when the user lacks the required permission (pass permission info as prop)

---

## 4. POTENTIAL ISSUES

### ISSUE-001 [MEDIUM]: Missing Error State for getInternalNotes

**Location:** `src/components/inbox/contact-panel.tsx`, `UnifiedNotesSection`

The internal notes fetch has a `.catch(() => {})` that silently swallows errors:

```typescript
getInternalNotes(orgId, conversationId)
  .then((data) => { /* ... */ })
  .catch(() => {})  // Silent failure
  .finally(() => setIsLoadingNotes(false));
```

If the server action fails (network error, auth expired, etc.), the user sees an empty notes list with "Nenhuma nota adicionada" instead of an error indicator. There is no way to retry without navigating away and back.

**Impact:** Low-moderate. Notes may silently fail to load with no user feedback.

**Recommendation:** Add an error state and a retry mechanism, similar to how `ContactDrawer` handles `loadError`.

---

### ISSUE-002 [MEDIUM]: Missing Error State for getCommitments

**Location:** `src/components/inbox/contact-panel.tsx`, `CommitmentsSection`

Same pattern as ISSUE-001. The commitments fetch silently swallows errors:

```typescript
getCommitments(orgId, conversationId)
  .then((data) => setCommitments(data))
  .catch(() => {})  // Silent failure
  .finally(() => setIsLoading(false));
```

Users see "Nenhum compromisso registrado" on fetch failure, indistinguishable from a genuinely empty list.

---

### ISSUE-003 [MEDIUM]: Flow Picker Silent Error on Load

**Location:** `src/components/inbox/contact-panel.tsx`, `QuickActionsSection`

```typescript
const loadFlows = React.useCallback(async () => {
  if (hasFetched) return;
  setIsLoadingFlows(true);
  try {
    const data = await getFlows(orgId);
    setFlows(data);
    setHasFetched(true);
  } catch {
    // silent
  } finally {
    setIsLoadingFlows(false);
  }
}, [orgId, hasFetched]);
```

The `catch` is explicitly labeled `// silent`. If flows fail to load:
- `hasFetched` stays `false`, so the loading spinner is shown perpetually on next click
- Actually no -- `finally` sets `isLoadingFlows` to `false`, but since `hasFetched` is still `false`, subsequent clicks will re-fetch (which is actually a reasonable retry strategy)
- However, the user sees "Nenhum fluxo publicado" (empty state from `flows.length === 0`) with no indication that it was an error

**Impact:** Low. The retry-on-click behavior is acceptable, but an error indicator would improve UX.

---

### ISSUE-004 [MEDIUM]: No Input Validation on Commitment Description

**Location:** `src/components/inbox/contact-panel.tsx`, `CommitmentsSection`

The commitment description input has no length limit:

```typescript
<input
  type="text"
  value={newDescription}
  onChange={(e) => setNewDescription(e.target.value)}
  // No maxLength
  placeholder="Adicionar compromisso..."
/>
```

The server-side `addCommitment` also does not validate description length. A user could submit an extremely long description that would break the UI layout.

Compare with `sendMessageSchema` which has `.max(10000)` -- no equivalent validation exists for commitments.

**Recommendation:** Add `maxLength={500}` to the input and server-side validation.

---

## 5. Edge Case Analysis

### Handled Correctly

| Edge Case | Handling |
|-----------|----------|
| Contact with no phone | Shows "Nao informado" in italics |
| Contact with no email | Shows "Nao informado" in italics |
| Contact with no avatar | Shows initials in fallback |
| Contact with single-word name | `split(" ").map(n => n[0]).join("").slice(0, 2)` produces single char -- acceptable |
| Contact with no tags | Shows "Nenhuma tag adicionada" empty state |
| Contact with no sequences/campaigns/pipeline | Each sub-section shows empty state text |
| Contact with no lead score | Falls back to `0` in StatsBar |
| Contact with no lastSeenAt | Shows "N/A" in StatsBar |
| Contact with no journey data | Shows "Desconhecido" (UNKNOWN state default) |
| No conversationId | Insight section shows "Selecione uma conversa para ver insights" |
| Journey with no transitions | Timeline simply not rendered |
| All tags already assigned | Dropdown shows "Nenhuma tag disponivel" |
| Panel closed | Returns `null` early, no rendering |

### NOT Handled

| Edge Case | Risk |
|-----------|------|
| Very long contact name (50+ chars) | Name editing input has no max-width constraint; could overflow the 320px panel. The display mode uses `text-sm font-bold` without `truncate`. |
| Very long tag name | `TagList` does not truncate tag text. A tag named "Clientes-potenciais-do-evento-de-marco-2026" would break layout. |
| Rapid assignment changes | No debounce on `onAssign`. Clicking multiple team members quickly could cause race conditions between server calls and optimistic updates. |
| Concurrent editors | If two agents view the same contact's sidebar and both edit the name or notes simultaneously, the last write wins with no conflict detection. |
| Large number of tags (50+) | The tag dropdown has no virtualization or scroll limit. |
| Large number of commitments | No pagination or virtualization; all commitments render at once. |
| Network disconnect during debounced note save | The observation auto-save fires 1s after typing. If the network drops during that window, the error toast fires but the user's text remains in the input, creating a false sense of saved state. The `lastSavedObs` tracker prevents re-save attempts of the same value, which is correct. |

---

## 6. Security Assessment

| Check | Status | Notes |
|-------|--------|-------|
| Auth on all server actions | PASS | All actions call `requireOrgAccess()` and `assertMemberPermission()` |
| Tenant isolation | PASS | Uses `createTenantClient(orgId)` for Prisma queries |
| Input sanitization | PARTIAL | Zod validation only on `sendMessage`. No validation on note content, commitment description, contact name. XSS risk is mitigated by React's default escaping. |
| CSRF protection | PASS | Server actions use Next.js built-in CSRF protection |
| Authorization on note delete | FAIL | No DELETE handler exists (BUG-001). When implemented, must verify the user is the note author or has admin permissions. |
| Permission on journey change | CONCERN | Uses `"integrations"` permission instead of `"liveChat"` (BUG-003) |

---

## 7. Test Coverage Assessment

**Current test coverage for sidebar components: ZERO**

Files searched:
- `src/__tests__/` -- 21 test files found, NONE related to inbox sidebar, contact panel, or shared components
- No test files match patterns: `contact-panel`, `ContactPanel`, `contact-drawer`, `ContactDrawer`, `sidebar`, `quick-actions`, `notes-section`, `tag-list`, `contact-info-card`, `section-header`

**Test gap by component:**

| Component | Lines of Code | Tests | Priority |
|-----------|--------------|-------|----------|
| `contact-panel.tsx` | 1433 | 0 | HIGH |
| `inbox-layout.tsx` (callbacks) | ~200 relevant | 0 | HIGH |
| `notes-section.tsx` | ~130 | 0 | HIGH (debounce, tabs) |
| `conversation-insight.tsx` | ~170 | 0 | MEDIUM (real-time) |
| `contact-info-card.tsx` | ~150 | 0 | LOW (presentational) |
| `quick-actions.tsx` | ~80 | 0 | LOW (presentational) |
| `tag-list.tsx` | ~90 | 0 | LOW (presentational) |
| `section-header.tsx` | ~100 | 0 | LOW (presentational) |
| Server actions (sidebar-related) | ~300 | 0 | CRITICAL |

**Recommended test plan (priority order):**

1. **Server action unit tests** -- `updateContact`, `addTag`, `removeTag`, `assignConversation`, `getContactDetails`, `getInternalNotes`, `addInternalNote`, `getCommitments`, `addCommitment`, `updateCommitmentStatus`, `getJourneyInfo`, `updateJourneyState`, `triggerFlow`
2. **NotesSection** -- debounce behavior, tab switching, add/delete flows
3. **CommitmentsSection** -- add, status transitions, keyboard submit
4. **ProfileHeader** -- inline edit, save, cancel, escape key
5. **QuickActionsSection** -- flow picker lazy load, trigger flow
6. **AssignmentJourneySection** -- assign/unassign, journey state change
7. **TagsSection** -- add with optimistic update + rollback, remove

---

## 8. Summary of Findings

### By Severity

| ID | Severity | Type | Summary |
|----|----------|------|---------|
| BUG-001 | CRITICAL | Bug | Note deletion API endpoint (DELETE handler) is missing entirely |
| BUG-002 | HIGH | Bug | Direct mutation of contact prop object in onNameUpdated callback |
| BUG-003 | HIGH | Bug | Journey state update requires "integrations" permission but sidebar users have "liveChat" |
| ISSUE-001 | MEDIUM | Missing Error State | Internal notes fetch failure is silent |
| ISSUE-002 | MEDIUM | Missing Error State | Commitments fetch failure is silent |
| ISSUE-003 | MEDIUM | Missing Error State | Flow list fetch failure is silent |
| ISSUE-004 | MEDIUM | Missing Validation | No length limit on commitment description input |

### Positive Findings

1. **Solid error handling pattern** in most server actions -- consistent `{ success, error }` return type
2. **Proper auth/permission checks** on every server action
3. **Tenant isolation** is correctly implemented via `createTenantClient`
4. **Optimistic updates with rollback** on tag operations -- well-implemented pattern
5. **useEffect cleanup** with `cancelled` flag on journey info fetch -- prevents race conditions
6. **Real-time updates** on conversation insights via Centrifugo -- properly subscribes/unsubscribes
7. **Loading skeletons** match the actual content layout
8. **Comprehensive empty states** for every data section
9. **Keyboard accessibility** -- Enter to save name, Enter to add commitment, Ctrl/Cmd+Enter for notes, Escape to cancel

---

## 9. Gate Decision

**NEEDS_WORK**

The sidebar is feature-rich and mostly well-implemented. However, BUG-001 (missing DELETE endpoint for notes) is a CRITICAL functional gap that affects a visible user feature. BUG-002 (prop mutation) is a correctness issue that could cause subtle rendering bugs. BUG-003 (permission mismatch) will cause 403 errors for most sidebar users attempting to change journey state.

These three issues should be resolved before considering the sidebar production-ready. The MEDIUM issues and test coverage gaps are important but can be addressed as follow-up work.

---

*-- Quinn, guardiao da qualidade*
