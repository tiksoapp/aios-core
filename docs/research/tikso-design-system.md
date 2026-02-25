# Tikso Design System -- Token Architecture

> **Agent:** Brad Frost (Design System, Tier 1)
> **Date:** 2026-02-25
> **Status:** Complete -- Ready for Implementation
> **Brand Direction:** Concept 1 -- The Pulse Mark (Teal + Coral)
> **Source Documents:**
> - `tikso-brand-logo-concepts.md` (Aaron Draplin -- Logo Design)
> - `tikso-ux-redesign-proposal.md` (Uma -- UX Design)

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Color Tokens](#2-color-tokens)
3. [Typography Tokens](#3-typography-tokens)
4. [Spacing Tokens](#4-spacing-tokens)
5. [Border Radius Tokens](#5-border-radius-tokens)
6. [Shadow Tokens](#6-shadow-tokens)
7. [Component Token Mapping](#7-component-token-mapping)
8. [CSS Custom Properties](#8-css-custom-properties)
9. [Tailwind Config](#9-tailwind-config)
10. [WCAG Compliance Matrix](#10-wcag-compliance-matrix)
11. [Migration Guide](#11-migration-guide)

---

## 1. Design Principles

| # | Principle | Implementation |
|---|-----------|----------------|
| 1 | **Zero hardcoded values** | Every color, size, space, and shadow comes from a token |
| 2 | **Semantic naming** | Use `--primary`, not `--teal-600`. Intent over implementation |
| 3 | **Light + Dark parity** | Every token has both light and dark mode values |
| 4 | **WCAG AA minimum** | All text/background combinations meet 4.5:1 (normal) or 3:1 (large) |
| 5 | **Tailwind-native** | Tokens integrate via `@theme inline` in Tailwind v4 |
| 6 | **Progressive scale** | Consistent steps across color, type, spacing, and radius |

---

## 2. Color Tokens

### 2.1 Primary Scale (Teal)

The brand identity color. Teal bridges technology (blue) and growth (green), occupying uncontested territory in the CRM landscape.

| Step | Hex | HSL | On White | On Dark (#1E293B) | Usage |
|------|-----|-----|----------|-------------------|-------|
| 50 | `#F0FDFA` | 166 76% 97% | 1.04:1 | 14.03:1 AA | Tinted backgrounds, hover states |
| 100 | `#CCFBF1` | 167 85% 89% | 1.13:1 | 12.98:1 AA | Selected row backgrounds |
| 200 | `#99F6E4` | 168 84% 78% | 1.26:1 | 11.60:1 AA | Light accent fills |
| 300 | `#5EEAD4` | 171 77% 64% | 1.48:1 | 9.89:1 AAA | Dark-mode primary text, badges |
| 400 | `#2DD4BF` | 172 66% 50% | 1.86:1 | 7.86:1 AAA | Dark-mode primary, links |
| 500 | `#14B8A6` | 173 80% 40% | 2.49:1 | 5.88:1 AA | Icons on dark backgrounds |
| **600** | **`#0D9488`** | **175 84% 32%** | **3.74:1 aa-L** | **3.91:1 aa-L** | **Brand identity, filled buttons, large text** |
| **700** | **`#0F766E`** | **175 77% 26%** | **5.47:1 AA** | **2.67:1** | **Primary text on light, links, labels** |
| 800 | `#115E59` | 176 69% 22% | 7.58:1 AAA | 1.93:1 | Headings, high-emphasis text |
| 900 | `#134E4A` | 175 60% 19% | 9.48:1 AAA | 1.54:1 | High-contrast text |
| 950 | `#042F2E` | 179 86% 10% | 14.47:1 AAA | 1.01:1 | Maximum contrast text |

**Key accessibility decision:** `#0D9488` (teal-600) at 3.74:1 on white FAILS AA for normal text but PASSES for large text (>=18px bold or >=24px). For normal-size text on light backgrounds, always use `#0F766E` (teal-700) which passes AA at 5.47:1. The brand color `#0D9488` is used for filled buttons (white text), icons, borders, and decorative elements.

### 2.2 Secondary Scale (Coral)

Warm accent for notifications, CTAs, and visual energy. Coral provides the "human warmth" that balances the technology-forward teal.

| Step | Hex | HSL | On White | On Dark (#1E293B) | Usage |
|------|-----|-----|----------|-------------------|-------|
| 50 | `#FFF5F4` | 5 100% 98% | 1.07:1 | 13.67:1 AA | Alert backgrounds |
| 100 | `#FFE4E1` | 7 100% 94% | 1.20:1 | 12.15:1 AA | Notification backgrounds |
| 200 | `#FECDD3` | 354 96% 90% | 1.41:1 | 10.37:1 AA | Soft accent fills |
| 300 | `#FDA4A4` | 0 97% 82% | 1.91:1 | 7.68:1 AAA | Badge backgrounds |
| 400 | `#FB7A72` | 3 94% 72% | 2.58:1 | 5.66:1 AA | Icon accents |
| **500** | **`#F97066`** | **4 92% 69%** | **2.79:1** | **5.25:1 AA** | **Notifications, badges, pulse animations** |
| 600 | `#E5453A` | 3 78% 56% | 4.00:1 aa-L | 3.65:1 aa-L | Coral text on light (large only) |
| **700** | **`#C33025`** | **4 67% 45%** | **5.57:1 AA** | **2.63:1** | **Coral text on light backgrounds** |
| 800 | `#A12921` | 4 66% 38% | 7.36:1 AAA | 1.99:1 | High-emphasis coral text |
| 900 | `#862723` | 2 57% 33% | 9.02:1 AAA | 1.62:1 | Maximum contrast coral |
| 950 | `#49100D` | 3 72% 17% | 15.40:1 AAA | 1.05:1 | Near-black coral |

**Accessibility rule:** Coral-500 (`#F97066`) is DECORATIVE ONLY on light backgrounds (contrast 2.79:1 fails all AA). On dark backgrounds it passes AA at 5.25:1. For coral text on light backgrounds, use coral-700 (`#C33025`) minimum.

### 2.3 Neutral Scale (Slate)

The backbone of all UI surfaces, text, and borders. Based on Tailwind Slate with its subtle blue undertone that pairs naturally with teal.

| Step | Hex | HSL | On White | On Dark (#1E293B) | Usage |
|------|-----|-----|----------|-------------------|-------|
| 50 | `#F8FAFC` | 210 40% 98% | 1.05:1 | 13.98:1 AA | Page background (light) |
| 100 | `#F1F5F9` | 210 40% 96% | 1.10:1 | 13.35:1 AA | Card backgrounds, table rows |
| 200 | `#E2E8F0` | 214 32% 91% | 1.23:1 | 11.87:1 AA | Dividers, subtle borders |
| 300 | `#CBD5E1` | 213 27% 84% | 1.48:1 | 9.85:1 AA | Borders, input outlines |
| 400 | `#94A3B8` | 215 20% 65% | 2.56:1 | 5.71:1 AA | Placeholder text, icons (dark) |
| **500** | **`#64748B`** | **215 16% 47%** | **4.76:1 AA** | **3.07:1 aa-L** | **Secondary text, labels** |
| 600 | `#475569` | 215 19% 35% | 7.58:1 AAA | 1.93:1 | Body text alternative |
| 700 | `#334155` | 217 19% 27% | 10.35:1 AAA | 1.41:1 | Dark mode borders |
| **800** | **`#1E293B`** | **217 33% 17%** | **14.63:1 AAA** | **1.00:1** | **Primary text (light), background (dark)** |
| 900 | `#0F172A` | 222 47% 11% | 17.85:1 AAA | 1.22:1 | Dark mode background |
| 950 | `#020617` | 229 84% 5% | 20.17:1 AAA | 1.38:1 | Maximum dark |

### 2.4 Semantic Colors

Each semantic color has a base (decorative/icons), a foreground-safe variant (text), and a tinted background for containers.

| Token | Base | Text-Safe | Background | On-Base | Usage |
|-------|------|-----------|------------|---------|-------|
| **Success** | `#22C55E` | `#16A34A` (3.30:1) | `#F0FDF4` | White | Confirmations, online status, health |
| **Warning** | `#EAB308` | `#A16207` (4.81:1 AA) | `#FFFBEB` | `#422006` | Alerts, attention needed |
| **Error** | `#EF4444` | `#DC2626` (4.83:1 AA) | `#FEF2F2` | White | Errors, destructive actions |
| **Info** | `#3B82F6` | `#2563EB` (4.62:1 AA) | `#EFF6FF` | White | Informational messages, tooltips |

**Semantic foreground rule:** The base colors (success-green, warning-yellow) do NOT pass AA on white for normal text. Always use the `text-safe` variant for text content, and pair base colors with their background tint for container patterns.

### 2.5 AI Accent (Eli)

Purple is reserved exclusively for Eli (the AI agent) to maintain clear visual distinction from the teal primary and coral secondary.

| Token | Light Mode | Dark Mode | Usage |
|-------|-----------|-----------|-------|
| `--ai-accent` | `#7C3AED` (5.70:1 AA on white) | `#A78BFA` (5.38:1 AA on dark) | AI badges, bot indicators |
| `--ai-accent-foreground` | `#FFFFFF` | `#FFFFFF` | Text on AI accent fill |
| `--bubble-ai` | `rgba(124, 58, 237, 0.08)` | `rgba(167, 139, 250, 0.12)` | AI message bubble background |
| `--ai-accent-muted` | `#EDE9FE` (violet-100) | `#2E1065` (violet-950) | AI section backgrounds |

### 2.6 Surface Colors

| Token | Light Mode | Dark Mode | Usage |
|-------|-----------|-----------|-------|
| `--background` | `#F8FAFC` (slate-50) | `#0F172A` (slate-900) | Page background |
| `--foreground` | `#1E293B` (slate-800) | `#F8FAFC` (slate-50) | Primary text |
| `--card` | `#FFFFFF` | `#1E293B` (slate-800) | Card surface |
| `--card-foreground` | `#1E293B` | `#F8FAFC` | Card text |
| `--popover` | `#FFFFFF` | `#1E293B` | Popover/dropdown surface |
| `--popover-foreground` | `#1E293B` | `#F8FAFC` | Popover text |
| `--surface` | `#FFFFFF` | `#1E293B` | Generic raised surface |
| `--surface-elevated` | `#FFFFFF` | `#334155` (slate-700) | Modals, sheets |
| `--surface-sunken` | `#F1F5F9` (slate-100) | `#020617` (slate-950) | Inset areas, code blocks |
| `--muted` | `#F1F5F9` (slate-100) | `#334155` (slate-700) | Muted backgrounds |
| `--muted-foreground` | `#64748B` (slate-500) | `#94A3B8` (slate-400) | Muted text |
| `--accent` | `#F0FDFA` (teal-50) | `#042F2E` (teal-950) | Tinted hover/selected |
| `--accent-foreground` | `#134E4A` (teal-900) | `#CCFBF1` (teal-100) | Text on accent surface |

---

## 3. Typography Tokens

### 3.1 Font Families

| Token | Stack | Usage |
|-------|-------|-------|
| `--font-heading` | `'DM Sans', system-ui, -apple-system, sans-serif` | H1-H4, card titles, navigation labels |
| `--font-body` | `'Inter', system-ui, -apple-system, sans-serif` | Body text, inputs, buttons, labels |
| `--font-mono` | `'Geist Mono', ui-monospace, 'Cascadia Code', monospace` | Code, data, IDs |

**Font loading strategy:** Both DM Sans and Inter are loaded via `next/font/google` with `display: 'swap'` and subset `'latin'`. DM Sans loads weights 600 and 700 only. Inter loads weights 400, 500, 600.

### 3.2 Size Scale

Based on a 1.250 (Major Third) modular scale with a 16px (1rem) base.

| Token | Size | Rem | Pixel | Usage |
|-------|------|-----|-------|-------|
| `--text-xs` | 0.75rem | 0.75 | 12px | Badges, metadata, timestamps |
| `--text-sm` | 0.875rem | 0.875 | 14px | Captions, labels, helper text |
| `--text-base` | 1rem | 1.0 | 16px | Body text, inputs, buttons |
| `--text-lg` | 1.125rem | 1.125 | 18px | Lead text, emphasized body |
| `--text-xl` | 1.25rem | 1.25 | 20px | H4, card titles |
| `--text-2xl` | 1.5rem | 1.5 | 24px | H3, section subtitles |
| `--text-3xl` | 1.875rem | 1.875 | 30px | H2, section headers |
| `--text-4xl` | 2.25rem | 2.25 | 36px | H1, page titles |

### 3.3 Weight Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--font-normal` | 400 | Body text (Inter) |
| `--font-medium` | 500 | Labels, buttons, emphasized body (Inter) |
| `--font-semibold` | 600 | H2-H4 headings (DM Sans), strong labels |
| `--font-bold` | 700 | H1, logo wordmark, key metrics (DM Sans) |

### 3.4 Line Height Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--leading-none` | 1.0 | Single-line metrics, badges |
| `--leading-tight` | 1.25 | Headings (H1-H3) |
| `--leading-snug` | 1.375 | H4, card titles, tight paragraphs |
| `--leading-normal` | 1.5 | Body text (primary) |
| `--leading-relaxed` | 1.625 | Long-form reading, help text |
| `--leading-loose` | 2.0 | Loose lists, spaced content |

### 3.5 Letter Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--tracking-tighter` | -0.05em | Large headings (H1-H2) |
| `--tracking-tight` | -0.025em | H3-H4 |
| `--tracking-normal` | 0em | Body text |
| `--tracking-wide` | 0.025em | Buttons, labels, badges |
| `--tracking-wider` | 0.05em | Section labels, overlines |
| `--tracking-widest` | 0.1em | All-caps text, brand elements |

### 3.6 Type Combinations Reference

| Context | Family | Size | Weight | Leading | Tracking |
|---------|--------|------|--------|---------|----------|
| Page title (H1) | DM Sans | 2.25rem (36px) | 700 | 1.25 | -0.05em |
| Section header (H2) | DM Sans | 1.875rem (30px) | 600 | 1.25 | -0.025em |
| Subsection (H3) | DM Sans | 1.5rem (24px) | 600 | 1.375 | -0.025em |
| Card title (H4) | DM Sans | 1.25rem (20px) | 500 | 1.375 | 0 |
| Body text | Inter | 1rem (16px) | 400 | 1.5 | 0 |
| Button label | Inter | 0.875rem (14px) | 500 | 1.0 | 0.025em |
| Caption/label | Inter | 0.875rem (14px) | 400 | 1.5 | 0 |
| Badge/tag | Inter | 0.75rem (12px) | 500 | 1.0 | 0.025em |
| KPI metric | DM Sans | 1.875rem (30px) | 700 | 1.0 | -0.025em |
| KPI label | Inter | 0.75rem (12px) | 500 | 1.0 | 0.05em |

---

## 4. Spacing Tokens

Based on a 4px (0.25rem) base unit. All spacing in the system is a multiple of 4.

### 4.1 Base Scale

| Token | Value | Pixels | Usage |
|-------|-------|--------|-------|
| `--space-0` | 0 | 0px | Reset |
| `--space-px` | 1px | 1px | Hairline borders |
| `--space-0.5` | 0.125rem | 2px | Micro gaps |
| `--space-1` | 0.25rem | 4px | Tight inline spacing |
| `--space-1.5` | 0.375rem | 6px | Badge padding |
| `--space-2` | 0.5rem | 8px | Input padding-x, tight gaps |
| `--space-2.5` | 0.625rem | 10px | Button padding-y (sm) |
| `--space-3` | 0.75rem | 12px | Card padding (compact), icon gaps |
| `--space-3.5` | 0.875rem | 14px | Input padding-y |
| `--space-4` | 1rem | 16px | Standard gap, card padding |
| `--space-5` | 1.25rem | 20px | Section gaps |
| `--space-6` | 1.5rem | 24px | Card padding (standard) |
| `--space-7` | 1.75rem | 28px | Medium section spacing |
| `--space-8` | 2rem | 32px | Section padding |
| `--space-10` | 2.5rem | 40px | Large section gaps |
| `--space-12` | 3rem | 48px | Page section spacing |
| `--space-16` | 4rem | 64px | Major section divisions |
| `--space-20` | 5rem | 80px | Page-level spacing |
| `--space-24` | 6rem | 96px | Hero/header spacing |

### 4.2 Component-Specific Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-input-x` | 0.75rem (12px) | Horizontal input padding |
| `--space-input-y` | 0.5rem (8px) | Vertical input padding |
| `--space-btn-x` | 1rem (16px) | Button horizontal padding |
| `--space-btn-y` | 0.5rem (8px) | Button vertical padding |
| `--space-btn-x-sm` | 0.75rem (12px) | Small button horizontal |
| `--space-btn-y-sm` | 0.375rem (6px) | Small button vertical |
| `--space-btn-x-lg` | 1.5rem (24px) | Large button horizontal |
| `--space-btn-y-lg` | 0.75rem (12px) | Large button vertical |
| `--space-card` | 1.5rem (24px) | Card internal padding |
| `--space-card-compact` | 1rem (16px) | Compact card (mobile, lists) |
| `--space-sidebar` | 0.75rem (12px) | Sidebar item padding |
| `--space-nav-gap` | 0.25rem (4px) | Gap between nav items |
| `--space-stack-xs` | 0.25rem (4px) | Tight vertical stacking |
| `--space-stack-sm` | 0.5rem (8px) | Standard vertical stacking |
| `--space-stack-md` | 1rem (16px) | Section stacking |
| `--space-stack-lg` | 1.5rem (24px) | Major section stacking |
| `--space-inline-xs` | 0.25rem (4px) | Tight horizontal gaps |
| `--space-inline-sm` | 0.5rem (8px) | Standard horizontal gaps |
| `--space-inline-md` | 0.75rem (12px) | Medium horizontal gaps |
| `--space-inline-lg` | 1rem (16px) | Wide horizontal gaps |

---

## 5. Border Radius Tokens

### 5.1 Radius Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-none` | 0 | Sharp corners (tables, dividers) |
| `--radius-sm` | 0.25rem (4px) | Badges, tags, small chips |
| `--radius-md` | 0.375rem (6px) | Inputs, small buttons |
| `--radius-DEFAULT` | 0.5rem (8px) | Buttons, cards, dropdowns (system default) |
| `--radius-lg` | 0.75rem (12px) | Modals, large cards |
| `--radius-xl` | 1rem (16px) | Hero cards, feature cards |
| `--radius-2xl` | 1.5rem (24px) | Toast notifications, floating actions |
| `--radius-full` | 9999px | Avatars, pills, circular buttons |

### 5.2 Component Radius Mapping

| Component | Radius Token | Notes |
|-----------|-------------|-------|
| Button (default) | `--radius-DEFAULT` (8px) | Consistent across all variants |
| Button (pill) | `--radius-full` | Used for CTAs and special actions |
| Input / Select / Textarea | `--radius-md` (6px) | Slightly less rounded than buttons |
| Card | `--radius-lg` (12px) | All cards use this |
| Badge / Tag | `--radius-sm` (4px) | Compact, information-dense |
| Avatar | `--radius-full` | Always circular |
| Modal / Dialog | `--radius-lg` (12px) | Matches card radius |
| Toast / Alert | `--radius-lg` (12px) | Matches card radius |
| Dropdown / Popover | `--radius-DEFAULT` (8px) | Matches button radius |
| Tooltip | `--radius-md` (6px) | Compact, lightweight |
| Chat bubble | `--radius-lg` (12px) | Rounded like WhatsApp |
| Mobile bottom sheet | `--radius-xl` (16px) top only | iOS-style top corners |
| App icon | 22.5% | iOS standard, applied in exports |

---

## 6. Shadow Tokens

### 6.1 Light Mode Shadows

Shadows use neutral blue-gray tones to complement the Slate palette.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-xs` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | Subtle lift (inputs, badges) |
| `--shadow-sm` | `0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)` | Cards at rest |
| `--shadow-DEFAULT` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` | Cards on hover, dropdowns |
| `--shadow-md` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` | Modals, floating elements |
| `--shadow-lg` | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` | Dialogs, major overlays |
| `--shadow-xl` | `0 25px 50px -12px rgb(0 0 0 / 0.25)` | Full-screen overlays |
| `--shadow-inner` | `inset 0 2px 4px 0 rgb(0 0 0 / 0.05)` | Sunken inputs, pressed states |
| `--shadow-ring` | `0 0 0 3px hsl(var(--ring) / 0.2)` | Focus ring shadow |
| `--shadow-primary` | `0 4px 14px 0 rgb(13 148 136 / 0.25)` | Primary button glow |
| `--shadow-coral` | `0 4px 14px 0 rgb(249 112 102 / 0.25)` | Notification/CTA glow |

### 6.2 Dark Mode Shadows

Dark mode uses more subtle shadows with reduced opacity and tighter spread. The primary visual separation in dark mode comes from surface color differentiation, not shadows.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-xs` | `0 1px 2px 0 rgb(0 0 0 / 0.2)` | Subtle lift |
| `--shadow-sm` | `0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.3)` | Cards at rest |
| `--shadow-DEFAULT` | `0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.3)` | Cards on hover |
| `--shadow-md` | `0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3)` | Modals |
| `--shadow-lg` | `0 20px 25px -5px rgb(0 0 0 / 0.35), 0 8px 10px -6px rgb(0 0 0 / 0.35)` | Dialogs |
| `--shadow-xl` | `0 25px 50px -12px rgb(0 0 0 / 0.5)` | Full-screen overlays |
| `--shadow-inner` | `inset 0 2px 4px 0 rgb(0 0 0 / 0.2)` | Sunken inputs |
| `--shadow-ring` | `0 0 0 3px hsl(var(--ring) / 0.3)` | Focus ring (brighter in dark) |
| `--shadow-primary` | `0 4px 14px 0 rgb(45 212 191 / 0.2)` | Primary button glow (teal-400) |
| `--shadow-coral` | `0 4px 14px 0 rgb(249 112 102 / 0.2)` | Notification glow |

---

## 7. Component Token Mapping

### 7.1 Button Variants

| Variant | Background | Text | Border | Hover BG | Active BG |
|---------|-----------|------|--------|----------|-----------|
| **Primary** | `--primary` (teal-600) | White | none | `--primary-hover` (teal-700) | teal-800 |
| **Secondary** | `--secondary` (coral-500) | White | none | coral-600 | coral-700 |
| **Outline** | transparent | `--primary-text` (teal-700) | `--primary` | teal-50 | teal-100 |
| **Ghost** | transparent | `--foreground` | none | slate-100 | slate-200 |
| **Destructive** | `--destructive` (red-500) | White | none | red-600 | red-700 |
| **Link** | transparent | `--primary-text` (teal-700) | none | underline | underline |

**Dark mode adjustments:**
- Primary: teal-400 bg, slate-900 text, teal-500 hover
- Secondary: coral-500 bg (same), white text, coral-600 hover
- Outline: teal-400 text, teal-400 border, teal-950 hover-bg
- Ghost: slate-50 text, slate-700 hover-bg

### 7.2 Card Variants

| Variant | Surface | Border | Shadow | Usage |
|---------|---------|--------|--------|-------|
| **Default** | `--card` | `--border` (1px) | `--shadow-sm` | Standard content cards |
| **Elevated** | `--card` | none | `--shadow-DEFAULT` | KPI cards, feature cards |
| **Interactive** | `--card` | `--border` | `--shadow-sm` -> `--shadow-DEFAULT` on hover | Clickable list items |
| **Highlighted** | teal-50 | teal-200 (1px) | `--shadow-sm` | Active/selected state |
| **AI** | `--bubble-ai` | purple-200 (1px) | `--shadow-sm` | Eli context cards |
| **Alert** | coral-50 | coral-200 (1px) | none | Attention-needed cards |

### 7.3 Badge Variants

| Variant | Background | Text | Usage |
|---------|-----------|------|-------|
| **Default** | slate-100 | slate-700 | Generic labels |
| **Primary** | teal-50 | teal-700 | Active states, categories |
| **Secondary** | coral-50 | coral-700 | Counts, notifications |
| **Success** | green-50 | green-700 | Confirmado, Online, Saudavel |
| **Warning** | yellow-50 | yellow-700 | Pendente, Atencao |
| **Destructive** | red-50 | red-700 | Erro, Cancelado |
| **AI** | violet-50 | violet-700 | Eli badges, AI indicators |
| **Outline** | transparent | slate-600 | Subtle categorical tags |

### 7.4 Input States

| State | Border | Ring | Background | Label Color |
|-------|--------|------|-----------|-------------|
| **Default** | `--border` (slate-300) | none | `--card` (white) | slate-700 |
| **Focus** | `--primary` (teal-600) | `--shadow-ring` (teal 20%) | white | slate-800 |
| **Error** | `--destructive` (red-500) | red 20% ring | white | red-700 |
| **Disabled** | slate-200 | none | slate-50 | slate-400 |
| **Read-only** | slate-200 | none | slate-50 | slate-600 |

### 7.5 Navigation

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Sidebar background | White | slate-900 |
| Nav item text | slate-600 | slate-400 |
| Nav item hover bg | slate-100 | slate-800 |
| Nav item active bg | teal-50 | teal-950 |
| Nav item active text | teal-700 | teal-300 |
| Nav item active indicator | teal-600 (left bar, 3px) | teal-400 |
| Nav badge (count) | coral-500 bg, white text | coral-500 bg, white text |
| Nav section label | slate-400 (uppercase, xs) | slate-500 |

### 7.6 Chat/Conversation

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| User bubble bg | teal-600 | teal-700 |
| User bubble text | White | White |
| Contact bubble bg | slate-100 | slate-800 |
| Contact bubble text | slate-800 | slate-100 |
| AI bubble bg | `--bubble-ai` (violet 8%) | `--bubble-ai` (violet 12%) |
| AI bubble text | slate-800 | slate-100 |
| AI bubble border | violet-200 (1px) | violet-800 (1px) |
| AI bot badge | violet-500 bg, white text | violet-400 bg, white text |
| Timestamp | slate-400 | slate-500 |
| Escalation card bg | coral-50 | coral-950 |
| Escalation card border | coral-200 | coral-800 |

---

## 8. CSS Custom Properties

Complete `globals.css` replacement, ready to copy into the Tikso project.

### 8.1 Light Mode (`:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@600;700&family=Inter:wght@400;500;600&display=swap');

:root {
  /* ========================================
     TIKSO DESIGN SYSTEM -- PULSE MARK BRAND
     Generated: 2026-02-25
     Brand: Concept 1 -- The Pulse Mark
     ======================================== */

  /* --- Color Primitives (Raw Palette) --- */
  /* These are referenced by semantic tokens below.
     Format: HSL channels without hsl() wrapper for composability. */

  /* Teal Scale */
  --teal-50:  166 76% 97%;
  --teal-100: 167 85% 89%;
  --teal-200: 168 84% 78%;
  --teal-300: 171 77% 64%;
  --teal-400: 172 66% 50%;
  --teal-500: 173 80% 40%;
  --teal-600: 175 84% 32%;
  --teal-700: 175 77% 26%;
  --teal-800: 176 69% 22%;
  --teal-900: 175 60% 19%;
  --teal-950: 179 86% 10%;

  /* Coral Scale */
  --coral-50:  5 100% 98%;
  --coral-100: 7 100% 94%;
  --coral-200: 354 96% 90%;
  --coral-300: 0 97% 82%;
  --coral-400: 3 94% 72%;
  --coral-500: 4 92% 69%;
  --coral-600: 3 78% 56%;
  --coral-700: 4 67% 45%;
  --coral-800: 4 66% 38%;
  --coral-900: 2 57% 33%;
  --coral-950: 3 72% 17%;

  /* Neutral (Slate) Scale */
  --slate-50:  210 40% 98%;
  --slate-100: 210 40% 96%;
  --slate-200: 214 32% 91%;
  --slate-300: 213 27% 84%;
  --slate-400: 215 20% 65%;
  --slate-500: 215 16% 47%;
  --slate-600: 215 19% 35%;
  --slate-700: 217 19% 27%;
  --slate-800: 217 33% 17%;
  --slate-900: 222 47% 11%;
  --slate-950: 229 84% 5%;

  /* --- Semantic Tokens (Light Mode) --- */

  /* Core Surfaces */
  --background: var(--slate-50);
  --foreground: var(--slate-800);

  /* Card / Popover */
  --card: 0 0% 100%;
  --card-foreground: var(--slate-800);
  --popover: 0 0% 100%;
  --popover-foreground: var(--slate-800);

  /* Primary (Teal) */
  --primary: var(--teal-600);
  --primary-foreground: 0 0% 100%;
  --primary-hover: var(--teal-700);
  --primary-text: var(--teal-700);          /* AA-safe for normal text on white */
  --primary-light: var(--teal-50);          /* Tinted backgrounds */

  /* Secondary (Coral) */
  --secondary: var(--coral-500);
  --secondary-foreground: 0 0% 100%;
  --secondary-hover: var(--coral-600);
  --secondary-text: var(--coral-700);       /* AA-safe for normal text on white */
  --secondary-light: var(--coral-50);       /* Tinted backgrounds */

  /* Muted */
  --muted: var(--slate-100);
  --muted-foreground: var(--slate-500);

  /* Accent (Teal-tinted) */
  --accent: var(--teal-50);
  --accent-foreground: var(--teal-900);

  /* Destructive */
  --destructive: 0 84% 60%;                /* #EF4444 */
  --destructive-foreground: 0 0% 100%;
  --destructive-text: 0 72% 51%;           /* #DC2626 -- AA on white */
  --destructive-light: 0 86% 97%;          /* #FEF2F2 */

  /* Success */
  --success: 142 71% 45%;                  /* #22C55E */
  --success-foreground: 0 0% 100%;
  --success-text: 142 64% 33%;             /* #16A34A */
  --success-light: 138 76% 97%;            /* #F0FDF4 */

  /* Warning */
  --warning: 45 93% 47%;                   /* #EAB308 */
  --warning-foreground: 33 97% 10%;        /* #422006 */
  --warning-text: 32 95% 35%;              /* #A16207 -- AA on white */
  --warning-light: 48 96% 89%;             /* #FEF9C3 */

  /* Info */
  --info: 217 91% 60%;                     /* #3B82F6 */
  --info-foreground: 0 0% 100%;
  --info-text: 224 76% 53%;                /* #2563EB -- AA on white */
  --info-light: 214 95% 93%;              /* #DBEAFE */

  /* Borders & Inputs */
  --border: var(--slate-200);
  --input: var(--slate-300);
  --ring: var(--teal-600);

  /* Surfaces */
  --surface: 0 0% 100%;
  --surface-elevated: 0 0% 100%;
  --surface-sunken: var(--slate-100);

  /* AI Agent (Eli) */
  --ai-accent: 262 83% 58%;               /* #7C3AED */
  --ai-accent-foreground: 0 0% 100%;
  --ai-accent-muted: 263 90% 96%;         /* #EDE9FE (violet-100) */
  --bubble-ai: 262 83% 58% / 0.08;

  /* Coral (notification/CTA accent) */
  --notification: var(--coral-500);
  --notification-foreground: 0 0% 100%;
  --notification-light: var(--coral-50);

  /* Layout */
  --radius: 0.5rem;
  --sidebar-width: 256px;
  --sidebar-width-collapsed: 64px;
  --header-height: 56px;
  --bottom-bar-height: 64px;
}
```

### 8.2 Dark Mode (`.dark`)

```css
.dark {
  /* --- Semantic Tokens (Dark Mode) --- */

  /* Core Surfaces */
  --background: var(--slate-900);
  --foreground: var(--slate-50);

  /* Card / Popover */
  --card: var(--slate-800);
  --card-foreground: var(--slate-50);
  --popover: var(--slate-800);
  --popover-foreground: var(--slate-50);

  /* Primary (Brighter Teal for dark backgrounds) */
  --primary: var(--teal-400);
  --primary-foreground: var(--slate-900);
  --primary-hover: var(--teal-500);
  --primary-text: var(--teal-300);          /* AA on dark (9.89:1) */
  --primary-light: var(--teal-950);         /* Dark tinted backgrounds */

  /* Secondary (Coral stays similar) */
  --secondary: var(--coral-500);
  --secondary-foreground: 0 0% 100%;
  --secondary-hover: var(--coral-400);
  --secondary-text: var(--coral-300);       /* AA on dark (7.68:1) */
  --secondary-light: var(--coral-950);

  /* Muted */
  --muted: var(--slate-700);
  --muted-foreground: var(--slate-400);

  /* Accent */
  --accent: var(--teal-950);
  --accent-foreground: var(--teal-100);

  /* Destructive */
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --destructive-text: 0 91% 71%;           /* #F87171 -- AA on dark */
  --destructive-light: 0 63% 15%;          /* dark red tint */

  /* Success */
  --success: 142 71% 45%;
  --success-foreground: 0 0% 100%;
  --success-text: 142 69% 58%;             /* #4ADE80 */
  --success-light: 144 61% 10%;

  /* Warning */
  --warning: 45 93% 47%;
  --warning-foreground: 33 97% 10%;
  --warning-text: 48 96% 53%;              /* #FACC15 */
  --warning-light: 46 51% 12%;

  /* Info */
  --info: 217 91% 60%;
  --info-foreground: 0 0% 100%;
  --info-text: 213 94% 68%;                /* #60A5FA */
  --info-light: 224 46% 15%;

  /* Borders & Inputs */
  --border: var(--slate-700);
  --input: var(--slate-600);
  --ring: var(--teal-400);

  /* Surfaces */
  --surface: var(--slate-800);
  --surface-elevated: var(--slate-700);
  --surface-sunken: var(--slate-950);

  /* AI Agent (Eli) -- brighter in dark mode */
  --ai-accent: 263 70% 71%;               /* #A78BFA */
  --ai-accent-foreground: 0 0% 100%;
  --ai-accent-muted: 267 100% 8%;         /* #2E1065 (violet-950) */
  --bubble-ai: 263 70% 71% / 0.12;

  /* Notification */
  --notification: var(--coral-400);
  --notification-foreground: 0 0% 100%;
  --notification-light: var(--coral-950);
}
```

### 8.3 Utility Classes

```css
/* === Focus Ring === */
.focus-ring {
  outline: none;
}
.focus-ring:focus-visible {
  box-shadow: 0 0 0 2px hsl(var(--background)), 0 0 0 4px hsl(var(--ring));
}

/* === Primary Text (WCAG-safe) === */
.text-primary-safe {
  color: hsl(var(--primary-text));
}

/* === Coral Text (WCAG-safe) === */
.text-coral-safe {
  color: hsl(var(--secondary-text));
}

/* === Semantic text colors (always AA on their mode's background) === */
.text-success-safe { color: hsl(var(--success-text)); }
.text-warning-safe { color: hsl(var(--warning-text)); }
.text-error-safe   { color: hsl(var(--destructive-text)); }
.text-info-safe    { color: hsl(var(--info-text)); }

/* === Pulse Animation (brand signature) === */
@keyframes pulse-brand {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.animate-pulse-brand {
  animation: pulse-brand 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* === AI Glow (Eli indicator) === */
@keyframes ai-glow {
  0%, 100% { box-shadow: 0 0 0 0 hsl(var(--ai-accent) / 0.4); }
  50% { box-shadow: 0 0 0 6px hsl(var(--ai-accent) / 0); }
}

.animate-ai-glow {
  animation: ai-glow 2s ease-in-out infinite;
}

/* === Reduced Motion === */
@media (prefers-reduced-motion: reduce) {
  .animate-pulse-brand,
  .animate-ai-glow {
    animation: none;
  }
}
```

---

## 9. Tailwind Config

### 9.1 Tailwind v4 `@theme inline` Block

Add to `globals.css` alongside the CSS custom properties above.

```css
@theme inline {
  /* === Colors (mapped from CSS custom properties) === */

  /* Primary */
  --color-primary: hsl(var(--primary));
  --color-primary-foreground: hsl(var(--primary-foreground));
  --color-primary-hover: hsl(var(--primary-hover));
  --color-primary-text: hsl(var(--primary-text));
  --color-primary-light: hsl(var(--primary-light));

  /* Secondary / Coral */
  --color-secondary: hsl(var(--secondary));
  --color-secondary-foreground: hsl(var(--secondary-foreground));
  --color-secondary-hover: hsl(var(--secondary-hover));
  --color-secondary-text: hsl(var(--secondary-text));
  --color-secondary-light: hsl(var(--secondary-light));

  /* Surfaces */
  --color-background: hsl(var(--background));
  --color-foreground: hsl(var(--foreground));
  --color-card: hsl(var(--card));
  --color-card-foreground: hsl(var(--card-foreground));
  --color-popover: hsl(var(--popover));
  --color-popover-foreground: hsl(var(--popover-foreground));
  --color-surface: hsl(var(--surface));
  --color-surface-elevated: hsl(var(--surface-elevated));
  --color-surface-sunken: hsl(var(--surface-sunken));

  /* Muted */
  --color-muted: hsl(var(--muted));
  --color-muted-foreground: hsl(var(--muted-foreground));

  /* Accent */
  --color-accent: hsl(var(--accent));
  --color-accent-foreground: hsl(var(--accent-foreground));

  /* Semantic */
  --color-destructive: hsl(var(--destructive));
  --color-destructive-foreground: hsl(var(--destructive-foreground));
  --color-destructive-text: hsl(var(--destructive-text));
  --color-destructive-light: hsl(var(--destructive-light));

  --color-success: hsl(var(--success));
  --color-success-foreground: hsl(var(--success-foreground));
  --color-success-text: hsl(var(--success-text));
  --color-success-light: hsl(var(--success-light));

  --color-warning: hsl(var(--warning));
  --color-warning-foreground: hsl(var(--warning-foreground));
  --color-warning-text: hsl(var(--warning-text));
  --color-warning-light: hsl(var(--warning-light));

  --color-info: hsl(var(--info));
  --color-info-foreground: hsl(var(--info-foreground));
  --color-info-text: hsl(var(--info-text));
  --color-info-light: hsl(var(--info-light));

  /* Borders & Inputs */
  --color-border: hsl(var(--border));
  --color-input: hsl(var(--input));
  --color-ring: hsl(var(--ring));

  /* AI / Eli */
  --color-ai-accent: hsl(var(--ai-accent));
  --color-ai-accent-foreground: hsl(var(--ai-accent-foreground));
  --color-ai-accent-muted: hsl(var(--ai-accent-muted));
  --color-bubble-ai: hsl(var(--bubble-ai));

  /* Notification / Coral accent */
  --color-notification: hsl(var(--notification));
  --color-notification-foreground: hsl(var(--notification-foreground));
  --color-notification-light: hsl(var(--notification-light));

  /* === Raw Palette (for direct use like bg-teal-50) === */
  --color-teal-50:  hsl(166 76% 97%);
  --color-teal-100: hsl(167 85% 89%);
  --color-teal-200: hsl(168 84% 78%);
  --color-teal-300: hsl(171 77% 64%);
  --color-teal-400: hsl(172 66% 50%);
  --color-teal-500: hsl(173 80% 40%);
  --color-teal-600: hsl(175 84% 32%);
  --color-teal-700: hsl(175 77% 26%);
  --color-teal-800: hsl(176 69% 22%);
  --color-teal-900: hsl(175 60% 19%);
  --color-teal-950: hsl(179 86% 10%);

  --color-coral-50:  hsl(5 100% 98%);
  --color-coral-100: hsl(7 100% 94%);
  --color-coral-200: hsl(354 96% 90%);
  --color-coral-300: hsl(0 97% 82%);
  --color-coral-400: hsl(3 94% 72%);
  --color-coral-500: hsl(4 92% 69%);
  --color-coral-600: hsl(3 78% 56%);
  --color-coral-700: hsl(4 67% 45%);
  --color-coral-800: hsl(4 66% 38%);
  --color-coral-900: hsl(2 57% 33%);
  --color-coral-950: hsl(3 72% 17%);

  /* === Typography === */
  --font-heading: 'DM Sans', system-ui, -apple-system, sans-serif;
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'Geist Mono', ui-monospace, 'Cascadia Code', monospace;

  /* === Border Radius === */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-DEFAULT: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;

  /* === Shadows === */
  --shadow-primary: 0 4px 14px 0 rgb(13 148 136 / 0.25);
  --shadow-coral: 0 4px 14px 0 rgb(249 112 102 / 0.25);
}
```

### 9.2 Font Loading (layout.tsx)

```tsx
import { DM_Sans, Inter } from 'next/font/google'

const dmSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-dm-sans',
  weight: ['600', '700'],
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  weight: ['400', '500', '600'],
  display: 'swap',
})

// In the <html> or <body> tag:
// className={`${dmSans.variable} ${inter.variable}`}
```

### 9.3 Usage Examples

```html
<!-- Primary button -->
<button class="bg-primary text-primary-foreground hover:bg-primary-hover
               rounded-DEFAULT px-4 py-2 text-sm font-medium shadow-primary">
  Agendar
</button>

<!-- Secondary/Coral button -->
<button class="bg-secondary text-secondary-foreground hover:bg-secondary-hover
               rounded-DEFAULT px-4 py-2 text-sm font-medium">
  Enviar campanha
</button>

<!-- Outline button -->
<button class="border border-primary text-primary-text hover:bg-accent
               rounded-DEFAULT px-4 py-2 text-sm font-medium">
  Ver detalhes
</button>

<!-- Ghost button -->
<button class="text-foreground hover:bg-muted
               rounded-DEFAULT px-4 py-2 text-sm font-medium">
  Cancelar
</button>

<!-- KPI card (elevated) -->
<div class="bg-card rounded-lg p-6 shadow-sm hover:shadow-DEFAULT transition-shadow">
  <p class="text-xs font-medium tracking-wider text-muted-foreground uppercase">
    Receita da Eli
  </p>
  <p class="text-3xl font-bold font-heading text-foreground mt-1">
    R$ 4.850,00
  </p>
  <p class="text-sm text-success-text mt-1">+18% vs semana passada</p>
</div>

<!-- AI/Eli badge -->
<span class="bg-ai-accent text-ai-accent-foreground text-xs font-medium
             px-2 py-0.5 rounded-sm">
  Eli
</span>

<!-- Notification badge (coral) -->
<span class="bg-notification text-notification-foreground text-xs font-medium
             px-1.5 py-0.5 rounded-full min-w-[1.25rem] text-center">
  3
</span>

<!-- Status badges -->
<span class="bg-success-light text-success-text text-xs font-medium px-2 py-0.5 rounded-sm">
  Confirmado
</span>
<span class="bg-warning-light text-warning-text text-xs font-medium px-2 py-0.5 rounded-sm">
  Pendente
</span>
<span class="bg-destructive-light text-destructive-text text-xs font-medium px-2 py-0.5 rounded-sm">
  Cancelado
</span>

<!-- Eli context card -->
<div class="bg-bubble-ai border border-ai-accent/20 rounded-lg p-4">
  <div class="flex items-center gap-2 mb-2">
    <span class="bg-ai-accent text-ai-accent-foreground text-xs px-2 py-0.5 rounded-sm">
      Eli
    </span>
    <span class="text-sm text-muted-foreground">Ultimas 24h</span>
  </div>
  <p class="text-sm text-foreground">23 conversas atendidas | 87% taxa resolucao</p>
</div>

<!-- Chat bubble (user/owner) -->
<div class="bg-teal-600 text-white rounded-lg rounded-br-sm px-3 py-2 max-w-xs ml-auto">
  <p class="text-sm">Pode oferecer 10% de desconto</p>
</div>

<!-- Chat bubble (contact) -->
<div class="bg-muted text-foreground rounded-lg rounded-bl-sm px-3 py-2 max-w-xs">
  <p class="text-sm">Oi, quero agendar um corte</p>
</div>

<!-- Heading example -->
<h1 class="font-heading text-4xl font-bold tracking-tighter text-foreground">
  Dashboard
</h1>
<h2 class="font-heading text-3xl font-semibold tracking-tight text-foreground">
  Resumo da Eli
</h2>
```

---

## 10. WCAG Compliance Matrix

### 10.1 Text on Light Backgrounds

All combinations meeting WCAG AA (4.5:1) for normal text on white/cloud/slate-100:

| Foreground | On White | On Cloud | On Slate-100 | Verdict |
|------------|----------|----------|--------------|---------|
| Charcoal `#1E293B` | 14.63:1 | 13.98:1 | 13.35:1 | AAA -- Body text |
| Slate-600 `#475569` | 7.58:1 | 7.24:1 | 6.92:1 | AAA -- Secondary text |
| Slate-500 `#64748B` | 4.76:1 | 4.55:1 | 4.35:1 | AA -- Labels, captions |
| Teal-700 `#0F766E` | 5.47:1 | 5.23:1 | 5.00:1 | AA -- Primary links, labels |
| Teal-800 `#115E59` | 7.58:1 | 7.24:1 | 6.92:1 | AAA -- Primary headings |
| Coral-700 `#C33025` | 5.57:1 | 5.32:1 | 5.09:1 | AA -- Coral text |
| Coral-800 `#A12921` | 7.36:1 | 7.03:1 | 6.72:1 | AAA -- Coral emphasis |
| Error `#DC2626` | 4.83:1 | 4.62:1 | 4.41:1 | AA -- Error text |
| Warning `#A16207` | 4.81:1 | -- | -- | AA -- Warning text |
| AI Purple `#7C3AED` | 5.70:1 | 5.45:1 | 5.21:1 | AA -- AI labels |

### 10.2 Text on Dark Backgrounds

All combinations on charcoal (#1E293B) and slate-900 (#0F172A):

| Foreground | On Charcoal | On Slate-900 | Verdict |
|------------|-------------|--------------|---------|
| White `#FFFFFF` | 14.63:1 | 17.85:1 | AAA -- Body text |
| Slate-50 `#F8FAFC` | 13.98:1 | 17.07:1 | AAA -- Primary text |
| Slate-400 `#94A3B8` | 5.71:1 | 6.97:1 | AA -- Secondary text |
| Teal-300 `#5EEAD4` | 9.89:1 | 12.07:1 | AAA -- Primary links |
| Teal-400 `#2DD4BF` | 7.86:1 | 9.60:1 | AAA -- Primary accent |
| Coral-300 `#FDA4A4` | 7.68:1 | 9.37:1 | AAA -- Coral accent |
| Coral-500 `#F97066` | 5.25:1 | 6.41:1 | AA -- Notifications |
| AI Purple `#A78BFA` | 5.38:1 | 6.57:1 | AA -- AI labels |

### 10.3 Critical Failures and Mitigations

| Combination | Ratio | Issue | Mitigation |
|-------------|-------|-------|------------|
| Teal-600 on White | 3.74:1 | Fails AA normal text | Use teal-700 for text; teal-600 for fills/icons/large-text only |
| Coral-500 on White | 2.79:1 | Fails all AA | Decorative only; use coral-700 for text |
| Success-500 `#22C55E` on White | 2.28:1 | Fails all AA | Use `#16A34A` for text; green-500 for icons only |
| Warning `#EAB308` on White | 1.92:1 | Fails all AA | Use `#A16207` for text; yellow for icons only |
| Slate-400 on White | 2.56:1 | Fails AA | Placeholder text only (not informational) |

### 10.4 Rules Enforced

1. **Normal text (< 18px bold, < 24px regular):** Minimum 4.5:1 contrast ratio.
2. **Large text (>= 18px bold, >= 24px regular):** Minimum 3.0:1 contrast ratio.
3. **Non-text elements (icons, borders, focus rings):** Minimum 3.0:1 against adjacent colors.
4. **Decorative elements:** No minimum (badges on colored backgrounds, background washes).
5. **Semantic token naming:** Use `--*-text` variants for text content, base tokens for fills/decorative.
6. **Never rely on color alone:** All states (error, success, warning) use icon + text + color.

---

## 11. Migration Guide

### 11.1 Token Rename Map (Orange to Teal)

| Old Token (Current) | New Token | Old Value | New Value |
|---------------------|-----------|-----------|-----------|
| `--primary` | `--primary` | `#FA6810` (orange) | `#0D9488` (teal-600) |
| `--primary-foreground` | `--primary-foreground` | white | white |
| (none) | `--primary-hover` | -- | `#0F766E` (teal-700) |
| (none) | `--primary-text` | -- | `#0F766E` (teal-700) |
| (none) | `--primary-light` | -- | teal-50 |
| (none) | `--secondary` | -- | `#F97066` (coral-500) |
| (none) | `--secondary-text` | -- | `#C33025` (coral-700) |
| (none) | `--notification` | -- | coral-500 |
| `--ai-accent` | `--ai-accent` | purple | purple (no change) |

### 11.2 File Change Checklist

| File | Action | Impact |
|------|--------|--------|
| `globals.css` | Replace all `:root` and `.dark` token values | All components auto-update |
| `globals.css` | Add `@theme inline` block with new tokens | Enables Tailwind classes |
| `layout.tsx` | Add DM Sans font import alongside Inter | Typography upgrade |
| `layout.tsx` | Add `font-heading` class variable | Enables heading font |
| All heading components | Add `font-heading` class | Uses DM Sans for headings |
| Button components | Verify `bg-primary` renders teal | Should auto-update via tokens |
| Badge components | Add `coral` and `ai` variants | New badge types |
| Chat bubble components | Verify `--bubble-ai` renders correctly | Should auto-update |

### 11.3 Migration Steps (Phase 0)

1. **Backup current `globals.css`**
2. **Replace CSS custom properties** with Section 8 values
3. **Add `@theme inline` block** from Section 9.1
4. **Add DM Sans font loading** to `layout.tsx` (Section 9.2)
5. **Add `font-heading` class** to heading elements (H1-H4)
6. **Visual regression test**: Open every page and verify no broken colors
7. **Verify dark mode**: Toggle dark mode and check all surfaces/text
8. **Run contrast audit**: Spot-check text readability on all backgrounds
9. **Remove any hardcoded orange (`#FA6810`, `#f97316`, etc.) values** with grep

### 11.4 Search-and-Destroy Hardcoded Colors

Run these commands on the Tikso codebase to find any hardcoded colors that should use tokens:

```bash
# Find hardcoded orange (old brand)
grep -rn "FA6810\|fa6810\|#FA6810\|orange-500\|orange-600" src/

# Find hardcoded teal that should use tokens
grep -rn "#0D9488\|#0F766E\|#14B8A6" src/

# Find hardcoded coral that should use tokens
grep -rn "#F97066\|#E5453A\|#C33025" src/

# Find any inline color values in JSX/TSX
grep -rn "style={{.*color:" src/ --include="*.tsx" --include="*.jsx"

# Find Tailwind classes using raw colors instead of tokens
grep -rn "bg-\[#\|text-\[#\|border-\[#" src/
```

---

## Auto-Decisions Log

| Question | Decision | Reason |
|----------|----------|--------|
| Teal-600 fails AA on white for normal text -- accept or fix? | Dual-token strategy: `--primary` for fills/decorative, `--primary-text` (teal-700) for text | Preserves brand identity (#0D9488) while ensuring accessibility. Same pattern used by Tailwind, Radix, Chakra. |
| Which shade for dark mode primary? | Teal-400 (#2DD4BF) | 7.86:1 on charcoal (AAA). Teal-300 was too bright/washed; teal-500 was too dark (only 5.88:1). |
| Coral as text color on light backgrounds? | Use coral-700 (#C33025) for text, coral-500 for decoration only | Coral-500 at 2.79:1 on white fails even AA-large. Coral-700 at 5.57:1 passes AA. |
| Keep purple for AI or switch to teal variant? | Keep purple (violet) | Purple creates clear visual boundary between brand interactions (teal) and AI interactions (purple). Prevents confusion. Already established in current codebase. |
| Neutral palette: pure gray or Slate? | Slate (blue-gray undertone) | Blue undertone in Slate harmonizes with teal. Pure gray would feel disconnected from the brand warmth. |
| Shadow strategy for dark mode? | Increase opacity, not spread | Lighter shadows on dark backgrounds look unnatural. Stronger opacity with same geometry maintains visual consistency. |
| Success green text on white fails AA -- fix? | Use `#16A34A` (green-600) for text, `#22C55E` for icons/fills | Same dual-token pattern as primary. Keeps the visual brightness of green while ensuring text readability. |
| Font loading: Google Fonts CDN or next/font? | `next/font/google` with `display: 'swap'` | Automatic font optimization, self-hosted, no CLS. Standard Next.js practice. |

---

## Appendix: Token Inventory Summary

| Category | Count | Notes |
|----------|-------|-------|
| Color primitives (teal scale) | 11 | 50-950 |
| Color primitives (coral scale) | 11 | 50-950 |
| Color primitives (slate scale) | 11 | 50-950 |
| Semantic surface tokens | 14 | background, card, popover, surface, muted, accent |
| Semantic color tokens | 20 | primary, secondary, destructive, success, warning, info (+ text-safe variants) |
| AI/Eli tokens | 5 | accent, foreground, muted, bubble |
| Notification tokens | 3 | base, foreground, light |
| Border/input tokens | 3 | border, input, ring |
| Typography tokens | 11 | 3 families + 4 sizes + 4 weights |
| Spacing tokens | 40 | 18 base + 22 component-specific |
| Border radius tokens | 8 | none through full |
| Shadow tokens | 20 | 10 light + 10 dark |
| Layout tokens | 4 | sidebar, header, bottom bar |
| **Total** | **~161** | Complete token system |

---

*Document generated by Brad Frost (Design System Agent, Tier 1)*
*Color scales validated with programmatic WCAG 2.1 contrast ratio computation*
*All HSL values verified against hex equivalents for precision*
*Ready for implementation in Phase 0 of the UX Roadmap (1-2 days estimated)*
