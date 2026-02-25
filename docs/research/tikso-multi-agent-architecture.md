# Tikso Multi-Agent Architecture -- Eli 2.0

**Data:** 2026-02-25
**Arquiteta:** Aria (AIOS Architect)
**Versao:** 1.0.0
**Status:** DRAFT -- Pending Review
**Documentos prerequisitos:**
- [Analise de Conversa Eli/Kelmer](/root/aios-core/docs/research/eli-chatbot-conversation-analysis.md)
- [Inteligencia Competitiva AwSales](/root/aios-core/docs/research/awsales-competitive-intelligence.md)
- [Storytelling AwSales](/root/aios-core/docs/research/awsales-storytelling-analysis.md)
- [Antiban Best Practices](/root/aios-core/docs/research/whatsapp-antiban-best-practices.md)

---

## Sumario Executivo

Este documento projeta a evolucao da Tikso de um unico agente (Eli) para uma **plataforma de agentes especializados**. A arquitetura foi concebida para resolver os problemas criticos identificados na analise de conversa (horarios fantasma, falha de service ID, ausencia de human handoff) enquanto habilita novos fluxos de receita (vendas, retencao, campanhas, feedback).

A arquitetura segue quatro principios fundamentais:

1. **Single Conversation Owner** -- Apenas um agente controla uma conversa por vez. Sem conflitos.
2. **Shared Memory, Private Tools** -- Todos os agentes acessam o mesmo perfil de cliente, mas cada um tem suas ferramentas especializadas.
3. **Antiban by Design** -- O sistema de antiban e uma camada de infraestrutura, nao uma responsabilidade do agente.
4. **Flywheel Architecture** -- Cada interacao alimenta inteligencia que melhora a proxima interacao.

**Decisao de stack:** A arquitetura reutiliza 100% do stack existente (Next.js 16, Prisma 7.4, Redis, BullMQ, Claude API, Evolution API). Nenhuma nova tecnologia de infraestrutura e necessaria.

---

## Table of Contents

