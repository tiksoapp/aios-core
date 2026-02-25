# Tikso CRM -- Contact Detail Sidebar Architecture Audit

**Author:** Aria (Architect Agent)
**Date:** 2026-02-25
**Scope:** Inbox view contact detail sidebar (`ContactPanel` component and its data flow)
**Server:** `vultr` (SSH alias), project at `/home/tikso/tikso/`

---

## 1. Component Map

The sidebar is a 3-column right panel within the inbox view. The component tree is:

```
InboxLayout (src/components/inbox/inbox-layout.tsx)  [1154 lines, "use client"]
  |
  +-- ConversationList (left column)
  +-- ChatArea (center column)
  +-- ContactPanel (right column, 320px fixed width)
        |
        +-- ProfileHeader          -- Avatar, editable name, subscriber badge, lead score
        +-- ContactInfoCard        -- Phone, email, registration date (shared component)
        +-- QuickActionsSection    -- Close, Trigger Flow, Pause Automation
        +-- AssignmentJourneySection -- Agent assignment dropdown + Journey state machine
        +-- TagsSection            -- Tag list with add/remove
        +-- UnifiedNotesSection    -- Personal observation + team internal notes (tabs)
        +-- ConversationInsight    -- AI "DNA da Conversa" (sentiment, intent, urgency, topics)
        +-- CommitmentsSection     -- Promise tracking (pending/fulfilled/broken)
        +-- ActivitySubSections    -- Sequences, Campaigns, Custom Fields, Pipeline cards
        +-- StatsBar               -- Last message time + Lead score
```

**File:** `/home/tikso/tikso/src/components/inbox/contact-panel.tsx` (1433 lines)

**Shared components from** `/home/tikso/tikso/src/components/contacts/shared/`:
- `ContactInfoCard` -- reusable contact info display
- `TagList` -- reusable tag display with edit capability
- `NotesSection` -- tabbed notes (observation + internal notes)
- `SectionHeader` -- collapsible section wrapper
- `QuickActions` -- close/flow/pause action buttons

---

## 2. Data Fetching Architecture

### 2.1 Pattern: Server Actions (NOT server components, NOT tRPC)

The entire inbox is a **client-side SPA** rendered inside a `"use client"` boundary. All data access goes through Next.js **Server Actions** (`"use server"` functions) defined in:

- `/home/tikso/tikso/src/app/(app)/[orgId]/inbox/actions.ts` -- Primary data layer (1821 lines)
- `/home/tikso/tikso/src/app/(app)/[orgId]/ai/actions.ts` -- Journey state operations
- `/home/tikso/tikso/src/app/(app)/[orgId]/campaigns/actions.ts` -- Org tags

Each server action:
1. Calls `requireOrgAccess(orgId)` for auth + tenant resolution
2. Creates a tenant-scoped Prisma client via `createTenantClient(orgId)`
3. Performs Prisma queries
4. Returns serialized DTOs

### 2.2 Data Flow for Sidebar

When a conversation is selected (`selectedId` changes), `InboxLayout` triggers **two parallel calls**:

```
useEffect [selectedId changes]
  |
  +-- loadMessages()  --> getMessages(orgId, selectedId)
  +-- loadContact()   --> getContactDetails(orgId, "", selectedId)
```

The `ContactPanel` then receives `contact` as a prop. Internally, **four additional child-level data fetches** fire:

| Sub-component | Server Action | Trigger |
|---|---|---|
| `AssignmentJourneySection` | `getJourneyInfo(orgId, contactId)` | `useEffect([orgId, contactId])` |
| `UnifiedNotesSection` | `getInternalNotes(orgId, conversationId)` | `useEffect([orgId, conversationId])` |
| `ConversationInsight` | `getConversationInsight(orgId, conversationId)` | `useEffect([orgId, conversationId])` |
| `CommitmentsSection` | `getCommitments(orgId, conversationId)` | `useEffect([orgId, conversationId])` |
| `QuickActionsSection` | `getFlows(orgId)` | On-demand (click "Fluxo" button) |

**Total network requests per conversation switch:** **6 sequential/parallel server action calls** (1 for messages, 1 for contact details, 4 for sidebar sub-sections).

### 2.3 Authentication Cost

Every server action independently calls `requireOrgAccess(orgId)` which hits the auth system. For 6 parallel actions, that is **6 separate `auth()` calls** per conversation switch. The `auth()` function from NextAuth v5 validates the session JWT each time.

