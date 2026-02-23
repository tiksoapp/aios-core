# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What Is This

Synkra AIOS is a CLI-first multi-agent orchestration framework (npm package `aios-core` v4.x). It installs into any project and coordinates specialized AI agents for development roles. The framework is IDE-agnostic with first-class support for Claude Code, Gemini CLI, Codex CLI, Cursor, and GitHub Copilot.

---

## Constitution (Non-Negotiable Rules)

Full document: `.aios-core/constitution.md`

| Artigo | Princípio | Severidade |
|--------|-----------|------------|
| I | **CLI First** — All functionality must work 100% via CLI before any UI. Dashboards observe, never control. | NON-NEGOTIABLE |
| II | **Agent Authority** — Only `@devops` can git push/PR/release. Only `@sm`/`@po` create stories. Only `@architect` makes architecture decisions. Only `@qa` issues quality verdicts. | NON-NEGOTIABLE |
| III | **Story-Driven Development** — All development starts from a story in `docs/stories/` | MUST |
| IV | **No Invention** — Implement exactly what specs say, nothing more | MUST |
| V | **Quality First** — All quality gates must pass before push | MUST |
| VI | **Absolute Imports** — Always use `@/` or `@synkra/` path aliases, never relative imports | SHOULD |

---

## Build, Test, Lint Commands

```bash
# Tests (Jest v30)
npm test                              # Run all tests
npm test -- --testPathPattern="synapse"  # Run tests matching a path pattern
npm test -- tests/unit/cli.test.js    # Run a single test file
npm run test:watch                    # Watch mode
npm run test:coverage                 # With coverage report
npm run test:health-check             # Health checks (Mocha, separate runner)

# Lint & Types
npm run lint                          # ESLint (v9 flat config)
npm run typecheck                     # TypeScript (strict, noEmit)
npm run format                        # Prettier (markdown files)

# Validation (AIOS-specific)
npm run validate:structure            # Source tree guardian
npm run validate:agents               # Agent definition validation
npm run validate:manifest             # Install manifest validation
npm run validate:semantic-lint        # Semantic lint on markdown
npm run validate:parity               # Multi-IDE sync parity check

# IDE Sync
npm run sync:ide                      # Sync all IDEs
npm run sync:ide:claude               # Claude Code only
npm run sync:ide:codex                # Codex CLI only
npm run sync:ide:gemini               # Gemini CLI only

# CLI (when developing the framework itself)
node bin/aios.js install              # Run installer locally
node bin/aios.js doctor               # System diagnostics
node bin/aios.js info                 # System info
```

**Quality gates before push:** `npm run lint && npm run typecheck && npm test`

---

## Architecture Overview

### Priority Hierarchy

```
CLI (source of truth) → Observability (monitoring) → UI (visualization)
```

### Monorepo Structure (npm workspaces)

```
aios-core/
├── bin/                          # CLI entry points
│   ├── aios.js                   # Main CLI (both `aios` and `aios-core` bins)
│   ├── aios-init.js              # Legacy installer (deprecated, fallback only)
│   ├── aios-minimal.js           # Minimal installer
│   └── aios-ids.js               # IDS CLI tooling
├── .aios-core/                   # Framework core
│   ├── core/                     # Runtime modules (see Core Modules below)
│   ├── development/              # Agent defs, tasks, templates, checklists
│   ├── data/                     # Knowledge base, entity registry
│   ├── infrastructure/           # CI/CD templates, IDE sync scripts, validators
│   └── constitution.md           # Non-negotiable rules
├── packages/                     # npm workspace packages
│   ├── installer/                # v4 modular installation wizard
│   ├── aios-install/             # Standalone npx installer (@synkra/aios-install)
│   ├── aios-pro-cli/             # Pro license management CLI
│   └── gemini-aios-extension/    # Gemini CLI native extension
├── .claude/                      # Claude Code integration
│   ├── hooks/                    # Lifecycle hooks (SYNAPSE engine, etc.)
│   └── rules/                    # Additional rules (MCP usage)
├── .synapse/                     # SYNAPSE runtime state & metrics
├── docs/stories/                 # Development stories (active/, completed/)
├── squads/                       # Squad expansions (domain-specific agent teams)
├── pro/                          # Pro submodule (proprietary, git submodule)
└── tests/                        # Test suite (unit/, integration/, synapse/, etc.)
```

### Core Modules (`.aios-core/core/`)

| Module | Purpose |
|--------|---------|
| **`synapse/`** | SYNAPSE context engine — 8-layer pipeline injecting rules into every prompt (see below) |
| **`orchestration/`** | Multi-agent orchestration — master orchestrator, workflow executor, parallel execution, skill dispatch, agent assignment |
| **`execution/`** | Build engine — autonomous build loop, wave executor, semantic merge, subagent dispatch |
| **`ids/`** | Incremental Decision System — service registry, circuit breaker, framework governor, verification gates |
| **`health-check/`** | System diagnostics — pluggable check registry, auto-healers, reporters |
| **`quality-gates/`** | 3-layer quality system — L1 pre-commit, L2 PR automation, L3 human review |
| **`memory/`** | Gotchas memory system for cross-session learning |
| **`elicitation/`** | Interactive elicitation engine for agent/task/workflow context gathering |
| **`code-intel/`** | Code intelligence — providers, enrichers, registry sync |
| **`permissions/`** | Operation guard, permission modes |
| **`session/`** | Session context detection and loading |
| **`mcp/`** | MCP config management, symlinks, OS detection |