1. [Diagrama Completo da Arquitetura](#1-diagrama-completo-da-arquitetura)
2. [Agent Router -- Roteamento de Mensagens](#2-agent-router--roteamento-de-mensagens)
3. [Agentes Especializados](#3-agentes-especializados)
4. [Conversational Flywheel Architecture](#4-conversational-flywheel-architecture)
5. [Tool System Evolution](#5-tool-system-evolution)
6. [Memory and Context System](#6-memory-and-context-system)
7. [Campaign Engine Architecture](#7-campaign-engine-architecture)
8. [Antiban Compliance Layer](#8-antiban-compliance-layer)
9. [Scalability -- Multi-Tenant at Scale](#9-scalability--multi-tenant-at-scale)
10. [Cost Optimization](#10-cost-optimization)
11. [Roadmap de Implementacao](#11-roadmap-de-implementacao)
12. [Trade-off Analysis](#12-trade-off-analysis)
13. [Security Considerations](#13-security-considerations)

---

## 1. Diagrama Completo da Arquitetura

### 1.1 System Overview (Macro)

```
+===========================================================================+
|                         TIKSO MULTI-AGENT PLATFORM                        |
+===========================================================================+
|                                                                           |
|  +-- INBOUND LAYER ------------------------------------------------+     |
|  |                                                                  |     |
|  |  [WhatsApp]  [WebChat]  [Instagram]  [Manual Trigger]           |     |
|  |       |           |          |              |                    |     |
|  |       v           v          v              v                    |     |
|  |  +------------------------------------------------------+       |     |
|  |  |           MESSAGE GATEWAY (Evolution API)             |       |     |
|  |  |  - Webhook receiver                                   |       |     |
|  |  |  - Message normalization                              |       |     |
|  |  |  - Media handling                                     |       |     |
|  |  +------------------------------------------------------+       |     |
|  +------------------------------------------------------------------+     |
|       |                                                                   |
|       v                                                                   |
|  +-- PROCESSING LAYER ---------------------------------------------+     |
|  |                                                                  |     |
|  |  +------------------------------------------------------+       |     |
|  |  |            MESSAGE PROCESSOR (existing)               |       |     |
|  |  |  - Dedup, validation, org resolution                  |       |     |
|  |  +------------------------------------------------------+       |     |
|  |       |                                                          |     |
|  |       v                                                          |     |
|  |  +------------------------------------------------------+       |     |
|  |  |            NEXUS ORCHESTRATOR (existing)              |       |     |
|  |  |  - Context loading                                    |       |     |
|  |  |  - DNA/CAIO/FORGE pipeline                            |       |     |
|  |  +------------------------------------------------------+       |     |
|  |       |                                                          |     |
|  |       v                                                          |     |
|  |  +------------------------------------------------------+       |     |
|  |  |               AGENT ROUTER (NEW)                      |       |     |
|  |  |                                                       |       |     |
|  |  |  1. Check active conversation lock                    |       |     |
|  |  |  2. Intent classification (LLM or rules)              |       |     |
|  |  |  3. Route to specialized agent                        |       |     |
|  |  |  4. Handle handoff between agents                     |       |     |
|  |  +------------------------------------------------------+       |     |
|  |       |           |           |          |           |           |     |
|  |       v           v           v          v           v           |     |
|  |  +---------+ +---------+ +---------+ +---------+ +---------+   |     |
|  |  |   ELI   | |  SALES  | | RETAIN  | |CAMPAIGN | |FEEDBACK |   |     |
|  |  | (Recep) | | (Closer)| | (Keeper)| |(Blaster)| |(Pulse)  |   |     |
|  |  +---------+ +---------+ +---------+ +---------+ +---------+   |     |
|  |       |           |           |          |           |           |     |
|  |       +-----+-----+-----+----+-----+----+-----+-----+          |     |
|  |             |                 |                |                 |     |
|  |             v                 v                v                 |     |
|  |     +-------------+   +-------------+   +-------------+        |     |
|  |     | TOOL SYSTEM |   |MEMORY SYSTEM|   | LLM GATEWAY |        |     |
|  |     | (Registry)  |   |(Short/Med/  |   | (Claude API) |        |     |
|  |     |             |   | Long-term)  |   |              |        |     |
|  |     +-------------+   +-------------+   +-------------+        |     |
|  +------------------------------------------------------------------+     |
|       |                                                                   |
|       v                                                                   |
|  +-- OUTBOUND LAYER -----------------------------------------------+     |
|  |                                                                  |     |
|  |  +------------------------------------------------------+       |     |
|  |  |            ANTIBAN MIDDLEWARE (existing)               |       |     |
|  |  |  - Rate limiter (per-org, per-destination)            |       |     |
|  |  |  - Typing simulation                                  |       |     |
|  |  |  - Gaussian jitter                                    |       |     |
|  |  |  - Health monitor                                     |       |     |
|  |  |  - Queue prioritization                               |       |     |
|  |  +------------------------------------------------------+       |     |
|  |       |                                                          |     |
|  |       v                                                          |     |
|  |  +------------------------------------------------------+       |     |
|  |  |           OUTBOUND QUEUE (BullMQ)                     |       |     |
|  |  |  - Priority queues per message type                   |       |     |
|  |  |  - Scheduled delivery                                 |       |     |
|  |  |  - Retry with backoff                                 |       |     |
|  |  +------------------------------------------------------+       |     |
|  |       |                                                          |     |
|  |       v                                                          |     |
|  |  [Evolution API] --> [WhatsApp]                                  |     |
|  +------------------------------------------------------------------+     |
|                                                                           |
|  +-- DATA LAYER ---------------------------------------------------+     |
|  |                                                                  |     |
|  |  [PostgreSQL/Prisma]    [Redis]           [BullMQ]              |     |
|  |  - Customers            - Session cache   - Message queues      |     |
|  |  - Conversations        - Agent locks     - Campaign jobs       |     |
|  |  - Appointments         - Rate limits     - Cron jobs           |     |
|  |  - Business config      - Typing state    - Retry queues       |     |
|  |  - Agent configs        - Context cache                         |     |
|  |  - Campaign data                                                |     |
|  |  - Feedback/NPS                                                 |     |
|  +------------------------------------------------------------------+     |
|                                                                           |
|  +-- OBSERVABILITY LAYER ------------------------------------------+     |
|  |                                                                  |     |
|  |  [Flywheel Analytics]   [Agent Metrics]   [Health Monitor]      |     |
|  |  - Conversion funnel    - Response time   - Connection status   |     |
|  |  - Revenue attribution  - Handoff rate    - Error rates         |     |
|  |  - Customer lifetime    - Resolution %    - Antiban risk score  |     |
|  +------------------------------------------------------------------+     |
+===========================================================================+
```

### 1.2 Agent Routing Flow (Detail)

```
                        INCOMING MESSAGE
                              |
                              v
                    +-------------------+
                    | Is there an active |
                    | conversation lock? |
                    +-------------------+
                      |              |
                     YES             NO
                      |              |
                      v              v
              +---------------+  +------------------+
              | Route to the  |  | INTENT CLASSIFIER |
              | locked agent  |  | (Tier 1: Rules)   |
              +---------------+  +------------------+
                                    |
                          +---------+---------+
                          |         |         |
                     MATCH?    AMBIGUOUS?   NO MATCH?
                          |         |         |
                          v         v         v
                    +--------+ +--------+ +--------+
                    |Route to| |Tier 2: | |Default |
                    |matched | |LLM     | |to Eli  |
                    |agent   | |classify | |(Recep) |
                    +--------+ +--------+ +--------+
                                  |
                            +-----+-----+
                            |           |
                       CLASSIFIED    UNCERTAIN
                            |           |
                            v           v
                      +--------+  +--------+
                      |Route to|  |Route to|
                      |agent   |  |Eli +   |
                      |        |  |flag for |
                      +--------+  |review  |
                                  +--------+
```

### 1.3 Agent Handoff Flow

```
    AGENT A (e.g., Eli)                    AGENT B (e.g., Sales)
         |                                       |
         | [Detects sales intent]                |
         |                                       |
         v                                       |
    +-------------------+                        |
    | Create HandoffReq |                        |
    | - reason          |                        |
    | - context summary |                        |
    | - customer data   |                        |
    | - conversation    |                        |
    +-------------------+                        |
         |                                       |
         v                                       |
    +-------------------+                        |
    | Send transition   |                        |
    | message to client |                        |
    | "Vou te conectar  |                        |
    |  com nosso        |                        |
    |  especialista..." |                        |
    +-------------------+                        |
         |                                       |
         v                                       v
    +--------------------------------------------------+
    |           AGENT ROUTER                            |
    |  1. Release lock from Agent A                     |
    |  2. Save handoff context to Redis                 |
    |  3. Acquire lock for Agent B                      |
    |  4. Pass enriched context to Agent B              |
    +--------------------------------------------------+
                                                 |
                                                 v
                                         +---------------+
                                         | Agent B reads |
                                         | handoff ctx   |
                                         | and continues |
                                         | conversation  |
                                         | seamlessly    |
                                         +---------------+
```

---

## 2. Agent Router -- Roteamento de Mensagens

### 2.1 Design Decision: Hybrid Router (Rules + LLM Fallback)

[AUTO-DECISION] Should the router use pure LLM classification or rules-based? -> Hybrid: rules first, LLM fallback (reason: 80% of messages can be classified by simple keyword/context rules at near-zero cost; LLM fallback handles the ambiguous 20% without wasting tokens on obvious cases)

**Architecture:**

```typescript
// /src/lib/ai/agent-router.ts

interface RouteDecision {
  agentId: AgentId;
  confidence: number;       // 0.0 - 1.0
  reason: string;
  tier: 'lock' | 'rules' | 'llm' | 'default';
}

type AgentId = 'eli' | 'sales' | 'retention' | 'campaign' | 'feedback';

class AgentRouter {
  // Tier 0: Check existing conversation lock (Redis)
  // Tier 1: Rule-based classification (keywords, conversation state, triggers)
  // Tier 2: LLM classification (Claude haiku -- fast, cheap)
  // Tier 3: Default to Eli (receptionist catches all)

  async route(message: IncomingMessage, context: ConversationContext): Promise<RouteDecision>;
}
```

### 2.2 Tier 0: Conversation Lock (Redis)

Every active conversation has a lock in Redis that assigns it to exactly one agent. This is the **primary conflict prevention mechanism**.

```
Key:    conv_lock:{orgId}:{contactPhone}
Value:  { agentId: "eli", lockedAt: timestamp, ttl: 1800 }
TTL:    30 minutes (auto-release if no activity)
```

**Rules:**
- If lock exists and is not expired, route to locked agent. No exceptions.
- If lock exists but expired (>30 min since last message), release and reclassify.
- Lock is released explicitly on: conversation end, agent handoff, or human takeover.

**Why Redis and not DB:** Lock operations happen on every single message. Redis provides sub-millisecond latency and atomic operations (SET NX EX) that prevent race conditions. Prisma round-trip would add 5-15ms per message.

### 2.3 Tier 1: Rule-Based Classification

Fast keyword/context rules that cover ~80% of routing decisions:

```typescript
const ROUTING_RULES: RoutingRule[] = [
  // --- SCHEDULING (Eli) ---
  { patterns: ['agendar', 'horario', 'marcar', 'reservar', 'disponivel',
               'corte', 'barba', 'cabelo', 'agenda', 'remarcar', 'cancelar',
               'desmarcar'],
    agent: 'eli', confidence: 0.9 },

  // --- SALES ---
  { patterns: ['plano', 'assinatura', 'preco', 'valor', 'desconto',
               'promocao', 'pacote', 'comprar', 'upgrade', 'mensalidade'],
    agent: 'sales', confidence: 0.85 },

  // --- FEEDBACK ---
  { patterns: ['nota', 'avaliacao', 'reclamacao', 'elogio', 'sugestao',
               'feedback', 'review', 'estrela', 'nps'],
    agent: 'feedback', confidence: 0.9 },

  // --- CONTEXT-BASED (overrides keywords) ---
  { condition: (ctx) => ctx.lastAgent === 'sales' && ctx.minutesSinceLastMsg < 30,
    agent: 'sales', confidence: 0.95 },
  { condition: (ctx) => ctx.isProactiveCampaign === true,
    agent: 'campaign', confidence: 1.0 },
  { condition: (ctx) => ctx.isRetentionTarget === true && ctx.isFirstMsgInThread,
    agent: 'retention', confidence: 0.9 },
];
```

### 2.4 Tier 2: LLM Classification (Claude Haiku)

For ambiguous messages that rules cannot classify (estimated ~20%):

```typescript
const CLASSIFICATION_PROMPT = `
Classify the following WhatsApp message into one of these categories:
- SCHEDULING: appointment booking, rescheduling, cancellation, availability check
- SALES: pricing questions, plan upgrades, promotions, subscription inquiries
- RETENTION: re-engagement from inactive customer, win-back scenarios
- FEEDBACK: reviews, complaints, suggestions, NPS
- GENERAL: greetings, FAQ, general questions

Customer context:
- Name: {customerName}
- Last visit: {lastVisit}
- Active plan: {planName}
- Last agent: {lastAgent}

Message: "{messageText}"

Reply with ONLY the category name.
`;
```

**Cost note:** Claude 3.5 Haiku costs ~$0.25/1M input tokens. A classification prompt is ~200 tokens. At 1000 ambiguous messages/day, this costs ~$0.05/day -- negligible.

### 2.5 Tier 3: Default to Eli

If all tiers fail or confidence is below 0.6, route to Eli (receptionist). Eli is the catch-all. She can always hand off to a specialist.

### 2.6 Conflict Prevention -- The Single Owner Rule

**CRITICAL ARCHITECTURAL INVARIANT:** At any given moment, a conversation belongs to exactly ONE agent. There is no scenario where two agents process the same conversation simultaneously.

Enforcement mechanism:

1. **Redis Lock (SET NX):** Atomic. If two messages arrive simultaneously, only the first acquires the lock.
2. **BullMQ Single Consumer:** Each conversation is processed by exactly one worker (keyed by contactPhone).
3. **Handoff Protocol:** Lock transfer is a single atomic Redis MULTI/EXEC (delete old, set new).

---

## 3. Agentes Especializados

### 3.1 Agent Architecture Overview

Each agent follows a common interface but has specialized behavior:

```typescript
// /src/lib/ai/agents/base-agent.ts

interface Agent {
  id: AgentId;
  name: string;
  systemPrompt: string;
  tools: Tool[];

  // Core methods
  handleMessage(msg: Message, ctx: AgentContext): Promise<AgentResponse>;
  canHandoff(to: AgentId): boolean;
  buildPrompt(ctx: AgentContext): string;
}

interface AgentContext {
  customer: CustomerProfile;        // From Prisma
  conversation: ConversationHistory; // Recent messages
  memory: CustomerMemory;           // Short + medium term
  businessConfig: BusinessConfig;   // Org-specific settings
  handoffContext?: HandoffContext;   // If coming from another agent
}

interface AgentResponse {
  messages: OutboundMessage[];       // What to send to the customer
  toolCalls: ToolCall[];            // Side effects (booking, CRM update, etc.)
  handoff?: HandoffRequest;         // If agent wants to transfer
  memoryUpdates: MemoryUpdate[];    // What to remember
  analytics: AnalyticsEvent[];      // What to track
}
```

### 3.2 Eli -- The Receptionist (EXISTING, ENHANCED)

**Persona:** Friendly, efficient, knows the business intimately.
**Scope:** Scheduling, FAQ, greetings, general inquiries, first contact.
**Evolution from current:** Add customer intelligence, fix service ID validation, add human handoff.

```
System Prompt (core):
"You are Eli, the virtual receptionist for {businessName}. You handle
scheduling, answer common questions, and make customers feel welcome.

KEY BEHAVIORS:
- For returning customers: greet by name, offer their usual service
- NEVER offer time slots shorter than the service duration
- If you fail to book twice, immediately hand off to a human
- NEVER expose technical errors to the customer
- You can hand off to: Sales (pricing/plans), Human (errors/complaints)"
```

**Exclusive Tools:**
- `checkAvailability(serviceId, date, barberId?)` -- enhanced with duration filtering
- `createAppointment(customerId, serviceId, barberId, datetime)`
- `cancelAppointment(appointmentId)`
- `rescheduleAppointment(appointmentId, newDatetime)`
- `getServiceCatalog(orgId)` -- returns services with durations and valid IDs
- `humanHandoff(reason, contextSummary)` -- escalate to human

**Improvements over current Eli:**
1. Validates service IDs on startup (catches the Kelmer bug)
2. Filters time slots by `serviceDuration + bufferTime`
3. Loads customer history before first response
4. Auto-escalates to human after 2 consecutive failures
5. Never exposes internal errors (sanitized error messages)

### 3.3 Sales Agent -- The Closer

**Persona:** Consultative, value-oriented, never pushy.
**Scope:** Plan sales, upsell, cross-sell, pricing questions, subscription management.
**Trigger:** Customer asks about pricing, plans, or promotions; Eli detects purchase intent.

```
System Prompt (core):
"You are the sales specialist for {businessName}. You help customers
find the perfect plan or package for their needs.

KEY BEHAVIORS:
- Always understand the customer's needs before recommending
- Present maximum 3 options (avoid paradox of choice)
- Use social proof: 'X% of our clients prefer this plan'
- If customer objects on price, reframe as value per visit
- Generate urgency contextually, never artificially
- You can hand off to: Eli (scheduling), Human (custom negotiations)"
```

**Exclusive Tools:**
- `getPlans(orgId)` -- returns available plans with pricing
- `calculateSavings(customerId, planId)` -- shows savings vs pay-per-visit
- `createSubscription(customerId, planId)`
- `applyDiscount(customerId, discountCode)`
- `getCustomerSpendHistory(customerId)` -- revenue data for value framing

**Conversational Flywheel contribution:** Sales data feeds into retention triggers. A customer who bought a plan but stopped visiting becomes a retention target.

### 3.4 Retention Agent -- The Keeper

**Persona:** Caring, personal, makes customers feel valued.
**Scope:** Reactivation of inactive customers, no-show follow-up, churn prevention.
**Trigger:** Proactive (cron-based) for customers inactive >30 days; reactive when customer mentions leaving.

```
System Prompt (core):
"You are the retention specialist for {businessName}. Your goal is
to bring back customers who haven't visited recently.

KEY BEHAVIORS:
- Lead with empathy: 'We noticed you haven't been around, everything ok?'
- Reference their specific history: last service, preferred barber
- Offer a concrete incentive only if needed (discount, free add-on)
- Never be guilt-tripping or desperate
- Maximum 2 messages if no response -- respect their silence
- You can hand off to: Eli (if they want to schedule), Sales (if interested in plans)"
```

**Exclusive Tools:**
- `getInactiveCustomers(orgId, daysSinceLastVisit)` -- segmentation query
- `getCustomerHistory(customerId)` -- full visit history with preferences
- `createRetentionOffer(customerId, offerType)` -- generate personalized offer
- `trackRetentionOutcome(customerId, outcome)` -- won-back, lost, pending

**Proactive triggers (via PULSE/cron):**
- 30 days inactive: first reactivation message
- 60 days inactive: second attempt with incentive
- 90 days inactive: final attempt, mark as churned if no response

### 3.5 Campaign Agent -- The Blaster

**Persona:** Professional, informative, respects boundaries.
**Scope:** Segmented campaign dispatch, bulk messaging, promotional announcements.
**Trigger:** Admin-initiated campaigns from dashboard; automated triggers (birthday, seasonal).

```
System Prompt (core):
"You are the campaign manager for {businessName}. You send targeted
promotional messages to customer segments.

KEY BEHAVIORS:
- ALWAYS use approved message templates
- ALWAYS personalize: name, last service, preferences
- NEVER send the same message to more than 3 contacts (content variation)
- Respect opt-out preferences absolutely
- If customer replies to a campaign, hand off to the appropriate agent
- Campaign messages ONLY during business hours (8h-20h)"
```

**Exclusive Tools:**
- `getSegment(orgId, segmentCriteria)` -- query customer segments
- `getApprovedTemplates(orgId, campaignType)` -- message templates
- `personalizeTemplate(templateId, customerId)` -- fill template with customer data
- `scheduleMessage(customerId, message, scheduledAt)` -- queue for delivery
- `trackCampaignMetrics(campaignId)` -- opens, replies, conversions
- `generateVariation(templateId, variationIndex)` -- content variation for antiban

**Antiban integration:** The Campaign Agent is the most tightly coupled with the antiban middleware. It MUST:
1. Respect per-org daily limits
2. Use content variation (min 5 variants per template)
3. Add gaussian jitter between sends (90-180s between contacts)
4. Pause automatically if risk score exceeds threshold

### 3.6 Feedback Agent -- The Listener

**Persona:** Empathetic, grateful, takes complaints seriously.
**Scope:** Post-service NPS, review collection, complaint handling.
**Trigger:** Proactive (2h after appointment completion); reactive when customer mentions feedback.

```
System Prompt (core):
"You are the feedback specialist for {businessName}. You collect
customer satisfaction data and handle complaints.

KEY BEHAVIORS:
- Thank the customer for their visit before asking for feedback
- Use a simple 1-5 scale for NPS (not 1-10 -- WhatsApp UX)
- If score <= 3: immediately ask what went wrong, empathize, log for human review
- If score >= 4: ask for a Google review (with direct link)
- NEVER argue with complaints -- acknowledge and escalate
- You can hand off to: Human (serious complaints), Eli (if they want to reschedule)"
```

**Exclusive Tools:**
- `sendNPSSurvey(customerId, appointmentId)` -- structured NPS
- `recordFeedback(customerId, score, comments)` -- save to DB
- `requestGoogleReview(customerId, reviewLink)` -- for high NPS scores
- `escalateComplaint(customerId, summary)` -- flag for human attention
- `getAppointmentDetails(appointmentId)` -- context for post-service feedback

**Flywheel contribution:** Feedback data feeds into:
- Business intelligence (which barbers get highest NPS?)
- Retention triggers (low NPS = retention risk)
- Sales insights (what services have highest satisfaction?)

---

## 4. Conversational Flywheel Architecture

### 4.1 The Flywheel Model

Inspired by AwSales' "Conversational Flywheel" but adapted for service businesses:

```
                         +---> [MEASURE] ---+
                         |                   |
                         |    Track NPS,     |
                         |    completion %,  |
                         |    revenue/conv   |
                         |                   |
                    [SELL] <---+         +---> [IMPROVE]
                         |     |         |         |
                    Upsell,    |         |    Update prompts,
                    plans,     |         |    fix patterns,
                    packages   |         |    train agents
                         |     |         |         |
                    [HELP] <---+---------+--> [UNDERSTAND]
                         |                         |
                    Schedule,                 Load customer
                    answer FAQ,               profile, intent,
                    resolve issues            preferences
                         |                         |
                         +---> [CONNECT] ---+------+
                                    |
                              Personalized
                              greeting,
                              remember history,
                              right agent
```

### 4.2 How Each Agent Contributes to the Flywheel

| Flywheel Phase | Primary Agent | Data Generated | Feeds Into |
|----------------|--------------|----------------|------------|
| **UNDERSTAND** | Agent Router + Memory System | Intent classification, customer segment | Agent selection, personalization |
| **CONNECT** | Eli (Receptionist) | Greeting preference, communication style | Future greetings, all agents |
| **HELP** | Eli + Feedback Agent | Service completion, issue resolution | NPS correlation, retention triggers |
| **SELL** | Sales Agent | Conversion data, objection patterns | Pricing optimization, campaign targeting |
| **MEASURE** | Feedback Agent + Analytics | NPS scores, review rate, revenue per conversation | Business intelligence dashboard |
| **IMPROVE** | System (automated) | Pattern analysis, failure modes | Prompt tuning, rule updates, training data |

### 4.3 Data Loops -- How Conversations Feed Intelligence

```
LOOP 1: Customer Intelligence Loop
  Conversation --> Extract preferences --> Store in CustomerMemory
  --> Next conversation loads memory --> More personalized response
  --> Higher satisfaction --> Better retention

LOOP 2: Business Intelligence Loop
  All conversations --> Aggregate metrics --> Identify patterns
  --> Adjust agent prompts --> Better responses
  --> Higher conversion --> More revenue

LOOP 3: Retention Loop
  Appointment completed --> Feedback collected --> Low NPS?
  --> Trigger retention agent --> Prevent churn
  --> Customer returns --> More data --> Better predictions

LOOP 4: Sales Loop
  Customer profile enriched --> Identify upsell opportunities
  --> Sales agent engages --> Conversion or not
  --> Learn what works --> Improve sales prompts
  --> Better targeting --> Higher conversion
```

### 4.4 Flywheel Metrics (KPIs)

| Metric | Current (Estimated) | Target (6 months) | Owner Agent |
|--------|--------------------|--------------------|-------------|
| Conversation-to-booking rate | ~35-45% | >85% | Eli |
| Messages per completed booking | 12+ | <5 | Eli |
| Human escalation rate | 0% (no handoff) | <15% | All |
| NPS response rate | 0% (not collected) | >40% | Feedback |
| Inactive customer reactivation | 0% | >15% | Retention |
| Plan upsell conversion | 0% | >5% | Sales |
| Campaign reply rate | N/A | >20% | Campaign |
| Revenue per conversation | Unknown | Tracked | Analytics |

---

## 5. Tool System Evolution

### 5.1 Tool Registry Architecture

[AUTO-DECISION] Should tools be statically assigned or dynamically discovered? -> Static assignment with dynamic registration (reason: at 5 agents and ~25 tools, a full service registry adds complexity without benefit; static assignment in agent config files is sufficient, but the registry pattern allows future plugin-based extension)

```typescript
// /src/lib/ai/tools/tool-registry.ts

interface ToolDefinition {
  id: string;
  name: string;
  description: string;           // Used by LLM for tool selection
  parameters: JSONSchema;
  handler: ToolHandler;
  scope: 'core' | 'agent-specific';
  allowedAgents: AgentId[];      // Which agents can use this tool
  requiresAuth: boolean;
  rateLimit?: { max: number; windowMs: number };
}

class ToolRegistry {
  private tools: Map<string, ToolDefinition> = new Map();

  register(tool: ToolDefinition): void;
  getToolsForAgent(agentId: AgentId): ToolDefinition[];
  executeTool(toolId: string, params: unknown, ctx: AgentContext): Promise<ToolResult>;
}
```

### 5.2 Core Tools (Shared by All Agents)

These tools are available to every agent:

| Tool | Description | Why Shared |
|------|-------------|-----------|
| `getCustomerProfile` | Load customer data by phone number | All agents need customer context |
| `updateCustomerProfile` | Update customer preferences/notes | Any agent may learn new preferences |
| `getConversationHistory` | Load recent conversation messages | All agents need conversation context |
| `sendMessage` | Send WhatsApp message (via antiban layer) | All agents send messages |
| `humanHandoff` | Escalate to human operator | All agents may need to escalate |
| `logAnalyticsEvent` | Track an event for analytics | All agents generate analytics |
| `getBusinessConfig` | Load business hours, services, staff | All agents need business context |

### 5.3 Agent-Specific Tools

| Agent | Exclusive Tools | Count |
|-------|----------------|-------|
| **Eli** | checkAvailability, createAppointment, cancelAppointment, rescheduleAppointment, getServiceCatalog | 5 |
| **Sales** | getPlans, calculateSavings, createSubscription, applyDiscount, getCustomerSpendHistory | 5 |
| **Retention** | getInactiveCustomers, getCustomerHistory, createRetentionOffer, trackRetentionOutcome | 4 |
| **Campaign** | getSegment, getApprovedTemplates, personalizeTemplate, scheduleMessage, trackCampaignMetrics, generateVariation | 6 |
| **Feedback** | sendNPSSurvey, recordFeedback, requestGoogleReview, escalateComplaint, getAppointmentDetails | 5 |

### 5.4 Adding New Integrations Without Touching Agent Code

The tool registry pattern allows new integrations to be added as standalone tool modules:

```typescript
// /src/lib/ai/tools/integrations/google-calendar.ts

export const googleCalendarTool: ToolDefinition = {
  id: 'syncGoogleCalendar',
  name: 'Sync Google Calendar',
  description: 'Sync appointments with staff Google Calendar',
  parameters: { /* ... */ },
  handler: async (params, ctx) => { /* ... */ },
  scope: 'core',
  allowedAgents: ['eli'],  // Only Eli needs calendar sync
  requiresAuth: true,
};

// Registration in /src/lib/ai/tools/index.ts
registry.register(googleCalendarTool);
```

**Key principle:** A new tool is a new file. No existing agent code changes. The tool declares which agents can use it. The registry handles discovery and injection.

---

## 6. Memory and Context System

### 6.1 Three-Tier Memory Architecture

```
+================================================================+
|                    MEMORY ARCHITECTURE                          |
+================================================================+
|                                                                 |
|  TIER 1: SHORT-TERM (Conversation Context)                     |
|  +---------------------------------------------------------+   |
|  | Storage: Redis (TTL: 30 minutes)                         |   |
|  | Scope: Current conversation thread                       |   |
|  | Content:                                                  |   |
|  |   - Last 20 messages (user + agent)                      |   |
|  |   - Current intent/topic                                 |   |
|  |   - Active agent ID                                      |   |
|  |   - Pending actions (e.g., awaiting confirmation)        |   |
|  |   - Handoff context (if transferred between agents)      |   |
|  | Access: Every message processing cycle                    |   |
|  | Cost: ~0 (Redis memory, negligible)                      |   |
|  +---------------------------------------------------------+   |
|                                                                 |
|  TIER 2: MEDIUM-TERM (Customer Profile)                        |
|  +---------------------------------------------------------+   |
|  | Storage: PostgreSQL (Prisma) + Redis cache (TTL: 1 hour) |   |
|  | Scope: Per-customer, cross-conversation                  |   |
|  | Content:                                                  |   |
|  |   - Last 5 appointments (date, service, barber, outcome) |   |
|  |   - Preferred barber                                     |   |
|  |   - Usual service(s)                                     |   |
|  |   - Preferred time slots                                 |   |
|  |   - Communication preferences (formal/informal)          |   |
|  |   - Active plan/subscription                             |   |
|  |   - NPS history                                          |   |
|  |   - Complaints/issues                                    |   |
|  |   - Last interaction date                                |   |
|  |   - Customer segment (VIP, regular, at-risk, churned)    |   |
|  | Access: On conversation start (cached in Redis)          |   |
|  | Cost: ~1 Prisma query per new conversation               |   |
|  +---------------------------------------------------------+   |
|                                                                 |
|  TIER 3: LONG-TERM (Business Intelligence)                     |
|  +---------------------------------------------------------+   |
|  | Storage: PostgreSQL (aggregated views/materialized)      |   |
|  | Scope: Per-organization, cross-customer                  |   |
|  | Content:                                                  |   |
|  |   - Peak hours heatmap (by day of week)                  |   |
|  |   - Most popular services (by month)                     |   |
|  |   - Average booking lead time                            |   |
|  |   - Barber utilization rates                             |   |
|  |   - No-show rate by customer segment                     |   |
|  |   - Campaign effectiveness by type                       |   |
|  |   - Seasonal patterns                                    |   |
|  |   - Churn predictors (features that correlate with churn)|   |
|  |   - Revenue per customer segment                         |   |
|  | Access: Nightly aggregation job (BullMQ cron)            |   |
|  | Cost: 1 aggregation job per night per org                |   |
|  +---------------------------------------------------------+   |
+================================================================+
```

### 6.2 Prisma Schema Extensions

```prisma
// Additions to existing schema

model CustomerMemory {
  id              String   @id @default(cuid())
  customerId      String
  customer        Customer @relation(fields: [customerId], references: [id])
  orgId           String

  // Preferences (learned from conversations)
  preferredBarber    String?
  usualServices      String[]    // Array of service IDs
  preferredTimeSlot  String?     // "morning" | "afternoon" | "evening"
  communicationStyle String?     // "formal" | "informal" | "brief"

  // Engagement
  lastInteractionAt  DateTime?
  totalConversations Int        @default(0)
  totalBookings      Int        @default(0)
  noShowCount        Int        @default(0)
  averageNPS         Float?
  customerSegment    CustomerSegment @default(NEW)

  // Revenue
  lifetimeValue      Float      @default(0)
  activePlanId       String?

  createdAt          DateTime   @default(now())
  updatedAt          DateTime   @updatedAt

  @@unique([customerId, orgId])
  @@index([orgId, customerSegment])
  @@index([orgId, lastInteractionAt])
}

enum CustomerSegment {
  NEW           // First interaction
  ACTIVE        // Visited in last 30 days
  REGULAR       // 3+ visits in last 90 days
  VIP           // High LTV or plan subscriber
  AT_RISK       // 30-60 days inactive
  CHURNED       // 60+ days inactive
  LOST          // 90+ days inactive, no response to reactivation
}

model AgentConversation {
  id              String   @id @default(cuid())
  conversationId  String
  orgId           String
  customerId      String
  agentId         String   // 'eli' | 'sales' | 'retention' | 'campaign' | 'feedback'

  startedAt       DateTime @default(now())
  endedAt         DateTime?
  outcome         ConversationOutcome?
  handoffFrom     String?  // Agent that handed off to this one
  handoffTo       String?  // Agent this one handed off to

  messageCount    Int      @default(0)
  toolCallCount   Int      @default(0)
  llmTokensUsed   Int      @default(0)

  @@index([orgId, agentId, startedAt])
  @@index([customerId])
}

enum ConversationOutcome {
  BOOKING_COMPLETED
  BOOKING_FAILED
  SALE_COMPLETED
  SALE_LOST
  RETENTION_WON
  RETENTION_LOST
  FEEDBACK_COLLECTED
  CAMPAIGN_REPLIED
  HUMAN_ESCALATED
  ABANDONED
}

model CampaignExecution {
  id              String   @id @default(cuid())
  orgId           String
  name            String
  type            CampaignType
  segmentCriteria Json
  templateId      String

  status          CampaignStatus @default(DRAFT)
  scheduledAt     DateTime?
  startedAt       DateTime?
  completedAt     DateTime?

  totalTargets    Int      @default(0)
  messagesSent    Int      @default(0)
  messagesDelivered Int    @default(0)
  replies         Int      @default(0)
  conversions     Int      @default(0)
  optOuts         Int      @default(0)

  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  @@index([orgId, status])
}

enum CampaignType {
  REACTIVATION        // Inactive customers
  BIRTHDAY            // Birthday offers
  SEASONAL            // Holiday/seasonal promos
  NEW_SERVICE         // New service announcements
  LOYALTY_REWARD      // Loyalty program
  CUSTOM              // Admin-defined
}

enum CampaignStatus {
  DRAFT
  SCHEDULED
  RUNNING
  PAUSED
  COMPLETED
  CANCELLED
}
```

### 6.3 Redis Key Structure

```
# Conversation context (short-term memory)
stm:{orgId}:{phone}              -> JSON: { messages[], intent, agentId, pending }
stm:{orgId}:{phone}:lock         -> JSON: { agentId, lockedAt }

# Customer profile cache (medium-term, hot cache)
mtm:{orgId}:{customerId}         -> JSON: { CustomerMemory }
mtm:{orgId}:{customerId}:history -> JSON: { last5Appointments[] }

# Agent-specific state
agent:{orgId}:{phone}:sales      -> JSON: { quotedPlans[], objections[] }
agent:{orgId}:{phone}:feedback   -> JSON: { surveyState, currentScore }

# Rate limiting (antiban)
rl:{orgId}:minute                -> Counter (TTL: 60s)
rl:{orgId}:hour                  -> Counter (TTL: 3600s)
rl:{orgId}:day                   -> Counter (TTL: 86400s)
rl:{orgId}:{phone}:last          -> Timestamp of last message to this contact

# Business intelligence cache
bi:{orgId}:peak_hours            -> JSON: { heatmap } (TTL: 24h)
bi:{orgId}:popular_services      -> JSON: { ranked[] } (TTL: 24h)

# Campaign state
campaign:{campaignId}:progress   -> JSON: { sent, pending, failed }
campaign:{campaignId}:paused     -> Boolean flag
```

### 6.4 Context Loading Pipeline

When a new message arrives, the memory system loads context in a specific order:

```
1. Redis: Load short-term memory (stm:*)           ~1ms
2. Redis: Check conversation lock                    ~1ms
3. Redis: Load customer profile cache (mtm:*)        ~1ms
   3a. If cache MISS: Prisma query + cache           ~15ms (rare)
4. Agent Router: Classify intent                     ~2ms (rules) or ~200ms (LLM)
5. Agent: Build prompt with full context             ~5ms
6. LLM: Generate response                           ~800-2000ms
7. Redis: Update short-term memory                   ~1ms
8. Redis: Update customer profile if learned          ~1ms
9. Prisma: Persist conversation (async, non-blocking) ~10ms
```

**Total latency budget:** <3s (p95) from message received to response queued.

---

## 7. Campaign Engine Architecture

### 7.1 Campaign Lifecycle

```
  [DEFINE]          [SEGMENT]         [COMPOSE]         [SCHEDULE]
     |                  |                  |                  |
     v                  v                  v                  v
  Admin sets       Query customers    Select template    Set delivery
  campaign         by criteria        + personalize      window
  parameters       (segment)         + variations        (date/time)
     |                  |                  |                  |
     +--------+---------+--------+--------+--------+---------+
              |                           |
              v                           v
         [APPROVE]                   [DISPATCH]
              |                           |
              v                           v
         Admin review              BullMQ processes
         + compliance              messages with:
         check                     - Antiban rate limits
              |                    - Gaussian jitter
              v                    - Content variation
         [MONITOR]                 - Typing simulation
              |                           |
              v                           v
         Real-time                  [ANALYZE]
         dashboard:                      |
         - Sent/delivered               v
         - Reply rate               Post-campaign
         - Opt-outs                 report:
         - Risk score               - Conversion rate
                                    - Revenue attributed
                                    - Reply rate
                                    - Best template variant
```

### 7.2 Segmentation Engine

```typescript
// /src/lib/ai/campaign/segmentation.ts

interface SegmentCriteria {
  // Time-based
  lastVisitDaysAgo?: { min?: number; max?: number };
  registeredDaysAgo?: { min?: number; max?: number };

  // Behavior-based
  totalVisits?: { min?: number; max?: number };
  noShowRate?: { max: number };
  averageNPS?: { min?: number };
  segment?: CustomerSegment[];

  // Product-based
  hasActivePlan?: boolean;
  usedServices?: string[];       // Service IDs
  preferredBarber?: string;      // Barber ID

  // Engagement-based
  respondedToLastCampaign?: boolean;
  optedOut?: false;              // MUST always exclude opt-outs

  // Custom
  customField?: { field: string; value: unknown };
}

// Example: "Customers who visited 2+ times but haven't been back in 30+ days"
const reactivationSegment: SegmentCriteria = {
  lastVisitDaysAgo: { min: 30 },
  totalVisits: { min: 2 },
  segment: ['AT_RISK', 'CHURNED'],
  optedOut: false,
};
```

### 7.3 Template System with Content Variation

```typescript
// /src/lib/ai/campaign/templates.ts

interface CampaignTemplate {
  id: string;
  name: string;
  type: CampaignType;
  orgId: string;

  // Base template with placeholders
  body: string;

  // Variation pools for antiban
  greetings: string[];          // ["Oi", "Ola", "E ai", "Bom dia"]
  closings: string[];           // ["Abraco!", "Ate mais!", "Conte conosco!"]
  bodyVariations: string[];     // Full body rewrites (min 5)

  // Personalization fields
  personalizationFields: string[];  // ["name", "lastService", "preferredBarber"]

  // Compliance
  includesOptOut: boolean;          // MUST be true
  optOutText: string;               // "Responda SAIR para nao receber mais"
  approvedAt?: Date;
  approvedBy?: string;
}

// Example template with variations:
const reactivationTemplate: CampaignTemplate = {
  id: 'reactivation-v1',
  name: 'Reativacao 30 dias',
  type: 'REACTIVATION',
  orgId: 'org_123',
  body: '{greeting} {name}! Faz um tempinho que voce nao aparece na {businessName}. {bodyVariation} {closing}\n\n{optOut}',
  greetings: ['Oi', 'Ola', 'E ai', 'Fala'],
  closings: ['Abraco!', 'Ate mais!', 'Conte conosco!', 'Estamos te esperando!'],
  bodyVariations: [
    'O {barber} perguntou de voce! Que tal agendar essa semana?',
    'Sua vaga favorita ({timeSlot}) esta disponivel. Bora agendar?',
    'Temos novidades! Quer saber o que mudou por aqui?',
    'Sentimos sua falta! Temos horarios abertos essa semana.',
    'Ja faz {daysSince} dias! O {barber} ta com a agenda aberta.',
  ],
  personalizationFields: ['name', 'barber', 'timeSlot', 'daysSince', 'businessName'],
  includesOptOut: true,
  optOutText: 'Responda SAIR para nao receber mais mensagens.',
};
```

### 7.4 BullMQ Campaign Queue Architecture

```typescript
// /src/lib/ai/campaign/campaign-dispatcher.ts

// One queue per campaign type (isolation + independent rate limiting)
const campaignQueues = {
  reactivation: new Queue('campaign:reactivation', { connection: redis }),
  birthday: new Queue('campaign:birthday', { connection: redis }),
  seasonal: new Queue('campaign:seasonal', { connection: redis }),
  custom: new Queue('campaign:custom', { connection: redis }),
};

// Worker with rate limiting built in
const worker = new Worker('campaign:reactivation', async (job) => {
  const { customerId, templateId, orgId, variationIndex } = job.data;

  // 1. Load customer profile
  const customer = await getCustomerProfile(customerId);

  // 2. Personalize message with variation
  const message = await personalizeTemplate(templateId, customer, variationIndex);

  // 3. Check antiban limits before sending
  const canSend = await antibanCheck(orgId, customer.phone);
  if (!canSend) {
    // Re-queue with delay
    await job.moveToDelayed(Date.now() + 300000); // 5 min delay
    return;
  }

  // 4. Send via antiban middleware
  await sendWithAntiban(orgId, customer.phone, message);

  // 5. Update campaign metrics
  await updateCampaignProgress(job.data.campaignId, 'sent');

}, {
  concurrency: 1,          // One message at a time per org
  limiter: {
    max: 3,                // Max 3 messages per minute
    duration: 60000,
  },
});
```

### 7.5 Automated Campaign Triggers

```typescript
// /src/lib/ai/campaign/automated-triggers.ts (BullMQ repeatable jobs)

const automatedCampaigns = [
  {
    name: 'birthday-greetings',
    cron: '0 9 * * *',              // Daily at 9am
    handler: async () => {
      const birthdays = await getBirthdaysToday();
      for (const customer of birthdays) {
        await campaignQueues.birthday.add('send', {
          customerId: customer.id,
          templateId: 'birthday-v1',
          campaignId: `auto-birthday-${today()}`,
        });
      }
    },
  },
  {
    name: 'post-service-feedback',
    cron: '*/30 * * * *',           // Every 30 minutes
    handler: async () => {
      const recentAppointments = await getCompletedAppointments({
        completedAgo: { min: 2, max: 4 }, // 2-4 hours ago
        feedbackCollected: false,
      });
      for (const appt of recentAppointments) {
        await feedbackQueue.add('nps', {
          customerId: appt.customerId,
          appointmentId: appt.id,
        });
      }
    },
  },
  {
    name: 'reactivation-check',
    cron: '0 10 * * 1',             // Every Monday at 10am
    handler: async () => {
      const inactiveCustomers = await getInactiveCustomers({ daysSinceLastVisit: 30 });
      // Batch into campaign
    },
  },
  {
    name: 'no-show-followup',
    cron: '0 10 * * *',             // Daily at 10am
    handler: async () => {
      const noShows = await getNoShowsYesterday();
      for (const noShow of noShows) {
        await retentionQueue.add('no-show', {
          customerId: noShow.customerId,
          appointmentId: noShow.appointmentId,
        });
      }
    },
  },
];
```

---

## 8. Antiban Compliance Layer

### 8.1 Antiban as Infrastructure, Not Agent Responsibility

**Critical design principle:** Individual agents do NOT manage antiban. They simply call `sendMessage()`. The antiban middleware intercepts all outbound messages and applies compliance rules transparently.

```
Agent --> sendMessage() --> Antiban Middleware --> BullMQ Queue --> Evolution API
                                |
                           +----+----+
                           |         |
                      Rate Check  Health Check
                           |         |
                      +----+----+  +-+-------+
                      |Allow    |  |Risk >60?|
                      |Queue    |  |PAUSE    |
                      |w/ delay |  |all sends|
                      +---------+  +---------+
```

### 8.2 Message Priority System

Not all messages are equal. The antiban system prioritizes:

| Priority | Message Type | Max Delay | Example |
|----------|-------------|-----------|---------|
| P0 (Critical) | Reply to customer message | 3-8s + typing | Customer asked a question |
| P1 (High) | Appointment confirmation | 10-30s | Booking just made |
| P2 (Medium) | Scheduled reminder | 1-5 min window | 2h before appointment |
| P3 (Low) | Proactive outreach | 90-180s between | Retention, follow-up |
| P4 (Batch) | Campaign messages | 3-5 min between | Bulk campaigns |

**Rationale:** Replies to customer messages are essentially zero-risk (customer initiated the conversation). Campaign blasts are highest risk. The antiban system should NEVER delay a reply to a customer who is actively chatting.

### 8.3 Per-Org Rate Limits (Multi-Tenant)

```typescript
// /src/lib/ai/antiban/rate-limiter.ts

interface OrgRateLimits {
  orgId: string;

  // Per-minute (across all message types)
  maxPerMinute: number;         // Default: 3 (conservative)

  // Per-hour
  maxPerHour: number;           // Default: 40

  // Per-day
  maxPerDay: number;            // Default: 300

  // Per-contact
  maxPerContactPerDay: number;  // Default: 5
  maxWithoutReply: number;      // Default: 2 (stop if no reply after 2 proactive msgs)

  // Dynamic adjustment based on number age
  numberAgeDays: number;        // How old is this WhatsApp number
  warmupMultiplier: number;     // 0.2 for new numbers, 1.0 for mature

  // Schedule
  activeHoursStart: number;     // 8
  activeHoursEnd: number;       // 20
  weekendFactor: number;        // 0.5
  sundayFactor: number;         // 0.25
}
```

### 8.4 Integration with Existing Antiban System

The Tikso project already has a robust antiban system (83 tests, ~100% capacity per ATLAS-2). The multi-agent architecture extends it, not replaces it:

**Existing (keep as-is):**
- Gaussian jitter
- Typing simulation (presence: "composing")
- Per-destination rate limiting
- 429 backoff handling
- Presence management
- Lunch time reduction
- Opt-out per org

**New additions for multi-agent:**
- Message priority queue (P0-P4)
- Per-agent rate budget allocation
- Campaign-specific rate limits (stricter than conversational)
- Cross-agent rate coordination (total org rate, not per-agent)

---

## 9. Scalability -- Multi-Tenant at Scale

### 9.1 Data Isolation Strategy

[AUTO-DECISION] Should multi-tenant isolation use separate databases, schemas, or row-level? -> Row-level security with orgId discriminator (reason: at the target scale of 1000 businesses, separate DBs would be operationally expensive and Prisma does not natively support schema-per-tenant; row-level with orgId is the standard pattern for SaaS at this scale)

```
+------------------------------------------------------------------+
|                    MULTI-TENANT ISOLATION                          |
+------------------------------------------------------------------+
|                                                                    |
|  DATABASE: Single PostgreSQL instance                             |
|  +------------------------------------------------------------+  |
|  |  Every table has: orgId String (indexed, required)          |  |
|  |  Every query has: WHERE orgId = {currentOrg}                |  |
|  |  Prisma middleware enforces orgId injection                  |  |
|  +------------------------------------------------------------+  |
|                                                                    |
|  REDIS: Namespace isolation via key prefix                        |
|  +------------------------------------------------------------+  |
|  |  All keys prefixed with orgId:                              |  |
|  |  stm:{orgId}:{phone}                                       |  |
|  |  mtm:{orgId}:{customerId}                                  |  |
|  |  rl:{orgId}:minute                                          |  |
|  +------------------------------------------------------------+  |
|                                                                    |
|  BULLMQ: Per-org queue isolation                                  |
|  +------------------------------------------------------------+  |
|  |  Queue naming: {queueType}:{orgId}                          |  |
|  |  Example: campaign:org_123:reactivation                     |  |
|  |  Allows per-org rate limiting and priority                  |  |
|  +------------------------------------------------------------+  |
|                                                                    |
|  EVOLUTION API: Per-org instance                                  |
|  +------------------------------------------------------------+  |
|  |  Each org has its own Evolution API instance                |  |
|  |  Instance name = orgId                                      |  |
|  |  Already supports this pattern                              |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### 9.2 Prisma Multi-Tenant Middleware

```typescript
// /src/lib/prisma/multi-tenant-middleware.ts

import { Prisma } from '@prisma/client';

export function multiTenantMiddleware(orgId: string): Prisma.Middleware {
  return async (params, next) => {
    // Inject orgId into all queries
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = { ...params.args.where, orgId };
    }
    if (params.action === 'create') {
      params.args.data = { ...params.args.data, orgId };
    }
    if (params.action === 'update' || params.action === 'delete') {
      params.args.where = { ...params.args.where, orgId };
    }
    return next(params);
  };
}
```

### 9.3 Scaling to 1000 Businesses

**Bottleneck analysis:**

| Component | Current Capacity | At 1000 orgs | Solution |
|-----------|-----------------|--------------|----------|
| **PostgreSQL** | Single instance | ~10k queries/sec needed | Connection pooling (PgBouncer), read replicas for analytics |
| **Redis** | Single instance | ~50k ops/sec needed | Redis Cluster (3 nodes) at ~500 orgs |
| **BullMQ Workers** | Single process | ~1000 concurrent jobs | Horizontal scaling: 1 worker per 100 orgs |
| **LLM API** | Rate limited | ~5000 calls/hour | Claude API supports this; batch classification for campaigns |
| **Evolution API** | 1 instance/org | 1000 instances | Evolution API supports multiple instances; resource: ~50MB RAM/instance |
| **Node.js** | Single process | CPU bound at ~200 orgs | PM2 cluster mode (4-8 workers) |

**Scaling milestones:**

| Orgs | Infrastructure Changes Needed |
|------|------------------------------|
| 1-50 | Current setup (single Vultr VPS) |
| 50-200 | Add PgBouncer, Redis memory upgrade, PM2 cluster (4 workers) |
| 200-500 | Dedicated DB server, Redis Cluster, multiple worker VPS |
| 500-1000 | Load balancer, read replicas, dedicated Evolution API servers |
| 1000+ | Kubernetes or managed infra (consider cloud migration) |

### 9.4 Queue Management Architecture

```
+--------------------------------------------------------------+
|                    BULLMQ QUEUE TOPOLOGY                      |
+--------------------------------------------------------------+
|                                                                |
|  INBOUND (per-org)                                            |
|  +----------------------------------------------------------+ |
|  | inbound:{orgId}                                           | |
|  | - All incoming WhatsApp messages                          | |
|  | - Concurrency: 1 per conversation (keyed by phone)        | |
|  | - Priority: FIFO                                          | |
|  +----------------------------------------------------------+ |
|                                                                |
|  OUTBOUND (per-org, prioritized)                              |
|  +----------------------------------------------------------+ |
|  | outbound:{orgId}:p0  (replies)     -- concurrency: 3     | |
|  | outbound:{orgId}:p1  (confirms)    -- concurrency: 2     | |
|  | outbound:{orgId}:p2  (reminders)   -- concurrency: 1     | |
|  | outbound:{orgId}:p3  (outreach)    -- concurrency: 1     | |
|  | outbound:{orgId}:p4  (campaigns)   -- concurrency: 1     | |
|  +----------------------------------------------------------+ |
|                                                                |
|  CAMPAIGN (global + per-org)                                  |
|  +----------------------------------------------------------+ |
|  | campaign:{orgId}:{campaignId}                             | |
|  | - One queue per active campaign                           | |
|  | - Rate limited: 3/min, 40/hour                            | |
|  | - Pausable independently                                  | |
|  +----------------------------------------------------------+ |
|                                                                |
|  CRON (global)                                                |
|  +----------------------------------------------------------+ |
|  | cron:feedback     -- post-service NPS (every 30 min)      | |
|  | cron:reactivation -- weekly reactivation scan             | |
|  | cron:birthday     -- daily birthday check                 | |
|  | cron:analytics    -- nightly aggregation                  | |
|  | cron:noshow       -- daily no-show followup               | |
|  +----------------------------------------------------------+ |
+--------------------------------------------------------------+
```

---

## 10. Cost Optimization

### 10.1 LLM Cost Analysis

Claude API is the most expensive component. Here is the cost breakdown per interaction type:

| Interaction | Model | Input Tokens | Output Tokens | Cost/Call | Volume/Day | Daily Cost |
|-------------|-------|-------------|---------------|-----------|------------|------------|
| **Agent Router (LLM tier)** | Haiku 3.5 | ~200 | ~10 | $0.00005 | ~200 (20% of 1000 msgs) | $0.01 |
| **Eli conversation** | Sonnet 3.5 | ~1500 | ~200 | $0.0012 | ~500 | $0.60 |
| **Sales conversation** | Sonnet 3.5 | ~2000 | ~300 | $0.0018 | ~50 | $0.09 |
| **Retention message** | Sonnet 3.5 | ~1500 | ~200 | $0.0012 | ~30 | $0.04 |
| **Campaign personalization** | Haiku 3.5 | ~300 | ~100 | $0.0001 | ~200 | $0.02 |
| **Feedback processing** | Haiku 3.5 | ~500 | ~100 | $0.00015 | ~100 | $0.015 |
| **Total per org** | | | | | | **~$0.78/day** |
| **Total at 100 orgs** | | | | | | **~$78/day** |
| **Total at 1000 orgs** | | | | | | **~$780/day** |

### 10.2 Cost Optimization Strategies

**Strategy 1: Tiered Model Selection**

Not every interaction needs the most powerful model:

| Task | Model | Why |
|------|-------|-----|
| Intent classification | Haiku | Simple classification, 10x cheaper |
| Campaign personalization | Haiku | Template filling, no reasoning needed |
| Feedback processing | Haiku | Sentiment analysis + NPS, simple |
| Scheduling (Eli) | Sonnet | Needs tool use + conversation management |
| Sales conversations | Sonnet | Needs persuasion + objection handling |
| Complex retention | Sonnet | Needs empathy + personalization |

**Strategy 2: Response Caching**

Many responses are similar across customers. Cache common patterns:

```typescript
// Cache FAQ responses (Redis, TTL: 24h)
const cacheKey = `faq:${orgId}:${normalizedQuestion}`;
const cached = await redis.get(cacheKey);
if (cached) return cached; // Skip LLM call entirely
```

**Estimated savings:** 20-30% reduction in LLM calls for FAQ-heavy orgs.

**Strategy 3: Prompt Optimization**

Shorter prompts = fewer tokens = lower cost:

- Use structured context injection (JSON, not prose)
- Load only relevant customer memory (not full history)
- Limit conversation history to last 10 messages (not 20)

**Strategy 4: Batch Processing for Campaigns**

Instead of one LLM call per campaign message, batch personalization:

```typescript
// Instead of: 200 individual LLM calls
// Do: 1 LLM call with batch of 20 contacts, generate 20 messages
// Repeat 10 times = 10 LLM calls instead of 200
```

**Estimated savings:** 90% reduction in campaign LLM costs.

### 10.3 Cost per Customer per Month

| Tier | Orgs | LLM Cost/Org/Month | Infra Cost/Org/Month | Total/Org/Month |
|------|------|-------------------|---------------------|-----------------|
| Starter (1-50 orgs) | 50 | ~$23 | ~$10 | ~$33 |
| Growth (50-200 orgs) | 200 | ~$20 | ~$5 | ~$25 |
| Scale (200-1000 orgs) | 1000 | ~$18 | ~$3 | ~$21 |

**Note:** These are marginal costs. The fixed infrastructure cost (VPS, DB, Redis) is amortized across orgs. At 1000 orgs, infrastructure cost per org drops to ~$3/month.

---

## 11. Roadmap de Implementacao

### Phase 0: Foundation (Week 1-2) -- "Fix What's Broken"

Priority: Fix the critical bugs identified in the Eli conversation analysis before building anything new.

| Task | Description | Effort | Impact |
|------|-------------|--------|--------|
| Fix service ID validation | Validate all service IDs on startup; add health check | 2 days | CRITICAL -- eliminates booking failures |
| Fix slot duration filtering | Filter available slots by service duration | 2 days | CRITICAL -- eliminates ghost time slots |
| Add error sanitization | Replace all technical error messages with user-friendly ones | 1 day | HIGH -- stops exposing internals |
| Add human handoff | After 2 failures, offer to connect to human | 3 days | HIGH -- recovers 55-65% of abandons |

**Deliverable:** Eli works reliably for 100% of scheduling scenarios.

### Phase 1: Agent Router + Memory (Week 3-5)

| Task | Description | Effort |
|------|-------------|--------|
| Implement AgentRouter | Tier 0 (lock) + Tier 1 (rules) + Tier 3 (default) | 1 week |
| Implement CustomerMemory model | Prisma schema + Redis cache layer | 3 days |
| Implement context loading pipeline | Load customer profile on conversation start | 2 days |
| Enhance Eli with customer intelligence | Use memory to personalize greetings, offer "the usual" | 3 days |
| Add conversation lock (Redis) | Single-owner guarantee | 2 days |

**Deliverable:** Eli is smarter. Returns customer data. Router exists but only routes to Eli.

### Phase 2: Sales + Retention Agents (Week 6-9)

| Task | Description | Effort |
|------|-------------|--------|
| Implement Sales Agent | System prompt, tools, subscription flow | 1 week |
| Implement Retention Agent | System prompt, tools, reactivation flow | 1 week |
| Implement agent handoff protocol | Lock transfer, context passing, transition messages | 3 days |
| Add LLM-based routing (Tier 2) | Haiku classifier for ambiguous messages | 2 days |
| Add AgentConversation tracking | Track which agent handled what + outcomes | 2 days |

**Deliverable:** Three agents live. Customers can be transferred between them.

### Phase 3: Campaign Engine (Week 10-13)

| Task | Description | Effort |
|------|-------------|--------|
| Implement Campaign model | Prisma schema, template system, variation engine | 1 week |
| Implement segmentation engine | Customer query by criteria | 3 days |
| Implement Campaign Agent | System prompt, tools, dispatch flow | 1 week |
| Integrate with antiban | Priority queue, per-campaign rate limits | 3 days |
| Build automated triggers | Birthday, reactivation, no-show cron jobs | 3 days |
| Admin campaign UI (basic) | Create/schedule/monitor campaigns from dashboard | 1 week |

**Deliverable:** Proactive messaging live. Automated campaigns running.

### Phase 4: Feedback Agent + Analytics (Week 14-17)

| Task | Description | Effort |
|------|-------------|--------|
| Implement Feedback Agent | System prompt, NPS flow, review request | 1 week |
| Implement post-service trigger | Automatic NPS 2h after appointment | 2 days |
| Build analytics aggregation | Nightly cron for business intelligence | 1 week |
| Build flywheel dashboard | KPI dashboard with agent metrics | 1 week |
| Implement customer segmentation automation | Auto-classify: NEW/ACTIVE/VIP/AT_RISK/CHURNED | 3 days |

**Deliverable:** Full 5-agent platform. Analytics dashboard. Flywheel operational.

### Phase 5: Optimization + Scale (Week 18-24)

| Task | Description | Effort |
|------|-------------|--------|
| LLM cost optimization | Response caching, prompt compression, batch processing | 2 weeks |
| Multi-tenant hardening | PgBouncer, Redis memory optimization, load testing | 1 week |
| Campaign A/B testing | Test template variants, track which performs best | 1 week |
| WhatsApp Cloud API integration | Official API for critical messages (reminders) | 2 weeks |
| Advanced flywheel features | Churn prediction, automated upsell triggers | 2 weeks |

**Deliverable:** Production-hardened, cost-optimized, scalable platform.

---

## 12. Trade-off Analysis

### 12.1 Single Agent vs. Multi-Agent

| Dimension | Single Agent (Current) | Multi-Agent (Proposed) |
|-----------|----------------------|----------------------|
| **Complexity** | Low -- one prompt, one codebase | Medium -- 5 agents, router, handoff protocol |
| **Prompt Quality** | Degrading -- one prompt tries to do everything | High -- each agent is a specialist with focused prompt |
| **Maintenance** | Low effort but hard to debug | Modular -- change one agent without affecting others |
| **Cost** | Lower (fewer LLM calls) | ~20% higher (router + specialized prompts) |
| **Capability** | Limited to scheduling | Full customer lifecycle: schedule, sell, retain, campaign, feedback |
| **Revenue Potential** | Scheduling only | Multiple revenue streams |

**Verdict:** Multi-agent is the correct choice. The 20% cost increase is dwarfed by the revenue potential from sales, retention, and campaigns.

### 12.2 Rules-Based vs. LLM-Based Routing

| Dimension | Rules Only | LLM Only | Hybrid (Chosen) |
|-----------|-----------|----------|-----------------|
| **Latency** | ~2ms | ~200-500ms | ~2ms (80%) / ~200ms (20%) |
| **Cost** | $0 | ~$5/day/org | ~$1/day/org |
| **Accuracy** | ~80% (misses nuanced intents) | ~95% (handles ambiguity) | ~93% (best of both) |
| **Maintainability** | Rules need manual updates | Prompt updates only | Rules + prompt updates |

**Verdict:** Hybrid is optimal. Rules handle the obvious 80% at zero cost and zero latency. LLM handles the nuanced 20%.

### 12.3 Redis vs. Database for Conversation Lock

| Dimension | Redis | PostgreSQL |
|-----------|-------|------------|
| **Latency** | <1ms | 5-15ms |
| **Atomicity** | SET NX (native) | Requires SELECT FOR UPDATE |
| **TTL** | Native TTL | Requires cron/trigger cleanup |
| **Failure Mode** | Lock auto-expires | Orphaned locks possible |
| **Persistence** | Volatile (acceptable for locks) | Durable (overkill for locks) |

**Verdict:** Redis is the clear winner for conversation locks.

### 12.4 Row-Level vs. Schema-Level Tenant Isolation

| Dimension | Row-Level (orgId) | Schema per Tenant |
|-----------|------------------|-------------------|
| **Setup Cost** | None (add column) | High (create schema per org) |
| **Query Safety** | Middleware required | Inherent isolation |
| **Migration** | Single migration | N migrations (one per tenant) |
| **Prisma Support** | Native | Not supported natively |
| **Performance at 1000 orgs** | Good (with indexes) | Better (smaller tables) |
| **Operational Overhead** | Low | Very high |

**Verdict:** Row-level with orgId discriminator. At 1000 orgs, operational simplicity outweighs the marginal performance benefit of schema isolation.

---

## 13. Security Considerations

### 13.1 Data Privacy

| Risk | Mitigation |
|------|-----------|
| Cross-tenant data leakage | Prisma middleware enforces orgId on every query; Redis keys namespaced by orgId |
| PII in LLM prompts | Customer names and phone numbers are sent to Claude API; Anthropic does not train on API data (confirmed policy) |
| Conversation data retention | Configurable per-org retention policy; default: 90 days for messages, 2 years for analytics |
| WhatsApp compliance | Opt-in required for proactive messages; opt-out honored immediately across all agents |

### 13.2 Agent Security

| Risk | Mitigation |
|------|-----------|
| Agent prompt injection | System prompts are server-side, never exposed to customer messages; customer input is always in `user` role |
| Tool abuse | Each tool validates orgId and permissions before execution; rate limits on destructive tools |
| Unauthorized handoff | Handoff matrix enforced: agents can only hand off to specific other agents |
| Financial transactions (Sales) | Subscription creation requires admin approval for custom plans; standard plans have guardrails |

### 13.3 Antiban Security

| Risk | Mitigation |
|------|-----------|
| WhatsApp account ban | Multi-layer antiban (rate limits + jitter + typing + content variation); health monitor with auto-pause |
| Mass campaign abuse | Admin approval required for campaigns >50 targets; rate limits enforced at infrastructure level |
| Spam complaints | Monitor block rate; auto-pause if block rate >2%; weekly review of campaigns with high opt-out |

### 13.4 Infrastructure Security

| Risk | Mitigation |
|------|-----------|
| Redis data exposure | Redis bound to localhost; no external access; AUTH required |
| API key leakage | Claude API key and Evolution API credentials in environment variables, never in code |
| DDoS via WhatsApp webhook | Rate limit on webhook endpoint; BullMQ absorbs bursts; backpressure if queue depth >1000 |

---

## Appendix A: File Structure (Proposed)

```
/home/tikso/tikso/src/lib/ai/
|-- agents/
|   |-- base-agent.ts              # Abstract base agent class
|   |-- eli-agent.ts               # Receptionist (existing, enhanced)
|   |-- sales-agent.ts             # Sales specialist
|   |-- retention-agent.ts         # Retention specialist
|   |-- campaign-agent.ts          # Campaign manager
|   |-- feedback-agent.ts          # Feedback collector
|   |-- agent-registry.ts          # Agent discovery + factory
|   |-- agent-types.ts             # Shared types/interfaces
|
|-- router/
|   |-- agent-router.ts            # Main router (Tier 0-3)
|   |-- routing-rules.ts           # Tier 1 rule definitions
|   |-- intent-classifier.ts       # Tier 2 LLM classifier
|   |-- conversation-lock.ts       # Redis lock management
|   |-- handoff-manager.ts         # Agent-to-agent handoff
|
|-- tools/
|   |-- tool-registry.ts           # Dynamic tool registry
|   |-- tool-types.ts              # Tool interfaces
|   |-- core/                      # Shared tools
|   |   |-- get-customer-profile.ts
|   |   |-- send-message.ts
|   |   |-- human-handoff.ts
|   |   |-- log-analytics.ts
|   |-- scheduling/                # Eli-specific tools
|   |   |-- check-availability.ts
|   |   |-- create-appointment.ts
|   |   |-- cancel-appointment.ts
|   |-- sales/                     # Sales-specific tools
|   |   |-- get-plans.ts
|   |   |-- create-subscription.ts
|   |-- retention/                 # Retention-specific tools
|   |   |-- get-inactive-customers.ts
|   |   |-- create-retention-offer.ts
|   |-- campaign/                  # Campaign-specific tools
|   |   |-- get-segment.ts
|   |   |-- personalize-template.ts
|   |-- feedback/                  # Feedback-specific tools
|   |   |-- send-nps-survey.ts
|   |   |-- record-feedback.ts
|
|-- memory/
|   |-- memory-manager.ts          # Orchestrates 3-tier memory
|   |-- short-term.ts              # Redis conversation context
|   |-- medium-term.ts             # Customer profile cache
|   |-- long-term.ts               # Business intelligence aggregation
|
|-- campaign/
|   |-- campaign-engine.ts         # Campaign lifecycle management
|   |-- segmentation.ts            # Customer segment queries
|   |-- template-engine.ts         # Template personalization + variation
|   |-- campaign-dispatcher.ts     # BullMQ dispatch + rate control
|   |-- automated-triggers.ts      # Cron-based campaign triggers
|
|-- analytics/
|   |-- flywheel-tracker.ts        # Flywheel phase tracking
|   |-- agent-metrics.ts           # Per-agent performance metrics
|   |-- aggregation-jobs.ts        # Nightly BI aggregation
|
|-- antiban/                       # Existing, extended
|   |-- (existing files)
|   |-- priority-queue.ts          # P0-P4 message prioritization (NEW)
|   |-- cross-agent-limiter.ts     # Org-level rate coordination (NEW)
```

## Appendix B: Agent Handoff Matrix

Which agent can hand off to which:

| From \ To | Eli | Sales | Retention | Campaign | Feedback | Human |
|-----------|-----|-------|-----------|----------|----------|-------|
| **Eli** | -- | YES | NO | NO | NO | YES |
| **Sales** | YES | -- | NO | NO | NO | YES |
| **Retention** | YES | YES | -- | NO | NO | YES |
| **Campaign** | YES | YES | YES | -- | NO | YES |
| **Feedback** | YES | NO | NO | NO | -- | YES |

**Rules:**
- Everyone can hand off to Eli (she is the receptionist, catch-all)
- Everyone can hand off to Human (universal escalation)
- Campaign can hand off to Retention (campaign reply from at-risk customer)
- Campaign can hand off to Sales (campaign reply with purchase intent)
- Retention can hand off to Sales (re-engaged customer wants to buy a plan)
- Feedback CANNOT hand off to Sales (collecting feedback should not feel like a sales pitch)

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| **Agent Router** | The component that decides which specialized agent handles a given message |
| **Conversation Lock** | A Redis-based mutex that ensures only one agent handles a conversation at a time |
| **Flywheel** | A self-reinforcing cycle where each interaction generates data that improves the next interaction |
| **Handoff** | The process of transferring a conversation from one agent to another with full context preservation |
| **STM (Short-Term Memory)** | Redis-based conversation context that lasts for the duration of a conversation (~30 min TTL) |
| **MTM (Medium-Term Memory)** | PostgreSQL + Redis cache of customer profile data (preferences, history, segment) |
| **LTM (Long-Term Memory)** | Aggregated business intelligence data (peak hours, popular services, churn predictors) |
| **Content Variation** | The practice of using multiple message variants to avoid WhatsApp spam detection |
| **Gaussian Jitter** | Randomized delay following a normal distribution to mimic human typing patterns |
| **Priority Queue** | BullMQ queue with P0-P4 priority levels for outbound message ordering |

---

-- Aria, arquitetando o futuro

*Documento gerado em 2026-02-25. Baseado na analise de 4 documentos de pesquisa, inteligencia competitiva da AwSales, e best practices atuais de mercado.*
