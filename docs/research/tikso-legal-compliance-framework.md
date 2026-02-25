# Framework Juridico Completo -- Tikso CRM

**Data:** 2026-02-25
**Autor:** Legal Chief (AIOS Legal Squad)
**Versao:** 1.0
**Status:** Analise orientativa

---

## SUMARIO EXECUTIVO

A Tikso e um CRM brasileiro com IA conversacional (chatbot "Eli") que atende clientes via WhatsApp. Este framework mapeia TODAS as obrigacoes juridicas, riscos e acoes necessarias para operar legalmente no Brasil e preparar expansao internacional.

**Nivel de Risco Geral: ALTO** -- A combinacao de IA + dados pessoais + WhatsApp + relacoes B2B2C cria uma superficie de exposicao juridica significativa que exige framework robusto.

### Prioridades Imediatas (0-30 dias)

| Prioridade | Acao | Risco se Ignorar |
|-----------|------|-------------------|
| P0 | Politica de Privacidade + Termos de Uso | Multa ANPD ate R$50M |
| P0 | Disclosure de IA no atendimento | Violacao transparencia (LGPD + PL IA) |
| P0 | Compliance WhatsApp Business API (ban chatbot generico) | Banimento da plataforma |
| P1 | DPA (Data Processing Agreement) com clientes | Exposicao contratual |
| P1 | Registro de marca "Tikso" no INPI | Perda de direito sobre a marca |
| P2 | ROPA (Registro de Atividades de Tratamento) | Multa em fiscalizacao |
| P2 | Contrato SaaS completo (ToS + SLA) | Disputas contratuais |

---

## 1. LGPD -- LEI GERAL DE PROTECAO DE DADOS

### 1.1 Enquadramento da Tikso

A Tikso opera em uma cadeia de tratamento de dados com TRES atores:

```
[Titular dos Dados]     [Cliente Tikso]        [Tikso]
  (consumidor final) --> (controlador) -------> (operador/processador)
                         usa CRM Tikso          processa dados em nome
                         para atender            do cliente
                         seus clientes
```

**Classificacao juridica:**
- **Tikso como OPERADOR (Processador):** Quando processa dados pessoais dos consumidores finais em nome dos seus clientes (empresas que contratam o CRM)
- **Tikso como CONTROLADOR:** Quando coleta dados dos proprios clientes (empresas), dados de uso da plataforma, analytics, e dados para treinamento/melhoria da IA

### 1.2 Bases Legais Aplicaveis

| Atividade de Tratamento | Base Legal | Artigo LGPD | Justificativa |
|------------------------|------------|-------------|---------------|
| Atendimento via chatbot Eli | Execucao de contrato (art. 7o, V) | Art. 7 | Necessario para prestar o servico contratado |
| Armazenamento de conversas | Execucao de contrato + Legitimo interesse | Art. 7, V e IX | Historico de atendimento e melhoria do servico |
| Analytics de uso da plataforma | Legitimo interesse | Art. 7, IX | Melhoria do produto, desde que anonimizado |
| Treinamento de modelos de IA | Consentimento | Art. 7, I | Requer opt-in explicito; dados anonimizados preferencialmente |
| Marketing direto (Tikso para leads) | Legitimo interesse | Art. 7, IX | Sujeito a opt-out imediato conforme Guia ANPD |
| Dados sensiveis (saude, religiao) | Consentimento especifico | Art. 11 | Se clientes da Tikso atuam em saude, por exemplo |
| Transferencia internacional | Clausulas contratuais padrao | Art. 33 | Se dados transitam por servidores fora do BR |

**ATENCAO sobre Legitimo Interesse:**
Conforme o Guia Orientativo da ANPD (fev/2024), o uso de legitimo interesse exige:
1. Teste de balanceamento em 3 fases: finalidade, necessidade, balanceamento e salvaguardas
2. NAO se aplica a dados sensiveis
3. O titular pode se opor a qualquer momento ao tratamento para marketing direto

### 1.3 Quando e OBRIGATORIO Informar que e IA Atendendo?

**Resposta curta: SEMPRE.**

Fundamentacao juridica multipla:

1. **LGPD Art. 20:** O titular tem direito a solicitar revisao de decisoes tomadas unicamente com base em tratamento automatizado. Logo, deve saber que esta interagindo com IA.

2. **PL 2338/2023 (Marco da IA):** Exige transparencia sobre sistemas de IA. O texto aprovado pelo Senado determina que o usuario deve ser informado quando interage com um sistema de IA.

3. **CDC Art. 6o, III:** Direito a informacao adequada e clara sobre produtos e servicos. Omitir que o atendimento e feito por IA constitui falha de informacao.

4. **Principio da Boa-Fe Objetiva (CC Art. 422):** Omitir a natureza automatizada do atendimento viola o dever de transparencia nas relacoes contratuais.

**Implementacao obrigatoria para a Tikso:**

```
MENSAGEM INICIAL OBRIGATORIA (exemplo):
"Ola! Eu sou a Eli, assistente virtual da [Nome da Empresa].
Posso ajudar com [X, Y, Z]. Se preferir falar com um
atendente humano, digite HUMANO a qualquer momento."
```

**Requisitos minimos do disclosure:**
- [ ] Identificar que e uma IA/assistente virtual
- [ ] Informar o que a IA pode fazer (escopo)
- [ ] Oferecer caminho para atendente humano
- [ ] Estar na PRIMEIRA mensagem da conversa
- [ ] Estar em portugues claro e acessivel

### 1.4 Direitos dos Titulares (SARR)

A Tikso DEVE implementar mecanismos para que os titulares exerçam:

| Direito | Artigo | Implementacao na Tikso |
|---------|--------|----------------------|
| Confirmacao de tratamento | Art. 18, I | Canal de atendimento (email/formulario) |
| Acesso aos dados | Art. 18, II | Exportacao de dados do CRM |
| Correcao | Art. 18, III | Edicao no perfil do contato |
| Anonimizacao/bloqueio/eliminacao | Art. 18, IV | Funcionalidade de "esquecer contato" |
| Portabilidade | Art. 18, V | Exportacao em formato padrao (CSV/JSON) |
| Eliminacao com consentimento | Art. 18, VI | Processo automatizado de exclusao |
| Informacao sobre compartilhamento | Art. 18, VII | Listagem de integrações ativas |
| Revogacao de consentimento | Art. 18, IX | Toggle em configuracoes |
| Revisao de decisao automatizada | Art. 20 | Escalacao para humano |

**SLA de resposta:** 15 dias (conforme LGPD), recomendado 5 dias uteis.

### 1.5 Modelo de Politica de Privacidade

