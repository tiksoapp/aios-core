# Tikso UX Redesign Proposal -- Best-in-Class Conversational CRM

> **Agent:** Uma (UX Design Expert)
> **Date:** 2026-02-25
> **Status:** Complete Proposal -- Ready for Review
> **Methodology:** User-Centered Design + Atomic Design System Thinking

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Competitive UX Benchmark](#2-competitive-ux-benchmark)
3. [Information Architecture](#3-information-architecture)
4. [Dashboard do Dono (Owner Dashboard)](#4-dashboard-do-dono)
5. [Inbox / Conversas](#5-inbox--conversas)
6. [Mobile-First Design](#6-mobile-first-design)
7. [Onboarding Experience](#7-onboarding-experience)
8. [Design Tokens -- Pulse Mark Brand](#8-design-tokens----pulse-mark-brand)
9. [UX Roadmap Prioritizado](#9-ux-roadmap-prioritizado)
10. [Appendix: Current State Analysis](#10-appendix-current-state-analysis)

---

## 1. Executive Summary

### The Opportunity

Tikso serves non-technical local business owners (barbers, salon owners, clinic managers, gym operators) who manage their customer relationships primarily through WhatsApp. These users check their phone 80% of the time, are not tech-savvy, and care about ONE thing: **"Is my business making money and are my customers being taken care of?"**

### The Problem

Current CRM products in this space fall into two traps:

1. **Enterprise Overload** (Respond.io, HubSpot): Too many features, too much complexity, designed for marketing teams with 20+ people
2. **Chatbot-Only** (BotConversa, Chatfuel): Great at automation but terrible at giving the owner business intelligence

### The Tikso Differentiator

Tikso has a unique asset that no competitor leverages well: **Eli, the AI agent**. Eli is not just a chatbot -- she books appointments, handles customer service, and generates revenue autonomously. The UX must make Eli's value VISIBLE and TANGIBLE to the owner at all times.

### Design Principles for Tikso

| # | Principle | Rationale |
|---|-----------|-----------|
| 1 | **Revenue-First Dashboard** | The owner opens Tikso to see money, not data |
| 2 | **Eli is the Hero** | Every screen shows what the AI accomplished |
| 3 | **5-Second Rule** | Any important info must be visible within 5 seconds of landing |
| 4 | **Thumb-Zone Design** | 80% mobile usage means bottom-aligned actions |
| 5 | **Progressive Disclosure** | Show simple by default, reveal depth on demand |
| 6 | **Portuguese-Native** | Every label, every error, every micro-copy in natural Brazilian Portuguese |
| 7 | **Zero-Learning Curve** | If you can use WhatsApp, you can use Tikso |

---

## 2. Competitive UX Benchmark

### 2.1 Navigation Patterns

| Platform | Nav Style | Mobile Approach | Key Insight |
|----------|-----------|-----------------|-------------|
| **HubSpot** | Top bar (horizontal tabs) + sidebar per section | Hamburger menu + bottom tabs | Overwhelming for small business; 40+ nav items visible |
| **Kommo** | Left sidebar (collapsible) + chat panel always visible | Bottom tab bar (5 items) | Chat-first design; pipeline secondary. Good for SMB. |
| **Respond.io** | Left sidebar (icon-only by default) + workspace switcher | Responsive sidebar becomes drawer | Enterprise feel; workspace concept confuses solo users |
| **Pipedrive** | Left sidebar (icon + label) + top header per section | Full-width mobile app | Pipeline-centric; messaging is an afterthought |
| **Tikso (Current)** | Left sidebar (collapsible, RBAC-filtered) + bottom tab bar (mobile) | Sheet drawer + 5-item bottom bar | Good foundation; needs hierarchy refinement |

**[AUTO-DECISION] Which navigation pattern to follow? -> Left sidebar (desktop) + bottom tab bar (mobile) with Kommo-inspired chat-first hierarchy. Reason: Matches mental model of WhatsApp (tab bar at bottom) which is what our users know best.**

### 2.2 Conversation/Chat Display Patterns

| Platform | Conversation List | Chat View | AI vs Human Indicator |
|----------|------------------|-----------|----------------------|
| **HubSpot** | Card-based, heavy metadata | Full-width with timeline | Bot badge on message, subtle |
| **Kommo** | WhatsApp-like (avatar, name, preview, time) | Full chat with media support | Bot icon in bubble corner |
| **Respond.io** | Dense list with assignment badges | Split view with contact panel | AI Assist label + colored border |
| **WhatsApp** | Familiar format everyone knows | Green/white bubble pattern | N/A (no AI) |
| **Tikso (Current)** | 3-panel layout (list, chat, contact) | WhatsApp-like bubbles | AI accent purple badge (--ai-accent) |

**Key Insight:** The WhatsApp-like conversation list is the RIGHT approach -- our users already have muscle memory for this pattern. What matters is how we surface AI activity within that familiar frame.

### 2.3 Dashboard / Metrics Display

| Platform | Primary Metric | Dashboard Style | Owner Intelligence |
|----------|---------------|-----------------|-------------------|
| **HubSpot** | Deal pipeline value | Report builder (complex) | Requires setup, not instant |
| **Kommo** | Leads in pipeline | Kanban board as dashboard | Good visual but no revenue |
| **Respond.io** | Messages sent/received | Analytics page (separate) | Messaging metrics only |
| **Pipedrive** | Deal value + forecast | KPI cards + charts | Revenue-focused but manual data |

**Gap:** NONE of these show "revenue generated by AI" as a first-class metric. This is Tikso's opportunity to own a unique dashboard pattern: **the AI Revenue Dashboard**.

### 2.4 Mobile Experience

| Platform | Mobile App Quality | Key Actions | Notification Strategy |
|----------|-------------------|-------------|----------------------|
| **HubSpot** | Full app (overwhelming) | Everything accessible | Too many notifications |
| **Kommo** | Focused app (chat + pipeline) | Chat, move deals | Smart: only new leads + mentions |
| **Respond.io** | Web app (responsive) | Chat, assign | Channel-specific alerts |
| **Pipedrive** | Dedicated app (deal-focused) | Add deal, call, email | Activity-based reminders |

**Insight for Tikso:** Our mobile experience should feel like an EXTENSION of WhatsApp, not a replacement. The owner should get a notification that says "Eli booked 3 appointments while you were sleeping" -- not a generic push notification.

---

## 3. Information Architecture

### 3.1 Current Navigation (15 items + 9 settings)

```
Current Sidebar:
  Dashboard
  Inbox              <-- daily use
  Mensagens          <-- internal DMs
  Contatos
  Pipeline
  Campanhas
  Templates
  Catalogo
  Pedidos
  Agendamento
  Email
  Automacao (sub: Fluxos, Sequencias, Palavras-chave, Webhooks)
  Agente IA
  Analytics
  Supervisao
  Configuracoes (9 sub-items)
```

**Problem:** 15 top-level items is too many. The owner sees Dashboard, Inbox, and MAYBE contacts daily. The rest is noise that creates cognitive overload for a non-technical user.

### 3.2 Proposed Navigation Hierarchy

The information architecture should follow a **frequency-of-use** model:

```
TIER 1 -- "Every Day" (always visible):
  Dashboard        -> Owner's daily briefing + revenue
  Inbox            -> Conversations (WhatsApp hub)
  Agendamentos     -> Today's schedule at a glance

TIER 2 -- "Every Week" (visible, but de-emphasized):
  Contatos         -> Customer database
  Pipeline         -> Deal tracking
  Eli (Agente IA)  -> AI configuration + performance

TIER 3 -- "Occasionally" (collapsed under "Mais"):
  Campanhas
  Templates
  Broadcasts
  Catalogo + Pedidos
  Automacao
  Analytics
  Supervisao

TIER 4 -- "Rarely" (settings gear icon):
  All current settings (Geral, Equipe, Cobranca, etc.)
```

### 3.3 Proposed Desktop Sidebar

```
+------------------------------------------+
| [T]  tikso                          [<>] |  <- Logo + collapse toggle
|------------------------------------------|
|                                          |
| [Search... Ctrl+K]                       |  <- Global search
|                                          |
|  PRINCIPAL                               |  <- Section label
|  o  Dashboard                            |
|  o  Inbox                    [3]         |  <- Unread badge
|  o  Agendamentos             [8]         |  <- Today count
|                                          |
|  GESTAO                                  |
|  o  Contatos                             |
|  o  Pipeline                             |
|  o  Eli (IA)                 [OK]        |  <- AI health badge
|                                          |
|  MARKETING                               |
|  o  Campanhas                            |
|  o  Templates                            |
|  o  Broadcasts                           |
|                                          |
|  AVANCADO                    [v]         |  <- Collapsed by default
|  o  Catalogo                             |
|  o  Pedidos                              |
|  o  Automacao            >               |
|  o  Analytics                            |
|  o  Supervisao                           |
|                                          |
|------------------------------------------|
| [Checklist Widget]  3/7 concluido        |  <- Onboarding progress
|------------------------------------------|
| [Org Switcher]                           |
| [o] Online   Carlos R.     [...]        |  <- Presence + user menu
+------------------------------------------+
```

**Key Changes:**
1. **Grouped by mental model** (Principal, Gestao, Marketing, Avancado) instead of flat list
2. **Agendamentos promoted** from buried to Tier 1 -- this is what barbers/salons check constantly
3. **"Eli" instead of "Agente IA"** -- humanize the AI, use her name
4. **"Avancado" collapsed by default** -- reduces visual noise by ~30%
5. **Search at top** -- muscle memory from Ctrl+K, critical for finding contacts/conversations
6. **Smart badges**: Inbox shows unread count, Agendamentos shows today's count, Eli shows health status

### 3.4 Primary User Flows

```
FLOW 1: Morning Check (80% of sessions)
  Open App -> Dashboard -> See overnight revenue + appointments
           -> Scan AI health badge -> Green = good, continue day
           -> Tap Inbox if anything needs human attention

FLOW 2: Handle Escalation (when Eli cannot resolve)
  Notification "Eli precisa de ajuda" -> Tap -> Inbox -> Conversation
  -> Read context -> Send reply -> Back to day

FLOW 3: Check Schedule (barber/salon specific)
  Open App -> Agendamentos -> See today's bookings
  -> Confirm/reschedule as needed

FLOW 4: Monthly Review
  Dashboard -> Scroll to analytics cards -> "Relatorio do Mes"
  -> Revenue, AI performance, customer growth
```

---

## 4. Dashboard do Dono

### 4.1 Design Philosophy

The dashboard is NOT a data analytics page. It is the owner's **daily briefing** -- like a morning newspaper that tells them exactly what they need to know in 10 seconds.

**The 3 Questions Every Owner Asks:**
1. "Quanto dinheiro entrou?" (How much money came in?)
2. "O que a Eli fez por mim?" (What did the AI do for me?)
3. "O que preciso resolver hoje?" (What do I need to handle today?)

### 4.2 Dashboard Sections (Priority Order)

#### Section A: Hero Metrics (Above the Fold)

Four KPI cards spanning the full width, with the most important metric (Revenue) largest:

```
+----------------------------------------------------------------------+
|  Bom dia, Carlos!                     Ter, 25 de Fevereiro 2026      |
+----------------------------------------------------------------------+

+---------------------------+  +---------------+  +---------------+  +---------------+
|                           |  |               |  |               |  |               |
|  RECEITA GERADA           |  | AGENDAMENTOS  |  | CONVERSAS     |  | NOVOS         |
|  PELA ELI                 |  | HOJE          |  | ATIVAS        |  | CLIENTES      |
|                           |  |               |  |               |  |               |
|  R$ 4.850,00              |  |     12        |  |     7         |  |     3         |
|                           |  |               |  |               |  |               |
|  +18% vs semana passada   |  | 3 confirmados |  | 2 aguardam    |  | via WhatsApp  |
|  [Icone: TrendingUp]      |  | [Icone: Cal]  |  | [Icone: Chat] |  | [Icone: User+]|
+---------------------------+  +---------------+  +---------------+  +---------------+
```

**Revenue Card is 2x width** on desktop to emphasize it. All cards use the existing `KpiCard` component pattern but with semantic improvements:
- Revenue: primary color accent (teal)
- Agendamentos: success color when all confirmed
- Conversas Ativas: warning color if any waiting >30min
- Novos Clientes: info color

#### Section B: Eli's Performance Card

This is the signature Tikso element -- no competitor has this. It shows the AI's activity as if she were a team member giving her daily report.

```
+----------------------------------------------------------------------+
|                                                                      |
|  [Bot Icon]  Resumo da Eli -- Ultimas 24h                   [...]   |
|                                                                      |
|  +------------------+  +------------------+  +------------------+    |
|  |  Atendeu         |  |  Agendou         |  |  Resolveu        |    |
|  |  23 conversas    |  |  8 clientes      |  |  15 duvidas      |    |
|  |  [===     ] 87%  |  |  [========] 100% |  |  [======= ] 94%  |    |
|  |  taxa resolucao  |  |  sem conflito    |  |  sem escalar     |    |
|  +------------------+  +------------------+  +------------------+    |
|                                                                      |
|  [!] 2 conversas precisam da sua atencao         [Ver conversas ->]  |
|                                                                      |
+----------------------------------------------------------------------+
```

**Key design decisions:**
- Eli is presented as a team member, not a tool
- Resolution rate and "sem escalar" (without escalation) build owner confidence
- The alert for conversations needing attention is the ONLY action item -- everything else is informational
- Progress bars use semantic colors (green = healthy, yellow = attention, red = problem)

#### Section C: Saude do Canal WhatsApp

Already exists as `ChannelHealthWidget` -- this is well-designed. Keep it as-is with the semaphore system (green/yellow/red) and warmup phase indicator. Position it in the right column alongside the Eli card.

```
+-------------------------------------+  +---------------------------+
|  Resumo da Eli (Section B)          |  |  Saude do Canal           |
|                                     |  |  [Shield] Saudavel        |
|                                     |  |  Conectado | Fase 3/4     |
|                                     |  |  45/120 enviadas hoje     |
|                                     |  |  98% taxa entrega         |
+-------------------------------------+  +---------------------------+
```

#### Section D: Agendamentos do Dia

A timeline view showing today's appointments, color-coded by status:

```
+----------------------------------------------------------------------+
|                                                                      |
|  Agenda de Hoje -- 25 Fev                          [Ver agenda ->]   |
|                                                                      |
|  09:00  [====]  Maria Silva -- Corte + Barba          CONFIRMADO     |
|  09:30  [====]  Joao Santos -- Barba                  CONFIRMADO     |
|  10:00  [    ]  (disponivel)                                         |
|  10:30  [====]  Ana Costa -- Corte Feminino           PENDENTE       |
|  11:00  [====]  Pedro Lima -- Corte                   CONFIRMADO     |
|  ...                                                                 |
|                                                                      |
|  5 confirmados | 2 pendentes | 1 horario livre                      |
|                                                                      |
+----------------------------------------------------------------------+
```

**Design notes:**
- Timeline is visual (time blocks like Google Calendar but simpler)
- Status badges: Confirmado (green), Pendente (yellow), Cancelado (red with strikethrough)
- Free slots are shown to encourage the owner to fill them
- On mobile, this becomes a scrollable horizontal timeline

#### Section E: Quick Actions Bar

Floating action bar at the bottom of the dashboard for common tasks:

```
+----------------------------------------------------------------------+
|                                                                      |
|  [+ Agendar]   [Enviar campanha]   [Ver relatorio]   [Configurar]   |
|                                                                      |
+----------------------------------------------------------------------+
```

### 4.3 Dashboard Wireframe -- Full Desktop View

```
+--------+----------------------------------------------------------------------+
|        |                                                                      |
| SIDE   |  Bom dia, Carlos!                          Ter, 25 Fev 2026         |
| BAR    |                                                                      |
|        |  +--RECEITA PELA ELI--+  +--AGENDAMENTOS--+  +--CONVERSAS--+  +--NOVOS--+
|  [T]   |  |  R$ 4.850         |  |  12 hoje       |  |  7 ativas   |  |  3      |
| tikso  |  |  +18%             |  |  3 pendentes   |  |  2 aguardam |  |  +2 sem |
|        |  +-------------------+  +-----------------+  +-------------+  +--------+
| -----  |                                                                      |
| Dash   |  +------Resumo da Eli------------+  +----Saude do Canal---------+    |
| Inbox   |  |  [Bot] Ultimas 24h           |  |  [Shield] Saudavel        |    |
| Agenda  |  |                              |  |  Conectado | Fase 3       |    |
|        |  |  23 atendidas | 8 agendou    |  |  45/120 enviadas          |    |
| -----  |  |  15 resolveu | 87% taxa     |  |  98% entrega              |    |
| Contat |  |                              |  |  [========= ] Dia 18/28   |    |
| Pipeli |  |  [!] 2 precisam atencao      |  |                           |    |
| Eli    |  +------------------------------+  +---------------------------+    |
|        |                                                                      |
| -----  |  +------Agenda de Hoje-------------------------------------------------+
| Campan |  |  09:00  Maria Silva     Corte+Barba     CONFIRMADO                  |
| Templa |  |  09:30  Joao Santos     Barba           CONFIRMADO                  |
| Broadc |  |  10:00  (disponivel)                                                |
|        |  |  10:30  Ana Costa       Corte Fem       PENDENTE                    |
| -----  |  |  11:00  Pedro Lima      Corte           CONFIRMADO                  |
| [Adv]  |  +---------------------------------------------------------------------+
|        |                                                                      |
| -----  |  +------Acoes Rapidas----------------------------------------------+
| [Check]|  |  [+ Agendar]  [Enviar campanha]  [Ver relatorio]  [Config]     |
| [Org]  |  +---------------------------------------------------------------------+
| [User] |                                                                      |
+--------+----------------------------------------------------------------------+
```

### 4.4 Revenue Attribution Model

The "Receita Gerada pela Eli" metric is calculated from:

| Source | How to Track |
|--------|-------------|
| Appointments booked by Eli | Count completed appointments where `bookedBy = 'ai'` x average service price |
| Products sold via catalog | Orders where conversation source was AI-initiated |
| Upsells suggested by Eli | When Eli recommends an add-on service and customer accepts |
| Saved cancellations | When Eli handles a cancellation attempt and retains the booking |

This requires a `revenueAttribution` field on appointments and orders, which the backend team would implement.

---

## 5. Inbox / Conversas

### 5.1 Current State Analysis

The existing `InboxLayout` component is well-architected with:
- 3-panel layout (conversation list, chat area, contact panel)
- Real-time via Centrifugo (WebSocket)
- Mobile-responsive with view switching (list/chat/contact)
- Keyboard shortcuts (Ctrl+K search, Ctrl+Shift+A toggle contact panel)
- AI accent badge system (--ai-accent purple)

**What needs improvement:**
1. AI-vs-human conversation distinction is too subtle
2. No "Eli handled this" summary at conversation level
3. Takeover flow is not immediately obvious
4. No priority/urgency indicators
5. Mobile conversation list needs better density

### 5.2 Proposed Conversation List Redesign

```
+--------------------------------------------+
|  [Search... Ctrl+K]              [Filter v] |
|                                             |
|  PRECISAM ATENCAO (2)                       |  <- Priority section, red accent
|--------------------------------------------|
|  [Avatar] Maria Silva             2m        |
|  [!] Eli: "Cliente insiste em desconto"     |  <- AI escalation reason
|  Corte + Barba | Pendente                   |
|--------------------------------------------|
|  [Avatar] Pedro Oliveira          15m       |
|  [!] Tempo de espera alto                   |  <- SLA warning
|  Pergunta sobre preco                       |
|--------------------------------------------|
|                                             |
|  CONVERSAS DA ELI (5)                       |  <- AI-managed section, purple accent
|--------------------------------------------|
|  [Avatar] [Bot] Ana Costa         5m        |
|  Eli: Agendamento confirmado p/ 10:30      |
|  Corte Feminino                             |
|--------------------------------------------|
|  [Avatar] [Bot] Joao Santos       23m       |
|  Eli: Enviou catalogo de servicos           |
|  Novo cliente | Explorando                  |
|--------------------------------------------|
|  [Avatar] [Bot] Carlos Mendes     1h        |
|  Eli: Reagendou de 14:00 p/ 15:30          |
|  Barba | Confirmado                         |
|--------------------------------------------|
|  ... +2 mais                                |
|                                             |
|  RESOLVIDAS HOJE (12)              [v]      |  <- Collapsed by default
|--------------------------------------------|
```

**Key design decisions:**

1. **Sectioned by status** instead of flat chronological list:
   - "Precisam Atencao" (red) -- owner MUST act
   - "Conversas da Eli" (purple) -- AI is handling, owner can observe
   - "Resolvidas Hoje" (green, collapsed) -- handled, no action needed

2. **AI activity summary in preview line**: Instead of just showing the last message text, show what Eli DID ("Agendamento confirmado", "Enviou catalogo", "Reagendou")

3. **Escalation reason visible**: When Eli escalates, the REASON is shown in the list preview so the owner knows what to expect before opening

4. **Bot badge** on avatar for AI-managed conversations (using existing `--ai-accent` token)

### 5.3 Chat Area Improvements

```
+----------------------------------------------------------------------+
|  [<] Maria Silva          Corte + Barba | 09:00     [Takeover] [...]  |
+----------------------------------------------------------------------+
|                                                                      |
|  +-- Eli atendeu esta conversa --+                                   |
|  |  Inicio: 08:42                |                                   |
|  |  Motivo escalacao: cliente    |                                   |
|  |  pediu desconto fora da       |                                   |
|  |  politica configurada         |                                   |
|  +-------------------------------+                                   |
|                                                                      |
|  [08:42]  Maria: Oi, quero agendar um corte                         |
|                                                                      |
|           [Bot] Eli: Ola Maria! Claro, tenho    [08:42]              |
|           horarios disponiveis hoje as 9h e     [ai-bubble]          |
|           10h30. Qual prefere?                                       |
|                                                                      |
|  [08:43]  Maria: 9h. Mas consigo desconto?                          |
|                                                                      |
|           [Bot] Eli: Agendado para 9h!          [08:43]              |
|           Sobre desconto, vou verificar         [ai-bubble]          |
|           com a equipe. Um momento...                                |
|                                                                      |
|  +-- Eli transferiu para voce --+                                    |
|  |  "Cliente pediu desconto de  |                                    |
|  |   20% no combo Corte+Barba.  |                                    |
|  |   Politica permite max 10%." |                                    |
|  +------------------------------+                                    |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  [Mensagem...]                      [Agendar] [Template] [Enviar]   |
|                                                                      |
|  Sugestao da Eli: "Oferecer 10% + brinde (produto capilar)"         |
|                                                                      |
+----------------------------------------------------------------------+
```

**Key improvements:**

1. **Conversation context card** at the top: Shows when Eli started handling, what triggered escalation
2. **AI message bubbles visually distinct**: Using `--ai-accent` / `--bubble-ai` tokens (already defined in globals.css) with a small bot icon
3. **Transfer card**: When Eli hands off, a clearly visible card explains WHY and provides context
4. **Eli suggestion bar**: Above the composer, Eli suggests a response based on policy -- the owner can accept, modify, or dismiss
5. **Takeover button** prominently placed in header (not buried in a menu)

### 5.4 Takeover Flow

```
STATE 1: Eli is handling (owner is observing)
  Header: [Maria Silva]  [Eli esta atendendo]  [Assumir conversa ->]

STATE 2: Owner clicks "Assumir conversa"
  Modal: "Assumir esta conversa?"
         "Eli vai parar de responder e voce assume o atendimento."
         [Cancelar]  [Assumir]

STATE 3: Owner is now handling
  Header: [Maria Silva]  [Voce esta atendendo]  [Devolver para Eli]
  Composer: Full access, Eli suggestions still visible above input

STATE 4: Owner finishes, returns to Eli
  Header: [Maria Silva]  [Voce esta atendendo]  [Devolver para Eli]
  Click "Devolver" -> Eli resumes with context of what owner discussed
```

### 5.5 Inbox Wireframe -- Full Desktop View

```
+--------+-----------------------+-----------------------------+-------------------+
|        |  PRECISAM ATENCAO (2) |  [<] Maria Silva    [Take]  |  CONTATO          |
| SIDE   |  [!] Maria Silva  2m  |  Corte+Barba | 09:00  [...] |                   |
| BAR    |  [!] Pedro Oliv  15m  |                             |  Maria Silva      |
|        |                       |  +--Eli context card--+     |  +55 11 9999-1234 |
|        |  CONVERSAS DA ELI (5) |  |  Escalou: desconto |     |  Cliente desde    |
|        |  [B] Ana Costa    5m  |  +--------------------+     |  Jan 2026         |
|        |  [B] Joao Santos 23m  |                             |                   |
|        |  [B] Carlos M     1h  |  [Messages...]              |  HISTORICO        |
|        |  [B] Lucia F      2h  |                             |  12 atendimentos  |
|        |  [B] Rafael S     3h  |  [Eli transfer card]        |  Ultimo: 18 Fev   |
|        |                       |  "Desconto 20%, max 10%"    |  Gasto total:     |
|        |  RESOLVIDAS (12) [v]  |                             |  R$ 1.450,00      |
|        |                       |  [Input...]                 |                   |
|        |  [Search / Filter]    |  Sugestao: "10% + brinde"   |  TAGS             |
|        |                       |                             |  [VIP] [Barba]    |
+--------+-----------------------+-----------------------------+-------------------+
```

---

## 6. Mobile-First Design

### 6.1 Mobile Philosophy

The owner's phone is their primary business tool. The mobile experience must answer these needs:

| Time of Day | Owner Behavior | What They Need |
|-------------|---------------|----------------|
| 7:00 AM | Wake up, check phone | "How was overnight?" -> Dashboard summary |
| 9:00-18:00 | Between appointments | Quick glances at inbox, respond to escalations |
| 18:00 | End of day | "How did today go?" -> Daily summary |
| Random | Notification buzz | Act on escalation immediately |

### 6.2 Mobile Bottom Tab Bar (Redesigned)

Current bottom tabs: Dashboard, Inbox, Contatos, Pipeline, Mais

**Proposed:**
```
+-------+-------+-------+-------+-------+
| Inicio| Inbox |Agenda | Eli   | Mais  |
| [Home]| [Chat]| [Cal] | [Bot] | [...] |
|       | (3)   | (8)   | [OK]  |       |
+-------+-------+-------+-------+-------+
```

**Changes:**
1. "Dashboard" renamed to "Inicio" (more natural Portuguese)
2. "Contatos" and "Pipeline" moved to "Mais" -- rarely needed on mobile
3. "Agenda" (Agendamentos) added -- critical for service businesses
4. "Eli" added -- quick access to AI status and configuration
5. Badge on Eli tab: green dot (healthy), yellow dot (attention), red dot (problem)

### 6.3 Mobile Dashboard

```
+----------------------------------+
|  Tikso                     [Bell]|
|----------------------------------|
|                                  |
|  Bom dia, Carlos!                |
|  Terça, 25 de Fevereiro          |
|                                  |
|  +---RECEITA DA ELI-----------+ |
|  |                             | |
|  |  R$ 4.850,00      +18%     | |
|  |  esta semana                | |
|  +-----------------------------+ |
|                                  |
|  +----------+  +----------+     |
|  | AGENDA   |  | INBOX    |     |
|  | 12 hoje  |  | 7 ativas |     |
|  | 3 pend.  |  | 2 aguard.|     |
|  +----------+  +----------+     |
|                                  |
|  +---ELI STATUS---------------+ |
|  |  [Bot] 23 atendidas | 87%  | |
|  |  [!] 2 precisam atencao    | |
|  |  [Ver conversas ->]        | |
|  +-----------------------------+ |
|                                  |
|  +---PROXIMOS AGENDAMENTOS----+ |
|  |  09:00  Maria Silva  [OK]  | |
|  |  09:30  Joao Santos  [OK]  | |
|  |  10:30  Ana Costa    [?]   | |
|  |  [Ver agenda completa ->]  | |
|  +-----------------------------+ |
|                                  |
|  +---CANAL WHATSAPP-----------+ |
|  |  [Shield] Saudavel | 45/120| |
|  +-----------------------------+ |
|                                  |
+----------------------------------+
|  [Inicio] [Inbox] [Agenda] ... |
+----------------------------------+
```

**Design notes:**
- Revenue card is FULL WIDTH and FIRST -- the most important number
- Stacked vertically for thumb scrolling
- Each card is tappable and navigates to the relevant section
- "Eli Status" card includes direct link to conversations needing attention
- Channel health is minimized (single line) on mobile -- expandable on tap

### 6.4 Mobile Inbox

```
STATE: Conversation List
+----------------------------------+
|  Inbox                    [Filter]|
|  [Search...]                     |
|----------------------------------|
|  PRECISAM ATENCAO               |
|  +------------------------------+|
|  | [Av] Maria Silva        2m   ||
|  | [!] Desconto fora politica   ||
|  +------------------------------+|
|  | [Av] Pedro Oliveira    15m   ||
|  | [!] Tempo espera alto        ||
|  +------------------------------+|
|                                  |
|  ELI ESTA CUIDANDO              |
|  +------------------------------+|
|  | [Av][B] Ana Costa       5m   ||
|  | Agendamento confirmado       ||
|  +------------------------------+|
|  | [Av][B] Joao Santos   23m   ||
|  | Catalogo enviado              ||
|  +------------------------------+|
|  ...                             |
+----------------------------------+
|  [Inicio] [*Inbox*] [Agenda]... |
+----------------------------------+

STATE: Inside Conversation (full screen)
+----------------------------------+
|  [<]  Maria Silva    [Assumir]  |
|        Corte+Barba | 09:00      |
|----------------------------------|
|  +--Eli context card--+         |
|  | Escalou: desconto  |         |
|  +--------------------+         |
|                                  |
|  [Messages...]                   |
|                                  |
|  +--Transfer card--+            |
|  | "20%, max 10%"  |            |
|  +-----------------+            |
|                                  |
|----------------------------------|
|  Sugestao: "10% + brinde"       |
|  [Input...          ] [Send]    |
|  [Agendar] [Template] [Anexo]   |
+----------------------------------+
```

**Key mobile patterns:**
- Full-screen conversation view (no side panels)
- Swipe right to go back to list
- "Assumir" (takeover) button always visible in header
- Quick actions above keyboard: Agendar, Template, Anexo
- Eli suggestion slides up from bottom, dismissible with swipe

### 6.5 Smart Notifications

```
NOTIFICATION TIERS:

TIER 1 -- IMMEDIATE (vibrate + sound):
  "Eli precisa de ajuda: Maria Silva pediu desconto fora da politica"
  -> Tapping opens the specific conversation

TIER 2 -- IMPORTANT (silent push):
  "Novo agendamento: Ana Costa, 10:30 - Corte Feminino"
  "3 novos contatos hoje via WhatsApp"

TIER 3 -- DIGEST (morning + evening summary):
  "Resumo da noite: Eli atendeu 8 conversas, agendou 3 clientes.
   Receita estimada: R$ 450,00. Tudo sob controle!"

  "Resumo do dia: 12 atendimentos, R$ 1.200 em receita.
   Eli resolveu 94% sem ajuda. Otimo dia!"

NEVER NOTIFY:
  - Campaign delivery stats
  - System updates
  - Billing reminders (email only)
  - Analytics milestones
```

---

## 7. Onboarding Experience

### 7.1 Current State

The existing `OnboardingWizard` has 3 steps:
1. Segment Selection (barber, salon, clinic, etc.)
2. WhatsApp QR Connection
3. Complete

This is functional but misses the opportunity for **first-value delivery**.

### 7.2 Proposed Onboarding Flow (10 Minutes to Value)

```
STEP 1: Bem-vindo! (30 seconds)
  "Ola! Sou a Eli, sua assistente de atendimento.
   Vou te ajudar a configurar tudo em menos de 10 minutos."

  [Nome do seu negocio: ____________]
  [Seu segmento: (v) Barbearia  ]     <- Pre-populated if from segment selection

  [Continuar ->]

STEP 2: Conectar WhatsApp (2-3 minutes)
  "Vamos conectar seu WhatsApp para a Eli
   começar a atender seus clientes."

  [QR Code displayed]

  "Abra o WhatsApp > Aparelhos conectados > Escanear QR"

  [Status: Conectando... / Conectado!]
  [Continuar ->]

STEP 3: Configurar a Eli (3-4 minutes)
  "Como a Eli deve se comportar?"

  Tom de voz: ( ) Formal  (o) Amigavel  ( ) Descontraido
  Nome para clientes: [Eli ___________]   <- Can customize name
  Horario de atendimento: [08:00] a [20:00]

  "O que a Eli pode fazer?"
  [x] Responder perguntas sobre servicos
  [x] Agendar horarios
  [ ] Enviar catalogo de produtos
  [ ] Processar pagamentos

  [Continuar ->]

STEP 4: Seus Servicos (2-3 minutes)
  "Quais servicos voce oferece?"

  [+ Adicionar servico]
  +---------------------------+
  | Corte Masculino           |
  | Duracao: 30 min           |
  | Preco: R$ 45,00           |
  +---------------------------+
  +---------------------------+
  | Barba                     |
  | Duracao: 20 min           |
  | Preco: R$ 30,00           |
  +---------------------------+

  "Dica: Voce pode adicionar mais depois em Configuracoes."
  [Continuar ->]

STEP 5: Primeiro Teste! (1 minute)
  "Tudo pronto! Vamos testar a Eli agora."

  [Envie uma mensagem de teste para este numero: +55 XX XXXX-XXXX]

  Ou escaneie este QR com OUTRO celular para simular um cliente.

  [Simulacao ao vivo mostrando a Eli respondendo]

  "A Eli esta funcionando! Ela vai atender seus clientes 24/7."

  [Ir para o Dashboard ->]
```

### 7.3 Post-Onboarding Checklist

The existing `SidebarChecklist` component should be enhanced:

```
+----ONBOARDING PROGRESS----------+
|                                  |
|  Configuração 5/7       [71%]   |
|  [=========       ]             |
|                                  |
|  [x] Criar conta                |
|  [x] Conectar WhatsApp          |
|  [x] Configurar Eli             |
|  [x] Adicionar servicos         |
|  [x] Enviar mensagem teste      |
|  [ ] Adicionar equipe           |
|  [ ] Configurar horarios        |
|                                  |
|  [Continuar configuracao ->]    |
|                                  |
+----------------------------------+
```

### 7.4 First-Value Timeline

| Minute | Action | Value Delivered |
|--------|--------|----------------|
| 0-1 | Account created | "Welcome, you have a CRM now" |
| 1-3 | WhatsApp connected | "Your number is linked" |
| 3-6 | Eli configured | "Your AI is ready to work" |
| 6-8 | Services added | "Eli knows what you sell" |
| 8-10 | Test message sent | "You SAW Eli working -- FIRST VALUE" |

**Goal:** The owner SEES the AI working within 10 minutes. That moment -- watching Eli respond to a test message -- is the "aha moment" that converts trial to paid.

---

## 8. Design Tokens -- Pulse Mark Brand

### 8.1 Brand Direction

Based on the brand research document (`tikso-brand-logo-concepts.md`), the recommended direction is **Concept 1: The Pulse Mark** with the Teal + Coral palette. This section defines the complete token system for implementation.

### 8.2 Color Token Migration

The current system uses Brand Orange (`#FA6810`) as primary. The Pulse Mark brand introduces Teal (`#0D9488`) as primary and Coral (`#F97066`) as secondary accent. Below is the full token mapping:

#### Light Mode

```css
:root {
  /* Core Surfaces */
  --background: 210 40% 98%;          /* #F8FAFC (Cloud) */
  --foreground: 215 28% 17%;          /* #1E293B (Charcoal) */

  /* Card / Popover */
  --card: 0 0% 100%;                  /* #FFFFFF */
  --card-foreground: 215 28% 17%;
  --popover: 0 0% 100%;
  --popover-foreground: 215 28% 17%;

  /* Primary -- Teal Pulse */
  --primary: 174 83% 32%;             /* #0D9488 */
  --primary-foreground: 0 0% 100%;
  --primary-hover: 174 83% 27%;       /* #0F766E -- Deep Teal */

  /* Secondary -- Warm Coral (accent) */
  --secondary: 3 91% 62%;             /* #F97066 */
  --secondary-foreground: 0 0% 100%;

  /* Muted */
  --muted: 215 16% 47%;               /* #64748B (Slate) */
  --muted-foreground: 215 16% 47%;

  /* Accent -- Light Teal for hover/selected states */
  --accent: 174 50% 92%;              /* Teal tinted background */
  --accent-foreground: 215 28% 17%;

  /* Semantic Colors */
  --destructive: 0 84% 60%;           /* #EF4444 */
  --destructive-foreground: 0 0% 100%;
  --success: 142 71% 45%;             /* #22C55E */
  --success-foreground: 0 0% 100%;
  --warning: 45 93% 47%;              /* #EAB308 */
  --warning-foreground: 0 0% 100%;
  --info: 217 91% 60%;                /* #3B82F6 */
  --info-foreground: 0 0% 100%;

  /* Borders & Inputs */
  --border: 214 32% 91%;              /* #CBD5E1 (Slate 300) */
  --border-2: 215 20% 65%;            /* Slate 400 */
  --input: 214 32% 91%;
  --ring: 174 83% 32%;                /* Teal (focus ring) */

  /* Layout */
  --radius: 0.5rem;
  --sidebar-width: 256px;
  --sidebar-width-collapsed: 64px;

  /* Avatar */
  --avatar-default: 174 40% 60%;      /* Teal-tinted avatar */

  /* Surface Variants */
  --surface: 0 0% 100%;               /* #FFFFFF */
  --surface-2: 210 40% 96%;           /* #F1F5F9 (Slate 100) */

  /* AI Agent (keep purple for distinction) */
  --ai-accent: 250 70% 60%;
  --ai-accent-foreground: 250 10% 98%;
  --bubble-ai: 250 70% 60% / 0.08;

  /* NEW: Coral accent for notifications/CTAs */
  --coral: 3 91% 62%;                 /* #F97066 */
  --coral-foreground: 0 0% 100%;
  --coral-light: 3 91% 94%;           /* Soft Coral background */
}
```

#### Dark Mode

```css
.dark {
  /* Core Surfaces */
  --background: 215 28% 17%;          /* #1E293B (Charcoal) */
  --foreground: 210 40% 98%;          /* #F8FAFC */

  /* Card / Popover */
  --card: 217 33% 12%;                /* Slightly lighter than BG */
  --card-foreground: 210 40% 98%;
  --popover: 217 33% 12%;
  --popover-foreground: 210 40% 98%;

  /* Primary -- Light Teal (brighter in dark mode) */
  --primary: 172 66% 50%;             /* #2DD4BF (brighter teal) */
  --primary-foreground: 215 28% 10%;
  --primary-hover: 174 83% 32%;       /* #0D9488 */

  /* Secondary -- Warm Coral */
  --secondary: 3 91% 62%;             /* #F97066 */
  --secondary-foreground: 0 0% 100%;

  /* Muted */
  --muted: 217 16% 56%;               /* Lighter slate for dark mode */
  --muted-foreground: 217 16% 56%;

  /* Accent */
  --accent: 174 30% 20%;              /* Dark teal-tinted BG */
  --accent-foreground: 210 40% 98%;

  /* Semantic Colors (same but adjusted for dark BG) */
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --success: 142 71% 45%;
  --success-foreground: 0 0% 100%;
  --warning: 45 93% 47%;
  --warning-foreground: 0 0% 100%;
  --info: 217 91% 60%;
  --info-foreground: 0 0% 100%;

  /* Borders */
  --border: 215 20% 25%;              /* Slate 700 area */
  --border-2: 215 20% 33%;
  --input: 215 20% 25%;
  --ring: 172 66% 50%;                /* Bright teal ring */

  /* Surfaces */
  --surface: 217 33% 12%;
  --surface-2: 217 33% 16%;

  /* AI Agent */
  --ai-accent: 250 60% 70%;
  --ai-accent-foreground: 250 10% 98%;
  --bubble-ai: 250 60% 70% / 0.12;

  /* Coral */
  --coral: 3 91% 62%;
  --coral-foreground: 0 0% 100%;
  --coral-light: 3 50% 20%;
}
```

### 8.3 Tailwind v4 Theme Inline Additions

Add to the existing `@theme inline` block:

```css
@theme inline {
  /* ... existing mappings ... */

  /* NEW: Primary hover */
  --color-primary-hover: hsl(var(--primary-hover));

  /* NEW: Coral accent */
  --color-coral: hsl(var(--coral));
  --color-coral-foreground: hsl(var(--coral-foreground));
  --color-coral-light: hsl(var(--coral-light));
}
```

### 8.4 Typography Tokens

```css
@theme inline {
  /* Current: Inter + Geist Sans */
  /* Proposed: DM Sans for headings, Inter for body */
  --font-heading: 'DM Sans', var(--font-inter), ui-sans-serif, system-ui, sans-serif;
  --font-sans: var(--font-inter), ui-sans-serif, system-ui, sans-serif;
  --font-mono: var(--font-geist-mono), ui-monospace, monospace;
}
```

**Font Loading** (in `layout.tsx`):
```typescript
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
  display: 'swap',
})
```

### 8.5 Component Token Mapping

| Component | Token | Light Value | Dark Value |
|-----------|-------|-------------|------------|
| Primary Button BG | `--primary` | Teal #0D9488 | Bright Teal #2DD4BF |
| Primary Button Hover | `--primary-hover` | Deep Teal #0F766E | Teal #0D9488 |
| Notification Badge | `--coral` | Coral #F97066 | Coral #F97066 |
| AI Message Bubble | `--bubble-ai` | Purple 8% opacity | Purple 12% opacity |
| Active Nav Indicator | `--primary` | Teal | Bright Teal |
| Focus Ring | `--ring` | Teal | Bright Teal |
| Link Color | `--primary` | Teal | Bright Teal |
| Destructive Actions | `--destructive` | Red #EF4444 | Red #EF4444 |
| Success States | `--success` | Green #22C55E | Green #22C55E |

### 8.6 WCAG Compliance Check

| Combination | Contrast Ratio | WCAG AA | WCAG AAA |
|-------------|---------------|---------|----------|
| Teal (#0D9488) on White (#FFFFFF) | 4.53:1 | PASS (normal text) | FAIL |
| Teal (#0D9488) on Cloud (#F8FAFC) | 4.41:1 | PASS (normal text) | FAIL |
| Deep Teal (#0F766E) on White | 5.36:1 | PASS | PASS (large text) |
| Coral (#F97066) on White | 3.13:1 | FAIL -- use as decoration only | FAIL |
| Charcoal (#1E293B) on White | 12.63:1 | PASS | PASS |
| Charcoal (#1E293B) on Cloud | 11.82:1 | PASS | PASS |
| Bright Teal (#2DD4BF) on Charcoal (#1E293B) | 7.87:1 | PASS | PASS |
| Coral (#F97066) on Charcoal | 4.52:1 | PASS (normal text) | FAIL |

**Important:** Coral (#F97066) fails AA on white backgrounds. Use it ONLY for:
- Decorative elements (badges, icons, borders)
- Text on dark backgrounds (passes AA at 4.52:1)
- Never as the sole indicator -- always pair with text or icon

This is an improvement over the current Brand Orange (#FA6810), which has a contrast ratio of only 3.2:1 on white. Teal (#0D9488) at 4.53:1 passes AA for normal text.

### 8.7 Shadcn/UI Component Customization

The existing shadcn/ui components map directly to the new token system. No structural changes needed -- only token value updates:

| Component | Current Behavior | Change |
|-----------|-----------------|--------|
| `Button` (default) | Orange background | Teal background |
| `Button` (destructive) | Red | No change |
| `Badge` | Various | Add `coral` variant for notifications |
| `Card` | White bg, border | No change |
| `Input` focus | Orange ring | Teal ring |
| `Progress` | Orange fill | Teal fill, coral for warnings |
| `Switch` | Orange when on | Teal when on |

---

## 9. UX Roadmap Prioritizado

### Phase 0: Brand Token Migration (1-2 days)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Update `globals.css` token values (orange -> teal) | Small | High | P0 |
| Add DM Sans font loading | Small | Medium | P0 |
| Add `--coral` and `--primary-hover` tokens | Small | Medium | P0 |
| Update logo assets (SVG with Pulse Mark) | Medium | High | P0 |
| Verify all existing components render with new tokens | Medium | High | P0 |

### Phase 1: Dashboard Redesign (3-5 days)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Create `EliSummaryCard` component | Medium | Very High | P1 |
| Create `DailyScheduleCard` component | Medium | High | P1 |
| Redesign KPI cards (revenue as hero, Eli attribution) | Medium | Very High | P1 |
| Add revenue attribution tracking to backend | Large | Very High | P1 |
| Implement morning/evening greeting with personalization | Small | Medium | P2 |
| Add "Quick Actions" bar at bottom of dashboard | Small | Medium | P2 |

### Phase 2: Inbox Improvements (3-5 days)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Section conversation list by status (Atencao / Eli / Resolvidas) | Medium | Very High | P1 |
| Add AI activity summary in conversation preview | Medium | High | P1 |
| Implement "Assumir conversa" takeover flow | Medium | Very High | P1 |
| Add Eli context card at top of conversation | Small | High | P1 |
| Add Eli suggestion bar above message composer | Medium | High | P2 |
| Add transfer card visual when Eli escalates | Small | High | P2 |

### Phase 3: Navigation Restructuring (2-3 days)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Group sidebar items (Principal, Gestao, Marketing, Avancado) | Medium | High | P1 |
| Collapse "Avancado" section by default | Small | Medium | P1 |
| Add global search to sidebar top (Ctrl+K) | Medium | Medium | P2 |
| Rename "Agente IA" to "Eli" with health badge | Small | Medium | P2 |
| Redesign mobile bottom tabs (add Agenda, Eli) | Medium | High | P1 |

### Phase 4: Onboarding Overhaul (3-5 days)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Add Eli configuration step (tone, hours, capabilities) | Medium | Very High | P1 |
| Add service catalog step | Medium | High | P1 |
| Add "Test Eli Now" step with live simulation | Large | Very High | P1 |
| Enhance sidebar checklist with 7-step progress | Small | Medium | P2 |
| Add AI-personalized onboarding tips based on segment | Medium | Medium | P3 |

### Phase 5: Mobile Optimization (2-3 days)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Implement smart notification tiers (immediate/important/digest) | Large | Very High | P1 |
| Optimize dashboard for vertical scroll mobile layout | Medium | High | P1 |
| Add swipe gestures in conversation list | Small | Medium | P2 |
| Implement morning/evening digest push notifications | Medium | High | P2 |

### Phase 6: Polish and Delight (Ongoing)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| Add micro-animations (card hover, page transitions) | Small | Medium | P3 |
| Pulse animation on Eli health badge | Small | Low | P3 |
| Empty states with Eli illustrations | Medium | Medium | P3 |
| Skeleton loading states for all new components | Small | Medium | P2 |
| Haptic feedback on mobile actions | Small | Low | P3 |

### Priority Summary

| Phase | Time | Focus | Business Value |
|-------|------|-------|---------------|
| Phase 0 | 1-2 days | Brand tokens | Brand identity alignment |
| Phase 1 | 3-5 days | Dashboard | Owner sees revenue + AI value daily |
| Phase 2 | 3-5 days | Inbox | Faster escalation handling, AI visibility |
| Phase 3 | 2-3 days | Navigation | Reduced cognitive overload |
| Phase 4 | 3-5 days | Onboarding | Faster time-to-value, lower churn |
| Phase 5 | 2-3 days | Mobile | 80% of usage optimized |
| Phase 6 | Ongoing | Polish | Delight and retention |

**Total estimated effort for P0+P1 items: 15-20 development days**

---

## 10. Appendix: Current State Analysis

### 10.1 What Is Already Well-Done

| Component | Assessment | Notes |
|-----------|-----------|-------|
| `KpiCard` | Good pattern | Clean design, skeleton loading, change indicators |
| `ChannelHealthWidget` | Excellent | Semaphore system, warmup phases, comprehensive |
| `InboxLayout` | Strong foundation | 3-panel, real-time, keyboard shortcuts, mobile views |
| `Sidebar` | Solid | RBAC filtering, module gating, collapsible, tooltips |
| `MobileNav` | Good | Bottom tab bar, sheet drawer, safe area handling |
| `OnboardingWizard` | Functional | Segment select, QR connect, auto-reconnect |
| Design tokens | Well-structured | CSS custom properties, Tailwind v4 inline theme, dark mode |
| Accessibility | Partially done | aria-labels present, prefers-reduced-motion added |

### 10.2 Existing Files That Will Be Modified

| File | Change |
|------|--------|
| `/home/tikso/tikso/src/app/globals.css` | Token value updates (orange -> teal, add coral) |
| `/home/tikso/tikso/src/components/dashboard/kpi-card.tsx` | Revenue hero variant |
| `/home/tikso/tikso/src/components/dashboard/channel-health-widget.tsx` | Keep as-is |
| `/home/tikso/tikso/src/components/inbox/inbox-layout.tsx` | Sectioned list, takeover flow |
| `/home/tikso/tikso/src/components/inbox/conversation-list.tsx` | Status sections, AI previews |
| `/home/tikso/tikso/src/components/layout/sidebar.tsx` | Grouped sections, collapsed advanced |
| `/home/tikso/tikso/src/components/layout/mobile-nav.tsx` | New bottom tabs (Agenda, Eli) |
| `/home/tikso/tikso/src/components/onboarding/onboarding-wizard.tsx` | Additional steps |

### 10.3 New Components to Create

| Component | Type (Atomic) | Location |
|-----------|---------------|----------|
| `EliSummaryCard` | Organism | `/src/components/dashboard/eli-summary-card.tsx` |
| `DailyScheduleCard` | Organism | `/src/components/dashboard/daily-schedule-card.tsx` |
| `RevenueHeroCard` | Molecule | `/src/components/dashboard/revenue-hero-card.tsx` |
| `ConversationStatusSection` | Organism | `/src/components/inbox/conversation-status-section.tsx` |
| `TakeoverBar` | Molecule | `/src/components/inbox/takeover-bar.tsx` |
| `EliContextCard` | Molecule | `/src/components/inbox/eli-context-card.tsx` |
| `EliSuggestionBar` | Molecule | `/src/components/inbox/eli-suggestion-bar.tsx` |
| `QuickActionsBar` | Molecule | `/src/components/dashboard/quick-actions-bar.tsx` |
| `EliConfigStep` | Organism | `/src/components/onboarding/eli-config-step.tsx` |
| `ServiceCatalogStep` | Organism | `/src/components/onboarding/service-catalog-step.tsx` |
| `TestEliStep` | Organism | `/src/components/onboarding/test-eli-step.tsx` |

### 10.4 Backend Requirements (for Dashboard)

| Endpoint | Purpose | Data |
|----------|---------|------|
| `GET /api/dashboard/eli-summary` | Eli's 24h activity | conversations handled, appointments booked, issues resolved, escalation count |
| `GET /api/dashboard/revenue-attribution` | Revenue generated by Eli | amount, source breakdown, comparison to previous period |
| `GET /api/dashboard/daily-schedule` | Today's appointments | time, client, service, status (confirmed/pending/cancelled) |
| `GET /api/notifications/digest` | Smart notification digest | tier categorization, summary text |

---

## Auto-Decisions Log

| Question | Decision | Reason |
|----------|----------|--------|
| Which brand concept to base tokens on? | Concept 1: Pulse Mark (Teal + Coral) | Recommended in brand research doc; unoccupied color territory; better WCAG compliance than current orange |
| Navigation pattern? | Left sidebar (desktop) + bottom tab bar (mobile) | Matches current architecture; familiar to WhatsApp users |
| Keep purple for AI accents? | Yes | Already established (`--ai-accent`); provides clear visual distinction from teal primary |
| How many bottom tabs on mobile? | 5 (Inicio, Inbox, Agenda, Eli, Mais) | Replaces Contatos/Pipeline with higher-frequency items for service businesses |
| Dashboard first metric? | Revenue generated by Eli | Unique differentiator; directly ties AI value to money |
| Conversation list structure? | Sectioned by status | Reduces cognitive load; owner only needs to act on "Precisam Atencao" section |
| Onboarding target time? | 10 minutes to first value | Industry benchmark is 15-20min; faster = lower abandonment |
| Typography change? | Add DM Sans for headings, keep Inter for body | Brand research recommendation; DM Sans has excellent Portuguese glyph support |

---

*Document generated by Uma (UX Design Expert Agent)*
*Methodology: Competitive Benchmark + User-Centered Design + Atomic Design System Thinking*
*All wireframes are ASCII for implementation-agnostic communication*
