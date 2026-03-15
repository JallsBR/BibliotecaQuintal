# Contexto de IA — Biblioteca Quintal

Esta pasta contém documentos de contexto para assistentes de IA (por ex. Cursor, Copilot) que trabalham no repositório **Biblioteca Quintal**.

Use estes arquivos como referência ao implementar ou alterar código no backend ou no frontend.

## Documentos

| Arquivo | Uso |
|--------|-----|
| **backend-context.md** | Backend Django: estrutura `api/`, apps (users, livros, leitor), modelos, URLs da API v1 (incl. auth: grupos, permissões, usuários para superuser), padrões de views/serializers, permissões (IsSuperuser), convenções. |
| **frontend-context.md** | Frontend Vue: estrutura `front/src/`, rotas (incl. /configuracao), store (Vuex, hasPermission, isSuperuser), serviços (APIService, livroService, leitorService, configService), páginas (incl. Configuração), botões por permissão, convenções (pt-br). |

## Quando usar

- **Alterar ou estender a API** → ler `backend-context.md` para manter padrões (views por modelo, serializers, IsSuperuser para config, mensagens em pt-br, etc.).  
- **Alterar ou estender o frontend** → ler `frontend-context.md` para rotas (incl. guard superuser), auth, hasPermission, serviços (configService) e componentes compartilhados.  
- **Integrar front com API** → cruzar endpoints em `backend-context.md` com chamadas em `frontend-context.md` e em `front/src/services/` (incl. `configService.js` para grupos/permissoes/usuários).

## README do projeto

Na raiz do repositório, o `README.md` descreve como subir o projeto (Docker, frontend, comandos úteis) e aponta para esta pasta.
