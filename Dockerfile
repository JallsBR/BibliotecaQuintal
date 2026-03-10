# Imagem base Python para desenvolvimento
FROM python:3.12-slim

# Evita criação de arquivos .pyc e buffering no stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema (necessárias para Pillow e possíveis libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

WORKDIR /app/api

# Porta do runserver
EXPOSE 8000

# Comando padrão: migrations + servidor (útil no primeiro run)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
