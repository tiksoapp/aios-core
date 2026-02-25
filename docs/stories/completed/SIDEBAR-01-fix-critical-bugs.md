# Story SIDEBAR-01: Corrigir Bugs Criticos do Painel de Contato

**Epic:** SIDEBAR — Contact Detail Panel Redesign
**Story ID:** SIDEBAR-01
**Priority:** Must Have
**Points:** 3
**Effort:** ~4 horas
**Status:** Done
**Type:** Bug Fix — Backend + Frontend
**Sprint:** Sprint SIDEBAR
**Lead:** @dev (Dex)
**Depends On:** —
**Repository:** tikso (Vultr: `/home/tikso/tikso/`)

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [manual-review, api-test, permission-test]
```

---

## User Story

**Como** atendente do Tikso CRM,
**Quero** que as funcoes basicas do painel lateral (excluir notas, editar nome, alterar jornada) funcionem corretamente,
**Para que** eu possa realizar meu trabalho sem encontrar erros silenciosos ou comportamentos inesperados.

---

## Acceptance Criteria

1. **AC1 — DELETE de notas funciona:** O botao de excluir nota interna (icone de lixeira) exclui a nota do banco de dados e remove do estado da UI sem erro. O endpoint `DELETE /api/inbox/notes?noteId={id}` retorna 200 com o registro excluido.
2. **AC2 — Autorizacao no DELETE:** Somente o autor da nota ou um membro com permissao de admin pode excluir. Tentativas nao autorizadas retornam 403.
3. **AC3 — Nome atualiza sem mutacao direta:** Apos editar o nome do contato no `ProfileHeader`, o valor atualizado e propagado via `setContact` no `InboxLayout` (spread imutavel). O `ContactInfoCard` abaixo no painel exibe o novo nome imediatamente sem necessidade de recarregar.
4. **AC4 — Journey acessivel por agentes liveChat:** Um usuario com permissao `"liveChat"` consegue alterar o estado de jornada de um contato sem receber erro 403. O `updateJourneyState` deve aceitar `"liveChat"` OU `"integrations"`.
5. **AC5 — Sem regressoes:** As funcionalidades existentes de adicionar notas, editar nome e exibir jornada continuam funcionando corretamente apos as correcoes.

---

## CodeRabbit Integration

### Story Type Analysis

**Primary Type:** API + Frontend
**Secondary Type(s):** Security (autorizacao)
**Complexity:** Medium

### Specialized Agent Assignment

**Primary Agents:**
- @dev: Implementacao das tres correcoes

**Supporting Agents:**
- @qa: Teste de permissao (BUG-003) e teste funcional de exclusao (BUG-001)

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Confirmar que nenhuma mutacao direta de prop permanece no componente
- [ ] Pre-PR (@devops): Run `npm run lint && npm run typecheck` no servidor Vultr

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
- Security: Verificar que o handler DELETE valida auth, tenant e autorizacao de autor/admin
- State management: Confirmar uso de spread imutavel em todos os callbacks de atualizacao de contato

**Secondary Focus:**
- Permission model: assertMemberPermission aceita `"liveChat"` para updateJourneyState
- Error handling: Respostas de erro consistentes (404 nota nao encontrada, 403 nao autorizado)

---

## Tasks / Subtasks

- [ ] **Task 1: BUG-001 — Adicionar handler DELETE em `/api/inbox/notes/route.ts`** [AC: 1, 2]
  - [ ] Abrir `src/app/api/inbox/notes/route.ts` e inspecionar os handlers existentes (POST, GET)
  - [ ] Adicionar funcao `export async function DELETE(request: NextRequest)`
  - [ ] Extrair `noteId` de `request.nextUrl.searchParams.get("noteId")` — validar presenca
  - [ ] Chamar `requireOrgAccess(orgId)` para autenticacao e resolucao de tenant (obter `orgId` do header ou context)
  - [ ] Criar `createTenantClient(orgId)` e buscar a nota pelo `noteId`
  - [ ] Verificar se `note.authorId === session.user.id` OU se o membro tem permissao admin — retornar 403 caso contrario
  - [ ] Executar `db.internalNote.delete({ where: { id: noteId } })`
  - [ ] Retornar `NextResponse.json({ success: true, id: noteId })` com status 200
  - [ ] Tratar nota nao encontrada: retornar 404

- [ ] **Task 2: BUG-002 — Corrigir mutacao direta em `onNameUpdated`** [AC: 3]
  - [ ] Abrir `src/components/inbox/contact-panel.tsx` e localizar linha ~149
  - [ ] Localizar o callback `onNameUpdated` passado ao `ProfileHeader`
  - [ ] Substituir `if (contact) contact.name = newName;` por chamada ao setter do pai
  - [ ] Em `InboxLayout`, adicionar (ou confirmar existencia de) callback `handleContactNameUpdated`:
    ```typescript
    const handleContactNameUpdated = useCallback((newName: string) => {
      setContact((prev) => prev ? { ...prev, name: newName } : null);
    }, []);
    ```
  - [ ] Passar `onNameUpdated={handleContactNameUpdated}` para `ContactPanel` via `InboxLayout`
  - [ ] Verificar que `ContactPanel` repassa para `ProfileHeader` sem mutacao

- [ ] **Task 3: BUG-003 — Corrigir permissao em `updateJourneyState`** [AC: 4]
  - [ ] Abrir `src/app/(app)/[orgId]/ai/actions.ts` e localizar linha ~351
  - [ ] Localizar `assertMemberPermission(member, "integrations")`
  - [ ] Avaliar a politica correta: se agentes de liveChat devem alterar jornada, substituir por `"liveChat"`
  - [ ] Alternativa mais conservadora: criar verificacao dupla — aceitar `"liveChat"` OU `"integrations"`:
    ```typescript
    const hasPermission =
      member.permissions.includes("liveChat") ||
      member.permissions.includes("integrations");
    if (!hasPermission) throw new Error("Forbidden");
    ```
  - [ ] Confirmar que a mudanca nao afeta outras chamadas a `updateJourneyState` (buscar por usages)

- [ ] **Task 4: Teste manual das tres correcoes** [AC: 5]
  - [ ] Testar exclusao de nota: criar nota, clicar lixeira, confirmar remocao da UI e do banco
  - [ ] Testar nota de outro usuario: confirmar que tentativa de exclusao retorna erro toast (nao remove)
  - [ ] Testar edicao de nome: editar nome, confirmar que `ContactInfoCard` abaixo atualiza imediatamente
  - [ ] Testar jornada com usuario liveChat: confirmar que "Alterar" funciona sem erro 403

---

## Dev Notes

### Contexto do Bug BUG-001 (DELETE de notas)

O arquivo `src/app/api/inbox/notes/route.ts` exporta apenas `POST` (criar nota) e `GET` (listar notas). O componente `UnifiedNotesSection` dentro de `contact-panel.tsx` (linha ~1040) ja tem o codigo de delete corretamente implementado no frontend:

```typescript
const handleDeleteNote = React.useCallback(async (noteId: string) => {
  try {
    const res = await fetch(`/api/inbox/notes?noteId=${noteId}`, { method: "DELETE" });
    if (res.ok) {
      setInternalNotes((prev) => prev.filter((n) => n.id !== noteId));
    } else {
      throw new Error("Failed");
    }
  } catch {
    toast.error("Erro ao excluir nota");
  }
}, []);
```

A correcao e apenas no backend: adicionar o handler `DELETE` na route. O padrao de todos os outros handlers no projeto usa `requireOrgAccess` + `createTenantClient` — seguir exatamente esse padrao.

Inspecionar o handler POST existente para entender como `orgId` e obtido (provavelmente do body ou de um header customizado). A nota tem campo `authorId` — usar para verificacao de autorizacao.

### Contexto do Bug BUG-002 (Mutacao direta)

Linha atual em `contact-panel.tsx`:

```typescript
// ERRADO — mutacao direta
onNameUpdated={(newName) => {
  if (contact) contact.name = newName;
}}
```

O padrao correto ja existe no projeto para notas (`handleUpdateNotes` em `InboxLayout`):

```typescript
// CORRETO — spread imutavel via setContact
onNameUpdated={(newName) => {
  setContact((prev) => prev ? { ...prev, name: newName } : null);
}}
```

A diferenca e que `contact.name = newName` muta o objeto sem notificar o React. O spread `{ ...prev, name: newName }` cria um novo objeto, disparando re-render correto em todos os filhos que dependem de `contact`.

### Contexto do Bug BUG-003 (Permissao de jornada)

Em `src/app/(app)/[orgId]/ai/actions.ts`, linha ~351:

```typescript
// ATUAL — bloqueia agentes de liveChat
assertMemberPermission(member, "integrations");
```

Agentes de inbox tem permissao `"liveChat"`, nao `"integrations"`. A permissao `"integrations"` e tipicamente para configurar webhooks e APIs externas — nao faz sentido semantico para alteracao de jornada por um agente humano.

Antes de alterar: verificar se existem outros usos de `updateJourneyState` que dependem da restricao `"integrations"` (ex: chamadas automatizadas via pipeline). Se existirem, criar uma segunda server action `updateJourneyStateByAgent` com a permissao corrigida ao inves de alterar a existente.

### Stack Relevante

- **Servidor:** `vultr`, path `/home/tikso/tikso/`
- **Auth:** NextAuth v5 beta — `requireOrgAccess(orgId)` e `assertMemberPermission(member, permission)`
- **ORM:** Prisma 7 com tenant isolation via `createTenantClient(orgId)`
- **API Routes:** Next.js App Router — `src/app/api/inbox/notes/route.ts`
- **Server Actions:** `src/app/(app)/[orgId]/ai/actions.ts`

### Testing

- **Tipo:** Teste manual no servidor de desenvolvimento
- **Ambiente:** SSH `vultr`, `cd /home/tikso/tikso && npm run dev`
- **Cenarios obrigatorios:**
  - [ ] DELETE nota propria: deve remover da UI e do banco (status 200)
  - [ ] DELETE nota de outro usuario sem admin: deve retornar toast de erro (status 403)
  - [ ] Editar nome, verificar que ambos `ProfileHeader` e `ContactInfoCard` mostram nome novo
  - [ ] Usuario com permissao `liveChat` altera estado de jornada sem erro 403
  - [ ] Usuario sem `liveChat` nem `integrations` recebe erro adequado ao tentar alterar jornada

---

## Change Log

| Data | Versao | Descricao | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 1.0 | Story criada baseada no QA Audit do sidebar | @sm (River) |

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
| `src/app/api/inbox/notes/route.ts` | MODIFY — adicionar handler DELETE com auth, autorizacao e delete no banco |
| `src/components/inbox/contact-panel.tsx` | MODIFY — corrigir callback `onNameUpdated` (linha ~149) |
| `src/components/inbox/inbox-layout.tsx` | MODIFY — adicionar `handleContactNameUpdated` com `setContact` imutavel |
| `src/app/(app)/[orgId]/ai/actions.ts` | MODIFY — corrigir permissao em `updateJourneyState` (linha ~351) |

---

## QA Results

### Re-Review Date: 2026-02-25

### Reviewed By: Quinn (Test Architect)

### Review Type: RE-REVIEW (apos fixes aplicados sobre issues da review inicial)

### Code Quality Assessment

Todas as tres correcoes solicitadas na review anterior foram implementadas corretamente. O codigo segue o padrao do projeto (uso de `requireOrgAccess`, `createTenantClient`, `memberHasPermission`, spread imutavel no React state) e nao apresenta regressoes nos handlers existentes.

### Fix Verification (3 issues da review anterior)

**[FIX-1] [CRITICAL] AC2 - Autorizacao no DELETE: CORRIGIDO**

- `notes-route.ts` L129: select agora inclui `authorId` -- `select: { id: true, organizationId: true, authorId: true }`
- `notes-route.ts` L143: verifica autoria -- `const isAuthor = session.user?.id === note.authorId`
- `notes-route.ts` L144: verifica role admin -- `const isAdmin = member.role === "ADMIN"`
- `notes-route.ts` L145-150: retorna 403 se nenhum dos dois -- `if (!isAuthor && !isAdmin) { return NextResponse.json({ success: false, error: "Nao autorizado a excluir esta nota" }, { status: 403 }) }`
- `notes-route.ts` L140: `requireOrgAccess` agora retorna `{ session, member }` -- ambos sao usados para as verificacoes

**[FIX-2] [MEDIUM] AC3 - Mobile `onContactUpdate` prop: CORRIGIDO**

- `inbox-layout.tsx` L1060: `ContactPanel` no layout mobile agora recebe `onContactUpdate={(updates) => setContact((prev) => prev ? { ...prev, ...updates } : prev)}` -- identico ao padrao do desktop (L1163)
- Confirma paridade completa entre desktop e mobile para propagacao imutavel de atualizacoes de contato

**[FIX-3] [MEDIUM] AC4 - Permissao dupla liveChat/integrations: CORRIGIDO**

- `ai-actions.ts` L5: importa `memberHasPermission` de `@/lib/auth/check-permission` -- usa funcao utilitaria existente do projeto em vez de acesso direto a array
- `ai-actions.ts` L357-358: comentario claro -- `// AC4: Accept liveChat OR integrations (agents have liveChat, automations have integrations)`
- `ai-actions.ts` L358: `const hasJourneyPermission = memberHasPermission(member, "liveChat") || memberHasPermission(member, "integrations")` -- aceita ambas permissoes conforme spec
- `ai-actions.ts` L359-361: retorna erro 400 em vez de throw -- `if (!hasJourneyPermission) { return { success: false, error: "Sem permissao para alterar jornada" } }` -- padrao consistente com o retorno da server action (nao lanca excecao)

