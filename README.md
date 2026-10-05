# EventOS — API REST para Gerenciamento de Eventos e Festivais

API desenvolvida em **FastAPI** e **PostgreSQL** para centralizar o ciclo de vida de eventos, incluindo cadastro de usuários, gestão de eventos, programação de atividades, vendas de ingressos e inscrições com controle de capacidade e segurança via JWT.

##  Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI** — Framework web assíncrono RESTful
* **SQLAlchemy 2.0** — ORM para mapeamento objeto-relacional
* **Alembic** — Migrações e controle de versão do banco
* **Pydantic v2** — Validação rigorosa de tipos e schemas
* **PyJWT / Passlib (bcrypt)** — Autenticação e segurança de senhas
* **Pytest** — Testes automatizados de integração e regras de negócio

---

##  Estrutura do Projeto

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

# Como Executar a Aplicação

## 1. Instalar as dependências
``bash
pip install -r requirements.txt
``
## 2. Iniciar o Servidor FastAPI
``bash
uvicorn app.main:app --reload
``

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---


##  Perfis de Acesso (RBAC)

* **Admin:** Acesso irrestrito a todas as rotas e exclusão de eventos (`RN10`).
* **Organizador:** Pode criar eventos, editar os próprios eventos (`RN09`) e adicionar atividades e ingressos aos seus eventos.
* **Participante:** Consulta eventos/atividades, realiza inscrições (`RN06`, `RN07`) e cancela a própria inscrição (`RN08`).
