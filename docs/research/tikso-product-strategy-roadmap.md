# Tikso -- Product Strategy & Roadmap 2026

**Documento:** PRD Estrategico
**Autor:** Morgan (PM Strategist) -- AIOS
**Data:** 2026-02-25
**Versao:** 1.0
**Status:** Draft para validacao do fundador
**Horizonte:** 12 meses (Mar/2026 -- Fev/2027)

**Documentos complementares:**
- [Inteligencia Competitiva AwSales](/root/aios-core/docs/research/awsales-competitive-intelligence.md)
- [Analise de Storytelling AwSales](/root/aios-core/docs/research/awsales-storytelling-analysis.md)
- [Analise de Conversa Eli/Kelmer](/root/aios-core/docs/research/eli-chatbot-conversation-analysis.md)
- [WhatsApp Antiban Best Practices](/root/aios-core/docs/research/whatsapp-antiban-best-practices.md)
- [Brand Identity & Logo Concepts](/root/aios-core/docs/research/tikso-brand-logo-concepts.md)

---

## Sumario Executivo

A Tikso tem a oportunidade de se tornar o CRM conversacional de referencia para negocios locais de servico no Brasil. O mercado de SaaS vertical para PMEs no pais cresce a ~25% ao ano, e nenhum player combina CRM + IA conversacional + WhatsApp num produto acessivel e vertical-first para segmentos como barbearias, clinicas esteticas e studios de beleza.

A estrategia proposta segue o modelo **"nail it then scale it"**: dominar o nicho de barbearias/beleza nos primeiros 6 meses (vertical-first), depois expandir horizontalmente para outros negocios locais de servico. O diferencial central -- a Eli como parceira de atendimento do negocio, nao um chatbot generico -- deve ser construido sobre um fosso de dados e integracao que torna a Tikso impossivel de substituir apos 3 meses de uso.

**Metricas-alvo para Fev/2027:**
- 200+ clientes pagantes
- R$80k+ MRR
- NPS > 60
- Churn mensal < 5%

---

## 1. Visao de Produto (Fev/2027)

### 1.1 Onde a Tikso precisa estar em 12 meses

Em fevereiro de 2027, a Tikso deve ser reconhecida como **a plataforma que faz negocio local faturar mais usando WhatsApp e IA**. Concretamente:

| Dimensao | Estado-alvo Fev/2027 |
|----------|---------------------|
| Clientes pagantes | 200+ |
| Verticais atendidas | 3-4 (barbearias, clinicas esteticas, studios de unhas, pet shops) |
| MRR | R$80-120k |
| Features core estabilizadas | Inbox, Eli (IA), agendamento, pipeline, campanhas, relatorios |
| Reputacao | Top-of-mind em "CRM para barbearia" no Brasil |
| Equipe | 5-8 pessoas (3-4 devs, 1 CS, 1 vendas, 1 marketing) |

### 1.2 Que mercados atacar

**[AUTO-DECISION]** Vertical-first ou horizontal? -> Vertical-first em beleza/barbearias, expandindo para verticais adjacentes a partir do Q3 (reason: time de 1-3 devs nao consegue atender necessidades divergentes de multiplas verticais simultaneamente; dominar um nicho cria case studies, referral organico e profundidade de produto impossivel de copiar por generalistas).

**Sequencia de expansao vertical:**

```
Q1-Q2 2026: Barbearias + Saloes de beleza
              |
Q3 2026: Clinicas esteticas + Studios de unhas
              |
Q4 2026: Pet shops + Clinicas veterinarias
              |
Q1-Q2 2027: Qualquer negocio local de servico com agendamento
```

**Racional da sequencia:**
1. **Barbearias/Saloes** -- Ja tem piloto (Trimmo), modelo de agendamento e recorrencia clara, ticket previsivel
2. **Clinicas esteticas/Unhas** -- Identico workflow (agendamento + servico), ticket maior (R$100-300/servico), alta recorrencia
3. **Pet shops/Vet** -- Mesmo padrao de agendamento, mas com twist de "paciente" (animal) que requer adaptacao no CRM
4. **Generalista local** -- Com as verticais anteriores dominadas, a plataforma ja tem as primitivas (agendamento, CRM, IA, campanhas) para qualquer negocio de servico

### 1.3 O "10x Better" que justifica existir

A Tikso nao e "mais um CRM". E a **parceira de atendimento que nunca falta, nunca esquece e sempre faz follow-up**. O "10x" vem de tres pilares:

**Pilar 1: Eli como funcionaria, nao como chatbot**

A Eli nao responde perguntas -- ela opera o negocio. Diferente de qualquer chatbot:
- Conhece cada cliente pelo historico (servico preferido, barbeiro favorito, frequencia)
- Agenda, reagenda e confirma sem atrito
- Faz follow-up proativo em quem nao apareceu
- Reativa clientes que sumiram
- Vende servicos adicionais no contexto certo

Nenhum concorrente no segmento de negocios locais oferece isso. Kommo e generalista. Respond.io e enterprise. AwSales foca em infoprodutos/e-commerce. BestBarbers e puro agendamento sem IA.

**Pilar 2: Setup em 15 minutos, valor em 24 horas**

O dono de barbearia nao quer configurar nada. A Tikso deve funcionar com:
1. Conectar WhatsApp (QR code)
2. Importar servicos e profissionais (ou digitar manualmente, 5 min)
3. A Eli comeca a atender

Em 24h, o dono ja ve agendamentos feitos pela Eli no dashboard. Isso e 10x mais rapido que qualquer CRM tradicional.

**Pilar 3: Impacto direto na receita, mensuravel em R$**

O dashboard mostra:
- "A Eli agendou R$3.200 essa semana"
- "12 clientes que iam dar no-show foram confirmados"
- "5 clientes inativos voltaram apos reativacao"

O dono ve o ROI em reais, nao em "leads qualificados" ou "conversas gerenciadas". Isso cria retencao porque desligar a Tikso = perder receita mensuravel.

---

## 2. Estrategia de Moat (Fosso Competitivo)

### 2.1 Data Moat -- Dados que so a Tikso tem

**O ativo mais valioso da Tikso nao e o codigo, e o grafo de relacionamento cliente-negocio.**

Apos 3 meses de uso, a Tikso acumula:

