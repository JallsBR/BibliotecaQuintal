# Biblioteca Quintal — Referência do Frontend (Vue 3)

Documento de contexto do frontend para uso por assistentes de IA e documentação do projeto.

---

## Visão geral

- **Projeto:** Biblioteca Quintal (frontend)  
- **Stack:** Vue 3 (Composition API / `<script setup>`), Vite 7, Vue Router 4, Vuex 4, PrimeVue 4, Axios  
- **Raiz do frontend:** `front/`  
- **Idioma da UI:** pt-br  
- **API:** Django REST em `http://localhost:8000`; em dev o Vite pode usar proxy para `/api/v1`.

---

## Estrutura de pastas (front)

```
front/
├── src/
│   ├── assets/           # theme-global.css, logos
│   ├── components/       # BaseDataTable, BaseSelect, BaseConfirmDialog, NavBar, FooterApp, AuthUserCard
│   ├── constants/       # pagination.js
│   ├── layouts/         # AuthLayout.vue (app autenticada), PublicLayout.vue (signin/signup)
│   ├── pages/           # Uma pasta por módulo: home, livros, leitores, emprestimos, reservas, recompensas, auth
│   ├── router/          # index.js — rotas e beforeEach (requiresAuth)
│   ├── services/        # APIService.js, livroService.js, leitorService.js
│   ├── store/           # index.js — Vuex (user, token, login, logout)
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── index.html
├── package.json
└── vite.config.js
```

---

## Rotas (router/index.js)

- **Públicas (PublicLayout):** `/signin` (signin), `/signup` (signup).  
- **Logout:** `/logout` — componente que despacha logout e redireciona.  
- **Autenticadas (AuthLayout, meta requiresAuth):** `/` (home), `/livros`, `/leitores`, `/emprestimos`, `/reservas`, `/recompensas`.  
- **Guard:** `beforeEach` — se `requiresAuth` e não autenticado → `{ name: 'signin' }`; se já autenticado e rota signin/signup → `{ name: 'home' }`.

---

## Store (Vuex)

- **State:** `user`, `token`, `loading`. Persistência em `localStorage` (`user`, `access`, `refresh`).  
- **Getters:** `isAuthenticated`, `getUser`, `isLoading`.  
- **Actions:** `login({ email, password })` (POST `/auth/signin`, commit SET_AUTH), `logout` (commit LOGOUT e `window.location.href = '/signin'`).  
- **Mutations:** SET_LOADING, SET_AUTH (user + access + refresh no state e localStorage), LOGOUT (limpa state e localStorage).

---

## Serviços de API

- **APIService.js:** instância Axios com `baseURL` = `/api/v1` em dev ou `http://127.0.0.1:8000/api/v1`. Interceptor de request adiciona `Authorization: Bearer <access>`. Interceptor de response: em 401 tenta refresh com POST `/auth/token/refresh/`; se falhar chama `handleLogout` (commit LOGOUT + push signin).  
- **livroService.js / leitorService.js:** funções que usam `api` (APIService) para CRUD de livros, categorias, autores, editoras, leitores, empréstimos, reservas, recompensas (conforme endpoints do backend).  
- **Paginação:** constante em `constants/pagination.js`; listagens usam parâmetros de query da API (page, page_size ou equivalente).

---

## Páginas e módulos

| Rota        | Página principal      | Observação |
|------------|------------------------|------------|
| `/`        | home/index.vue         | Dashboard / início |
| `/livros`  | livros/index.vue       | Listagem + LivroDialog (criar/editar) |
| `/leitores`| leitores/index.vue     | Listagem + LeitorDialog |
| `/emprestimos` | emprestimos/index.vue | Listagem + EmprestimoDialog |
| `/reservas`| reservas/index.vue     | Listagem + ReservaDialog |
| `/recompensas` | recompensas/index.vue | Listagem (recompensas) |
| `/signin`  | auth/SiginPage.vue     | Login |
| `/signup`  | auth/SigupPage.vue     | Cadastro de usuário |

- Diálogos de criação/edição (ex.: LivroDialog, LeitorDialog) usam PrimeVue (Dialog, inputs, botões) e chamam os serviços correspondentes; mensagens e labels em pt-br.

---

## Componentes compartilhados

- **BaseDataTable:** tabela PrimeVue (DataTable) reutilizável com paginação e ações.  
- **BaseSelect:** select (dropdown) reutilizável.  
- **BaseConfirmDialog:** diálogo de confirmação (ex.: exclusão).  
- **NavBar:** menu da aplicação autenticada (links para home, livros, leitores, etc.; usuário e logout).  
- **FooterApp:** rodapé.  
- **AuthUserCard:** exibição do usuário logado (ex.: no layout).

---

## Convenções para manter

1. **Idioma:** textos da interface, placeholders, mensagens de erro e sucesso em português (pt-br).  
2. **API:** usar sempre o cliente `api` (APIService) para chamadas HTTP; não criar novas instâncias Axios para a mesma baseURL.  
3. **Auth:** rotas que exigem login devem ter `meta: { requiresAuth: true }` e estar sob o layout que usa o guard.  
4. **Formulários:** validação e feedback em pt-br; uso de PrimeVue para inputs e botões.  
5. **Nomenclatura:** páginas em `pages/<modulo>/index.vue` ou `pages/<modulo>/NomeDialog.vue`; serviços em `services/<modulo>Service.js`.

---

## Dependências principais (front)

- vue, vue-router, vuex  
- vite, @vitejs/plugin-vue  
- primevue, primeicons, @primevue/themes  
- axios  

---

## Documentação relacionada

- **README do projeto:** `README.md` (raiz) — como subir API e front.  
- **Contexto do backend:** `docs/ai/backend-context.md` — Django, modelos, URLs da API.