### SYNAPSE Context Engine

SYNAPSE is the framework's nervous system. It runs as a **Claude Code `UserPromptSubmit` hook** (`.claude/hooks/synapse-engine.cjs`) on every user prompt, injecting contextual rules in <100ms.

**8-Layer Pipeline:**
| Layer | Name | Purpose |
|-------|------|---------|
| L0 | Constitution | Non-negotiable framework rules |
| L1 | Global | Project-wide conventions |
| L2 | Agent | Active agent's specific rules |
| L3 | Workflow | Current workflow state |
| L4 | Task | Current task context |
| L5 | Squad | Squad-specific rules |
| L6 | Keyword | Rules triggered by prompt keywords |
| L7 | Star-command | `*command` invocation handling |

**Key files:** `engine.js` (orchestrator, 100ms hard timeout), `layers/l0-l7` (layer processors, 15ms budget each), `context/context-tracker.js` (bracket-aware: LIGHT/MEDIUM/HEAVY based on prompt count), `output/formatter.js` (emits `<synapse-rules>` XML).

### Agent System

12 agents defined in `.aios-core/development/agents/*.md` (Markdown with embedded YAML):

| Agent | Persona | Exclusive Authority |
|-------|---------|-------------------|
| `@dev` (Dex) | Full Stack Developer | Code implementation |
| `@qa` (Quinn) | QA Engineer | Quality verdicts |
| `@architect` (Aria) | System Architect | Architecture decisions |
| `@pm` (Morgan) | Product Manager | Product strategy |
| `@po` (Pax) | Product Owner | Story/backlog management |
| `@sm` (River) | Scrum Master | Sprint/story creation |
| `@analyst` (Alex) | Business Analyst | Research & analysis |
| `@data-engineer` (Dara) | Data Engineer | Database design |
| `@ux-design-expert` (Uma) | UX Designer | UX/UI design |
| `@devops` (Gage) | DevOps Engineer | **git push, PRs, releases (EXCLUSIVE)** |
| `@aios-master` | Meta-orchestrator | Framework development |
| `@squad-creator` | Squad builder | Creates new squads |

**Activation:** `@agent-name` or `/AIOS:agents:agent-name`. Commands use `*` prefix (`*help`, `*create-story`, `*task {name}`, `*exit`).

### Installer Architecture

Two-tier system routing through `bin/aios.js`:
- **Primary:** `packages/installer/src/wizard/` — Modern wizard with `@clack/prompts`, i18n, brownfield upgrade detection
- **Fallback:** `bin/aios-init.js` — Legacy wizard (deprecated since v3.11.3, removal planned v5.0.0)

The installer generates IDE-specific files: `.claude/commands/AIOS/` for Claude Code, `.cursor/rules/AIOS/*.mdc` for Cursor, `.gemini/rules/AIOS/` for Gemini, `.github/chatmodes/aios-*.md` for Copilot.

### Hooks (`.claude/hooks/`)

| Hook | Event | Purpose |
|------|-------|---------|
| `synapse-engine.cjs` | UserPromptSubmit | SYNAPSE context injection (main hook) |
| `precompact-session-digest.cjs` | PreCompact | Session digest before context compaction |
| `enforce-architecture-first.py` | — | Architecture-first principle enforcement |
| `write-path-validation.py` | — | Protects critical file paths from writes |
| `read-protection.py` | — | Read access control |
| `sql-governance.py` | — | SQL safety governance |

---

## Code Conventions

- **Files:** kebab-case (`workflow-list.tsx`)
- **Components/Interfaces:** PascalCase (`WorkflowList`, `WorkflowListProps`)
- **Constants:** SCREAMING_SNAKE_CASE (`MAX_RETRIES`)
- **Hooks:** `use` prefix (`useWorkflowOperations`)
- **Imports:** Always absolute (`@/stores/feature/store`, never `../../../`)
- **TypeScript:** No `any` — use `unknown` with type guards. `as const` for constant objects.
- **Path aliases:** `@synkra/aios-core` → `.aios-core/core/`, `@synkra/aios-core/*` → `.aios-core/core/*`

---

## Git Conventions

**Commits:** Conventional Commits with story reference — `feat: implement feature [Story 2.1]`
- `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`

**Branches:** `main`, `feat/*`, `fix/*`, `docs/*`

**Push authority:** Only `@devops` can push to remote.

**Pre-commit (Husky + lint-staged):** ESLint fix + Prettier on JS/TS, Prettier + semantic-lint on Markdown, IDE sync when agent `.md` files change.

---

## Story-Driven Development

1. Every task starts with a story in `docs/stories/`
2. Update checkboxes as tasks complete: `[ ]` → `[x]`
3. Maintain the File List section in the story
4. Implement exactly what acceptance criteria specify

**Workflow:** `@po *create-story → @dev implements → @qa tests → @devops push`

---

## Language Configuration

Language is set via Claude Code's native `language` setting in `~/.claude/settings.json` or `.claude/settings.json`:
```json
{ "language": "portuguese" }
```

---

## MCP Usage

See `.claude/rules/mcp-usage.md` for full rules. Key points:
- Always prefer native Claude Code tools over MCP
- `@devops` exclusively manages MCP infrastructure
- Docker MCP Toolkit for EXA (search), Context7 (library docs), Apify (scraping)
- Playwright for browser automation only when explicitly requested
