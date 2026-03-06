# Biblioteca Quintal — Referência do Backend (Django)

Documento de contexto do backend para uso por assistentes de IA e documentação do projeto.

---

## Visão geral

- **Projeto:** Biblioteca Quintal  
- **Backend:** Django (API REST)  
- **Raiz do backend:** `api/`  
- **App de configuração:** `api/app/` (settings, urls, wsgi)  
- **Autenticação:** JWT (Simple JWT)  
- **Idioma:** pt-br | **Fuso:** America/Sao_Paulo  

---

## Estrutura de pastas (API)

```
api/
├── app/                 # Configuração do projeto (settings, urls, wsgi)
├── users/               # Autenticação e usuários do sistema
├── livros/              # Catálogo: categorias, autores, editoras, livros
├── leitor/              # Leitores, recompensas, empréstimos, reservas
├── manage.py
├── db.sqlite3
└── media/               # Uploads (ex.: imagens de livros)
```

---

## Apps e responsabilidades

| App     | Responsabilidade |
|--------|-------------------|
| **users** | Usuários do sistema (AbstractUser), login, signup, refresh token, logout |
| **livros** | Categoria, Autor, Editora, Livro (catálogo da biblioteca) |
| **leitor** | Recompensa, Leitor, Emprestimo, Reserva (gestão de leitores e empréstimos) |

---

## URLs da API (v1)

Base: `/api/v1/`

| Prefixo        | Inclui (app) | Rotas |
|----------------|--------------|--------|
| `api/v1/auth/` | users        | signin, signup, token/refresh/, user, logout |
| `api/v1/livros/` | livros     | categorias/, autores/, editoras/, livros/ (cada um com list-create e retrieve-update-destroy por `<int:pk>`) |
| `api/v1/leitor/` | leitor     | recompensas/, leitores/, emprestimos/, reservas/ (mesmo padrão) |

- **Admin:** `/admin/`  
- **Media:** conforme `MEDIA_URL` (ex.: `/media/`)

---

## Modelos de dados

### users

- **User** (AbstractUser): `email` (unique), herda username, password, etc.  
  - `AUTH_USER_MODEL = 'users.User'`

### livros

- **Categoria:** nome, created_at, updated_at  
- **Autor:** nome, created_at, updated_at  
- **Editora:** nome, created_at, updated_at  
- **Livro:** titulo, descricao, pontuacao, qtd_paginas, ano_publicacao, qtd_disponivel, qtd_emprestados, is_disponivel, idioma, isbn, ativo, imagem (ImageField), FK autor, editora, categoria, created_at, updated_at  
  - Regras: `clean()` para qtd/ano/páginas; `save()` atualiza `is_disponivel` (qtd_disponivel vs qtd_emprestados)

### leitor

- **Recompensa:** nome, descricao, pontuacao, created_at, updated_at, created_by (FK User), ativo  
- **Leitor:** nome, livros_lidos (M2M Livro), recompensas (M2M Recompensa), pontuacao_atual, pontuacao_total, email (unique), data_nascimento, sexo, profissao, telefone, endereco, cidade, estado, pais, cep, numero, complemento, bairro, cpf (unique, opcional), created_at, updated_at, ativo, created_by (FK User)  
- **Emprestimo:** leitor (FK), livro (FK), data_emprestimo, data_devolucao, created_at, updated_at, created_by, ativo  
  - `clean()`: livro deve estar disponível; datas coerentes (empréstimo/devolução e não no passado)  
- **Reserva:** leitor (FK), livro (FK), data_reserva, data_expiracao, created_at, updated_at, created_by, ativo  
  - `clean()`: data_reserva e data_expiracao coerentes e não no passado  

---

## Padrão de views (DRF)

- **Um arquivo por modelo** em `app/views/` (ex.: `livros/views/autor.py`, `leitor/views/emprestimo.py`).  
- Para cada recurso:
  - **ListCreate:** `{Modelo}ListCreateView` (generics.ListCreateAPIView)  
  - **Detalhe/edição/remoção:** `{Modelo}RetrieveUpdateDestroyView` (generics.RetrieveUpdateDestroyAPIView)  
- **Permissão:** `IsAuthenticated` em todas as views de livros e leitor.  
- **Filtros/ordenação:** `DjangoFilterBackend` + `OrderingFilter`; `filterset_fields` e `ordering_fields`/`ordering` por view.  
- **Delete:** método `destroy()` sobrescrito retornando mensagem de sucesso em português (ex.: "Autor removido com sucesso.").  
- **Queryset:** `get_queryset()` retornando `Modelo.objects.all()`; `get_object()` com `get_object_or_404(queryset, pk=self.kwargs["pk"])`.

---

## Serializers

- Um serializer por modelo (ex.: `AutorSerializer`, `EmprestimoSerializer`).  
- Uso típico: `fields = '__all__'`, `read_only_fields = ['created_at', 'updated_at']` quando fizer sentido.

---

## Configurações relevantes (settings)

- **INSTALLED_APPS:** jazzmin, django apps, rest_framework, corsheaders, rest_framework_simplejwt, users, livros, leitor  
- **REST_FRAMEWORK:** JWT auth, IsAuthenticated default, DjangoFilterBackend, PageNumberPagination (PAGE_SIZE=10)  
- **CORS:** CORS_ALLOW_ALL_ORIGINS = True; CORS_ALLOWED_ORIGINS inclui localhost:5173 (Vue).  
- **SIMPLE_JWT:** ACCESS_TOKEN_LIFETIME 5 min, REFRESH_TOKEN_LIFETIME 1 dia.  
- **Database:** SQLite (db.sqlite3).  
- **MEDIA:** MEDIA_ROOT, MEDIA_URL em uso para uploads (ex.: imagens de livros).

---

## Convenções para manter

1. **apps.py:** apenas `AppConfig` (name do app). Não importar models em `apps.py`; registro de admin em `admin.py`.  
2. **Views:** um módulo por modelo em `views/`, exportar no `views/__init__.py` e referenciar em `urls.py` como `views.NomeDaView`.  
3. **URLs:** list-create em `recurso/`, retrieve-update-destroy em `recurso/<int:pk>/`.  
4. **Mensagens e validações:** em português (incluindo `ValidationError` e respostas de destroy).  
5. **Nomes de apps:** `users`, `livros`, `leitor` (minúsculo, singular para livros/leitor).

---

## Dependências principais

- Django  
- djangorestframework  
- djangorestframework-simplejwt  
- django-cors-headers  
- django-filter  
- Pillow (para ImageField em Livro)  
- jazzmin (admin theme)

---

*Última atualização: referência ao estado do backend Biblioteca Quintal (Django).*
