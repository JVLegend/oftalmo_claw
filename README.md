<p align="center">
  <img src="assets/logo.svg" alt="OftalmoClaw" width="120" />
</p>

<h1 align="center">OftalmoClaw</h1>

<p align="center">
  <strong>AI-Powered Ophthalmology Mission Control</strong>
  <br />
  <em>Intelligent agent for ophthalmic image analysis, clinical decision support, and collaborative diagnostics</em>
</p>

<p align="center">
  <a href="#features">Features</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#deploy">Deploy</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#skills">Skills</a> &bull;
  <a href="#second-opinion">Second Opinion</a> &bull;
  <a href="#dashboard">Dashboard</a> &bull;
  <a href="#api">API</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-0D9488?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-0D9488?style=for-the-badge" />
  <img src="https://img.shields.io/badge/railway-deploy-0D9488?style=for-the-badge&logo=railway&logoColor=white" />
  <img src="https://img.shields.io/badge/status-active-0D9488?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LGPD-compliant-0D9488?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Created%20by-GeekVision-1E3A5F?style=for-the-badge" />
</p>

---

> **OftalmoClaw** is an open-source, self-improving AI agent specialized in ophthalmology. It combines intelligent image analysis, clinical decision support, collaborative second-opinion workflows, and real-time analytics into a single mission control platform designed for eye care professionals.
>
> Built on the architecture of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research, OftalmoClaw extends it with deep ophthalmology domain knowledge, medical-grade tools, and a purpose-built web dashboard.

---

## Why OftalmoClaw?

| Problem | Solution |
|---------|----------|
| Ophthalmic image interpretation requires years of training | AI-assisted analysis of OCT, fundoscopy, visual fields, topography |
| Second opinions are slow and fragmented | Real-time collaborative case discussion between specialists |
| No unified view of clinical volume and trends | Mission Control dashboard with analytics and KPIs |
| Existing tools don't understand ophthalmology context | Domain-specific skills, calculators, and protocols built-in |
| Medical AI tools are closed-source and expensive | Fully open-source, self-hostable, Railway-ready |

---

## Features

### Core Agent
- **Self-improving AI** with persistent memory and skill generation
- **Multi-model support** - Claude, GPT-4, Gemini, open-source models via OpenRouter
- **40+ tools** including terminal, web search, file management, code execution
- **13 messaging platforms** - Telegram, WhatsApp, Discord, Slack, email, and more
- **Persistent memory** across sessions with FTS5 search

### Ophthalmology Suite
- **Image Analysis** - AI-powered interpretation of OCT, fundoscopy, topography, visual fields
- **Clinical Calculators** - IOL calculation (SRK/T, Barrett), VA conversion, IOP correction
- **Report Generator** - Structured ophthalmic reports with standard terminology
- **Protocol Engine** - Evidence-based clinical protocols (AAO, CBO, EURETINA)
- **Drug Reference** - Complete ophthalmic pharmacology database

### Second Opinion System
- **Case submission** with images, clinical history, and exam data
- **Specialist routing** by subspecialty (Retina, Glaucoma, Cornea, etc.)
- **Real-time discussion threads** between referring and consulting doctors
- **Urgency levels** and status tracking (Pending, In Analysis, Completed)
- **AI-assisted draft opinions** for specialist review
- **Notifications** via WhatsApp, Telegram, or email

### Mission Control Dashboard
- **Volume & Quality trends** over time (weekly, monthly, quarterly, yearly)
- **Performance by exam type** - Fundoscopy, OCT, Visual Fields, Topography
- **Operator rankings** with quality scores and growth metrics
- **Active users**, average report time, pathology distribution
- **Export** to CSV/PDF for administrative reporting

---

## Quick Start

### Prerequisites

- Python 3.11+
- An LLM API key (OpenRouter, Anthropic, OpenAI, or compatible)

### Installation

```bash
# Clone the repository
git clone https://github.com/geekvision/oftalmo-claw.git
cd oftalmo-claw

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys and settings

# Run the application
python main.py
```

### First Run