```markdown
# POLITICA DE PRIVACIDADE -- TIKSO

Ultima atualizacao: [DATA]

## 1. QUEM SOMOS
Tikso e uma plataforma de CRM com inteligencia artificial que
auxilia empresas no atendimento ao cliente via WhatsApp e outros canais.
[Razao social, CNPJ, endereco]

## 2. DADOS QUE COLETAMOS

### 2.1 Dados dos Clientes (Empresas)
- Dados cadastrais: nome, email, CNPJ, telefone
- Dados de pagamento: informacoes de cobranca (processadas por [gateway])
- Dados de uso: logs de acesso, funcionalidades utilizadas, metricas

### 2.2 Dados dos Consumidores Finais (tratados em nome dos Clientes)
- Dados de identificacao: nome, telefone (WhatsApp)
- Dados de conversa: historico de mensagens com o chatbot e atendentes
- Dados comportamentais: preferencias, historico de interacoes
- Metadados: horarios de acesso, dispositivo, localizacao aproximada

### 2.3 Dados coletados automaticamente
- Cookies e tecnologias similares (na plataforma web)
- Logs de sistema e dados de performance

## 3. COMO USAMOS SEUS DADOS

| Finalidade | Base Legal | Dados Utilizados |
|-----------|------------|------------------|
| Prestacao do servico de CRM | Execucao contratual | Cadastrais, conversas |
| Melhoria da IA e algoritmos | Legitimo interesse* | Dados anonimizados |
| Comunicacao sobre o servico | Execucao contratual | Email, telefone |
| Marketing e novidades | Legitimo interesse | Email (com opt-out) |
| Cumprimento de obrigacoes legais | Obrigacao legal | Conforme exigido |
| Seguranca e prevencao a fraude | Legitimo interesse | Logs, metadados |

*Para treinamento de IA com dados nao-anonimizados, sera solicitado
consentimento especifico.

## 4. INTELIGENCIA ARTIFICIAL
A Tikso utiliza inteligencia artificial ("Eli") para auxiliar
no atendimento ao cliente. Informamos que:
- O chatbot Eli e identificado como IA em toda interacao
- Decisoes automatizadas podem ser revisadas por humanos
- O titular pode solicitar atendimento humano a qualquer momento
- Dados de conversas podem ser utilizados, de forma anonimizada,
  para melhorar a qualidade das respostas

## 5. COMPARTILHAMENTO DE DADOS
Compartilhamos dados com:
- Provedores de infraestrutura (hospedagem, CDN)
- Gateway de pagamento
- WhatsApp/Meta (para entrega de mensagens)
- Provedores de IA (processamento de linguagem natural)
Todos vinculados por acordos de protecao de dados (DPA).

## 6. TRANSFERENCIA INTERNACIONAL
[Se aplicavel] Dados podem ser transferidos para servidores em
[paises], com salvaguardas conforme Art. 33 da LGPD:
- Clausulas contratuais padrao
- Certificacao de adequacao do pais receptor

## 7. SEGURANCA
Implementamos medidas tecnicas e administrativas:
- Criptografia em transito (TLS 1.3) e em repouso (AES-256)
- Controle de acesso baseado em funcao (RBAC)
- Logs de auditoria
- Backups automatizados
- Testes de seguranca periodicos

## 8. RETENCAO DE DADOS
- Dados de conta: durante vigencia do contrato + 5 anos
- Conversas: conforme configuracao do cliente (padrao: 2 anos)
- Logs de sistema: 1 ano
- Dados anonimizados: sem prazo definido (nao sao dados pessoais)

## 9. SEUS DIREITOS
Voce tem direito a: confirmacao, acesso, correcao, anonimizacao,
portabilidade, eliminacao, informacao sobre compartilhamento,
revogacao de consentimento, e revisao de decisao automatizada.

Exerca seus direitos em: privacidade@tikso.com.br
Prazo de resposta: 15 dias.

## 10. ENCARREGADO (DPO)
[Nome do Encarregado]
Email: dpo@tikso.com.br

## 11. ALTERACOES
Esta politica pode ser atualizada. Notificaremos por email
sobre mudancas relevantes.

## 12. CONTATO E RECLAMACOES
- Tikso: privacidade@tikso.com.br
- ANPD: www.gov.br/anpd
```

### 1.6 Modelo de Termos de Uso

```markdown
# TERMOS DE USO -- PLATAFORMA TIKSO

Ultima atualizacao: [DATA]

## 1. ACEITE
Ao acessar e usar a plataforma Tikso, voce concorda com estes
Termos. Se nao concordar, nao utilize o servico.

## 2. DEFINICOES
- "Plataforma": o software SaaS Tikso, incluindo API, dashboard
  e integrações
- "Cliente": pessoa juridica que contrata a Tikso
- "Usuario": colaborador do Cliente que acessa a plataforma
- "Consumidor Final": pessoa que interage com o Cliente via
  canais atendidos pela Tikso
- "Eli": assistente virtual com inteligencia artificial da Tikso
- "Dados": quaisquer dados pessoais tratados na plataforma

## 3. SERVICOS
A Tikso oferece:
a) CRM para gestao de relacionamento com clientes
b) Integracao com WhatsApp Business API
c) Chatbot com IA (Eli) para atendimento automatizado
d) Dashboard analitico
e) Automacoes de mensagens e workflows

## 4. OBRIGACOES DO CLIENTE
O Cliente se compromete a:
a) Obter consentimento/base legal para tratamento de dados
   dos seus consumidores finais
b) Informar seus consumidores sobre o uso de IA no atendimento
c) Cumprir as politicas do WhatsApp Business
d) Nao utilizar a plataforma para spam, assedio ou fraude
e) Manter suas credenciais seguras
f) Cumprir a legislacao aplicavel (LGPD, CDC, Marco Civil)

## 5. USO ACEITAVEL
E PROIBIDO usar a Tikso para:
a) Enviar mensagens nao solicitadas (spam)
b) Conteudo ilegal, discriminatorio ou difamatorio
c) Engenharia reversa da IA ou da plataforma
d) Compartilhar credenciais com terceiros nao autorizados
e) Exceder limites de uso do plano contratado
f) Uso que viole a politica do WhatsApp Business

## 6. INTELIGENCIA ARTIFICIAL (ELI)
6.1 O chatbot Eli utiliza modelos de IA para gerar respostas.
6.2 Respostas da IA sao ORIENTATIVAS e podem conter imprecisoes.
6.3 O Cliente e responsavel por supervisionar e configurar a IA.
6.4 A Tikso nao garante acuracia de 100% das respostas da IA.
6.5 Decisoes criticas devem envolver supervisao humana.
6.6 A Tikso pode utilizar dados ANONIMIZADOS de conversas para
    melhorar os modelos de IA.

## 7. PROPRIEDADE INTELECTUAL
7.1 A plataforma Tikso, incluindo software, IA, marca e design,
    sao propriedade exclusiva da Tikso.
7.2 O Cliente retem propriedade sobre seus dados e conteudo.
7.3 Conversas entre o Cliente e seus consumidores pertencem
    ao Cliente.
7.4 O Cliente concede a Tikso licenca limitada para processar
    os dados conforme necessario para prestar o servico.
7.5 Dados anonimizados e agregados podem ser utilizados pela
    Tikso para melhoria de produto e benchmarks.

## 8. DISPONIBILIDADE E SLA
8.1 A Tikso se compromete com disponibilidade de 99.5% mensal
    (excluindo manutencoes programadas).
8.2 Manutencoes programadas serao comunicadas com 48h de
    antecedencia.
8.3 Em caso de indisponibilidade acima do SLA, o Cliente tera
    credito proporcional conforme tabela do SLA.

## 9. PAGAMENTO
9.1 Cobranca mensal/anual conforme plano contratado.
9.2 Reajuste anual pelo IGPM ou IPCA.
9.3 Atraso superior a 15 dias: suspensao do servico.
9.4 Atraso superior a 60 dias: rescisao e exclusao dos dados.

## 10. LIMITACAO DE RESPONSABILIDADE
10.1 A Tikso NAO se responsabiliza por:
     a) Decisoes tomadas com base em respostas da IA
     b) Conteudo gerado pelo Cliente ou seus consumidores
     c) Indisponibilidade do WhatsApp ou terceiros
     d) Danos indiretos, lucros cessantes ou danos morais
     e) Uso em desacordo com estes Termos

10.2 A responsabilidade total da Tikso esta limitada ao valor
     pago pelo Cliente nos ultimos 12 meses.

10.3 IMPORTANTE: Esta limitacao nao se aplica a:
     a) Violacoes da LGPD (responsabilidade solidaria)
     b) Dolo ou culpa grave
     c) Danos ao consumidor final (CDC)

## 11. RESCISAO
11.1 Qualquer parte pode rescindir com 30 dias de aviso.
11.2 Rescisao por justa causa: imediata, sem aviso.
11.3 Apos rescisao: dados disponiveis para exportacao por 30 dias,
     apos os quais serao permanentemente excluidos.

## 12. CONFIDENCIALIDADE
12.1 Ambas as partes manterao sigilo sobre informacoes
     confidenciais por 5 anos apos o termino do contrato.

## 13. LEI APLICAVEL E FORO
13.1 Estes Termos sao regidos pela lei brasileira.
13.2 Foro: comarca de [cidade sede da Tikso].
13.3 As partes concordam em tentar mediacao antes de litigio.
```