| Dado | Valor estrategico | Quem mais tem |
|------|-------------------|---------------|
| Historico de servicos por cliente | Permite sugestao proativa ("O de sempre?") | Ninguem -- BestBarbers tem agenda, nao historico conversacional |
| Frequencia de visita por cliente | Permite prever no-show e reativar no momento certo | Ninguem |
| Preferencia de profissional | Personaliza atendimento instantaneamente | Ninguem |
| Taxa de resposta por tipo de mensagem | Otimiza campanhas automaticamente | AwSales tem, mas para e-commerce, nao servico local |
| Receita por canal (WhatsApp vs presencial) | Mostra ROI da Eli em R$ | Ninguem |
| Padroes de sazonalidade do negocio | Pre-configura campanhas ("Promocao de verao" automatica) | Ninguem |

**Por que isso e um moat:** Quanto mais tempo o negocio usa a Tikso, mais a Eli fica inteligente sobre aquele negocio especifico. Migrar para outro CRM significa perder toda essa inteligencia. Depois de 6 meses, o custo de troca e proibitivo -- nao pelo preco, mas pela perda de dados contextuais.

### 2.2 Integration Moat -- Integracao como trava

| Integracao | Quando | Efeito de trava |
|------------|--------|-----------------|
| WhatsApp (Evolution API / Cloud API) | Dia 1 | Todas as conversas vivem na Tikso |
| BestBarbers / Trinks / AgendaBarber | Q1-Q2 | Agendamento fluido sem trocar de sistema |
| Maquininha (Stone, PagBank, Mercado Pago) | Q2-Q3 | Dados de pagamento enriquecem CRM |
| Contabilidade (ContaAzul, Omie) | Q3-Q4 | Relatorios fiscais automaticos |
| Google Business Profile | Q2 | Avaliacoes e reputacao conectadas |

**A cada integracao, o custo de troca aumenta.** Um negocio com WhatsApp + agenda + maquininha + contabilidade na Tikso nao migra para concorrente por R$50/mes de diferenca.

### 2.3 Network Effects

**Efeito de rede direto:** Nao existe (a Tikso nao e marketplace). Mas existe efeito de rede indireto:

1. **Referral dentro do nicho:** Barbeiros se conhecem. Se a Trimmo usa Tikso e fatura mais, os barbeiros vizinhos sabem. No segmento de barbearias, o word-of-mouth e o canal #1 de aquisicao.

2. **Dados agregados de benchmark:** Com 50+ barbearias na plataforma, a Tikso pode dizer "seu ticket medio e R$65, a media do mercado e R$78 -- aqui estao 3 sugestoes para aumentar". Benchmarks setoriais so existem com escala, e criam mais valor para cada cliente conforme a base cresce.

3. **Templates de Eli compartilhados:** Quando um dono configura um fluxo de reativacao que funciona (ex: "Faz tempo que voce nao aparece! Temos um slot com o Natan amanha"), esse template pode ser oferecido a outros negocios do mesmo vertical. Quanto mais negocios, melhores os templates, mais valor para todos.

### 2.4 Switching Costs (resumo)

| Fator | Custo de troca | Tempo para ficar "preso" |
|-------|---------------|--------------------------|
| Historico de conversas | Alto -- perder contexto de todos os clientes | 1 mes |
| Dados do CRM | Medio -- exportavel, mas reconstruir e penoso | 2 meses |
| Inteligencia da Eli | Muito alto -- IA treinada com dados do negocio | 3 meses |
| Integracoes configuradas | Alto -- refazer todas as conexoes | 3 meses |
| Habito do time | Medio -- reaprender nova ferramenta | 1 mes |
| Numero de WhatsApp vinculado | Alto -- risco de perder o numero em migracao | Imediato |

**Janela critica: 90 dias.** Se o cliente fica 90 dias ativo na Tikso, a probabilidade de churn cai para <3% mensal. A estrategia de onboarding deve focar obsessivamente nos primeiros 90 dias.

---

## 3. Feature Roadmap Priorizado

### 3.1 Visao de alto nivel

```
  Mar 2026         Abr-Jun 2026         Jul-Set 2026         Out-Dez 2026
  --------         -----------          -----------          -----------
  FOUNDATION       GROWTH               SCALE                DOMINATION
  10 clientes      50 clientes          200 clientes         Referencia
     |                |                    |                     |
  Fix Eli bugs     Campanhas          Multi-vertical       Marketplace
  Onboarding       Relatorios $       Self-service          Benchmarks
  Antiban P0       Integracoes        WhatsApp Cloud API    API publica
  Dashboard v1     Referral           Multi-usuario          White-label
```

---

### Q1 2026 (Marco) -- FOUNDATION: 10 primeiros clientes

**Objetivo:** Produto estavel que resolve o problema core -- agendamento via WhatsApp com IA -- sem falhas criticas.

**Contexto critico:** A analise da conversa Eli/Kelmer revelou 3 falhas sistemicas que precisam ser corrigidas ANTES de vender para qualquer novo cliente. Um produto quebrado nao rettem ninguem.

| # | Feature | RICE Score | Esforco | Detalhe |
|---|---------|-----------|---------|---------|
| F1 | **Fix Service ID resolution** | 57.0 | 0.5 sem | Bug critico: agendamento de servicos combinados (Corte+Barba) falha 100% das vezes. Perda estimada: R$5.760/mes por negocio |
| F2 | **Reordenar fluxo: servico ANTES de horario** | 9.0 | 2 sem | Eli oferece horarios fantasma porque nao sabe a duracao do servico antes de consultar. Perguntar servico primeiro, filtrar slots por duracao |
| F3 | **Escalacao automatica para humano** | 10.8 | 2 sem | Apos 2 falhas consecutivas, transferir para humano com contexto completo. 62% dos clientes abandonam apos 2 falhas sem escalacao |
| F4 | **Sanitizar mensagens de erro** | 5.7 | 1 sem | Nunca expor "service ID", "erro interno", detalhes tecnicos ao cliente. Logging interno + mensagem amigavel |
| F5 | **Antiban P0** | -- | 2 sem | Rate limiter (3/min, 30/h), typing simulation (30ms/char), gaussian jitter, horario comercial. Sem isso, numero e banido em dias |
| F6 | **Dashboard de receita v1** | -- | 2 sem | Metricas basicas: agendamentos via Eli, receita gerada, no-shows evitados, clientes reativados. O dono precisa ver o ROI em R$ |
| F7 | **Inteligencia de cliente basica** | 5.3 | 2 sem | Consultar CRM por numero de WhatsApp. Se cliente recorrente, oferecer fluxo express: "O de sempre com o Natan?" |
| F8 | **Tom de voz: parceiro de balcao** | -- | 1 sem | Eli deve falar como o atendente mais atencioso da barbearia, nao como um bot corporativo. Informal, direto, acolhedor |
| F9 | **Onboarding wizard** | -- | 1.5 sem | Setup guiado em 15 min: conectar WhatsApp, cadastrar servicos+profissionais, ativar Eli. Primeiro valor em <24h |

