<p align="center">
  <img src="assets/logo.svg" alt="OftalmoClaw" width="120" />
</p>

<h1 align="center">OftalmoClaw</h1>

<p align="center">
  <strong>Mission Control de Oftalmologia com IA</strong>
  <br />
  <em>Agente inteligente para analise de imagens, suporte a decisao clinica e diagnostico colaborativo</em>
</p>

<p align="center">
  <a href="#o-que-e">O que e</a> &bull;
  <a href="#guia-rapido-para-medicos">Guia para Medicos</a> &bull;
  <a href="#usando-com-claude-code">Claude Code</a> &bull;
  <a href="#instalacao-tecnica">Instalacao</a> &bull;
  <a href="#segunda-opiniao">Segunda Opiniao</a> &bull;
  <a href="#dashboard-de-tendencias">Tendencias</a> &bull;
  <a href="#api">API</a> &bull;
  <a href="#contribuindo">Contribuir</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-0D9488?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/licenca-MIT-0D9488?style=for-the-badge" />
  <img src="https://img.shields.io/badge/railway-deploy-0D9488?style=for-the-badge&logo=railway&logoColor=white" />
  <img src="https://img.shields.io/badge/LGPD-compativel-0D9488?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Criado%20por-GeekVision-1E3A5F?style=for-the-badge" />
</p>

---

## O que e

**OftalmoClaw** e um sistema open-source que funciona como um assistente de IA especializado em oftalmologia. Ele combina:

- **Analise de imagens** (OCT, fundoscopia, topografia, campimetria)
- **Segunda opiniao** entre especialistas em tempo real
- **Dashboard de tendencias** com volume de exames, qualidade e rankings
- **Calculadoras clinicas** (LIO, acuidade visual, PIO corrigida)
- **Gerador de laudos** com terminologia padrao

Pense nele como um "painel de controle" para sua clinica ou consultorio, com IA embutida.

### O que NAO e

- **Nao e um dispositivo medico** - nao tem registro ANVISA/FDA
- **Nao substitui o medico** - toda analise precisa de validacao por oftalmologista
- **Nao armazena prontuario** - e um sistema de apoio, nao um PEP/EMR

### Relacao com o Hermes Agent