### AC Traceability

| AC | Resultado | Evidencia |
|----|-----------|-----------|
| AC1 - DELETE de notas funciona | PASS | `notes-route.ts` L113-162: handler DELETE exportado, extrai `noteId` de searchParams (L117), valida presenca (L119-124), busca nota com `prisma.internalNote.findUnique` (L127-130), retorna 404 se nao encontrada (L132-137), valida org com `requireOrgAccess` (L140), deleta com `db.internalNote.delete` (L154), retorna 200 (L156). Frontend em `contact-panel.tsx` L1265-1277 faz `fetch(..., { method: "DELETE" })` e remove do state com `setInternalNotes(prev => prev.filter(...))`. |
| AC2 - Autorizacao no DELETE | PASS | `notes-route.ts` L129: select inclui `authorId`. L140: desestrutura `{ session, member }` de `requireOrgAccess`. L143: `isAuthor = session.user?.id === note.authorId`. L144: `isAdmin = member.role === "ADMIN"`. L145-150: retorna 403 com mensagem se nenhum dos dois. Cobre os cenarios: autor pode excluir propria nota, admin pode excluir qualquer nota, outros membros recebem 403. |
| AC3 - Nome atualiza sem mutacao | PASS | `contact-panel.tsx` L179-183: callback `onNameUpdated` chama `onContactUpdate({ name: newName })` -- sem mutacao direta. `inbox-layout.tsx` L1163 (desktop): `onContactUpdate={(updates) => setContact(prev => prev ? { ...prev, ...updates } : prev)}` -- spread imutavel. `inbox-layout.tsx` L1060 (mobile): `onContactUpdate={(updates) => setContact((prev) => prev ? { ...prev, ...updates } : prev)}` -- identico ao desktop. Paridade desktop/mobile confirmada. |
| AC4 - Journey acessivel por liveChat | PASS | `ai-actions.ts` L5: importa `memberHasPermission` de `@/lib/auth/check-permission`. L358: `memberHasPermission(member, "liveChat") \|\| memberHasPermission(member, "integrations")`. L359-361: retorna `{ success: false, error }` se nenhuma permissao. Usuarios com `liveChat` (agentes de inbox) e usuarios com `integrations` (automacoes/pipelines) podem alterar jornada. |
| AC5 - Sem regressoes | PASS | Handlers POST (L6-70) e GET (L73-110) em `notes-route.ts` permanecem intactos. `ProfileHeader` continua funcional. Demais server actions em `ai-actions.ts` (`updateAIConfig`, `addKnowledgeBase`, etc.) continuam usando `assertMemberPermission(member, "integrations")` -- sem impacto colateral. Mobile e desktop tem paridade de props no `ContactPanel`. |