**Total estimado:** ~14 semanas de trabalho (2 devs = ~7 semanas calendario)

**Criterio de sucesso Q1:**
- 0 falhas de agendamento por bug de service ID
- Taxa de conclusao de agendamento via Eli > 75%
- 10 clientes pagantes ativos (barbearias/saloes)
- Zero bans de WhatsApp nos primeiros 30 dias de cada cliente

---

### Q2 2026 (Abr-Jun) -- GROWTH: 50 clientes

**Objetivo:** Features que fazem o cliente faturar MAIS e funcionalidades que permitem escalar a aquisicao.

| # | Feature | Prioridade | Esforco | Detalhe |
|---|---------|-----------|---------|---------|
| G1 | **Recuperacao de no-show automatizada** | P0 | 2 sem | Eli detecta no-show e dispara: "Oi [nome], vi que voce nao conseguiu vir hoje. Quer reagendar?" Pode recuperar 30-40% dos no-shows |
| G2 | **Reativacao de clientes inativos** | P0 | 2 sem | Eli identifica clientes que nao agendaram em 30+ dias e envia mensagem personalizada: "Faz tempo! O Natan tem horario [dia]" |
| G3 | **Campanhas de WhatsApp (broadcast segmentado)** | P0 | 3 sem | Enviar mensagens para segmentos (todos os clientes, inativos, aniversariantes, etc.) com antiban automatico (fila, delay, variacao) |
| G4 | **Relatorios de receita por canal** | P1 | 2 sem | Dashboard completo: receita via Eli vs presencial, ticket medio, frequencia de visita, ranking de profissionais, taxa de retorno |
| G5 | **Programa de fidelidade basico** | P1 | 2 sem | "A cada 10 cortes, 1 gratis" gerenciado pela Eli. Envia lembrete quando falta 2 para o gratuito. Aumenta recorrencia em 15-25% |
| G6 | **Integracao BestBarbers/Trinks** | P1 | 2 sem | Sincronizar agenda bidirecional. Cliente agenda por qualquer canal, tudo fica atualizado. Elimina conflito de horarios |
| G7 | **Upsell/cross-sell via IA** | P1 | 1.5 sem | Eli sugere servicos adicionais no contexto: "Vai querer barba tambem?" ou "Temos um tratamento novo para cabelo que ta fazendo sucesso" |
| G8 | **Sistema de referral** | P1 | 1.5 sem | "Indique uma barbearia amiga e ganhe 1 mes gratis." Dashboard para acompanhar indicacoes. Canal #1 de aquisicao no nicho |
| G9 | **Multi-usuario basico** | P2 | 2 sem | Dono + 1-2 funcionarios com acessos diferenciados. Necessario para barbearias com >1 profissional gerenciando agenda |
| G10 | **Lembrete automatico de agendamento** | P0 | 1 sem | 24h e 2h antes do horario. Reduz no-show em ate 70%. Feature mais pedida por negocios de servico |

**Total estimado:** ~19 semanas de trabalho (2-3 devs = ~7-10 semanas calendario)

**Criterio de sucesso Q2:**
- 50 clientes pagantes ativos
- MRR > R$15k
- Taxa de no-show dos clientes Tikso < 15% (vs media de 30% do mercado)
- Pelo menos 10 clientes adquiridos via referral organico
- Churn mensal < 8%

---

### Q3 2026 (Jul-Set) -- SCALE: 200 clientes

**Objetivo:** Preparar o produto para operar em multiplas verticais com minimo esforco de customizacao, e escalar a infra para 200+ clientes.

| # | Feature | Prioridade | Esforco | Detalhe |
|---|---------|-----------|---------|---------|
| S1 | **Multi-vertical: templates por segmento** | P0 | 3 sem | Pacotes pre-configurados para clinica estetica, studio de unhas, pet shop. Servicos, tom de voz e fluxos especificos por vertical |
| S2 | **WhatsApp Cloud API (oficial)** | P0 | 3 sem | Migrar mensagens criticas (lembretes, confirmacoes) para API oficial da Meta. Elimina risco de ban para as funcoes mais importantes do produto |
| S3 | **Self-service signup** | P0 | 3 sem | Landing page -> cadastro -> wizard de setup -> pagamento -> Eli ativa. Sem necessidade de contato comercial para plano Starter |
| S4 | **Avaliacoes Google automatizadas** | P1 | 1.5 sem | Apos servico concluido, Eli pede avaliacao no Google. Aumenta reputacao online do negocio. Feature de altissimo valor percebido |
| S5 | **Integracao maquininha (Stone/PagBank)** | P1 | 3 sem | Dados de pagamento enriquecem o CRM: receita real por cliente, ticket medio, frequencia de compra. Dashboard mostra ROI real |
| S6 | **Relatorio de sazonalidade** | P1 | 1.5 sem | "Sextas sao 40% mais cheias que tercas. Crie uma promocao para tercar para equilibrar." Insights acionaveis com dados do proprio negocio |
| S7 | **Multi-numero (WhatsApp)** | P2 | 2 sem | Negocio com mais de 1 numero de WhatsApp (ex: recepcao + barbeiro senior). Cada numero com sua instancia |
| S8 | **Webhook/API basica** | P2 | 2 sem | Permitir integracoes customizadas via webhook. Necessario para clientes maiores que tem sistemas proprios |
| S9 | **App mobile (PWA)** | P2 | 3 sem | Dashboard acessivel pelo celular do dono. Notificacoes push para agendamentos e alertas. Donos de barbearia nao ficam no computador |

**Total estimado:** ~22 semanas de trabalho (3-4 devs = ~6-8 semanas calendario)

**Criterio de sucesso Q3:**
- 200 clientes pagantes ativos
- MRR > R$50k
- 3+ verticais ativas (barbearias, clinicas esteticas, +1)
- Self-service responsavel por >50% dos novos signups
- 0 incidentes de ban afetando funcoes criticas (lembrete/confirmacao via Cloud API)

