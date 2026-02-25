# Tikso CRM - Revenue Analytics System Design

**Author:** Dara (Data Engineer)
**Date:** 2026-02-25
**Status:** DRAFT - Pending Architecture Review
**Stack:** Next.js 16, Prisma 7.4, PostgreSQL, Redis, BullMQ

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Existing Schema Analysis](#2-existing-schema-analysis)
3. [Analytics Schema Design (Prisma)](#3-analytics-schema-design-prisma)
4. [Attribution Model](#4-attribution-model)
5. [Queries for Every Metric](#5-queries-for-every-metric)
6. [Dashboard Design](#6-dashboard-design)
7. [Caching Strategy (Redis)](#7-caching-strategy-redis)
8. [Aggregation Jobs (BullMQ)](#8-aggregation-jobs-bullmq)
9. [Smart Alerts](#9-smart-alerts)
10. [Competitive Benchmark](#10-competitive-benchmark)
11. [Implementation Roadmap](#11-implementation-roadmap)
12. [Migration Plan](#12-migration-plan)

---

## 1. Executive Summary

### The Problem

Business owners pay for Tikso but have no clear picture of how much revenue the AI generates. Without visible ROI, churn is inevitable. The owner needs to open one screen and immediately see: "The AI generated R$12,400 this month."

### The Solution

A revenue analytics system that:

- Attributes every real (R$) to its source: AI, human, or organic
- Tracks appointments, orders, pipeline value, and reactivations
- Pre-aggregates metrics daily/weekly/monthly for instant dashboards
- Sends WhatsApp alerts when milestones or problems are detected
- Shows comparisons (this month vs. last month, AI vs. human)

### Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Aggregation approach | Materialized aggregation tables | Real-time queries on millions of messages would be too slow; pre-compute daily |
| Attribution model | Last-touch with multi-touch visibility | Simple for the owner to understand; track all touches for future analysis |
| Storage for events | Append-only events table | Immutable audit trail; aggregations computed from events |
| Time bucketing | Daily granularity, rolled up to weekly/monthly | Daily is the smallest useful grain for business owners |
| Caching layer | Redis with TTL per metric type | Dashboard loads in <200ms; background jobs refresh every 5-15 minutes |

---

## 2. Existing Schema Analysis

### What Already Exists (Leverage These)

The current schema at 83 models already has strong foundations for analytics:

| Model | Analytics Value | Notes |
|-------|----------------|-------|
| `RevenueAttribution` | Revenue tracking with attribution | Already has contactId, conversationId, campaignId, sequenceId, flowId, attributionType |
| `AgentReplyEvent` | Response time tracking per agent | Has responseTimeMs, agentId, contactId |
| `AgentDecisionLog` | AI decision audit trail | Tracks every AI action with confidence score |
| `ConversationInsight` | Sentiment, intent, quality score | WATCH agent quality score already present |
| `Appointment` | Scheduling with status (NO_SHOW, COMPLETED) | Has assignedToId for attribution |
| `Order` / `OrderItem` | Revenue from products | Has status, total, conversationId |
| `PipelineCard` | Deal values | Has value (Decimal) and stageId |
| `ChurnScore` | Risk scoring | Already computed per contact |
| `LeadScore` | Lead temperature | Score 0-100, grade cold/warm/hot/on-fire |
| `JourneyTransition` | Contact lifecycle | State machine transitions with timestamps |
| `KeyEvent` / `KeyEventOccurrence` | Custom conversion tracking | Flexible event system per org |
| `Contact.journeyState` | Current lifecycle state | unknown, lead, engaged, customer, churned |
| `ChannelHealth` | Anti-ban metrics | sentToday, deliveredToday, deliveryRate |
| `Message` | All messages with direction and metadata | direction (INBOUND/OUTBOUND), metadata holds AI analysis |

### What Is Missing

1. **Daily aggregation tables** -- no pre-computed metrics exist
2. **AI vs. Human attribution on messages** -- Message.metadata may have AI info but there is no explicit `isAiGenerated` flag
3. **Appointment source tracking** -- no field to indicate if AI booked the appointment
4. **Session/period tracking** -- no way to correlate a set of messages into a "session"
5. **Dashboard-ready materialized views** -- all current queries would be real-time scans

---

## 3. Analytics Schema Design (Prisma)

### 3.1 New Enums

```prisma
enum MetricPeriod {
  DAILY
  WEEKLY
  MONTHLY
}

enum AttributionSource {
  AI_AGENT        // AI autonomously handled
  AI_ASSISTED     // AI helped, human closed
  HUMAN           // Fully human-handled
  FLOW            // Automated flow (no AI reasoning)
  CAMPAIGN        // Broadcast/campaign attribution
  ORGANIC         // Contact-initiated, no clear attribution
}

enum AlertType {
  REVENUE_MILESTONE    // Revenue exceeds target
  NO_SHOW_SPIKE        // No-show rate above threshold
  AI_FAILURE_SPIKE     // AI escalation rate too high
  VIP_WAITING          // VIP contact waiting too long
  RESPONSE_TIME_HIGH   // Average response time degraded
  OCCUPANCY_LOW        // Professional occupancy below target
  REACTIVATION_WIN     // Churned contact came back
}

enum AlertStatus {
  PENDING
  SENT
  ACKNOWLEDGED
  DISMISSED
}
```

### 3.2 New Models

#### AnalyticsEvent (Append-Only Event Stream)

Every significant action in the system writes an event. This is the single source of truth for all analytics computations.

```prisma
model AnalyticsEvent {
  id             String            @id @default(cuid())
  organizationId String
  organization   Organization      @relation(fields: [organizationId], references: [id], onDelete: Cascade)

  // What happened
  eventType      String            // "appointment_created", "order_completed", "message_sent_ai",
                                   // "message_sent_human", "lead_converted", "contact_reactivated",
                                   // "ai_escalated", "no_show", "pipeline_stage_moved"
  eventCategory  String            // "revenue", "engagement", "scheduling", "conversion", "support"

  // Who / What
  contactId      String?
  conversationId String?
  appointmentId  String?
  orderId        String?
  flowId         String?
  campaignId     String?
  userId         String?           // Human user if applicable

  // Attribution
  source         AttributionSource @default(ORGANIC)

  // Value
  revenueAmount  Decimal?          @db.Decimal(12, 2)
  numericValue   Float?            // Generic numeric value (e.g., response time in ms, score)

  // Context
  metadata       Json?             // Flexible additional data
  occurredAt     DateTime          @default(now())
  createdAt      DateTime          @default(now())

  @@index([organizationId, occurredAt])
  @@index([organizationId, eventType, occurredAt])
  @@index([organizationId, eventCategory, occurredAt])
  @@index([organizationId, source, occurredAt])
  @@index([contactId, occurredAt])
  @@index([conversationId])
}
```

#### DailyMetrics (Pre-Aggregated Daily Snapshot)

One row per organization per day. This is the primary data source for the dashboard.

```prisma
model DailyMetrics {
  id             String       @id @default(cuid())
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id], onDelete: Cascade)
  date           DateTime     @db.Date

  // === REVENUE ===
  totalRevenue          Decimal @default(0) @db.Decimal(12, 2)
  aiRevenue             Decimal @default(0) @db.Decimal(12, 2)
  humanRevenue          Decimal @default(0) @db.Decimal(12, 2)
  flowRevenue           Decimal @default(0) @db.Decimal(12, 2)
  campaignRevenue       Decimal @default(0) @db.Decimal(12, 2)
  organicRevenue        Decimal @default(0) @db.Decimal(12, 2)

  // === APPOINTMENTS ===
  appointmentsTotal     Int     @default(0)
  appointmentsByAi      Int     @default(0)
  appointmentsByHuman   Int     @default(0)
  appointmentsCompleted Int     @default(0)
  appointmentsNoShow    Int     @default(0)
  appointmentsCancelled Int     @default(0)

  // === CONVERSATIONS ===
  conversationsOpened   Int     @default(0)
  conversationsClosed   Int     @default(0)
  messagesInbound       Int     @default(0)
  messagesOutboundAi    Int     @default(0)
  messagesOutboundHuman Int     @default(0)
  messagesOutboundFlow  Int     @default(0)

  // === CONTACTS ===
  newContacts           Int     @default(0)
  returningContacts     Int     @default(0)
  reactivatedContacts   Int     @default(0)  // Were churned, came back
  churnedContacts       Int     @default(0)

  // === CONVERSION ===
  leadsCreated          Int     @default(0)
  leadsConverted        Int     @default(0)  // lead -> customer
  conversionRate        Float   @default(0)  // leadsConverted / leadsCreated

  // === PERFORMANCE ===
  avgResponseTimeMs     Float   @default(0)  // Average first response time
  avgAiResponseTimeMs   Float   @default(0)
  avgHumanResponseTimeMs Float  @default(0)
  aiEscalations         Int     @default(0)  // Times AI handed off to human
  aiConfidenceAvg       Float   @default(0)  // Average AI confidence score

  // === PIPELINE ===
  pipelineValueTotal    Decimal @default(0) @db.Decimal(12, 2)
  pipelineValueNew      Decimal @default(0) @db.Decimal(12, 2)  // New deals today
  pipelineValueWon      Decimal @default(0) @db.Decimal(12, 2)  // Deals closed-won today
  pipelineValueLost     Decimal @default(0) @db.Decimal(12, 2)  // Deals closed-lost today

  // === SATISFACTION ===
  sentimentAvg          Float   @default(0)  // -1 to 1, average from ConversationInsight
  qualityScoreAvg       Float   @default(0)  // 0-10, from WATCH agent
  npsEstimated          Float   @default(0)  // Inferred NPS from sentiment patterns

  // === OCCUPANCY (for service businesses like barbers) ===
  totalSlots            Int     @default(0)  // Available appointment slots
  filledSlots           Int     @default(0)
  occupancyRate         Float   @default(0)  // filledSlots / totalSlots

  // === CAMPAIGNS ===
  campaignsSent         Int     @default(0)
  campaignsDelivered    Int     @default(0)
  campaignsRead         Int     @default(0)

  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt

  @@unique([organizationId, date])
  @@index([organizationId, date])
}
```

#### MonthlyMetrics (Rolled Up Monthly)

Same structure but aggregated monthly for fast period comparisons.

```prisma
model MonthlyMetrics {
  id             String       @id @default(cuid())
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id], onDelete: Cascade)
  year           Int
  month          Int          // 1-12

  // === REVENUE ===
  totalRevenue          Decimal @default(0) @db.Decimal(12, 2)
  aiRevenue             Decimal @default(0) @db.Decimal(12, 2)
  humanRevenue          Decimal @default(0) @db.Decimal(12, 2)
  flowRevenue           Decimal @default(0) @db.Decimal(12, 2)
  campaignRevenue       Decimal @default(0) @db.Decimal(12, 2)

  // === APPOINTMENTS ===
  appointmentsTotal     Int     @default(0)
  appointmentsByAi      Int     @default(0)
  appointmentsByHuman   Int     @default(0)
  appointmentsNoShow    Int     @default(0)
  noShowRate            Float   @default(0)

  // === CONTACTS ===
  newContacts           Int     @default(0)
  returningContacts     Int     @default(0)
  reactivatedContacts   Int     @default(0)
  churnedContacts       Int     @default(0)
  activeContacts        Int     @default(0)  // Distinct contacts with activity

  // === CONVERSION ===
  leadsCreated          Int     @default(0)
  leadsConverted        Int     @default(0)
  conversionRate        Float   @default(0)

  // === PERFORMANCE ===
  avgResponseTimeMs     Float   @default(0)
  aiEscalationRate      Float   @default(0)

  // === MESSAGES ===
  totalMessages         Int     @default(0)
  aiMessages            Int     @default(0)
  humanMessages         Int     @default(0)
  aiMessageRatio        Float   @default(0)  // aiMessages / totalOutbound

  // === LTV ===
  avgTicket             Decimal @default(0) @db.Decimal(12, 2)
  avgLtv                Decimal @default(0) @db.Decimal(12, 2)  // Revenue per contact (lifetime)

  // === SATISFACTION ===
  sentimentAvg          Float   @default(0)
  qualityScoreAvg       Float   @default(0)

  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt

  @@unique([organizationId, year, month])
  @@index([organizationId, year, month])
}
```

#### AnalyticsAlert

```prisma
model AnalyticsAlert {
  id             String       @id @default(cuid())
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id], onDelete: Cascade)

  alertType      AlertType
  status         AlertStatus  @default(PENDING)
  title          String
  message        String       @db.Text
  severity       String       @default("info")  // info, warning, critical
  metric         String?      // Which metric triggered it (e.g., "noShowRate")
  currentValue   Float?       // The value that triggered the alert
  thresholdValue Float?       // The threshold that was crossed
  metadata       Json?

  sentAt         DateTime?    // When notification was sent
  acknowledgedAt DateTime?    // When owner acknowledged
  createdAt      DateTime     @default(now())

  @@index([organizationId, status])
  @@index([organizationId, alertType, createdAt])
  @@index([organizationId, createdAt])
}
```

#### AlertConfig (Per-Org Thresholds)

```prisma
model AlertConfig {
  id             String       @id @default(cuid())
  organizationId String       @unique
  organization   Organization @relation(fields: [organizationId], references: [id], onDelete: Cascade)

  // Revenue alerts
  revenueTargetMonthly  Decimal? @db.Decimal(12, 2)  // Target monthly revenue
  revenueAlertEnabled   Boolean  @default(true)

  // No-show alerts
  noShowThreshold       Float    @default(0.2)  // Alert if >20% no-show rate
  noShowAlertEnabled    Boolean  @default(true)

  // AI failure alerts
  aiEscalationThreshold Float   @default(0.3)  // Alert if >30% escalation rate
  aiFailureAlertEnabled Boolean  @default(true)

  // VIP response time
  vipResponseTimeMs     Int      @default(300000)  // 5 minutes
  vipAlertEnabled       Boolean  @default(true)

  // Occupancy alerts
  occupancyLowThreshold Float   @default(0.5)  // Alert if <50% occupancy
  occupancyAlertEnabled Boolean  @default(true)

  // Notification channel
  notifyWhatsApp        Boolean  @default(true)
  notifyPhone           String?  // WhatsApp number of the owner
  notifyEmail           String?
  quietHoursStart       String?  // "22:00"
  quietHoursEnd         String?  // "07:00"

  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt
}
```

### 3.3 Schema Changes to Existing Models

These additions to existing models enable proper attribution tracking.

```prisma
// ADD TO Message model:
//   isAiGenerated  Boolean  @default(false)  // True if AI composed this message
//   aiConfidence   Float?                     // AI confidence when generating

// ADD TO Appointment model:
//   bookedBy       AttributionSource @default(ORGANIC)  // Who booked it?
//   bookedVia      String?           // "whatsapp_ai", "whatsapp_human", "booking_page", "manual"

// ADD TO Order model:
//   attributionSource  AttributionSource @default(ORGANIC)

// ADD TO Conversation model:
//   handledBy      AttributionSource? // Primary handler: AI_AGENT, AI_ASSISTED, HUMAN

// ADD TO Organization model:
//   analyticsEvents     AnalyticsEvent[]
//   dailyMetrics        DailyMetrics[]
//   monthlyMetrics      MonthlyMetrics[]
//   analyticsAlerts     AnalyticsAlert[]
//   alertConfig         AlertConfig?
```

---

## 4. Attribution Model

### 4.1 How to Determine AI vs. Human

The attribution flows from the conversation context:

```
Message arrives (INBOUND)
  |
  v
Who responded?
  |
  +---> AgentDecisionLog with action=RESPOND --> AI_AGENT
  |     (confidence > threshold, no escalation)
  |
  +---> AgentDecisionLog with action=ESCALATE --> AI_ASSISTED
  |     (AI started, human finished)
  |
  +---> No AgentDecisionLog, human User replied --> HUMAN
  |
  +---> Flow triggered (keyword/welcome) --> FLOW
  |
  +---> Campaign/Broadcast sent --> CAMPAIGN
```

### 4.2 Revenue Attribution Rules

| Event | Attribution Logic |
|-------|-------------------|
| **Appointment booked via WhatsApp** | Check if the conversation's `handledBy` is AI_AGENT. If AI was the last touch before the booking, attribute to AI. |
| **Order completed** | Check the conversation linked to the order. If AI was involved at any point, mark as AI_ASSISTED. If AI handled end-to-end, mark AI_AGENT. |
| **Pipeline card moved to Won** | Check the contact's last conversation. Apply last-touch attribution. |
| **Contact reactivated** | If a PULSE agent follow-up preceded the reactivation, attribute to AI. Check `AgentDecisionLog` for `REACTIVATION_SENT` action. |
| **Campaign conversion** | If a campaign message led to a conversation that led to revenue, attribute to CAMPAIGN. |

### 4.3 Conversation-Level Attribution

Set `Conversation.handledBy` based on message analysis:

```typescript
function determineConversationAttribution(conversationId: string): AttributionSource {
  const messages = await prisma.message.findMany({
    where: { conversationId, direction: 'OUTBOUND' },
    orderBy: { createdAt: 'asc' },
  });

  const aiMessages = messages.filter(m => m.isAiGenerated);
  const humanMessages = messages.filter(m => !m.isAiGenerated);

  if (aiMessages.length > 0 && humanMessages.length === 0) return 'AI_AGENT';
  if (aiMessages.length > 0 && humanMessages.length > 0) return 'AI_ASSISTED';
  if (humanMessages.length > 0) return 'HUMAN';
  return 'ORGANIC';
}
```

### 4.4 Appointment Attribution

When an appointment is created, determine source:

```typescript
function attributeAppointment(appointment: Appointment): AttributionSource {
  // Check if there is a conversation with this contact in the last 24h
  const recentConversation = await prisma.conversation.findFirst({
    where: {
      organizationId: appointment.organizationId,
      contactIdentity: { contactId: appointment.contactId },
      lastMessageAt: { gte: subHours(appointment.createdAt, 24) },
    },
    include: { messages: { where: { direction: 'OUTBOUND' }, orderBy: { createdAt: 'desc' }, take: 5 } },
  });

  if (!recentConversation) return 'ORGANIC'; // Booked via booking page directly

  // Check AgentDecisionLog for this conversation
  const aiDecisions = await prisma.agentDecisionLog.findMany({
    where: {
      conversationId: recentConversation.id,
      action: { in: ['RESPOND', 'FLOW_TRIGGERED'] },
      createdAt: { gte: subHours(appointment.createdAt, 24) },
    },
  });

  if (aiDecisions.length > 0) {
    const humanMessages = recentConversation.messages.filter(m => !m.metadata?.isAiGenerated);
    return humanMessages.length > 0 ? 'AI_ASSISTED' : 'AI_AGENT';
  }

  return 'HUMAN';
}
```

---

## 5. Queries for Every Metric

### 5.1 Revenue Metrics

#### Monthly Revenue (Current vs. Previous)

```sql
-- Current month revenue by source
SELECT
  SUM(d."totalRevenue") AS total_revenue,
  SUM(d."aiRevenue") AS ai_revenue,
  SUM(d."humanRevenue") AS human_revenue,
  SUM(d."flowRevenue") AS flow_revenue,
  SUM(d."campaignRevenue") AS campaign_revenue,
  SUM(d."organicRevenue") AS organic_revenue
FROM "DailyMetrics" d
WHERE d."organizationId" = $1
  AND d.date >= date_trunc('month', CURRENT_DATE)
  AND d.date < date_trunc('month', CURRENT_DATE) + interval '1 month';

-- Previous month (for comparison)
SELECT
  SUM(d."totalRevenue") AS total_revenue,
  SUM(d."aiRevenue") AS ai_revenue,
  SUM(d."humanRevenue") AS human_revenue
FROM "DailyMetrics" d
WHERE d."organizationId" = $1
  AND d.date >= date_trunc('month', CURRENT_DATE) - interval '1 month'
  AND d.date < date_trunc('month', CURRENT_DATE);
```

**Prisma equivalent:**

```typescript
const currentMonthRevenue = await prisma.dailyMetrics.aggregate({
  where: {
    organizationId: orgId,
    date: {
      gte: startOfMonth(new Date()),
      lt: startOfMonth(addMonths(new Date(), 1)),
    },
  },
  _sum: {
    totalRevenue: true,
    aiRevenue: true,
    humanRevenue: true,
    flowRevenue: true,
    campaignRevenue: true,
  },
});
```

#### AI Revenue Percentage

```sql
SELECT
  CASE
    WHEN SUM("totalRevenue") > 0
    THEN ROUND(SUM("aiRevenue") * 100.0 / SUM("totalRevenue"), 1)
    ELSE 0
  END AS ai_revenue_pct
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= date_trunc('month', CURRENT_DATE);
```

#### Average Ticket per Channel

```sql
SELECT
  ae.source,
  ROUND(AVG(ae."revenueAmount"), 2) AS avg_ticket,
  COUNT(*) AS total_transactions
FROM "AnalyticsEvent" ae
WHERE ae."organizationId" = $1
  AND ae."eventCategory" = 'revenue'
  AND ae."revenueAmount" > 0
  AND ae."occurredAt" >= date_trunc('month', CURRENT_DATE)
GROUP BY ae.source
ORDER BY avg_ticket DESC;
```

#### LTV per Contact (Lifetime Value)

```sql
SELECT
  c.id AS contact_id,
  c.name,
  c."journeyState",
  COALESCE(SUM(ra."revenueAmount"), 0) AS lifetime_value,
  COUNT(DISTINCT ra.id) AS total_transactions,
  MIN(ra."occurredAt") AS first_purchase,
  MAX(ra."occurredAt") AS last_purchase
FROM "Contact" c
LEFT JOIN "RevenueAttribution" ra ON ra."contactId" = c.id
WHERE c."organizationId" = $1
GROUP BY c.id, c.name, c."journeyState"
HAVING SUM(ra."revenueAmount") > 0
ORDER BY lifetime_value DESC
LIMIT 50;
```

### 5.2 Appointment Metrics

#### Appointments Today/This Week (AI vs. Human)

```sql
-- Today
SELECT
  "appointmentsTotal",
  "appointmentsByAi",
  "appointmentsByHuman",
  "appointmentsCompleted",
  "appointmentsNoShow"
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date = CURRENT_DATE;

-- This week
SELECT
  SUM("appointmentsTotal") AS total,
  SUM("appointmentsByAi") AS by_ai,
  SUM("appointmentsByHuman") AS by_human,
  SUM("appointmentsNoShow") AS no_shows,
  CASE
    WHEN SUM("appointmentsTotal") > 0
    THEN ROUND(SUM("appointmentsNoShow") * 100.0 / SUM("appointmentsTotal"), 1)
    ELSE 0
  END AS no_show_rate
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= date_trunc('week', CURRENT_DATE)
  AND date <= CURRENT_DATE;
```

#### No-Show Rate Trend (Last 30 Days)

```sql
SELECT
  date,
  "appointmentsTotal",
  "appointmentsNoShow",
  CASE
    WHEN "appointmentsTotal" > 0
    THEN ROUND("appointmentsNoShow" * 100.0 / "appointmentsTotal", 1)
    ELSE 0
  END AS no_show_rate
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= CURRENT_DATE - interval '30 days'
ORDER BY date;
```

#### Professional Occupancy Rate

```sql
-- Real-time query against Appointments + Availability
SELECT
  u.id AS professional_id,
  u.name AS professional_name,
  COUNT(a.id) FILTER (WHERE a.status IN ('SCHEDULED', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED'))
    AS booked_appointments,
  -- Calculate total available slots from Availability for this period
  COUNT(a.id) FILTER (WHERE a.status = 'COMPLETED') AS completed,
  COUNT(a.id) FILTER (WHERE a.status = 'NO_SHOW') AS no_shows
FROM "User" u
JOIN "OrgMember" om ON om."userId" = u.id AND om."organizationId" = $1
LEFT JOIN "Appointment" a ON a."assignedToId" = u.id
  AND a."startTime" >= $2  -- period start
  AND a."startTime" < $3   -- period end
GROUP BY u.id, u.name
ORDER BY booked_appointments DESC;
```

### 5.3 Conversion Metrics

#### AI Conversion Rate (Lead to Appointment/Purchase)

```sql
-- How many contacts that AI handled ended up converting?
WITH ai_conversations AS (
  SELECT DISTINCT ae."contactId"
  FROM "AnalyticsEvent" ae
  WHERE ae."organizationId" = $1
    AND ae.source = 'AI_AGENT'
    AND ae."eventCategory" = 'engagement'
    AND ae."occurredAt" >= date_trunc('month', CURRENT_DATE)
),
ai_conversions AS (
  SELECT DISTINCT ae."contactId"
  FROM "AnalyticsEvent" ae
  WHERE ae."organizationId" = $1
    AND ae.source IN ('AI_AGENT', 'AI_ASSISTED')
    AND ae."eventCategory" = 'revenue'
    AND ae."occurredAt" >= date_trunc('month', CURRENT_DATE)
    AND ae."contactId" IN (SELECT "contactId" FROM ai_conversations)
)
SELECT
  (SELECT COUNT(*) FROM ai_conversations) AS ai_leads,
  (SELECT COUNT(*) FROM ai_conversions) AS ai_conversions,
  CASE
    WHEN (SELECT COUNT(*) FROM ai_conversations) > 0
    THEN ROUND(
      (SELECT COUNT(*) FROM ai_conversions) * 100.0 /
      (SELECT COUNT(*) FROM ai_conversations), 1
    )
    ELSE 0
  END AS ai_conversion_rate;
```

#### New vs. Returning Contacts

```sql
SELECT
  SUM("newContacts") AS new_contacts,
  SUM("returningContacts") AS returning_contacts,
  CASE
    WHEN SUM("newContacts") + SUM("returningContacts") > 0
    THEN ROUND(
      SUM("returningContacts") * 100.0 /
      (SUM("newContacts") + SUM("returningContacts")), 1
    )
    ELSE 0
  END AS returning_pct
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= date_trunc('month', CURRENT_DATE);
```

#### Reactivated Contacts by AI

```sql
SELECT
  SUM("reactivatedContacts") AS reactivated_total,
  -- Revenue from reactivated contacts
  COALESCE(
    (SELECT SUM(ae."revenueAmount")
     FROM "AnalyticsEvent" ae
     WHERE ae."organizationId" = $1
       AND ae."eventType" = 'contact_reactivated'
       AND ae."occurredAt" >= date_trunc('month', CURRENT_DATE)),
    0
  ) AS reactivation_revenue
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= date_trunc('month', CURRENT_DATE);
```

### 5.4 Performance Metrics

#### Messages: AI vs. Human

```sql
SELECT
  SUM("messagesOutboundAi") AS ai_messages,
  SUM("messagesOutboundHuman") AS human_messages,
  SUM("messagesOutboundFlow") AS flow_messages,
  SUM("messagesInbound") AS inbound,
  CASE
    WHEN SUM("messagesOutboundAi") + SUM("messagesOutboundHuman") + SUM("messagesOutboundFlow") > 0
    THEN ROUND(
      SUM("messagesOutboundAi") * 100.0 /
      (SUM("messagesOutboundAi") + SUM("messagesOutboundHuman") + SUM("messagesOutboundFlow")), 1
    )
    ELSE 0
  END AS ai_pct
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= date_trunc('month', CURRENT_DATE);
```

#### Average Response Time

```sql
SELECT
  ROUND(AVG("avgResponseTimeMs") / 1000.0, 1) AS avg_response_seconds,
  ROUND(AVG("avgAiResponseTimeMs") / 1000.0, 1) AS avg_ai_response_seconds,
  ROUND(AVG("avgHumanResponseTimeMs") / 1000.0, 1) AS avg_human_response_seconds
FROM "DailyMetrics"
WHERE "organizationId" = $1
  AND date >= CURRENT_DATE - interval '7 days';
```

#### Satisfaction Score (Inferred from Sentiment)

```sql
-- Map sentiment (-1 to 1) to satisfaction categories
SELECT
  COUNT(*) FILTER (WHERE ci.sentiment > 0.3) AS positive,
  COUNT(*) FILTER (WHERE ci.sentiment BETWEEN -0.3 AND 0.3) AS neutral,
  COUNT(*) FILTER (WHERE ci.sentiment < -0.3) AS negative,
  ROUND(AVG(ci.sentiment), 2) AS avg_sentiment,
  ROUND(AVG(ci."qualityScore"), 1) AS avg_quality_score,
  -- Estimated NPS: (% positive - % negative) * 100
  ROUND(
    (COUNT(*) FILTER (WHERE ci.sentiment > 0.3) * 100.0 / NULLIF(COUNT(*), 0)) -
    (COUNT(*) FILTER (WHERE ci.sentiment < -0.3) * 100.0 / NULLIF(COUNT(*), 0)),
    0
  ) AS estimated_nps
FROM "ConversationInsight" ci
JOIN "Conversation" conv ON conv.id = ci."conversationId"
WHERE ci."organizationId" = $1
  AND conv."lastMessageAt" >= date_trunc('month', CURRENT_DATE);
```

### 5.5 Pipeline Metrics

#### Pipeline Value by Stage

```sql
SELECT
  ps.name AS stage_name,
  ps.color,
  ps."sortOrder",
  COUNT(pc.id) AS card_count,
  COALESCE(SUM(pc.value), 0) AS total_value
FROM "PipelineStage" ps
LEFT JOIN "PipelineCard" pc ON pc."stageId" = ps.id
WHERE ps."organizationId" = $1
  AND ps."pipelineId" = $2
GROUP BY ps.id, ps.name, ps.color, ps."sortOrder"
ORDER BY ps."sortOrder";
```

---

## 6. Dashboard Design

### 6.1 Card Hierarchy and Layout

The dashboard is organized in 3 tiers of visual priority.

#### Tier 1: Hero Cards (Top of page -- the "money shot")

These are the first things the owner sees. Large numbers, bold colors.

```
+-------------------------------------------------------+
|  FATURAMENTO DO MES          |  RECEITA DA IA          |
|  R$ 24.800,00                |  R$ 12.400,00 (50%)     |
|  +18% vs mes anterior       |  +32% vs mes anterior   |
+-------------------------------------------------------+
|  AGENDAMENTOS HOJE  |  TAXA OCUPACAO  |  NO-SHOW RATE  |
|  12                  |  78%            |  8%            |
|  8 pela IA           |  target: 80%   |  target: <15%  |
+-------------------------------------------------------+
```

#### Tier 2: Performance Cards (Middle section)

```
+----------------------------+----------------------------+
|  MENSAGENS RESPONDIDAS      |  TEMPO MEDIO RESPOSTA     |
|  [====== AI 72% ======]     |  AI: 4s                   |
|  [== Humano 28% ==]         |  Humano: 3m 12s           |
|  Total: 1,847 este mes      |  Geral: 52s               |
+----------------------------+----------------------------+
|  CONVERSAO (Lead -> Agend.) |  SATISFACAO ESTIMADA      |
|  AI: 34%                    |  Score: 8.2/10            |
|  Humano: 28%                |  NPS estimado: +62        |
|  Geral: 31%                 |  [====Positivo 78%====]   |
+----------------------------+----------------------------+
```

#### Tier 3: Deep Dive (Bottom section, scrollable)

```
+----------------------------+----------------------------+
|  CLIENTES NOVOS vs RETORNO  |  CLIENTES REATIVADOS      |
|  [Chart: stacked bar 30d]   |  23 este mes pela IA      |
|  Novos: 145 | Retorno: 89   |  R$ 3,200 em receita      |
+----------------------------+----------------------------+
|  PIPELINE DE VENDAS         |  TOP 10 CLIENTES (LTV)    |
|  [Funnel visualization]     |  1. Joao Silva - R$4,200  |
|  R$45k total | R$12k novos  |  2. Maria Santos - R$3,800|
+----------------------------+----------------------------+
|  TENDENCIA RECEITA (30d)    |  TAXA NO-SHOW (30d)       |
|  [Line chart: AI vs Human]  |  [Line chart with target] |
+----------------------------+----------------------------+
```

### 6.2 Card Specifications

| Card | Data Source | Refresh | Cache TTL |
|------|------------|---------|-----------|
| Faturamento do Mes | `MonthlyMetrics` or SUM(`DailyMetrics`) | 15 min | 5 min |
| Receita da IA | `DailyMetrics.aiRevenue` SUM | 15 min | 5 min |
| Agendamentos Hoje | `DailyMetrics` (today) + live query | 5 min | 2 min |
| Taxa Ocupacao | Live: `Appointment` vs `Availability` | 5 min | 2 min |
| No-Show Rate | `DailyMetrics` (week rolling) | 15 min | 5 min |
| Mensagens AI vs Humano | `DailyMetrics` SUM | 15 min | 5 min |
| Tempo Medio Resposta | `DailyMetrics.avgResponseTimeMs` | 15 min | 5 min |
| Conversao | `DailyMetrics.conversionRate` | 30 min | 10 min |
| Satisfacao | `ConversationInsight` aggregate | 30 min | 10 min |
| Clientes Novos vs Retorno | `DailyMetrics` (30d) | 1 hour | 30 min |
| Reativados pela IA | `DailyMetrics.reactivatedContacts` | 1 hour | 30 min |
| Pipeline | Live: `PipelineCard` aggregate | 15 min | 5 min |
| Top Clientes LTV | `RevenueAttribution` aggregate | 1 hour | 30 min |
| Tendencia 30d | `DailyMetrics` (30 rows) | 1 hour | 30 min |

### 6.3 Time Range Selector

The dashboard supports these period views:

- **Hoje** (default for operational metrics)
- **Esta Semana**
- **Este Mes** (default for revenue metrics)
- **Ultimos 30 dias**
- **Mes anterior**
- **Personalizado** (date range picker)

Every card that shows a comparison uses the equivalent previous period (this month vs last month, this week vs last week).

---

## 7. Caching Strategy (Redis)

### 7.1 Cache Key Structure

```
analytics:{orgId}:{metric}:{period}:{params}
```

Examples:

```
analytics:org_abc:revenue:month:2026-02       # Monthly revenue summary
analytics:org_abc:appointments:day:2026-02-25  # Today's appointments
analytics:org_abc:pipeline:live:pipe_xyz       # Pipeline value by stage
analytics:org_abc:dashboard:month:2026-02      # Full dashboard payload (combined)
analytics:org_abc:top_clients:ltv:50           # Top 50 LTV clients
```

### 7.2 TTL Strategy

| Metric Category | TTL | Rationale |
|-----------------|-----|-----------|
| Real-time (today's appointments, occupancy) | 2 minutes | Owner needs near-real-time view |
| Operational (messages, response time) | 5 minutes | Good enough for monitoring |
| Revenue (monthly totals, AI revenue) | 5 minutes | Updated by aggregation job |
| Trend data (30d charts) | 30 minutes | Historical data changes slowly |
| LTV / Top clients | 30 minutes | Computed hourly |
| Dashboard composite | 5 minutes | Single cached payload for initial load |

### 7.3 Cache Warming

On dashboard load, the API checks Redis first. If cache miss, it computes the metric and stores it. Background jobs also pre-warm caches proactively.

```typescript
async function getDashboardData(orgId: string, period: string): Promise<DashboardPayload> {
  const cacheKey = `analytics:${orgId}:dashboard:${period}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Compute all metrics in parallel
  const [revenue, appointments, messages, conversion, satisfaction, pipeline] = await Promise.all([
    computeRevenueMetrics(orgId, period),
    computeAppointmentMetrics(orgId, period),
    computeMessageMetrics(orgId, period),
    computeConversionMetrics(orgId, period),
    computeSatisfactionMetrics(orgId, period),
    computePipelineMetrics(orgId, period),
  ]);

  const payload = { revenue, appointments, messages, conversion, satisfaction, pipeline, updatedAt: new Date() };

  await redis.setex(cacheKey, 300, JSON.stringify(payload)); // 5 min TTL
  return payload;
}
```

### 7.4 Cache Invalidation

Cache is invalidated in two ways:

1. **TTL expiry** (primary) -- caches naturally expire
2. **Event-driven invalidation** -- when an AnalyticsEvent is written, invalidate related caches:

```typescript
async function onAnalyticsEvent(event: AnalyticsEvent): Promise<void> {
  const { organizationId, eventCategory } = event;
  const patterns = [
    `analytics:${organizationId}:dashboard:*`,
    `analytics:${organizationId}:${eventCategory}:*`,
  ];
  for (const pattern of patterns) {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) await redis.del(...keys);
  }
}
```

---

## 8. Aggregation Jobs (BullMQ)

### 8.1 Job Architecture

```
Queue: analytics-aggregation
  |
  +-- Job: compute-daily-metrics     (runs every 15 min)
  +-- Job: compute-monthly-metrics   (runs every hour)
  +-- Job: check-alerts              (runs every 10 min)
  +-- Job: backfill-daily-metrics    (manual trigger or on deploy)
  +-- Job: compute-occupancy         (runs every 5 min, service businesses only)
```

### 8.2 Daily Metrics Computation Job

```typescript
// File: /home/tikso/tikso/src/jobs/analytics/compute-daily-metrics.ts

import { Queue, Worker } from 'bullmq';
import { prisma } from '@/lib/prisma';

const QUEUE_NAME = 'analytics-aggregation';

export const analyticsQueue = new Queue(QUEUE_NAME, { connection: redisConnection });

// Schedule: every 15 minutes
analyticsQueue.add('compute-daily-metrics', {}, {
  repeat: { every: 15 * 60 * 1000 },
  removeOnComplete: 100,
  removeOnFail: 50,
});

export const dailyMetricsWorker = new Worker(QUEUE_NAME, async (job) => {
  if (job.name !== 'compute-daily-metrics') return;

  const today = startOfDay(new Date());
  const orgs = await prisma.organization.findMany({ select: { id: true } });

  for (const org of orgs) {
    await computeDailyMetricsForOrg(org.id, today);
  }
}, { connection: redisConnection, concurrency: 3 });

async function computeDailyMetricsForOrg(orgId: string, date: Date): Promise<void> {
  const dayStart = date;
  const dayEnd = endOfDay(date);

  // Parallel computation of all metrics
  const [
    revenue,
    appointments,
    messages,
    contacts,
    conversions,
    performance,
    pipeline,
    satisfaction,
    campaigns,
  ] = await Promise.all([
    computeRevenue(orgId, dayStart, dayEnd),
    computeAppointments(orgId, dayStart, dayEnd),
    computeMessages(orgId, dayStart, dayEnd),
    computeContacts(orgId, dayStart, dayEnd),
    computeConversions(orgId, dayStart, dayEnd),
    computePerformance(orgId, dayStart, dayEnd),
    computePipeline(orgId, dayStart, dayEnd),
    computeSatisfaction(orgId, dayStart, dayEnd),
    computeCampaigns(orgId, dayStart, dayEnd),
  ]);

  // Upsert daily metrics (idempotent)
  await prisma.dailyMetrics.upsert({
    where: { organizationId_date: { organizationId: orgId, date: dayStart } },
    create: {
      organizationId: orgId,
      date: dayStart,
      ...revenue,
      ...appointments,
      ...messages,
      ...contacts,
      ...conversions,
      ...performance,
      ...pipeline,
      ...satisfaction,
      ...campaigns,
    },
    update: {
      ...revenue,
      ...appointments,
      ...messages,
      ...contacts,
      ...conversions,
      ...performance,
      ...pipeline,
      ...satisfaction,
      ...campaigns,
    },
  });
}
```

### 8.3 Individual Metric Computation Functions

```typescript
async function computeRevenue(orgId: string, start: Date, end: Date) {
  const attributions = await prisma.revenueAttribution.groupBy({
    by: ['attributionType'],
    where: {
      organizationId: orgId,
      occurredAt: { gte: start, lt: end },
    },
    _sum: { revenueAmount: true },
  });

  // Also use AnalyticsEvent for more granular source tracking
  const events = await prisma.analyticsEvent.groupBy({
    by: ['source'],
    where: {
      organizationId: orgId,
      eventCategory: 'revenue',
      occurredAt: { gte: start, lt: end },
    },
    _sum: { revenueAmount: true },
  });

  const bySource = Object.fromEntries(events.map(e => [e.source, e._sum.revenueAmount || 0]));

  return {
    totalRevenue: Object.values(bySource).reduce((a, b) => a + Number(b), 0),
    aiRevenue: Number(bySource['AI_AGENT'] || 0) + Number(bySource['AI_ASSISTED'] || 0),
    humanRevenue: Number(bySource['HUMAN'] || 0),
    flowRevenue: Number(bySource['FLOW'] || 0),
    campaignRevenue: Number(bySource['CAMPAIGN'] || 0),
    organicRevenue: Number(bySource['ORGANIC'] || 0),
  };
}

async function computeAppointments(orgId: string, start: Date, end: Date) {
  const appts = await prisma.appointment.groupBy({
    by: ['status', 'bookedBy'],
    where: {
      organizationId: orgId,
      startTime: { gte: start, lt: end },
    },
    _count: true,
  });

  let total = 0, byAi = 0, byHuman = 0, completed = 0, noShow = 0, cancelled = 0;
  for (const a of appts) {
    const count = a._count;
    total += count;
    if (a.bookedBy === 'AI_AGENT' || a.bookedBy === 'AI_ASSISTED') byAi += count;
    else byHuman += count;
    if (a.status === 'COMPLETED') completed += count;
    if (a.status === 'NO_SHOW') noShow += count;
    if (a.status === 'CANCELLED') cancelled += count;
  }

  return {
    appointmentsTotal: total,
    appointmentsByAi: byAi,
    appointmentsByHuman: byHuman,
    appointmentsCompleted: completed,
    appointmentsNoShow: noShow,
    appointmentsCancelled: cancelled,
  };
}

async function computeMessages(orgId: string, start: Date, end: Date) {
  const inbound = await prisma.message.count({
    where: { organizationId: orgId, direction: 'INBOUND', createdAt: { gte: start, lt: end } },
  });

  const outboundAi = await prisma.message.count({
    where: {
      organizationId: orgId,
      direction: 'OUTBOUND',
      isAiGenerated: true,
      createdAt: { gte: start, lt: end },
    },
  });

  const outboundTotal = await prisma.message.count({
    where: { organizationId: orgId, direction: 'OUTBOUND', createdAt: { gte: start, lt: end } },
  });

  return {
    messagesInbound: inbound,
    messagesOutboundAi: outboundAi,
    messagesOutboundHuman: outboundTotal - outboundAi, // Simplified; refine with flow detection
    messagesOutboundFlow: 0, // TODO: detect flow-generated messages
  };
}

async function computeContacts(orgId: string, start: Date, end: Date) {
  const newContacts = await prisma.contact.count({
    where: { organizationId: orgId, createdAt: { gte: start, lt: end } },
  });

  // Returning: contacts who had a message today but were created before today
  const returning = await prisma.$queryRaw`
    SELECT COUNT(DISTINCT c.id)::int AS count
    FROM "Contact" c
    JOIN "ContactIdentity" ci ON ci."contactId" = c.id
    JOIN "Conversation" conv ON conv."contactIdentityId" = ci.id
    JOIN "Message" m ON m."conversationId" = conv.id
    WHERE c."organizationId" = ${orgId}
      AND c."createdAt" < ${start}
      AND m."createdAt" >= ${start} AND m."createdAt" < ${end}
      AND m.direction = 'INBOUND'
  `;

  // Reactivated: journeyState changed from "churned" to something else today
  const reactivated = await prisma.journeyTransition.count({
    where: {
      organizationId: orgId,
      fromState: 'churned',
      toState: { not: 'churned' },
      createdAt: { gte: start, lt: end },
    },
  });

  // Churned: journeyState changed to "churned" today
  const churned = await prisma.journeyTransition.count({
    where: {
      organizationId: orgId,
      toState: 'churned',
      createdAt: { gte: start, lt: end },
    },
  });

  return {
    newContacts,
    returningContacts: returning[0]?.count || 0,
    reactivatedContacts: reactivated,
    churnedContacts: churned,
  };
}

async function computePerformance(orgId: string, start: Date, end: Date) {
  const replyEvents = await prisma.agentReplyEvent.aggregate({
    where: { organizationId: orgId, createdAt: { gte: start, lt: end } },
    _avg: { responseTimeMs: true },
  });

  // AI escalations
  const escalations = await prisma.agentDecisionLog.count({
    where: {
      organizationId: orgId,
      action: 'ESCALATE',
      createdAt: { gte: start, lt: end },
    },
  });

  const aiConfidence = await prisma.agentDecisionLog.aggregate({
    where: {
      organizationId: orgId,
      action: 'RESPOND',
      createdAt: { gte: start, lt: end },
    },
    _avg: { confidence: true },
  });

  return {
    avgResponseTimeMs: replyEvents._avg.responseTimeMs || 0,
    avgAiResponseTimeMs: 0,   // TODO: filter by AI agent
    avgHumanResponseTimeMs: 0, // TODO: filter by human agent
    aiEscalations: escalations,
    aiConfidenceAvg: aiConfidence._avg.confidence || 0,
  };
}

async function computeSatisfaction(orgId: string, start: Date, end: Date) {
  const insights = await prisma.conversationInsight.aggregate({
    where: {
      organizationId: orgId,
      conversation: { lastMessageAt: { gte: start, lt: end } },
    },
    _avg: {
      sentiment: true,
      qualityScore: true,
    },
  });

  return {
    sentimentAvg: insights._avg.sentiment || 0,
    qualityScoreAvg: insights._avg.qualityScore || 0,
    npsEstimated: (insights._avg.sentiment || 0) * 100, // Simplified NPS estimation
  };
}
```

### 8.4 Monthly Roll-Up Job

```typescript
// Runs every hour, recomputes current month
analyticsQueue.add('compute-monthly-metrics', {}, {
  repeat: { every: 60 * 60 * 1000 },
  removeOnComplete: 50,
});

async function computeMonthlyMetrics(orgId: string, year: number, month: number): Promise<void> {
  const dailyData = await prisma.dailyMetrics.findMany({
    where: {
      organizationId: orgId,
      date: {
        gte: new Date(year, month - 1, 1),
        lt: new Date(year, month, 1),
      },
    },
  });

  if (dailyData.length === 0) return;

  const sumField = (field: string) => dailyData.reduce((sum, d) => sum + Number(d[field] || 0), 0);
  const avgField = (field: string) => {
    const values = dailyData.map(d => Number(d[field] || 0)).filter(v => v > 0);
    return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
  };

  const totalOutbound = sumField('messagesOutboundAi') + sumField('messagesOutboundHuman') + sumField('messagesOutboundFlow');

  await prisma.monthlyMetrics.upsert({
    where: { organizationId_year_month: { organizationId: orgId, year, month } },
    create: {
      organizationId: orgId,
      year,
      month,
      totalRevenue: sumField('totalRevenue'),
      aiRevenue: sumField('aiRevenue'),
      humanRevenue: sumField('humanRevenue'),
      flowRevenue: sumField('flowRevenue'),
      campaignRevenue: sumField('campaignRevenue'),
      appointmentsTotal: sumField('appointmentsTotal'),
      appointmentsByAi: sumField('appointmentsByAi'),
      appointmentsByHuman: sumField('appointmentsByHuman'),
      appointmentsNoShow: sumField('appointmentsNoShow'),
      noShowRate: sumField('appointmentsTotal') > 0
        ? sumField('appointmentsNoShow') / sumField('appointmentsTotal') : 0,
      newContacts: sumField('newContacts'),
      returningContacts: sumField('returningContacts'),
      reactivatedContacts: sumField('reactivatedContacts'),
      churnedContacts: sumField('churnedContacts'),
      leadsCreated: sumField('leadsCreated'),
      leadsConverted: sumField('leadsConverted'),
      conversionRate: sumField('leadsCreated') > 0
        ? sumField('leadsConverted') / sumField('leadsCreated') : 0,
      avgResponseTimeMs: avgField('avgResponseTimeMs'),
      aiEscalationRate: sumField('messagesOutboundAi') > 0
        ? sumField('aiEscalations') / sumField('messagesOutboundAi') : 0,
      totalMessages: sumField('messagesInbound') + totalOutbound,
      aiMessages: sumField('messagesOutboundAi'),
      humanMessages: sumField('messagesOutboundHuman'),
      aiMessageRatio: totalOutbound > 0
        ? sumField('messagesOutboundAi') / totalOutbound : 0,
      sentimentAvg: avgField('sentimentAvg'),
      qualityScoreAvg: avgField('qualityScoreAvg'),
    },
    update: {
      // Same fields as create -- full recompute each time
      totalRevenue: sumField('totalRevenue'),
      aiRevenue: sumField('aiRevenue'),
      // ... (all other fields)
    },
  });
}
```

### 8.5 Backfill Job

For initial deployment, backfill historical data from existing tables:

```typescript
analyticsQueue.add('backfill-daily-metrics', {
  startDate: '2025-01-01',
  endDate: new Date().toISOString(),
}, { attempts: 3, backoff: { type: 'exponential', delay: 60000 } });

// The worker iterates day by day and calls computeDailyMetricsForOrg
// This should be run once after migration, then disabled
```

---

## 9. Smart Alerts

### 9.1 Alert Check Job

```typescript
// Runs every 10 minutes
analyticsQueue.add('check-alerts', {}, {
  repeat: { every: 10 * 60 * 1000 },
});

async function checkAlerts(orgId: string): Promise<void> {
  const config = await prisma.alertConfig.findUnique({ where: { organizationId: orgId } });
  if (!config) return;

  const today = await prisma.dailyMetrics.findUnique({
    where: { organizationId_date: { organizationId: orgId, date: startOfDay(new Date()) } },
  });
  if (!today) return;

  // Revenue milestone
  if (config.revenueAlertEnabled && config.revenueTargetMonthly) {
    const monthlyRevenue = await prisma.dailyMetrics.aggregate({
      where: {
        organizationId: orgId,
        date: { gte: startOfMonth(new Date()), lt: endOfMonth(new Date()) },
      },
      _sum: { totalRevenue: true },
    });

    const total = Number(monthlyRevenue._sum.totalRevenue || 0);
    if (total >= Number(config.revenueTargetMonthly)) {
      await createAlert(orgId, {
        alertType: 'REVENUE_MILESTONE',
        title: 'Meta de receita atingida!',
        message: `Parabens! Sua receita mensal atingiu R$ ${total.toFixed(2)} (meta: R$ ${Number(config.revenueTargetMonthly).toFixed(2)}).`,
        severity: 'info',
        metric: 'totalRevenue',
        currentValue: total,
        thresholdValue: Number(config.revenueTargetMonthly),
      });
    }
  }

  // No-show spike
  if (config.noShowAlertEnabled && today.appointmentsTotal > 0) {
    const noShowRate = today.appointmentsNoShow / today.appointmentsTotal;
    if (noShowRate > config.noShowThreshold) {
      await createAlert(orgId, {
        alertType: 'NO_SHOW_SPIKE',
        title: 'Taxa de no-show alta',
        message: `${(noShowRate * 100).toFixed(0)}% dos agendamentos de hoje nao compareceram (${today.appointmentsNoShow}/${today.appointmentsTotal}). Limite: ${(config.noShowThreshold * 100).toFixed(0)}%.`,
        severity: 'warning',
        metric: 'noShowRate',
        currentValue: noShowRate,
        thresholdValue: config.noShowThreshold,
      });
    }
  }

  // AI failure spike (high escalation rate)
  if (config.aiFailureAlertEnabled) {
    const totalAi = today.messagesOutboundAi + today.aiEscalations;
    if (totalAi > 10) { // minimum threshold to avoid noise
      const escalationRate = today.aiEscalations / totalAi;
      if (escalationRate > config.aiEscalationThreshold) {
        await createAlert(orgId, {
          alertType: 'AI_FAILURE_SPIKE',
          title: 'IA com muitas transferencias',
          message: `A IA transferiu ${(escalationRate * 100).toFixed(0)}% das conversas para humanos hoje (${today.aiEscalations} de ${totalAi}). Verifique o treinamento da IA.`,
          severity: 'warning',
          metric: 'aiEscalationRate',
          currentValue: escalationRate,
          thresholdValue: config.aiEscalationThreshold,
        });
      }
    }
  }

  // VIP waiting too long
  if (config.vipAlertEnabled) {
    await checkVipWaiting(orgId, config.vipResponseTimeMs);
  }
}
```

### 9.2 VIP Waiting Alert

```typescript
async function checkVipWaiting(orgId: string, maxWaitMs: number): Promise<void> {
  // Find open conversations with VIP contacts that have waited too long
  const vipConversations = await prisma.$queryRaw`
    SELECT
      conv.id,
      c.name AS contact_name,
      c.phone,
      conv."lastMessageAt",
      EXTRACT(EPOCH FROM (NOW() - conv."lastMessageAt")) * 1000 AS wait_ms
    FROM "Conversation" conv
    JOIN "ContactIdentity" ci ON ci.id = conv."contactIdentityId"
    JOIN "Contact" c ON c.id = ci."contactId"
    JOIN "ContactTag" ct ON ct."contactId" = c.id
    JOIN "Tag" t ON t.id = ct."tagId"
    WHERE conv."organizationId" = ${orgId}
      AND conv.status = 'OPEN'
      AND t.name ILIKE '%vip%'
      AND conv."lastMessageAt" IS NOT NULL
      AND EXTRACT(EPOCH FROM (NOW() - conv."lastMessageAt")) * 1000 > ${maxWaitMs}
    LIMIT 5
  `;

  for (const conv of vipConversations) {
    await createAlert(orgId, {
      alertType: 'VIP_WAITING',
      title: `Cliente VIP esperando: ${conv.contact_name}`,
      message: `${conv.contact_name} esta esperando resposta ha ${Math.round(conv.wait_ms / 60000)} minutos.`,
      severity: 'critical',
      metric: 'vipResponseTime',
      currentValue: conv.wait_ms,
      thresholdValue: maxWaitMs,
      metadata: { conversationId: conv.id, contactName: conv.contact_name, phone: conv.phone },
    });
  }
}
```

### 9.3 Alert Notification via WhatsApp

```typescript
async function sendAlertNotification(alert: AnalyticsAlert): Promise<void> {
  const config = await prisma.alertConfig.findUnique({
    where: { organizationId: alert.organizationId },
  });
  if (!config?.notifyWhatsApp || !config.notifyPhone) return;

  // Check quiet hours
  if (config.quietHoursStart && config.quietHoursEnd) {
    const now = format(new Date(), 'HH:mm');
    if (now >= config.quietHoursStart || now <= config.quietHoursEnd) {
      return; // Do not disturb
    }
  }

  // Deduplicate: only send if no similar alert was sent in last 2 hours
  const recentSimilar = await prisma.analyticsAlert.findFirst({
    where: {
      organizationId: alert.organizationId,
      alertType: alert.alertType,
      status: 'SENT',
      sentAt: { gte: subHours(new Date(), 2) },
    },
  });
  if (recentSimilar) return;

  // Send via Evolution API (same infrastructure as regular messages)
  await evolutionApi.sendText({
    instanceName: getOrgInstanceName(alert.organizationId),
    to: config.notifyPhone,
    text: `*[Tikso Analytics]*\n\n${alert.title}\n\n${alert.message}`,
  });

  await prisma.analyticsAlert.update({
    where: { id: alert.id },
    data: { status: 'SENT', sentAt: new Date() },
  });
}
```

---

## 10. Competitive Benchmark

### 10.1 What Competitors Show

| Platform | Key Analytics Features | Missing in Tikso |
|----------|----------------------|------------------|
| **HubSpot** | Revenue attribution by source, deal pipeline forecasting, activity reports per user, email open rates, meeting analytics | Pipeline forecasting, activity heatmaps |
| **Kommo (amoCRM)** | Pipeline conversion rates, lead response time, win/loss reasons, sales forecasting, team performance | Win/loss reason tracking |
| **Respond.io** | Message volume by channel, first response time, resolution time, CSAT scores, agent performance leaderboard | Agent leaderboard |
| **BotConversa** | Tag-based funnel tracking, sequence completion rates, broadcast delivery stats | Tag funnel visualization |
| **Zendesk** | Satisfaction scores, SLA compliance, ticket volumes, one-touch resolution rate | One-touch resolution rate |

### 10.2 What Business Owners Actually Value Most

Based on competitive analysis and SaaS churn research:

| Rank | Metric | Why Owners Care | Tikso Implementation |
|------|--------|-----------------|---------------------|
| 1 | **Monthly revenue** | "Am I making money?" | Hero card, month-over-month comparison |
| 2 | **Revenue from AI** | "Is the AI paying for itself?" | Dedicated card with % of total |
| 3 | **Appointments today** | "How busy am I?" | Real-time counter with AI attribution |
| 4 | **No-show rate** | "Am I losing money to no-shows?" | Trend chart with alert |
| 5 | **Response time** | "Are customers being served quickly?" | AI vs. Human comparison |
| 6 | **New vs. returning clients** | "Am I growing?" | Stacked bar chart |
| 7 | **Professional occupancy** | "Is my team productive?" | Percentage gauge per professional |
| 8 | **AI escalation rate** | "Is the AI working well?" | Trend line with threshold |

### 10.3 Tikso's Competitive Edge

What Tikso will have that competitors do not:

1. **AI Revenue Attribution** -- No competitor cleanly shows "AI generated R$X this month"
2. **WhatsApp-native alerts** -- HubSpot uses email; Tikso alerts via the same channel the owner already uses
3. **Integrated booking analytics** -- Competitors separate CRM analytics from appointment analytics; Tikso unifies them
4. **Sentiment-based NPS** -- No survey needed; inferred from AI conversation analysis
5. **Contact reactivation tracking** -- Shows how many churned customers the AI brought back

---

## 11. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal:** Schema migration and event pipeline

- [ ] Add new fields to existing models (`Message.isAiGenerated`, `Appointment.bookedBy`, etc.)
- [ ] Create `AnalyticsEvent`, `DailyMetrics`, `MonthlyMetrics` tables
- [ ] Create `AnalyticsAlert`, `AlertConfig` tables
- [ ] Write Prisma migration
- [ ] Implement event emission in existing code paths:
  - When a message is sent (AI or human) -> emit event
  - When an appointment is created -> emit event with attribution
  - When an order is completed -> emit event with revenue
  - When a contact is reactivated -> emit event
  - When AI escalates -> emit event
- [ ] Backfill historical DailyMetrics from existing data

**Files to create/modify:**
```
prisma/schema.prisma                           # Schema changes
prisma/migrations/XXXX_analytics_system/       # Migration
src/lib/analytics/event-emitter.ts             # Central event emission
src/lib/analytics/attribution.ts               # Attribution logic
```

### Phase 2: Aggregation (Week 2-3)

**Goal:** Background jobs computing metrics

- [ ] Implement `compute-daily-metrics` BullMQ job
- [ ] Implement `compute-monthly-metrics` BullMQ job
- [ ] Implement `backfill-daily-metrics` one-time job
- [ ] Add Redis caching layer
- [ ] Write unit tests for all metric computation functions
- [ ] Validate metrics against raw data (reconciliation checks)

**Files to create:**
```
src/jobs/analytics/compute-daily-metrics.ts
src/jobs/analytics/compute-monthly-metrics.ts
src/jobs/analytics/backfill.ts
src/lib/analytics/cache.ts
src/lib/analytics/metrics/revenue.ts
src/lib/analytics/metrics/appointments.ts
src/lib/analytics/metrics/messages.ts
src/lib/analytics/metrics/contacts.ts
src/lib/analytics/metrics/performance.ts
src/lib/analytics/metrics/satisfaction.ts
tests/analytics/                               # Test directory
```

### Phase 3: Dashboard API (Week 3-4)

**Goal:** REST/tRPC endpoints for frontend

- [ ] `/api/analytics/dashboard` -- composite dashboard endpoint
- [ ] `/api/analytics/revenue` -- revenue breakdown
- [ ] `/api/analytics/appointments` -- appointment metrics
- [ ] `/api/analytics/messages` -- message volume metrics
- [ ] `/api/analytics/contacts` -- contact lifecycle metrics
- [ ] `/api/analytics/pipeline` -- pipeline value metrics
- [ ] `/api/analytics/trends` -- 30-day trend data for charts
- [ ] `/api/analytics/top-clients` -- LTV leaderboard

**Files to create:**
```
src/app/api/analytics/dashboard/route.ts
src/app/api/analytics/revenue/route.ts
src/app/api/analytics/appointments/route.ts
src/app/api/analytics/messages/route.ts
src/app/api/analytics/contacts/route.ts
src/app/api/analytics/pipeline/route.ts
src/app/api/analytics/trends/route.ts
src/app/api/analytics/top-clients/route.ts
```

### Phase 4: Dashboard UI (Week 4-6)

**Goal:** React components for the analytics dashboard

- [ ] Dashboard page layout (`/dashboard/analytics`)
- [ ] Hero cards component (revenue, AI revenue)
- [ ] Appointment cards component
- [ ] Performance cards component (response time, AI messages)
- [ ] Trend charts (use existing chart library or add lightweight one)
- [ ] Period selector component
- [ ] Mobile-responsive layout

### Phase 5: Smart Alerts (Week 6-7)

**Goal:** Alert system with WhatsApp notifications

- [ ] Implement `check-alerts` BullMQ job
- [ ] Alert configuration UI (thresholds, notification preferences)
- [ ] WhatsApp notification sender (via Evolution API)
- [ ] Alert history and acknowledgment UI
- [ ] Deduplication logic

### Phase 6: Polish and Optimize (Week 7-8)

**Goal:** Performance tuning and edge cases

- [ ] Index optimization based on actual query patterns
- [ ] Load testing dashboard with realistic data volumes
- [ ] Add occupancy rate computation for service businesses
- [ ] Add LTV computation to monthly roll-up
- [ ] Error handling and graceful degradation
- [ ] Documentation for business owners

---

## 12. Migration Plan

### 12.1 Migration SQL (Prisma-Generated + Manual Indexes)

The migration will be generated by `prisma migrate dev` but here are the key DDL statements:

```sql
-- New enums
CREATE TYPE "MetricPeriod" AS ENUM ('DAILY', 'WEEKLY', 'MONTHLY');
CREATE TYPE "AttributionSource" AS ENUM ('AI_AGENT', 'AI_ASSISTED', 'HUMAN', 'FLOW', 'CAMPAIGN', 'ORGANIC');
CREATE TYPE "AlertType" AS ENUM ('REVENUE_MILESTONE', 'NO_SHOW_SPIKE', 'AI_FAILURE_SPIKE', 'VIP_WAITING', 'RESPONSE_TIME_HIGH', 'OCCUPANCY_LOW', 'REACTIVATION_WIN');
CREATE TYPE "AlertStatus" AS ENUM ('PENDING', 'SENT', 'ACKNOWLEDGED', 'DISMISSED');

-- Existing model additions (non-breaking, all nullable or with defaults)
ALTER TABLE "Message" ADD COLUMN "isAiGenerated" BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE "Message" ADD COLUMN "aiConfidence" DOUBLE PRECISION;

ALTER TABLE "Appointment" ADD COLUMN "bookedBy" "AttributionSource" NOT NULL DEFAULT 'ORGANIC';
ALTER TABLE "Appointment" ADD COLUMN "bookedVia" TEXT;

ALTER TABLE "Order" ADD COLUMN "attributionSource" "AttributionSource" NOT NULL DEFAULT 'ORGANIC';

ALTER TABLE "Conversation" ADD COLUMN "handledBy" "AttributionSource";

-- AnalyticsEvent table
CREATE TABLE "AnalyticsEvent" (
  "id" TEXT NOT NULL,
  "organizationId" TEXT NOT NULL,
  "eventType" TEXT NOT NULL,
  "eventCategory" TEXT NOT NULL,
  "contactId" TEXT,
  "conversationId" TEXT,
  "appointmentId" TEXT,
  "orderId" TEXT,
  "flowId" TEXT,
  "campaignId" TEXT,
  "userId" TEXT,
  "source" "AttributionSource" NOT NULL DEFAULT 'ORGANIC',
  "revenueAmount" DECIMAL(12,2),
  "numericValue" DOUBLE PRECISION,
  "metadata" JSONB,
  "occurredAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "AnalyticsEvent_pkey" PRIMARY KEY ("id")
);

-- DailyMetrics table (truncated for brevity -- Prisma generates the full DDL)
CREATE TABLE "DailyMetrics" (
  "id" TEXT NOT NULL,
  "organizationId" TEXT NOT NULL,
  "date" DATE NOT NULL,
  "totalRevenue" DECIMAL(12,2) NOT NULL DEFAULT 0,
  "aiRevenue" DECIMAL(12,2) NOT NULL DEFAULT 0,
  -- ... (all other columns from the Prisma model)
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMP(3) NOT NULL,
  CONSTRAINT "DailyMetrics_pkey" PRIMARY KEY ("id")
);

-- Unique and performance indexes
CREATE UNIQUE INDEX "DailyMetrics_organizationId_date_key"
  ON "DailyMetrics"("organizationId", "date");

CREATE INDEX "AnalyticsEvent_org_occurred"
  ON "AnalyticsEvent"("organizationId", "occurredAt");
CREATE INDEX "AnalyticsEvent_org_type_occurred"
  ON "AnalyticsEvent"("organizationId", "eventType", "occurredAt");
CREATE INDEX "AnalyticsEvent_org_category_occurred"
  ON "AnalyticsEvent"("organizationId", "eventCategory", "occurredAt");
CREATE INDEX "AnalyticsEvent_org_source_occurred"
  ON "AnalyticsEvent"("organizationId", "source", "occurredAt");

-- Foreign keys
ALTER TABLE "AnalyticsEvent"
  ADD CONSTRAINT "AnalyticsEvent_organizationId_fkey"
  FOREIGN KEY ("organizationId") REFERENCES "Organization"("id") ON DELETE CASCADE;

ALTER TABLE "DailyMetrics"
  ADD CONSTRAINT "DailyMetrics_organizationId_fkey"
  FOREIGN KEY ("organizationId") REFERENCES "Organization"("id") ON DELETE CASCADE;

-- Similar for MonthlyMetrics, AnalyticsAlert, AlertConfig
```

### 12.2 Rollback Plan

If the migration needs to be reversed:

```sql
-- Rollback: Drop new tables (no data loss in existing tables)
DROP TABLE IF EXISTS "AnalyticsAlert" CASCADE;
DROP TABLE IF EXISTS "AlertConfig" CASCADE;
DROP TABLE IF EXISTS "MonthlyMetrics" CASCADE;
DROP TABLE IF EXISTS "DailyMetrics" CASCADE;
DROP TABLE IF EXISTS "AnalyticsEvent" CASCADE;

-- Rollback: Remove new columns from existing tables
ALTER TABLE "Message" DROP COLUMN IF EXISTS "isAiGenerated";
ALTER TABLE "Message" DROP COLUMN IF EXISTS "aiConfidence";
ALTER TABLE "Appointment" DROP COLUMN IF EXISTS "bookedBy";
ALTER TABLE "Appointment" DROP COLUMN IF EXISTS "bookedVia";
ALTER TABLE "Order" DROP COLUMN IF EXISTS "attributionSource";
ALTER TABLE "Conversation" DROP COLUMN IF EXISTS "handledBy";

-- Rollback: Remove new enums
DROP TYPE IF EXISTS "AlertStatus";
DROP TYPE IF EXISTS "AlertType";
DROP TYPE IF EXISTS "AttributionSource";
DROP TYPE IF EXISTS "MetricPeriod";
```

### 12.3 Data Backfill Strategy

After migration, run a one-time backfill to:

1. **Set `Message.isAiGenerated`** by cross-referencing `AgentDecisionLog`:
```sql
UPDATE "Message" m
SET "isAiGenerated" = true
WHERE EXISTS (
  SELECT 1 FROM "AgentDecisionLog" adl
  WHERE adl."conversationId" = m."conversationId"
    AND adl.action = 'RESPOND'
    AND adl."createdAt" BETWEEN m."createdAt" - interval '5 seconds' AND m."createdAt" + interval '5 seconds'
)
AND m.direction = 'OUTBOUND';
```

2. **Set `Conversation.handledBy`** based on message analysis per conversation.

3. **Backfill `DailyMetrics`** for all historical days using the computation functions described in Section 8.

### 12.4 Zero-Downtime Deployment

1. Run `prisma migrate deploy` -- all new columns have defaults, so no lock issues
2. Deploy updated application code with event emission
3. Run backfill jobs in background (BullMQ)
4. Enable dashboard route once backfill completes
5. Enable alert jobs after verification

---

## Appendix A: Estimated Table Sizes

| Table | Rows/Month (per org, moderate usage) | Storage Notes |
|-------|--------------------------------------|---------------|
| `AnalyticsEvent` | ~5,000-20,000 | Append-only, partition by month after 6 months |
| `DailyMetrics` | 30 | One row per day per org |
| `MonthlyMetrics` | 1 | One row per month per org |
| `AnalyticsAlert` | ~10-50 | Low volume, auto-cleanup after 90 days |

For 100 organizations with moderate usage, expect:

- `AnalyticsEvent`: ~1-2M rows/month (manageable with indexes)
- `DailyMetrics`: ~3,000 rows/month
- `MonthlyMetrics`: ~100 rows/month

### Partition Strategy (Future)

If `AnalyticsEvent` grows beyond 10M rows, implement range partitioning:

```sql
-- Future: Partition AnalyticsEvent by month
CREATE TABLE "AnalyticsEvent" (
  ...
) PARTITION BY RANGE ("occurredAt");

CREATE TABLE "AnalyticsEvent_2026_01" PARTITION OF "AnalyticsEvent"
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

This is not needed at launch but should be planned for 6+ months of data.

---

## Appendix B: Redis Memory Estimation

Per organization with full dashboard cached:

| Cache Entry | Approximate Size | Count | Total |
|-------------|-----------------|-------|-------|
| Dashboard composite | ~5 KB | 1 | 5 KB |
| 30-day trend data | ~3 KB | 4 metrics | 12 KB |
| Pipeline by stage | ~1 KB | 1 | 1 KB |
| Top 50 LTV clients | ~5 KB | 1 | 5 KB |
| **Total per org** | | | **~23 KB** |

For 100 organizations: ~2.3 MB -- negligible Redis overhead.

---

## Appendix C: API Response Format

```typescript
// GET /api/analytics/dashboard?period=month
interface DashboardResponse {
  period: {
    type: 'day' | 'week' | 'month' | 'custom';
    start: string; // ISO date
    end: string;
  };
  revenue: {
    total: number;
    aiRevenue: number;
    humanRevenue: number;
    flowRevenue: number;
    campaignRevenue: number;
    aiPercentage: number;
    comparison: {
      previousTotal: number;
      changePercentage: number;
    };
  };
  appointments: {
    total: number;
    byAi: number;
    byHuman: number;
    completed: number;
    noShow: number;
    noShowRate: number;
    occupancyRate: number;
  };
  messages: {
    inbound: number;
    outboundAi: number;
    outboundHuman: number;
    outboundFlow: number;
    aiPercentage: number;
  };
  performance: {
    avgResponseTimeMs: number;
    avgAiResponseTimeMs: number;
    avgHumanResponseTimeMs: number;
    aiEscalations: number;
    aiConfidenceAvg: number;
  };
  contacts: {
    newContacts: number;
    returningContacts: number;
    reactivatedByAi: number;
    churnedContacts: number;
  };
  satisfaction: {
    sentimentAvg: number;       // -1 to 1
    qualityScoreAvg: number;    // 0 to 10
    estimatedNps: number;       // -100 to 100
  };
  pipeline: {
    totalValue: number;
    newValue: number;
    wonValue: number;
    stages: Array<{
      name: string;
      color: string;
      cardCount: number;
      totalValue: number;
    }>;
  };
  updatedAt: string; // ISO timestamp
}
```

---

*-- Dara, arquitetando dados*