### 1.7 Modelo de DPA (Data Processing Agreement)

```markdown
# ACORDO DE PROCESSAMENTO DE DADOS (DPA)
# DATA PROCESSING AGREEMENT

Entre:
CONTROLADOR: [Cliente], inscrito no CNPJ [X]
OPERADOR: Tikso Tecnologia Ltda., inscrita no CNPJ [X]

## 1. OBJETO
Este acordo regula o tratamento de dados pessoais realizado
pelo Operador em nome do Controlador, conforme a LGPD.

## 2. DADOS TRATADOS

| Categoria | Tipos de Dados | Titulares |
|----------|---------------|-----------|
| Identificacao | Nome, telefone, email | Consumidores do Controlador |
| Conversas | Mensagens de texto, audio, imagens | Consumidores do Controlador |
| Comportamentais | Historico de interacoes, preferencias | Consumidores do Controlador |
| Metadados | IP, horarios, dispositivo | Consumidores do Controlador |

## 3. FINALIDADE
O Operador tratara os dados EXCLUSIVAMENTE para:
a) Prestacao do servico de CRM contratado
b) Funcionamento do chatbot com IA
c) Geracao de relatorios e analytics para o Controlador
d) Suporte tecnico

## 4. OBRIGACOES DO OPERADOR (TIKSO)
4.1 Tratar dados apenas conforme instrucoes documentadas
4.2 Garantir que pessoas autorizadas estejam sob
    confidencialidade
4.3 Implementar medidas de seguranca tecnicas e organizacionais
4.4 Nao subcontratar sem autorizacao previa por escrito
4.5 Auxiliar o Controlador no atendimento a direitos dos titulares
4.6 Notificar incidentes de seguranca em ate 48 horas
4.7 Ao termino do contrato, devolver ou excluir os dados
4.8 Disponibilizar informacoes para auditorias

## 5. SUBOPERADORES AUTORIZADOS

| Suboperador | Servico | Localizacao |
|------------|---------|-------------|
| [Cloud Provider] | Hospedagem | Brasil / [Pais] |
| Meta/WhatsApp | Entrega de mensagens | EUA |
| [AI Provider] | Processamento de linguagem | [Pais] |
| [Payment Gateway] | Cobrancas | Brasil |

Mudancas nos suboperadores serao comunicadas com 30 dias
de antecedencia, permitindo objecao pelo Controlador.

## 6. TRANSFERENCIA INTERNACIONAL
[Se aplicavel]
6.1 Dados podem ser transferidos para [paises]
6.2 Salvaguardas: clausulas contratuais padrao da ANPD
6.3 O Controlador autoriza a transferencia para os
    suboperadores listados na clausula 5.

## 7. SEGURANCA
O Operador implementa:
- Criptografia AES-256 em repouso
- TLS 1.3 em transito
- RBAC (controle de acesso por funcao)
- MFA para acesso administrativo
- Backup diario com retencao de 30 dias
- Logs de auditoria com retencao de 1 ano
- Testes de penetracao anuais

## 8. NOTIFICACAO DE INCIDENTES
8.1 Notificacao ao Controlador: ate 48 horas
8.2 Conteudo minimo: natureza do incidente, dados afetados,
    medidas adotadas, ponto de contato
8.3 Cooperacao na notificacao a ANPD e titulares

## 9. DIREITOS DOS TITULARES
9.1 O Operador auxiliara o Controlador no atendimento
9.2 Solicitacoes diretas ao Operador serao redirecionadas
    ao Controlador em ate 24 horas
9.3 Implementacao tecnica para: acesso, correcao, exclusao,
    portabilidade

## 10. AUDITORIA
10.1 O Controlador pode auditar o Operador com aviso de 30 dias
10.2 Alternativa: relatorios de auditoria independente (SOC 2)
10.3 Custos da auditoria: do Controlador (exceto se identificada
     nao-conformidade)

## 11. VIGENCIA
Este DPA vigora enquanto durar o contrato principal.
Sobrevivem: clausulas de confidencialidade e retorno/exclusao
de dados.

## 12. RESPONSABILIDADE
12.1 O Operador responde por danos causados por tratamento em
     desacordo com as instrucoes do Controlador ou com a LGPD.
12.2 Limitacao: conforme contrato principal (exceto dolo/culpa grave).
```

### 1.8 ROPA -- Registro de Atividades de Tratamento

Modelo baseado no template da ANPD para agentes de pequeno porte:

```markdown
# REGISTRO DE ATIVIDADES DE TRATAMENTO (ROPA)
# TIKSO TECNOLOGIA LTDA.

Data de elaboracao: [DATA]
Responsavel: [DPO / Encarregado]

---

## ATIVIDADE 1: Cadastro de Clientes (Empresas)
- **Controlador:** Tikso
- **Categorias de titulares:** Representantes legais de empresas
- **Dados tratados:** Nome, email, telefone, CNPJ, cargo
- **Finalidade:** Prestacao do servico SaaS
- **Base legal:** Execucao de contrato (Art. 7, V)
- **Compartilhamento:** Gateway de pagamento, plataforma email
- **Transferencia internacional:** Nao [ou Sim: qual pais]
- **Medidas de seguranca:** Criptografia, RBAC, MFA
- **Prazo de retencao:** Vigencia do contrato + 5 anos
- **Forma de eliminacao:** Exclusao logica + anonimizacao

## ATIVIDADE 2: Tratamento de Dados via CRM (como Operador)
- **Controlador:** Cliente da Tikso (empresa contratante)
- **Operador:** Tikso
- **Categorias de titulares:** Consumidores finais do Cliente
- **Dados tratados:** Nome, telefone, historico de conversas,
  preferencias, metadados de interacao
- **Finalidade:** Prestacao do servico de CRM e atendimento via IA
- **Base legal:** Execucao de contrato + instrucoes do Controlador
- **Compartilhamento:** WhatsApp/Meta (entrega de mensagens),
  provedor de IA (processamento), cloud provider (hospedagem)
- **Transferencia internacional:** Sim (Meta/WhatsApp - EUA;
  [AI Provider - pais])
- **Medidas de seguranca:** Criptografia E2E (WhatsApp),
  TLS 1.3, AES-256, RBAC, logs de auditoria
- **Prazo de retencao:** Conforme instrucao do Controlador
  (padrao: 2 anos)
- **Forma de eliminacao:** Exclusao permanente com log de auditoria

## ATIVIDADE 3: Analytics e Melhoria da IA
- **Controlador:** Tikso
- **Categorias de titulares:** Consumidores finais (dados anonimizados)
- **Dados tratados:** Dados anonimizados de conversas, metricas
  de atendimento, padroes de linguagem
- **Finalidade:** Melhoria dos algoritmos de IA e do produto
- **Base legal:** Legitimo interesse (dados anonimizados nao sao
  dados pessoais per LGPD)
- **Compartilhamento:** Provedor de IA (treinamento)
- **Medidas de seguranca:** Anonimizacao irreversivel,
  agregacao minima de 50 registros
- **Prazo de retencao:** Indeterminado (dados anonimizados)

## ATIVIDADE 4: Marketing Direto
- **Controlador:** Tikso
- **Categorias de titulares:** Leads e prospects
- **Dados tratados:** Nome, email, empresa, cargo
- **Finalidade:** Comunicacao comercial sobre o produto Tikso
- **Base legal:** Legitimo interesse (Art. 7, IX)
- **Compartilhamento:** Plataforma de email marketing
- **Medidas de seguranca:** Opt-out em toda comunicacao
- **Prazo de retencao:** Ate opt-out ou 2 anos sem interacao
- **Forma de eliminacao:** Exclusao logica imediata apos opt-out

## ATIVIDADE 5: Logs de Sistema e Seguranca
- **Controlador:** Tikso
- **Categorias de titulares:** Usuarios da plataforma
- **Dados tratados:** IP, user-agent, timestamps, acoes no sistema
- **Finalidade:** Seguranca, prevencao a fraude, auditoria
- **Base legal:** Legitimo interesse + obrigacao legal (Marco Civil)
- **Compartilhamento:** Nenhum (exceto ordem judicial)
- **Prazo de retencao:** 6 meses (Marco Civil) a 1 ano
- **Forma de eliminacao:** Exclusao automatizada apos periodo
```

