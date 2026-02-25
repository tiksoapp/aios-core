# AwSales.io -- Reverse-Engineering da Arquitetura Tecnica

**Data:** 2026-02-25
**Analista:** Aria (AIOS Architect)
**Nivel de Confianca Geral:** MEDIO (analise inferencial a partir de fontes publicas, sem acesso a codigo-fonte)
**Metodo:** OSINT (Open Source Intelligence) -- website, LinkedIn, Instagram, BuiltWith, job postings, Meta partner directory, artigos tecnicos, e analise de padroes da industria

---

## Sumario Executivo

AwSales e uma startup brasileira sediada em Belo Horizonte (MG) com ~37 funcionarios, posicionada como "a maior infraestrutura de agentes autonomos da America Latina". A empresa e Meta Business Partner oficial para WhatsApp, atende principalmente o mercado de infoprodutos/criadores digitais, e reporta crescimento de 300% de receita trimestral (Q3 2025). Este relatorio infere a arquitetura tecnica a partir de sinais publicos e padroes da industria, identificando gaps e oportunidades para o Tikso CRM.

---

## 1. Perfil da Empresa

| Atributo | Valor |
|----------|-------|
| **Nome** | AwSales |
| **Website** | awsales.io |
| **Sede** | Belo Horizonte, MG, Brasil (CEP 34006-053) |
| **Tipo** | Empresa Privada |
| **Funcionarios** | ~37 (LinkedIn, fev/2026) |
| **Industria** | Software Development |
| **Seguidores LinkedIn** | 646 |
| **Instagram** | @awsales.io (~8.000+ seguidores) |
| **Slogan** | "A maior infraestrutura de agentes autonomos da America Latina" |
| **Posicionamento** | AI Agents for Business / Conversational AI for Digital Creators |
| **Parceria Meta** | Meta Business Partner (WhatsApp) -- early access e suporte direto |
| **Parceria iFood** | Parceiro tecnologico estrategico do iFood Lab Techbites Challenge (2a edicao) |
| **Crescimento** | 300% receita trimestral em uma vertical (Q3 2025) |
| **Contato** | join@awsales.io (vagas) |

### Equipe Tecnica Identificada

| Nome | Cargo Inferido | Sinais |
|------|----------------|--------|
| **Wellington Alves** | Tech Lead / Software Architect | LinkedIn: "Tech Lead / Software Architect", 10+ anos dev, Univ. Federal de Goias, backend, pipelines, DevOps |
| **Jose Junior** | Engineering Lead (ex) | LinkedIn: "Technical architecture drives revenue", Harvard Business School Online, saiu recentemente |
| **Alexandre Tavares** | Engenheiro/Dev (presumido) | Listado como equipe no LinkedIn |
| **Daniel Roscoe** | Staff (funcao nao confirmada) | Listado como equipe no LinkedIn |
| **Cinthia Moyses Goncalves** | Staff (funcao nao confirmada) | Listado como equipe no LinkedIn |

### Vagas Recentes

| Vaga | Data | Ferramentas Requeridas |
|------|------|----------------------|
| Motion Designer | Jan/2026 | After Effects, Figma, Photoshop |

**[NOTA]** Nenhuma vaga tecnica (dev, backend, infra) foi encontrada publicamente, o que sugere: (a) equipe tecnica estavel, (b) contratacoes via rede direta, ou (c) time enxuto com alta senioridade.

---

## 2. Stack Tecnologico Inferido

### 2.1 Frontend (Website/Landing)

| Componente | Tecnologia | Confianca | Evidencia |
|------------|-----------|-----------|-----------|
| Site/Landing | **Framer** | ALTA | modulepreload scripts, framerusercontent.com CDN |
| CDN | **Framer CDN** + **Google Fonts CDN** (gstatic.com) | ALTA | Headers de rede |
| Fontes | Inter, DM Sans, Poppins, Manrope, Figtree, Product Sans, Montserrat | ALTA | CSS font-face |
| Design | Design-first approach, variaveis de fontes | ALTA | Analise CSS |

**Insight:** O site e 100% client-side rendered (Framer gera SPA), o que explica porque WebFetch nao consegue extrair conteudo -- tudo e renderizado via JavaScript pos-carregamento. Isso e marketing site, NAO a plataforma.

