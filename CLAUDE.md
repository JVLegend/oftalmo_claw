# OftalmoClaw - Contexto para Claude Code

## O que e este projeto
OftalmoClaw e um Mission Control de oftalmologia com IA. Criado por GeekVision.
Baseado na arquitetura do Hermes Agent (Nous Research), mas e um projeto independente.

## Stack
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy (async), Pydantic
- **Frontend**: Jinja2 templates, CSS puro (sem framework), JS vanilla
- **Banco**: SQLite (dev) / PostgreSQL (prod via DATABASE_URL)
- **Deploy**: Railway (Dockerfile), Docker Compose
- **IA**: OpenRouter ou Anthropic API

## Estrutura principal
- `main.py` - Entry point (modos: web, cli, gateway)
- `config.py` - Pydantic Settings com .env
- `web/app.py` - FastAPI app com rotas e templates
- `web/routes/` - API endpoints (dashboard, cases, analytics, api)
- `web/templates/` - HTML (base.html com sidebar + topbar + toast + PWA)
- `web/static/css/theme.css` - Tema medico completo (~1150 linhas)
- `web/static/js/app.js` - JS utilitarios (~230 linhas: toast, modal, search, markdown)
- `web/static/manifest.json` - PWA manifest (app instalavel)
- `models/` - SQLAlchemy models (Case, Doctor, ExamRecord, etc.)
- `skills/ophthalmology/` - Skills em Markdown com frontmatter YAML
- `tools/registry.py` - Registro central de ferramentas do agente
- `agent/core.py` - Loop do agente de IA
- `gateway/` - Integracoes Telegram, WhatsApp, etc.

## Paginas do frontend
- `dashboard.html` - Mission Control (boas-vindas, cards guiados, stats colapsaveis)
- `second_opinion.html` - Segunda Opiniao (form novo caso, detalhe com timeline, lista)
- `calculators.html` - Calculadoras (LIO SRK/T, conversor AV, correcao PIO)
- `chat.html` - Chat com IA (sugestoes rapidas, markdown, timestamps)
- `trends.html` - Tendencias (graficos, tipos de exame, rankings)
- `login.html` - Tela de login (existe mas nao esta wired)
- `base.html` - Layout base (sidebar, topbar com busca/notif/perfil, disclaimer)

## Componentes CSS em theme.css
- `.modal-overlay`, `.modal`, `.modal-header/body/footer` - Sistema de modais
- `.toast`, `#toast-container` - Notificacoes toast (success/error/warning/info)
- `.skeleton`, `.skeleton-card`, `.skeleton-text` - Loading skeletons com shimmer
- `.intro-box`, `.welcome-banner` - Onboarding de primeiro uso
- `.action-card`, `.action-cards-grid` - Cards guiados do dashboard
- `.case-detail-panel`, `.case-timeline` - Detalhe do caso e timeline
- `.form-grid`, `.form-group`, `.form-error` - Sistema de formularios
- `.table-medical` - Tabelas medicas com zebra striping
- `.disclaimer-box`, `.medical-disclaimer` - Disclaimers medicos
- `.topbar-search`, `.topbar-user`, `.notif-panel` - Topbar profissional
- `.chat-chip`, `.chat-suggestions` - Sugestoes rapidas no chat
- `.hamburger-btn`, `.sidebar-overlay` - Menu mobile
- `.print-btn`, `.print-header`, `@media print` - Impressao
- Utilities: `.mt-sm/md/lg`, `.text-center`, `.text-muted`, `.flex-col-gap`

## Funcoes JS em app.js
- `showToast(msg, type)` - Notificacao toast global
- `openModal(id)` / `closeModal(id)` - Abrir/fechar modais (ESC + click-outside)
- `toggleSidebar()` - Menu hamburger mobile com overlay
- `dismissIntro(id, key)` / `checkIntroDismissed(id, key)` - Intro boxes
- `toggleSection(id)` - Secoes colapsaveis
- `renderMarkdown(text)` - Markdown basico (bold, italic, code, listas, headers)
- `handleSearch(query)` / `loadSearchData()` - Busca global na topbar
- `toggleNotifications()` / `toggleUserMenu()` - Paineis dropdown

## Paleta de cores medicas
- Primary (Teal): #0D9488
- Navy: #1E3A5F
- Coral (urgente): #EF4444
- Amber (pendente): #F59E0B
- Emerald (online/ok): #10B981
- Backgrounds: #FFFFFF, #F1F5F9, #F8FAFC

## Convencoes
- Skills seguem o padrao agentskills.io (Markdown com YAML frontmatter)
- Tools se registram via `tools/registry.py` com `register()`
- Templates herdam de `base.html` (sidebar + topbar + page-content)
- CSS usa variaveis em :root (--primary, --navy, etc.)
- Novos estilos vao em `theme.css` (NAO inline nos templates)
- API segue REST em `/api/v1/`
- Idioma principal: Portugues (BR) para UI, ingles para codigo
- Usar `showToast()` para feedback de acoes
- Usar `openModal()`/`closeModal()` para dialogos
- Usar classes utility em vez de inline styles

## Modelos de dados importantes
- `Case`: Caso de segunda opiniao (status, urgencia, especialidade)
- `Doctor`: Medico/especialista (CRM, especialidade, online)
- `Opinion`: Parecer sobre um caso
- `CaseMessage`: Mensagem na discussao de um caso
- `CaseImage`: Imagem anexada ao caso
- `ExamRecord`: Registro de exame com quality_score
- `AnalyticsSnapshot`: Dados pre-computados para dashboard

## Ao editar
- Mantenha a consistencia visual (use as classes CSS existentes em theme.css)
- NAO use inline styles — crie classes CSS nomeadas
- Novos endpoints vao em `web/routes/` e sao incluidos em `web/app.py`
- Novas skills vao em `skills/ophthalmology/{nome}/SKILL.md`
- Use terminologia oftalmologica correta
- Disclaimer medico e obrigatorio em qualquer saida clinica
- Teste com `.venv/bin/python -m uvicorn web.app:app` antes de commitar