O OftalmoClaw foi construido com base na arquitetura do [Hermes Agent](https://github.com/NousResearch/hermes-agent), um projeto open-source da Nous Research. Aproveitamos:

| Do Hermes Agent | No OftalmoClaw |
|-----------------|----------------|
| Sistema de skills (conhecimento em Markdown) | Skills especificas de oftalmologia |
| Registry de tools (ferramentas do agente) | Tools de analise de imagem, laudos, calculadoras |
| Gateway de mensagens (Telegram, WhatsApp) | Notificacoes de casos para medicos |
| Memoria persistente entre sessoes | Historico de casos e padroes clinicos |

**Voce NAO precisa instalar o Hermes Agent separadamente.** O OftalmoClaw e um projeto independente que ja inclui tudo que precisa.

---

## Guia Rapido para Medicos

> Se voce nunca mexeu com programacao, este guia e para voce.

### O que voce vai precisar

| Item | O que e | Como conseguir |
|------|---------|----------------|
| **Computador** | Mac, Windows ou Linux | O que voce ja usa |
| **Chave de IA** | Uma "senha" que permite ao sistema usar inteligencia artificial | Veja o passo 1 abaixo |
| **Railway** (opcional) | Um servico na nuvem que roda o sistema 24h | Veja a secao de Deploy |

### Passo 1: Obter sua chave de IA

O OftalmoClaw precisa de uma chave de API para acessar modelos de IA (como o Claude da Anthropic). Voce tem duas opcoes:

#### Opcao A: OpenRouter (mais facil, varios modelos)

1. Acesse [openrouter.ai](https://openrouter.ai)
2. Clique em **"Sign Up"** e crie uma conta (pode usar Google)
3. Va em **"Keys"** no menu lateral
4. Clique em **"Create Key"**
5. Copie a chave que comeca com `sk-or-...`
6. Adicione creditos: va em **"Credits"** e adicione $5 (rende ~500 consultas simples)

#### Opcao B: Anthropic direto (melhor qualidade com Claude)

1. Acesse [console.anthropic.com](https://console.anthropic.com)
2. Crie uma conta
3. Va em **"API Keys"**
4. Clique em **"Create Key"**
5. Copie a chave que comeca com `sk-ant-...`
6. Adicione creditos em **"Billing"** (minimo $5)

#### Quanto custa?

| Uso | Custo estimado/mes |
|-----|--------------------|
| Consultas de texto simples (perguntas clinicas) | ~$2-5 |
| Analise de imagens (OCT, fundoscopia) | ~$5-15 |
| Uso intensivo (clinica com varios medicos) | ~$20-50 |

> Os modelos de IA cobram por "tokens" (palavras processadas). Imagens custam mais que texto. Voce pode acompanhar seus gastos no painel do OpenRouter ou Anthropic.

### Passo 2: Rodar o sistema

#### Caminho facil: Railway (na nuvem, sem instalar nada)

1. Crie uma conta gratis em [railway.app](https://railway.app) (pode usar GitHub ou Google)
2. Clique em **"New Project"** > **"Deploy from GitHub repo"**
3. Conecte este repositorio
4. Em **"Variables"**, adicione:
   - `OPENROUTER_API_KEY` = sua chave do passo 1
   - `SECRET_KEY` = qualquer frase longa (ex: `minha-clinica-oftalmologia-2024`)
5. Clique em **"Deploy"**
6. Em ~2 minutos voce tera uma URL como `oftalmo-claw-production.up.railway.app`
7. Abra essa URL no navegador - pronto!

**Custo do Railway:** Plano Starter e gratuito para testes. Plano Pro custa $5/mes para uso continuo.

#### Caminho local: No seu computador

Se voce prefere rodar no seu proprio computador (mais privado, sem custo de servidor):

```bash
# 1. Instale o Python 3.11+ (se nao tiver)
#    Mac: baixe em python.org ou use "brew install python"
#    Windows: baixe em python.org e marque "Add to PATH" na instalacao

# 2. Baixe o projeto (no Terminal/Prompt de Comando)
git clone https://github.com/geekvision/oftalmo-claw.git
cd oftalmo-claw

# 3. Prepare o ambiente
python -m venv .venv
source .venv/bin/activate    # Mac/Linux
# .venv\Scripts\activate     # Windows

# 4. Instale as dependencias
pip install -r requirements.txt

# 5. Configure sua chave de IA
cp .env.example .env
# Abra o arquivo .env com qualquer editor de texto
# e cole sua chave na linha OPENROUTER_API_KEY=

# 6. Inicie!
python main.py
```

Abra o navegador em `http://localhost:8000` e voce vera o Mission Control.

### O que voce vai ver

Ao abrir o sistema, voce tera acesso a:

**Mission Control (pagina principal)**
- Resumo do dia: exames realizados, casos pendentes, especialistas online
- Acesso rapido a todas as ferramentas
- Ultimos casos de segunda opiniao

**Segunda Opiniao**
- Lista de casos pendentes com nivel de urgencia
- Painel de especialistas disponiveis (Retina, Glaucoma, Cornea...)
- Discussao por caso com historico completo
- Upload de imagens (OCT, retinografia, etc.)

**Dashboard de Tendencias**
- Volume de exames por periodo (semana/mes/trimestre/ano)
- Score de qualidade por tipo de exame
- Ranking de operadores por produtividade e qualidade
- Exportacao para CSV/PDF

---

<h2 id="usando-com-claude-code">Usando com Claude Code</h2>

Se voce ja usa o **Claude Code** (a ferramenta de linha de comando da Anthropic), pode integra-lo diretamente com o OftalmoClaw para desenvolver, personalizar e operar o sistema.

### O que e o Claude Code?

O Claude Code e um assistente de programacao que roda no seu terminal. Voce conversa com ele em portugues e ele edita codigo, roda comandos e resolve problemas. E como ter um programador assistente 24h.

### Como usar juntos

```bash
# 1. Abra o terminal na pasta do projeto
cd oftalmo-claw

# 2. Inicie o Claude Code
claude

# 3. Agora voce pode pedir coisas como:

> "Adicione um novo tipo de exame chamado Paquimetria no dashboard de tendencias"

> "Crie uma skill de farmacologia com os colirios mais usados em glaucoma"

> "Configure o gateway do Telegram para eu receber notificacoes de novos casos"

> "Adicione um campo de CID-10 no formulario de segunda opiniao"

> "Mude a cor do cabecalho para azul mais escuro"
```

### Fluxo recomendado

```
Voce (medico) descreve o que quer em portugues
        |
Claude Code entende e edita o codigo
        |
Voce testa no navegador (localhost:8000)
        |
Gostou? Peca para o Claude fazer deploy no Railway
        |
Nao gostou? Descreva o ajuste e ele corrige
```

### Dicas para medicos usando Claude Code

- **Seja especifico**: em vez de "melhore o sistema", diga "adicione um campo de pressao intraocular no caso de segunda opiniao"
- **Descreva como medico**: use termos clinicos naturalmente - "quero classificar por ETDRS", "incluir escala de Shaffer"
- **Peca screenshots**: diga "abra o navegador e me mostre como ficou"
- **Salve versoes**: diga "faca um commit com essas mudancas" para nao perder trabalho

### Arquivo CLAUDE.md

O projeto inclui um arquivo `CLAUDE.md` na raiz que da contexto ao Claude Code sobre o projeto. Isso faz com que ele entenda automaticamente:

- A estrutura de pastas e arquivos
- O padrao de skills (Markdown com frontmatter YAML)
- O padrao de tools (registro no registry.py)
- O tema de cores medicas
- As convencoes do projeto

---

## Funcionalidades

### Hoje (implementado)

| Funcionalidade | Status | Descricao |
|---------------|--------|-----------|
| Mission Control | MVP | Dashboard principal com stats e acesso rapido |
| Segunda Opiniao | MVP | Interface de casos, especialistas, urgencia |
| Dashboard Tendencias | MVP | Volume, qualidade, rankings (dados demo) |
| Skills Oftalmologicas | Parcial | Core e Imaging completos, outros em andamento |
| Calculadora IOL | MVP | SRK/T simplificado via API |
| Conversor Acuidade | Pronto | Snellen, decimal, LogMAR |
| Login | UI | Tela pronta, auth em desenvolvimento |
| API REST | MVP | Endpoints para cases, analytics, calculadoras |
| Deploy Railway | Pronto | Dockerfile + railway.json configurados |

### Em desenvolvimento

| Funcionalidade | Prioridade | Descricao |
|---------------|-----------|-----------|
| Analise de imagens com IA | Alta | Upload + interpretacao de OCT, fundoscopia |
| Conexao com LLM | Alta | Integrar agente com OpenRouter/Anthropic |
| Autenticacao real | Alta | Login com CRM, sessoes, permissoes |
| Banco de dados real | Alta | Migrar de dados demo para PostgreSQL |
| Notificacoes WhatsApp | Media | Alertas de novos casos via WhatsApp |
| Gerador de laudos | Media | Templates por tipo de exame |
| Protocolos clinicos | Media | Fluxogramas AAO, CBO, EURETINA |
| Skills cirurgica + farmaco | Media | Facoemulsificacao, anti-VEGF, colirios |
| DICOM | Baixa | Leitura de arquivos de equipamentos |
| LGPD | Baixa | Anonimizacao, consentimento, audit trail |

---

<h2 id="segunda-opiniao">Sistema de Segunda Opiniao</h2>

Permite que medicos enviem casos clinicos para consulta com outros especialistas.

### Fluxo

```
Medico A envia caso (imagens + historia clinica)
        |
Sistema identifica especialistas disponiveis
        |
IA gera rascunho de analise (opcional)
        |
Especialista B revisa e emite parecer
        |
Thread de discussao entre os medicos
        |
Caso encerrado com consenso final
```

### Dados do caso

- **Paciente**: idade, sexo, historico relevante (anonimizado)
- **Queixa principal**: descricao do problema
- **Exames**: imagens anexadas (OCT, retinografia, campo visual, etc.)
- **Hipotese diagnostica**: o que o medico solicitante suspeita
- **Urgencia**: Normal, Urgente (24h), Emergencia (imediato)
- **Especialidade**: Retina, Glaucoma, Cornea, Refrativa, Oculoplastica, Estrabismo, Neuro-oftalmo, Uveite

### Especialidades e roteamento

| Especialidade | Quando encaminhar |
|--------------|-------------------|
| **Retina** | DMRI, retinopatia diabetica, RVO, descolamento, maculopatia |
| **Glaucoma** | PIO elevada, dano no nervo optico, perda de campo visual |
| **Cornea** | Ceratocone, infeccoes, ectasia, transplante |
| **Refrativa** | Candidatura LASIK/PRK, ICL, surpresa refrativa |
| **Oculoplastica** | Palpebras, vias lacrimais, orbita |
| **Estrabismo** | Desalinhamento, diplopia |
| **Neuro-oftalmo** | Neurite optica, papiledema, paralisia de nervos cranianos |
| **Uveite** | Inflamacao intraocular, doencas autoimunes |

---

<h2 id="dashboard-de-tendencias">Dashboard de Tendencias</h2>

Visao macro do desempenho da clinica/servico.

### Metricas disponiveis

- **Volume por periodo** - Quantidade de exames por semana/mes/trimestre/ano
- **Score de qualidade** - Media por tipo de exame e por operador
- **Performance por tipo de exame** - Fundoscopia, OCT, Campimetria, Topografia, Biometria
- **Ranking de operadores** - Medicos ordenados por volume e qualidade
- **Usuarios ativos** - Quantos medicos estao usando o sistema
- **Segunda opiniao** - Casos pendentes, resolvidos, tempo medio de resposta
- **Tempo de laudo** - Media entre exame e assinatura do laudo

### Consulta por chat (com IA conectada)

Quando o agente de IA estiver configurado, voce podera perguntar em linguagem natural:

```
"Quantos OCTs fizemos este mes?"
"Quem e o operador com melhor score de qualidade?"
"Qual a tendencia de fundoscopias no ultimo trimestre?"
"Exporta o relatorio mensal em CSV"
```

---

## API

O sistema expoe uma API REST para integracao com outros sistemas (prontuario, equipamentos, apps).

### Endpoints principais

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/health` | Verifica se o sistema esta rodando |
| `POST` | `/api/v1/chat` | Envia mensagem para o agente de IA |
| `GET` | `/api/v1/cases` | Lista casos de segunda opiniao |
| `POST` | `/api/v1/cases` | Cria novo caso |
| `GET` | `/api/v1/cases/:id` | Detalhes de um caso |
| `POST` | `/api/v1/cases/:id/opinions` | Envia parecer sobre um caso |
| `GET` | `/api/v1/analytics/trends` | Dados de tendencias |
| `GET` | `/api/v1/analytics/rankings` | Ranking de operadores |
| `GET` | `/api/v1/calculators/iol` | Calculo de LIO (SRK/T) |
| `GET` | `/api/v1/calculators/va-convert` | Conversao de acuidade visual |

### Exemplo: Calcular LIO

```
GET /api/v1/calculators/iol?al=23.5&k1=43.0&k2=44.0&target=-0.5

Resposta:
{
  "result": {
    "iol_power": 20.55,
    "formula": "SRK/T (simplified)",
    "disclaimer": "For educational purposes only."
  }
}
```

### Exemplo: Converter acuidade visual

```
GET /api/v1/calculators/va-convert?snellen=20/40

Resposta:
{
  "snellen": "20/40",
  "decimal": 0.5,
  "logmar": 0.3,
  "category": "Mild vision loss"
}
```

---

<h2 id="instalacao-tecnica">Instalacao Tecnica (para desenvolvedores)</h2>

### Pre-requisitos

- Python 3.11+
- Git
- Uma chave de API (OpenRouter ou Anthropic)

### Setup completo

```bash
# Clonar
git clone https://github.com/geekvision/oftalmo-claw.git
cd oftalmo-claw

# Ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Configurar
cp .env.example .env
# Edite .env com suas chaves

# Rodar
python main.py
```

### Modos de execucao

```bash
python main.py                  # Web (Mission Control) - padrao
python main.py --mode cli       # Agente por linha de comando
python main.py --mode gateway   # Gateway de mensagens (Telegram, WhatsApp)
python main.py --setup          # Assistente de configuracao
```

### Deploy no Railway

1. Faca fork deste repositorio no GitHub
2. Crie conta em [railway.app](https://railway.app)
3. New Project > Deploy from GitHub repo
4. Adicione as variaveis de ambiente:

| Variavel | Obrigatoria | Descricao |
|----------|-------------|-----------|
| `OPENROUTER_API_KEY` | Sim | Chave do OpenRouter para acesso a IA |
| `SECRET_KEY` | Sim | Frase secreta para criptografia de sessao |
| `DATABASE_URL` | Nao | URL do PostgreSQL (Railway provisiona automaticamente) |
| `PORT` | Nao | Porta do servidor (padrao: 8000) |
| `ANTHROPIC_API_KEY` | Nao | Chave da Anthropic (alternativa ao OpenRouter) |
| `TELEGRAM_TOKEN` | Nao | Token do bot Telegram para notificacoes |
| `WHATSAPP_TOKEN` | Nao | Token WhatsApp Cloud API |
| `LOG_LEVEL` | Nao | Nivel de log: INFO, DEBUG, WARNING |

5. Deploy automatico via Dockerfile incluido.

### Docker local

```bash
docker build -t oftalmo-claw .

docker run -d \
  --name oftalmo-claw \
  -p 8000:8000 \
  -e OPENROUTER_API_KEY=sk-or-sua-chave \
  -e SECRET_KEY=sua-frase-secreta \
  -v oftalmo-data:/app/data \
  oftalmo-claw
```

### Estrutura do projeto

```
oftalmo-claw/
├── main.py                     # Ponto de entrada
├── config.py                   # Configuracoes (.env)
├── requirements.txt            # Dependencias Python
│
├── web/                        # Mission Control (interface web)
│   ├── app.py                  # Aplicacao FastAPI
│   ├── routes/                 # Rotas da API
│   │   ├── dashboard.py        # Stats do painel principal
│   │   ├── cases.py            # CRUD de casos (segunda opiniao)
│   │   ├── analytics.py        # Tendencias e rankings
│   │   └── api.py              # Chat, calculadoras
│   ├── templates/              # Paginas HTML
│   │   ├── base.html           # Layout base (sidebar, tema)
│   │   ├── dashboard.html      # Mission Control
│   │   ├── second_opinion.html # Segunda Opiniao
│   │   ├── trends.html         # Dashboard de Tendencias
│   │   └── login.html          # Tela de login
│   └── static/
│       ├── css/theme.css       # Tema medico (cores, componentes)
│       └── js/app.js           # Interacoes frontend
│
├── agent/                      # Agente de IA
│   └── core.py                 # Loop principal do agente
│
├── tools/                      # Ferramentas do agente
│   └── registry.py             # Registro central de tools
│
├── skills/                     # Conhecimento (Markdown)
│   └── ophthalmology/
│       ├── core/SKILL.md       # Anatomia, patologias, CID-10
│       ├── imaging/SKILL.md    # OCT, fundoscopia, campo visual
│       ├── second-opinion/     # Protocolo de consulta
│       └── analytics/          # Queries de analytics
│
├── models/                     # Modelos do banco de dados
│   ├── database.py             # Conexao SQLAlchemy
│   ├── case.py                 # Caso, Opiniao, Mensagem, Imagem
│   ├── doctor.py               # Medico / Especialista
│   └── exam.py                 # Registro de exame, snapshots
│
├── gateway/                    # Integracoes de mensagem
│   └── platforms/              # Telegram, WhatsApp, etc.
│
├── Dockerfile                  # Container para deploy
├── railway.json                # Config Railway
├── Procfile                    # Processos (web + worker)
└── .env.example                # Exemplo de configuracao
```

### Skills: como funcionam

Skills sao arquivos Markdown que dao conhecimento especializado ao agente. Ficam em `skills/ophthalmology/` e seguem o padrao [agentskills.io](https://agentskills.io):

```markdown
---
name: minha-skill
description: O que esta skill ensina ao agente
version: 1.0.0
author: Seu Nome
license: MIT
metadata:
  hermes:
    tags: [ophthalmology, minha-area]
    category: ophthalmology
---

# Titulo

Conteudo que o agente vai "saber"...
```

**Skills incluidas:**

| Skill | Conteudo |
|-------|----------|
| `core` | Anatomia ocular, patologias, CID-10, classificacoes (Shaffer, LOCS III, AREDS) |
| `imaging` | Interpretacao de OCT, fundoscopia, campimetria, topografia, biometria |
| `second-opinion` | Protocolo de consulta colaborativa, checklist, roteamento |
| `analytics` | Queries em linguagem natural para o dashboard |

**Para criar uma nova skill:** crie uma pasta em `skills/ophthalmology/` com um arquivo `SKILL.md` seguindo o formato acima.

---

## Contribuindo

Aceitamos contribuicoes de oftalmologistas, desenvolvedores e pesquisadores.

### Como contribuir

1. Faca **Fork** do repositorio
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Faca suas alteracoes e commit: `git commit -m 'Adiciona minha feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um **Pull Request**

### Areas de contribuicao

| Area | Perfil | Impacto |
|------|--------|---------|
| **Skills clinicas** | Oftalmologista | Alto - melhora diretamente o conhecimento da IA |
| **Protocolos** | Oftalmologista | Alto - guidelines baseados em evidencia |
| **Tools/API** | Desenvolvedor Python | Alto - novas funcionalidades |
| **Frontend** | Desenvolvedor Web | Medio - melhorias na interface |
| **Testes** | Desenvolvedor | Medio - estabilidade |
| **Traducoes** | Qualquer | Baixo - acessibilidade |

### Para oftalmologistas sem experiencia em codigo

Voce pode contribuir sem programar:

1. **Abra uma Issue** descrevendo uma funcionalidade que faria diferenca na sua pratica
2. **Revise as skills** - leia os arquivos em `skills/ophthalmology/` e sugira correcoes ou adicoes
3. **Teste o sistema** e reporte bugs ou sugestoes de melhoria
4. **Compartilhe protocolos** que poderiam ser incluidos como skills

---

## Aviso Medico

> **OftalmoClaw NAO e um dispositivo medico.** Destina-se exclusivamente a pesquisa, educacao e suporte a decisao clinica. NAO deve ser usado como substituto do julgamento medico profissional. Todos os diagnosticos e decisoes de tratamento devem ser feitos por profissionais de saude qualificados. As analises e sugestoes geradas por IA requerem revisao e validacao obrigatoria por oftalmologista habilitado antes de qualquer acao clinica.

---

## Licenca

MIT License - veja [LICENSE](LICENSE) para detalhes.

**Atribuicao obrigatoria:** qualquer projeto que use o OftalmoClaw deve incluir:

> Built with OftalmoClaw by GeekVision

---

## Agradecimentos

- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** da Nous Research - base arquitetural
- **[agentskills.io](https://agentskills.io)** - padrao de skills
- Comunidade global de oftalmologia

---

<p align="center">
  <strong>Feito com cuidado por <a href="https://github.com/geekvision">GeekVision</a></strong>
  <br />
  <em>Empoderando o cuidado ocular com IA open-source</em>
  <br /><br />
  <img src="https://img.shields.io/badge/oftalmologia-IA-0D9488?style=flat-square" />
  <img src="https://img.shields.io/badge/open--source-1E3A5F?style=flat-square" />
  <img src="https://img.shields.io/badge/feito%20no-Brasil-10B981?style=flat-square" />
</p>

---

<details>
<summary><strong>English version (click to expand)</strong></summary>

OftalmoClaw is an open-source, AI-powered ophthalmology mission control platform. It provides image analysis, second opinion workflows, clinical calculators, and a trends dashboard for eye care professionals.

Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent) architecture by Nous Research.

For the full English documentation, see [docs/README_EN.md](docs/README_EN.md).

</details>
