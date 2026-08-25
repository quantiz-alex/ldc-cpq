# LDC Insumos — Plataforma Comercial (CPQ Inteligente)

Plataforma comercial que digitaliza e automatiza o processo de captação, configuração,
precificação e cotação (CPQ) de pedidos de defensivos e fertilizantes da LDC Insumos. O
sistema recebe demandas que hoje chegam de forma dispersa (WhatsApp, e-mail, texto e
imagem), estrutura o pedido em um formulário padronizado e aplica análises automáticas de
consistência antes que o pedido siga para o trader — que valida, questiona ou aprova a
cotação. O motor de recomendação sugere produtos complementares com base no histórico de
compras e na sazonalidade da cultura.

## Stack Tecnológico

| Camada | Tecnologia |
|---|---|
| Frontend | Dash 2.17+, Dash Bootstrap Components, Dash AG Grid, Plotly |
| Processamento de dados | Pandas, NumPy |
| Backend | FastAPI, SQLAlchemy 2.x, Pydantic v2 |
| Autenticação | JWT (python-jose) + bcrypt (passlib) |
| Banco de dados | SQL Server / Microsoft Fabric via pyodbc (fallback SQLite em dev) |
| Testes | Pytest (backend), Cypress (frontend/E2E) |

## Estrutura de Pastas

```
ldc-cpq/
├── backend/
│   ├── models/            # Entidades SQLAlchemy
│   ├── schemas/           # Schemas Pydantic v2 (Create/Update/Response + validações de negócio)
│   ├── repositories/       # Acesso a dados (CRUD puro)
│   ├── services/           # Regras de negócio, orquestração e workflows
│   ├── api/routes/         # Endpoints FastAPI
│   ├── auth.py             # JWT, hashing de senha, dependência get_current_user
│   ├── config.py           # Settings (.env)
│   ├── database.py         # Engine, sessão, create_tables()
│   └── main.py              # App FastAPI + CORS + routers
├── frontend/
│   ├── components/          # Componentes reutilizáveis Dash
│   └── pages/                # Páginas do app (por módulo)
├── docs/                     # YAMLs gerados (requirements, data_model, api_contracts, business_logic, screens)
├── database/                  # Scripts SQL (schema, views, procedures, seed)
├── mock_data/                  # Dados de teste (CSV + JSON por entidade)
├── tests/
│   ├── backend/                 # Testes Pytest da API
│   ├── frontend/                 # Testes Cypress do Dash
│   └── integration/               # Testes ponta a ponta
├── requirements.txt
└── .env.example
```

## Como Rodar

### 1. Configurar ambiente

```bash
cp .env.example .env
# edite .env com as credenciais reais (ou mantenha USE_SQLITE=true para desenvolvimento local)
```

### 2. Instalar dependências

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

```bash
pip install -r requirements.txt
```

### 3. Rodar o backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

A API sobe em `http://localhost:8000` — documentação interativa em `/docs` (Swagger) e
`/redoc`. Health check em `GET /health`.

### 4. Rodar o frontend (Dash)

```bash
python -m frontend.app
```

O app sobe em `http://localhost:1050`.

## Deploy no Render

O repositório traz um blueprint (`render.yaml`) que publica **apenas o frontend Dash**
como Web Service. É o suficiente para a demo: as telas leem `mock_data/*.csv` com
pandas e não dependem da API FastAPI.

### Passos

1. No Render: **New + → Blueprint**
2. Conecte o repositório `quantiz-alex/ldc-cpq` e selecione a branch `main`
3. O Render lê o `render.yaml` e cria o serviço — clique em **Apply**

Não há variável de ambiente obrigatória. `APP_ENV` e `APP_DEBUG` já vêm definidas
no blueprint.

### Como o serviço sobe

| Item | Valor |
| --- | --- |
| Build | `pip install -r requirements.txt` |
| Start | `gunicorn frontend.app:server --bind 0.0.0.0:$PORT --workers 1` |
| Objeto WSGI | `server = app.server`, em `frontend/app.py` |
| Python | fixado em `.python-version` |
| Health check | `/` |

### Limitações conhecidas (plano free)

- **Disco efêmero.** As telas de Captação, Fila de Validação e Administração gravam
  de volta nos CSVs (`to_csv`). Esse conteúdo é perdido a cada deploy, restart ou
  hibernação — os dados voltam ao estado versionado no repositório.
- **`--workers 1` é obrigatório.** Dois processos gravando no mesmo CSV corrompem o
  arquivo. Não aumente o número de workers enquanto a persistência for em CSV.
- **Hibernação.** O serviço dorme após ~15 min sem tráfego; o primeiro acesso
  seguinte leva algumas dezenas de segundos para responder.
