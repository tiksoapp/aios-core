# Story TL-03: Cloud API Migration Plan — Spike e Plano de Migração

**Epic:** Tikso Launch (TL)
**Story ID:** TL-03
**Priority:** P0 — Risco existencial (Evolution API viola ToS da Meta)
**Points:** 5
**Effort:** ~1.5 dias
**Status:** Ready for Dev
**Type:** Spike / Architecture — Backend
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** —
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [manual-review, architecture-review]
```

---

## User Story

**Como** time técnico da Tikso,
**Quero** um plano concreto e testado de migração da Evolution API (Baileys, não-oficial) para a WhatsApp Cloud API oficial da Meta,
**Para que** possamos eliminar o risco existencial de ban permanente do número de WhatsApp dos nossos clientes antes de escalar para 10+ clientes pagantes.

---

## Acceptance Criteria

1. **AC1 — Documento de análise de risco publicado:** Existe um arquivo `docs/architecture/cloud-api-migration-plan.md` com: (a) análise do risco atual (Evolution API + Baileys viola ToS da Meta), (b) comparação técnica Evolution API vs Cloud API (capacidades, limitações, custo por mensagem), (c) impacto por feature da Tikso (quais features dependem de API não-oficial e precisam de adaptação).

2. **AC2 — Prova de conceito (PoC) em ambiente de teste:** Um número de WhatsApp de teste está conectado à Cloud API oficial via conta Meta Business + BSP (Business Solution Provider). A PoC demonstra: envio de mensagem de texto, recebimento de webhook, e envio de template aprovado. O código da PoC está documentado no arquivo de migration plan.

3. **AC3 — Mapeamento de breaking changes:** O documento lista cada função do wrapper atual da Evolution API (`/src/lib/integrations/whatsapp/`) com o equivalente na Cloud API e flag `breaking: true/false`. Identifica os top 5 pontos de maior esforço de migração.

4. **AC4 — Estimativa de esforço e cronograma:** O documento inclui estimativa em dias de desenvolvimento para migração completa, breakdown por fase (fase 1: mensagens básicas; fase 2: media; fase 3: templates; fase 4: deprecar Evolution API), e recomendação de quando iniciar a migração baseada no risco atual.

5. **AC5 — BSP selecionado e credenciais de teste ativas:** Um BSP (Business Solution Provider) foi selecionado e avaliado (Twilio, 360dialog, ou Gupshup são os principais), conta de teste criada, e as credenciais estão documentadas no `.env.local` do ambiente de desenvolvimento (não commitadas).

---

## Tasks / Subtasks

- [ ] **Task 1: Análise do risco atual** [AC: 1]
  - [ ] Documentar como a Evolution API usa Baileys (protocolo WhatsApp não-oficial)
  - [ ] Levantar casos reais de ban de números usando Evolution API (pesquisa em GitHub/Reddit/grupos)
  - [ ] Mapear quais clientes atuais (ex: Trimmo) estão em risco imediato
  - [ ] Quantificar impacto de um ban: receita perdida, custo de recuperação (novo número, reconfiguração)

- [ ] **Task 2: Comparação técnica Evolution API vs Cloud API** [AC: 1, 3]
  - [ ] Listar capacidades da Evolution API atualmente usadas no codebase (grep em `src/lib/integrations/`)
  - [ ] Para cada capacidade, verificar se Cloud API tem equivalente e como implementar
  - [ ] Identificar features que NÃO têm equivalente (ex: ler mensagens de grupos, multi-device sem logout)
  - [ ] Calcular custo estimado de mensagens via Cloud API vs custo atual com Evolution API self-hosted

- [ ] **Task 3: Prova de Conceito Cloud API** [AC: 2, 5]
  - [ ] Criar conta Meta Business Manager com número de teste
  - [ ] Selecionar BSP: avaliar 360dialog (mais barato para BR) vs Twilio (mais confiável)
  - [ ] Configurar webhook receptor de teste (pode usar endpoint temporário ngrok ou `/api/whatsapp-test/`)
  - [ ] Implementar `sendMessage()` básico via Cloud API REST
  - [ ] Implementar handler de webhook de entrada
  - [ ] Testar envio de template (template deve ser aprovado pela Meta — usar template "hello_world" padrão)
  - [ ] Documentar o código da PoC no arquivo de migration plan

- [ ] **Task 4: Mapeamento de breaking changes** [AC: 3]
  - [ ] Criar tabela: `| Função | Arquivo | Cloud API equivalente | Breaking? | Esforço (h) |`
  - [ ] Priorizar top 5 por criticidade + esforço
  - [ ] Identificar se há funções usadas pela Eli que não têm equivalente direto

- [ ] **Task 5: Documento final e cronograma** [AC: 4]
  - [ ] Criar `docs/architecture/cloud-api-migration-plan.md`
  - [ ] Incluir: sumário executivo, análise de risco, comparação técnica, PoC results, breaking changes, cronograma
  - [ ] Recomendar: migrar mensagens críticas (lembretes, confirmações) para Cloud API em Q2, manter Evolution para conversas reativas até Q3

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`
- **API atual:** Evolution API v2.3.7 (patched), modo Baileys

