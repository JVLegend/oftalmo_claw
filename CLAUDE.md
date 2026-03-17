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
- `web/templates/` - HTML (base.html com sidebar + topbar)
- `web/static/css/theme.css` - Tema medico completo
- `models/` - SQLAlchemy models (Case, Doctor, ExamRecord, etc.)
- `skills/ophthalmology/` - Skills em Markdown com frontmatter YAML
- `tools/registry.py` - Registro central de ferramentas do agente
- `agent/core.py` - Loop do agente de IA
- `gateway/` - Integracoes Telegram, WhatsApp, etc.

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
- API segue REST em `/api/v1/`
- Idioma principal: Portugues (BR) para UI, ingles para codigo

## Modelos de dados importantes
- `Case`: Caso de segunda opiniao (status, urgencia, especialidade)
- `Doctor`: Medico/especialista (CRM, especialidade, online)
- `Opinion`: Parecer sobre um caso
- `ExamRecord`: Registro de exame com quality_score
- `AnalyticsSnapshot`: Dados pre-computados para dashboard

## Ao editar
- Mantenha a consistencia visual (use as classes CSS existentes em theme.css)
- Novos endpoints vao em `web/routes/` e sao incluidos em `web/app.py`
- Novas skills vao em `skills/ophthalmology/{nome}/SKILL.md`
- Use terminologia oftalmologica correta
- Disclaimer medico e obrigatorio em qualquer saida clinica
