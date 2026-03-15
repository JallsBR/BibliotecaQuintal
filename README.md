# Biblioteca Quintal

Sistema de gestão de biblioteca com **backend Django (REST)** e **frontend Vue 3**. Documentação de contexto para IA em `docs/ai/`.

## Estrutura do projeto

- **`api/`** — Backend Django (API REST, JWT, MySQL). Inclui API de auth para superuser: grupos, permissões, usuários. Ver `docs/ai/backend-context.md`.
- **`front/`** — Frontend Vue 3 + Vite + PrimeVue. Inclui página Configuração (superuser), controle de botões por permissão Django e serviços de configuração. Ver `docs/ai/frontend-context.md`.
- **`docs/ai/`** — Documentos de contexto para assistentes de IA (backend e frontend).

## Desenvolvimento com Docker

Requisitos: Docker e Docker Compose (`docker-compose` ou `docker compose`).

```bash
# Subir apenas a API e o banco
docker-compose up --build
# ou: docker compose up --build
```

- **API:** http://localhost:8000  
- **Admin Django:** http://localhost:8000/admin/  
- **MySQL:** porta 3308, banco `bibliotecaquintal` (credenciais em `docker-compose.yml`)  
- Código em `./api` está montado no container; alterações refletem sem rebuild.  
- Dados do MySQL persistem no volume `mysql_data`.

### Frontend (sem Docker)

Com a API rodando (Docker ou local), em outro terminal:

```bash
npm run frontend
# ou: cd front && npm run dev
```

- **Frontend:** http://localhost:5173 (Vite).  
- Em desenvolvimento o front usa proxy para a API (configurado no Vite).

### Tudo junto (API + front)

```bash
npm run dev
```

Sobe a API com Docker e o frontend com Vite no mesmo comando.

## Comandos úteis (API)

```bash
# Criar superusuário (para acessar o admin)
docker-compose run --rm api python manage.py createsuperuser

# Rodar testes
docker-compose run --rm api python manage.py test

# Shell Django
docker-compose run --rm api python manage.py shell
```

## Desenvolvimento local (API sem Docker)

MySQL deve estar rodando na porta 3308 com o banco `bibliotecaquintal` criado. Configure via variáveis de ambiente:

```bash
export DB_HOST=localhost DB_PORT=3308 DB_NAME=bibliotecaquintal DB_USER=root DB_PASSWORD=sua_senha
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd api && python manage.py migrate && python manage.py runserver
```

## Documentação para IA

- **Backend:** `docs/ai/backend-context.md` — modelos, URLs (incl. auth: grupos, permissões, usuários), padrões Django/DRF, IsSuperuser.  
- **Frontend:** `docs/ai/frontend-context.md` — rotas (incl. /configuracao), store (hasPermission, isSuperuser), serviços (configService), botões por permissão, componentes Vue.  
- **Índice:** `docs/ai/README.md` — visão geral dos contextos.
