# Story 6.11: Framework Documentation Consolidation

**Epic:** Open-Source Readiness (OSR)
**Story ID:** 6.11
**Sprint:** 6
**Priority:** 🟠 Medium
**Points:** 3
**Effort:** 2-3 hours
**Status:** ⚪ Ready
**Type:** 📝 Documentation / Refactoring

---

## 📊 Status

- [x] Draft
- [x] Validated (PO Review)
- [ ] Approved
- [ ] In Progress
- [ ] Ready for Review
- [ ] Done

---

## 📋 User Story

**Como** desenvolvedor ou agente AIOS,
**Quero** que os documentos oficiais do framework estejam em um único local bem definido (`docs/framework/`),
**Para** evitar confusão entre documentos portáveis do framework e análises específicas do projeto.

---

## 🎯 Objetivo

Consolidar a documentação oficial do framework em `docs/framework/` e organizar `docs/architecture/` para conter apenas documentos específicos do projeto.

### Problemas Identificados (Story 6.10 QA)

| Problema | Impacto |
|----------|---------|
| `core-config.yaml` aponta para `docs/architecture/` | Inconsistência |
| `agent-config-requirements.yaml` aponta para `docs/framework/` | Conflito de referências |
| `docs/framework/` está desatualizado (v1.0, aios/aios-core) | Documentação incorreta |
| `docs/architecture/` tem 39 arquivos misturados | Difícil navegação |
| Duplicação de source-tree, coding-standards, tech-stack | Manutenção difícil |

---

## 🔍 Contexto

### Análise de Padrões da Indústria

| Fonte | Recomendação |
|-------|--------------|
| Microsoft Engineering Playbook | Separar docs do repo vs docs do projeto |
| Nx (Monorepo Tool) | Agrupar por scope/propósito |
| GitHub Best Practices | README + estrutura clara por propósito |

### Estrutura Atual vs Proposta

```
ATUAL (Problemático):
docs/
├── architecture/           # 39 arquivos misturados
│   ├── source-tree.md      # ✅ Atualizado (v1.1)
│   ├── coding-standards.md # ✅ Atualizado
│   ├── tech-stack.md       # ✅ Atualizado
│   ├── mcp-optimization-1mcp.md  # Análise de projeto
│   ├── tools-system-analysis-log.md  # Análise de projeto
│   └── ... (36 outros arquivos)
│
├── framework/              # 4 arquivos desatualizados
│   ├── source-tree.md      # ❌ v1.0 (aios/aios-core)
│   ├── coding-standards.md # ❌ Desatualizado
│   ├── tech-stack.md       # ❌ Desatualizado
│   └── README.md

PROPOSTO (Limpo):
docs/
├── framework/              # Docs OFICIAIS do framework (portáveis)
│   ├── source-tree.md      # ✅ Sincronizado de architecture/
│   ├── coding-standards.md # ✅ Sincronizado
│   ├── tech-stack.md       # ✅ Sincronizado
│   └── README.md           # ✅ Atualizado
│
├── architecture/           # Docs ESPECÍFICOS do projeto
│   ├── decisions/          # ADRs e decisões arquiteturais
│   ├── analysis/           # Análises técnicas (mcp, tools, etc.)
│   ├── diagrams/           # Diagramas de arquitetura
│   └── ARCHITECTURE-INDEX.md
```

---

## ✅ Acceptance Criteria

### AC1: Framework Docs Synchronized
- [ ] `docs/framework/source-tree.md` sincronizado com versão v1.1
- [ ] `docs/framework/coding-standards.md` sincronizado
- [ ] `docs/framework/tech-stack.md` sincronizado
- [ ] `docs/framework/README.md` atualizado com Migration Notice para `SynkraAI/aios-core`

### AC2: core-config.yaml Updated
- [ ] `devLoadAlwaysFiles` aponta para `docs/framework/`
- [ ] `devLoadAlwaysFilesFallback` inclui fallback para `docs/architecture/`
- [ ] Comentário explicando a preferência por `docs/framework/`

### AC3: Architecture Folder Organized
- [ ] Subpasta `docs/architecture/analysis/` criada
- [ ] Arquivos de análise movidos para `analysis/`
- [ ] `ARCHITECTURE-INDEX.md` atualizado com nova estrutura

### AC4: References Updated
- [ ] Grep confirma nenhuma referência quebrada
- [ ] Agent loaders funcionam corretamente
- [ ] `npm test` passa

### AC5: Duplicates Deprecated
- [ ] `docs/architecture/source-tree.md` marcado como DEPRECATED (aponta para framework/)
- [ ] `docs/architecture/coding-standards.md` marcado como DEPRECATED
- [ ] `docs/architecture/tech-stack.md` marcado como DEPRECATED

---

## 📝 Tasks

### Task 1: Sync Framework Docs (30min)

**Files:**
- `docs/framework/source-tree.md`
- `docs/framework/coding-standards.md`
- `docs/framework/tech-stack.md`
- `docs/framework/README.md`

**Actions:**
1. [ ] Copy content from `docs/architecture/source-tree.md` (v1.1) to `docs/framework/source-tree.md`
2. [ ] Copy content from `docs/architecture/coding-standards.md` to `docs/framework/coding-standards.md`
3. [ ] Copy content from `docs/architecture/tech-stack.md` to `docs/framework/tech-stack.md`
4. [ ] Update `docs/framework/README.md` with SynkraAI migration notice

### Task 2: Update core-config.yaml (15min)

**File:** `.aios-core/core-config.yaml`