---

## 3. State Management Analysis

### 3.1 No Zustand Store

There is **no Zustand store** for inbox state. There is no `/src/stores/` directory at all. All state lives in `InboxLayout` as local `React.useState` hooks:

```typescript
// InboxLayout local state (excerpt)
const [conversations, setConversations] = useState<ConversationListItem[]>([]);
const [selectedId, setSelectedId] = useState<string | null>(null);
const [messages, setMessages] = useState<MessageItem[]>([]);
const [contact, setContact] = useState<ContactDetails | null>(null);
const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
const [orgTags, setOrgTags] = useState<{...}[]>([]);
const [isContactPanelOpen, setIsContactPanelOpen] = useState(true);
// ... ~25+ useState hooks total
```

### 3.2 Prop Drilling Depth

`InboxLayout` passes **16 props** to `ContactPanel`. `ContactPanel` then distributes them to 8 sub-components. There is no context provider -- all state flows via props.

### 3.3 Re-render Triggers

The `ContactPanel` re-renders when **any** of these 16 props change. Because all state lives in `InboxLayout`, updates to conversation list, messages, or contact data all trigger re-renders of the parent, which cascades to `ContactPanel` even if sidebar-specific data has not changed.

Key re-render triggers:
1. **Conversation selection** -- Full re-render + 6 data fetches
2. **Real-time message arrival** -- `messages` state update triggers `InboxLayout` re-render, which cascades to `ContactPanel` despite the sidebar having no dependency on messages
3. **Typing indicator** -- Same cascade issue
4. **Tag add/remove** -- Optimistic update to `contact` state, correct behavior
5. **Assignment change** -- Updates `conversations` array, cascades to sidebar

---

## 4. Real-Time Architecture

### 4.1 Centrifugo WebSocket Integration

Real-time events flow through **Centrifugo** via the `useRealtimeInbox` hook and `useCentrifugo` provider.

**Channels subscribed:**
- `org:{orgId}` -- Org-wide events (new messages, conversation updates, typing, status changes, org freeze/unfreeze)
- `conversation:{selectedConversationId}` -- Per-conversation events (message status, typing, transcription)

**Events handled by the sidebar:**

| Event | Channel | Sidebar Impact |
|---|---|---|
| `message:new` | `org:*` | Indirect -- triggers `InboxLayout` re-render |
| `conversation:update` | `org:*` | Updates `assignedToId` in conversation list, reflected via prop |
| `insight:update` | `conversation:*` | **Direct** -- `ConversationInsight` subscribes independently to Centrifugo |
| `contact:typing` | Both | No sidebar impact (only chat area) |
| `message:status` | Both | No sidebar impact (only chat area) |

### 4.2 What Is NOT Real-Time in the Sidebar

The following sidebar sections **do not receive real-time updates**:

| Section | Problem |
|---|---|
| **Contact details** (name, email, phone) | If another agent edits the contact, this sidebar shows stale data until conversation is re-selected |
| **Tags** | Tag changes from other agents/automations are invisible |
| **Journey state** | AI-driven journey transitions (e.g., "exploring" -> "negotiating") are not pushed to the sidebar |
| **Commitments** | New commitments added by AI agents or other users are invisible |
| **Internal notes** | Notes added by other agents are invisible |
| **Lead score** | Score changes from scoring cron are invisible |
| **Activity** (sequences, campaigns, pipeline) | Enrollment/progress changes are invisible |

Only `ConversationInsight` has its own Centrifugo subscription for real-time updates.

---

## 5. Prisma Data Model Connections

The sidebar pulls data from **12 Prisma models** across 6 server actions:

```
getContactDetails() touches:
  Contact
  ContactTag -> Tag
  SequenceEnrollment -> Sequence
  CampaignRecipient -> Campaign
  PipelineCard -> PipelineStage -> Pipeline
  LeadScore
  VariableValue -> CustomFieldDef (via Variable)

getJourneyInfo() touches:
  Contact (journeyState, journeyStateAt)
  JourneyTransition

getConversationInsight() touches:
  ConversationInsight

getInternalNotes() touches:
  InternalNote -> User (author)

getCommitments() touches:
  Commitment (via HandoffService)

getFlows() touches:
  Flow
```

### 5.1 The `getContactDetails` Query

This is the heaviest single query. It uses **6 nested `include` clauses** with Prisma:

