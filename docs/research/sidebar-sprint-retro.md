# Retrospectiva do Sprint SIDEBAR

**Epic:** SIDEBAR -- Contact Detail Panel Redesign (Tikso CRM)
**Data:** 2026-02-25
**Facilitador:** Pax (PO)
**Servidor:** Vultr (`/home/tikso/tikso/`)

---

## 1. Resumo do Sprint

| Metrica | Valor |
|---------|-------|
| Stories planejadas | 7 (SIDEBAR-01 a SIDEBAR-07) |
| Stories entregues | 7/7 (100%) |
| Stories implementadas nesta sessao | 6 (SIDEBAR-02 a SIDEBAR-07) |
| Story points entregues | 24 pts (sessao) + SIDEBAR-01 (anterior) |
| Arquivos modificados | 8 (7 existentes + 1 novo) |
| Arquivo mais tocado | `contact-panel.tsx` (6 stories) |
| Decisoes pragmaticas (scope trim) | 3 ACs ajustados |
| Erros de execucao encontrados | 5 problemas tecnicos |

### Distribuicao por Prioridade (MoSCoW)

| Prioridade | Stories | Pontos |
|------------|---------|--------|
| Must Have | SIDEBAR-02 | 5 |
| Should Have | SIDEBAR-03, SIDEBAR-04 | 5 + 3 = 8 |
| Could Have | SIDEBAR-05, SIDEBAR-06, SIDEBAR-07 | 3 + 5 + 3 = 11 |

### Arquivos Modificados

| Arquivo | Stories que tocaram |
|---------|-------------------|
| `contact-panel.tsx` | SIDEBAR-02, 03, 04, 05, 06, 07 |
| `contact-info-card.tsx` | SIDEBAR-02, 04, 07 |
| `inbox-layout.tsx` | SIDEBAR-02, 04, 05 |
| `section-header.tsx` | SIDEBAR-03, 07 |
| `notes-section.tsx` | SIDEBAR-04 |
| `tag-list.tsx` | SIDEBAR-04 |
| `actions.ts` | SIDEBAR-03, 06 |
| `error-boundary.tsx` (NOVO) | SIDEBAR-06 |

---

## 2. O que funcionou bem (Keep)

### 2.1 Python scripts para modificar TypeScript
Gotcha herdada do ATLAS-1 se confirmou novamente: usar Python para fazer replaces em arquivos TypeScript evita os problemas classicos de `sed -i` com template literals, regex greedy e encoding. Este padrao ja esta consolidado como pratica obrigatoria no projeto.

### 2.2 Padrao SCP + Execute
O fluxo `criar script local -> scp para o servidor -> executar via SSH` funcionou de forma consistente e previsivel. Reduz o risco de corromper codigo ao evitar heredocs e escaping multiplo em cadeia bash/SSH.

### 2.3 Quality gate consistente entre stories
Executar `TypeScript check + build + PM2 restart` apos cada story garantiu que erros de integracao fossem detectados imediatamente. Isso evitou acumulo de divida tecnica entre stories.

### 2.4 Stories bem escritas pelo SM
As stories tinham tasks detalhadas, acceptance criteria claros, e estimativas de esforco realistas. Isso permitiu implementacao fluida sem ambiguidades. O formato YAML com AC numerados (AC1-AC5) facilitou o tracking.

### 2.5 Implementacao incremental story-by-story
Deploy entre cada story permitiu validacao visual imediata. Problemas de TypeScript (como os erros do SIDEBAR-04) foram detectados e corrigidos antes de seguir para a proxima story.

---

## 3. O que precisa melhorar (Improve)

### 3.1 Template literal corruption via SSH
**Problema:** Backticks e `${}` em TypeScript sao interpretados pelo shell intermediario (Python -> bash -> SSH). Isso corrompeu codigo em pelo menos uma ocasiao.
**Impacto:** Retrabalho para diagnosticar e corrigir substituicoes defeituosas.
**Sugestao:** Documentar no gotcha do SYNAPSE que scripts Python que geram TypeScript com template literals devem usar raw strings (`r""`) e escapar `$` como `\$` dentro de strings que serao passadas por SSH.