---

### Q4 2026 (Out-Dez) -- DOMINATION: Referencia no mercado

**Objetivo:** Consolidar posicao de referencia em negocios locais de servico, preparar para rodada seed.

| # | Feature | Prioridade | Esforco | Detalhe |
|---|---------|-----------|---------|---------|
| D1 | **Benchmarks setoriais** | P0 | 2 sem | "Seu ticket medio e R$65, a media de barbearias na sua regiao e R$78. Aqui estao 3 sugestoes." So possivel com base de 200+ negocios |
| D2 | **Eli multi-idioma** | P1 | 2 sem | Suporte a espanhol para expansao LATAM. O mercado hispano tem as mesmas dores e zero solucoes verticais |
| D3 | **Marketplace de templates** | P1 | 3 sem | Fluxos pre-configurados criados pela comunidade: "Template de reativacao que converte 35%", "Campanha de Black Friday para salao" |
| D4 | **White-label basico** | P1 | 3 sem | Franquias e redes de barbearias (ex: Corleone, King's Barbershop) querem a Tikso com sua marca. Revenue multiplier |
| D5 | **API publica documentada** | P1 | 3 sem | Desenvolvedores podem construir integracoes com a Tikso. Abre canal de parceria com ERPs, contabilidades, maquininhas |
| D6 | **IA de voz (audio no WhatsApp)** | P2 | 4 sem | Eli entende e responde audios. Donos de barbearia preferem mandar audio. Diferencial massivo vs texto-only |
| D7 | **Programa de parceiros (agencies)** | P1 | 2 sem | Agencias de marketing para saloes/barbearias revendem e implementam Tikso. Canal de crescimento escalavel |

**Total estimado:** ~19 semanas de trabalho (3-4 devs = ~5-7 semanas calendario)

**Criterio de sucesso Q4:**
- 200+ clientes pagantes ativos
- MRR > R$80k
- NPS > 60
- Pelo menos 1 rede/franquia usando white-label
- Pipeline de expansao LATAM mapeado
- Metricas de unit economics prontas para apresentar em rodada seed

---

## 4. Revenue-Generating Features (Prioridade Maxima)

Estas sao as features que DIRETAMENTE aumentam o faturamento do cliente da Tikso. A logica e simples: **se o cliente fatura mais com a Tikso, ele nao cancela.**

### 4.1 Recuperacao de No-Show (Q2)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | No-show medio em barbearias/saloes: 20-30%. Para negocio com 20 agendamentos/dia, sao 4-6 perdidos |
| **Solucao** | Eli detecta no-show (horario passou, cliente nao checou) e dispara mensagem em 30min: "Oi [nome]! Vi que nao conseguiu vir hoje. Quer remarcar? Tenho [proximos 2 horarios disponiveis]" |
| **Impacto estimado** | Recuperacao de 30-40% dos no-shows = 1-2 agendamentos extras/dia = R$80-160/dia = R$1.600-3.200/mes por negocio |
| **Metricas** | Taxa de recuperacao, receita recuperada em R$, tempo medio de reagendamento |

### 4.2 Reativacao de Clientes Inativos (Q2)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Cliente medio de barbearia vai a cada 3-4 semanas. Apos 6 semanas sem aparecer, 50% nao voltam espontaneamente |
| **Solucao** | Eli identifica clientes com >30 dias sem agendamento: "Faz um tempo que voce nao aparece, [nome]! O [barbeiro preferido] tem horario [proximo dia disponivel]. Bora?" |
| **Impacto estimado** | Reativacao de 15-25% dos inativos = 5-10 clientes/mes de volta = R$400-800/mes por negocio |
| **Metricas** | Taxa de reativacao, receita reativada, LTV incremento |

### 4.3 Upsell/Cross-sell Contextual (Q2)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | 60% dos clientes pedem "so o corte" quando poderiam fazer corte + barba (ticket 50-80% maior) |
| **Solucao** | Eli sugere no momento do agendamento: "Vai querer barba tambem? O [barbeiro] ta mandando muito bem no degradezinho da barba" ou apos agendamento: "A gente tem um tratamento capilar novo que ta fazendo sucesso. Quer incluir?" |
| **Impacto estimado** | Conversao de 10-15% dos upsells = aumento de 5-8% no ticket medio = R$3-6 por agendamento = R$600-1.200/mes por negocio |
| **Metricas** | Taxa de aceite de upsell, aumento de ticket medio, receita incremental |

### 4.4 Programa de Fidelidade Automatizado (Q2)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Fidelizacao e informal ("na proxima vc ganha desconto"). Sem tracking, nenhum efeito comportamental real |
| **Solucao** | Eli gerencia programa automatico: "Voce esta no 8o corte! Faltam 2 para o gratuito." Envia lembrete proativo quando falta 1-2 para o premio |
| **Impacto estimado** | Aumento de frequencia de 15-25% entre participantes. Se 30% dos clientes aderem, impacto de R$1.000-2.000/mes por negocio |
| **Metricas** | Adesao ao programa, frequencia pre vs pos, receita incremental por membro |

### 4.5 Campanhas de Marketing via WhatsApp (Q2)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Donos querem promover ofertas mas nao sabem como, ou fazem manualmente (1 por 1) e arriscam ban |
| **Solucao** | Interface de campanha: escolher segmento (todos, inativos, aniversariantes), escrever mensagem (com sugestao da IA), programar envio. Tikso cuida do antiban automaticamente (fila, delay, variacao) |
| **Impacto estimado** | Campanha bem-feita converte 3-8% dos contatos. Para base de 500 clientes, sao 15-40 agendamentos extras = R$1.200-3.200 por campanha |
| **Metricas** | Taxa de entrega, taxa de abertura (read receipts), taxa de conversao, receita por campanha |

### 4.6 Relatorios de Receita por Canal (Q2)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Dono nao sabe quanto a Eli gera de receita vs agendamentos presenciais/telefone. Sem ROI visivel, cancela |
| **Solucao** | Dashboard: "A Eli agendou R$12.400 esse mes (45% do total). Recuperou R$1.800 em no-shows. Reativou R$640 em clientes inativos. ROI: 22x o custo da Tikso." |
| **Impacto estimado** | Nao gera receita direta, mas RETEEM o cliente. Com ROI visivel, churn cai de 8% para <4% |
| **Metricas** | Receita atribuida a Eli, ROI mensal, tempo de visualizacao do dashboard |

### Impacto combinado

Para uma barbearia tipica com 20 agendamentos/dia e ticket medio de R$70:

| Feature | Receita incremental/mes |
|---------|------------------------|
| Recuperacao de no-show | R$1.600-3.200 |
| Reativacao de inativos | R$400-800 |
| Upsell/cross-sell | R$600-1.200 |
| Programa de fidelidade | R$1.000-2.000 |
| Campanhas WhatsApp | R$1.200-3.200 (por campanha) |
| **Total estimado** | **R$4.800-10.400/mes** |

**ROI para o cliente:** Se a Tikso custa R$297/mes (plano Pro) e gera R$4.800-10.400/mes em receita incremental, o ROI e de **16x a 35x**. Esse e o argumento de venda mais poderoso possivel.

---

## 5. Modelo de Negocio e Pricing

### 5.1 Modelo de pricing

**[AUTO-DECISION]** Per seat, per contact, per message ou usage-based? -> **Pricing por tier fixo com limite de contatos** (reason: donos de negocio local odeiam pricing imprevisivel. "Per message" gera medo de conta surpresa. "Per seat" nao faz sentido para negocios de 1-3 pessoas. Tier fixo com limite de contatos e previsivel e escala naturalmente com o crescimento do negocio).

### 5.2 Tiers de Pricing

```
                STARTER              PRO                 BUSINESS
                R$97/mes             R$297/mes           R$597/mes
                --------             ---------           ----------
Contatos        500                  2.000               10.000
Usuarios        1                    3                   10
WhatsApp #s     1                    1                   3
Mensagens IA    500/mes              3.000/mes           Ilimitado
Campanhas       2/mes                Ilimitado           Ilimitado
Integracao      WhatsApp only        +BestBarbers        +Maquininha, API
Relatorios      Basico               Completo            +Benchmarks
Fidelidade      --                   Sim                 Sim
White-label     --                   --                  Sim
Suporte         Email                WhatsApp priority   Dedicado
Setup           Self-service         Assistido           White-glove
```

### 5.3 Racional de pricing

| Tier | Publico-alvo | Justificativa do preco |
|------|-------------|------------------------|
| **Starter R$97** | Barbearia solo (1 cadeira), profissional autonomo | Preco de "cafezinho por dia" (R$3.2/dia). Acessivel, baixa barreira de entrada. Limite de 500 contatos e natural para negocio pequeno |
| **Pro R$297** | Barbearia media (2-5 cadeiras), salao de beleza | Sweet spot: acessivel para negocio que fatura R$15-30k/mes, com ROI claro de 16x+. 80% dos clientes devem ficar aqui |
| **Business R$597** | Rede/franquia, clinica estetica com multiplos profissionais | Para negocios que faturam R$50k+/mes, R$597 e irrelevante se o ROI se mantem. Multi-numero e white-label justificam |

**Pricing anual:** 2 meses gratis (R$970/ano Starter, R$2.970/ano Pro, R$5.970/ano Business)

### 5.4 Add-ons

| Add-on | Preco | Disponibilidade |
|--------|-------|-----------------|
| Pacote extra de 1.000 mensagens IA | R$49/mes | Todos os tiers |
| Numero WhatsApp adicional | R$97/mes | Pro e Business |
| Integracao customizada | R$497 one-time | Business |
| Onboarding assistido | R$297 one-time | Starter e Pro |

### 5.5 Projecao de MRR (12 meses)

**Cenario conservador:**

| Mes | Starter | Pro | Business | Total Clientes | MRR |
|-----|---------|-----|----------|---------------|-----|
| Mar/26 | 5 | 3 | 0 | 8 | R$1.376 |
| Abr/26 | 8 | 5 | 1 | 14 | R$2.858 |
| Mai/26 | 12 | 10 | 1 | 23 | R$5.331 |
| Jun/26 | 15 | 15 | 2 | 32 | R$7.899 |
| Jul/26 | 18 | 22 | 3 | 43 | R$10.995 |
| Ago/26 | 20 | 30 | 5 | 55 | R$14.815 |
| Set/26 | 22 | 40 | 7 | 69 | R$19.933 |
| Out/26 | 25 | 55 | 10 | 90 | R$26.890 |
| Nov/26 | 28 | 70 | 14 | 112 | R$35.774 |
| Dez/26 | 30 | 90 | 18 | 138 | R$47.406 |
| Jan/27 | 32 | 110 | 22 | 164 | R$58.878 |
| Fev/27 | 35 | 130 | 28 | 193 | R$73.141 |

**Premissas:**
- Churn mensal: 8% no Q1, 6% no Q2, 4% no Q3-Q4 (melhora com produto + onboarding)
- Mix shift gradual de Starter para Pro conforme features de Pro justificam upgrade
- Aquisicao: 5-8 novos/mes no Q1 (manual), 10-15/mes no Q2 (referral), 15-25/mes no Q3-Q4 (self-service + referral + content)
- Upsell rate: 15% dos Starter migram para Pro em 3 meses

**Cenario otimista:** MRR de R$120k+ em Fev/2027 se referral e self-service funcionarem acima do esperado.

### 5.6 Unit Economics alvo

| Metrica | Alvo Q1 | Alvo Q4 |
|---------|---------|---------|
| CAC (custo de aquisicao) | R$200 (manual/indicacao) | R$400 (mix de canais) |
| LTV (lifetime value) | R$2.376 (8 meses * R$297) | R$4.752 (16 meses * R$297) |
| LTV:CAC ratio | 11.9x | 11.9x |
| Payback period | <1 mes | <2 meses |
| Gross margin | 85% (infra minima) | 75% (com Cloud API + suporte) |

---

## 6. Go-to-Market Strategy

### 6.1 Fase 1: Os primeiros 10 clientes (Mar/2026)

**Canal primario: Outreach manual + rede do Trimmo**

A Trimmo ja e cliente. O dono da Trimmo conhece outros donos de barbearia. A estrategia:

1. **Trimmo como case study:** Documentar resultados (agendamentos via Eli, no-shows evitados, receita gerada). Criar video curto (1 min) com depoimento do dono.

2. **Warm intro via Trimmo:** Pedir ao dono para indicar 5-10 barbearias que ele conhece. Oferecer: "1 mes gratis + setup feito por nos". O dono da Trimmo ganha desconto por indicacao.

3. **Visita presencial:** Para os primeiros 10, fazer setup presencial (ir na barbearia, configurar no celular do dono, mostrar funcionando). Isso gera confianca, feedback direto e relacao.

4. **Comunidade local:** Grupos de WhatsApp de barbeiros, feiras de beleza locais, Instagram de barbearias. Nao anuncio pago -- presenca genuina.

**Meta:** 10 clientes pagantes ate fim de Marco. 8 barbearias + 2 saloes de beleza.

### 6.2 Fase 2: De 10 para 50 (Q2 2026)

**Canais:**

| Canal | Investimento | Resultado esperado | Detalhe |
|-------|-------------|-------------------|---------|
| **Referral program** | R$0 (custo do mes gratis) | 15-20 clientes | "Indique e ganhe 1 mes gratis." Dono de barbearia fala com outros donos naturalmente |
| **Conteudo Instagram/TikTok** | 2h/semana + R$500/mes | 10-15 clientes | Videos curtos: "Como a Trimmo aumentou 30% o faturamento com IA no WhatsApp". Antes/depois. Bastidores |
| **Parceria BestBarbers** | Equity/revenue share a negociar | 5-10 clientes | BestBarbers tem base de barbearias que ja usam agendamento. Tikso como upgrade com IA |
| **Google My Business SEO** | R$0 (organico) | 3-5 clientes | Pagina otimizada para "CRM para barbearia", "agendamento WhatsApp barbearia" |
| **WhatsApp groups** | R$0 | 2-3 clientes | Participar (nao spammar) de grupos de barbeiros, oferecer valor genuino |

**Meta:** 50 clientes pagantes ate fim de Junho.

### 6.3 Fase 3: De 50 para 200 (Q3-Q4 2026)

**Escala dos canais existentes + novos:**

| Canal | Investimento | Resultado esperado |
|-------|-------------|-------------------|
| **Self-service signup** | Desenvolvimento (ja no roadmap) | 30-40% dos novos clientes vem sem contato humano |
| **Meta Ads (Instagram/Facebook)** | R$3-5k/mes | 15-25 clientes/mes. Targeting: donos de negocio local, segmento beleza |
| **Content marketing (blog + YouTube)** | 4h/semana | SEO de longo prazo: "como reduzir no-show na barbearia", "WhatsApp para salao de beleza" |
| **Programa de parceiros (agencies)** | Revenue share 20% | Agencias de marketing que atendem saloes revendem Tikso. Canal escalavel |
| **Feiras e eventos** | R$2-5k por evento | Presenca em feiras de beleza (Beauty Fair, Hair Brasil). Stand com demo ao vivo |
| **Case studies video** | R$500/video | 1 video/mes com cliente real mostrando resultados. Social proof poderoso |

**Meta:** 200 clientes pagantes ate fim de Dezembro.

### 6.4 Estrategia vertical-first

**Por que vertical-first e critico para GTM:**

1. **Messaging claro:** "CRM para barbearia" e infinitamente mais claro que "CRM para negocios locais". O dono pensa "isso e pra mim".

2. **Community effect:** Barbeiros se conhecem. Feirantes de beleza se conhecem. Um nicho bem atendido gera referral exponencial.

3. **Product-market fit profundo:** Features especificas (ex: "tempo de servico por tipo de corte") mostram que voce entende o negocio. Generalistas nunca tem isso.

4. **Preco de referencia:** Em conversa com barbeiros, "R$297/mes" se compara com "custo de 4 cortes". Facil justificar. Em comparacao generica, R$297 vira "mais uma assinatura".

5. **Expansao natural:** Donos de barbearia frequentemente tem esposas/amigos com salao de beleza, clinica estetica. A expansao vertical vem organicamente.

### 6.5 Partnerships estrategicas

| Parceiro | Tipo | Valor para Tikso | Valor para parceiro | Timing |
|----------|------|-----------------|--------------------|----|
| **BestBarbers** | Integracao + co-marketing | Base de clientes, agenda integrada | Oferece IA como upgrade, sticky factor | Q1-Q2 |
| **Trinks** | Integracao | Base de saloes de beleza | Mesma logica do BestBarbers | Q2 |
| **Evolution API** | Tecnologia | Infra de WhatsApp, community | Case study "Tikso usa Evolution API" | Ja existe |
| **Stone/PagBank** | Integracao | Dados de pagamento, credibilidade | Mais valor para sua base de PMEs | Q3 |
| **Sebrae** | Educacional | Acesso a rede de PMEs, credibilidade | Oferece solucao de IA para seus atendidos | Q3-Q4 |
| **Agencias de marketing para saloes** | Revenue share | Canal de distribuicao escalavel | Ferramenta que agrega valor ao servico deles | Q4 |

---

## 7. Competitive Positioning

### 7.1 Mapa competitivo

```
                    ENTERPRISE
                        |
                   Respond.io
                        |
             Kommo     |
                |       |
                |       |              AwSales
   GENERALISTA -+-------+-------+-------+-- ESPECIALISTA
                |       |       |
                |       |    TIKSO (alvo)
                |       |       |
          BotConversa   |       |
                        |    BestBarbers
                        |       |
                    PME/LOCAL
```

**Posicao-alvo da Tikso:** Quadrante inferior-direito. PME/Local + Especialista. Nenhum player domina esse quadrante.

### 7.2 Comparativo direto

| Capacidade | Tikso | Kommo | Respond.io | AwSales | BestBarbers |
|-----------|-------|-------|------------|---------|-------------|
| CRM conversacional | Sim | Sim | Sim | Parcial | Nao |
| IA generativa (LLM) | Sim (Claude) | Nao (fluxos) | Sim | Sim (provavelmente GPT) | Nao |
| Especializado em servico local | **SIM** | Nao | Nao | Nao (infoprodutos) | Parcial (so agenda) |
| Agendamento integrado | Sim | Plugin | Plugin | Sim | **SIM** |
| WhatsApp nativo | Sim | Sim | Sim | Sim | Nao (app) |
| Preco para PME | **R$97-597** | US$15-299 | US$79-599 | Custom (caro) | R$49-199 |
| Setup < 15 min | **Alvo** | Nao (complexo) | Nao (complexo) | Nao (consultivo) | Sim |
| Dashboard de ROI em R$ | **Sim** | Nao | Nao | Parcial | Nao |
| Portugues nativo | **Sim** | Traduzido | Ingles | Sim | Sim |
| Suporte em portugues | **Sim** | Parcial | Nao | Sim | Sim |

### 7.3 Contra cada concorrente

**vs Kommo:**
- Kommo e caro (US$15-299 = R$75-1.500), complexo de configurar, generalista
- Tikso e 3x mais barato, setup em 15 min, feito para negocio local brasileiro
- Messaging: "Kommo e para empresas de vendas. Tikso e para quem atende cliente pessoalmente"

**vs Respond.io:**
- Respond.io e enterprise (US$79+), em ingles, zero foco em servico local
- Tikso e brasileira, fala portugues, entende barbearia/salao
- Messaging: "Respond.io e para call center. Tikso e para quem quer faturar mais no WhatsApp sem complicacao"

**vs AwSales:**
- AwSales foca em infoprodutos/e-commerce, pricing enterprise, vendas consultivas
- Tikso foca em negocio local de servico, pricing acessivel, self-service
- Messaging: "AwSales e para influenciador digital. Tikso e para dono de barbearia que quer mais clientes voltando"

**vs BestBarbers:**
- BestBarbers e puro agendamento, sem IA, sem CRM, sem WhatsApp conversacional
- Tikso faz tudo que BestBarbers faz + IA + CRM + campanhas + WhatsApp
- Messaging: "BestBarbers e uma agenda. Tikso e sua funcionaria mais inteligente que nunca falta"

### 7.4 USP (Unique Selling Proposition)

**Uma frase:**

> "A Tikso e a funcionaria de atendimento que nunca falta, nunca esquece e faz seu negocio faturar mais pelo WhatsApp."

**Versao expandida (elevator pitch):**

> "Imagina ter uma funcionaria que atende seus clientes no WhatsApp 24 horas, agenda automaticamente, lembra de confirmar, liga de volta quando alguem nao aparece, e ainda sugere servicos extras. E voce so paga R$297 por mes. Isso e a Tikso."

**Versao para anuncio (5 segundos):**

> "Sua barbearia perdendo cliente por nao responder WhatsApp? A Eli resolve."

### 7.5 Messaging Framework

| Contexto | Mensagem principal | Prova |
|----------|-------------------|-------|
| Landing page hero | "Sua IA de atendimento que faz seu negocio faturar mais" | "A Trimmo aumentou 30% o faturamento em 60 dias" |
| Para barbeiro cetico | "Nao e chatbot. E como ter uma recepcionista que conhece cada cliente" | Demo ao vivo agendando |
| Para quem usa BestBarbers | "Mantenha sua agenda. Adicione IA que atende pelo WhatsApp" | Integracao mostrando dados sincronizados |
| Para quem nao tem nada | "Setup em 15 minutos. Primeiro agendamento via IA em 24 horas" | Video de setup real |
| Para quem tem medo de IA | "A Eli aprende com voce. Se ela nao souber algo, transfere pra voce na hora" | Demo de escalacao para humano |
| Redes sociais | "X clientes recuperados. Y agendamentos feitos pela Eli. Z reais a mais no caixa" | Screenshots do dashboard |

---

## 8. Riscos e Mitigacoes

| # | Risco | Probabilidade | Impacto | Mitigacao |
|---|-------|--------------|---------|-----------|
| R1 | **Ban do WhatsApp** por uso de API nao-oficial (Evolution API) | ALTA (30-50% em 3 meses por numero) | CRITICO -- produto para de funcionar | Migrar funcoes criticas para Cloud API oficial (Q3). Manter Evolution apenas para funcoes de baixo risco. Antiban robusto (implementado no Q1) |
| R2 | **Churn alto** nos primeiros 3 meses por produto imaturo | MEDIO (40-60% sem as fixes do Q1) | ALTO -- mata unit economics | Priorizar fixes de Eli (F1-F4) antes de vender. Onboarding assistido nos primeiros 30 clientes |
| R3 | **Time muito pequeno** (1-3 devs) para roadmap ambicioso | ALTA | ALTO -- atrasos em tudo | Priorizar ruthlessly. Cada quarter tem 3-4 features core, resto e stretch. Contratar dev #3 no Q2 com MRR |
| R4 | **Concorrente vertical** entra no mercado (ex: BestBarbers adiciona IA) | MEDIA | ALTO -- perde diferencial | Speed matters. Cada mes de vantagem cria mais data moat. Integrar com BestBarbers (se nao pode vencer, junte-se) |
| R5 | **Custo de Claude API** escala mais rapido que receita | MEDIA | MEDIO -- margem shrinks | Otimizar prompts agressivamente. Cache de respostas comuns. Usar modelo menor (Haiku) para tarefas simples |
| R6 | **Regulacao de WhatsApp** fica mais restritiva | MEDIA | MEDIO -- limita funcionalidade | Ja mitigado parcialmente pela migracao para Cloud API. Diversificar para Instagram DM, SMS |
| R7 | **Dono de barbearia nao adota tecnologia** | MEDIA | MEDIO -- TAM menor que estimado | Onboarding extremamente simples (15 min). Videos explicativos. Setup presencial nos primeiros 20 clientes |
| R8 | **Dependencia de infraestrutura single-server** (Vultr) | MEDIA | ALTO -- downtime = todos os clientes afetados | Q2: migrar para infra com redundancia. Health monitoring desde Q1 |

### Matriz de risco

```
  IMPACTO
   ALTO  | R1  R2  R4  R8 |
         |                  |
  MEDIO  | R3  R5  R6  R7  |
         |                  |
  BAIXO  |                  |
         +------------------+
           MEDIA      ALTA
               PROBABILIDADE
```

**Risco #1 (Ban do WhatsApp) e o existential risk.** A mitigacao primaria (Cloud API para funcoes criticas no Q3) deve ser antecipada se houver incidentes nos primeiros meses.

---

## 9. Metricas de Sucesso (KPIs)

### 9.1 North Star Metric

**"Receita gerada pela Eli por cliente por mes"**

Essa metrica captura tudo: se a Eli esta agendando, se o negocio esta faturando, se o produto entrega valor real. Alvo: > R$3.000/mes por cliente (10x o custo do plano Pro).

### 9.2 KPIs por area

| Area | KPI | Meta Q1 | Meta Q2 | Meta Q3 | Meta Q4 |
|------|-----|---------|---------|---------|---------|
| **Revenue** | MRR | R$2k | R$8k | R$20k | R$50k+ |
| **Revenue** | Clientes pagantes | 10 | 50 | 120 | 200+ |
| **Revenue** | ARPU | R$200 | R$250 | R$280 | R$300 |
| **Product** | Taxa de agendamento via Eli | >75% | >85% | >85% | >90% |
| **Product** | Tempo setup ate 1o agendamento | <24h | <12h | <6h | <3h |
| **Product** | No-show rate dos clientes Tikso | <25% | <15% | <12% | <10% |
| **Retention** | Churn mensal | <10% | <7% | <5% | <4% |
| **Retention** | NPS | >30 | >45 | >55 | >60 |
| **Retention** | Retencion 90 dias | >60% | >70% | >80% | >85% |
| **Growth** | Novos clientes/mes | 8 | 15 | 25 | 30 |
| **Growth** | % via referral | -- | >30% | >35% | >40% |
| **Infra** | Uptime | >99% | >99.5% | >99.9% | >99.9% |
| **Infra** | Incidentes de ban WhatsApp | 0 | <2 | 0 (Cloud API) | 0 |

---

## 10. Decisoes Pendentes e Proximos Passos

### Decisoes que precisam do fundador

| # | Decisao | Opcoes | Recomendacao | Impacto |
|---|---------|--------|-------------|---------|
| D1 | Pricing: confirmar tiers | R$97/R$297/R$597 vs alternativa | Manter como proposto, validar com 5 clientes antes de fixar | Direto no MRR |
| D2 | Nome da IA: manter "Eli"? | Eli, outro nome, ou personalizavel por negocio | Manter Eli como default, permitir customizacao no Business | Brand |
| D3 | Cloud API vs Evolution API: quando migrar | Q2 (mais cedo) vs Q3 (conforme roadmap) | Q3, exceto se ban ocorrer em cliente nos primeiros 30 dias | Risco existencial |
| D4 | Contratacao: dev #3 quando | Agora vs com MRR > R$5k | Com MRR > R$5k (Jun/2026). Ate la, focar no core com 2 devs | Velocity de roadmap |
| D5 | Brand: qual conceito de logo | Concept 1 (Pulse), 2 (Tik Link), 3 (Folded T) | Concept 1 (Pulse Mark), conforme recomendacao do brand doc | Identidade visual |
| D6 | Vertical: so barbearias ou incluir saloes desde Q1 | Barbearias only vs beleza amplo | Beleza amplo desde Q1 (mesmo workflow, templates diferentes) | TAM |

### Proximos passos imediatos

1. **Semana 1 (Mar/2026):** Fixar bugs criticos da Eli (F1-F4). Zero vendas ate Eli funcionar sem falhas
2. **Semana 2-3:** Implementar antiban P0 (F5). Sem isso, qualquer cliente novo arrisca perder o numero
3. **Semana 3-4:** Dashboard de receita v1 (F6) + inteligencia de cliente basica (F7)
4. **Semana 4-5:** Tom de voz (F8) + onboarding wizard (F9)
5. **Semana 6:** Primeiro pitch para 5 barbearias indicadas pela Trimmo. Oferecer 30 dias gratis
6. **Semana 7-8:** Iterar com feedback dos primeiros clientes. Corrigir o que quebrar
7. **Semana 9-10:** Comecar a cobrar. 10 clientes pagantes como validacao de product-market fit

---

## Anexo A: Analise Financeira Detalhada

### Custos mensais estimados

| Item | Q1 | Q2 | Q3 | Q4 |
|------|----|----|----|----|
| Infra (Vultr/Cloud) | R$200 | R$500 | R$1.500 | R$3.000 |
| Claude API (Anthropic) | R$300 | R$1.500 | R$4.000 | R$8.000 |
| WhatsApp Cloud API | R$0 | R$0 | R$1.000 | R$3.000 |
| Evolution API (hosting) | R$100 | R$200 | R$300 | R$300 |
| Dominio + Email + SaaS tools | R$200 | R$300 | R$500 | R$800 |
| Marketing (ads + content) | R$0 | R$1.500 | R$5.000 | R$10.000 |
| Time (salarios/freelancers) | R$0* | R$5.000* | R$15.000 | R$30.000 |
| **Total** | **R$800** | **R$9.000** | **R$27.300** | **R$55.100** |

*Q1-Q2: fundador(es) nao retiram pro-labore. Investem tempo.

### Break-even

| Cenario | MRR necessario | Quando |
|---------|---------------|--------|
| Solo (sem time) | R$800 | Mar/2026 (8 clientes Starter) |
| Com 1 dev contratado | R$5.800 | Jun/2026 (~20 clientes) |
| Com time completo (5 pessoas) | R$27.300 | Set/2026 (~100 clientes) |
| Lucratividade 30%+ | R$55.100 * 1.3 = R$71.630 | Dez/2026-Jan/2027 (~170 clientes) |

---

## Anexo B: Glossario

| Termo | Definicao |
|-------|-----------|
| **Eli** | IA conversacional da Tikso. Opera como "funcionaria virtual" de atendimento |
| **PULSE** | Agente do sistema responsavel por mensagens proativas (follow-up, lembretes, reativacao) |
| **Antiban** | Conjunto de tecnicas para evitar banimento do numero de WhatsApp |
| **Evolution API** | API open-source para WhatsApp (nao-oficial, via Baileys) |
| **Cloud API** | API oficial da Meta para WhatsApp Business |
| **No-show** | Cliente que agendou mas nao compareceu |
| **MRR** | Monthly Recurring Revenue (receita recorrente mensal) |
| **ARPU** | Average Revenue Per User (receita media por usuario) |
| **CAC** | Customer Acquisition Cost (custo de aquisicao de cliente) |
| **LTV** | Lifetime Value (valor total que um cliente gera durante sua vida) |
| **Churn** | Taxa de cancelamento mensal |
| **NPS** | Net Promoter Score (indicador de satisfacao) |
| **TAM** | Total Addressable Market (mercado total enderecavel) |
| **RICE** | Framework de priorizacao: Reach, Impact, Confidence, Effort |

---

*-- Morgan, planejando o futuro*

*Documento gerado em 2026-02-25. Baseado em dados de pesquisa competitiva (AwSales, Kommo, Respond.io), analise de produto (conversa Eli/Kelmer), pesquisa antiban, e principios de product strategy.*