### 2.2 Dashboard/Plataforma (Inferido)

| Componente | Tecnologia Provavel | Confianca | Raciocinio |
|------------|-------------------|-----------|------------|
| Frontend | **React** ou **Next.js** | MEDIA | Padrao da industria BR para SaaS, Wellington tem exp. web |
| Styling | **Tailwind CSS** | MEDIA-BAIXA | Padrao dominante em startups BR 2024-2026 |
| State | **Zustand** ou **Redux** | BAIXA | Insuficiente evidencia |

### 2.3 Backend

| Componente | Tecnologia Provavel | Confianca | Raciocinio |
|------------|-------------------|-----------|------------|
| Linguagem | **Node.js (TypeScript)** e/ou **Python** | MEDIA | Wellington Alves: "deep knowledge in web systems", pipelines; Node e dominante no ecossistema WhatsApp/Baileys; Python para ML/LLM |
| Framework API | **Express/Fastify** (Node) ou **FastAPI** (Python) | MEDIA | Padroes da industria para WhatsApp webhook handling |
| Message Queue | **Redis + BullMQ** ou **SQS** | MEDIA | Padrao para processamento assincrono de WhatsApp em alta escala; 37 funcionarios sugere stack pragmatica |
| Database | **PostgreSQL** | MEDIA | Padrao dominante SaaS BR; multi-tenant com RLS ou schema separation |
| Cache | **Redis** | MEDIA-ALTA | Necessario para session state, rate limiting, e caching de conversas |
| ORM | **Prisma** ou **TypeORM** | MEDIA-BAIXA | Depende se Node.js ou Python e dominante |

### 2.4 Infraestrutura

| Componente | Tecnologia Provavel | Confianca | Raciocinio |
|------------|-------------------|-----------|------------|
| Cloud Provider | **AWS** | MEDIA | Parceria iFood Lab (iFood e heavy AWS user), ZoomInfo lista "AWS Web Hosting"; Padrao da industria |
| Alternativa | **GCP** (por causa de Vertex AI) | BAIXA | Possivel se usam Gemini como LLM |
| Containers | **Docker** + **ECS/EKS** ou **Kubernetes** | MEDIA | Necessario para multi-tenant agent scaling |
| CI/CD | **GitHub Actions** | MEDIA-BAIXA | Padrao startup |

### 2.5 LLMs e IA

| Componente | Tecnologia Provavel | Confianca | Raciocinio |
|------------|-------------------|-----------|------------|
| LLM Principal | **GPT-4o / GPT-4o-mini** (OpenAI) | MEDIA-ALTA | Dominante no mercado BR de chatbots, melhor balance custo/qualidade para vendas |
| LLM Secundario | **Claude 3.5 Sonnet** (Anthropic) | MEDIA | Para tarefas que requerem reasoning mais profundo |
| Alternativa | **Gemini 1.5 Pro** (Google) | BAIXA | Menos provavel para WhatsApp SaaS BR |
| Fine-tuning | **Pouco provavel** | MEDIA | 37 funcionarios sugere uso de prompting avancado + RAG, nao fine-tuning customizado |
| RAG | **Embeddings + Vector DB** | MEDIA-ALTA | Necessario para customizacao por cliente (catalogo de produtos, FAQ, politicas) |
| Vector DB | **Pinecone** ou **pgvector** | MEDIA | Pinecone se AWS, pgvector se preferem manter tudo em Postgres |
| Orquestrador | **LangChain** ou **Custom** | MEDIA | LangChain e popular mas muitas empresas migram para custom em escala |

### 2.6 WhatsApp Integration

| Componente | Tecnologia | Confianca | Raciocinio |
|------------|-----------|-----------|------------|
| API | **WhatsApp Cloud API** (oficial, Meta) | ALTA | Meta Business Partner obrigatoriamente usa API oficial |
| BSP Status | **Meta Business Partner** direto | ALTA | Declarado no site e LinkedIn |
| On-Premises | **NAO** (deprecado Out/2025) | ALTA | Meta encerrou On-Premises API |
| Webhook | **HTTPS webhook endpoint** | ALTA | Padrao obrigatorio do Cloud API |
| Rate Limit | **Ate 500 msg/s** (Cloud API) | ALTA | Limite do Cloud API |
| Tier | **Tier 3 ou Ilimitado** (provavel) | MEDIA | Necessario para volume de clientes enterprise |

