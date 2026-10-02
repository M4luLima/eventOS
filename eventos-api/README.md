# EventOS — API REST para Gerenciamento de Eventos e Festivais

API desenvolvida em **FastAPI** e **PostgreSQL** para centralizar o ciclo de vida de eventos, incluindo cadastro de usuários, gestão de eventos, programação de atividades, vendas de ingressos e inscrições com controle de capacidade e segurança via JWT.

## 🚀 Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI** — Framework web assíncrono RESTful
* **SQLAlchemy 2.0** — ORM para mapeamento objeto-relacional
* **Alembic** — Migrações e controle de versão do banco
* **Pydantic v2** — Validação rigorosa de tipos e schemas
* **PyJWT / Passlib (bcrypt)** — Autenticação e segurança de senhas
* **Pytest** — Testes automatizados de integração e regras de negócio

---

## 📁 Estrutura do Projeto

```text
eventos-api/
├── app/
│   ├── main.py              # Ponto de entrada da aplicação FastAPI
│   ├── database.py          # Configuração da sessão e engine SQLAlchemy
│   ├── core/
│   │   ├── config.py        # Configurações globais e variáveis de ambiente
│   │   ├── security.py      # Funções de Hash de senha e geração JWT
│   │   └── deps.py          # Injeção de dependências e controle RBAC
│   ├── models/              # Modelos do Banco de Dados (ORM)
│   ├── schemas/             # Schemas de Validação (Pydantic)
│   └── routers/             # Rotas e Endpoints organizados por recurso
├── alembic/                 # Script de migração de banco de dados
├── tests/                   # Suíte de testes automatizados com Pytest
├── .env.example             # Exemplo de arquivo de configuração
├── requirements.txt         # Dependências do projeto
└── README.md
```

---

## ⚙️ Como Executar a Aplicação

### 1. Clonar o repositório e criar o ambiente virtual
```bash
git clone <URL_DO_REPOSITORIO>
cd eventos-api
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env` e configure suas credenciais do banco PostgreSQL:
```bash
cp .env.example .env
```

### 4. Executar as Migrações do Banco
```bash
alembic upgrade head
```

### 5. Iniciar o Servidor FastAPI
```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa no navegador:
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Como Executar os Testes Automatizados

```bash
pytest -v
```

---

## 🔐 Perfis de Acesso (RBAC)

* **Admin:** Acesso irrestrito a todas as rotas e exclusão de eventos (`RN10`).
* **Organizador:** Pode criar eventos, editar os próprios eventos (`RN09`) e adicionar atividades e ingressos aos seus eventos.
* **Participante:** Consulta eventos/atividades, realiza inscrições (`RN06`, `RN07`) e cancela a própria inscrição (`RN08`).