```typescript
db.contact.findUnique({
  where: { id: resolvedContactId },
  include: {
    tags: { include: { tag: { select: { id, name, color } } } },
    sequenceEnrollments: { include: { sequence: { select: { name, _count: { select: { steps } } } } } },
    campaignRecipients: { include: { campaign: { select: { name, status } } }, orderBy: { createdAt: "desc" } },
    pipelineCards: { include: { stage: { select: { name, color, pipeline: { select: { name } } } } } },
    leadScores: { orderBy: { lastCalculated: "desc" }, take: 1 },
    variableValues: { include: { variable: { select: { key, label, type } } } },
  },
});
```

**Concern:** This query **always loads ALL related data** (all campaigns, all sequence enrollments, all pipeline cards, all variable values) regardless of whether the user expands the Activity section. The Activity section defaults to **collapsed** (`defaultOpen={false}`), meaning the data is loaded but never rendered in the common case.

### 5.2 Contact Resolution Path

When `getContactDetails` is called from `InboxLayout`, the `contactId` parameter is passed as empty string `""`:

```typescript
const details = await getContactDetails(orgId, "", selectedId!);
```

This forces the server action to perform an **extra query** to resolve the contact from the conversation:

```typescript
// Inside getContactDetails:
if (!resolvedContactId && conversationId) {
  const conversation = await db.conversation.findUnique({
    where: { id: conversationId },
    include: { contactIdentity: { select: { contactId: true } } },
  });
  resolvedContactId = conversation.contactIdentity.contactId;
}
```

This is an unnecessary extra round-trip. The conversation data is already loaded in `InboxLayout` and could resolve the contactId on the client side.

---

## 6. Identified Issues

### CRITICAL

#### C1. Direct Object Mutation in ProfileHeader

```typescript
// contact-panel.tsx, line 148-149
onNameUpdated={(newName) => {
  if (contact) contact.name = newName;
}}
```

This **directly mutates the `contact` prop** instead of calling `setContact()`. React will not detect this mutation, leaving the component in an inconsistent state where the prop value differs from what React "knows." The `handleUpdateNotes` callback in `InboxLayout` correctly uses `setContact((prev) => ...)`, but `ProfileHeader`'s name update does not follow this pattern.

**Impact:** The name appears updated visually (because the mutation affects the same object reference), but React's reconciliation is bypassed. If a parent re-render occurs for any other reason, the sidebar could flash stale data or exhibit unpredictable behavior.

### HIGH

#### H1. Waterfall Data Fetching (N+1 Server Action Pattern)

Each conversation switch triggers **6 independent server action calls**, each of which independently:
- Validates the session (`auth()`)
- Resolves org access (`requireOrgAccess()`)
- Creates a Prisma tenant client (`createTenantClient()`)

This means **6 separate authentication checks** and **6 separate Prisma client instantiations** per conversation switch. The `getContactDetails` query alone performs 2 Prisma queries (contact resolution + main query with 6 includes).

**Recommendation:** Create a single `getSidebarData(orgId, conversationId)` server action that bundles contact details, journey info, notes, commitments, and insight in a single server-side call with shared auth.

#### H2. Missing Note Delete Server Action (Mixed Pattern)

Note deletion uses a **raw `fetch()` call** to an API route instead of a server action:

```typescript
// UnifiedNotesSection, line 1034
const res = await fetch(`/api/inbox/notes?noteId=${noteId}`, { method: "DELETE" });
```

However, the `/home/tikso/tikso/src/app/api/inbox/notes/route.ts` file **does not implement a DELETE handler**. It only has `POST` and `GET`. This means note deletion silently fails (the `fetch` returns a 405 Method Not Allowed, which the catch block swallows with `toast.error`).

**Impact:** Users cannot delete internal notes. The delete button appears functional but does nothing.

#### H3. Over-fetching for Collapsed Sections

The `getContactDetails` query loads **all** campaigns, sequences, pipeline cards, and custom fields eagerly. The Activity section that renders this data defaults to `collapsed` (`defaultOpen={false}`). For a contact with 50 campaigns and 20 sequence enrollments, this is pure waste on every conversation switch.

**Recommendation:** Lazy-load Activity section data only when the user expands it, similar to how flows are loaded on-demand.

#### H4. No Real-Time Updates for Most Sidebar Sections

As documented in section 4.2, only `ConversationInsight` has real-time updates. Tags, journey state, notes, commitments, and lead score can become stale if changed by other agents, automations, or AI pipelines while the sidebar is open.