```bash
# Interactive setup wizard
python main.py --setup

# Or start directly with CLI
python main.py --mode cli

# Start the web Mission Control
python main.py --mode web

# Start messaging gateway (Telegram, WhatsApp, etc.)
python main.py --mode gateway
```

Open your browser at `http://localhost:8000` to access the Mission Control.

---

## Deploy

### Railway (Recommended)

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/oftalmo-claw)

1. Click the button above or create a new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Set the required environment variables:

```
OPENROUTER_API_KEY=sk-or-...
SECRET_KEY=your-secret-key-here
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

4. Deploy. Railway will use the included `Dockerfile` automatically.

### Docker

```bash
# Build
docker build -t oftalmo-claw .

# Run
docker run -d \
  --name oftalmo-claw \
  -p 8000:8000 \
  -e OPENROUTER_API_KEY=sk-or-... \
  -e SECRET_KEY=your-secret-key \
  -v oftalmo-data:/app/data \
  oftalmo-claw
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://oftalmo:oftalmo@db:5432/oftalmo
    volumes:
      - app-data:/app/data
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: oftalmo
      POSTGRES_PASSWORD: oftalmo
      POSTGRES_DB: oftalmo
    volumes:
      - pg-data:/var/lib/postgresql/data

volumes:
  app-data:
  pg-data:
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key for LLM access |
| `SECRET_KEY` | Yes | Application secret for session encryption |
| `DATABASE_URL` | No | PostgreSQL URL (defaults to SQLite) |
| `PORT` | No | Server port (default: 8000) |
| `ANTHROPIC_API_KEY` | No | Direct Anthropic API access |
| `TELEGRAM_TOKEN` | No | Telegram bot token for gateway |
| `WHATSAPP_TOKEN` | No | WhatsApp Cloud API token |
| `FIRECRAWL_API_KEY` | No | Web scraping capabilities |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

---

## Architecture

```
oftalmo-claw/
├── main.py                          # Application entry point
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
│
├── agent/                           # Core AI agent
│   ├── core.py                      # Agent loop & conversation
│   ├── prompt_builder.py            # System prompt assembly
│   ├── memory.py                    # Persistent memory (MEMORY.md)
│   └── context_compressor.py        # Auto context compression
│
├── tools/                           # Agent tools (40+)
│   ├── registry.py                  # Central tool registry
│   ├── ophthalmo_image_tool.py      # Ophthalmic image analysis
│   ├── ophthalmo_report_tool.py     # Report generation
│   ├── ophthalmo_calc_tool.py       # Clinical calculators
│   ├── second_opinion_tool.py       # Second opinion workflow
│   ├── ophthalmo_analytics_tool.py  # Analytics & trends
│   ├── clinical_protocol_tool.py    # Clinical protocols
│   └── ...                          # Web, file, terminal, etc.
│
├── skills/                          # Domain knowledge (Markdown)
│   └── ophthalmology/
│       ├── core/SKILL.md            # Anatomy, pathology, terminology
│       ├── imaging/SKILL.md         # OCT, fundoscopy, fields, topo
│       ├── surgical/SKILL.md        # Surgical procedures
│       ├── pharmacology/SKILL.md    # Ophthalmic drugs
│       ├── second-opinion/SKILL.md  # Second opinion protocols
│       └── analytics/SKILL.md       # Analytics queries
│
├── web/                             # Mission Control (Web UI)
│   ├── app.py                       # FastAPI application
│   ├── templates/                   # Jinja2 HTML templates
│   │   ├── base.html                # Base layout (medical theme)
│   │   ├── dashboard.html           # Main Mission Control
│   │   ├── second_opinion.html      # Second Opinion page
│   │   ├── trends.html              # Trends dashboard
│   │   └── login.html               # Authentication
│   └── static/
│       ├── css/theme.css            # Medical color system
│       └── js/                      # Frontend interactions
│
├── gateway/                         # Messaging platforms
│   ├── run.py                       # Gateway server
│   └── platforms/                   # Telegram, WhatsApp, etc.
│
├── models/                          # Database models
│   ├── case.py                      # Second opinion cases
│   ├── doctor.py                    # Specialist profiles
│   ├── exam.py                      # Exam records
│   └── analytics.py                 # Analytics aggregation
│
├── Dockerfile                       # Container definition
├── railway.json                     # Railway deployment config
├── Procfile                         # Process definitions
└── .env.example                     # Environment template
```