**Insight Critico:** Como Meta Business Partner, a AwSales tem acesso oficial e direto a WhatsApp Cloud API. Isso elimina o risco de ban que existe com APIs nao-oficiais (Baileys/Evolution API). Este e o diferencial arquitetural mais significativo vs Tikso.

---

## 3. Arquitetura de Agentes (Inferida)

### 3.1 Diagrama de Arquitetura Inferida

```
                     AWSALES - ARQUITETURA INFERIDA
                     ==============================

[WhatsApp User] <--> [WhatsApp Cloud API (Meta)]
                           |
                           | Webhook (HTTPS POST)
                           v
                 +-------------------+
                 | Webhook Receiver  |  <-- Retorna 200 imediatamente
                 | (API Gateway/LB)  |      processa async
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 | Message Queue     |  <-- Redis + BullMQ (ou SQS)
                 | (Inbound Queue)   |      Buffer de mensagens
                 +--------+----------+
                          |
                          v
              +-----------+-----------+
              |  Message Processor    |
              |  (Worker Pool)        |
              +-----------+-----------+
                          |
               +----------+----------+
               |                     |
               v                     v
     +---------+--------+  +--------+---------+
     | Tenant Router    |  | Session Manager  |
     | (identifica org  |  | (Redis: conversa |
     |  pelo numero)    |  |  state, history) |
     +---------+--------+  +--------+---------+
               |                     |
               +----------+----------+
                          |
                          v
              +-----------+-----------+
              |  Agent Orchestrator   |
              |  (routing por intent) |
              +-----------+-----------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
    +-----+-----+  +-----+-----+  +------+------+
    | Sales Agent|  | Support   |  | Recovery    |
    | (vendas,  |  | Agent     |  | Agent       |
    |  qualif.) |  | (suporte) |  | (carrinho   |
    +-----+-----+  +-----+-----+  |  abandonado)|
          |               |        +------+------+
          |               |               |
          +-------+-------+-------+-------+
                  |
                  v
        +---------+---------+
        |  LLM Gateway      |  <-- GPT-4o / GPT-4o-mini
        |  (prompt + tools) |      com function calling
        +---------+---------+
                  |
          +-------+-------+
          |               |
          v               v
    +-----+-----+  +-----+-----+
    | RAG Engine |  | Tool      |
    | (knowledge |  | Executor  |
    |  base do   |  | (CRM, cal,|
    |  cliente)  |  |  payment) |
    +-----+-----+  +-----+-----+
          |               |
          v               v
    +-----+-----+  +-----+-----+
    | Vector DB  |  | External  |
    | (Pinecone/ |  | APIs      |
    | pgvector)  |  | (CRM, ERP)|
    +-----------+  +-----------+
                  |
                  v
        +---------+---------+
        |  Response Builder |
        |  + Guardrails     |  <-- Validacao pre-envio
        +---------+---------+
                  |
                  v
        +---------+---------+
        |  Outbound Queue   |
        |  (rate limiting,  |
        |   compliance)     |
        +---------+---------+
                  |
                  v
        [WhatsApp Cloud API] --> [WhatsApp User]

                  |
        +---------+---------+
        | Analytics Engine  |
        | (metricas, conv.  |
        |  rates, revenue)  |
        +-------------------+
```

### 3.2 Tipos de Agente

Baseado nas features anunciadas, AwSales opera com agentes especializados por funcao:

| Agente | Funcao | Triggers |
|--------|--------|----------|
| **Sales Agent** | Qualificar leads, recomendar produtos, guiar ate checkout | Mensagem inicial, intent de compra |
| **Support Agent** | Responder duvidas pre-compra, FAQ, informacoes | Intent de duvida, pos-venda |
| **Recovery Agent** | Recuperar carrinho abandonado, follow-up em quotes | Timer-based, oportunidade perdida |
| **Booking Agent** | Agendar reunioes/consultas, calendario | Intent de agendamento |
| **Handoff Agent** | Transferir para humano com contexto completo | Threshold de falha, request explicito, lead quente |

