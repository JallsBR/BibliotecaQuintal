# Biblioteca Quintal — Frontend

Frontend do sistema Biblioteca Quintal: **Vue 3**, **Vite**, **PrimeVue**, **Vuex**, **Vue Router**. Comunica com a API Django em `http://localhost:8000` (dev com proxy).

Documentação de contexto para IA: `docs/ai/frontend-context.md` (na raiz do repositório).

## Stack

- Vue 3 (Composition API / `<script setup>`)
- Vite 7
- Vue Router 4
- Vuex 4
- PrimeVue 4 + PrimeIcons
- Axios (API com interceptors e refresh JWT)

## Desenvolvimento

```bash
npm install
npm run dev
```

- App: http://localhost:5173  
- Em `DEV` o front usa proxy para `/api/v1` (API na mesma máquina).

## Scripts

- `npm run dev` — servidor de desenvolvimento (Vite)
- `npm run build` — build de produção
- `npm run preview` — preview do build

## Estrutura principal

- `src/router/index.js` — rotas e guard de autenticação
- `src/store/index.js` — Vuex (auth: user, token, login/logout)
- `src/services/APIService.js` — cliente Axios, baseURL, interceptors (Bearer + refresh)
- `src/services/livroService.js`, `leitorService.js` — chamadas à API por domínio
- `src/pages/` — páginas: home, livros, leitores, empréstimos, reservas, recompensas, auth (signin/signup/logout)
- `src/layouts/` — AuthLayout (app autenticada), PublicLayout (login/signup)
- `src/components/` — NavBar, FooterApp, BaseDataTable, BaseSelect, BaseConfirmDialog, AuthUserCard

## Autenticação

- Login em `/signin`; rotas em `/` exigem autenticação (meta `requiresAuth`).
- Token JWT em `localStorage` (access + refresh); refresh automático no interceptor em 401.
- Logout limpa store e localStorage e redireciona para `/signin`.