### Arquivos relevantes para análise

```
src/lib/integrations/whatsapp/           — ANALISAR (wrapper atual da Evolution API)
src/lib/integrations/providers/          — ANALISAR (providers que usam WhatsApp)
src/app/api/webhook/                     — ANALISAR (handlers de webhook)
```

### BSPs recomendados para avaliar

```
360dialog:  https://www.360dialog.com/pricing
            - Pricing: a partir de €79/mo + custo por mensagem da Meta
            - Vantagem: preço mais acessível, suporte em português
            - Desvantagem: menos features enterprise

Twilio:     https://www.twilio.com/en-us/whatsapp/pricing
            - Pricing: US$0 setup + custo por mensagem Meta
            - Vantagem: documentação excelente, SDK Node.js robusto
            - Desvantagem: custo pode escalar

Gupshup:    https://www.gupshup.io/pricing
            - Vantagem: muito usado no Brasil, suporte PT-BR
```

### Estrutura do documento de saída

```markdown
# Cloud API Migration Plan

## 1. Sumário Executivo (risco atual + recomendação)
## 2. Análise de Risco (Evolution API + casos reais de ban)
## 3. Comparação Técnica (tabela de capacidades)
## 4. Breaking Changes (tabela por função)
## 5. Prova de Conceito (código + resultados)
## 6. Estimativa de Esforço (por fase)
## 7. Cronograma Recomendado
## 8. BSP Selecionado e Configuração
```

### Referência de risco do relatório de segurança

Do `tikso-security-blueprint.md`:
> "CRITICAL — Evolution API (Baileys) violates Meta ToS — risk of permanent bans — Business continuity"

Do `tikso-product-strategy-roadmap.md` Risco R1:
> "Ban do WhatsApp por uso de API não-oficial: Probabilidade ALTA (30-50% em 3 meses por número)"

### Gotchas Relevantes
- A PoC precisa de um número de telefone real para registrar no Meta Business
- Templates da Meta levam 24-72h para aprovação — iniciar imediatamente
- Cloud API cobra por mensagem (não conversa) desde Jul/2025 — calcular custo com cuidado

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-product-strategy-roadmap.md` — Seção 8 Risco R1 "Ban do WhatsApp" + Seção 3 Feature S2 "WhatsApp Cloud API (oficial)"
- `docs/research/tikso-security-blueprint.md` — Seção 1 Critical Findings (Evolution API + Baileys)
- `docs/research/tikso-legal-compliance-framework.md` — Seção 3.1 "ALERTA CRÍTICO: Ban de Chatbots Genéricos (Jan 2026)"

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada — spike de arquitetura para mitigação de risco existencial | @sm (River) |

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
| `docs/architecture/cloud-api-migration-plan.md` | CREATE — documento principal |
| `src/app/api/whatsapp-test/route.ts` | CREATE — endpoint PoC (remover após teste) |
| `.env.local` | MODIFY — credenciais BSP (não commitar) |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Architecture
  secondary: [Backend]
  complexity: Medium

specialized_agents:
  primary: "@dev"
  secondary: ["@architect"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Documento docs/architecture/cloud-api-migration-plan.md criado e completo
      - PoC Cloud API envia e recebe mensagem com sucesso (evidência nos resultados da PoC)
      - Credenciais BSP em .env.local (não commitadas)
      - Endpoint de teste /api/whatsapp-test/ marcado para remoção

  pre_pr:
    agent: "@github-devops"
    checks:
      - .env.local não incluído no commit
      - Nenhuma credencial hardcoded no código da PoC

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Segurança: credentials não commitadas
  - Completude do documento de análise (todos os 8 itens da estrutura)
  - Viabilidade técnica da PoC confirmada com evidências
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
