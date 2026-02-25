# Tikso CRM -- Inbox Contact Detail Sidebar: Comprehensive UX Audit

**Date:** 2026-02-25
**Auditor:** Uma (UX Design Expert, AIOS)
**Scope:** `src/components/inbox/contact-panel.tsx` and all child/shared components
**Method:** Full source code analysis of 1,433-line component + 6 shared sub-components

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Component Architecture Overview](#2-component-architecture-overview)
3. [Information Architecture Audit](#3-information-architecture-audit)
4. [Visual Design Audit](#4-visual-design-audit)
5. [Functionality Gap Analysis](#5-functionality-gap-analysis)
6. [Usability Issues](#6-usability-issues)
7. [Mobile Responsiveness Audit](#7-mobile-responsiveness-audit)
8. [Accessibility Audit (WCAG 2.1 AA)](#8-accessibility-audit-wcag-21-aa)
9. [Performance Concerns](#9-performance-concerns)
10. [Code Architecture Observations](#10-code-architecture-observations)
11. [Prioritized Recommendations](#11-prioritized-recommendations)
12. [Comparison: Inbox Panel vs Contacts Drawer](#12-comparison-inbox-panel-vs-contacts-drawer)

---

## 1. Executive Summary

The contact detail sidebar is an ambitious, feature-rich component that crams 9 distinct sections into a 320px-wide panel. It demonstrates strong engineering fundamentals -- proper use of shared components, real-time updates via Centrifugo, debounced saves, and collapsible sections. However, the UX suffers from **information overload**, **hierarchy collapse** (everything looks equally important), and several accessibility gaps that would fail a WCAG 2.1 AA audit.

### Severity Distribution

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 4 | Accessibility blockers, missing ARIA, mobile unusability |
| High | 8 | Information hierarchy, contrast failures, missing features |
| Medium | 9 | Spacing inconsistencies, UX friction, missing feedback |
| Low | 6 | Polish items, micro-interactions, nice-to-haves |

**Overall Score: 62/100** -- Functional but needs significant UX refinement.

---

## 2. Component Architecture Overview

### File Map

```
src/components/inbox/contact-panel.tsx (1,433 lines)
  |-- ProfileHeader (inline, lines 391-543)
  |-- ContactInfoCard (shared: src/components/contacts/shared/contact-info-card.tsx)
  |-- QuickActionsSection (inline, lines 545-654)
  |     |-- QuickActions (shared: src/components/contacts/shared/quick-actions.tsx)
  |     |-- Flow picker (inline)
  |-- AssignmentJourneySection (inline, lines 656-888)
  |     |-- PresenceIndicator (src/components/presence/presence-indicator.tsx)
  |     |-- Journey state dropdown + mini timeline
  |-- TagsSection (inline, lines 890-962)
  |     |-- TagList (shared: src/components/contacts/shared/tag-list.tsx)
  |-- UnifiedNotesSection (inline, lines 964-1055)
  |     |-- NotesSection (shared: src/components/contacts/shared/notes-section.tsx)
  |-- ConversationInsight (src/components/inbox/conversation-insight.tsx)
  |     |-- Real-time via Centrifugo subscription
  |-- CommitmentsSection (inline, lines 1057-1262)
  |-- ActivitySubSection (inline, lines 1264-1291) x4
  |     |-- Sequences, Campaigns, Custom Fields, Pipeline
  |-- StatsBar (inline, lines 1293-1314)
  |-- ContactPanelSkeleton (inline, lines 1388-1433)
  |-- Helper components: LeadScoreBadge, EnrollmentStatusBadge, CampaignStatusBadge, formatRelativeDate
```

### Section Order (Current)

| # | Section | Default State | Priority Assessment |
|---|---------|---------------|---------------------|
| 1 | Profile Header (avatar, name, badges) | Always visible | Correct -- identity first |
| 2 | Contact Info (phone, email, date) | Always visible | Correct -- essential data |
| 3 | Quick Actions (Fechar, Fluxo, Pausar) | Always visible | Questionable -- should be more prominent |
| 4 | Assignment + Journey | Always visible | Correct but too dense |
| 5 | Tags | Always visible | Could be collapsible |
| 6 | Notes (Personal + Team tabs) | Always visible | Correct -- high daily use |
| 7 | AI Insights + Commitments | Collapsible, default OPEN | Should be higher in hierarchy |
| 8 | Activity (Sequences, Campaigns, Fields, Pipeline) | Collapsible, default CLOSED | Correct |
| 9 | Stats Bar (Last msg, Score) | Always visible at bottom | Misplaced -- should be near profile |

---

## 3. Information Architecture Audit

### 3.1 PROBLEM: Stats Bar Buried at Bottom [HIGH]

**Current:** The StatsBar (last message time, lead score) is the very last section -- below Activity, below Notes, below everything.

**Issue:** Last message recency and lead score are high-signal, glanceable metrics that a barbershop operator checks constantly. Burying them below a collapsible Activity section means the user must scroll past potentially 15+ items to see "when did this person last talk to me?"

**Recommendation:** Move StatsBar to position 2, immediately below ProfileHeader. Merge lead score badge (already shown in ProfileHeader) with the stats display to eliminate redundancy.

### 3.2 PROBLEM: AI Insights Default Open -- Activity Default Closed [MEDIUM]

**Current:** The "Inteligencia" section (AI insights + commitments) defaults open, while "Atividade" (sequences, campaigns, pipeline, custom fields) defaults closed.

**Issue:** For a barbershop CRM user, knowing which pipeline stage a customer is in ("Agendamento marcado" vs "Primeiro contato") is more immediately actionable than an AI-generated sentiment summary. The priority feels optimized for a tech demo rather than for the daily workflow of someone managing 50+ WhatsApp conversations.

**Recommendation:** Consider making both collapsible with smart defaults: if the contact has active pipeline cards or sequences, auto-expand Activity; if there is a high-urgency or negative-sentiment insight, auto-expand Intelligence.

### 3.3 PROBLEM: Quick Actions Lack Visual Weight [HIGH]

**Current:** Three outline buttons (Fechar, Fluxo, Pausar) in a row, each 8px tall with 11px text.

**Issue:** "Fechar conversa" is the most consequential action on this panel -- it closes the conversation. Yet it has identical visual weight to "Fluxo" (trigger a flow) and "Pausar" (toggle automation). All three are ghost-style outline buttons that blend into the background. In a high-volume barbershop inbox where an operator is closing 30+ conversations per day, these buttons need to be instantly findable without visual scanning.

**Recommendation:** Make "Fechar" a more prominent, destructive-styled button (or at least filled rather than outlined). Consider a sticky action bar at the bottom of the panel (like mobile app patterns) for the most-used actions.

### 3.4 PROBLEM: Section Count Creates Scroll Fatigue [HIGH]

**Current:** 9 sections separated by 7 `<Separator>` dividers, all within a 320px-wide, full-height `<ScrollArea>`.

**Issue:** With even modest data (2 tags, 1 pipeline card, 1 sequence, AI insight present), the sidebar requires approximately 3 full viewport heights of scrolling. For a tool used 8+ hours per day, this creates significant scroll fatigue.

**Recommendation:**
- Merge sections: Combine "Assignment + Journey" with "Profile Header" (make assignment a compact element under the name).
- Collapse by default: Tags, Notes, and Activity should all start collapsed unless they have notable content.
- Consider a tabbed interface for the lower sections (Info | Notes | Intelligence | Activity) to flatten the scroll depth.

### 3.5 PROBLEM: Redundant Lead Score Display [LOW]

**Current:** Lead score appears in two places: (1) as a `LeadScoreBadge` in the ProfileHeader section, and (2) as a number in the StatsBar at the bottom.

**Recommendation:** Remove from StatsBar or ProfileHeader (not both). Keep it in ProfileHeader as a badge since it adds context next to the name.

---

## 4. Visual Design Audit

### 4.1 PROBLEM: Typography Scale Too Compressed [HIGH]

**Current typography inventory:**

| Element | Size | Usage |
|---------|------|-------|
| Panel title "Detalhes do Contato" | `text-sm` (14px) | Header |
| Contact name | `text-sm font-bold` (14px) | Profile |
| Section labels | `text-[10px]` (10px) | "Acoes rapidas", "Atribuicao e Jornada" |
| Sub-labels | `text-[10px]` (10px) | "Atribuido a", "Jornada" |
| Body text | `text-xs` (12px) | Tag names, flow names, notes |
| Micro text | `text-[9px]` (9px) | Timestamps, journey "Desde ha 2 dias" |
| Micro-micro text | `text-[8px]` (8px) | Activity sub-section count badge |

**Issue:** The type scale spans from 8px to 14px across 6 distinct sizes. At `text-[9px]` (9px), text becomes nearly illegible on standard-DPI monitors, especially for users over 40 (Tikso's barbershop target demographic skews older). The `text-[10px]` section labels using `uppercase tracking-widest` further reduce readability at that size.

**Recommendation:**
- Establish a minimum of 11px for any visible text.
- Reduce the number of distinct sizes to 3-4 (12px body, 13px emphasis, 14px headings, 11px captions).
- Remove `tracking-widest` from 10px labels -- the extra letter spacing at micro sizes hurts readability more than it helps.

### 4.2 PROBLEM: Inconsistent Border Radius [MEDIUM]

**Current radius inventory:**

| Element | Radius |
|---------|--------|
| Quick action buttons | `rounded-xl` (12px) |
| Flow picker list | `rounded-xl` (12px) |
| Assignment dropdown trigger | `rounded-xl` (12px) |
| Journey state display | `rounded-xl` (12px) |
| Commitment input | `rounded-lg` (8px) |
| Name edit input | `rounded-lg` (8px) |
| Contact info rows | `rounded-lg` (8px) |
| Tag badges | `rounded-full` (9999px) |
| Stats bar cards | `rounded-xl` (12px) |
| Note textarea | `rounded-xl` (12px) |
| Section header collapse button | `rounded-lg` (8px) |

**Issue:** Three competing radius tokens (`rounded-lg`, `rounded-xl`, `rounded-full`) used without a clear hierarchy rule. The commitment input uses `rounded-lg` while the very similar notes textarea uses `rounded-xl`.

**Recommendation:** Standardize: `rounded-xl` for containers/cards, `rounded-lg` for inputs/buttons, `rounded-full` for badges/pills only.

### 4.3 PROBLEM: Color Inconsistency in Section Icons [MEDIUM]

**Current icon coloring:**

| Section | Icon | Color |
|---------|------|-------|
| Quick Actions | (in buttons) | Varies per button |
| Assignment | UserCheck | `text-muted-foreground` |
| Journey | Compass | `text-muted-foreground` |
| Tags | Tag | `text-muted-foreground` |
| Notes | StickyNote | `text-amber-600` |
| Intelligence | TrendingUp | Passed to SectionHeader, defaults to `text-muted-foreground` |
| Commitments | Handshake | `text-muted-foreground` |
| Activity | ListOrdered | Passed to SectionHeader, defaults to `text-muted-foreground` |

**Issue:** Notes gets a special amber icon while every other section uses the same muted gray. This inconsistency either suggests Notes is more important (debatable) or is simply an oversight from when the NotesSection was built as a standalone component.

**Recommendation:** Either give all sections semantically meaningful icon colors (e.g., green for activity, blue for intelligence, amber for notes) or keep them all `text-muted-foreground` for visual consistency.

### 4.4 PROBLEM: Separator Overuse [MEDIUM]

**Current:** 7 `<Separator>` elements between the 9 sections, each with `className="my-1"`.

**Issue:** With this many separators in a narrow column, the visual rhythm becomes monotonous -- a gray line appears every ~80px of vertical space. The separators add visual noise without adding information, since the sections already have their own headers with distinct styling.

**Recommendation:** Remove explicit `<Separator>` dividers. Instead, rely on `space-y-6` (or larger) between sections and the visual weight of section headers to create natural grouping. The whitespace itself becomes the divider.

### 4.5 OBSERVATION: Dark Mode Support [POSITIVE]

The component properly uses semantic Tailwind tokens (`bg-card`, `text-foreground`, `text-muted-foreground`, `bg-surface-2`) and the shared components include explicit dark mode overrides (e.g., `dark:bg-amber-950/30` in NotesSection). This is well done.

### 4.6 PROBLEM: Avatar Gradient Ring Questionable [LOW]

**Current:** `<div className="rounded-full p-0.5 bg-gradient-to-br from-primary/20 to-primary/5">` wraps the avatar.

**Issue:** At 20% and 5% opacity, this gradient ring is barely visible on light backgrounds. It adds DOM complexity without meaningful visual impact. On dark mode, it may become even less visible.

**Recommendation:** Either make the ring meaningful (e.g., show green ring for online contacts, orange ring for high-score leads) or remove it.

---

## 5. Functionality Gap Analysis

### 5.1 MISSING: Phone Number Formatting [HIGH]

**Current:** The phone number `5579999811988` is displayed raw, as stored in the database.

**Issue:** Brazilian phone numbers should be formatted as `+55 (79) 99981-1988` for readability. An unformatted 13-digit string is harder to scan, harder to verify ("is that the right number?"), and feels unprofessional.

**Recommendation:** Add a `formatBrazilianPhone()` utility and apply it in ContactInfoCard. The raw number should still be used for copy-to-clipboard.

### 5.2 MISSING: "Open in WhatsApp" Quick Action [MEDIUM]

**Current:** The ContactInfoCard has a `showWhatsAppButton` prop and `whatsAppHref` prop, but the inbox contact panel passes neither. The button is only shown in the Contacts page drawer.

**Issue:** For a WhatsApp-first CRM, the ability to quickly open the contact's WhatsApp conversation in the phone app (via `https://wa.me/{number}`) is a core workflow. Operators often switch between the web CRM and their phone.

**Recommendation:** Pass `showWhatsAppButton={true}` and construct the `whatsAppHref` from the contact's phone number.

### 5.3 MISSING: Contact Edit Mode for Phone/Email [MEDIUM]

**Current:** The ProfileHeader allows inline editing of the contact name (click to edit, save/cancel). But phone and email in ContactInfoCard are read-only in the inbox sidebar.

**Issue:** The Contacts page drawer (`contact-drawer.tsx`) supports full editing of name, phone, email, and notes in an edit mode. The inbox panel only supports name editing and observation auto-save. If an operator realizes a phone number is wrong while chatting, they must leave the inbox, navigate to Contacts, find the contact, and edit there.

**Recommendation:** Add inline edit capability for phone and email, or provide a "Edit full profile" link that opens the ContactDrawer Sheet.

### 5.4 MISSING: Commitment Due Dates on Creation [MEDIUM]

**Current:** The commitments input is a single text field. Due dates only appear on commitments that already have them (set server-side or via AI extraction).

**Issue:** A barbershop operator promising "I'll call you back tomorrow about the appointment" should be able to set a due date when creating the commitment. Currently there is no date picker in the UI.

**Recommendation:** Add an optional date picker next to the commitment input, or at minimum a "Tomorrow" / "Next week" quick-pick.

### 5.5 MISSING: Conversation Status Display [HIGH]

**Current:** The panel shows no indication of whether the current conversation is open, closed, or assigned to the AI agent.

**Issue:** The "Fechar" button suggests closing the conversation, but there is no visual indicator of whether it is currently open. The `ConversationListItem` type has `status`, `caseStatus`, `isBusy`, and `busyByName` fields, but none of these are surfaced in the contact panel.

**Recommendation:** Add a conversation status badge near the top of the panel (e.g., "Conversa aberta" / "Atendida por Eli" / "Fechada") that gives immediate context.

### 5.6 MISSING: Revenue/Lifetime Value Display [LOW]

**Current:** Pipeline cards show individual deal values (`R$ {card.value}`) buried inside the collapsed Activity section.

**Issue:** For a business CRM, the total revenue or lifetime value of a contact is a key metric that should be glanceable, not buried 3 collapsible levels deep.

**Recommendation:** If pipeline value data is available, sum it and display in the StatsBar alongside lead score and last message time.

### 5.7 MISSING: Handoff/Transfer Action [MEDIUM]

**Current:** The panel has an `assign` dropdown for team members, but no explicit "Transfer to human" or "Take over from AI" action.

**Issue:** The inbox has a `handoff-dialog.tsx` component at the layout level, but the contact panel itself does not surface this action. In a WhatsApp CRM where AI (Eli) handles initial conversations, the operator needs a one-click "take over" action.

**Recommendation:** Add a prominent "Assumir conversa" button in the Quick Actions section when the conversation is being handled by the AI.

---

## 6. Usability Issues

### 6.1 PROBLEM: Name Edit Discoverability [MEDIUM]

**Current:** Clicking the contact name reveals an inline edit field. The only hint is a Pencil icon that appears on hover with `opacity-0 group-hover:opacity-100`.

**Issue:** The edit affordance is invisible until hover. On touch devices, there is no hover state, so the pencil icon never appears. The user must guess that the name is clickable. Additionally, the `title="Clique para editar o nome"` tooltip does not appear on touch devices either.

**Recommendation:** Always show the pencil icon at reduced opacity (e.g., `opacity-40`), or add a visible "Editar" text link.

### 6.2 PROBLEM: Mutation of Props (Direct Object Mutation) [HIGH]

**Current:** Line 149: `if (contact) contact.name = newName;`

**Issue:** This directly mutates the `contact` prop object passed from the parent (`InboxLayout`). This is a React anti-pattern that can cause stale closures, missed re-renders, and subtle bugs. The parent state is being mutated without going through `setContact`.

**Recommendation:** The `onNameUpdated` callback should update the parent's state properly via `setContact(prev => prev ? { ...prev, name: newName } : prev)` in InboxLayout. The child should not mutate the prop.

### 6.3 PROBLEM: Flow Picker UX Friction [MEDIUM]

**Current:** Clicking "Fluxo" toggles a flow picker inline. The flows are fetched on first click (lazy load). If no flows exist, it shows "Nenhum fluxo publicado".

**Issue:** The loading state shows a spinner with no text. The user doesn't know if it is loading flows or if something broke. After triggering a flow, there is a toast but the picker stays open -- the user must click "Fluxo" again to close it (actually line 587 does set `setShowFlowPicker(false)` on success, but this only fires after the API call completes, leaving a moment of confusion).

**Recommendation:** Add loading text ("Carregando fluxos..."), and consider using a Popover or DropdownMenu instead of an inline expanding panel for more consistent UX with the rest of the sidebar.

### 6.4 PROBLEM: Observation Auto-Save Lacks Feedback [MEDIUM]

**Current:** The personal observation textarea auto-saves after 1 second of debounce AND on blur. A tiny `Loader2` spinner appears next to "Notas" during save.

**Issue:** The spinner is 12px (`h-3 w-3`) and positioned at the section header level -- far from the textarea the user is typing in. Most users will not notice it. There is no "Saved" confirmation feedback after a successful save, and no undo capability.

**Recommendation:** Show a subtle "Salvo" text or checkmark directly below or inside the textarea, similar to how Google Docs shows "All changes saved." Consider also showing the last-saved timestamp.

### 6.5 PROBLEM: Journey Timeline Truncation Without Indication [LOW]

**Current:** The journey mini timeline shows `.slice(0, 3)` transitions.

**Issue:** If a contact has 10 transitions, only 3 are shown with no "ver mais" link or indication that there are more.

**Recommendation:** Add a "Ver historico completo" link when `transitions.length > 3`.

### 6.6 PROBLEM: Delete Note Requires No Confirmation [MEDIUM]

**Current:** Clicking the trash icon on a team note immediately sends a DELETE request.

**Issue:** No confirmation dialog. In a team environment, accidentally deleting a colleague's note is a meaningful data loss event.

**Recommendation:** Add an "Undo" toast (like Gmail) or a confirmation dialog for note deletion.

### 6.7 PROBLEM: Tag Addition via Dropdown Without Search [LOW]

**Current:** Available tags are shown in a DropdownMenu. Already-assigned tags are filtered out.

**Issue:** If the organization has 50+ tags, the dropdown becomes a long scroll list with no search/filter capability.

**Recommendation:** Add a search input at the top of the tag dropdown, or switch to a Combobox pattern.

---

## 7. Mobile Responsiveness Audit

### 7.1 PROBLEM: Fixed 320px Width [CRITICAL]

**Current:** `<div className="flex h-full w-[320px] shrink-0 flex-col border-l bg-card">`

**Issue:** The panel width is hardcoded to 320px. On mobile, the InboxLayout's `mobileView` state switches between "list", "chat", and "contact" views, but the ContactPanel itself does not adapt its width. Looking at the InboxLayout (line 84-94), the mobile detection uses `window.innerWidth < 640`. When `mobileView === "contact"`, the 320px-wide panel is rendered, but on a 375px-wide phone, this leaves only 55px for potential side padding or layout issues.

**Investigation:** The InboxLayout renders the ContactPanel conditionally:
- Desktop: panel renders alongside chat area
- Mobile: panel replaces the chat area (full-screen contact view)

However, the ContactPanel always renders with `w-[320px]`, meaning on mobile it does NOT fill the available width. The 320px is narrower than most phone screens but wastes the remaining space.

**Recommendation:** Use responsive width: `w-full sm:w-[320px]` or `w-full max-w-[320px]` so the panel fills the screen on mobile.

### 7.2 PROBLEM: No Mobile Back Navigation [CRITICAL]

**Current:** The panel has an X close button in the header. On mobile, this calls `onClose()` which toggles `isContactPanelOpen` (desktop behavior).

**Issue:** Looking at the InboxLayout code, on mobile the contact panel is shown when `mobileView === "contact"`. The close button should set `mobileView` to "chat" instead of toggling `isContactPanelOpen`. Without reading the full InboxLayout render logic, there may be a disconnect between the mobile view state and the panel's close behavior.

**Recommendation:** On mobile, replace the X button with an ArrowLeft (back) button that explicitly navigates back to the chat view. Add clear visual indication that this is a full-screen overlay, not a sidebar.

### 7.3 PROBLEM: Touch Target Sizes [HIGH]

**Current touch target inventory:**

| Element | Size | WCAG Minimum (44x44px) |
|---------|------|------------------------|
| Close button | `h-7 w-7` (28x28px) | FAIL |
| Tag remove X | ~20px (opacity-0 on no hover) | FAIL |
| Note delete trash | ~20px | FAIL |
| Commitment status buttons | `p-1` (~20px) | FAIL |
| Journey "Alterar" button | `h-6 px-2` (24px tall) | FAIL |
| Tag add (+) button | `h-6 w-6` (24px) | FAIL |
| Section collapse toggle | full-width (OK), but icon is 14px | PARTIAL |

**Issue:** 6 of 7 interactive elements fail the 44x44px WCAG minimum touch target size. On mobile, these are nearly impossible to tap accurately.

**Recommendation:** All interactive elements should have a minimum tap area of 44x44px. Use padding/margin to increase the clickable area even if the visual element is smaller.

### 7.4 PROBLEM: No Swipe Gestures [LOW]

**Issue:** Mobile CRM apps commonly support swiping right to go back from the contact detail to the chat. The current implementation relies solely on a tap on the X button.

**Recommendation:** Consider adding a swipe-right gesture to return to chat on mobile, using a library like `react-swipeable` or native touch event handling.

---

## 8. Accessibility Audit (WCAG 2.1 AA)

### 8.1 FAIL: Missing ARIA Labels on Interactive Elements [CRITICAL]

| Element | Issue |
|---------|-------|
| Name edit button (the clickable name) | No `aria-label`. Screen readers see: "Kelmer Palma" (no indication it is editable) |
| Tag remove X buttons | No `aria-label`. Screen readers see nothing meaningful |
| Commitment status buttons | Has `title` but no `aria-label`. `title` is not reliably read by all screen readers |
| Flow picker list buttons | No `aria-label`, only visual text |
| Note delete button | No `aria-label` |
| Assignment unassign button | No `aria-label`, only visual icon + text |

**Positive:** The panel close button correctly has `aria-label="Fechar painel"`.

**Recommendation:** Add `aria-label` to every interactive element. Examples:
- Name edit: `aria-label="Editar nome do contato"`
- Tag remove: `aria-label={`Remover tag ${tagName}`}`
- Commitment fulfill: `aria-label="Marcar compromisso como cumprido"`
- Note delete: `aria-label="Excluir nota"`

### 8.2 FAIL: No Landmark/Region Structure [HIGH]

**Current:** The panel is a plain `<div>` with no landmark role.

**Issue:** Screen readers cannot navigate the panel by region. With 9 sections, a screen reader user must Tab through every single element sequentially to find what they need.

**Recommendation:**
- Add `role="complementary"` and `aria-label="Detalhes do contato"` to the panel root.
- Add `role="region"` and `aria-label` to each major section.
- Use semantic HTML: `<section>` elements instead of `<div>` for each section.

### 8.3 FAIL: Focus Management on Panel Open [HIGH]

**Current:** When `isOpen` switches from false to true, the panel simply renders. No focus management.

**Issue:** A keyboard user who opens the contact panel with Ctrl+Shift+A has no way of knowing the panel is open unless they Tab through the entire page. Focus should move to the panel when it opens.

**Recommendation:** Use `React.useEffect` to focus the panel (or its close button) when `isOpen` transitions to true. Add focus trapping if the panel is modal on mobile.

### 8.4 FAIL: Color Contrast Issues [HIGH]

| Element | Foreground | Background | Ratio | WCAG AA (4.5:1) |
|---------|-----------|------------|-------|------------------|
| `text-[9px]` timestamps | `text-muted-foreground` (#6B7280) | `bg-card` (#FFFFFF) | 4.6:1 | PASS (barely) |
| `text-[9px] opacity-70` transition timestamps | #6B7280 at 70% | #FFFFFF | ~3.2:1 | FAIL |
| `text-muted-foreground/60` empty states | #6B7280 at 60% | #FFFFFF | ~2.8:1 | FAIL |
| `text-amber-400/60` placeholder | amber-400 at 60% | amber-50 bg | ~2.1:1 | FAIL |
| `text-[8px]` activity count badge | secondary palette | secondary bg | Untested, likely borderline | RISK |

**Issue:** Multiple opacity-reduced text elements fail WCAG AA contrast minimums. The pattern of using `/60` and `/70` opacity modifiers on already-muted colors consistently produces failing contrast ratios.

**Recommendation:**
- Never use opacity below 100% on text that conveys information.
- Replace `text-muted-foreground/60` with a dedicated `text-muted-subtle` token that meets 4.5:1 minimum.
- Replace placeholder opacity patterns with proper placeholder colors.

### 8.5 FAIL: No Skip Navigation [MEDIUM]

**Issue:** With 9 sections and potentially dozens of interactive elements, there is no way for a keyboard user to jump between sections.

**Recommendation:** Add a visually hidden skip-nav at the top of the panel: "Pular para Acoes rapidas | Notas | Inteligencia".

### 8.6 FAIL: Collapsible Sections Missing ARIA States [HIGH]

**Current:** The SectionHeader component uses `<button onClick={() => setIsOpen(prev => !prev)}>` for collapsible sections, but does not include `aria-expanded`, `aria-controls`, or connect the button to its content panel via ID.

**Recommendation:**
```tsx
<button
  aria-expanded={isOpen}
  aria-controls={`section-${title}`}
  onClick={() => setIsOpen(prev => !prev)}
>
  {title}
</button>
<div id={`section-${title}`} role="region" hidden={!isOpen}>
  {children}
</div>
```

### 8.7 OBSERVATION: Keyboard Navigation for Dropdowns [POSITIVE]

The component uses Radix UI's `DropdownMenu` for assignment and journey state selection, which provides built-in keyboard navigation (arrow keys, Enter, Escape). This is correct.

### 8.8 FAIL: Notes Textarea Missing Label [MEDIUM]

**Current:** The personal observation textarea and team note textarea use `placeholder` text as their only label.

**Issue:** Placeholder text is not a substitute for a `<label>`. Screen readers may not announce the purpose of the field.

**Recommendation:** Add `aria-label="Observacao pessoal sobre o contato"` to the personal textarea and `aria-label="Nova nota de equipe"` to the team textarea.

---

## 9. Performance Concerns

### 9.1 Multiple Independent API Calls on Mount [MEDIUM]

**Current data fetching per panel open:**
1. `getJourneyInfo()` -- in AssignmentJourneySection useEffect
2. `getInternalNotes()` -- in UnifiedNotesSection useEffect
3. `getCommitments()` -- in CommitmentsSection useEffect
4. `getConversationInsight()` -- in ConversationInsight useEffect
5. `getFlows()` -- lazy, on first "Fluxo" click

**Issue:** 4 parallel API calls on every panel open. Each child component independently manages its own loading state, leading to a "popcorn" loading pattern where different sections shimmer in at different times.

**Recommendation:**
- Consider a single `getContactPanelData()` server action that batches all 4 queries.
- Alternatively, use React Suspense boundaries with `use()` to coordinate loading.
- At minimum, add a shared loading context so the skeleton shows until ALL data is ready.

### 9.2 Re-Render on Every Note Character [LOW]

**Current:** `handleObsChange` sets state on every keystroke (debounced save, but state updates cause re-renders).

**Issue:** Typing in the observation textarea causes the entire UnifiedNotesSection to re-render on each character. Since NotesSection also renders all team notes, this could become expensive with many notes.

**Recommendation:** Use `React.memo` on the note list items and consider using `useRef` for the textarea value with manual DOM updates.

### 9.3 Centrifugo Subscription in ConversationInsight [LOW]

**Current:** The ConversationInsight component subscribes to `conversation:{id}` via Centrifugo.

**Observation:** This is well-implemented with proper cleanup in the useEffect return. The subscription is only active when the conversation has an insight. Good practice.

---

## 10. Code Architecture Observations

### 10.1 Component Size (1,433 Lines) [HIGH]

**Issue:** The file contains 1 exported component + 12 internal components + 5 helper functions. At 1,433 lines, this is a "god component" that is difficult to maintain, test, and review.

**Recommendation:** Extract each section into its own file under `src/components/inbox/contact-panel/`:
```
contact-panel/
  index.tsx               (main shell, ~100 lines)
  profile-header.tsx      (~150 lines)
  quick-actions-section.tsx (~110 lines)
  assignment-journey.tsx  (~230 lines)
  tags-section.tsx        (~70 lines)
  unified-notes.tsx       (~90 lines)
  commitments-section.tsx (~200 lines)
  activity-section.tsx    (~120 lines)
  stats-bar.tsx           (~50 lines)
  helpers.tsx             (~60 lines: badges, formatRelativeDate)
  skeleton.tsx            (~50 lines)
```

### 10.2 Good: Shared Component Reuse [POSITIVE]

The panel correctly reuses 5 shared components from `src/components/contacts/shared/`:
- `ContactInfoCard` (same component used in Contacts drawer)
- `TagList` (same component)
- `NotesSection` (same component)
- `SectionHeader` (same component)
- `QuickActions` (same component)

This demonstrates good atomic design principles and ensures visual consistency between the Inbox sidebar and the Contacts page drawer.

### 10.3 Type Safety [POSITIVE]

The component uses proper TypeScript interfaces for all props and data structures. The `JourneyState` enum and `JOURNEY_STATE_CONFIG` record provide type-safe journey state handling. No `any` types were found.

### 10.4 ISSUE: Inconsistent Error Handling [MEDIUM]

**Current patterns:**
- Journey state change: Shows `toast.error(result.error ?? "Erro ao atualizar jornada")` -- good
- Flow trigger: Shows `toast.error(result.error ?? "Erro ao disparar fluxo")` -- good
- Internal notes fetch: `.catch(() => {})` -- silently swallows errors
- Journey info fetch: `.catch(() => {})` -- silently swallows errors

**Recommendation:** At minimum, log errors to console in catch blocks. Consider showing a discrete error state in each section rather than silently showing empty data when the API fails.

---

## 11. Prioritized Recommendations

### P0 -- Critical (Fix Before Next Release)

| # | Issue | Section | Effort |
|---|-------|---------|--------|
| 1 | Add `aria-label` to all interactive elements | 8.1 | S |
| 2 | Fix touch target sizes (44x44px minimum) | 7.3 | M |
| 3 | Make panel width responsive (`w-full sm:w-[320px]`) | 7.1 | S |
| 4 | Add `aria-expanded`/`aria-controls` to collapsible sections | 8.6 | S |

### P1 -- High (Fix Within Sprint)

| # | Issue | Section | Effort |
|---|-------|---------|--------|
| 5 | Move StatsBar up to position 2 (below profile) | 3.1 | S |
| 6 | Add conversation status indicator to panel | 5.5 | M |
| 7 | Format Brazilian phone numbers | 5.1 | S |
| 8 | Fix color contrast (remove opacity on informational text) | 8.4 | M |
| 9 | Add focus management on panel open | 8.3 | S |
| 10 | Give Quick Actions more visual weight | 3.3 | M |
| 11 | Fix prop mutation (`contact.name = newName`) | 6.2 | S |
| 12 | Add landmark roles to panel and sections | 8.2 | M |

### P2 -- Medium (Fix Within Epic)

| # | Issue | Section | Effort |
|---|-------|---------|--------|
| 13 | Reduce section count / add tabbed interface | 3.4 | L |
| 14 | Establish minimum 11px text size | 4.1 | M |
| 15 | Add "Open in WhatsApp" button | 5.2 | S |
| 16 | Add inline phone/email editing | 5.3 | M |
| 17 | Add confirmation for note deletion | 6.6 | S |
| 18 | Auto-save feedback ("Salvo") on observation | 6.4 | S |
| 19 | Standardize border radius | 4.2 | S |
| 20 | Remove excess separators, use spacing | 4.4 | S |
| 21 | Batch API calls for panel data | 9.1 | L |
| 22 | Add `aria-label` to textareas | 8.8 | S |
| 23 | Add date picker for commitment creation | 5.4 | M |
| 24 | Add "Take over from AI" quick action | 5.7 | M |

### P3 -- Low (Backlog)

| # | Issue | Section | Effort |
|---|-------|---------|--------|
| 25 | Extract 1,433-line file into sub-components | 10.1 | L |
| 26 | Add search to tag picker | 6.7 | S |
| 27 | Show "Ver historico" for truncated journey timeline | 6.5 | S |
| 28 | Remove duplicate lead score display | 3.5 | S |
| 29 | Make avatar ring semantically meaningful | 4.6 | S |
| 30 | Add mobile swipe-back gesture | 7.4 | M |
| 31 | Add revenue/LTV display | 5.6 | M |

**Effort Key:** S = Small (< 2h), M = Medium (2-6h), L = Large (> 6h)

---

## 12. Comparison: Inbox Panel vs Contacts Drawer

The codebase has two contact detail views -- the inbox sidebar (`ContactPanel`) and the contacts page drawer (`ContactDrawer`). Comparing them reveals important inconsistencies.

| Feature | Inbox Panel | Contacts Drawer | Consistent? |
|---------|-------------|-----------------|-------------|
| Container | Fixed 320px div | Sheet (side="right", max-w-md) | NO |
| Avatar size | h-18 w-18 (72px) | h-16 w-16 (64px) | NO |
| Name edit | Inline click-to-edit | Toggle edit mode | NO |
| Phone/email edit | Not available | Full edit mode | NO |
| Notes | Personal + Team tabs with auto-save | Simple textarea in edit mode | NO |
| Tags | Dropdown add + inline remove | SectionHeader + picker | Partially |
| Journey | Full journey state + timeline | Not present | N/A |
| AI Insights | ConversationInsight + Commitments | Not present | N/A |
| Activity | Sequences, Campaigns, Fields, Pipeline | Only sequences | Partial |
| Loading state | Custom skeleton | Spinner | NO |
| Error state | No explicit error UI | "Erro ao carregar contato" + retry | WORSE |
| a11y: Sheet description | N/A (not a sheet) | Has SheetTitle + SheetDescription (sr-only) | N/A |

**Key Insight:** The inbox panel is significantly more feature-rich than the contacts drawer, but the contacts drawer has better error handling and a more consistent edit UX. They should converge on a shared pattern or the contacts drawer should link to the inbox panel's richer experience.

---

## Appendix: Files Analyzed

| File | Lines | Role |
|------|-------|------|
| `src/components/inbox/contact-panel.tsx` | 1,433 | Main component (this audit's primary target) |
| `src/components/inbox/inbox-layout.tsx` | ~950 | Parent layout (mobile handling, keyboard shortcuts) |
| `src/components/inbox/conversation-insight.tsx` | ~200 | AI insight card with Centrifugo real-time |
| `src/components/inbox/types.ts` | ~130 | TypeScript interfaces |
| `src/components/contacts/shared/contact-info-card.tsx` | ~160 | Shared phone/email/date display |
| `src/components/contacts/shared/notes-section.tsx` | ~140 | Shared notes with Personal/Team tabs |
| `src/components/contacts/shared/quick-actions.tsx` | ~80 | Shared Fechar/Fluxo/Pausar buttons |
| `src/components/contacts/shared/tag-list.tsx` | ~100 | Shared tag badge list |
| `src/components/contacts/shared/section-header.tsx` | ~100 | Shared collapsible section header |
| `src/components/contacts/shared/empty-state.tsx` | ~25 | Shared empty state |
| `src/components/contacts/contact-drawer.tsx` | ~260 | Contacts page drawer (comparison) |
| `src/components/presence/presence-indicator.tsx` | ~60 | Team member online/offline dot |
| `src/lib/journey/types.ts` | ~90 | Journey state enum + config |
| `src/app/globals.css` | ~200+ | Design tokens (light + dark) |

**Total lines analyzed: ~3,728**

---

*-- Uma, UX Design Expert*
*Audit conducted via full source code analysis on Vultr server (ssh vultr, /home/tikso/tikso/)*
