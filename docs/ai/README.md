# Contexto de IA — Biblioteca Quintal

Esta pasta contém documentos de contexto para assistentes de IA (por ex. Cursor, Copilot) que trabalham no repositório **Biblioteca Quintal**.

Use estes arquivos como referência ao implementar ou alterar código no backend ou no frontend.

## Documentos

| Arquivo | Uso |
|--------|-----|
| **backend-context.md** | Backend Django: estrutura `api/`, apps (users, livros, leitor), modelos, URLs da API v1, padrões de views/serializers, configurações (JWT, CORS, DB MySQL), convenções. |
| **frontend-context.md** | Frontend Vue: estrutura `front/src/`, rotas, store (Vuex), serviços (APIService, livroService, leitorService), páginas e componentes, convenções (pt-br, uso da API). |

## Quando usar

- **Alterar ou estender a API** → ler `backend-context.md` para manter padrões (views por modelo, serializers, mensagens em pt-br, etc.).  
- **Alterar ou estender o frontend** → ler `frontend-context.md` para rotas, auth, serviços e componentes compartilhados.  
- **Integrar front com API** → cruzar endpoints em `backend-context.md` com chamadas em `frontend-context.md` e em `front/src/services/`.

## README do projeto

Na raiz do repositório, o `README.md` descreve como subir o projeto (Docker, frontend, comandos úteis) e aponta para esta pasta.
