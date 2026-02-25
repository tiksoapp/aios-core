# WhatsApp Antiban Best Practices para Evolution API v2

**Data:** 2026-02-23
**Contexto:** Tikso CRM com Evolution API v2.3.7, agente PULSE para mensagens proativas
**Confianca Geral:** MEDIA-ALTA (baseado em 15+ fontes cruzadas)
**Autor:** Atlas (AIOS Analyst)

---

## Sumario Executivo

Este relatorio consolida pesquisa extensiva sobre tecnicas antiban para WhatsApp usando APIs nao-oficiais (Baileys/Evolution API). A conclusao principal e que **nao existe garantia de zero-ban** ao usar APIs nao-oficiais -- o risco e inerente. No entanto, a adocao sistematica das praticas documentadas aqui pode reduzir drasticamente a probabilidade de restricao ou banimento.

**Descoberta critica:** Evolution API v2.3.7 tem um problema conhecido (GitHub Issue #2298) onde contas sao restringidas apos 1-2 dias de uso normal, independente do volume de mensagens. Isso indica que o problema pode estar parcialmente na camada de protocolo, nao apenas no comportamento de mensagens.

---

## 1. Meta/WhatsApp Business API -- Politicas Oficiais 2025-2026

### 1.1 Sistema de Tiers (Oficial)

| Tier | Limite de Conversas Unicas/24h | Requisito |
|------|-------------------------------|-----------|
| Inicial (nao verificado) | 250 | Conta nova |
| Tier 1 | 1.000 | Verificacao basica |
| Tier 2 | 10.000 | Quality rating alto mantido |
| Tier 3 | 100.000 | Quality rating alto + volume consistente |
| Ilimitado | Sem limite | Nivel maximo de confianca |

**Nota:** Esses limites se aplicam a API oficial. Para APIs nao-oficiais (Baileys/Evolution), os limites sao significativamente mais baixos antes de acionar deteccao.

### 1.2 Quality Rating

O quality rating e calculado com base em:
- **Sinais dos ultimos 7 dias**, ponderados por recencia
- Bloqueios por usuarios
- Reports de spam
- Taxa de resposta e engajamento

**Status do numero:**
- **Connected:** Pode enviar mensagens normalmente
- **Flagged:** Quality rating Low -- nao pode subir de tier enquanto flagged
- **Restricted:** Atingiu limite -- bloqueado por 24h para novas conversas

### 1.3 Regras de Opt-in (Abril 2025+)

- Toda mensagem proativa requer **opt-in explicito** do destinatario
- Opt-in deve mostrar: nome do negocio + tipo de conteudo (ofertas, lembretes, etc.)
- **Pre-checked boxes sao proibidos**
- Mudanca 2025: Consentimento generico de mensagens (nao especifico do WhatsApp) agora aceito se em conformidade com leis locais
- **EUA:** Marketing messages pausados desde abril 2025 para numeros americanos (utility e authentication continuam)

### 1.4 Categorias de Template

| Categoria | Uso | Revisao |
|-----------|-----|---------|
| Marketing | Promocoes, ofertas | Mais restritivo, monitorado |
| Utility | Confirmacoes, lembretes, atualizacoes | Aprovacao mais rapida |
| Authentication | Codigos OTP, verificacao | Regras especificas |

**Template Pacing/Pausing:** Meta monitora metricas de desempenho (block rates, spam reports, engagement) e pode pausar templates automaticamente.

**Confianca:** ALTA -- baseado em documentacao oficial Meta e BSPs autorizados.

### Fontes
- [WATI - WhatsApp API Rate Limits](https://www.wati.io/en/blog/whatsapp-business-api/whatsapp-api-rate-limits/)
- [360dialog - Capacity, Quality Rating, and Messaging Limits](https://docs.360dialog.com/docs/waba-management/capacity-quality-rating-and-messaging-limits)
- [Infobip - Template Compliance](https://www.infobip.com/docs/whatsapp/compliance/template-compliance)
- [WhatsApp Business Messaging Policy](https://business.whatsapp.com/policy)

---

## 2. Evolution API -- Problemas Conhecidos e Antiban

### 2.1 Issues Criticas no GitHub

**Issue #2298 -- Restricao Temporaria apos 1-2 Dias (v2.3.7)**
- Contas sao restringidas automaticamente apos 1-2 dias de uso "normal"
- WhatsApp exibe: "Sua conta esta atualmente restrita. Parece que voce esta usando ferramentas que nao seguem nossos Termos"
- QR Code bloqueado por ~24h
- Sem solucao confirmada pelos mantenedores
- Relatos de restricao com apenas 2 mensagens enviadas (v2.3.6)
- **O ciclo se repete**: restricao -> espera 24h -> reconecta -> restricao novamente
- URL: https://github.com/EvolutionAPI/evolution-api/issues/2298

**Issue #2228 -- Risco de Ban ao Verificar Numeros**
- Endpoint `/chat/whatsappNumbers/{{instance}}` nao implementa rate limiting
- Verificacao em massa de numeros aciona deteccao de atividade suspeita
- Sem mecanismo de protecao implementado
- URL: https://github.com/EvolutionAPI/evolution-api/issues/2228

**Issue #1946 -- Compilado de Best Practices Antiban**
- Thread comunitaria solicitando metodos antiban
- Recomendacoes-chave da comunidade:
  - **Usar proxy estatico** (residencial, nao datacenter) -- custo ~$50-100/mes
  - **Evitar envio em massa com numero frio**
  - IPs de datacenter (especialmente Hostinger) causam ban rapido
  - Receber mensagens tem risco minimo; enviar e o que causa ban
  - Numeros novos podem ser banidos em 4h mesmo com 3 mensagens de teste
- URL: https://github.com/EvolutionAPI/evolution-api/issues/1946

### 2.2 Configuracao de Typing no Evolution API v2

A Evolution API suporta nativamente:

```json
// Enviar mensagem com typing indicator
POST /message/sendText/{{instance}}
{
  "number": "5511999999999",
  "text": "Sua mensagem aqui",
  "options": {
    "delay": 1200,
    "presence": "composing"
  }
}
```

**Parametros disponíveis:**
- `delay`: Tempo em ms antes de enviar (simula digitacao)
- `presence`: `"composing"` (digitando) ou `"recording"` (gravando audio)
- `delayMessage`: Config do Evolution Bot em ms

**Dica da comunidade (Issue #1639):** Usar delay randomizado:
```javascript
Math.floor(Math.random() * (15000 - 10000 + 1) + 10000)
// Gera delay entre 10s e 15s
```

### 2.3 Avaliacao de Risco da Evolution API

| Fator | Risco | Notas |
|-------|-------|-------|
| Conexao via Baileys | ALTO | API nao-oficial viola ToS |
| Datacenter IP sem proxy | CRITICO | Deteccao quase imediata |
| Volume alto de envio | CRITICO | Principal trigger de ban |
| Verificacao de numeros em massa | ALTO | Sem rate limiting nativo |
| Reconexoes frequentes | ALTO | Padrao detectado como automacao |

**Confianca:** ALTA -- baseado em issues do GitHub com relatos de usuarios reais.

### Fontes
- [Evolution API Issue #2298](https://github.com/EvolutionAPI/evolution-api/issues/2298)
- [Evolution API Issue #2228](https://github.com/EvolutionAPI/evolution-api/issues/2228)
- [Evolution API Issue #1946](https://github.com/EvolutionAPI/evolution-api/issues/1946)
- [Evolution API Issue #1639](https://github.com/EvolutionAPI/evolution-api/issues/1639)

---

## 3. Baileys Antiban -- Tecnicas e Middleware

### 3.1 Biblioteca baileys-antiban

A biblioteca `baileys-antiban` (GitHub: kobie3717/baileys-antiban) e o middleware mais completo encontrado. Seus defaults representam o consenso da comunidade:

### 3.2 Rate Limiter -- Valores Recomendados

| Parametro | Valor Default | Descricao |
|-----------|--------------|-----------|
| `maxPerMinute` | **8** | Mensagens por minuto |
| `maxPerHour` | **200** | Mensagens por hora |
| `maxPerDay` | **1500** | Mensagens por dia |
| `minDelayMs` | **1500** | Delay minimo entre mensagens (ms) |
| `maxDelayMs` | **5000** | Delay maximo entre mensagens (ms) |
| `newChatDelayMs` | **3000** | Delay extra para novo contato |
| `maxIdenticalMessages` | **3** | Bloqueia apos 3 mensagens identicas |
| `burstAllowance` | **3** | Mensagens rapidas antes de limitar |

**RECOMENDACAO PARA TIKSO/PULSE:** Usar valores MAIS CONSERVADORES que os defaults:

| Parametro | Valor Sugerido | Razao |
|-----------|---------------|-------|
| `maxPerMinute` | **3-5** | Margem de seguranca extra |
| `maxPerHour` | **50-80** | Bem abaixo do limite tecnico |
| `maxPerDay` | **200-500** | Proporcional a maturidade do numero |
| `minDelayMs` | **3000** | Mais conservador |
| `maxDelayMs` | **8000** | Spread maior |
| `newChatDelayMs` | **5000** | Extra cautela para novos contatos |

### Fontes
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)

---

## 4. Typing Simulation -- Best Practices

### 4.1 Por Que Simular Typing

WhatsApp monitora a presenca do typing indicator. Contas que enviam mensagens sem nunca exibir "digitando..." sao sinalizadas como automacao. A simulacao deve ser **proporcional ao tamanho da mensagem**.

### 4.2 Implementacao Recomendada

**Formula base:**
```
typingDelayMs = baseDelay + (charCount * msPerChar) + gaussianJitter
```

**Parametros recomendados:**

| Parametro | Valor | Descricao |
|-----------|-------|-----------|
| `baseDelay` | 500-1000ms | Tempo antes de comecar a "digitar" |
| `msPerChar` | 25-35ms | ~30ms por caractere (simula digitacao) |
| `gaussianJitter` | +/- 30% | Variacao gaussiana (nao uniforme) |
| `maxTypingDelay` | 15000ms | Cap para mensagens longas |
| `minTypingDelay` | 1500ms | Minimo mesmo para mensagens curtas |

**Exemplo pratico para Evolution API:**
```javascript
function calculateTypingDelay(text) {
  const charDelay = text.length * 30; // ~30ms por caractere
  const base = 800;
  const jitter = gaussianRandom(-0.3, 0.3) * charDelay;
  const total = base + charDelay + jitter;
  return Math.min(Math.max(total, 1500), 15000);
}

// Mensagem curta (20 chars): ~1500ms (minimo)
// Mensagem media (100 chars): ~3800ms
// Mensagem longa (300 chars): ~9800ms
// Mensagem muito longa (500 chars): ~15000ms (cap)
```

**Na Evolution API:**
```json
{
  "number": "5511999999999",
  "text": "Ola! Como posso ajudar?",
  "options": {
    "delay": 2200,
    "presence": "composing"
  }
}
```

### 4.3 Typing para Audio (se aplicavel)

Para mensagens de audio, usar `"presence": "recording"` com delays mais longos (5-15s).

**Confianca:** MEDIA-ALTA -- baseado em baileys-antiban defaults + praticas da comunidade.

### Fontes
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)
- [Evolution API Issue #1639](https://github.com/EvolutionAPI/evolution-api/issues/1639)

---

## 5. Message Delays -- Intervalos Recomendados

### 5.1 Entre Mensagens (Mesmo Contato)

| Cenario | Delay Recomendado | Notas |
|---------|-------------------|-------|
| Mensagem seguida de outra | 2-6s + jitter | Simula digitacao rapida |
| Resposta a pergunta | 5-15s + typing | Simula leitura + digitacao |
| Follow-up na mesma conversa | 30-120s | Parece troca natural |
| Segunda mensagem sem resposta | 4-24h | NUNCA enviar spam |

### 5.2 Entre Contatos Diferentes

| Cenario | Delay Recomendado | Notas |
|---------|-------------------|-------|
| Mensagens proativas sequenciais | 90-180s | Nunca burst |
| Batch de follow-ups | 1-3 min entre cada | Distribuir ao longo de horas |
| Campanha (mesmo template) | 3-5 min entre cada | Variacao obrigatoria |

### 5.3 Burst vs Sustained

| Modo | Limite | Risco |
|------|--------|-------|
| Burst (< 5 min) | Max 3 mensagens | BAIXO se raro |
| Sustained (por hora) | Max 20-30 mensagens | MEDIO |
| Diario (total) | Max 200-500 | MEDIO-BAIXO se warm-up feito |

**REGRA DE OURO:** Nunca enviar mais de 3 mensagens no mesmo minuto, nunca mais de 30 por hora, e distribuir uniformemente ao longo do horario comercial.

**Confianca:** MEDIA -- nao existem limites oficiais publicados; valores derivados de experiencia coletiva.

### Fontes
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)
- [WAPI Random Delay](https://wapi7.com/random-delay-between-messages-in-wapi-whatsapp-marketing/)
- [WAWarmer Warm-Up Guide](https://warmer.wadesk.io/blog/whatsapp-account-warm-up)

---

## 6. Random Jitter -- Tecnicas de Aleatorizacao

### 6.1 Por Que Jitter Importa

WhatsApp detecta padroes ritmicos. Se mensagens sao enviadas a cada 60s exatos, o sistema identifica como automacao. A aleatorizacao deve ser **gaussiana** (bell curve), nao uniforme.

### 6.2 Distribuicao Gaussiana vs Uniforme

**Uniforme (RUIM):**
```
delay = random(1000, 5000) // Todos os valores igualmente provaveis
// Resultado: 1000, 4500, 2100, 4900, 1300 (parece artificial)
```

**Gaussiana (BOM):**
```
delay = gaussianRandom(mean=3000, stddev=800)
// Resultado: 2800, 3200, 2600, 3100, 3400 (cluster natural no centro)
```

### 6.3 Implementacao Recomendada

```javascript
function gaussianRandom(mean, stddev) {
  // Box-Muller transform
  const u1 = Math.random();
  const u2 = Math.random();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return mean + z * stddev;
}

function getMessageDelay(baseDelay = 3000) {
  const jitter = gaussianRandom(0, baseDelay * 0.3); // 30% stddev
  const delay = baseDelay + jitter;
  return Math.max(1500, Math.min(delay, baseDelay * 2)); // Clamp
}
```

### 6.4 Camadas de Jitter Recomendadas

| Camada | Variacao | Aplicacao |
|--------|----------|-----------|
| Delay base entre mensagens | +/- 30% gaussiano | Sempre |
| Typing duration | +/- 20% gaussiano | Por mensagem |
| Horario de inicio diario | +/- 15 min | Por dia |
| Pausa para "almoco" | 0-30 min offset | Opcional |
| Intervalo weekend | 50% mais lento | Sabados/domingos |

**Confianca:** ALTA -- tecnica bem estabelecida em anti-fingerprinting.

### Fontes
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)
- [FullAgenticStack Anti-Patterns](https://dev.to/fullagenticstack/fullagenticstack-whatsapp-first-anti-patterns-a-reference-handbook-3jb0)

---

## 7. Rate Limits -- Limites para Mensagens Proativas

### 7.1 Limites Recomendados por Fase

**FASE 1: Numero Novo (Semanas 1-3)**

| Periodo | Limite | Notas |
|---------|--------|-------|
| Dia 1-3 | 10-20 msgs/dia | Apenas contatos conhecidos |
| Dia 4-7 | 20-65 msgs/dia | Introduzir 1-2 contatos novos/dia |
| Dia 8-14 | 65-200 msgs/dia | Escalar gradualmente |
| Dia 15-21 | 200-500 msgs/dia | Se quality ok |

**FASE 2: Numero Aquecido (Semana 4+)**

| Periodo | Limite | Notas |
|---------|--------|-------|
| Por hora | 20-30 msgs | Distribuir uniformemente |
| Por dia | 200-800 msgs | Depende da idade do numero |
| Por semana | 1500-5000 msgs | Monitorar quality rating |

**FASE 3: Numero Maduro (Mes 2+)**

| Periodo | Limite | Notas |
|---------|--------|-------|
| Por hora | 30-50 msgs | Com jitter |
| Por dia | 500-1500 msgs | Se reply rate > 30% |
| Por semana | 3000-8000 msgs | Com content variation |

### 7.2 Limites Especificos para PULSE (Recomendacao)

Dado que o PULSE envia follow-ups, lembretes e reativacoes:

| Tipo de Mensagem | Limite/Dia | Delay entre msgs |
|------------------|-----------|-------------------|
| Follow-up (apos interacao) | 50-100 | 2-5 min |
| Lembrete de agendamento | 30-50 | 3-5 min |
| Reativacao (contato frio) | 20-30 | 5-10 min |
| **Total combinado** | **100-180** | Distribuir em 8h |

**IMPORTANTE:** Esses limites assumem um numero ja aquecido (3+ semanas). Para numeros novos, usar 20% desses valores.

**Confianca:** MEDIA -- derivado de multiplas fontes comunitarias, sem dados oficiais.

### Fontes
- [WAWarmer Warm-Up Guide](https://warmer.wadesk.io/blog/whatsapp-account-warm-up)
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)
- [SendWo - WhatsApp Message Limits](https://sendwo.com/blog/whatsapp-message-limits/)

---

## 8. Warm-Up Strategy -- Aquecimento Gradual

### 8.1 Protocolo de Warm-Up Completo (20 Dias)

**FASE 1: Ativacao (Dias 1-3)**

| Acao | Detalhe |
|------|---------|
| Registro | SIM card real (NAO VOIP/virtual) |
| Perfil | Foto real, nome humano (nao logo), status preenchido |
| Primeiro dia | **NAO envie mensagens** -- mantenha app aberto 20-30 min |
| Dia 2-3 | 5-10 conversas com contatos mutuos (amigos/familia) |
| Grupos | Participar de 2-3 grupos, enviar 1-2 msgs/grupo/dia |
| Status | Atualizar status 1x/dia com conteudo variado |

**FASE 2: Aceleracao (Dias 4-7)**

| Acao | Detalhe |
|------|---------|
| Conversas | 20-30 rounds/dia com topicos variados |
| Novos contatos | Introduzir 1-2 interacoes com desconhecidos/dia |
| Atividade | Manter conta ativa varias horas por dia |
| Midias | Enviar e receber fotos, audios, links |

**FASE 3: Crescimento (Dias 8-14)**

| Acao | Detalhe |
|------|---------|
| Novos contatos | Max 3 interacoes com desconhecidos/dia |
| Volume | Escalar para 65-200 msgs/dia |
| Tipos | Variar entre texto, audio, imagem, link |
| Two-way | Garantir que esta RECEBENDO mensagens tambem |

**FASE 4: Estabilizacao (Dias 15-20)**

| Acao | Detalhe |
|------|---------|
| Volume | 200-500 msgs/dia |
| Testar outreach | Iniciar mensagens proativas cautelosamente |
| Monitorar | Se qualquer sinal de restricao, pausar 24-48h |
| Atingir estabilidade | ~20 dias para estado durable |

### 8.2 Escala Exponencial (baileys-antiban)

| Dia | Limite de Mensagens | Crescimento |
|-----|-------------------|-------------|
| 1 | 20 | - |
| 2 | 36 | 1.8x |
| 3 | 65 | 1.8x |
| 4 | 117 | 1.8x |
| 5 | 210 | 1.8x |
| 6 | 378 | 1.8x |
| 7 | 680 | 1.8x |
| 8+ | Ilimitado* | *Sujeito a rate limits normais |

**Growth factor:** 1.8x por dia (agressivo). **Recomendacao para Tikso:** Usar 1.4-1.5x para margem de seguranca.

### 8.3 Re-Aquecimento

Se o numero ficar **inativo por 72h+**, reentrar no processo de warm-up (nao do zero, mas retroceder 2-3 fases). Manter atividade minima (1-2 msgs/dia) mesmo em dias sem necessidade.

### 8.4 Red Flags -- O Que NAO Fazer

| Red Flag | Risco |
|----------|-------|
| Setup de perfil em < 5 minutos | CRITICO |
| Enviar mensagens imediatamente apos registro | CRITICO |
| Blast de 1000+ msgs no dia 1 | BAN IMEDIATO |
| Mensagens a numeros nao-salvos nos primeiros dias | ALTO |
| Sempre responder instantaneamente (0 delay) | ALTO |
| Nao receber nenhuma mensagem (so enviar) | ALTO |
| Mudar dispositivo ou IP durante warm-up | ALTO |

**Confianca:** ALTA -- consenso entre multiplas fontes.

### Fontes
- [WAWarmer Warm-Up Guide](https://warmer.wadesk.io/blog/whatsapp-account-warm-up)
- [WUSeller - Warm-Up Strategy](https://www.wuseller.com/blog/warm-up-strategy-for-new-whatsapp-business-platform-accounts-anti-ban-tactics/)
- [Whapi - Warming Up New Phone Numbers](https://support.whapi.cloud/help-desk/blocking/warming-up-new-phone-numbers-for-whatsapp-api)
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)

---

## 9. Content Variation -- Evitar Deteccao de Spam

### 9.1 Por Que Conteudo Identico e Detectado

WhatsApp usa ML/AI para identificar padroes de spam. Templates identicos enviados a multiplos contatos sao sinalizados. A deteccao analisa:
- **Texto identico** entre mensagens
- **Estrutura sintatica** similar
- **Frequencia de links** identicos
- **Padroes de formatacao** repetitivos

### 9.2 Tecnicas de Variacao

**Nivel 1: Personalizacao Basica (OBRIGATORIO)**
```
// Template base
"Ola {nome}! Lembrete: seu agendamento e amanha as {hora}."

// Resultado
"Ola Maria! Lembrete: seu agendamento e amanha as 14:00."
"Ola Joao! Lembrete: seu agendamento e amanha as 15:30."
```

**Nivel 2: Variacao Estrutural (RECOMENDADO)**
```javascript
const greetings = ["Ola", "Oi", "E ai", "Bom dia", "Boa tarde"];
const closings = [
  "Qualquer duvida, estamos aqui!",
  "Precisando de algo, e so chamar.",
  "Conte conosco!",
  "Abraco!"
];

// Aleatorizar greeting + closing para cada mensagem
```

**Nivel 3: Sinonimos e Reformulacao (AVANCADO)**
```javascript
const variations = [
  "Seu agendamento e amanha",
  "Amanha temos seu horario marcado",
  "Lembrando que amanha e seu dia",
  "So passando pra confirmar amanha"
];
```

**Nivel 4: Caracteres Invisiveis (CAUTELOSO)**
- Zero-width characters entre palavras
- Variacao sutil de pontuacao
- **RISCO:** WhatsApp pode detectar e penalizar esta tecnica

### 9.3 Regras da Meta para Templates

- Templates duplicados com body/footer identico sao **rejeitados automaticamente**
- Templates com apenas placeholders (sem texto real) sao rejeitados
- Erros gramaticais aumentam report rate
- Meta monitora: block rates, spam reports, engagement levels

### 9.4 Recomendacao para PULSE

| Tipo de Msg | Nivel de Variacao | Implementacao |
|-------------|-------------------|---------------|
| Follow-up | Nivel 2 | Pool de 5-8 templates por tipo |
| Lembrete | Nivel 1-2 | Personalizar + variar greeting |
| Reativacao | Nivel 3 | Pool de 10+ mensagens diferentes |
| Resposta | Nivel 1 | Personalizar por contexto |

**Confianca:** MEDIA-ALTA -- combina praticas oficiais (templates Meta) com tecnicas comunitarias.

### Fontes
- [Infobip - Template Compliance](https://www.infobip.com/docs/whatsapp/compliance/template-compliance)
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)
- [InsiderOne - Template Pacing and Pausing](https://academy.insiderone.com/docs/whatsapp-template-pacing-and-pausing)

---

## 10. Multi-Device/Session -- Riscos e Mitigacoes

### 10.1 Como Funciona

Baileys (e por extensao Evolution API) se autentica como um **cliente secundario** do WhatsApp Web via QR Code ou Pairing Code. O WhatsApp Multi-Device permite ate 4 dispositivos vinculados.

### 10.2 Riscos Documentados

| Risco | Severidade | Descricao |
|-------|-----------|-----------|
| Reconnect loops | ALTO | Sessao desconecta/reconecta repetidamente, detectado como automacao |
| Session rejection | ALTO | WhatsApp aceita handshake mas rejeita sessao depois |
| Multiple instances | CRITICO | Nao executar 2+ instancias no mesmo numero |
| IP inconsistencia | ALTO | IP mudando frequentemente sinaliza automacao |
| Credential reuse | MEDIO | Credenciais salvas podem ser rejeitadas na revalidacao |

### 10.3 Mitigacoes

**Conexao:**
- Manter **1 unica instancia** por numero
- Usar IP estavel (preferencialmente residencial/movel)
- Implementar reconnect com backoff exponencial (nao retry imediato)
- Monitorar contagem de disconnects (>3/hora = alarme)

**Sessao:**
- Salvar e restaurar estado da sessao (auth state) corretamente
- Nao fazer logout/login frequente
- Se restringido, esperar 24-48h completas antes de reconectar
- Monitorar `disconnectCriticalThreshold`: 5 disconnects/hora = parar

**Infraestrutura:**
- **Proxy residencial** (NAO datacenter) -- $50-100/mes
- IP fixo ou rotacao lenta (cada 24-48h no maximo)
- Evitar IPs de provedores blacklistados (Hostinger mencionado especificamente)
- VPS com IP residencial e o ideal

### 10.4 Health Monitoring (baileys-antiban)

| Score | Status | Acao |
|-------|--------|------|
| 0-29 | Verde (Normal) | Operacao normal |
| 30-59 | Amarelo (Medio) | Reduzir mensagens 50% |
| 60-84 | Laranja (Alto) | Reduzir 80%, considerar pausar |
| 85-100 | Vermelho (Critico) | **PARAR IMEDIATAMENTE** |

**Eventos que aumentam risk score:**
- Disconnects frequentes: +15 a +30 pontos
- Erro 403 Forbidden: +40 pontos
- Erro 401 Logged Out: +60 pontos
- Mensagens falhadas: +20 pontos

**Confianca:** ALTA -- baseado em comportamentos documentados e amplamente confirmados.

### Fontes
- [Baileys Issue #2110 - Reconnect Issues](https://github.com/WhiskeySockets/Baileys/issues/2110)
- [Baileys Issue #1869 - High Number of Bans](https://github.com/WhiskeySockets/Baileys/issues/1869)
- [Evolution API Issue #2298](https://github.com/EvolutionAPI/evolution-api/issues/2298)
- [baileys-antiban GitHub](https://github.com/kobie3717/baileys-antiban)

---

## 11. Mecanismos de Deteccao do WhatsApp

### 11.1 Sistema Multi-Camada da Meta

O WhatsApp usa um sistema de deteccao em 3 camadas:

**Camada 1: Device Fingerprinting**
- Centenas de parametros: hardware IDs, resolucao, fontes, plugins, Canvas rendering
- Multiplas contas com fingerprint similar = associacao automatica
- Rotacao recomendada: semanal

**Camada 2: Network/IP Analysis**
- IPs de datacenter sao flagged automaticamente
- IPs compartilhados entre multiplas contas = flag
- Mudancas frequentes de IP = flag
- Rotacao natural recomendada: cada 24-48h

**Camada 3: Behavior Analysis**
- Velocidade de digitacao
- Intervalos entre mensagens
- Uso de emojis
- Taxa de resposta (reply rate)
- Duracao de sessao
- Variedade de conteudo

### 11.2 Sinais de Alerta Especificos

| Sinal | O Que Detecta |
|-------|---------------|
| Mensagens sem typing indicator | Automacao |
| Intervalos identicos | Bot com delay fixo |
| Apenas envio, zero recepcao | Spam unidirecional |
| Alto volume + baixo reply rate | Spam |
| Multiplos reports/blocks em curto periodo | Spam confirmado |
| IP de datacenter | Infraestrutura de automacao |
| Reconnect loops | Software instavel/automatizado |
| Mensagens identicas a muitos contatos | Blast/spam |
| Atividade 24/7 sem pausa | Automacao |

### 11.3 Metrica-Chave: Reply Rate

A taxa de resposta e provavelmente o **indicador mais importante** de legitimidade. Contas com reply rate alto raramente sao banidas.

| Reply Rate | Risco |
|------------|-------|
| > 50% | BAIXO -- parece conversa genuina |
| 30-50% | MEDIO-BAIXO -- aceitavel para business |
| 10-30% | MEDIO-ALTO -- monitorar de perto |
| < 10% | CRITICO -- alto risco de ban |

**Confianca:** MEDIA-ALTA -- baseado em WhatsApp whitepaper + analise comunitaria.

### Fontes
- [WAWarmer - Mass Marketing Risk Control](https://warmer.wadesk.io/blog/whatsapp-mass-marketing-risk-control)
- [WhatsApp Stopping Abuse Whitepaper](https://internetlab.org.br/wp-content/uploads/2019/10/WA_StoppingAbuse_Whitepaper_020618-Final-1.pdf)
- [Saasyto - Why WhatsApp Accounts Get Banned](https://saasyto.com/why-whatsapp-accounts-get-banned/)

---

## 12. Recomendacoes Praticas para Tikso CRM + PULSE

### 12.1 Arquitetura Antiban Recomendada

```
[PULSE Agent]
    |
    v
[Message Queue (BullMQ)]  <-- Rate limiter aqui
    |
    v
[Antiban Middleware]  <-- Typing, delay, jitter, health monitoring
    |
    v
[Evolution API v2]  <-- Proxy residencial
    |
    v
[WhatsApp]
```

### 12.2 Implementacao por Prioridade

**P0 -- CRITICO (Implementar Imediatamente)**

1. **Rate Limiter no BullMQ:** Nunca enviar mais de 3 msgs/min, 30/hora, distribuir ao longo do dia
2. **Typing Simulation:** Calcular delay baseado no tamanho da mensagem (30ms/char)
3. **Gaussian Jitter:** Em todos os delays (nao usar valores fixos NUNCA)
4. **Proxy Residencial:** Nao operar com IP de datacenter da Vultr diretamente
5. **Content Variation:** Pool de templates por tipo de mensagem (minimo 5 variantes)

**P1 -- ALTO (Implementar na Semana 1)**

6. **Health Monitor:** Rastrear disconnects, erros, risk score
7. **Auto-Pause:** Parar automaticamente se risk score > 60
8. **Warm-Up Protocol:** Para cada numero novo, seguir protocolo de 20 dias
9. **Horario Comercial:** Apenas enviar entre 8h-20h com offset aleatorio
10. **Weekend Throttle:** 50% do volume normal em sabados, 25% em domingos

**P2 -- MEDIO (Implementar no Mes 1)**

11. **Reply Rate Tracking:** Monitorar e alertar se < 20%
12. **Conversation Balance:** Garantir ratio envio/recebimento saudavel
13. **Inactivity Guard:** Reentrar warm-up apos 72h sem atividade
14. **Fallback to Official API:** Considerar migrar mensagens criticas (lembretes de agendamento) para WhatsApp Cloud API oficial
15. **A/B Testing de Templates:** Testar qual variacao gera menos blocks

### 12.3 Configuracao Sugerida para Evolution API

```javascript
// Configuracao de envio para PULSE
const PULSE_CONFIG = {
  // Rate Limits
  maxPerMinute: 3,
  maxPerHour: 40,
  maxPerDay: 300,       // Conservador para comecar

  // Delays
  minDelayBetweenMessages: 90000,  // 90s entre contatos diferentes
  maxDelayBetweenMessages: 180000, // 180s entre contatos diferentes

  // Typing Simulation
  typingMsPerChar: 30,
  typingBaseDelay: 800,
  typingMaxDelay: 15000,
  typingMinDelay: 1500,

  // Jitter
  jitterType: 'gaussian',
  jitterStdDev: 0.3,     // 30% do valor base

  // Schedule
  activeHoursStart: 8,    // 8:00
  activeHoursEnd: 20,     // 20:00
  weekendFactor: 0.5,     // 50% do volume
  sundayFactor: 0.25,     // 25% do volume

  // Safety
  maxIdenticalMessages: 2,
  autoPauseRiskScore: 60,
  disconnectWarningThreshold: 3,  // por hora
  disconnectCriticalThreshold: 5, // por hora

  // Content
  minTemplateVariants: 5,   // por tipo de mensagem
  personalizeAlways: true,
};
```

### 12.4 Cenario de Risco: Migracao para API Oficial

Dado o Issue #2298 (restricoes recorrentes em v2.3.7), a recomendacao de medio prazo e:

| Funcao PULSE | API Recomendada | Razao |
|-------------|-----------------|-------|
| Lembretes de agendamento | **WhatsApp Cloud API (oficial)** | Critico para negocio, precisa de confiabilidade |
| Follow-ups pos-atendimento | Evolution API (com antiban) | Toleravel se falhar ocasionalmente |
| Reativacao de contatos frios | Evolution API (com antiban) | Menor criticidade |
| Respostas a mensagens recebidas | Evolution API | Baixo risco (resposta, nao proativo) |

**Custo da API Oficial:** Conversas de utility a partir de ~$0.03/conversa no Brasil. Para 50-100 lembretes/dia = ~$3-6/dia = ~$90-180/mes.

### 12.5 Metricas de Monitoramento

| Metrica | Alerta Amarelo | Alerta Vermelho | Acao |
|---------|---------------|-----------------|------|
| Reply rate | < 30% | < 15% | Reduzir volume |
| Block rate | > 2% | > 5% | Pausar proativas |
| Disconnects/hora | > 2 | > 4 | Investigar conexao |
| Messages failed/hora | > 3 | > 5 | Verificar restricao |
| Risk score | > 40 | > 70 | Auto-throttle/pause |

---

## 13. Conclusao e Niveis de Confianca

### Resumo de Confianca por Secao

| Secao | Confianca | Base |
|-------|-----------|------|
| 1. Politicas Meta | ALTA | Documentacao oficial + BSPs |
| 2. Evolution API Issues | ALTA | GitHub issues com relatos reais |
| 3. Baileys Antiban | MEDIA-ALTA | Biblioteca open-source ativa |
| 4. Typing Simulation | MEDIA-ALTA | Consenso comunitario |
| 5. Message Delays | MEDIA | Experiencia coletiva, sem dados oficiais |
| 6. Random Jitter | ALTA | Tecnica matematicamente fundamentada |
| 7. Rate Limits | MEDIA | Limites empiricos, variam por conta |
| 8. Warm-Up | ALTA | Multiplas fontes concordantes |
| 9. Content Variation | MEDIA-ALTA | Politicas oficiais + praticas |
| 10. Multi-Device | ALTA | Issues bem documentadas |
| 11. Deteccao | MEDIA-ALTA | Whitepaper + engenharia reversa comunitaria |

### Risco Residual

Mesmo com todas as praticas implementadas, o uso de APIs nao-oficiais (Baileys/Evolution) carrega risco inerente:
- **Ban permanente:** ~5-15% de chance ao longo de 6 meses (estimativa)
- **Restricoes temporarias:** ~30-50% de chance de pelo menos 1 evento em 3 meses
- **Numero considerado "queimado":** Apos 3+ restricoes, considerar trocar numero

### Recomendacao Final

1. **Curto prazo:** Implementar todas as medidas P0 + P1 listadas na secao 12.2
2. **Medio prazo:** Migrar funcoes criticas (lembretes) para WhatsApp Cloud API oficial
3. **Longo prazo:** Avaliar se o volume de mensagens do Tikso justifica uma conta WABA completa com BSP

---

*-- Atlas, investigando a verdade*

*Relatorio gerado em 2026-02-23. Fontes verificadas e cruzadas em 15+ referencias.*