**Actions:**
1. [ ] Change `devLoadAlwaysFiles` paths from `docs/architecture/` to `docs/framework/`
2. [ ] Add `docs/architecture/` paths to `devLoadAlwaysFilesFallback`
3. [ ] Add comment explaining the change
4. [ ] Bump version to 2.3.0

### Task 3: Organize Architecture Folder (45min)

**Actions:**
1. [ ] Create `docs/architecture/analysis/` directory
2. [ ] Move analysis files to `analysis/`:
   - mcp-optimization-1mcp.md
   - mcp-context-optimization-strategy.md
   - mcp-solution-comparison-checklist.md
   - tools-system-analysis-log.md
   - tools-system-gap-analysis.md
   - expansion-packs-dependency-analysis.md
   - expansion-packs-structure-inventory.md
   - scripts-consolidation-analysis.md
   - subdirectory-migration-impact-analysis.md
   - repository-strategy-analysis.md
3. [ ] Update `ARCHITECTURE-INDEX.md` with new structure
4. [ ] Verify no broken links

### Task 4: Deprecate Duplicates (15min)

**Actions:**
1. [ ] Add DEPRECATED notice to `docs/architecture/source-tree.md`
2. [ ] Add DEPRECATED notice to `docs/architecture/coding-standards.md`
3. [ ] Add DEPRECATED notice to `docs/architecture/tech-stack.md`
4. [ ] Each notice should point to `docs/framework/` equivalent

### Task 5: Validation (30min)

**Actions:**
1. [ ] Run `npm test`
2. [ ] Verify dev agent loads correctly with new paths
3. [ ] Grep for broken references
4. [ ] Manual review of changes

---

## 📁 Files to Modify

| File | Action | Priority |
|------|--------|----------|
| `docs/framework/source-tree.md` | Sync | 🔴 High |
| `docs/framework/coding-standards.md` | Sync | 🔴 High |
| `docs/framework/tech-stack.md` | Sync | 🔴 High |
| `docs/framework/README.md` | Update | 🔴 High |
| `.aios-core/core-config.yaml` | Update | 🔴 High |
| `docs/architecture/source-tree.md` | Deprecate | 🟠 Medium |
| `docs/architecture/coding-standards.md` | Deprecate | 🟠 Medium |
| `docs/architecture/tech-stack.md` | Deprecate | 🟠 Medium |
| `docs/architecture/ARCHITECTURE-INDEX.md` | Update | 🟠 Medium |
| `docs/architecture/analysis/` | Create | 🟡 Low |
| Multiple analysis files | Move | 🟡 Low |

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Story 6.10 | ✅ Done | Documentation cleanup complete |
| OSR-8 | ✅ Done | Squads guide created |
| OSR-9 | ✅ Done | Rebranding to Synkra complete |

---

## ⚠️ Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking agent loaders | Medium | High | Add fallback paths in core-config |
| Broken internal links | Medium | Low | Grep validation + manual review |
| Confusion during transition | Low | Medium | Clear DEPRECATED notices |

---

## 🤖 CodeRabbit Integration

### Story Type Analysis
- **Primary Type:** Documentation/Refactoring
- **Complexity:** Low
- **Secondary Types:** Configuration

### Specialized Agents
- **Primary:** @dev
- **Supporting:** @architect (for structure validation)

### Quality Gates
- [ ] Pre-Commit (@dev): Lint/format all modified files
- [ ] Pre-PR (@qa): Verify no broken paths/references

### Self-Healing Configuration
- **Mode:** light
- **Max Iterations:** 2
- **Timeout:** 15 minutes

---

## 📝 Dev Notes

### Technical Context
- Framework docs should be portable across all AIOS projects
- `docs/framework/` was created in Story 6.1.2.6 (Jan 2025) but never fully activated
- `agent-config-requirements.yaml` already references `docs/framework/` (future-ready)
- This story completes the migration started in 6.1.2.6

### Key Files Reference
```
Framework Docs (TARGET):
├── docs/framework/source-tree.md      # Official structure
├── docs/framework/tech-stack.md       # Official tech stack
├── docs/framework/coding-standards.md # Official standards

Configuration:
├── .aios-core/core-config.yaml        # devLoadAlwaysFiles
├── .aios-core/data/agent-config-requirements.yaml  # Already correct

Architecture (ORGANIZE):
├── docs/architecture/analysis/        # NEW: Analysis docs
├── docs/architecture/decisions/       # EXISTS: ADRs
└── docs/architecture/ARCHITECTURE-INDEX.md
```

### Deprecation Notice Template
```markdown
> ⚠️ **DEPRECATED**: This file is maintained for backward compatibility only.
>
> **Official version:** [docs/framework/{filename}](../framework/{filename})
>
> This file will be removed in Q2 2026 after migration to `SynkraAI/aios-core`.
```

---

## 🎯 Definition of Done

- [ ] All framework docs in `docs/framework/` are current (v1.1+)
- [ ] `core-config.yaml` references `docs/framework/`
- [ ] Fallback paths ensure backward compatibility
- [ ] Architecture folder organized with `analysis/` subdir
- [ ] Duplicate files marked DEPRECATED
- [ ] All tests pass
- [ ] Agent loaders work correctly
- [ ] PR merged to main

---

## 📝 Notes

This story completes the documentation consolidation started in Story 6.1.2.6 and addresses technical debt identified during Story 6.10 QA review.

**Rationale for `docs/framework/` name:**
- Semantically correct (these are framework standards)
- Already exists with README explaining purpose
- Referenced in `agent-config-requirements.yaml`
- Industry patterns favor separation by purpose
- Minimal changes required (sync vs restructure)

---

## 📋 Version History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-14 | 1.0 | Initial story creation | Quinn (QA) |

---

*Story created as follow-up to Story 6.10 QA review findings*
