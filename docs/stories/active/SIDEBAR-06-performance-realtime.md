# Story SIDEBAR-06: Performance e Atualizacoes em Tempo Real

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-06
**Priority:** Could Have
**Points:** 5
**Effort:** ~8-12 horas
**Status:** Ready for Dev
**Type:** Feature — Backend + Frontend
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** SIDEBAR-01 (bugs corrigidos), SIDEBAR-02 (estrutura base)
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [manual-review, network-tab-inspection, realtime-test]
```

---

## User Story

**Como** atendente do Tikso CRM gerenciando multiplas conversas simultaneamente,
**Quero** que o painel de contato carregue mais rapido e mostre atualizacoes em tempo real de tags, notas e jornada,
**Para que** eu veja dados atualizados sem precisar reabrir a conversa e sem perceber atrasos ao trocar de contato.

---

## Acceptance Criteria

1. **AC1 — Batch de server actions:** Um novo server action `getSidebarData(orgId, conversationId)` busca dados de contato, jornada, notas internas, compromissos e insight em uma unica chamada ao servidor, substituindo as 4-6 chamadas independentes atuais. A autenticacao (`requireOrgAccess`) e executada uma unica vez.
2. **AC2 — Lazy load da secao Atividade:** A secao "Atividade" (sequencias, campanhas, campos customizados, pipeline) so busca os dados quando o usuario expande a secao, nao no carregamento inicial do painel. O `getContactDetails` e refatorado para excluir esses dados da consulta padrao.
3. **AC3 — Tempo real para tags:** Quando outro agente ou automacao adiciona ou remove uma tag do contato enquanto o painel esta aberto, a lista de tags no painel e atualizada automaticamente (via Centrifugo ou re-fetch). O usuario nao precisa reabrir a conversa.
4. **AC4 — Tempo real para notas:** Quando outro agente adiciona uma nota interna enquanto o painel esta aberto, a nova nota aparece na lista sem recarregar a pagina.
5. **AC5 — Error boundaries em componentes Centrifugo:** Os componentes que se inscrevem no Centrifugo (`ConversationInsight` e quaisquer novos assinantes) estao envoltos em `ErrorBoundary` React para que falhas de WebSocket nao quebrem o painel inteiro.
6. **AC6 — Sem regressoes de funcionalidade:** Todas as features existentes de tags, notas, jornada e compromissos continuam funcionando apos as mudancas de data fetching.

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** API + Frontend
**Secondary Type(s):** Real-time (Centrifugo), Performance
**Complexity:** High

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Implementacao de getSidebarData, lazy load e subscricoes Centrifugo

**Supporting Agents:**
- @qa: Verificacao de performance (network tab), teste de subscricoes em tempo real com dois usuarios simultaneos

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Confirmar que `getContactDetails` nao inclui dados de atividade na consulta padrao; grep para `sequenceEnrollments` e `campaignRecipients` no novo getContactDetails
- [ ] Pre-PR (@devops): Run `npm run lint && npm run typecheck`

### Self-Healing Configuration

**Expected Self-Healing:**
- Primary Agent: @dev (full mode)
- Max Iterations: 3
- Timeout: 30 minutos
- Severity Filter: CRITICAL e HIGH

**Predicted Behavior:**
- CRITICAL issues: auto_fix
- HIGH issues: auto_fix

### CodeRabbit Focus Areas

**Primary Focus:**
- Performance: auth() chamada apenas uma vez no getSidebarData (nao 4-6 vezes)
- Real-time: cleanup de subscricoes Centrifugo no return do useEffect

**Secondary Focus:**
- Error boundaries: envolvem apenas os componentes com subscricoes Centrifugo
- Lazy load: dados de atividade so carregados no evento onExpand da secao

---

## Tasks / Subtasks

- [ ] **Task 1: Criar `getSidebarData` server action** [AC: 1]
  - [ ] Abrir `src/app/(app)/[orgId]/inbox/actions.ts`
  - [ ] Criar novo server action `getSidebarData(orgId: string, conversationId: string)`:
    ```typescript
    "use server";
    export async function getSidebarData(orgId: string, conversationId: string) {
      const { member } = await requireOrgAccess(orgId); // 1x autenticacao
      const db = createTenantClient(orgId);

      const [contact, journeyInfo, internalNotes, commitments, insight] = await Promise.all([
        getContactDetailsInternal(db, conversationId),      // refatorado sem atividade
        getJourneyInfoInternal(db, conversationId),
        getInternalNotesInternal(db, conversationId),
        getCommitmentsInternal(db, conversationId),
        getConversationInsightInternal(db, conversationId),
      ]);

      return { contact, journeyInfo, internalNotes, commitments, insight };
    }
    ```
  - [ ] Extrair as queries internas das actions existentes como funcoes auxiliares privadas (prefixo `Internal` ou `_`)
  - [ ] Verificar que o tipo de retorno e completo para todas as secoes do painel
  - [ ] Atualizar o `InboxLayout` para chamar `getSidebarData` ao inves das 4 chamadas independentes

- [ ] **Task 2: Refatorar `getContactDetails` para excluir dados de atividade** [AC: 2]
  - [ ] Localizar em `src/app/(app)/[orgId]/inbox/actions.ts` a query `getContactDetails`
  - [ ] Remover os `include` de `sequenceEnrollments`, `campaignRecipients`, `pipelineCards` e `variableValues` da consulta padrao
  - [ ] Criar funcao separada `getContactActivityData(orgId, contactId)` que busca apenas esses dados
  - [ ] No `ContactPanel`, na secao `ActivitySubSections`, adicionar um `onExpandCallback`:
    ```typescript
    const [activityData, setActivityData] = useState<ActivityData | null>(null);
    const [isLoadingActivity, setIsLoadingActivity] = useState(false);

    const handleExpandActivity = async () => {
      if (activityData) return; // ja carregado
      setIsLoadingActivity(true);
      const data = await getContactActivityData(orgId, contact.id);
      setActivityData(data);
      setIsLoadingActivity(false);
    };
    ```
  - [ ] Passar `onExpand={handleExpandActivity}` para o `SectionHeader` da secao Atividade
  - [ ] Adicionar prop `onExpand?: () => void` ao `SectionHeader` se nao existir

- [ ] **Task 3: Subscricao Centrifugo para atualizacoes de tags** [AC: 3]
  - [ ] Inspecionar `src/hooks/use-realtime-inbox.ts` para entender os canais e eventos existentes
  - [ ] Verificar se existe evento `contact:tag:changed` ou `contact:updated` — se nao, documentar que o servidor precisa emitir esse evento (fora do escopo desta story se necessitar mudancas no backend)
  - [ ] Se o evento existir: adicionar subscricao no `InboxLayout` ou em hook dedicado:
    ```typescript
    // No handler de eventos Centrifugo do canal org:{orgId}
    case "contact:tag:changed":
      if (data.contactId === contact?.id) {
        // Re-fetch apenas as tags, ou atualizar via payload delta
        loadContactTags(orgId, data.contactId).then(setContactTags);
      }
      break;
    ```
  - [ ] [AUTO-DECISION] Se o evento Centrifugo nao existe: implementar re-fetch otimista quando o usuario retorna ao foco da aba (visibilitychange event) como alternativa ao tempo real completo. Documentar decisao.

- [ ] **Task 4: Subscricao Centrifugo para novas notas internas** [AC: 4]
  - [ ] Similar a Task 3, verificar existencia de evento `note:added` ou `internal_note:created` no canal `conversation:{conversationId}`
  - [ ] Se o evento existir: adicionar ao handler do `UnifiedNotesSection`:
    ```typescript
    // Ao receber note:added via Centrifugo
    setInternalNotes((prev) => [newNote, ...prev]);
    ```
  - [ ] Se o evento nao existir: implementar polling leve (a cada 30s quando o painel esta visivel) como fallback
  - [ ] [AUTO-DECISION] Polling de 30s e aceitavel para notas (nao e dado critico de tempo real). Subscricao Centrifugo e preferida se o canal ja existir.

- [ ] **Task 5: Adicionar ErrorBoundary nos componentes Centrifugo** [AC: 5]
  - [ ] Verificar se o projeto tem um componente `ErrorBoundary` reutilizavel — buscar em `src/components/` por `error-boundary` ou `ErrorBoundary`
  - [ ] Se nao existir, criar `src/components/ui/error-boundary.tsx`:
    ```typescript
    import React from "react";

    interface ErrorBoundaryProps {
      fallback?: React.ReactNode;
      children: React.ReactNode;
    }

    interface State {
      hasError: boolean;
    }

    export class ErrorBoundary extends React.Component<ErrorBoundaryProps, State> {
      state = { hasError: false };

      static getDerivedStateFromError() {
        return { hasError: true };
      }

      componentDidCatch(error: Error) {
        console.error("ErrorBoundary caught:", error);
      }

      render() {
        if (this.state.hasError) {
          return this.props.fallback ?? <div className="p-2 text-xs text-muted-foreground">Erro ao carregar componente.</div>;
        }
        return this.props.children;
      }
    }
    ```
  - [ ] Envolver `ConversationInsight` em `ErrorBoundary` no `contact-panel.tsx`
  - [ ] Envolver quaisquer novos componentes com subscricao Centrifugo (notas, tags) em `ErrorBoundary`

- [ ] **Task 6: Verificacao de performance e regressao** [AC: 6]
  - [ ] Abrir Chrome DevTools > Network > filtrar por "actions"
  - [ ] Trocar de conversa: verificar que apenas 1-2 chamadas de server action sao feitas (nao 6)
  - [ ] Expandir secao Atividade: verificar que a chamada `getContactActivityData` e feita apenas nesse momento
  - [ ] Trocar de conversa e voltar: verificar que o lazy load de atividade e reiniciado (nao usa dados da conversa anterior)
  - [ ] Testar funcionalidade completa: adicionar tag, remover tag, adicionar nota, alterar jornada, adicionar compromisso

---

## Dev Notes

### Contexto da Arquitetura Atual

O arquivo `src/app/(app)/[orgId]/inbox/actions.ts` tem **1821 linhas** e contem todas as server actions do inbox. O padrao atual de cada action independente:

```typescript
// Padrao atual (6x por troca de conversa)
export async function getInternalNotes(orgId, conversationId) {
  const { member } = await requireOrgAccess(orgId); // auth separada
  const db = createTenantClient(orgId);              // client separado
  return db.internalNote.findMany({ where: { conversationId }, include: { author: true } });
}
```

O `getSidebarData` unifica isso em uma chamada, com `Promise.all` para paralelismo das queries:

```typescript
export async function getSidebarData(orgId: string, conversationId: string) {
  const { member } = await requireOrgAccess(orgId); // 1x apenas
  const db = createTenantClient(orgId);             // 1x apenas

  const [contact, notes, commitments, insight, journey] = await Promise.all([
    db.contact.findFirst({ /* ... sem sequenceEnrollments etc */ }),
    db.internalNote.findMany({ where: { conversationId }, include: { author: true } }),
    // ... outras queries
  ]);

  return { contact, notes, commitments, insight, journey };
}
```

### Query de ContactDetails sem Atividade

A query atual de `getContactDetails` inclui 6 `include` clauses pesadas. Para o batch, usar apenas os dados necessarios para exibicao imediata:

```typescript
// Dados do contato SEM atividade (carregados no batch)
db.contact.findUnique({
  where: { id: resolvedContactId },
  include: {
    tags: { include: { tag: { select: { id: true, name: true, color: true } } } },
    leadScores: { orderBy: { lastCalculated: "desc" }, take: 1 },
    // REMOVIDOS: sequenceEnrollments, campaignRecipients, pipelineCards, variableValues
  },
});
```

Reducao estimada: de ~9 queries por troca de conversa para ~6 queries no batch (sem atividade).

### Centrifugo — Canais Existentes

Baseado no architecture audit:

- Canal `org:{orgId}`: eventos de organizacao (mensagens novas, atualizacoes de conversa)
- Canal `conversation:{selectedConversationId}`: eventos por conversa

O hook `useRealtimeInbox` em `src/hooks/use-realtime-inbox.ts` (~280 linhas) e o ponto central para adicionar novos handlers de eventos. Ler esse arquivo antes de implementar as Tasks 3 e 4.

Se os eventos `contact:tag:changed` e `note:added` nao existirem no servidor Centrifugo, a implementacao de tempo real completa requer mudancas no backend de publicacao (fora do escopo desta story). Nesse caso, implementar o fallback de re-fetch documentado nas Tasks 3 e 4.

### Sobre `SectionHeader.onExpand`

O lazy load da secao Atividade (Task 2) requer que o `SectionHeader` notifique o pai quando a secao e expandida pela primeira vez. Adicionar a prop:

```typescript
interface SectionHeaderProps {
  // ... props existentes
  onExpand?: () => void; // chamada na primeira vez que isOpen muda para true
}