**Recommendation:** Publish Centrifugo events for `contact:updated`, `contact:tag:changed`, `journey:transition`, `note:added`, and `commitment:updated`. Subscribe in the sidebar.

### MEDIUM

#### M1. No Error Boundaries

There are no React error boundaries within the `ContactPanel`. If `ConversationInsight` (which subscribes to Centrifugo) throws an unhandled error, the entire sidebar crashes.

#### M2. 25+ useState Hooks in InboxLayout

`InboxLayout` manages ~25 `useState` hooks in a single component (1154 lines). This is a maintainability concern that makes the component difficult to reason about. Any state change in `InboxLayout` triggers re-renders for all children, including the sidebar.

**Recommendation:** Extract sidebar-specific state into either a `useSidebarState` custom hook or a lightweight context/Zustand store that is scoped to the sidebar.

#### M3. Journey Info Fetched Redundantly

`getJourneyInfo` makes **two separate Prisma queries** (one for contact, one for transitions). The contact's `journeyState` and `journeyStateAt` are already loaded by `getContactDetails` (which fetches the full `Contact` record). These fields are not included in the returned DTO but they exist in the query result.

#### M4. Missing useEffect Cleanup in CommitmentsSection

```typescript
// CommitmentsSection, line 1074-1080
React.useEffect(() => {
  setIsLoading(true);
  getCommitments(orgId, conversationId)
    .then((data) => setCommitments(data))
    .catch(() => {})
    .finally(() => setIsLoading(false));
}, [orgId, conversationId]);
```

No cancellation flag. If the user rapidly switches conversations, state updates from stale promises can apply to the wrong conversation. The `AssignmentJourneySection` correctly uses the `cancelled` flag pattern, but `CommitmentsSection` does not.

#### M5. Notes Delete Uses Mixed API Pattern

Even if the DELETE handler existed (see H2), using `fetch()` for one operation and server actions for all others creates an inconsistent architecture. The note create uses `addInternalNote` (server action), the note list uses `getInternalNotes` (server action), but delete uses a REST API route.

#### M6. teamMembers and orgTags Loaded Once, Never Refreshed

```typescript
// InboxLayout, line 424-438
React.useEffect(() => {
  async function loadTeamAndTags() {
    const [members, tags] = await Promise.all([
      getTeamMembers(orgId),
      getOrgTags(orgId),
    ]);
    setTeamMembers(members);
    setOrgTags(tags);
  }
  loadTeamAndTags();
}, [orgId]);
```

Team members and org tags are loaded once when the inbox mounts and never refreshed. If an admin adds a new tag or a new team member while the inbox is open, they won't appear in the assignment dropdown or tag picker until the page is reloaded.

### LOW

#### L1. Fixed 320px Sidebar Width

The sidebar is hardcoded to `w-[320px]`. On wide screens this may feel cramped for the Activity section content, and there is no resize handle.

#### L2. No Virtualization for Long Lists

If a contact has many tags, campaigns, sequences, or commitments, all items are rendered in the DOM. For the typical case (under 20 items per section), this is fine. For power users with 50+ tags or campaigns, this could cause jank.

#### L3. `hasFetched` Flag in QuickActionsSection

The `hasFetched` flag prevents refetching flows after the first load. If flows are published while the sidebar is open, the user sees a stale list. This is acceptable for a low-frequency operation but worth noting.

---

## 7. Data Flow Diagram

```
                     InboxLayout (client component, "use client")
                     |                              |                        |
           [selectedId changes]               [initial mount]          [Centrifugo]
                     |                              |                        |
           +--------+--------+            +---------+--------+      useRealtimeInbox
           |                 |            |                  |              |
     getMessages()    getContactDetails()  getTeamMembers()  getOrgTags()  |
     (actions.ts)     (actions.ts)         (actions.ts)      (campaigns)   |
           |                 |                                             |
           v                 v                                             v
     messages state    contact state -----> ContactPanel              org channel
           |                 |              (16 props)                subscription
           |                 |                   |
           |                 |    +---------+----+----+---------+---------+
           |                 |    |         |         |         |         |
           |                 | Profile  QuickAct  AssignJrn  Tags    UnifiedNotes
           |                 |    |         |         |         |         |
           |                 |    |    [on-demand]    |         |     getInternalNotes()
           |                 |    |    getFlows()     |         |         |
           |                 |    |                   |         |    InternalNote model
           |                 |    |           getJourneyInfo()  |
           |                 |    |                   |         |
           |                 |    |           Contact model     |
           |                 |    |           JourneyTransition |
           |                 |    |                             |
           |                 |    |    +----------+----------+  |
           |                 |    |    |          |          |  |
           |                 |    |  ConvInsight  Commitments StatsBar
           |                 |    |    |          |
           |                 |    |  getCInsight() getCommitments()
           |                 |    |    |          |
           |                 |    |  +Centrifugo  Commitment model
           |                 |    |  subscription
           |                 |    |  (insight:update)
```