---

## 2. MARCO LEGAL DA IA NO BRASIL

### 2.1 Status do PL 2338/2023

| Marco | Data | Status |
|-------|------|--------|
| Apresentacao no Senado | Maio 2023 | Concluido |
| Aprovacao no Senado | Dezembro 2024 | Concluido |
| Envio a Camara dos Deputados | Dezembro 2024 | Concluido |
| PL do Governo (SIA) | Dezembro 2025 | Apensado ao PL 2338 |
| Votacao na Camara | Prevista 1o sem. 2026 | PENDENTE |
| Sancao presidencial | Prevista 2o sem. 2026 | PENDENTE |

**Recomendacao:** Mesmo sem aprovacao final, a Tikso DEVE se preparar proativamente. O texto aprovado pelo Senado indica a direcao regulatoria, e a ANPD ja fiscaliza com base na LGPD existente.

### 2.2 Classificacao de Risco da IA da Tikso

O PL 2338/2023 adota uma abordagem baseada em risco, semelhante ao EU AI Act:

**Classificacao da Tikso: RISCO MODERADO (nao alto)**

Justificativa:
- A Tikso NAO se enquadra em "risco excessivo" (proibido): nao manipula comportamento, nao faz scoring social
- A Tikso NAO se enquadra claramente em "alto risco": nao opera em infraestrutura critica, recrutamento, justica criminal, saude diagnostica
- A Tikso opera em atendimento ao cliente e CRM, que sao funcoes comerciais regulares

**Porem, ATENCAO a areas de risco elevado:**

| Funcionalidade | Risco | Razao |
|---------------|-------|-------|
| Chatbot para atendimento generico | Moderado | Pode dar informacao incorreta |
| Classificacao automatica de leads (scoring) | Alto potencial | Se influenciar acesso a credito/servicos |
| Respostas sobre produtos financeiros | Alto | Se clientes da Tikso forem bancos/financeiras |
| Atendimento em saude | Alto | Se clientes da Tikso forem clinicas/hospitais |
| Perfilamento comportamental | Moderado-Alto | Se usado para decisoes automatizadas |

### 2.3 Obrigacoes de Transparencia

Independentemente da classificacao de risco, TODO sistema de IA deve:

1. **Identificacao:** Informar ao usuario que esta interagindo com IA
2. **Explicabilidade:** Fornecer explicacao sobre como a IA toma decisoes
3. **Contestacao:** Permitir que decisoes da IA sejam contestadas
4. **Revisao humana:** Disponibilizar revisao por humano quando solicitado
5. **Documentacao:** Manter documentacao tecnica sobre o sistema

**Implementacao na Tikso:**

```
CHECKLIST DE TRANSPARENCIA DA IA:
[x] Disclosure na primeira mensagem (Eli se identifica como IA)
[ ] Pagina "Como funciona a IA" no site/dashboard
[ ] Botao "Por que recebi esta resposta?" nas respostas automatizadas
[ ] Opcao "Falar com humano" sempre visivel
[ ] Documentacao tecnica do modelo de IA mantida internamente
[ ] Registro de decisoes automatizadas para auditoria
```

### 2.4 Responsabilidade Civil por Decisoes da IA

**Cenario critico para a Tikso:**

No direito brasileiro, aplica-se a **responsabilidade objetiva** (sem necessidade de provar culpa) quando:

1. **CDC Art. 14:** O fornecedor de servicos responde independentemente de culpa por defeitos na prestacao do servico. Se a IA "Eli" der uma resposta errada que cause dano ao consumidor final, TANTO o Cliente quanto a Tikso podem ser responsabilizados.

2. **LGPD Art. 42:** O controlador ou operador que causar dano em razao do tratamento de dados e obrigado a repara-lo. Responsabilidade solidaria.

3. **PL 2338/2023:** Estabelece que o fornecedor de sistema de IA responde por danos causados, com direito de regresso contra quem deu causa.

**Jurisprudencia emergente (2024):** 83% dos 1.795 acordaos sobre IA envolvem relacoes de consumo, indicando forte tendencia de aplicacao do CDC.

**Medidas de protecao para a Tikso:**

| Medida | Implementacao | Prioridade |
|--------|--------------|------------|
| Disclaimer em toda resposta da IA | "Resposta gerada por IA, sujeita a revisao" | P0 |
| Limitacao de responsabilidade no contrato | Cap de 12 meses de pagamento | P0 |
| Seguro de responsabilidade civil | Seguro E&O (Errors & Omissions) | P1 |
| Logs de todas as interacoes | Retencao minima 2 anos | P0 |
| Supervisao humana em decisoes criticas | Escalacao automatica por keywords | P1 |
| Clausula de indemnification no ToS | Cliente assume uso da IA | P1 |

---

## 3. WHATSAPP BUSINESS -- TERMOS E COMPLIANCE

### 3.1 ALERTA CRITICO: Ban de Chatbots Genericos (Jan 2026)

**A partir de 15 de janeiro de 2026**, a Meta proibiu chatbots de IA de proposito geral na WhatsApp Business API.

**O que esta BANIDO:**
- Chatbots que funcionam como assistentes abertos (estilo ChatGPT)
- Bots que respondem perguntas sobre qualquer assunto
- IA como "funcionalidade principal" do servico no WhatsApp

**O que esta PERMITIDO (e a Tikso se enquadra aqui):**
- Chatbots para suporte ao cliente (FAQ, triagem de tickets)
- Servicos transacionais (rastreamento de pedidos, confirmacoes)
- Notificacoes (atualizacoes, lembretes, alertas)
- Gerenciamento de leads (qualificacao e roteamento para humanos)
- IA como funcionalidade "anciliar" (auxiliar) ao servico principal

**Regra-chave: "Primary vs. Ancillary"**

O papel da IA deve ser ANCILIAR a um servico de negocio legitimo, nao ser o centro da interacao. A Tikso e um CRM que USA IA para melhorar atendimento -- a IA e o meio, nao o fim. Isso e PERMITIDO.

**CHECKLIST DE COMPLIANCE WHATSAPP:**