### 3.2 Unicode matching issues
**Problema:** "Ultima" vs "Ultima" (com/sem acento) causou falha em operacoes de replace no Python.
**Impacto:** Script de modificacao nao encontrou o trecho alvo; necessitou debug adicional.
**Sugestao:** Sempre usar `re.IGNORECASE` nao basta -- o padrao de busca deve considerar ambas as formas (acentuada e nao-acentuada) ou usar regex com classe de caractere (ex: `[UuUu]ltima`).

### 3.3 TypeScript errors apos integracao (SIDEBAR-04)
**Problema:** `onEmailSaved` nao destructured corretamente, `updateContact` sem campo email, `newDescription` sem null safety. Tres erros de compilacao em sequencia.
**Impacto:** Exigiu uma sessao de correcao adicional antes de seguir para SIDEBAR-05.
**Sugestao:** Antes de executar cada script de modificacao, incluir uma etapa de analise do codigo atual para mapear todas as dependencias de tipo. Considerar gerar um "type context snapshot" antes de modificacoes.

### 3.4 Ownership de arquivos (root vs tikso)
**Problema:** `tsconfig.tsbuildinfo` ficou com owner `root` em vez de `tikso`, causando falha no build.
**Impacto:** Debug necessario para identificar a causa; `chown` manual para corrigir.
**Sugestao:** Todo script que modifica arquivos no servidor deve incluir `chown tikso:tikso` como ultimo passo. Criar um wrapper script padrao para isso.

### 3.5 Permissao de git push
**Problema:** O usuario `tiksoapp` nao tem acesso ao org SynkraAI/aios-core para push.
**Impacto:** Nenhum push foi feito no servidor remoto nesta sessao.
**Sugestao:** Configurar deploy key ou SSH key para o user tikso com acesso ao repositorio correto. Alternativamente, validar se o push deve acontecer do servidor ou de outro ambiente.

---

## 4. Itens de Acao

| # | Acao | Responsavel | Prioridade | Sprint |
|---|------|-------------|------------|--------|
| 1 | Criar gotcha SYNAPSE para template literal escaping via SSH | @po / @sm | Alta | Proximo |
| 2 | Criar gotcha SYNAPSE para Unicode matching em Python replaces | @po / @sm | Media | Proximo |
| 3 | Adicionar `chown tikso:tikso` como passo padrao em scripts de deploy | @dev | Alta | Proximo |
| 4 | Resolver permissao de git push no Vultr (deploy key ou SSH key) | @devops | Alta | Proximo |
| 5 | Criar "type context snapshot" pre-modificacao para evitar erros de compilacao | @dev | Media | Backlog |
| 6 | SIDEBAR-04 AC5 -- Implementar SectionHeader wrapping para Tags/Notes (adiado por invasividade) | @dev | Baixa | Backlog |
| 7 | SIDEBAR-06 AC1 -- getSidebarData batch refactor (adiado por risco) | @dev | Baixa | Backlog |
| 8 | SIDEBAR-06 AC3/AC4 -- Migrar de visibilitychange para Centrifugo quando eventos existirem | @dev | Baixa | Backlog |
| 9 | QA manual do painel completo (todas as 7 stories integradas) | @qa | Alta | Proximo |

---

## 5. Decisoes Pragmaticas Documentadas

Tres acceptance criteria foram ajustados durante a implementacao por razoes tecnicas legitimas:

| Story | AC | Decisao | Justificativa |
|-------|-----|---------|---------------|
| SIDEBAR-04 | AC5 | Skip SectionHeader wrapping para Tags/Notes | Wrapping exigiria refactor invasivo nos componentes filhos; o beneficio nao justificava o risco |
| SIDEBAR-06 | AC1 | getSidebarData batch NAO implementado | Refatorar o fluxo de dados inteiro era arriscado demais para uma otimizacao de performance |
| SIDEBAR-06 | AC3/AC4 | visibilitychange fallback em vez de Centrifugo | Eventos de Centrifugo para tags/notas/jornada simplesmente nao existem ainda no backend |

Estas decisoes sao aceitaveis do ponto de vista de produto. Os itens foram registrados como backlog para implementacao futura quando o contexto for mais favoravel.

---

## 6. Gotchas para o SYNAPSE

