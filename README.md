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
- **MySQL:** porta 3308, banco `bibliotecaquintal` (credenciais em `docker-compose.yml`)  
- O código em `./api` está montado no container; alterações refletem sem rebuild.  
- Dados do MySQL persistem no volume `mysql_data`.

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

MySQL deve estar rodando na porta 3308 com o banco `bibliotecaquintal` criado. Configure via variáveis de ambiente:

```bash
export DB_HOST=localhost DB_PORT=3308 DB_NAME=bibliotecaquintal DB_USER=root DB_PASSWORD=sua_senha
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd api && python manage.py migrate && python manage.py runserver
```