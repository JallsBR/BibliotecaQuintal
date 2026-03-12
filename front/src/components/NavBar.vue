<template>
  <aside class="navbar">
    <div class="navbar-header">
      <router-link to="/" class="navbar-logo-link">
        <img :src="logoNavBar" alt="Biblioteca Quintal" class="navbar-logo" />
      </router-link>
    </div>

    <nav class="navbar-links">
      <router-link to="/" class="nav-link" exact-active-class="nav-link--active">
        <i class="pi pi-home"></i>
        <span>Início</span>
      </router-link>
      <router-link to="/livros" class="nav-link" active-class="nav-link--active">
        <i class="pi pi-book"></i>
        <span>Livros</span>
      </router-link>
      <router-link to="/leitores" class="nav-link" active-class="nav-link--active">
        <i class="pi pi-user"></i>
        <span>Leitores</span>
      </router-link>
      <router-link to="/emprestimos" class="nav-link" active-class="nav-link--active">
        <i class="pi pi-arrow-right"></i>
        <span>Empréstimos</span>
      </router-link>
      <router-link to="/reservas" class="nav-link" active-class="nav-link--active">
        <i class="pi pi-clock"></i>
        <span>Reservas</span>
      </router-link>
      <router-link to="/recompensas" class="nav-link" active-class="nav-link--active">
        <i class="pi pi-gift"></i>
        <span>Recompensas</span>
      </router-link>
    </nav>

    <div class="navbar-separator" role="separator"></div>

    <div class="navbar-user">
      <div class="navbar-user-actions">
        <Button label="Logout" severity="danger" size="small" class="navbar-logout-btn" @click="logout" />
        <button type="button" class="navbar-theme-btn" :aria-label="temaAtual === 'escuro' ? 'Tema claro' : 'Tema escuro'" @click="toggleTema">
          <i class="pi" :class="temaAtual === 'escuro' ? 'pi-sun' : 'pi-moon'"></i>
        </button>
      </div>
    </div>
  </aside>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import store from '../store'
import Button from 'primevue/button'

const TEMA_KEY = 'tema'

export default {
  name: 'NavBar',
  components: { Button },
  setup() {
    const temaAtual = ref('claro')

    onMounted(() => {
      temaAtual.value = document.documentElement.getAttribute('data-tema') || 'claro'
    })

    const logoNavBar = computed(() =>
      temaAtual.value === 'escuro' ? '/logoHAmarelo.png' : '/logoHAzul.png'
    )

    const userName = computed(() => {
      const user = store.state?.user
      if (user?.nome) return user.nome
      if (user?.username) return user.username
      if (user?.email) return user.email
      return 'Usuário'
    })

    function logout() {
      store.dispatch('logout')
    }

    function toggleTema() {
      const proximo = temaAtual.value === 'escuro' ? 'claro' : 'escuro'
      document.documentElement.setAttribute('data-tema', proximo)
      localStorage.setItem(TEMA_KEY, proximo)
      temaAtual.value = proximo
    }

    return { userName, logout, temaAtual, toggleTema, logoNavBar }
  }
}
</script>

<style scoped>
.navbar {
  width: 260px;
  min-width: 260px;
  height: 100vh;
  background: var(--azulquintal);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.navbar-header {
  padding: 1.25rem 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-logo-link {
  display: block;
  line-height: 0;
}

.navbar-logo {
  max-width: 100%;
  max-height: 76px;
  object-fit: contain;
}

.navbar-links {
  flex: 1;
  padding: 0.75rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  margin: 0 0.5rem;
  color: var(--texto-sobre-azul);
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background: color-mix(in srgb, var(--texto-sobre-azul) 15%, transparent);
}

.nav-link--active {
  background: color-mix(in srgb, var(--texto-sobre-azul) 20%, transparent);
}

.nav-link .pi {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.navbar-separator {
  height: 1px;
  background: color-mix(in srgb, var(--texto-sobre-azul) 30%, transparent);
  margin: 0 1rem;
}

.navbar-user {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 1rem 1.25rem;
  color: var(--texto-sobre-azul);
  font-size: 0.9rem;
}

.navbar-user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-user-info .pi {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.navbar-user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.navbar-user-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-user :deep(.navbar-logout-btn.p-button) {
  flex: 1;
  background: var(--perigo) !important;
  border-color: var(--perigo) !important;
}

.navbar-user :deep(.navbar-logout-btn.p-button:hover) {
  background: color-mix(in srgb, var(--perigo) 85%, black) !important;
  border-color: color-mix(in srgb, var(--perigo) 85%, black) !important;
}

.navbar-theme-btn {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
  border-radius: 6px;
  background: color-mix(in srgb, var(--texto-sobre-azul) 20%, transparent);
  color: var(--texto-sobre-azul);
  cursor: pointer;
  flex-shrink: 0;
  transition: background-color 0.2s;
}

.navbar-theme-btn:hover {
  background: color-mix(in srgb, var(--texto-sobre-azul) 30%, transparent);
}

.navbar-theme-btn .pi {
  font-size: 1.1rem;
}
</style>
