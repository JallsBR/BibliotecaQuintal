# Biblioteca Quintal

API Django (REST) para gestão da biblioteca. Documentação do backend em `docs/ai/backend-context.md`.

## Desenvolvimento com Docker

Requisitos: Docker e Docker Compose (`docker-compose` ou `docker compose`).

```bash
# Subir a API (migrations rodam automaticamente)
docker-compose up --build
# ou: docker compose up --build
```

- **API:** http://localhost:8000  
- **Admin:** http://localhost:8000/admin/  
- O código em `./api` está montado no container; alterações refletem sem rebuild.  
- O banco SQLite fica em `api/db.sqlite3` no host (persiste entre subidas).

Comandos úteis:

```bash
# Criar superusuário (para acessar o admin)
docker-compose run --rm api python manage.py createsuperuser

# Rodar testes
docker-compose run --rm api python manage.py test

# Shell Django
docker-compose run --rm api python manage.py shell
```

## Desenvolvimento local (sem Docker)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd api && python manage.py migrate && python manage.py runserver
```