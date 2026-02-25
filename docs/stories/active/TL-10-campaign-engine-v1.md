# Story TL-10: Campaign Engine v1 — Broadcast Segmentado com Antiban

**Epic:** Tikso Launch (TL)
**Story ID:** TL-10
**Priority:** P2 — Sprint 2, aquisição de receita por campanha
**Points:** 13
**Effort:** ~3 dias
**Status:** Ready for Dev
**Type:** Feature — Backend + Frontend
**Sprint:** Sprint 2 — Tikso Launch Growth
**Lead:** @dev (Dex)
**Depends On:** TL-04, TL-05 (padrões de cron e BullMQ)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit-test, integration-test, manual-review, visual-review]
```

---

## User Story

**Como** dono de barbearia,
**Quero** enviar mensagens de marketing para segmentos da minha base de clientes (todos os clientes, inativos, aniversariantes) com proteção antiban automática,
**Para que** eu possa promover ofertas e trazer clientes de volta sem risco de ban e sem precisar enviar mensagem por mensagem manualmente.

---

## Acceptance Criteria

1. **AC1 — Interface de criação de campanha:** Existe uma rota `/campanhas/nova` com um formulário de 3 etapas: (a) Segmento: quem vai receber (todos os clientes, clientes inativos +30 dias, aniversariantes do mês, clientes VIP com 10+ agendamentos); (b) Mensagem: campo de texto com variáveis dinâmicas `{nome}`, `{serviço_preferido}`, `{barbeiro_favorito}`, preview em tempo real do texto final com dados do primeiro contato do segmento; (c) Agendamento: enviar agora ou agendar para uma data/hora específica.

2. **AC2 — Estimativa de alcance:** Na etapa de segmento, ao selecionar um segmento, o sistema exibe imediatamente (em < 2s) quantos contatos seriam alcançados: `"Este segmento alcança [N] contatos"`. Usa query COUNT do banco com os mesmos filtros que o envio real usará.

3. **AC3 — Mensagem usa variáveis dinâmicas:** O template de mensagem suporta as variáveis: `{nome}` (primeiro nome do contato), `{negocio}` (nome do negócio), `{barbeiro_favorito}` (nome do profissional do último agendamento, ou omitido se desconhecido). O preview mostra o texto com os dados do primeiro contato do segmento preenchidos.

4. **AC4 — Envio com antiban obrigatório:** O broadcast é enfileirado no BullMQ e enviado com: (a) intervalo mínimo de 10 segundos entre mensagens para destinatários diferentes, (b) jitter gaussiano de ±3s por mensagem, (c) pausa de 15 minutos a cada 50 mensagens enviadas, (d) respeito ao rate limit global da organização. Não envia para contatos com opt-out. O limite máximo por campanha é de 500 contatos (padrão — configurável por plano).

5. **AC5 — Tracking de status:** Cada campanha tem um painel de status em tempo real (polling a cada 10s): total de destinatários, enviados, entregues (delivery confirmed), com erro, e progresso em %. Uma campanha em andamento pode ser pausada ou cancelada.

6. **AC6 — Métricas pós-campanha:** 48 horas após o término de uma campanha, o sistema calcula e exibe: mensagens enviadas, taxa de resposta (% de destinatários que responderam), e agendamentos que vieram após a campanha (contatos que responderam e depois agendaram).

7. **AC7 — Listagem de campanhas:** A rota `/campanhas` lista todas as campanhas da organização com: nome da campanha (auto-gerado se não informado: "Campanha [data]"), segmento, data de envio, e status (Rascunho, Agendada, Em andamento, Concluída, Pausada, Cancelada).

8. **AC8 — Testes:** Mínimo 5 testes: seleção de segmento retorna COUNT correto, variáveis dinâmicas preenchidas corretamente, campanha respeitando limite de 500, job enfileirado corretamente no BullMQ, opt-out excluído do destinatário.

---

## Tasks / Subtasks

- [ ] **Task 1: Schema Prisma** [AC: 5, 7]
  - [ ] Verificar se o model `Campaign` já existe no schema Prisma
  - [ ] Se não existir, criar:
    ```prisma
    model Campaign {
      id              String    @id @default(cuid())
      organizationId  String
      name            String
      segment         String    // 'all' | 'inactive' | 'birthday' | 'vip'
      messageTemplate String
      scheduledAt     DateTime?
      startedAt       DateTime?
      completedAt     DateTime?
      status          String    @default("DRAFT") // DRAFT|SCHEDULED|RUNNING|PAUSED|COMPLETED|CANCELLED
      totalRecipients Int       @default(0)
      sentCount       Int       @default(0)
      deliveredCount  Int       @default(0)
      errorCount      Int       @default(0)
      responseCount   Int       @default(0)
      createdAt       DateTime  @default(now())
    }
    ```
  - [ ] Migration: `npx prisma migrate dev --name add-campaign-model`

- [ ] **Task 2: API — segmentos e estimativa de alcance** [AC: 2]
  - [ ] Criar `GET /api/campaigns/segments/:segment/count`
  - [ ] Implementar queries para cada segmento:
    - `all`: `Contact.count({ where: { organizationId, optOut: false } })`
    - `inactive`: `Contact.count({ where: { organizationId, optOut: false, lastAppointmentAt: { lt: subDays(now, 30) } } })`
    - `birthday`: `Contact.count({ where: { organizationId, optOut: false, birthDate: { month: currentMonth } } })`
    - `vip`: Contatos com 10+ agendamentos completed

- [ ] **Task 3: API — criar campanha** [AC: 1, 3, 4]
  - [ ] Criar `POST /api/campaigns` — recebe `{ segment, messageTemplate, scheduledAt? }`, valida, cria registro Campaign com status `DRAFT`
  - [ ] Criar `POST /api/campaigns/:id/send` — dispara o envio:
    - Busca todos os contatos do segmento (máx 500)
    - Para cada contato: resolve variáveis dinâmicas e enfileira job no BullMQ
    - Atualiza status para `RUNNING` e `totalRecipients`

- [ ] **Task 4: Job de envio com antiban** [AC: 4]
  - [ ] Criar `campaign-message-job.ts` no BullMQ
  - [ ] Configurar fila com delay programático (10s base + jitter gaussiano)
  - [ ] A cada 50 mensagens enviadas na mesma campanha: pausar a fila por 15 minutos (usar BullMQ `Queue.pause()` + setTimeout para resume)
  - [ ] Verificar opt-out antes de enviar
  - [ ] Após envio: atualizar `Campaign.sentCount`, registrar delivery status

- [ ] **Task 5: API — status em tempo real** [AC: 5]
  - [ ] Criar `GET /api/campaigns/:id/status` retornando métricas atuais da campanha
  - [ ] Criar `POST /api/campaigns/:id/pause` e `POST /api/campaigns/:id/cancel`

- [ ] **Task 6: API — métricas pós-campanha** [AC: 6]
  - [ ] Cron job diário (ou triggered 48h após término): calcular `responseCount` (contatos que responderam após o envio)
  - [ ] Calcular `bookingsAfterCampaign`: agendamentos de contatos que responderam, criados nos 7 dias após a campanha
  - [ ] Atualizar o registro da campanha com as métricas

- [ ] **Task 7: Frontend — formulário de criação** [AC: 1, 2, 3]
  - [ ] Criar `/src/app/(dashboard)/campanhas/nova/page.tsx`
  - [ ] Wizard de 3 etapas com `stepper` visual
  - [ ] Etapa 1: cards clicáveis para segmento, badge de "N contatos" atualizado em tempo real
  - [ ] Etapa 2: textarea com botões de inserção de variável (`{nome}`, `{negocio}`, etc.), preview ao lado
  - [ ] Etapa 3: dois botões: "Enviar agora" e "Agendar", datepicker se agendar

- [ ] **Task 8: Frontend — listagem e status** [AC: 5, 7]
  - [ ] Criar `/src/app/(dashboard)/campanhas/page.tsx` — tabela de campanhas com status badge
  - [ ] Criar `/src/app/(dashboard)/campanhas/[id]/page.tsx` — detalhe com progress bar + métricas

- [ ] **Task 9: Testes** [AC: 8]
  - [ ] `tests/unit/campaign-engine.test.ts` — mínimo 5 testes conforme AC8

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, BullMQ, Redis, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos de referência

```
src/lib/cron/antiban-cron.ts         — padrão de delays e jitter
src/lib/cron/reactivation-cron.ts    — padrão de seleção de contatos (TL-05)
src/app/(dashboard)/campanhas/       — verificar se existe implementação parcial
```

### Substituição de variáveis

```typescript
function interpolateMessage(
  template: string,
  contact: Contact & { preferredProfessional?: string }
): string {
  return template
    .replace(/\{nome\}/g, contact.name?.split(' ')[0] ?? 'você')
    .replace(/\{negocio\}/g, contact.organization?.name ?? 'nosso negócio')
    .replace(/\{barbeiro_favorito\}/g, contact.preferredProfessional ?? '');
}
```

### Configuração antiban para campanha

```typescript
// Delay entre mensagens: 10s base + jitter gaussiano ±3s
function calculateMessageDelay(index: number): number {
  const baseDelay = 10_000; // 10s
  const jitter = (Math.random() - 0.5) * 6_000; // ±3s
  const pauseAfterFifty = Math.floor(index / 50) * 15 * 60 * 1_000; // +15min a cada 50
  return baseDelay + jitter + pauseAfterFifty;
}