### Design Principles

1. **Agent-First** - The AI agent is the core. Everything else is a tool or interface.
2. **Skills as Knowledge** - Medical knowledge is stored as Markdown skills, easy to update and version.
3. **Tools as Actions** - Each capability (image analysis, calculators, reports) is a registered tool.
4. **Memory Compounds** - The agent learns from every interaction, building expertise over time.
5. **Platform Agnostic** - Same agent accessible via web, CLI, Telegram, WhatsApp, or any gateway.

### Color System

OftalmoClaw uses a medical-grade color palette:

| Color | Hex | Usage |
|-------|-----|-------|
| **Teal** | `#0D9488` | Primary actions, success states |
| **Navy** | `#1E3A5F` | Headers, navigation, authority |
| **White** | `#FFFFFF` | Backgrounds, cards |
| **Slate** | `#F1F5F9` | Secondary backgrounds |
| **Coral** | `#EF4444` | Urgent, critical alerts |
| **Amber** | `#F59E0B` | Warnings, pending states |
| **Emerald** | `#10B981` | Online status, completed |

---

## Skills

OftalmoClaw ships with specialized ophthalmology skills following the [agentskills.io](https://agentskills.io) standard.

### Built-in Skills

| Skill | Description |
|-------|-------------|
| `ophthalmology-core` | Anatomy, pathology, ICD-10, terminology, classifications |
| `ophthalmology-imaging` | OCT, fundoscopy, topography, visual fields, angiography |
| `ophthalmology-surgical` | Phaco, vitrectomy, refractive, MIGS, transplant |
| `ophthalmology-pharmacology` | Eye drops, anti-VEGF, hypotensives, antibiotics |
| `ophthalmology-second-opinion` | Collaborative case workflow protocols |
| `ophthalmology-analytics` | Natural language analytics queries |

### Creating Custom Skills

```markdown
---
name: my-custom-skill
description: Description of the skill
version: 1.0.0
author: Your Name
license: MIT
metadata:
  hermes:
    tags: [ophthalmology, custom]
    category: ophthalmology
---

# My Custom Skill

Instructions for the agent on how to use this skill...
```

---

<h2 id="second-opinion">Second Opinion System</h2>

The Second Opinion system enables real-time collaborative consultations between ophthalmology specialists.

### How It Works

```
1. Doctor A submits a case (images + clinical data)
          |
2. System routes to available specialist(s)
          |
3. AI generates draft analysis for specialist review
          |
4. Specialist B reviews, edits, and submits opinion
          |
5. Discussion thread opens for Q&A
          |
6. Case marked as resolved with final consensus
```

### Case Submission

```python
# Via agent chat
"Submit a second opinion case for a 56-year-old female with
suspected macular edema. Attaching OCT images."

# Via API
POST /api/v1/cases
{
  "patient": { "age": 56, "gender": "F" },
  "history": "Progressive visual loss OS, DM2 for 10 years",
  "images": ["oct_macula_os.dcm"],
  "hypothesis": "Diabetic macular edema",
  "urgency": "urgent",
  "specialty_requested": "retina"
}
```

### Specialist Dashboard

- View pending cases assigned to you
- See available specialists and their status (online/offline)
- Open discussion threads with referring doctor
- View attached images with zoom and annotation tools
- Submit structured opinions with confidence levels

---

<h2 id="dashboard">Trends Dashboard</h2>

The Mission Control trends dashboard provides macro-level analytics for clinical operations.

### Available Metrics

- **Volume & Quality by Period** - Exam counts and quality scores over time
- **Performance by Exam Type** - Fundoscopy, OCT, Visual Fields, Topography, Biometry
- **Operator Rankings** - Doctors ranked by volume and quality score
- **Active Users** - User engagement metrics
- **Pathology Distribution** - Most common diagnoses
- **Second Opinion Stats** - Pending, resolved, average turnaround time
- **Report Turnaround** - Average time from exam to signed report

### Query via Chat

```
"How many OCT exams were performed this month?"
"Show me the top 5 operators by quality score"
"What's the trend for fundoscopy volume in the last quarter?"
"Export the monthly report as CSV"
```

---

## API

OftalmoClaw exposes a RESTful API for integration with external systems.

### Authentication

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://your-instance.railway.app/api/v1/health
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/chat` | Send message to agent |
| `GET` | `/api/v1/cases` | List second opinion cases |
| `POST` | `/api/v1/cases` | Create new case |
| `GET` | `/api/v1/cases/:id` | Get case details |
| `POST` | `/api/v1/cases/:id/opinions` | Submit opinion |
| `GET` | `/api/v1/analytics/trends` | Get trends data |
| `GET` | `/api/v1/analytics/rankings` | Get operator rankings |
| `POST` | `/api/v1/images/analyze` | Analyze ophthalmic image |
| `POST` | `/api/v1/reports/generate` | Generate exam report |
| `GET` | `/api/v1/calculators/iol` | IOL calculation |

### Webhooks

Configure webhooks for real-time notifications:

```json
{
  "url": "https://your-system.com/webhook",
  "events": ["case.created", "opinion.submitted", "case.resolved"],
  "secret": "your-webhook-secret"
}
```

---

## Roadmap

- [x] Core agent with persistent memory
- [x] Skills system (agentskills.io compatible)
- [x] Multi-platform gateway (Telegram, WhatsApp, Discord, etc.)
- [x] Railway deployment support
- [ ] Ophthalmology core skills
- [ ] Image analysis tool (OCT, fundoscopy, topography)
- [ ] Second Opinion system
- [ ] Mission Control web dashboard
- [ ] Trends & analytics dashboard
- [ ] Clinical calculators (IOL, VA conversion, IOP correction)
- [ ] Report generator
- [ ] Protocol engine
- [ ] DICOM integration
- [ ] EHR/FHIR interoperability
- [ ] LGPD compliance module
- [ ] Mobile-responsive Mission Control

---

## Contributing

We welcome contributions from ophthalmologists, developers, and AI researchers.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/my-feature`)
3. **Commit** your changes (`git commit -m 'Add my feature'`)
4. **Push** to the branch (`git push origin feature/my-feature`)
5. **Open** a Pull Request