```
COMPLIANCE WHATSAPP BUSINESS API:
[x] IA e anciliar ao servico do cliente (CRM)
[ ] Escalacao para humano disponivel em toda conversa
[ ] Nenhuma resposta "open-ended" sem contexto de negocio
[ ] Eli responde apenas dentro do escopo configurado pelo cliente
[ ] Mecanismo de fallback quando IA nao sabe responder
[ ] Rate limiting implementado (antiban)
[ ] Mensagens template aprovadas pela Meta
```

### 3.2 Politica de Mensagens

| Regra | Requisito | Status Tikso |
|-------|-----------|-------------|
| Opt-in | Consentimento ANTES de enviar mensagens | Implementar |
| 24h Window | Respostas livres apenas dentro de 24h da ultima msg do usuario | Implementar |
| Templates | Fora da janela de 24h, apenas templates aprovados | Implementar |
| Anti-spam | Nao enviar mensagens em massa nao solicitadas | OK (antiban) |
| Conteudo proibido | Sem armas, drogas, adulto, phishing, desinformacao | Configurar filtros |
| Frequencia | Nao exceder limites de envio da plataforma | OK (antiban) |

### 3.3 Opt-in Requirements (Detalhado)

O opt-in para WhatsApp Business DEVE ser:
1. **Ativo:** O usuario deve tomar uma acao afirmativa (clicar, digitar, selecionar)
2. **Informado:** Deve ficar claro que consentira receber mensagens pelo WhatsApp
3. **Especifico:** Deve indicar quais tipos de mensagens recebera
4. **Documentado:** A empresa deve manter registro do consentimento
5. **Revogavel:** Deve existir mecanismo facil de opt-out

**Exemplos de opt-in valido:**
- Formulario web com checkbox nao pre-marcado
- Mensagem SMS/email com link de confirmacao
- QR code em loja fisica com texto explicativo
- Conversa iniciada pelo proprio usuario no WhatsApp

**Exemplos de opt-in INVALIDO:**
- Checkbox pre-marcado em formulario
- Termos genericos "aceito receber comunicacoes"
- Importar lista de contatos sem consentimento especifico

### 3.4 Regra da Janela de 24 Horas

```
FLUXO DE MENSAGENS WHATSAPP:

[Usuario envia mensagem]
    |
    v
[JANELA DE 24H ABERTA] --> Respostas livres (sem template)
    |                       - Chatbot Eli pode responder
    |                       - Atendente humano pode responder
    |                       - Midia, localizacao, documentos OK
    |
[24h sem mensagem do usuario]
    |
    v
[JANELA FECHADA] ----------> Apenas templates aprovados
                              - Notificacoes transacionais
                              - Follow-up pre-aprovado
                              - Lembretes
                              - NAO pode iniciar conversa livre
```

### 3.5 Modelo de Precificacao (desde Jul 2025)

Desde julho de 2025, o WhatsApp Business API cobra por mensagem (nao mais por conversa):
- Mensagens de utilidade (transacionais): custo menor
- Mensagens de marketing: custo maior
- Mensagens de autenticacao: custo intermediario
- Mensagens de servico (dentro da janela 24h): gratuitas*

*Politica de mensagens de servico gratuitas pode variar por regiao e BSP.

### 3.6 Sistema Antiban da Tikso

A Tikso ja possui um sistema antiban robusto (conforme memoria do projeto). Para compliance juridico, garantir:

- [ ] Rate limiting por destinatario (max mensagens/hora)
- [ ] Backoff em erros 429
- [ ] Reducao automatica em horario de almoco
- [ ] Feedback loop (detectar respostas negativas)
- [ ] Opt-out automatico quando usuario solicita
- [ ] Presenca humana detectavel (nao parecer 100% bot)
- [ ] Log de todas as mensagens para auditoria

---

## 4. CONTRATOS SAAS

### 4.1 Clausulas Essenciais para SaaS com IA

Alem dos Termos de Uso (secao 1.6), o contrato SaaS completo deve incluir:

**Clausulas criticas especificas para IA:**

```
CLAUSULA: USO DE INTELIGENCIA ARTIFICIAL

1. O CONTRATANTE reconhece que a Plataforma utiliza tecnologia
   de inteligencia artificial para auxiliar no atendimento ao
   cliente.

2. As respostas geradas pela IA sao AUXILIARES e nao substituem
   aconselhamento profissional especializado.

3. O CONTRATANTE e responsavel por:
   a) Configurar adequadamente os parametros da IA
   b) Supervisionar as interacoes da IA com seus consumidores
   c) Treinar a IA com informacoes corretas e atualizadas
   d) Monitorar a qualidade das respostas

4. A TIKSO nao garante:
   a) Acuracia de 100% nas respostas da IA
   b) Que a IA substituira integralmente o atendimento humano
   c) Resultados comerciais especificos

5. Em caso de falha da IA que cause dano ao consumidor final
   do CONTRATANTE, as responsabilidades serao apuradas conforme
   a legislacao vigente (CDC, LGPD), observada a contribuicao
   de cada parte para o evento danoso.
```

### 4.2 SLA (Service Level Agreement) Modelo

```markdown
# SLA -- TIKSO PLATAFORMA

## 1. METRICAS DE DISPONIBILIDADE

| Metrica | Meta | Medicao |
|---------|------|---------|
| Uptime da plataforma | 99.5% mensal | Monitoramento 24/7 |
| Uptime da API | 99.5% mensal | Health checks a cada 60s |
| Tempo de resposta da IA | < 3 segundos (p95) | Metricas internas |
| Entrega de mensagens WhatsApp | 99% em ate 5 min | Logs de delivery |

## 2. EXCLUSOES DO CALCULO DE SLA
- Manutencoes programadas (comunicadas com 48h)
- Indisponibilidade do WhatsApp/Meta
- Indisponibilidade de provedores de IA terceiros
- Forca maior
- Ataques DDoS ou incidentes de seguranca

## 3. CREDITOS POR INDISPONIBILIDADE

| Uptime Mensal | Credito |
|--------------|---------|
| 99.0% - 99.5% | 5% do valor mensal |
| 98.0% - 99.0% | 10% do valor mensal |
| 95.0% - 98.0% | 25% do valor mensal |
| < 95.0% | 50% do valor mensal |

Credito maximo: 50% do valor mensal.
Credito nao e cumulativo e deve ser solicitado em ate 30 dias.

## 4. SUPORTE

| Canal | Horario | Tempo de Resposta |
|-------|---------|------------------|
| Chat in-app | 8h-20h (dias uteis) | 30 minutos |
| Email | 24/7 | 4 horas uteis |
| Telefone | 9h-18h (dias uteis) | Imediato |
| Emergencia (sistema fora) | 24/7 | 15 minutos |

## 5. SEVERIDADES DE INCIDENTES

| Severidade | Descricao | Tempo de Resolucao |
|-----------|-----------|-------------------|
| Critica | Sistema completamente indisponivel | 4 horas |
| Alta | Funcionalidade essencial degradada | 8 horas |
| Media | Funcionalidade nao-essencial indisponivel | 24 horas |
| Baixa | Bug cosmetico ou melhoria | Proximo release |
```

### 4.3 Propriedade Intelectual das Conversas

**Questao critica: Quem e dono das conversas?**

```
CADEIA DE PROPRIEDADE:

[Consumidor Final] <---> [Cliente Tikso] <---> [Tikso]
   Titular dos dados      Proprietario do       Processador
   (direitos LGPD)        conteudo das          (licenca limitada
                           conversas             para processar)

REGRA GERAL:
- O CONTEUDO das conversas pertence ao Cliente
- Os DADOS PESSOAIS sao do titular (consumidor final)
- A TECNOLOGIA (IA, algoritmos) pertence a Tikso
- INSIGHTS anonimizados e agregados: licenca para a Tikso
```

**Clausula modelo:**

