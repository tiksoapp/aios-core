# Story TL-01: Política de Privacidade, Termos de Uso e Disclosure de IA

**Epic:** Tikso Launch (TL)
**Story ID:** TL-01
**Priority:** P0 — Bloqueia tudo (Must Have)
**Points:** 3
**Effort:** ~6 horas
**Status:** Ready for Dev
**Type:** Compliance / Feature — Frontend + Configuração
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** —
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [manual-review, visual-review]
```

---

## User Story

**Como** operador da plataforma Tikso,
**Quero** ter Política de Privacidade, Termos de Uso e disclosure de IA publicados e funcionais,
**Para que** a Tikso opere legalmente no Brasil sem risco de multa da ANPD (até R$50M) e sem violar as políticas da Meta/WhatsApp.

---

## Acceptance Criteria

1. **AC1 — Página de Política de Privacidade publicada:** Existe uma rota `/privacidade` (ou `/privacy`) no Next.js que renderiza a Política de Privacidade completa em PT-BR. O conteúdo cobre: quem somos, dados coletados, bases legais (LGPD), uso de IA, compartilhamento, transferência internacional, segurança, retenção, direitos dos titulares (SARR), e contato do DPO.

2. **AC2 — Página de Termos de Uso publicada:** Existe uma rota `/termos` (ou `/terms`) que renderiza os Termos de Uso completos em PT-BR. O conteúdo cobre: aceite, definições, serviços, obrigações do cliente, uso aceitável, cláusula de IA (Eli), propriedade intelectual, SLA 99.5%, pagamento, limitação de responsabilidade, rescisão, e foro.

3. **AC3 — Links acessíveis no footer do dashboard e na tela de login:** Footer do layout principal e a tela de login/signup exibem links para `/privacidade` e `/termos`. Links abrem nas próprias rotas (não em modal nem nova aba).

4. **AC4 — Disclosure de IA na primeira mensagem da Eli:** A primeira mensagem enviada pela Eli em qualquer nova conversa começa com identificação como assistente virtual. Formato mínimo: `"Olá! Sou a Eli, assistente virtual de [nome do negócio]. Posso ajudar com agendamentos, informações sobre serviços e muito mais. Se preferir falar com um atendente, é só digitar HUMANO."` — O texto exato pode ser configurável pelo dono, mas deve manter os elementos obrigatórios: identificação como IA, escopo, e caminho para humano.

5. **AC5 — Checkbox de aceite nos Termos no signup:** O fluxo de cadastro de novo cliente (empresa) inclui checkbox obrigatório não pré-marcado: `"Li e aceito os Termos de Uso e a Política de Privacidade"` com links para ambos. Não é possível completar o cadastro sem marcar.

---

## Tasks / Subtasks

- [ ] **Task 1: Criar páginas estáticas de Política e Termos** [AC: 1, 2]
  - [ ] Criar `/src/app/(public)/privacidade/page.tsx` usando o modelo do relatório jurídico `tikso-legal-compliance-framework.md` Seção 1.5
  - [ ] Criar `/src/app/(public)/termos/page.tsx` usando o modelo da Seção 1.6
  - [ ] Preencher campos `[DATA]`, `[Razão social]`, `[CNPJ]`, `[cidade sede]` com dados reais da Tikso — se não souber, usar placeholder visível `TODO: preencher antes de publicar`
  - [ ] Aplicar layout simples com `prose` do Tailwind (tipografia legível, sem sidebar do CRM)

- [ ] **Task 2: Links no footer e login** [AC: 3]
  - [ ] Localizar o componente de footer do dashboard (provavelmente em `src/components/layout/`)
  - [ ] Adicionar links `Política de Privacidade` e `Termos de Uso` com estilo muted/subtle
  - [ ] Repetir na tela de login/signup existente

- [ ] **Task 3: Disclosure de IA no prompt-builder** [AC: 4]
  - [ ] Em `/home/tikso/tikso/src/lib/ai/prompt-builder.ts`, localizar onde é definida a primeira mensagem de boas-vindas da Eli
  - [ ] Garantir que o sistema injete a mensagem de disclosure como a **primeira mensagem** em conversas novas (quando `isFirstMessage === true`)
  - [ ] O texto base deve ser armazenado em `OrgConfig` ou similar, com fallback para o texto padrão
  - [ ] Adicionar campo `aiDisclosureMessage` (string, opcional) na configuração da org para permitir customização pelo dono

- [ ] **Task 4: Checkbox de aceite no signup** [AC: 5]
  - [ ] Localizar o formulário de cadastro de nova organização
  - [ ] Adicionar campo `termsAccepted` (boolean) com validação `required`
  - [ ] Salvar timestamp de aceite (`termsAcceptedAt: DateTime`) no model `Organization` ou `User` via Prisma migration
  - [ ] Checkbox não pode ser pré-marcado — validação no frontend e no backend (API route)

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, Prisma 7.4, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivos-chave
```
src/app/(public)/privacidade/page.tsx         — CRIAR
src/app/(public)/termos/page.tsx              — CRIAR
src/components/layout/footer.tsx              — MODIFICAR (adicionar links)
src/app/(auth)/login/page.tsx                 — MODIFICAR (adicionar links)
src/app/(auth)/signup/page.tsx                — MODIFICAR (checkbox aceite)
src/lib/ai/prompt-builder.ts                  — MODIFICAR (disclosure primeira msg)
prisma/schema.prisma                          — MODIFICAR (campo termsAcceptedAt)
```

### Modelo de Disclosure (texto padrão)

```typescript
// Em prompt-builder.ts
const DEFAULT_AI_DISCLOSURE = (orgName: string) =>
  `Olá! Sou a Eli, assistente virtual de ${orgName}. ` +
  `Posso ajudar com agendamentos, dúvidas sobre serviços e muito mais. ` +
  `Se preferir falar com um atendente, é só digitar HUMANO.`;