- **Login sem senha.** A autenticação valida apenas se o email existe em
  `mock_data/usuarios.csv` (ver seção *Autenticação*). Numa URL pública, qualquer
  pessoa que saiba um dos emails entra.

### Dependências e o `pyodbc`

`pyodbc` foi movido para `requirements-sqlserver.txt`. Ele exige unixODBC e o
Microsoft ODBC Driver 18 (bibliotecas de sistema) e **falha ao compilar** no runtime
Python do Render. Como nada em produção usa SQL Server hoje, ele sai do caminho:

```bash
pip install -r requirements.txt              # runtime (é o que o Render usa)
pip install -r requirements-dev.txt          # + pytest, httpx, requests
pip install -r requirements-sqlserver.txt    # + pyodbc (local, para SQL Server/Fabric)
```

## Páginas Disponíveis

| Módulo | Rota | Descrição |
|---|---|---|
| Dashboard Comercial | `/dashboard` | KPIs de receita, volume, mix de produtos e fila de validação |
| Captação de Pedido (CPQ) | `/captacao-pedido` | Formulário de pedido, itens parcelados por janela, importação assistida |
| Fila de Validação do Trader | `/fila-validacao` | Aprovar, rejeitar ou devolver pedidos pendentes |
| Motor de Recomendação (Cross-sell) | `/recomendacoes` | Sugestões de produto por cliente |
| Relatórios Comerciais | `/relatorios` | Receita por período, eficiência de triagem |
| Administração | `/administracao` | Usuários, catálogo de produtos e preços por janela |

## Autenticação

- `POST /api/v1/auth/login` — recebe `{"email": ..., "password": ...}`, retorna
  `{"access_token", "token_type", "expires_in"}`.
- `POST /api/v1/auth/refresh` — renova o token do usuário autenticado (`Authorization: Bearer <token>`).
- Todos os demais endpoints de `/api/v1/*` exigem o header `Authorization: Bearer <token>`.

## Regras de Negócio Implementadas (destaques)

- **RN-004** (`pedido_itens`) — `preco_unitario`/`subtotal` calculados automaticamente por
  lookup em `precos_por_janela` (produto + janela + condição comercial). Ver
  `backend/services/pedido_itens.py::calcular_precificacao`, chamada em `criar()`/`atualizar()`
  e também exposta como consulta isolada em `GET /api/v1/precos-por-janela/lookup`.
- **RN-003 / RN-006 / RN-008 / RN-017** — validações de negócio (completude do pedido antes
  do envio, soma de quantidades parceladas por janela, comentário obrigatório em
  rejeição/devolução, e-mail único) — ver `docs/business_logic.yaml` e os comentários em
  `backend/schemas/pedidos.py`, `backend/schemas/pedido_itens.py` e `backend/schemas/usuarios.py`.
- **RN-007 / RN-009 / RN-010 / RN-011** — workflow de aprovação da Fila de Validação do
  Trader (`POST /api/v1/pedidos/{id}/submit|approve|reject|return`) — ver
  `backend/services/pedidos.py`.

## Testes

```bash
# Backend (Pytest)
pytest tests/backend -v

# Frontend / E2E (Cypress) — requer o frontend e o backend rodando
npx cypress run --spec "tests/frontend/**/*.cy.js"
npx cypress open   # modo interativo
```

> Os diretórios `tests/backend`, `tests/frontend` e `tests/integration` existem, mas os
> arquivos de teste ainda não foram gerados — execute o agente `test-writer` (standalone)
> após validar o build com o cliente.

## Próximos Passos

- Substituir o SQLite de desenvolvimento pela conexão real com SQL Server / Microsoft
  Fabric (preencher `DB_SERVER`, `DB_USER`, `DB_PASSWORD` no `.env` e definir `USE_SQLITE=false`).
  Rodar `database/schema.sql` (e demais scripts em `database/`) contra o ambiente real.
  A camada SQLAlchemy já é compatível com `mssql+pyodbc` — nenhuma alteração de código é
  necessária além da configuração de ambiente.
- Detalhar RN-013 (fórmula/pesos do score do motor de recomendação) no `roadmap.md` — hoje
  marcada como `parsed: false` em `docs/business_logic.yaml`; o campo `score` é aceito no
  payload de criação, mas o cálculo automático ainda não está implementado.
- Gerar a suíte de testes (Pytest + Cypress) com o agente `test-writer`.
- Ligar `frontend/pages/login/login_callbacks.py` à API real (`POST /api/v1/auth/login`)
  quando a página de login for gerada pelo `frontend-builder`.