```
PROPRIEDADE INTELECTUAL E DADOS

1. Dados e Conteudo do Cliente: O Cliente retem todos os
   direitos sobre seus dados, incluindo conversas com
   seus consumidores. A Tikso nao adquire propriedade
   sobre tais dados.

2. Licenca Operacional: O Cliente concede a Tikso licenca
   nao exclusiva, limitada ao escopo e duracao do contrato,
   para processar os dados conforme necessario para
   prestar o servico.

3. Dados Anonimizados: O Cliente autoriza a Tikso a utilizar
   dados anonimizados e agregados (que nao permitam
   identificacao de titulares ou do Cliente) para fins de
   melhoria de produto, benchmarks e pesquisa.

4. Tecnologia: A plataforma Tikso, incluindo software, IA,
   algoritmos, modelos, marca e design, sao e permanecem
   propriedade exclusiva da Tikso.

5. Rescisao: Apos o termino do contrato, o Cliente pode
   exportar seus dados por 30 dias. Apos este prazo,
   os dados serao permanentemente excluidos, exceto
   dados anonimizados ja incorporados aos modelos.
```

---

## 5. COMPLIANCE INTERNACIONAL

### 5.1 GDPR (Europa) -- Diferencas com LGPD

Se a Tikso expandir para a Europa ou atender clientes com consumidores europeus:

| Aspecto | LGPD | GDPR | Acao para Tikso |
|---------|------|------|----------------|
| Bases legais | 10 bases | 6 bases | Mapear equivalencias |
| DPO obrigatorio | Sempre (Art. 41) | Condicional | Ja deve ter DPO |
| Notificacao de breach | "Prazo razoavel" | 72 horas | Adotar 72h como padrao |
| Resposta a titular | 15 dias | 30 dias | Manter 15 dias |
| Multa maxima | 2% receita / R$50M | 4% receita global / EUR20M | GDPR e mais severo |
| Transferencia intl. | Clausulas contratuais | SCCs + adequacao | Implementar SCCs |
| Encarregado (DPO) | Indicacao obrigatoria | Obrigatorio em certos casos | Nomear DPO |
| DPIA obrigatorio | Nao explicito | Sim, para alto risco | Implementar DPIA |
| Consentimento de menor | 12 anos (com pais) | 16 anos (pode ser 13) | Avaliar audiencia |

**Acoes para GDPR-readiness:**
1. Implementar mecanismo de consentimento granular (cookie consent)
2. Nomear representante na UE (se nao tiver escritorio la)
3. Implementar Data Protection Impact Assessment (DPIA) para a IA
4. Criar processo de notificacao de breach em 72h
5. Documentar SCCs (Standard Contractual Clauses) para transferencias

### 5.2 CCPA/CPRA (California)

Aplicavel se tiver clientes ou usuarios na California:

| Requisito CCPA/CPRA | Implementacao para Tikso |
|---------------------|------------------------|
| Right to Know | Pagina "What data we collect" |
| Right to Delete | Funcionalidade de exclusao de dados |
| Right to Opt-Out of Sale | Botao "Do Not Sell My Personal Information" |
| Right to Non-Discrimination | Nao penalizar quem exerce direitos |
| ADMT (Automated Decision-Making) | Disclosure sobre IA + opt-out de decisoes automatizadas |
| Risk Assessment | Privacy Risk Assessment documentado |
| Cybersecurity Audit | Necessario se receita > $100M (2027+) |

**Limiar de aplicabilidade (2026):**
- Receita anual > US$26.625.000, OU
- Dados de 100.000+ residentes da California, OU
- 50%+ da receita de venda/compartilhamento de dados pessoais

**Prazo critico:** Requisitos de ADMT entram em vigor em 01/01/2027. Risk Assessments obrigatorios a partir de 01/01/2026.

### 5.3 SOC 2 (para Clientes Enterprise)

SOC 2 nao e uma lei, mas e um requisito de mercado para vender a enterprise:

**Quando comecar:**
- Quando tiver deals enterprise (> US$100K ACV) no pipeline
- Normalmente entre US$1M-2M ARR
- Custo estimado: US$10K-25K (Type I), US$25K-50K (Type II)

**Roteiro para SOC 2:**

| Fase | Acao | Prazo |
|------|------|-------|
| 1. Gap Analysis | Identificar lacunas de controle | 2-4 semanas |
| 2. Politicas | Criar politicas de seguranca formais | 4-6 semanas |
| 3. Implementacao | Implementar controles tecnicos | 6-12 semanas |
| 4. Type I | Auditoria pontual (snapshot) | 3-6 meses |
| 5. Type II | Auditoria ao longo de 6-12 meses | 12-18 meses |

**Ferramentas de automacao recomendadas:** Vanta, Drata, Sprinto, Secureframe (reduzem timeline em 90%).

### 5.4 HIPAA (Healthcare -- Expansao Futura)

Se a Tikso expandir para atender clinicas, hospitais ou planos de saude:

**Requisitos obrigatorios:**
1. **BAA (Business Associate Agreement):** Contrato especifico com cada cliente de saude
2. **Criptografia obrigatoria:** ePHI em transito E repouso
3. **Controle de acesso:** MFA obrigatorio, RBAC granular
4. **Logs de auditoria:** Retencao minima de 6 anos
5. **Treinamento:** Equipe treinada em HIPAA
6. **Plano de resposta a incidentes:** Notificacao em 60 dias para breaches 500+
7. **Infraestrutura dedicada:** Servidores com BAA do cloud provider (AWS HIPAA eligible, etc.)

**Custo estimado para HIPAA compliance:** US$50K-200K + custos recorrentes

**Recomendacao:** NAO buscar HIPAA compliance agora. Apenas quando houver oportunidade concreta de mercado em saude. Priorizar LGPD + SOC 2 primeiro.

### 5.5 SOX (Sarbanes-Oxley)

SOX aplica-se a empresas de capital aberto (listadas em bolsa) nos EUA. Para a Tikso, isso so se torna relevante se:
- Fizer IPO em bolsa americana (NYSE, NASDAQ)
- Atender clientes que exijam compliance SOX de fornecedores

**Acao atual:** Nenhuma. Revisar se/quando houver planos de IPO ou cliente enterprise que exija.

---

## 6. PROTECAO DA MARCA

### 6.1 Registro de Marca "Tikso" no INPI

**Status do sistema INPI (2026):**
- Taxa unica desde setembro 2025 (deposito + analise + 10 anos de vigencia)
- Prazo medio: 12-24 meses do protocolo ate concessao
- Formulario inteligente com IA previsto para 1o semestre 2026

**Classes NCL recomendadas para registro:**

| Classe | Descricao | Prioridade | Custo (c/ desconto*) |
|--------|-----------|-----------|---------------------|
| Classe 9 | Software, programas de computador, aplicativos | P0 | R$ 440 |
| Classe 42 | Servicos de tecnologia, SaaS, cloud computing | P0 | R$ 440 |
| Classe 35 | Publicidade, gestao de negocios, CRM | P1 | R$ 440 |
| Classe 38 | Servicos de telecomunicacao, mensageria | P2 | R$ 440 |

*Valor com desconto para ME/EPP/MEI. Valor integral: R$ 880 por classe.

**TOTAL ESTIMADO:** R$ 1.760 (com desconto, 4 classes) ou R$ 3.520 (integral)

**Passo a passo:**

1. **Pesquisa de anterioridade** (gratuita no site do INPI)
   - Verificar se "Tikso" ja existe nas classes desejadas
   - URL: https://busca.inpi.gov.br/pePI/

2. **Cadastro no e-INPI**
   - Portal: https://www.gov.br/inpi
   - CNPJ da empresa + certificado digital (opcional)