// BullMQ job com delay
await campaignQueue.add(
  'send-campaign-message',
  { campaignId, contactId, message },
  { delay: calculateMessageDelay(index), jobId: `campaign-${campaignId}-${contactId}` }
);
```

### Impacto esperado (do roadmap PM)

"Campanha bem-feita converte 3-8% dos contatos. Para base de 500 clientes, são 15-40 agendamentos extras = R$1.200-3.200 por campanha"

### Gotchas Relevantes
- BullMQ `Queue.pause()` pausa GLOBALMENTE — usar delay nos jobs ao invés de pause para não afetar outras filas
- Verificar se o model `Campaign` já existe (o schema tem 83+ models)
- Aniversariantes: `birthDate` pode ser null para contatos sem data de nascimento cadastrada
- Nunca usar `sed -i` com regex em `.ts`
- PM2 roda como user `tikso`
- Testar em horário comercial (não enviar campanhas de madrugada — adicionar verificação de horário)

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-product-strategy-roadmap.md` — Seção 4.5 "Campanhas de Marketing via WhatsApp" + Feature G3
  - "Impacto estimado: R$1.200-3.200 por campanha para base de 500 clientes"
- `docs/research/tikso-legal-compliance-framework.md` — Seção 3 "WhatsApp Business Compliance"
  - Opt-in requirements, anti-spam rules, template requirements
