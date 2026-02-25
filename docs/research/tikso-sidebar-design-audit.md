# Tikso CRM -- Contact Detail Sidebar: Visual/Interaction Design Audit

> **Agent:** Design Chief (routing UX Design audit)
> **Specialist Domain:** UX/UI Visual Design, Interaction Patterns, CRM Information Architecture
> **Date:** 2026-02-25
> **Status:** Complete -- Ready for Implementation
> **Reference Docs:**
> - `tikso-design-system.md` (Brad Frost -- Token Architecture)
> - `tikso-ux-redesign-proposal.md` (Uma -- UX Redesign)
> - `tikso-world-best-crms-analysis.md` (Atlas -- Competitive Analysis)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current Layout Analysis](#2-current-layout-analysis)
3. [Audit 1: Information Hierarchy](#3-audit-1-information-hierarchy)
4. [Audit 2: Visual Density](#4-audit-2-visual-density)
5. [Audit 3: Interaction Patterns](#5-audit-3-interaction-patterns)
6. [Audit 4: Empty States](#6-audit-4-empty-states)
7. [Audit 5: Color Usage](#7-audit-5-color-usage)
8. [Audit 6: Typography Hierarchy](#8-audit-6-typography-hierarchy)
9. [Audit 7: Spacing and Grouping](#9-audit-7-spacing-and-grouping)
10. [Recommended Layout: ASCII Wireframes](#10-recommended-layout-ascii-wireframes)
11. [Component-Level Specifications](#11-component-level-specifications)
12. [Implementation Priority](#12-implementation-priority)
13. [Auto-Decisions Log](#13-auto-decisions-log)

---

## 1. Executive Summary

The contact detail sidebar is the **single most visited panel** in a CRM after the conversation view. Every time a team member opens a conversation, this sidebar provides the context they need to decide how to respond. In a WhatsApp-first CRM for barbershops, the sidebar must answer three questions in under 3 seconds:

1. **Who is this person?** (name, phone, how long they have been a customer)
2. **What is their status?** (journey stage, assigned agent, engagement level)
3. **What should I do next?** (upcoming appointments, pending actions, suggested follow-up)

### Overall Verdict

The current sidebar has a **solid foundation** but suffers from seven specific problems:

| Problem | Severity | Impact |
|---------|----------|--------|
| Information hierarchy is inverted -- identity takes too much space, actionable data is buried | HIGH | User cannot quickly assess what to do next |
| Quick actions are text links, not discoverable buttons | HIGH | Critical actions (start flow, pause) get missed |
| Empty states are passive dead-ends | HIGH | "Nenhuma tag" and "Nenhum compromisso" waste space and miss onboarding opportunities |
| No visual distinction between data sections | MEDIUM | Everything runs together in a flat list |
| Brand palette is underused -- no color accents | MEDIUM | Sidebar feels generic, not like Tikso |
| Activity section is too minimal (just two numbers) | MEDIUM | Score of "0" with no context is meaningless |
| Typography lacks clear weight hierarchy | LOW | Labels and values compete for attention |

---

## 2. Current Layout Analysis

### 2.1 Current Structure (As Described)

```
+--------------------------------------+
|  Detalhes do Contato                 |  <- Section title
|                                      |
|           KP                         |  <- Avatar circle (initials)
|                                      |
|       Kelmer Palma                   |  <- Name (centered)
|  Telefone: 5579999811988             |  <- Phone (label:value)
|  E-mail: Nao informado              |  <- Email (label:value, empty)
|  Data de inscricao: 23 de fev 2026  |  <- Date (label:value)
|                                      |
|  Acoes rapidas:                      |  <- Section label
|  Fechar | Fluxo | Pausar            |  <- Text links
|                                      |
|  Atribuicao e Jornada:              |  <- Section label
|  Atribuido a: Nao atribuido         |  <- Assignment (empty)
|  Jornada: Desconhecido (Alterar)    |  <- Journey (unknown)
|  Desde ha 2 dias                     |  <- Duration
|                                      |
|  Tags: Nenhuma tag adicionada        |  <- Tags (empty)
|                                      |
|  Notas: Pessoal | Equipe            |  <- Notes tabs
|  "Adicione uma observacao sobre..."  |  <- Note input placeholder
|                                      |
|  Inteligencia                        |  <- Section label
|                                      |
|  Compromissos:                       |  <- Section label
|  "Adicionar compromisso..."          |  <- Action placeholder
|  "Nenhum compromisso registrado"     |  <- Empty state
|                                      |
|  Atividade:                          |  <- Section label
|  16h Ultima msg                      |  <- Last message time
|  0 Score                             |  <- Engagement score
+--------------------------------------+
```

### 2.2 Section Inventory

| Section | Lines Used (approx) | Information Value | Action Value |
|---------|---------------------|-------------------|--------------|
| Header + Avatar + Name | 5-6 lines | HIGH (identity) | NONE |
| Contact details (phone, email, date) | 3 lines | MEDIUM | LOW (no click-to-call) |
| Quick actions | 2 lines | N/A | HIGH (but poor discoverability) |
| Assignment + Journey | 3-4 lines | HIGH (status) | MEDIUM (Alterar link) |
| Tags | 1-2 lines | MEDIUM | LOW (no add button visible) |
| Notes | 3-4 lines | MEDIUM | MEDIUM (input present) |
| Intelligence | 1 line | ZERO (label only) | NONE |
| Compromissos | 3 lines | MEDIUM | MEDIUM (add placeholder) |
| Activity | 2 lines | HIGH | NONE |

**Key observation:** The highest-value sections (Activity, Intelligence, Compromissos) are at the BOTTOM where they require scrolling. The lowest-value section (the avatar and centered name layout) occupies the most premium real estate at the TOP.

---

## 3. Audit 1: Information Hierarchy

### 3.1 What CRM Sidebars Must Prioritize

Based on the competitive analysis (`tikso-world-best-crms-analysis.md`), the best CRM contact panels follow this priority:

| Priority | Content | Rationale |
|----------|---------|-----------|
| P0 | Identity (name + primary contact method) | "Who am I talking to?" |
| P0 | Status indicator (journey stage + engagement) | "Where are they in my funnel?" |
| P1 | Next action (upcoming appointment, pending task) | "What do I need to do?" |
| P1 | Quick actions (call, flow, assign) | "How do I act on this?" |
| P2 | Context (tags, notes, history) | "What do I already know?" |
| P3 | Intelligence (score, analytics, AI insights) | "What does the system know?" |

### 3.2 Current Problems

**Problem 1: The avatar and name occupy excessive vertical space.**
The centered layout with a large avatar circle, name below it, then three label:value pairs consumes approximately 30% of the visible sidebar area. In a CRM, identity confirmation should take 1-2 seconds and 15% of space maximum.

**Problem 2: "Acoes rapidas" appears AFTER contact details.**
Quick actions like "Fluxo" (trigger automation) and "Pausar" (pause AI) are critical operational controls. Placing them after the phone/email/date block means the user must visually scan past low-priority information to reach high-priority actions.

**Problem 3: Activity data is at the very bottom.**
"16h Ultima msg" and "0 Score" are among the most actionable data points -- they tell the agent whether this contact is engaged or going cold. These are buried below empty sections (empty tags, empty commitments).

**Problem 4: "Inteligencia" section is a label with no content.**
An empty section header wastes space and creates false expectation. If there is no intelligence data yet, this section should not be shown at all, or it should show an actionable prompt.

### 3.3 Recommendations

| Change | Effort | Impact |
|--------|--------|--------|
| Move avatar + name to a compact horizontal layout (avatar left, name + phone right) | SMALL | HIGH -- saves 3-4 lines of vertical space |
| Move quick actions immediately below the identity row | SMALL | HIGH -- actions are always visible without scrolling |
| Move activity/engagement data into a compact status bar right below identity | SMALL | HIGH -- most actionable data visible first |
| Move journey + assignment into a visual "status card" with color coding | MEDIUM | HIGH -- status becomes scannable |
| Push notes and intelligence below the fold (they are reference, not action) | SMALL | MEDIUM -- reduces clutter above fold |
| Remove "Inteligencia" section header when empty | SMALL | LOW -- removes dead space |

---

## 4. Audit 2: Visual Density

### 4.1 CRM Density Benchmarks

| CRM | Sidebar Density | Strategy |
|-----|-----------------|----------|
| HubSpot | HIGH -- dense property list with collapsible sections | Works for power users, overwhelming for SMB |
| Kommo | MEDIUM -- card-based sections with clear boundaries | Good balance, each section is a distinct card |
| Pipedrive | MEDIUM -- clean list with smart grouping | Simple, fast to scan |
| Respond.io | LOW-MEDIUM -- minimal sidebar, expand on demand | Clean but hides too much |

### 4.2 Current Problems

**Problem 5: Everything is at the same visual density.**
The current layout presents phone, email, date, assignment, journey, tags, notes, and activity all at the same visual weight. Nothing stands out. When everything looks the same, nothing gets noticed.

**Problem 6: Empty data inflates the layout.**
"E-mail: Nao informado", "Tags: Nenhuma tag adicionada", "Nenhum compromisso registrado" -- these three empty states consume approximately 15-20% of the sidebar while providing zero information. They push valuable content further down.

**Problem 7: No collapsible sections.**
Unlike HubSpot and Kommo which use collapsible sections to manage density, the current sidebar shows everything open at all times. This is acceptable for a 5-section panel but becomes problematic when sections are often empty.

### 4.3 Recommendations

| Change | Effort | Impact |
|--------|--------|--------|
| Use card-based sections with subtle borders or background differences (per design system `--surface-sunken` for section containers) | MEDIUM | HIGH -- creates visual rhythm and scanability |
| Collapse empty sections by default, show only a compact "add" prompt | SMALL | HIGH -- removes visual noise, surfaces content below |
| Use a 2-column grid for compact data points (e.g., "Atribuido" and "Jornada" side by side) | SMALL | MEDIUM -- reduces vertical space by 30% for metadata |
| Add visual separators between section groups using `--border` token (slate-200) | SMALL | MEDIUM -- prevents the "wall of text" feeling |

---

## 5. Audit 3: Interaction Patterns

### 5.1 Current Quick Actions Analysis

The current quick actions are presented as: `Fechar | Fluxo | Pausar`

This has several problems:

**Problem 8: Text-only actions with no visual affordance.**
"Fechar", "Fluxo", and "Pausar" are plain text separated by pipes. There is no visual signal that these are interactive elements. In mobile use (80% of Tikso sessions per the UX redesign proposal), tap targets for text links are unreliable and frustrating.

**Problem 9: "Fechar" is not a contact action -- it is a UI action.**
"Fechar" (close) closes the sidebar panel. It is a navigation control, not a contact action. Mixing navigation controls with domain actions ("Fluxo", "Pausar") in the same row creates confusion about what each button does.

**Problem 10: Missing critical actions.**
For a WhatsApp CRM, the most common sidebar actions are:
- Call/WhatsApp (initiate conversation)
- Assign to team member
- Add to flow/automation
- Pause/resume AI
- Add tag
- Create appointment

The current sidebar only exposes 3 of these (and one is just "close panel").

### 5.2 Journey State Change

"Jornada: Desconhecido (Alterar)" -- the "(Alterar)" link is the only way to change a contact's journey stage. This interaction has problems:

**Problem 11: "Desconhecido" is the default journey state, which is useless.**
A new contact should be automatically assigned a journey stage based on their entry point. If they came through WhatsApp, they should start at "Novo Lead" or "Primeiro Contato", not "Desconhecido".

**Problem 12: "(Alterar)" is a parenthetical afterthought.**
Changing the journey stage is a primary CRM action -- it moves the contact through the funnel. Making it a small parenthetical text link buries a critical workflow step.

### 5.3 Recommendations

| Change | Effort | Impact |
|--------|--------|--------|
| Replace text links with icon buttons in a horizontal action bar | SMALL | HIGH -- clear affordance, proper tap targets |
| Separate "Fechar" (X button in panel header) from contact actions | SMALL | HIGH -- eliminates confusion |
| Add icon buttons for: WhatsApp, Assign, Flow, Pause, Tag, Appointment | MEDIUM | HIGH -- all common actions in one row |
| Replace "(Alterar)" with a visual journey stepper/dropdown | MEDIUM | HIGH -- journey management becomes a first-class interaction |
| Auto-assign initial journey stage based on entry source (WhatsApp = "Novo Lead") | MEDIUM | MEDIUM -- eliminates "Desconhecido" for new contacts |
| Add tooltip or label to each icon button on hover | SMALL | MEDIUM -- accessibility and discoverability |

---

## 6. Audit 4: Empty States

### 6.1 Current Empty States

| Field | Empty State Text | Problem |
|-------|-----------------|---------|
| Email | "Nao informado" | Passive, no way to add |
| Assignment | "Nao atribuido" | Critical field left empty without prompting action |
| Journey | "Desconhecido" | Meaningless default |
| Tags | "Nenhuma tag adicionada" | Dead end, no inline add |
| Notes | "Adicione uma observacao..." | Acceptable -- has input affordance |
| Compromissos | "Nenhum compromisso registrado" | Dead end after action prompt |

### 6.2 Empty State Design Principles

Good empty states must do three things:
1. **Explain** what this section is for (education)
2. **Invite** the user to take action (CTA)
3. **Feel lightweight** so they do not dominate the layout

### 6.3 Recommendations

**Email: "Nao informado"**
- Replace with: clickable text "Adicionar e-mail" in muted color with a small plus icon
- On click: inline input field appears
- Rationale: transforms dead data into a micro-interaction that enriches the contact

**Assignment: "Nao atribuido"**
- Replace with: avatar placeholder with "Atribuir" label, styled as a subtle button
- On click: dropdown with team members
- Optional: if Eli is handling, show Eli's avatar with "Eli esta atendendo" badge
- Rationale: makes assignment feel like an active choice, not a missing field

**Journey: "Desconhecido"**
- Replace with: journey stage selector styled as a colored badge/chip
- New contacts should auto-assign to "Novo Lead" (not "Desconhecido")
- Show as: `[Novo Lead v]` -- a selectable chip that opens a dropdown
- Rationale: journey management is core CRM functionality, not an afterthought

**Tags: "Nenhuma tag adicionada"**
- Replace with: `[+ Adicionar tag]` chip in muted/dashed border
- On click: tag input with autocomplete from existing tags
- Hide the label "Tags:" entirely when there are no tags -- the add button is self-explanatory
- Rationale: invites enrichment without wasting vertical space

**Compromissos: "Nenhum compromisso registrado"**
- Replace with: single-line `[+ Agendar compromisso]` button
- Remove the redundant "Adicionar compromisso..." AND "Nenhum compromisso registrado" double-messaging
- Rationale: one clear CTA is better than an action prompt followed by a "nothing here" message

**Activity: "0 Score"**
- Replace with: if score is 0, show "Novo contato -- sem interacoes" with a small info icon
- On hover: tooltip explaining what the engagement score measures
- Rationale: "0 Score" is meaningless without context. Users need to understand the scale.

---

## 7. Audit 5: Color Usage

### 7.1 Current Color Analysis

Based on the described layout, the sidebar appears to use:
- **Dark text** (#1E293B) for all content -- names, labels, values
- **Avatar** with brand color background (likely orange #FA6810 or teal #0D9488)
- **No semantic color coding** for status, journey, or activity

This is a monochromatic sidebar with no visual energy.

### 7.2 Brand Palette Application Points

Per the design system (`tikso-design-system.md`), the Pulse Mark brand has these tokens available:

| Token | Value | Sidebar Application |
|-------|-------|---------------------|
| `--primary` (teal-600) | #0D9488 | Avatar bg, active journey badge, primary action buttons |
| `--secondary` (coral-500) | #F97066 | Notification badges, urgency indicators, overdue markers |
| `--success` | #22C55E | Confirmed appointments, healthy engagement score |
| `--warning` | #EAB308 | Pending assignments, stale contacts |
| `--destructive` | #EF4444 | Paused status, overdue tasks |
| `--ai-accent` (violet) | #7C3AED | Eli status indicator, AI-generated tags |
| `--muted-foreground` (slate-500) | #64748B | Labels, secondary text, timestamps |
| `--accent` (teal-50) | #F0FDFA | Highlighted section backgrounds |
| `--border` (slate-200) | #E2E8F0 | Section separators |

### 7.3 Recommendations

| Element | Current | Recommended | Token |
|---------|---------|-------------|-------|
| Avatar background | Single color | Teal-600 with white initials | `--primary` / `--primary-foreground` |
| Journey badge | Plain text "Desconhecido" | Colored chip: teal for active stages, yellow for unknown, green for converted | `--primary`, `--warning`, `--success` |
| Engagement score | "0 Score" plain text | Color-coded ring: red (cold), yellow (warm), green (hot) | Semantic tokens |
| Quick action icons | No color | Teal-700 for primary actions, slate-500 for secondary | `--primary-text`, `--muted-foreground` |
| Tags | Plain text | Colored chips matching tag categories (use badge variants from design system) | Badge variant tokens |
| "Eli esta atendendo" | Not present | Purple badge with AI accent | `--ai-accent` |
| Section headers | Same as body text | Smaller, uppercase, wider tracking, muted color | `--muted-foreground`, `--tracking-wider` |
| Last message time "16h" | Plain text | Orange/coral if > 24h (going cold), green if < 1h (active) | `--secondary-text` (coral) for cold, `--success-text` for active |

---

## 8. Audit 6: Typography Hierarchy

### 8.1 Current Typography Problems

**Problem 13: Everything appears to be the same font size and weight.**
The layout description shows "Detalhes do Contato", "Kelmer Palma", field labels, field values, section headers, and action links all at what appears to be similar visual weight. When the type hierarchy is flat, the eye has no guidance.

**Problem 14: Labels compete with values.**
"Telefone: 5579999811988" -- the label "Telefone:" and the value "5579999811988" are at the same visual weight. In information-dense panels, labels should recede and values should stand out.

### 8.2 Recommended Typography Hierarchy

Using the design system's type combinations:

| Element | Font | Size | Weight | Color | Token Reference |
|---------|------|------|--------|-------|-----------------|
| Panel title "Detalhes do Contato" | DM Sans | 14px (text-sm) | 600 (semibold) | slate-800 | `--font-heading`, `--text-sm`, `--font-semibold` |
| Contact name "Kelmer Palma" | DM Sans | 20px (text-xl) | 600 (semibold) | slate-800 | `--font-heading`, `--text-xl`, `--font-semibold` |
| Phone number | Inter | 14px (text-sm) | 400 (normal) | slate-800 | `--font-body`, `--text-sm`, `--font-normal` |
| Field labels ("Telefone", "E-mail") | Inter | 12px (text-xs) | 500 (medium) | slate-500 | `--font-body`, `--text-xs`, `--font-medium`, `--muted-foreground` |
| Field values | Inter | 14px (text-sm) | 400 (normal) | slate-800 | `--font-body`, `--text-sm`, `--font-normal` |
| Section headers ("Atribuicao e Jornada") | Inter | 11px (text-xs) | 500 (medium) | slate-400 | `--text-xs`, `--font-medium`, uppercase, `--tracking-wider` |
| Action button labels | Inter | 12px (text-xs) | 500 (medium) | teal-700 | `--text-xs`, `--font-medium`, `--primary-text` |
| Empty state text | Inter | 13px (text-sm) | 400 (normal) | slate-400 | `--text-sm`, `--muted-foreground` |
| Engagement metrics | DM Sans | 24px (text-2xl) | 700 (bold) | slate-800 | `--font-heading`, `--text-2xl`, `--font-bold` |
| Metric labels | Inter | 11px (text-xs) | 500 (medium) | slate-500 | `--text-xs`, `--font-medium`, `--tracking-wide` |

### 8.3 Key Principle: Labels Recede, Values Dominate

```
WRONG (current):
  Telefone: 5579999811988        <- Same weight, competing

RIGHT (recommended):
  TELEFONE                        <- xs, medium, slate-400, uppercase
  +55 79 9999-81988               <- sm, normal, slate-800, formatted
```

Notice also the phone number formatting. Raw "5579999811988" is hard to read. Format as "+55 79 9999-81988" for Brazilian numbers.

---

## 9. Audit 7: Spacing and Grouping

### 9.1 Current Spacing Problems

**Problem 15: No visual grouping between related sections.**
The current sidebar appears to present all sections as a continuous list with the same spacing between them. "Assignment" and "Journey" are related (both describe status) but are visually indistinguishable from the gap between "Tags" and "Notes".

**Problem 16: The notes section has too much vertical commitment.**
"Notas: Pessoal | Equipe" plus the input placeholder takes 3-4 lines for what is often empty space. Notes are reference data, not primary actions.

### 9.2 Recommended Grouping

The sidebar should be organized into 4 distinct visual groups:

```
GROUP 1: IDENTITY (always visible, compact)
  - Avatar + Name + Phone (horizontal layout)
  - Quick action icon bar

GROUP 2: STATUS (always visible, color-coded)
  - Journey stage (colored badge)
  - Assignment (avatar or "Atribuir")
  - Engagement summary (score + last activity)

GROUP 3: CONTEXT (visible, expandable)
  - Tags (chips or "add" prompt)
  - Upcoming appointments (next 1-2 or "add" prompt)

GROUP 4: REFERENCE (below fold, collapsible)
  - Notes (Pessoal | Equipe tabs)
  - Full activity log
  - AI intelligence panel (when populated)
```

### 9.3 Spacing Token Application

| Between | Spacing Token | Pixels |
|---------|--------------|--------|
| Panel edge to content | `--space-card` | 24px (or `--space-card-compact` = 16px for narrow sidebars) |
| Within a group (items) | `--space-stack-sm` | 8px |
| Between groups | `--space-stack-lg` | 24px |
| Group header to first item | `--space-stack-xs` | 4px |
| Icon button spacing | `--space-inline-md` | 12px |
| Section divider line margin | `--space-stack-md` top and bottom | 16px |

---

## 10. Recommended Layout: ASCII Wireframes

### 10.1 Redesigned Sidebar -- Desktop (360px width)

```
+--------------------------------------+
|  Detalhes do Contato            [X]  |  <- Panel header, close button
+--------------------------------------+
|                                      |
|  [KP]  Kelmer Palma                  |  <- Avatar (40px) + Name (text-xl)
|        +55 79 9999-81988    [copy]   |  <- Phone formatted + copy icon
|        Cliente desde 23 Fev          |  <- Compact date
|                                      |
|  [WhatsApp] [Atribuir] [Fluxo]      |  <- Icon buttons row 1
|  [Agendar]  [Tag]      [Pausar]     |  <- Icon buttons row 2
|                                      |
+- - - - - - - - - - - - - - - - - - -+  <- Subtle divider (--border)
|                                      |
|  STATUS                              |  <- Section label (xs, uppercase)
|                                      |
|  +----------------------------------+|
|  |  [Novo Lead v]    Desde 2 dias   ||  <- Journey badge + duration
|  |                                  ||
|  |  [Eli avatar] Eli esta atendendo ||  <- Assignment (AI indicator)
|  +----------------------------------+|
|                                      |
|  +-------+  +-------+  +-------+    |
|  | 16h   |  |  0    |  |  1    |    |  <- Metric mini-cards
|  | ult.  |  | score |  | conv. |    |
|  | msg   |  |       |  |       |    |
|  +-------+  +-------+  +-------+    |
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  TAGS                                |  <- Section label
|  [+ Adicionar tag]                   |  <- Dashed chip, add action
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  PROXIMO COMPROMISSO                 |  <- Section label
|  [+ Agendar compromisso]            |  <- Single CTA when empty
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  NOTAS          [Pessoal] [Equipe]   |  <- Tabs
|  +----------------------------------+|
|  | Adicione uma observacao...       ||  <- Input area
|  +----------------------------------+|
|                                      |
+--------------------------------------+
```

### 10.2 Redesigned Sidebar -- With Populated Data

```
+--------------------------------------+
|  Detalhes do Contato            [X]  |
+--------------------------------------+
|                                      |
|  [KP]  Kelmer Palma                  |
|        +55 79 9999-81988    [copy]   |
|        kelmer@email.com              |
|        Cliente desde 23 Fev          |
|                                      |
|  [WhatsApp] [Atribuir] [Fluxo]      |
|  [Agendar]  [Tag]      [Pausar]     |
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  STATUS                              |
|                                      |
|  +----------------------------------+|
|  |  [Em Conversa v]  Desde 2 dias  ||
|  |                                  ||
|  |  [Carlos R.]  Atribuido         ||
|  +----------------------------------+|
|                                      |
|  +-------+  +-------+  +-------+    |
|  | 2h    |  |  42   |  |  3    |    |
|  | ult.  |  | score |  | conv. |    |
|  | msg   |  | [===] |  |       |    |
|  +-------+  +-------+  +-------+    |
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  TAGS                                |
|  [VIP] [Barba] [Fiel]  [+]          |
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  PROXIMO COMPROMISSO                 |
|  +----------------------------------+|
|  |  Ter 25 Fev, 14:00              ||
|  |  Corte + Barba                   ||
|  |  [CONFIRMADO]                    ||
|  +----------------------------------+|
|  [Ver todos (3)]                     |
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  NOTAS          [Pessoal] [Equipe]   |
|  +----------------------------------+|
|  | "Cliente VIP, sempre pede         ||
|  |  desconto no combo. Oferecer     ||
|  |  10% max." -- Carlos, 20 Fev    ||
|  +----------------------------------+|
|  | Adicione uma observacao...       ||
|  +----------------------------------+|
|                                      |
+- - - - - - - - - - - - - - - - - - -+
|                                      |
|  INTELIGENCIA DA ELI                 |  <- Only shown when populated
|  +----------------------------------+|
|  |  [Bot] 3 conversas atendidas     ||
|  |  Ultimo tema: preco do combo     ||
|  |  Sentimento: positivo            ||
|  +----------------------------------+|
|                                      |
+--------------------------------------+
```

### 10.3 Redesigned Sidebar -- Mobile (Full Width Sheet)

On mobile, the sidebar becomes a bottom sheet that slides up from the bottom. The layout is the same but with some mobile-specific adaptations:

```
+--------------------------------------+
|  ---- (drag handle) ----             |  <- Bottom sheet handle
+--------------------------------------+
|                                      |
|  [KP]  Kelmer Palma            [X]  |
|        +55 79 9999-81988             |
|                                      |
|  [WhatsApp] [Atribuir] [Fluxo]      |  <- Horizontally scrollable
|  [Agendar]  [Tag]      [Pausar]     |  <- on very narrow screens
|                                      |
+--------------------------------------+
|                                      |
|  [Novo Lead v]       16h ultima msg  |  <- Compact status row
|  [Eli atendendo]     Score: 0        |
|                                      |
+--------------------------------------+
|  ... (scrollable sections below)     |
+--------------------------------------+
```

### 10.4 Quick Action Bar -- Detailed Wireframe

```
+--------------------------------------+
|                                      |
|  +----+  +--------+  +------+       |
|  |    |  |        |  |      |       |
|  | WA |  | Assign |  | Flow |       |
|  | [] |  | [+]    |  | [>>] |       |
|  +----+  +--------+  +------+       |
|                                      |
|  +------+  +-----+  +-------+       |
|  |      |  |     |  |       |       |
|  | Cal  |  | Tag |  | Pause |       |
|  | [+]  |  | [#] |  | [||]  |       |
|  +------+  +-----+  +-------+       |
|                                      |
+--------------------------------------+

Button specs:
- Size: 48x40px (meets 44px minimum tap target)
- Border radius: --radius-md (6px)
- Background: transparent
- Border: 1px solid --border (slate-200)
- Icon color: --primary-text (teal-700)
- Hover: bg --accent (teal-50)
- Label: text-xs below icon, --muted-foreground
- Grid: 3 columns, --space-inline-sm (8px) gap
```

### 10.5 Engagement Metrics Row -- Detailed Wireframe

```
+----------+  +----------+  +----------+
|          |  |          |  |          |
|   16h    |  |    0     |  |    1     |
|          |  |          |  |          |
|  ultima  |  |  score   |  | conversa |
|   msg    |  |          |  |          |
+----------+  +----------+  +----------+

   AMBER        GRAY          TEAL

Metric mini-card specs:
- Size: equal-width columns, fill available space
- Background: --surface-sunken (slate-100)
- Border radius: --radius-DEFAULT (8px)
- Padding: --space-2 (8px) vertical, --space-3 (12px) horizontal
- Value: text-lg, font-heading (DM Sans), font-bold, --foreground
- Label: text-xs, font-body (Inter), --muted-foreground
- Color coding:
  - "Ultima msg" value: green if <1h, amber if 1-24h, red if >24h
  - "Score" value: color fill bar below number (0-33 red, 34-66 yellow, 67-100 green)
  - "Conversas" value: always teal-700
```

### 10.6 Journey Badge -- Detailed Wireframe

```
Current:
  Jornada: Desconhecido (Alterar) -- Desde ha 2 dias

Redesigned:
  +--------------------------------------------+
  |                                            |
  |  [Novo Lead  v]              Desde 2 dias  |
  |   ^^^^^^^^^                                |
  |   teal-50 bg                               |
  |   teal-700 text                            |
  |   text-xs, font-medium                     |
  |   rounded-sm (4px)                         |
  |   px-2 py-0.5                              |
  |   dropdown on click                        |
  |                                            |
  +--------------------------------------------+

Journey stage color map:
  Novo Lead      -> teal-50 bg, teal-700 text (primary badge)
  Em Conversa    -> info-light bg, info-text text
  Proposta       -> warning-light bg, warning-text text
  Agendado       -> success-light bg, success-text text
  Convertido     -> success bg, white text (filled)
  Inativo        -> slate-100 bg, slate-500 text (muted badge)
  Desconhecido   -> slate-100 bg, slate-400 text, dashed border
```

---

## 11. Component-Level Specifications

### 11.1 ContactSidebarHeader

```
Component: ContactSidebarHeader
Purpose: Identity + phone + quick actions (always visible, never scrolls)

Props:
  contact: { name, initials, phone, email?, createdAt }
  isAiHandling: boolean
  assignedTo: User | null

Layout:
  - Avatar (40px circle, --radius-full) aligned left
  - Name + phone stacked right of avatar
  - Copy button next to phone (Clipboard icon, 16px)
  - Close button [X] top-right of panel header

Tokens:
  - Avatar bg: --primary (teal-600), text: white
  - Name: font-heading, text-xl (20px), font-semibold, --foreground
  - Phone: text-sm (14px), --foreground, formatted as +55 XX XXXXX-XXXX
  - Date: text-xs (12px), --muted-foreground
```

### 11.2 ContactQuickActions

```
Component: ContactQuickActions
Purpose: Primary actions for this contact

Props:
  contactId: string
  isPaused: boolean
  isAiHandling: boolean

Actions (6 buttons, 3x2 grid):
  1. WhatsApp  -> Opens conversation in inbox
  2. Atribuir  -> Opens team member dropdown
  3. Fluxo     -> Opens flow selector
  4. Agendar   -> Opens appointment creator
  5. Tag       -> Opens tag input with autocomplete
  6. Pausar    -> Toggles AI pause (changes to "Retomar" when paused)

Button variant: Ghost with border (outline)
  - border: 1px solid --border
  - hover bg: --accent (teal-50)
  - icon: 18px, --primary-text (teal-700)
  - label: text-xs, --muted-foreground
  - Pausar when active: --destructive-light bg, --destructive-text icon
```

### 11.3 ContactStatusCard

```
Component: ContactStatusCard
Purpose: Journey + assignment + engagement at a glance

Props:
  journey: { stage, since }
  assignment: { user?, isAi? }
  activity: { lastMessage, score, conversationCount }

Layout:
  - Top row: Journey badge (left) + "Desde X" (right)
  - Second row: Assignment avatar + name (or "Atribuir" CTA)
  - Bottom row: 3 metric mini-cards (equal width)

Background: --surface-sunken (slate-100)
Border radius: --radius-lg (12px)
Padding: --space-card-compact (16px)
```

### 11.4 ContactTagsSection

```
Component: ContactTagsSection
Purpose: Display and manage tags

Props:
  tags: Tag[]
  onAdd: (tag: string) => void
  onRemove: (tagId: string) => void

States:
  - Empty: Single dashed-border chip "[+ Adicionar tag]"
  - Populated: Tag chips in flex-wrap + small [+] button at end
  - Editing: Inline input with autocomplete dropdown

Tag chip:
  - bg: slate-100, text: slate-700 (default badge variant)
  - Or category-colored using badge variant tokens
  - Close icon (X) on hover
  - text-xs, font-medium, rounded-sm (4px), px-2 py-0.5
```

### 11.5 ContactAppointmentSection

```
Component: ContactAppointmentSection
Purpose: Show next appointment or prompt to create one

Props:
  appointments: Appointment[]

States:
  - Empty: "[+ Agendar compromisso]" button (ghost variant)
  - Has next: Mini appointment card (date, service, status badge)
  - Has multiple: Mini card + "[Ver todos (N)]" link

Appointment card:
  - bg: --card (white)
  - border: 1px solid --border
  - border-radius: --radius-DEFAULT (8px)
  - Date: text-sm, font-medium, --foreground
  - Service: text-sm, --foreground
  - Status badge: colored per journey badge pattern
    - CONFIRMADO: success-light bg, success-text
    - PENDENTE: warning-light bg, warning-text
    - CANCELADO: destructive-light bg, destructive-text
```

---

## 12. Implementation Priority

### 12.1 Phase 1: Layout Restructuring (1 day)

| Task | Effort | Impact |
|------|--------|--------|
| Refactor avatar + name to horizontal layout | SMALL | HIGH |
| Move close button to panel header | SMALL | HIGH |
| Reorder sections: Identity > Actions > Status > Tags > Appointments > Notes | SMALL | HIGH |
| Add subtle dividers between section groups using `--border` | SMALL | MEDIUM |
| Format phone number as +55 XX XXXXX-XXXX | SMALL | MEDIUM |

### 12.2 Phase 2: Quick Actions Bar (0.5 day)

| Task | Effort | Impact |
|------|--------|--------|
| Create 3x2 icon button grid component | SMALL | HIGH |
| Implement WhatsApp, Assign, Flow, Schedule, Tag, Pause actions | MEDIUM | HIGH |
| Add tooltip labels on hover | SMALL | MEDIUM |
| Add pause/resume toggle state | SMALL | MEDIUM |

### 12.3 Phase 3: Empty State Redesign (0.5 day)

| Task | Effort | Impact |
|------|--------|--------|
| Replace "Nao informado" with "Adicionar" inline CTAs | SMALL | HIGH |
| Replace "Nenhuma tag" with dashed add-tag chip | SMALL | HIGH |
| Replace double compromisso messaging with single CTA | SMALL | MEDIUM |
| Auto-assign "Novo Lead" journey for new WhatsApp contacts | MEDIUM | HIGH |

### 12.4 Phase 4: Status Card + Metrics (1 day)

| Task | Effort | Impact |
|------|--------|--------|
| Create engagement metric mini-cards (3-column) | MEDIUM | HIGH |
| Add color-coded last-message-time indicator | SMALL | MEDIUM |
| Create journey stage badge with dropdown selector | MEDIUM | HIGH |
| Add Eli assignment indicator with AI accent badge | SMALL | MEDIUM |

### 12.5 Phase 5: Typography + Color Polish (0.5 day)

| Task | Effort | Impact |
|------|--------|--------|
| Apply DM Sans to name and metric values | SMALL | MEDIUM |
| Apply uppercase + tracking-wider to section labels | SMALL | MEDIUM |
| Separate label and value typography weights | SMALL | MEDIUM |
| Apply semantic colors to journey badges | SMALL | MEDIUM |
| Apply color coding to engagement metrics | SMALL | MEDIUM |

### Total Estimated Effort: 3.5 development days

---

## 13. Auto-Decisions Log

| Question | Decision | Reason |
|----------|----------|--------|
| Should the sidebar use the old orange palette or the new teal Pulse Mark palette? | New teal Pulse Mark palette | The design system has been finalized with teal-600 as primary. The sidebar should be consistent with the brand direction. |
| How many quick action buttons? | 6 (WhatsApp, Assign, Flow, Schedule, Tag, Pause) | These cover the 6 most common actions from the inbox context. Based on Kommo and HubSpot patterns which show 4-8 quick actions. |
| Should notes be above or below appointments? | Below | Appointments are more actionable (time-sensitive). Notes are reference material. |
| Should the "Intelligence" section be shown when empty? | No | Empty section headers waste space and create false expectations. Show only when Eli has generated insights. |
| Collapsible sections or flat scroll? | Flat scroll with visual grouping | For a sidebar of this size (7 sections), collapsible accordions add interaction overhead. Visual grouping via spacing and dividers is sufficient. |
| Should email field be shown when empty? | No -- show only the "Adicionar e-mail" CTA | Displaying "E-mail: Nao informado" wastes a line. A subtle add-link is more compact and more actionable. |
| Avatar size? | 40px (compact, not 64px+ centered) | CRM sidebars need to be information-dense. A 40px avatar provides identity confirmation without dominating the layout. HubSpot uses 40px, Kommo uses 36px. |
| Journey default for new contacts? | "Novo Lead" instead of "Desconhecido" | "Desconhecido" is meaningless. If a contact entered through WhatsApp, they are a lead. This matches the pipeline stages from the competitive analysis. |
| Phone number format? | +55 XX XXXXX-XXXX (Brazilian format with spaces) | Raw "5579999811988" is hard to read and hard to copy correctly. Formatted numbers improve scanability and reduce errors. |

---

## Appendix A: Before vs After Comparison

### Before (Current)

```
+--------------------------------------+
|  Detalhes do Contato                 |
|                                      |
|              KP                      |  <- WASTED: large centered avatar
|                                      |
|          Kelmer Palma                |  <- WASTED: centered name
|  Telefone: 5579999811988             |  <- UNCLEAR: unformatted number
|  E-mail: Nao informado              |  <- WASTED: empty field shown
|  Data de inscricao: 23 de fev 2026  |  <- OK but verbose
|                                      |
|  Acoes rapidas:                      |  <- BURIED: below identity block
|  Fechar | Fluxo | Pausar            |  <- POOR: text links, mixed concerns
|                                      |
|  Atribuicao e Jornada:              |  <- OK label
|  Atribuido a: Nao atribuido         |  <- EMPTY: no actionable CTA
|  Jornada: Desconhecido (Alterar)    |  <- POOR: meaningless default
|  Desde ha 2 dias                     |  <- OK
|                                      |
|  Tags: Nenhuma tag adicionada        |  <- EMPTY: dead end
|                                      |
|  Notas: Pessoal | Equipe            |  <- OK
|  "Adicione uma observacao..."        |  <- OK
|                                      |
|  Inteligencia                        |  <- EMPTY: label only
|                                      |
|  Compromissos:                       |  <- OK
|  "Adicionar compromisso..."          |  <- REDUNDANT with below
|  "Nenhum compromisso registrado"     |  <- REDUNDANT with above
|                                      |
|  Atividade:                          |  <- BURIED: most important data
|  16h Ultima msg                      |  <- BURIED: no color coding
|  0 Score                             |  <- MEANINGLESS: no context
+--------------------------------------+

Vertical lines used: ~30
Empty/wasted lines: ~10 (33%)
```

### After (Recommended)

```
+--------------------------------------+
|  Detalhes do Contato            [X]  |
+--------------------------------------+
|                                      |
|  [KP]  Kelmer Palma                  |  <- COMPACT: horizontal layout
|        +55 79 9999-81988    [copy]   |  <- FORMATTED: readable number
|        Cliente desde 23 Fev          |  <- CONCISE: date without label
|                                      |
|  [WA] [Assign] [Flow]               |  <- VISIBLE: icon buttons, row 1
|  [Cal] [Tag]   [Pause]              |  <- VISIBLE: icon buttons, row 2
|                                      |
|- - - - - - - - - - - - - - - - - - -|
|                                      |
|  STATUS                              |
|  +----------------------------------+|
|  |  [Novo Lead v]    Desde 2 dias   ||  <- ACTIONABLE: clickable badge
|  |  [Eli] Eli esta atendendo        ||  <- CLEAR: AI status shown
|  +----------------------------------+|
|                                      |
|  +------+  +------+  +------+       |
|  | 16h  |  |  0   |  |  1   |       |  <- PROMINENT: metrics visible
|  | msg  |  | score|  | conv |       |  <- COLOR-CODED: urgency signals
|  +------+  +------+  +------+       |
|                                      |
|- - - - - - - - - - - - - - - - - - -|
|                                      |
|  TAGS                                |
|  [+ Adicionar tag]                   |  <- ACTIONABLE: invite to add
|                                      |
|- - - - - - - - - - - - - - - - - - -|
|                                      |
|  PROXIMO COMPROMISSO                 |
|  [+ Agendar compromisso]            |  <- SINGLE CTA: no redundancy
|                                      |
|- - - - - - - - - - - - - - - - - - -|
|                                      |
|  NOTAS          [Pessoal] [Equipe]   |
|  +----------------------------------+|
|  | Adicione uma observacao...       ||
|  +----------------------------------+|
|                                      |
+--------------------------------------+

Vertical lines used: ~28
Empty/wasted lines: ~2 (7%)
Information visible above fold: Identity + Actions + Status + Metrics
```

### Key Improvements Summary

| Dimension | Before | After | Improvement |
|-----------|--------|-------|-------------|
| Identity to action (lines) | 8 lines | 4 lines | 2x faster to act |
| Empty state handling | 5 dead-end empty fields | 0 dead-ends, all have CTAs | 100% actionable |
| Quick actions | 3 text links (1 is "close") | 6 icon buttons with clear affordance | 2x more actions, properly styled |
| Engagement data position | Bottom (requires scroll) | Middle (always visible) | No scroll needed |
| Journey management | "(Alterar)" text link | Colored dropdown badge | First-class interaction |
| Color usage | Monochromatic | Semantic color coding on metrics, badges, status | Scannable at a glance |
| Typography hierarchy | Flat (everything same weight) | 4-level hierarchy (heading, value, label, muted) | Clear visual guidance |
| Phone formatting | Raw digits | Brazilian format with spaces | Readable and copyable |
| AI status | Not shown | Purple badge "Eli esta atendendo" | Owner knows AI state |
| Vertical space efficiency | 33% wasted on empty states | 7% minimal overhead | 4.7x more efficient |

---

*Document generated by Design Chief, routing UX Design audit expertise*
*Design system tokens referenced from `tikso-design-system.md` (Brad Frost)*
*Competitive benchmarks referenced from `tikso-world-best-crms-analysis.md` (Atlas)*
*UX principles aligned with `tikso-ux-redesign-proposal.md` (Uma)*
*All spacing, color, and typography values use the established Pulse Mark design token system*
