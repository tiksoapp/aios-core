# Story TL-07: Onboarding Wizard v2 — 10 Minutos até o Primeiro Valor

**Epic:** Tikso Launch (TL)
**Story ID:** TL-07
**Priority:** P1 — Sprint 1, converte trial em pago
**Points:** 8
**Effort:** ~2 dias
**Status:** Ready for Dev
**Type:** Feature — Frontend + Backend
**Sprint:** Sprint 1 — Tikso Launch Foundation
**Lead:** @dev (Dex)
**Depends On:** ELI-01, ELI-04 (tom de voz)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit-test, manual-review, visual-review]
```

---

## User Story

**Como** dono de barbearia que acabou de criar conta na Tikso,
**Quero** um wizard de configuração guiado que me configure em menos de 10 minutos e mostre a Eli respondendo de verdade antes de terminar,
**Para que** eu tenha o "momento aha" — ver a IA funcionando ao vivo — e me convença a continuar usando a ferramenta.

---

## Acceptance Criteria

1. **AC1 — Etapa 3: Configuração da Eli (complementa etapas existentes):** O wizard exibe uma nova etapa "Configurar a Eli" após a conexão do WhatsApp. A etapa tem: (a) seletor de tom de voz com 3 opções — "Amigável" (padrão), "Formal", "Descontraído" — com preview de como a Eli vai falar em cada tom, (b) campo de horário de atendimento (início e fim, padrão 08:00-20:00), (c) checkboxes de capacidades: "Agendar horários" (marcado), "Responder dúvidas sobre serviços" (marcado), "Enviar catálogo de produtos" (desmarcado), e (d) botão "Salvar e Continuar".

2. **AC2 — Etapa 4: Adicionar serviços:** O wizard exibe uma etapa "Seus Serviços" com uma lista de serviços padrão pré-preenchidos para o segmento selecionado na Etapa 1 (ex: para barbearia: "Corte Masculino R$45 30min", "Barba R$30 20min", "Corte + Barba R$65 50min"). O dono pode: editar o preço e duração inline, excluir serviços, e adicionar novos via botão `[+ Adicionar serviço]`. Ao avançar, os serviços são salvos na tabela `Service`.

3. **AC3 — Etapa 5: "Teste a Eli Agora!" — o momento aha:** O wizard exibe uma etapa final com um número de WhatsApp de teste (o número conectado da organização). O texto instrui: "Envie 'Oi' para este número agora de outro celular e veja a Eli responder!" — Abaixo, um painel em tempo real (polling ou WebSocket) exibe as últimas mensagens trocadas com aquele número, atualizando ao vivo à medida que o dono testa. Quando a Eli responde ao teste, o botão "Ir para o Dashboard" fica ativo e exibe `"Perfeito! A Eli está funcionando! 🎉"`.

4. **AC4 — Progresso salvo:** O progresso do wizard é salvo incrementalmente. Se o dono sair e voltar, retoma da etapa onde parou. Campo `onboardingStep: Int @default(0)` na tabela `Organization`.

5. **AC5 — Checklist na sidebar:** Após o wizard, a sidebar exibe um checklist de onboarding persistente com 7 itens: "Criar conta", "Conectar WhatsApp", "Configurar Eli", "Adicionar serviços", "Testar Eli", "Adicionar equipe" e "Configurar horários". Itens 1-5 são marcados automaticamente ao completar o wizard. O checklist some da sidebar após todos os 7 estarem completos.

6. **AC6 — Tempo medido:** O sistema registra `onboardingStartedAt` e `onboardingCompletedAt` na tabela `Organization`. Esses campos alimentam a métrica interna "Tempo até primeiro valor" (North Star KPI).

7. **AC7 — Testes:** Mínimo 3 testes: dados de serviços pré-preenchidos corretos por segmento (barbearia → 3 serviços padrão), salvamento de OrgConfig com tom de voz, e flag `onboardingCompleted` setado ao finalizar o wizard.

---

## Tasks / Subtasks

- [ ] **Task 1: Schema Prisma** [AC: 4, 6]
  - [ ] Adicionar ao model `Organization`: `onboardingStep Int @default(0)`, `onboardingStartedAt DateTime?`, `onboardingCompletedAt DateTime?`
  - [ ] Adicionar ao model `OrgConfig`: `voiceTone String @default('friendly')`, `supportHoursStart String @default('08:00')`, `supportHoursEnd String @default('20:00')`
  - [ ] Migration: `npx prisma migrate dev --name add-onboarding-progress`

- [ ] **Task 2: Etapa 3 — Configuração da Eli** [AC: 1]
  - [ ] Criar `/src/components/onboarding/eli-config-step.tsx`
  - [ ] 3 opções de tom com cards clicáveis (não radio button), cada card mostra preview de mensagem no estilo daquele tom
  - [ ] Campos de horário: dois `<input type="time">` com labels "Das" e "Até"
  - [ ] Checkboxes de capacidades com descrições em linguagem simples (não técnica)
  - [ ] Submit: `PATCH /api/org/config` com `{ voiceTone, supportHoursStart, supportHoursEnd, capabilities }`

- [ ] **Task 3: Etapa 4 — Serviços** [AC: 2]
  - [ ] Criar `/src/components/onboarding/service-catalog-step.tsx`
  - [ ] Dados pré-preenchidos por segmento: criar constante `DEFAULT_SERVICES_BY_SEGMENT` com serviços para barbearia, salão, clínica estética
  - [ ] Cada serviço no formulário: nome (text), preço (number, formato BRL), duração em minutos (number)
  - [ ] Edição inline: clicar no campo para editar in-place
  - [ ] Adicionar serviço: formulário inline no final da lista (não modal)
  - [ ] Submit: `POST /api/services/batch` criando todos os serviços de uma vez

- [ ] **Task 4: Etapa 5 — Teste ao vivo** [AC: 3]
  - [ ] Criar `/src/components/onboarding/test-eli-step.tsx`
  - [ ] Exibir o número de WhatsApp da org em formato grande e legível com botão "Copiar número"
  - [ ] Polling de mensagens recentes: `GET /api/conversations/recent?limit=5` a cada 3 segundos
  - [ ] Exibir thread de mensagens estilo WhatsApp (reutilizar componente de chat existente ou simplificado)
  - [ ] Quando `messages.length > 0 && hasAiReply === true`: mostrar mensagem de sucesso e ativar botão "Ir para o Dashboard"
  - [ ] Botão "Ir para o Dashboard" sempre visível (mas disabled até ter resposta da Eli), com link de escape "Pular e ir para o Dashboard"

- [ ] **Task 5: Integrar etapas no wizard existente** [AC: 4]
  - [ ] Localizar `/src/components/onboarding/onboarding-wizard.tsx`
  - [ ] Adicionar as 3 novas etapas após a etapa 2 (WhatsApp QR)
  - [ ] Salvar `onboardingStep` a cada etapa via `PATCH /api/org`
  - [ ] Ao completar: salvar `onboardingCompletedAt = now()`, redirecionar para dashboard

- [ ] **Task 6: Checklist na sidebar** [AC: 5]
  - [ ] Localizar/criar componente `SidebarChecklist` na sidebar
  - [ ] Buscar status dos 7 itens via `GET /api/org/onboarding-checklist`
  - [ ] API retorna: `{ items: [{ label, completed, key }] }`
  - [ ] Lógica de completude: "Criar conta" = user existe, "Conectar WhatsApp" = `whatsappConnected`, "Configurar Eli" = `onboardingStep >= 3`, etc.
  - [ ] Esconder checklist quando todos os 7 estão completos (`completedCount === 7`)

- [ ] **Task 7: Testes** [AC: 7]
  - [ ] `tests/unit/onboarding-defaults.test.ts`: verificar `DEFAULT_SERVICES_BY_SEGMENT['barbershop']` retorna 3 serviços com name, price, duration
  - [ ] Teste de OrgConfig: voiceTone salvo corretamente
  - [ ] Teste de `onboardingCompletedAt` setado ao finalizar

---

## Dev Notes

### Stack e Contexto
- **Projeto:** Tikso CRM, Next.js 16, React 19, Prisma 7.4, Tailwind v4, shadcn/ui
- **Servidor:** SSH alias `vultr`, path `/home/tikso/tikso/`

### Arquivo existente a verificar

```
src/components/onboarding/onboarding-wizard.tsx   — MODIFICAR (adicionar etapas 3, 4, 5)
src/app/(dashboard)/settings/general/             — referência para padrão de formulários de config
```

### Serviços padrão por segmento

```typescript
const DEFAULT_SERVICES_BY_SEGMENT: Record<string, ServiceTemplate[]> = {
  barbershop: [
    { name: 'Corte Masculino', price: 45, durationMinutes: 30 },
    { name: 'Barba', price: 30, durationMinutes: 20 },
    { name: 'Corte + Barba', price: 65, durationMinutes: 50 },
  ],
  salon: [
    { name: 'Corte Feminino', price: 80, durationMinutes: 60 },
    { name: 'Escova', price: 70, durationMinutes: 45 },
    { name: 'Coloração', price: 150, durationMinutes: 120 },
  ],
  aesthetic: [
    { name: 'Limpeza de Pele', price: 120, durationMinutes: 60 },
    { name: 'Depilação Corporal', price: 80, durationMinutes: 45 },
    { name: 'Manicure + Pedicure', price: 90, durationMinutes: 90 },
  ],
};
```

### Preview de ton de voz

```typescript
const VOICE_TONE_PREVIEWS = {
  friendly: '"Oi! Que bom te ver por aqui! 😊 Quando você quer marcar?"',
  formal: '"Olá! Fico à disposição para auxiliá-lo com seu agendamento."',
  casual: '"E aí! Bora marcar um horário? Quando fica bom pra você?"',
};
```

### Polling para live preview

```typescript
useEffect(() => {
  const interval = setInterval(async () => {
    const res = await fetch('/api/conversations/recent?limit=5');
    const { messages } = await res.json();
    setMessages(messages);
    const hasAiReply = messages.some(m => m.direction === 'OUTBOUND' && m.isAi);
    if (hasAiReply) setEliResponded(true);
  }, 3000);
  return () => clearInterval(interval);
}, []);
```

### Referência de UX

Conforme `docs/research/tikso-ux-redesign-proposal.md` Seção 7 "Onboarding Experience":
- Step 3: Configuração da Eli (tom de voz, horários, capacidades)
- Step 4: Serviços (lista editável)
- Step 5: Teste ao vivo ("Aha moment")
- Meta: 10 minutos até primeiro valor, cliente VÊ a Eli funcionando

### Gotchas Relevantes
- Nunca usar `sed -i` com regex em `.ts`
- PM2 roda como user `tikso`
- O polling de 3s é aceitável para demo; em produção considerar WebSocket (já disponível via Centrifugo)
- `<input type="time">` tem comportamento diferente em iOS Safari — testar em mobile

---

## Referência de Pesquisa

Originado em:
- `docs/research/tikso-product-strategy-roadmap.md` — Feature F9 "Onboarding wizard — setup guiado em 15 min"
- `docs/research/tikso-ux-redesign-proposal.md` — Seção 7 "Onboarding Experience" completa
  - Seção 7.4: "First-Value Timeline" — meta de 10 minutos
  - Seção 10.3: novos componentes `EliConfigStep`, `ServiceCatalogStep`, `TestEliStep`

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada a partir do UX Redesign Proposal e Product Roadmap (Feature F9) | @sm (River) |

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
| `src/components/onboarding/eli-config-step.tsx` | CREATE |
| `src/components/onboarding/service-catalog-step.tsx` | CREATE |
| `src/components/onboarding/test-eli-step.tsx` | CREATE |
| `src/components/onboarding/onboarding-wizard.tsx` | MODIFY — adicionar etapas 3, 4, 5 |
| `src/components/layout/sidebar-checklist.tsx` | CREATE (ou MODIFY) |
| `src/app/api/org/onboarding-checklist/route.ts` | CREATE |
| `src/app/api/services/batch/route.ts` | CREATE |
| `src/lib/constants/default-services.ts` | CREATE |
| `prisma/schema.prisma` | MODIFY — onboardingStep + voiceTone + supportHours |
| `tests/unit/onboarding-defaults.test.ts` | CREATE |

---

## CodeRabbit Integration

```yaml
story_type:
  primary: Frontend
  secondary: [Backend, Database]
  complexity: High

specialized_agents:
  primary: "@dev"
  secondary: ["@ux-expert", "@db-sage"]

quality_gates:
  pre_commit:
    agent: "@dev"
    checks:
      - 3 testes passando (serviços padrão por segmento, voiceTone salvo, onboardingCompleted)
      - Live preview da Eli na Etapa 5 atualiza em tempo real (polling funciona)
      - Checklist na sidebar reflete progresso corretamente
      - Progresso salvo ao navegar entre etapas (onboardingStep persistido)
      - Retoma da etapa correta ao voltar ao wizard

  pre_pr:
    agent: "@github-devops"
    checks:
      - Migration sem conflitos
      - <input type="time"> testado em iOS Safari (comportamento diferente)

self_healing:
  mode: light
  max_iterations: 2
  timeout_minutes: 15
  severity_threshold: CRITICAL

focus_areas:
  - UX do "momento aha" (Etapa 5 deve ser visualmente clara e responsiva)
  - Mobile compatibility do wizard (donos usam celular)
  - Segurança do polling (não vazar conversas de outras orgs)
```

---

## QA Results

_A ser preenchido pelo agente de QA após implementação_