// Dentro do SectionHeader:
const handleToggle = () => {
  const newIsOpen = !isOpen;
  setIsOpen(newIsOpen);
  if (newIsOpen && !hasExpanded) {
    setHasExpanded(true);
    onExpand?.();
  }
};
```

O flag `hasExpanded` evita chamar `onExpand` toda vez que o usuario fecha e reabre a secao.

### Gotcha: useEffect Cleanup para Subscricoes

Ao adicionar subscricoes Centrifugo, sempre usar o padrao com cleanup:

```typescript
useEffect(() => {
  if (!centrifugoClient || !conversationId) return;

  const sub = centrifugoClient.subscribe(`conversation:${conversationId}`, handler);

  return () => {
    sub.unsubscribe();
  };
}, [centrifugoClient, conversationId]);
```

Sem cleanup, subscricoes vazam ao trocar de conversa, acumulando handlers que disparam em conversas erradas.

### Testing

- **Tipo:** Teste de performance (network tab) + teste funcional + teste de tempo real (dois usuarios)
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios de teste:**
  - [ ] Network tab: trocar de conversa — contar chamadas server action (deve ser 1-2, nao 6)
  - [ ] Network tab: carregar painel sem expandir Atividade — confirmar que queries de sequencias/campanhas nao aparecem
  - [ ] Network tab: expandir Atividade — confirmar que `getContactActivityData` e chamada
  - [ ] Dois usuarios: usuario A abre painel, usuario B adiciona tag — usuario A ve a tag aparecer (ou re-fetch ao focar)
  - [ ] ErrorBoundary: simular erro no ConversationInsight (ex: passar prop invalida) — painel nao quebra
  - [ ] Todas as funcoes CRUD continuam funcionando: add tag, delete note (SIDEBAR-01), change journey

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada baseada no Architecture Audit do sidebar | @sm (River) |

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
| `src/app/(app)/[orgId]/inbox/actions.ts` | MODIFY — criar `getSidebarData`, refatorar `getContactDetails` sem atividade, criar `getContactActivityData` |
| `src/components/inbox/contact-panel.tsx` | MODIFY — usar dados do batch, lazy load de atividade, ErrorBoundary em componentes Centrifugo |
| `src/components/inbox/inbox-layout.tsx` | MODIFY — chamar `getSidebarData` ao inves das actions independentes |
| `src/components/contacts/shared/section-header.tsx` | MODIFY — adicionar prop `onExpand` para lazy load callback |
| `src/hooks/use-realtime-inbox.ts` | MODIFY — adicionar handlers para contact:tag:changed e note:added (se eventos existirem) |
| `src/components/ui/error-boundary.tsx` | CREATE — componente ErrorBoundary reutilizavel |

---

## QA Results

_A ser preenchido pelo agente de QA apos implementacao_