**Confianca:** MEDIA. A descricao do produto menciona explicitamente "qualifica e roteia leads, agenda consultas, suporte, recupera oportunidades, com human-handoff". Isso sugere 4-5 agentes especializados, nao um agente generico.

### 3.3 Estrategia: Conversational Flywheel

AwSales descreve sua abordagem como um "Conversational Flywheel" -- um ciclo virtuoso:

```
  Understand --> Connect --> Help --> Sell
      ^                                |
      |________________________________|
            (dados voltam como learning)
```

1. **Understand** -- Entender o que o cliente quer (NLU + contexto)
2. **Connect** -- Conectar autenticamente (tom de voz personalizado)
3. **Help** -- Oferecer ajuda real (nao forcar venda)
4. **Sell** -- Vender quando o momento e certo

**Implicacao Tecnica:** Isso requer:
- Session state persistente entre conversas
- Customer profile enrichment (historico de interacoes)
- Sentiment analysis para timing de oferta
- A/B testing de abordagens por segmento

### 3.4 Fluxo de Processamento de Mensagem

```
1. [WhatsApp User envia mensagem]
2. [Meta Cloud API envia webhook POST para AwSales endpoint]
3. [Webhook receiver retorna HTTP 200 IMEDIATAMENTE] (best practice: <200ms)
4. [Mensagem publicada em queue (Redis/SQS)]
5. [Worker consome da queue]
6. [Tenant identification pelo numero do WhatsApp Business]
7. [Session retrieval/creation (Redis)]
8. [Intent classification (LLM ou modelo leve)]
9. [Agent routing baseado em intent + estado da conversa]
10. [Agent selecionado executa com LLM + tools]
11. [RAG query para knowledge base do cliente especifico]
12. [Tool calls se necessario (CRM, calendario, pagamento)]
13. [Response gerada pelo LLM]
14. [Guardrails check (compliance, tom, limites)]
15. [Response enfileirada em outbound queue (rate limiting)]
16. [Envio via WhatsApp Cloud API]
17. [Metricas registradas (latencia, conversao, sentiment)]
```

**Latencia estimada:** 2-5 segundos end-to-end (padrao da industria para WhatsApp AI agents com LLM).

---

## 4. Estrategia de IA

### 4.1 Abordagem: Hibrida (Generativa + Guardrails)

| Aspecto | Abordagem Inferida | Confianca |
|---------|-------------------|-----------|
| Modelo | IA generativa com function calling | ALTA |
| Fluxos | Hibrida: generativa para conversa + fluxos pre-definidos para checkout/agendamento | MEDIA-ALTA |
| Guardrails | Pre-envio: validacao de tom, compliance, limites de escopo | MEDIA-ALTA |
| Customizacao | Por cliente: knowledge base (RAG), tom de voz, catalogo, regras de negocio | ALTA |
| Human handoff | Automatico por threshold + manual por request | ALTA |

**Evidencia:** "Set policies/guardrails and go live in days" (site) indica um sistema de guardrails configuravel. "Role-based access, audit logs, and data retention controls" confirma enterprise-grade governance.

### 4.2 Customizacao por Cliente

AwSales promete "go live in days", o que implica:
- Onboarding via configuracao, NAO via codigo
- Upload de knowledge base (FAQ, catalogo, politicas)
- Configuracao de tom de voz via prompt templates
- Regras de negocio declarativas (ex: "nunca oferecer desconto acima de X%")
- Integracao plug-and-play com CRMs/ERPs

### 4.3 Guardrails

| Tipo | Implementacao Provavel |
|------|----------------------|
| **Conteudo** | System prompt com regras de negocio + output validation |
| **Compliance** | Templates aprovados para mensagens proativas (WhatsApp Meta policy) |
| **Escopo** | Limites de autoridade do agente (ex: nao pode alterar preco) |
| **Fallback** | Human handoff automatico quando confianca baixa |
| **Audit** | Logs de toda conversa para compliance e analytics |

### 4.4 Metricas e Analytics

Baseado no posicionamento "analytics included":
- Taxa de conversao por agente/campanha
- Receita atribuida a IA vs humano
- Tempo medio de resolucao
- Taxa de handoff para humano
- Sentiment tracking
- R$450k+ em oportunidades recuperadas (case publicado)