---

## 8. Prisma Query Count per Conversation Switch

| Query | Source | Models Touched | Estimated Cost |
|-------|--------|---------------|----------------|
| Resolve contactId from conversation | `getContactDetails` | Conversation, ContactIdentity | Light |
| Fetch contact + 6 includes | `getContactDetails` | Contact, ContactTag, Tag, SequenceEnrollment, Sequence, CampaignRecipient, Campaign, PipelineCard, PipelineStage, Pipeline, LeadScore, VariableValue, Variable | **Heavy** |
| Fetch contact journeyState | `getJourneyInfo` | Contact | Light |
| Fetch journey transitions (top 15) | `getJourneyInfo` | JourneyTransition | Light |
| Fetch conversation insight | `getConversationInsight` | ConversationInsight | Light |
| Fetch internal notes | `getInternalNotes` | InternalNote, User | Light |
| Fetch commitments | `getCommitments` | Commitment (via HandoffService) | Light |

**Total:** ~9 Prisma queries minimum for sidebar data alone (plus 3-4 for messages in the chat area).

---

## 9. Recommendations Summary

| Priority | Issue | Recommendation |
|----------|-------|----------------|
| **CRITICAL** | C1. Direct prop mutation | Use `setContact()` functional update in `onNameUpdated` callback |
| **HIGH** | H1. Waterfall fetching | Create bundled `getSidebarData()` server action |
| **HIGH** | H2. Broken note delete | Add DELETE handler to `/api/inbox/notes/route.ts` or create server action |
| **HIGH** | H3. Over-fetching | Lazy-load Activity section on expand |
| **HIGH** | H4. No real-time for sidebar | Add Centrifugo subscriptions for contact/tag/journey/note events |
| **MEDIUM** | M1. No error boundaries | Add `ErrorBoundary` around `ConversationInsight` and `CommitmentsSection` |
| **MEDIUM** | M2. State bloat | Extract `useSidebarState` hook or introduce scoped Zustand store |
| **MEDIUM** | M3. Redundant journey query | Include `journeyState`/`journeyStateAt` in `getContactDetails` DTO |
| **MEDIUM** | M4. Missing cleanup | Add `cancelled` flag to `CommitmentsSection` useEffect |
| **MEDIUM** | M5. Mixed API pattern | Migrate note delete to server action for consistency |
| **MEDIUM** | M6. Stale team/tags | Refresh on Centrifugo `org:settings:updated` event or add polling |

---

## 10. Key File Inventory

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| ContactPanel | `/home/tikso/tikso/src/components/inbox/contact-panel.tsx` | 1433 | Sidebar component + 8 sub-components |
| InboxLayout | `/home/tikso/tikso/src/components/inbox/inbox-layout.tsx` | 1154 | Parent orchestrator, all state lives here |
| Inbox Actions | `/home/tikso/tikso/src/app/(app)/[orgId]/inbox/actions.ts` | 1821 | Server actions data layer |
| AI Actions | `/home/tikso/tikso/src/app/(app)/[orgId]/ai/actions.ts` | ~600 | Journey state operations |
| ConversationInsight | `/home/tikso/tikso/src/components/inbox/conversation-insight.tsx` | ~200 | AI insight display with Centrifugo sub |
| useRealtimeInbox | `/home/tikso/tikso/src/hooks/use-realtime-inbox.ts` | ~280 | Centrifugo WebSocket integration |
| Types | `/home/tikso/tikso/src/components/inbox/types.ts` | ~140 | Shared TypeScript interfaces |
| Journey Types | `/home/tikso/tikso/src/lib/journey/types.ts` | ~100 | Journey state enum + config |
| Notes API Route | `/home/tikso/tikso/src/app/api/inbox/notes/route.ts` | ~100 | REST API (POST + GET only, no DELETE) |
| Shared Components | `/home/tikso/tikso/src/components/contacts/shared/` | ~5 files | Reusable contact UI components |

---

*-- Aria, arquitetando o futuro*