- `docs/research/tikso-multi-agent-architecture.md` — Seção 7 "Campaign Engine Architecture"
- `docs/research/whatsapp-antiban-best-practices.md` — delays e jitter para broadcasts

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do roadmap PM (Feature G3) e framework legal | @sm (River) |

---

## Dev Agent Record

### Agent Model Used
_A ser preenchido pelo agente de desenvolvimento_

### Debug Log References
_A ser preenchido pelo agente de desenvolvimento_

### Completion Notes List
_A ser preenchido pelo agente de desenvolvimento_

### File List

| Arquivo | Acao |
|---------|------|
| `src/app/(dashboard)/campanhas/page.tsx` | CREATE (ou MODIFY) |
| `src/app/(dashboard)/campanhas/nova/page.tsx` | CREATE |
| `src/app/(dashboard)/campanhas/[id]/page.tsx` | CREATE |
| `src/app/api/campaigns/route.ts` | CREATE |
| `src/app/api/campaigns/[id]/route.ts` | CREATE |
| `src/app/api/campaigns/[id]/send/route.ts` | CREATE |
| `src/app/api/campaigns/[id]/status/route.ts` | CREATE |
| `src/app/api/campaigns/segments/[segment]/count/route.ts` | CREATE |
| `src/lib/jobs/campaign-message-job.ts` | CREATE |
| `src/lib/utils/message-interpolation.ts` | CREATE |
| `prisma/schema.prisma` | MODIFY — Campaign model |
| `tests/unit/campaign-engine.test.ts` | CREATE |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Backend
  secondary: [Frontend, Database]
  complexity: Very High

specialized_agents:
  primary: "@dev"
  secondary: ["@db-sage", "@ux-expert"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - 5+ testes passando (conforme AC8)
      - Opt-out verificado ANTES de cada envio (nunca enviar para quem optou fora)
      - Limite de 500 destinatários respeitado
      - Delays antiban aplicados (10s base + jitter, pausa a cada 50)
      - Preview de mensagem com variáveis preenchidas funciona corretamente
      - Campanha pausável e cancelável

  pre_pr:
    agent: "@github-devops"
    checks:
      - jobId único por contato (não re-envia se job já na fila)
      - Migration Campaign sem conflitos
      - Verificar se model Campaign já existe antes de criar

self_healing:
  mode: full
  max_iterations: 3
  timeout_minutes: 30
  severity_threshold: HIGH

focus_areas:
  - Compliance WhatsApp: opt-out obrigatório, não enviar fora do horário comercial
  - Idempotência dos jobs de campanha
  - Performance da query de segmento COUNT (índices corretos)
  - Atomicidade: cancelamento interrompe todos os jobs pendentes da fila
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