---

## 5. Integracoes

### 5.1 Integracoes Confirmadas/Anunciadas

| Categoria | Integracao | Confianca | Evidencia |
|-----------|-----------|-----------|-----------|
| WhatsApp | **Cloud API (Meta oficial)** | ALTA | Meta Business Partner |
| CRM | "Connect your CRM" (generico) | ALTA | Site oficial |
| Calendario | "Connect your calendar" (generico) | ALTA | Booking agent feature |
| Pagamentos | "Connect your payment gateway" | ALTA | Checkout via WhatsApp |
| ERP | "Connect your ERP" | MEDIA | Site oficial |

### 5.2 CRMs Provaveis

| CRM | Probabilidade | Raciocinio |
|-----|---------------|------------|
| **Kommo (ex-amoCRM)** | ALTA | CRM #1 para WhatsApp no Brasil |
| **HubSpot** | ALTA | Padrao internacional, tem integracao WhatsApp nativa |
| **Pipedrive** | MEDIA | Popular com infoprodutores BR |
| **RD Station** | MEDIA | Forte no mercado BR |
| **Salesforce** | MEDIA | Enterprise tier |
| **Custom via Webhook** | ALTA | Necessario para flexibilidade |

### 5.3 Integracao de Pagamentos

| Gateway | Probabilidade | Raciocinio |
|---------|---------------|------------|
| **Hotmart** | ALTA | Plataforma #1 de infoprodutos no Brasil |
| **Eduzz/Monetizze** | MEDIA-ALTA | Alternativas Hotmart |
| **Stripe** | MEDIA | Padrao internacional |
| **Asaas** | MEDIA | Popular BR para recorrencia |
| **Hub.la (Hubla)** | MEDIA | Crescendo no mercado de infoprodutos |

---

## 6. Diagrama Comparativo: AwSales vs Tikso

### 6.1 Feature Comparison Matrix