3. **Deposito do pedido**
   - Tipo: marca mista (nome + logo) ou nominativa (apenas nome)
   - Recomendacao: registrar AMBAS (mista e nominativa)
   - Especificacao: usar especificacao pre-aprovada (mais barato)

4. **Acompanhamento**
   - Revista da Propriedade Industrial (RPI) semanal
   - Prazos de manifestacao: 60 dias para oposicoes

### 6.2 Protecao do Nome "Eli" (a IA)

**Analise de viabilidade:**

| Aspecto | Avaliacao |
|---------|-----------|
| Distintividade | MEDIA -- "Eli" e um nome proprio comum |
| Risco de confusao | ALTO -- existem outras marcas "Eli" |
| Registrabilidade | POSSIVEL como marca mista (Eli + elemento grafico) |
| Alternativa | Registrar "Eli by Tikso" ou "Tikso Eli" |

**Recomendacao:**
1. Pesquisar anterioridade para "Eli" nas classes 9 e 42
2. Se disponivel, registrar como marca MISTA (nome + logo da IA)
3. Se indisponivel como marca isolada, registrar "Eli by Tikso"
4. Proteger tambem via direito autoral do personagem/avatar

### 6.3 Dominios Defensivos

**Dominios prioritarios para registro:**

| Dominio | Status | Prioridade |
|---------|--------|-----------|
| tikso.com.br | Verificar | P0 |
| tikso.com | Verificar | P0 |
| tikso.ai | Verificar | P0 |
| tikso.io | Verificar | P1 |
| tiksocrm.com | Verificar | P1 |
| tiksocrm.com.br | Verificar | P1 |
| eli.tikso.com.br | Subdominio | P2 |
| tikso.app | Verificar | P2 |
| tikso.tech | Verificar | P2 |

**Custo estimado:** R$ 40-80/ano por dominio .com.br, US$ 10-15/ano por .com/.io/.ai

**Acoes defensivas adicionais:**
- Registrar handles em redes sociais: @tikso, @tiksocrm, @tikso_ai
- Registrar no Google Business (para evitar squatting)
- Considerar registro no exterior (USPTO) quando expandir

---

## 7. CHECKLISTS DE COMPLIANCE

### 7.1 Checklist LGPD Completo

```
COMPLIANCE LGPD -- TIKSO CRM

GOVERNANCA:
[ ] DPO/Encarregado nomeado publicamente
[ ] Politica de privacidade publicada (site + app)
[ ] Termos de uso publicados
[ ] ROPA elaborado e atualizado
[ ] Politica interna de seguranca da informacao
[ ] Treinamento de equipe em protecao de dados
[ ] Plano de resposta a incidentes documentado
[ ] Canal de atendimento ao titular (email DPO)

TECNICO:
[ ] Criptografia em transito (TLS 1.3)
[ ] Criptografia em repouso (AES-256)
[ ] RBAC implementado
[ ] MFA para acesso administrativo
[ ] Logs de auditoria ativos (retencao 1 ano)
[ ] Backup automatizado com teste de restauracao
[ ] Processo de exclusao de dados (hard delete)
[ ] Exportacao de dados em formato padrao (CSV/JSON)
[ ] Anonimizacao para analytics/treinamento IA

CONTRATUAL:
[ ] DPA modelo com todos os clientes
[ ] Clausulas de protecao de dados nos contratos
[ ] Acordos com suboperadores (cloud, WhatsApp, IA)
[ ] Clausulas de transferencia internacional

TRANSPARENCIA IA:
[ ] Disclosure na primeira mensagem do chatbot
[ ] Opcao de atendimento humano sempre disponivel
[ ] Pagina explicativa sobre como a IA funciona
[ ] Mecanismo de revisao de decisoes automatizadas
```

### 7.2 Checklist WhatsApp Business

```
COMPLIANCE WHATSAPP -- TIKSO CRM

POLITICA DE MENSAGENS:
[ ] Opt-in coletado ANTES de enviar mensagens
[ ] Registro de consentimento armazenado
[ ] Mecanismo de opt-out funcional
[ ] Templates aprovados pela Meta
[ ] Janela de 24h respeitada
[ ] Rate limiting implementado
[ ] Conteudo proibido filtrado

CHATBOT IA:
[ ] Eli e anciliar ao servico (nao primary)
[ ] Escalacao para humano implementada
[ ] Respostas limitadas ao escopo do negocio do cliente
[ ] Fallback para "nao sei responder"
[ ] Identificacao como IA na primeira mensagem

TECNICO:
[ ] WhatsApp Cloud API (nao on-premise, depreciado)
[ ] BSP (Business Solution Provider) autorizado
[ ] Webhooks configurados corretamente
[ ] Tratamento de erros e retry logic
[ ] Monitoramento de delivery status
```

### 7.3 Checklist Contratual

```
CONTRATOS SAAS -- TIKSO CRM

DOCUMENTOS BASE:
[ ] Terms of Service (Termos de Uso)
[ ] Privacy Policy (Politica de Privacidade)
[ ] SLA (Service Level Agreement)
[ ] DPA (Data Processing Agreement)
[ ] Cookie Policy (se tiver dashboard web)
[ ] Acceptable Use Policy

CLAUSULAS ESSENCIAIS:
[ ] Definicao clara dos servicos
[ ] Obrigacoes de cada parte
[ ] Uso de IA: disclaimer + limitacoes
[ ] Propriedade intelectual definida
[ ] Limitacao de responsabilidade (cap 12 meses)
[ ] Excecoes a limitacao (LGPD, CDC, dolo)
[ ] Confidencialidade (5 anos pos-contrato)
[ ] Rescisao e transicao de dados
[ ] Foro e lei aplicavel
[ ] Clausula de mediacao pre-litigio
```

---

## 8. ROADMAP LEGAL

### Fase 1: Fundacao (0-30 dias) -- URGENTE

| Acao | Responsavel | Custo Est. | Risco se Nao Fizer |
|------|------------|-----------|-------------------|
| Politica de Privacidade | Juridico | R$ 0 (modelo acima) | Multa ANPD |
| Termos de Uso | Juridico | R$ 0 (modelo acima) | Exposicao contratual |
| Disclosure de IA (Eli) | Dev + Juridico | R$ 0 | Violacao transparencia |
| Nomear DPO/Encarregado | Gestao | R$ 0 | Obrigacao legal |
| Pesquisa de marca INPI | Juridico | R$ 0 (pesquisa gratuita) | Perda da marca |

### Fase 2: Estruturacao (30-90 dias)

| Acao | Responsavel | Custo Est. | Risco se Nao Fizer |
|------|------------|-----------|-------------------|
| DPA modelo | Advogado | R$ 3K-8K | Exposicao com clientes |
| Registro de marca INPI (4 classes) | Advogado marcario | R$ 1.760-3.520 + honorarios | Perda de direitos |
| ROPA completo | DPO | R$ 0 (modelo acima) | Multa em fiscalizacao |
| Contrato SaaS revisado | Advogado | R$ 5K-15K | Disputas contratuais |
| SLA formalizado | Produto + Juridico | R$ 0 (modelo acima) | Expectativas desalinhadas |
| Plano de resposta a incidentes | DevOps + Juridico | R$ 0 | Despreparo em breach |
| Dominios defensivos | TI | R$ 500-1K/ano | Brand squatting |

### Fase 3: Robustecimento (3-6 meses)

