# Funcionalidades do OftalmoClaw

Documentacao tecnica e detalhada de cada funcionalidade do sistema.

---

## 1. Mission Control (Dashboard)

**Rota:** `/` | **Template:** `dashboard.html`

### Componentes
- **Banner de boas-vindas** — aparece na primeira visita (localStorage `oftalmo_welcomed`), gradiente teal, botao "Entendi"
- **Cards guiados** — 4 action-cards com icone, titulo, descricao e hint:
  - Perguntar a IA → `/chat`
  - Pedir Segunda Opiniao → `/second-opinion`
  - Usar Calculadoras → `/calculators`
  - Ver Tendencias → `/trends`
- **Resumo do dia** — secao colapsavel com 4 stat-cards (exames hoje, casos pendentes, especialistas online, score qualidade 30d)
- **Casos recentes** — secao colapsavel com os 3 ultimos casos em formato compacto (case-row)

### Dados
- Stats: `GET /api/v1/dashboard/stats`
- Casos: `GET /api/v1/cases/`

---

## 2. Segunda Opiniao

**Rota:** `/second-opinion` | **Template:** `second_opinion.html`

### Componentes
- **Intro box** — explica o fluxo (dismissivel, localStorage `so_intro_hidden`)
- **Tabs** — Pendentes / Concluidos com contadores dinamicos
- **Lista de casos** — cards clicaveis com badge de urgencia, queixa, meta-dados
- **Modal "Novo Caso"** — formulario com 10 campos:
  - `patient_age` (number, 0-120)
  - `patient_gender` (select: F/M)
  - `chief_complaint` (textarea, obrigatorio)
  - `exam_findings` (textarea)
  - `hypothesis` (text)
  - `patient_history` (textarea)
  - `urgency` (select: normal/urgent/emergency)
  - `specialty_requested` (select: 10 especialidades)
  - `requested_by_id` (select: lista de medicos)
  - `assigned_to_id` (select: automatico ou medico especifico)
- **Modal "Detalhe do Caso"** — carrega `GET /api/v1/cases/{id}` e exibe:
  - Dados do paciente e badge de status
  - Grid de campos: solicitante, atribuido, queixa, achados, hipotese, historia
  - Timeline de opinioes (dot azul): diagnostico, recomendacao, confianca
  - Timeline de mensagens (dot cinza): autor, conteudo, timestamp
- **Painel de especialistas** — lista de medicos com avatar, especialidade, status online
- **Card de dicas** — 4 dicas para primeiro uso

### API utilizada
- `GET /api/v1/cases/` — lista de casos
- `GET /api/v1/cases/{id}` — detalhe completo
- `GET /api/v1/cases/specialists` — lista de especialistas
- `POST /api/v1/cases/` — criar novo caso

---

## 3. Chat com IA

**Rota:** `/chat` | **Template:** `chat.html`

### Componentes
- **Mensagem de boas-vindas** — lista o que a IA pode ajudar + disclaimer
- **5 sugestoes rapidas** (chat-chips) — clicaveis, somem apos primeiro uso:
  - Conduta para edema macular diabetico
  - DD de olho vermelho agudo
  - Colirios para glaucoma
  - Quando indicar trabeculectomia?
  - Interpretar OCT macular
- **Area de mensagens** — bolhas com timestamp (HH:MM), scroll automatico
- **Typing indicator** — 3 dots animados enquanto a IA processa
- **Markdown rendering** — bold, italic, code inline, code blocks, headers, listas
- **Seguranca XSS** — mensagens do usuario usam `textContent`, da IA usam `innerHTML` com escape

### API utilizada
- `POST /api/v1/chat` — envia mensagem, recebe resposta

### Provedores suportados
- OpenRouter (`OPENROUTER_API_KEY`)
- Anthropic (`ANTHROPIC_API_KEY`)
- OpenAI (`OPENAI_API_KEY`)
- Fallback: retorna mensagem "IA nao configurada"

---

## 4. Calculadoras Clinicas

**Rota:** `/calculators` | **Template:** `calculators.html`