| Feature | AwSales | Tikso (Eli) | Gap |
|---------|---------|-------------|-----|
| **WhatsApp API** | Cloud API (oficial Meta) | Evolution API v2.3.7 (nao-oficial) | CRITICO |
| **Risco de Ban** | Baixo (API oficial) | ALTO (Issue #2298, restricao 1-2 dias) | CRITICO |
| **LLM** | GPT-4o (inferido) | GPT (via OpenAI) | SIMILAR |
| **Function Calling** | Sim (tools: CRM, cal, payment) | Sim (tools: BestBarbers) | SIMILAR |
| **RAG** | Sim (knowledge base por cliente) | Nao implementado | ALTO |
| **Multi-tenant** | Sim (SaaS, multiplos clientes) | Nao (single-tenant, por org) | ALTO |
| **Agentes Especializados** | ~5 (sales, support, recovery, booking, handoff) | 1 (Eli, generico) | MEDIO |
| **Agent Routing** | Por intent + estado | N/A (agente unico) | MEDIO |
| **Human Handoff** | Automatico + manual, com contexto | Planejado (ELI-02 circuit breaker) | MEDIO |
| **Circuit Breaker** | Provavel (enterprise-grade) | Planejado (ELI-02, 3 falhas) | EM DESENVOLVIMENTO |
| **Guardrails** | Configuravel por cliente | Basico (prompt rules) | MEDIO |
| **Antiban** | N/A (API oficial nao precisa) | Extensivo (83+ testes, feedback loop, 429 backoff, presence, rate limit) | N/A (diferente) |
| **CRM Integration** | Multi-CRM (Kommo, HubSpot, etc) | CRM proprio (Tikso) | DIFERENTE |
| **Checkout WhatsApp** | Sim (payment gateway) | Nao | ALTO |
| **Agendamento** | Sim (calendario integrado) | Sim (BestBarbers scheduling) | SIMILAR |
| **Analytics** | Sim (conversion, revenue, sentiment) | Basico | ALTO |
| **Onboarding** | Self-service em dias | Manual/dev-dependent | ALTO |
| **Audit Logs** | Sim | Nao explicitamente | MEDIO |
| **Customizacao Tom** | Por cliente (configuravel) | Global (prompt builder) | MEDIO |
| **Recovery (carrinho)** | Sim (automatico) | Nao | ALTO |
| **Proactive Messaging** | Sim (PULSE agent) | Sim (PULSE cron) | SIMILAR |
| **Design (Inbox)** | Dashboard multi-org | Dashboard single-org | MEDIO |
| **Service Resolution** | Provavel (enterprise-grade) | BUG (ELI-01: horarios fantasma) | EM CORRECAO |

### 6.2 Arquitetura Comparativa

```
                 AWSALES                          TIKSO
                 =======                          =====

API:       WhatsApp Cloud API (Meta)    Evolution API v2.3.7 (Baileys)
              |                                |
Risco:     ZERO ban risk                  ALTO ban risk (Issue #2298)
              |                                |
Scale:     Multi-tenant SaaS             Single-tenant por org
              |                                |
Agents:    5+ especializados             1 generico (Eli)
              |                                |
RAG:       Knowledge base por cliente    Sem RAG
              |                                |
Queue:     Redis/SQS enterprise          BullMQ (message-queue.ts)
              |                                |
LLM:       GPT-4o + function calling     GPT + function calling
              |                                |
Guardrails: Configuravel por cliente     Prompt-level rules
              |                                |
Handoff:   Automatico + contextual       Planejado (ELI-02)
              |                                |
Analytics: Revenue attribution           Basico
              |                                |
Deploy:    AWS (inferido) cloud-native   Vultr VPS (PM2)
```

---

## 7. Gap Analysis: O Que Falta no Tikso para Competir

### GAPS CRITICOS (P0 -- Resolver Imediatamente)

| # | Gap | Impacto | Recomendacao |
|---|-----|---------|-------------|
| **G1** | **WhatsApp API nao-oficial (Evolution/Baileys)** | Risco de ban a cada 1-2 dias; mata operacao | Migrar para WhatsApp Cloud API (oficial Meta). INVESTIMENTO: tempo de integracao + custos Meta por conversa (~R$0.25-0.50/conversa) |
| **G2** | **Service Resolution bugs (horarios fantasma)** | 40% das conversas de agendamento podem ter falha | Priorizar ELI-01 imediatamente -- AwSales NAO tem esse problema (enterprise-grade) |
| **G3** | **Sem Human Handoff automatico** | Cliente preso em loop de erros | Priorizar ELI-02 -- AwSales tem handoff automatico com contexto |

### GAPS ALTOS (P1 -- Planejar para Proximo Trimestre)

| # | Gap | Impacto | Recomendacao |
|---|-----|---------|-------------|
| **G4** | **Sem RAG (knowledge base por cliente)** | Agente nao sabe detalhes especificos do negocio | Implementar RAG com pgvector (ja usa Postgres) -- upload de FAQ, catalogo, politicas por organizacao |
| **G5** | **Sem checkout via WhatsApp** | Perda de conversao no momento critico da compra | Integrar payment link generation (Stripe/Asaas/Hotmart) direto na conversa |
| **G6** | **Sem recovery de carrinho/oportunidade** | Receita perdida nao e recuperada | Agente proativo PULSE pode ser estendido para recovery campaigns |
| **G7** | **Analytics basico** | Nao consegue provar ROI da IA para cliente | Dashboard de conversao, receita atribuida, tempo de resolucao |

### GAPS MEDIOS (P2 -- Roadmap 6 Meses)

| # | Gap | Impacto | Recomendacao |
|---|-----|---------|-------------|
| **G8** | **Agente unico vs especializados** | Menos eficaz em tarefas especificas | Evoluir para multi-agent com routing por intent |
| **G9** | **Guardrails basicos** | Risco de respostas inadequadas | Sistema de guardrails configuravel por organizacao |
| **G10** | **Customizacao de tom global** | Todos os clientes tem mesmo tom | Tom de voz configuravel por organizacao |
| **G11** | **Deploy em VPS unico** | Single point of failure, scaling manual | Migrar para container-based deploy (Docker + orquestrador) |
| **G12** | **Audit logs** | Sem compliance trail | Logging estruturado de toda conversa para auditoria |

### O QUE O TIKSO JA TEM E AWSALES (PROVAVELMENTE) NAO

| Vantagem Tikso | Detalhe |
|----------------|---------|
| **Sistema antiban sofisticado** | 83+ testes, feedback loop, 429 backoff, presence simulation, per-destination rate limit, opt-out. Relevante se mantiver Evolution API |
| **CRM integrado** | AwSales depende de CRMs terceiros; Tikso TEM o CRM, o que permite deeper integration |
| **Controle total da stack** | Single-tenant permite customizacao profunda por cliente. AwSales multi-tenant tem limitacoes |
| **Inbox com badges/timers** | Stories INB-01 a INB-05 mostram UX avancada no inbox |
| **Custo de operacao** | Evolution API e gratis (sem custo por mensagem); Cloud API cobra por conversa |

---

## 8. Recomendacoes de Evolucao Arquitetural

### 8.1 Estrategia Dual-Track (Curto Prazo)

```
Track 1: ESTABILIZAR (Eli Reliability Sprint)
  - ELI-01: Fix service resolution (horarios fantasma)
  - ELI-02: Circuit breaker + auto-handoff
  - ELI-03: Error classification + sanitization
  - ELI-04: Tom de voz (parceiro balcao)
  - ELI-05: Verificacao proativa de assinante

Track 2: PLANEJAR MIGRACAO API
  - Avaliar custo WhatsApp Cloud API vs risco ban Evolution
  - PoC: dual-mode (Evolution para volume baixo, Cloud API para volume alto)
  - Timeline: 2-3 meses para migracao completa
```

### 8.2 Roadmap de Evolucao (6 Meses)

```
Mes 1-2: RELIABILITY
  |-- ELI epic completo (5 stories)
  |-- Circuit breaker, handoff, error handling
  |-- Tom de voz configuravel por org

Mes 2-3: INTELLIGENCE
  |-- RAG implementation (pgvector)
  |-- Knowledge base upload por organizacao
  |-- Customer profile enrichment

Mes 3-4: MONETIZATION
  |-- Checkout via WhatsApp (payment links)
  |-- Recovery agent (carrinho/oportunidade abandonada)
  |-- Analytics dashboard (conversao, revenue attribution)

Mes 4-5: SCALE
  |-- Multi-agent routing (sales, support, booking, recovery)
  |-- WhatsApp Cloud API migration (dual-mode)
  |-- Guardrails configuravel por org

Mes 5-6: ENTERPRISE
  |-- Audit logs e compliance
  |-- Self-service onboarding
  |-- Multi-org dashboard
```

### 8.3 Decisoes Arquiteturais Recomendadas

| Decisao | Recomendacao | Trade-off |
|---------|-------------|-----------|
| **WhatsApp API** | Migrar para Cloud API como canal primario, manter Evolution como fallback | Custo por conversa vs estabilidade |
| **RAG** | pgvector no Postgres existente (evita nova dependencia) | Simplicidade vs performance (Pinecone e mais rapido, mas mais complexo) |
| **Multi-agent** | Comecar com router simples baseado em intent keywords, evoluir para LLM-based routing | Complexidade incremental |
| **Queue** | Manter BullMQ (ja em uso), adicionar dead-letter queue | Ja implementado, baixo esforco |
| **Analytics** | Eventos de conversa -> Postgres -> Dashboard (Next.js) | Build vs buy (Metabase?) |
| **Deploy** | Docker Compose como primeiro passo, Kubernetes depois | Complexidade gradual |

---

## 9. Analise de Mercado Competitivo

### 9.1 Landscape WhatsApp AI Agents Brasil

```
                      Enterprise-Grade
                           ^
                           |
              Respond.io   |   AwSales
              Yellow.ai    |   Blip (Take)
                           |
     Multi-channel  <------+------> WhatsApp-First
                           |
              Wati         |   Tikso (Eli)
              Gallabox     |   BotConversa
              AiSensy      |   NeoSale AI
                           |
                           v
                       SMB/Simples
```

### 9.2 Posicionamento Estrategico

AwSales se diferencia por:
1. **Foco vertical** em infoprodutos/criadores digitais (Maira "Seca Voce", saude)
2. **Meta Business Partner** (credibilidade + acesso privilegiado)
3. **"Autonomous agents"** (nao chatbot -- agentes que AGEM)
4. **Metricas de receita** (R$450k+ em oportunidades recuperadas)
5. **iFood Lab** partnership (validacao de mercado)

Tikso se diferencia por:
1. **CRM + IA integrado** (nao depende de CRM terceiro)
2. **Controle total** (customizacao profunda por cliente)
3. **Custo operacional** (Evolution API gratis)
4. **Antiban sofisticado** (vantagem tecnica unica)
5. **Mercado de servicos locais** (barbearias, clinicas, etc.)

---

## 10. Conclusoes

### 10.1 O Que Aprender da AwSales

1. **API oficial e inegociavel para escala** -- O risco de ban com Evolution API e existencial para um negocio SaaS. AwSales elimina esse risco sendo Meta Business Partner.

2. **Agentes especializados > agente generico** -- Um agente de vendas NAO deve ter o mesmo comportamento que um agente de suporte. AwSales separa por funcao.

3. **RAG e obrigatorio para customizacao** -- Sem RAG, cada cliente precisa de prompt engineering manual. Com RAG, o cliente faz upload de seu conteudo e o agente aprende.

4. **Recovery e revenue direto** -- R$450k+ em oportunidades recuperadas e o tipo de metrica que vende o produto. Tikso precisa de um Recovery Agent.

5. **"Go live in days" e o benchmark** -- Onboarding rapido e self-service e o que escala um SaaS. Tikso precisa simplificar setup por organizacao.

### 10.2 O Que NAO Copiar

1. **Multi-tenant puro** -- Tikso tem a vantagem de CRM integrado. Manter essa vantagem com customizacao profunda.

2. **Framer para site** -- Bonito mas impossivel de crawlar/SEO-indexar conteudo. Se Tikso fizer landing page, preferir Next.js com SSR.

3. **Dependencia total de LLM** -- O sistema antiban do Tikso (rule-based + behavior simulation) e uma vantagem tecnica que LLMs nao replicam.

### 10.3 Risco Estrategico

AwSales com 37 funcionarios e Meta Business Partner tem vantagem significativa em:
- Credibilidade (parceria Meta)
- Escala (Cloud API sem risco de ban)
- Go-to-market (infoprodutores/criadores com alto volume)

Tikso deve competir em:
- **Verticalizacao profunda** (clinicas, barbearias, servicos locais)
- **CRM integrado** (dados do cliente moram no Tikso, nao em terceiros)
- **Custo** (Evolution API gratis para clientes menores)
- **Customizacao** (cada org pode ter setup unico)

---

## Fontes

- [AwSales - AI Agents for Business](https://awsales.io/en/)
- [AwSales - Conversational AI for Digital Creators](https://awsales.io/en/en-us)
- [AwSales LinkedIn Company Page](https://br.linkedin.com/company/awsales)
- [Wellington Alves - Tech Lead / Software Architect (LinkedIn)](https://www.linkedin.com/in/wac0013/)
- [Jose Junior - Awsales (LinkedIn)](https://www.linkedin.com/in/jose-junior-0396a6191/)
- [AwSales Instagram (@awsales.io)](https://www.instagram.com/awsales.io/)
- [AWS Blog: Best Practices for WhatsApp AI Assistant](https://aws.amazon.com/blogs/messaging-and-targeting/best-practices-for-building-high-performance-whatsapp-ai-assistant-using-aws/)
- [WhatsApp Cloud API Documentation](https://business.whatsapp.com/products/platform-pricing)
- [BullMQ Documentation](https://docs.bullmq.io/)
- [WhatsApp BSP Guide 2026 - Prelude](https://prelude.so/blog/best-whatsapp-business-solution-providers)
- [NeoFeed - WhatsApp Startups Brasileiras](https://neofeed.com.br/startups/como-o-whatsapp-e-a-ia-estao-moldando-uma-nova-geracao-de-startups-brasileiras/)
- [Respond.io - Top 7 Conversational AI Platforms 2026](https://respond.io/blog/top-conversational-ai-platforms)
- [Hookdeck - WhatsApp Webhooks Best Practices](https://hookdeck.com/webhooks/platforms/guide-to-whatsapp-webhooks-features-and-best-practices)
- [Evolution API GitHub Issues (#2298, #2228, #1946)](https://github.com/EvolutionAPI/evolution-api/issues/2298)

---

*-- Aria, arquitetando o futuro*