### Contribution Areas

| Area | Skills Needed | Impact |
|------|---------------|--------|
| **Skills** | Ophthalmology knowledge | High |
| **Tools** | Python, API development | High |
| **Frontend** | HTML/CSS/JS, UI/UX | Medium |
| **Docs** | Technical writing | Medium |
| **Testing** | Python, pytest | Medium |
| **Translations** | Portuguese, Spanish | Low |

### Development Setup

```bash
git clone https://github.com/geekvision/oftalmo-claw.git
cd oftalmo-claw
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
ruff check .
```

---

## Medical Disclaimer

> **OftalmoClaw is NOT a medical device.** It is intended for research, education, and clinical decision support only. It should NOT be used as a substitute for professional medical judgment. All diagnoses and treatment decisions must be made by qualified healthcare professionals. The AI-generated analyses and suggestions require mandatory review and validation by a licensed ophthalmologist before any clinical action.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

**Attribution Required:** Any project using OftalmoClaw must include:

> Built with OftalmoClaw by GeekVision

---

## Acknowledgments

- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** by Nous Research - Architectural foundation
- **[agentskills.io](https://agentskills.io)** - Skill standard specification
- The global ophthalmology community for domain expertise

---

<p align="center">
  <strong>Built with care by <a href="https://github.com/geekvision">GeekVision</a></strong>
  <br />
  <em>Empowering eye care with open-source AI</em>
  <br /><br />
  <img src="https://img.shields.io/badge/ophthalmology-AI-0D9488?style=flat-square" />
  <img src="https://img.shields.io/badge/open-source-1E3A5F?style=flat-square" />
  <img src="https://img.shields.io/badge/made%20in-Brazil-10B981?style=flat-square" />
</p>