| Acao | Responsavel | Custo Est. | Risco se Nao Fizer |
|------|------------|-----------|-------------------|
| Seguro E&O (responsabilidade civil) | Gestao | R$ 5K-20K/ano | Exposicao pessoal socios |
| Auditoria de seguranca (pentest) | DevOps | R$ 10K-30K | Vulnerabilidades ocultas |
| Politica interna de SI | DPO + DevOps | R$ 0 | Falta de governanca |
| Treinamento equipe (LGPD + IA) | DPO | R$ 2K-5K | Erros humanos |
| Cookie consent (dashboard web) | Dev | R$ 0-500 | Non-compliance web |

### Fase 4: Expansao Internacional (6-18 meses)

| Acao | Responsavel | Custo Est. | Gatilho |
|------|------------|-----------|---------|
| GDPR compliance | Advogado EU | EUR 10K-30K | Clientes na Europa |
| CCPA compliance | Advogado US | US$ 5K-15K | Clientes na California |
| SOC 2 Type I | Auditor + Automacao | US$ 10K-25K | Deal enterprise >$100K |
| SOC 2 Type II | Auditor | US$ 25K-50K | Pos Type I (6-12 meses) |
| Registro marca internacional | Advogado PI | US$ 5K-15K | Entrada em mercado |
| HIPAA compliance | Especialista | US$ 50K-200K | Clientes healthcare |
| Representante na UE | Advogado EU | EUR 3K-5K/ano | Obrigatorio se GDPR |

---

## 9. MATRIZ DE RISCO CONSOLIDADA

| Risco | Probabilidade | Impacto | Severidade | Mitigacao |
|-------|--------------|---------|-----------|-----------|
| Multa ANPD por falta de PP/ToS | Alta | Alto (ate R$50M) | CRITICO | Publicar PP+ToS imediatamente |
| Ban do WhatsApp (chatbot generico) | Media | Critico (fim do servico) | CRITICO | Garantir IA anciliar + escalacao humana |
| Processo CDC por resposta errada da IA | Media | Alto | ALTO | Disclaimer + supervisao + seguro |
| Vazamento de dados | Baixa | Critico | ALTO | Criptografia + auditoria + plano de resposta |
| Perda da marca "Tikso" | Media | Alto | ALTO | Registrar no INPI imediatamente |
| Penalidades por PL da IA (futuro) | Media | Alto | MEDIO | Compliance proativo com texto aprovado |
| Cliente enterprise sem SOC 2 | Alta | Medio (perda de deal) | MEDIO | Iniciar SOC 2 quando pipeline justificar |
| Acao trabalhista (pejotizacao) | Baixa-Media | Medio | MEDIO | Avaliar regime de contratacao |
| Transferencia internacional irregular | Baixa | Medio | MEDIO | Implementar SCCs + DPA |

---

## 10. RESUMO DE CUSTOS ESTIMADOS

### Investimento Minimo para Compliance Basico (Fase 1-2)

| Item | Custo Estimado |
|------|---------------|
| Documentos juridicos (modelos deste framework) | R$ 0 (DIY) |
| Revisao por advogado especialista | R$ 10K-25K |
| Registro de marca INPI (4 classes) | R$ 1.760-3.520 |
| Dominios defensivos | R$ 500-1K/ano |
| **TOTAL FASE 1-2** | **R$ 12K-30K** |

### Investimento para Compliance Robusto (Fase 3-4)

| Item | Custo Estimado |
|------|---------------|
| Seguro E&O | R$ 5K-20K/ano |
| Auditoria de seguranca | R$ 10K-30K |
| SOC 2 (se necessario) | US$ 35K-75K |
| GDPR compliance (se expandir) | EUR 10K-30K |
| **TOTAL FASE 3-4** | **R$ 80K-300K** (variavel) |

---

## FONTES E REFERENCIAS

### Legislacao
- [LGPD (Lei 13.709/2018)](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [CDC (Lei 8.078/1990)](http://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm)
- [Marco Civil da Internet (Lei 12.965/2014)](http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm)
- [PL 2338/2023 - Senado Federal](https://www25.senado.leg.br/web/atividade/materias/-/materia/157233)

### Regulamentacao e Guias
- [ANPD - Guia Orientativo sobre Legitimo Interesse](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-lanca-guia-orientativo-sobre-legitimo-interesse)
- [ANPD - Modelo ROPA para Agentes de Pequeno Porte](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/modelo_de_ropa_para_atpp.pdf)
- [WhatsApp Business Messaging Policy](https://business.whatsapp.com/policy)
- [WhatsApp Business Solution Terms](https://www.whatsapp.com/legal/business-solution-terms/preview)
- [INPI - Manual de Marcas](https://manualdemarcas.inpi.gov.br/)

### Analises e Artigos
- [WhatsApp 2026 AI Policy Explained - Respond.io](https://respond.io/blog/whatsapp-general-purpose-chatbots-ban)
- [PL 2338/2023 Aprovado pelo Senado - FAS Advogados](https://fasadv.com.br/pt/bra/publication/pl-2338-2023-aprovado-pelo-senado-federal)
- [Votacao do Marco da IA Adiado para 2026 - Desinformante](https://desinformante.com.br/votacao-do-marco-da-ia-fica-para-2026-em-meio-a-impasses-politicos-e-criticas-ao-texto)
- [LGPD para Chatbots e IA - Contabeis](https://www.contabeis.com.br/artigos/69603/lgpd-para-chatbots-e-ia-como-garantir-a-conformidade/)
- [Compliance 2026: LGPD 2.0 e IA - SYS4B](https://sys4b.com.br/compliance-2026-lgpd-2-0-e-o-impacto-da-ia-nos-dados-corporativos/)
- [LGPD vs GDPR - Endpoint Protector](https://www.endpointprotector.com/blog/lgpd-vs-gdpr-the-biggest-differences/)
- [CCPA Requirements 2026 - SecurePrivacy](https://secureprivacy.ai/blog/ccpa-requirements-2026-complete-compliance-guide)
- [California Finalizes CCPA AI Regulations - Wiley](https://www.wiley.law/alert-California-Finalizes-Pivotal-CCPA-Regulations-on-AI-Cyber-Audits-and-Risk-Governance)
- [Responsabilidade Civil IA Brasil - Conjur](https://www.conjur.com.br/2025-mar-05/perspectivas-sobre-a-responsabilidade-civil-do-fornecedor-de-sistema-de-ia/)
- [Ofertas por Chatbots Obrigam Fornecedor - Jusbrasil](https://www.jusbrasil.com.br/artigos/ofertas-e-promessas-feitas-por-aplicativos-ia-e-chatbots-obrigam-o-fornecedor/5455230800)
- [SOC 2 for SaaS Startups - CompAI](https://trycomp.ai/soc-2-checklist-for-saas-startups)
- [HIPAA Compliance for SaaS - HIPAA Journal](https://www.hipaajournal.com/hipaa-compliance-for-saas/)
- [Registro de Marca INPI 2026 - Gaviglia](https://gaviglia.com/blog/como-registrar-marca-no-inpi-em-2026-passo-a-passo-custos)
- [Meta Bans General-Purpose AI Chatbots on WhatsApp - TechCrunch](https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform/)
- [WhatsApp Cloud API Security 2026 Guide - WuSeller](https://www.wuseller.com/whatsapp-business-knowledge-hub/whatsapp-cloud-api-security-2026-privacy-compliance-guide-for-business/)

---

> **AVISO LEGAL**
>
> Esta analise e orientativa e nao substitui consulta com advogado.
> Para questoes especificas, consulte um profissional habilitado.
> Os modelos de documentos fornecidos sao templates iniciais que
> DEVEM ser revisados por advogado antes de publicacao.
> Legislacao e regulamentacao estao sujeitas a alteracoes.
> Ultima verificacao das fontes: fevereiro de 2026.