### Compliance Check

- Coding Standards: PASS -- Segue padrao do projeto (kebab-case, imports absolutos com `@/`, TypeScript)
- Project Structure: PASS -- Arquivos nos locais corretos (api routes, components, server actions)
- Security: PASS -- Autorizacao autor/admin implementada no DELETE, permissoes validadas via `memberHasPermission`
- Testing Strategy: N/A -- Story define apenas testes manuais (aplicacao em servidor Vultr)
- All ACs Met: PASS -- Todos os 5 ACs satisfeitos

### Issues Found

Nenhum issue pendente. Todos os 3 issues da review anterior foram resolvidos.

### Security Review

O endpoint DELETE de notas agora implementa controle de acesso correto em tres camadas: (1) autenticacao via `requireOrgAccess` que valida pertinencia a organizacao, (2) verificacao de autoria `session.user?.id === note.authorId`, (3) fallback para role admin `member.role === "ADMIN"`. Tentativas nao autorizadas retornam 403 com mensagem descritiva. A permissao de jornada usa `memberHasPermission` (funcao utilitaria do projeto) em vez de acesso direto a propriedades, o que e mais seguro e mantem consistencia.

### Performance Considerations

Nenhum problema de performance identificado. O handler DELETE faz uma query global para buscar a nota antes de deletar (necessario para validar org e autoria antes de criar o tenant client), seguido de delete com tenant client -- padrao correto.

### Refactoring Performed

Nenhum. QA nao modifica codigo fonte.

### Files Modified During Review

Nenhum arquivo de codigo modificado. Apenas a secao QA Results desta story foi atualizada.

### Gate Status

**Gate: APPROVED**

- 0 issues CRITICAL
- 0 issues MEDIUM
- 5/5 ACs satisfeitos
- 3/3 fixes da review anterior confirmados

Quality Score: **100/100**

### Recommended Status

**APPROVED** -- Todos os acceptance criteria estao satisfeitos e todos os issues identificados na review anterior foram corrigidos com evidencia de codigo. A story esta pronta para teste manual no servidor Vultr e posterior deploy por @devops.