### LIO (SRK/T)
- **Campos:** comprimento axial (15-40mm), K1 (35-55D), K2 (35-55D), refracao alvo (-10 a +10D)
- **Validacao:** rejeita valores fora do range clinico com erro inline vermelho
- **Resultado:** poder da LIO em dioptrias + disclaimer
- **API:** `GET /api/v1/calculators/iol?al=&k1=&k2=&target=`

### Conversor de Acuidade Visual
- **Campo:** select Snellen (20/10 a 20/400)
- **Resultado:** 3 stat-cards (Snellen, Decimal, LogMAR) + classificacao (Normal, Leve, Moderada, Severa, Cegueira Legal, Profunda)
- **API:** `GET /api/v1/calculators/va-convert?snellen=`

### Correcao de PIO (Ehlers)
- **Campos:** PIO medida (1-80 mmHg), paquimetria (350-700 um)
- **Formula:** correcao = (545 - paquimetria) * 0.07
- **Resultado:** PIO medida vs PIO corrigida + fator de correcao
- **Calculo:** client-side (sem API call)

### Tabela de Referencia
- Conversoes Snellen/Decimal/LogMAR mais usadas
- Usa classe `.table-medical` com zebra striping

### Impressao
- Botao "Imprimir resultado" em cada calculadora
- `@media print` esconde sidebar, topbar, disclaimer e mostra header "OftalmoClaw"

---

## 5. Tendencias

**Rota:** `/trends` | **Template:** `trends.html`

### Componentes
- **Intro box** — explica os dados (dismissivel, localStorage `trends_intro_hidden`)
- **Grafico de barras** — volume por mes (ultimos 6 meses) com score de qualidade
- **Performance por tipo de exame** — barras de progresso (fundoscopia, OCT, campimetria, topografia, biometria, retinografia)
- **Ranking de operadores** — medalhas ouro/prata/bronze, score por medico

### API utilizada
- `GET /api/v1/analytics/trends` — volume e qualidade por mes
- `GET /api/v1/analytics/by-exam-type` — performance por tipo
- `GET /api/v1/analytics/rankings` — ranking de operadores

---

## 6. Topbar (base.html)

### Componentes
- **Hamburger menu** — visivel em mobile (< 768px), toggle sidebar com overlay
- **Titulo e subtitulo** — dinamico por pagina
- **Barra de busca** — busca client-side em cache de casos (caso, paciente, medico)
- **Sino de notificacoes** — badge vermelho com contagem de casos pendentes
- **Perfil do usuario** — avatar + nome + role, dropdown com Perfil/Config/Sair
- **Acoes da pagina** — slot para botoes especificos (ex: "Novo Caso")

---

## 7. Sistema de Design (theme.css)

### Cores
| Nome | Hex | Uso |
|------|-----|-----|
| Primary (Teal) | #0D9488 | Botoes, links, destaques |
| Navy | #1E3A5F | Titulos, sidebar, avatares |
| Coral | #EF4444 | Urgencia, erros, badges |
| Amber | #F59E0B | Pendente, avisos, disclaimers |
| Emerald | #10B981 | Online, sucesso, confirmacao |
| Slate | #F8FAFC a #334155 | Backgrounds, textos, bordas |

### Componentes reutilizaveis
- Modal (`.modal-overlay`, `.modal`, header/body/footer)
- Toast (`.toast`, `#toast-container`, 4 tipos)
- Skeleton (`.skeleton`, `.skeleton-card`, `.skeleton-text`)
- Form (`.form-grid`, `.form-group`, `.form-input`, `.form-error`)
- Table (`.table-medical`)
- Badge (`.badge-urgent/pending/analysis/completed`)
- Card (`.card`, `.stat-card`, `.action-card`, `.case-card`)
- Empty state (`.empty-state`, `.empty-state-illustration`)
- Intro (`.intro-box`, `.welcome-banner`)
- Timeline (`.case-timeline`, `.timeline-item`, `.timeline-dot`)

### Responsivo
- Desktop: sidebar fixa 260px + conteudo fluido
- Tablet (< 1024px): busca reduzida, user-info hidden
- Mobile (< 768px): sidebar hidden, hamburger menu, search hidden

### PWA
- `manifest.json` com icones SVG + PNG (192px, 512px)
- Meta tags Apple para mobile web app
- Theme color: #1E3A5F (Navy)
