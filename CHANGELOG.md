# Changelog

Todas as mudanças relevantes do OftalmoClaw estao documentadas aqui.

## [0.2.0] - 2026-03-21

### Adicionado
- **Formulario "Novo Caso"** — modal com 10 campos (idade, sexo, queixa, achados, hipotese, historia, urgencia, especialidade, medico solicitante, encaminhamento) que envia para `POST /api/v1/cases/`
- **Detalhe do caso** — clicar em um caso abre modal com dados completos, timeline de opinioes e discussao
- **Chat com IA** — pagina `/chat` com suporte a OpenRouter, Anthropic e OpenAI
- **5 sugestoes rapidas no chat** — chips clicaveis: DME, olho vermelho, glaucoma, trabeculectomia, OCT
- **Calculadoras clinicas** — pagina `/calculators` com LIO (SRK/T), conversor AV (Snellen/Decimal/LogMAR), correcao PIO (Ehlers)
- **Validacao nas calculadoras** — rejeita valores fora do range clinico (ex: comprimento axial <15 ou >40mm)
- **Botao "Imprimir resultado"** nas calculadoras com `@media print` otimizado
- **Tabela de referencia rapida** de acuidade visual com classificacao
- **Sistema de toast notifications** — `showToast(msg, type)` com auto-dismiss em 4s
- **Loading skeletons** — animacao shimmer substitui "Carregando..." em todas as paginas
- **Busca global** — barra na topbar busca por caso, paciente, medico
- **Notificacoes** — sino com badge vermelho mostrando casos pendentes
- **Perfil do usuario** — avatar, nome, role no topbar com dropdown (Perfil, Config, Sair)
- **Menu hamburger mobile** — sidebar toggle com overlay semi-transparente
- **PWA** — manifest.json + icones 192px/512px + meta tags Apple
- **Banner de boas-vindas** — aparece na primeira visita, some apos clicar "Entendi"
- **Cards guiados** — "O que voce gostaria de fazer?" com 4 acoes explicadas
- **Intro boxes** — explicacoes em cada pagina para primeiro uso (dismissiveis)
- **Disclaimer medico global** — footer em todas as paginas
- **Empty states com SVG** — ilustracoes e botoes CTA quando nao ha dados
- **Timestamps no chat** — hora (HH:MM) abaixo de cada mensagem
- **Markdown no chat** — bold, italic, code, listas, headers nas respostas da IA
- **Timeline visual** — dots coloridos para opinioes (azul) e mensagens (cinza) no detalhe do caso

### Melhorado
- **Dashboard** — redesenhado com layout guiado, stats colapsaveis, menos sobrecarga visual
- **Segunda Opiniao** — casos carregados da API real (nao mais hardcoded), especialistas dinamicos
- **Tendencias** — dados carregados da API real, skeleton loading, error handling
- **theme.css** — de 719 para ~1150 linhas com modal, toast, skeleton, form, table, utilities
- **app.js** — de 39 para ~230 linhas com toast, modal, search, markdown, sidebar
- **Error handling** — `.catch(() => {})` substituido por toasts informativos
- **Inline styles eliminados** — utility classes e CSS classes nomeadas
- **CSS duplicado removido** — intro-box, welcome, action-cards movidos para theme.css
- **Focus-visible** — outline de acessibilidade em todos os elementos interativos
- **Micro-interacoes** — fadeIn na pagina, hover em cards, press em botoes

### Corrigido
- Sidebar: links atualizados para paginas reais (calculadoras, chat)
- Sidebar: itens "Em breve" usam `.nav-item.disabled` em vez de inline styles
- Titulo da pagina Tendencias alinhado com sidebar (`Tendencias` em vez de `Dashboard de Tendencias`)
- Badge de casos pendentes na sidebar atualizado dinamicamente

## [0.1.0] - 2026-03-20

### Adicionado
- Estrutura inicial do projeto (FastAPI + SQLAlchemy + Jinja2)
- Mission Control com dashboard de stats
- Sistema de segunda opiniao com CRUD completo
- Dashboard de tendencias com volume e rankings
- API REST com 15+ endpoints
- Skills oftalmologicas (core, imaging, second-opinion, analytics)
- Seed de dados demo (5 medicos, 3 casos, 900 exames)
- Deploy Railway (Dockerfile + railway.json)
- Tema medico com paleta de cores (Teal, Navy, Coral, Amber, Emerald)