```

### Rota pública

As páginas de Privacidade e Termos devem ser acessíveis SEM autenticação. Verificar se há middleware de auth que precise ser bypassado para `/privacidade` e `/termos`.

```typescript
// middleware.ts — adicionar à lista de rotas públicas
const publicRoutes = ['/login', '/signup', '/privacidade', '/termos'];
```

### Conteúdo das páginas

Os templates completos estão no relatório de origem:
- **Política de Privacidade:** `.aios-core/docs/research/tikso-legal-compliance-framework.md` — Seção 1.5
- **Termos de Uso:** `.aios-core/docs/research/tikso-legal-compliance-framework.md` — Seção 1.6

### Gotchas Relevantes
- Nunca usar `sed -i` com regex global em `.ts` — usar Python ou editor
- PM2 roda como user `tikso`: `su - tikso -c 'pm2 restart all'`
- Schema Prisma: após alterar, rodar `npx prisma migrate dev --name add-terms-accepted`

---

## Referência de Pesquisa

Originado em: `docs/research/tikso-legal-compliance-framework.md`
- Seção 1: LGPD — Bases legais, direitos dos titulares, obrigação de disclosure de IA
- Seção 1.5: Modelo completo de Política de Privacidade
- Seção 1.6: Modelo completo de Termos de Uso
- Seção 7.1: Checklist LGPD (itens: PP publicada, ToS publicado, disclosure IA)
- Prioridade P0 — Risco se ignorar: "Multa ANPD até R$50M"

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do framework jurídico da AIOS Legal Squad | @sm (River) |

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
| `src/app/(public)/privacidade/page.tsx` | CREATE — Política de Privacidade PT-BR |
| `src/app/(public)/termos/page.tsx` | CREATE — Termos de Uso PT-BR |
| `src/components/layout/footer.tsx` | MODIFY — adicionar links PP e ToS |
| `src/app/(auth)/login/page.tsx` | MODIFY — links PP e ToS |
| `src/app/(auth)/signup/page.tsx` | MODIFY — checkbox aceite obrigatório |
| `src/lib/ai/prompt-builder.ts` | MODIFY — disclosure AI primeira mensagem |
| `prisma/schema.prisma` | MODIFY — campo termsAcceptedAt |
| `prisma/migrations/...` | CREATE — migration termsAcceptedAt |
| `src/middleware.ts` | MODIFY — adicionar rotas públicas |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Frontend
  secondary: [Backend, Compliance]
  complexity: Medium

specialized_agents:
  primary: "@dev"
  secondary: ["@ux-expert"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - Páginas /privacidade e /termos acessíveis sem autenticação
      - Checkbox de aceite não pré-marcado e validado no backend
      - Disclosure de IA presente na primeira mensagem de nova conversa
      - Links no footer e login apontando para rotas corretas

  pre_pr:
    agent: "@github-devops"
    checks:
      - Nenhuma rota pública retorna 404
      - Conteúdo das páginas legais completo (não placeholder)

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - Acessibilidade de rotas públicas (sem auth redirect)
  - Conformidade do texto de disclosure (identificação como IA + caminho para humano)
  - Validação de formulário de aceite (checkbox required no frontend e backend)
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