```yaml
gotchas:
  - id: gotcha-SIDEBAR-SSH-TEMPLATE-LITERAL
    title: "Template literal corruption via SSH pipeline"
    category: "Remote Execution"
    severity: high
    wrong: |
      Python script gera TypeScript com ${variable} e backticks,
      envia via bash -> SSH -> executa no servidor.
      Shell intermediario interpreta os template literals.
    right: |
      Usar raw strings em Python (r"").
      Escapar $ como \$ em strings que passam por SSH.
      Validar output do script com diff antes de aplicar.
    reason: >
      Backticks e ${} em TypeScript sao metacaracteres do bash.
      Ao passar por multiplas camadas de shell (local -> SSH -> bash remoto),
      eles sao expandidos/interpretados em vez de tratados como literals.
    discoveredAt: "2026-02-25"
    storyId: "SIDEBAR-02+"
    relatedFiles:
      - contact-panel.tsx
    tags: [ssh, remote, typescript, template-literals]

  - id: gotcha-SIDEBAR-UNICODE-MATCHING
    title: "Unicode/acento mismatch em Python replace operations"
    category: "String Manipulation"
    severity: medium
    wrong: |
      script.replace("Ultima mensagem", "novo texto")
      Falha se o arquivo contiver "Ultima" (com acento) em vez de "Ultima" (sem).
    right: |
      Usar regex com alternativa: re.sub(r"[UU]ltima", ...)
      Ou normalizar ambos os lados com unicodedata.normalize('NFC', ...) antes de comparar.
    reason: >
      Codigo no servidor pode ter sido escrito com ou sem acentos dependendo
      do encoding do editor/terminal. Python diferencia 'U' de 'U' (com acento).
    discoveredAt: "2026-02-25"
    storyId: "SIDEBAR-04"
    relatedFiles:
      - contact-info-card.tsx
    tags: [python, unicode, encoding, i18n]

  - id: gotcha-SIDEBAR-FILE-OWNERSHIP
    title: "Arquivo com owner root apos script executado como root"
    category: "Server Administration"
    severity: high
    wrong: |
      Executar script Python como root no servidor.
      Arquivo gerado/modificado fica com owner root.
      Build do Next.js falha porque PM2 roda como user tikso.
    right: |
      Sempre finalizar scripts com: chown tikso:tikso <arquivo_modificado>
      Ou executar o script inteiro como user tikso: su - tikso -c 'python3 script.py'
    reason: >
      PM2 roda como user tikso via systemd (pm2-tikso.service).
      Arquivos com owner root nao sao acessiveis pelo processo de build.
      tsconfig.tsbuildinfo e .next/ sao os mais comumente afetados.
    discoveredAt: "2026-02-25"
    storyId: "SIDEBAR-06"
    relatedFiles:
      - tsconfig.tsbuildinfo
    tags: [server, permissions, pm2, tikso]

  - id: gotcha-SIDEBAR-TS-DESTRUCTURE
    title: "TypeScript destructure errors ao adicionar props em componentes existentes"
    category: "TypeScript"
    severity: medium
    wrong: |
      Adicionar nova prop a um componente sem atualizar o destructure
      no ponto de chamada E na interface de tipos.
    right: |
      Ao adicionar props: (1) atualizar interface/type, (2) atualizar
      o destructure no componente, (3) atualizar todos os call sites.
      Rodar tsc --noEmit antes de qualquer outro passo.
    reason: >
      Scripts de modificacao frequentemente adicionam props mas esquecem
      de atualizar o destructure pattern ou os call sites. O TypeScript
      check so detecta isso apos a modificacao, causando retrabalho.
    discoveredAt: "2026-02-25"
    storyId: "SIDEBAR-04"
    relatedFiles:
      - contact-panel.tsx
      - contact-info-card.tsx
    tags: [typescript, props, destructure, refactor]
```

---

## Conclusao

O Sprint SIDEBAR foi altamente produtivo: 24 pontos entregues em uma unica sessao, com todas as 6 stories implementadas e deployadas incrementalmente. A taxa de entrega de 100% valida a maturidade do processo story-driven e do padrao de execucao remota via SCP.

Os problemas encontrados sao todos operacionais e previstos (shell escaping, encoding, permissoes) -- nenhum deles foi arquitetural ou de produto. As tres decisoes pragmaticas de scope trim foram bem fundamentadas e geraram itens de backlog apropriados.

O principal risco residual e a falta de QA manual integrada. Recomenda-se uma sessao de validacao visual antes de considerar a epic como fechada.

--- Pax, equilibrando prioridades
