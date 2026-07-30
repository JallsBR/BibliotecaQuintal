<template>
  <div class="navbar-shell">
    <div v-if="menuAberto" class="navbar-overlay" @click="fecharMenu"></div>

    <aside id="navbar-menu" class="navbar" :class="{ 'navbar--aberto': menuAberto }">
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
        <router-link v-if="hasPermission('livros.view_livro')" to="/livros" class="nav-link" active-class="nav-link--active">
          <i class="pi pi-book"></i>
          <span>Livros</span>
        </router-link>
        <router-link to="/acervo" class="nav-link" active-class="nav-link--active">
          <i class="pi pi-images"></i>
          <span>Acervo</span>
        </router-link>
        <router-link to="/recompensas" class="nav-link" active-class="nav-link--active">
          <i class="pi pi-gift"></i>
          <span>Recompensas</span>
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
        <router-link
          v-if="isSuperuser"
          to="/configuracao"
          class="nav-link"
          active-class="nav-link--active"
        >
          <i class="pi pi-cog"></i>
          <span>Configuração</span>
        </router-link>
      </nav>

      <div class="navbar-separator" role="separator"></div>

      <div class="navbar-user">
        <div class="navbar-user-actions">
          <Button label="Logout" severity="danger" size="small" class="navbar-logout-btn" @click="logout" />
          <button type="button" class="navbar-theme-btn" :aria-label="temaAtual === 'escuro' ? 'Tema claro' : 'Tema escuro'" @click="alternarTema">
            <i class="pi" :class="temaAtual === 'escuro' ? 'pi-sun' : 'pi-moon'"></i>
          </button>
        </div>
      </div>
    </aside>

    <button
      type="button"
      class="navbar-fab"
      :aria-label="menuAberto ? 'Fechar menu' : 'Abrir menu'"
      :aria-expanded="menuAberto"
      aria-controls="navbar-menu"
      @click="alternarMenu"
    >
      <i v-if="menuAberto" class="pi pi-times"></i>
      <img v-else :src="logoNavBar" alt="" class="navbar-fab-logo" />
    </button>
  </div>
</template>

<script>
import { computed, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import store from '../store'
import Button from 'primevue/button'
import { useTema } from '@/composables/useTema'

// Precisa acompanhar o breakpoint do CSS deste componente e do AuthLayout
const MOBILE_QUERY = '(max-width: 900px)'

export default {
  name: 'NavBar',
  components: { Button },
  setup() {
    const { tema: temaAtual, logo: logoNavBar, alternarTema } = useTema()
    const menuAberto = ref(false)
    const route = useRoute()

    let mediaQuery = null

    function aoMudarViewport(evento) {
      if (!evento.matches) {
        menuAberto.value = false
      }
    }

    function aoPressionarTecla(evento) {
      if (evento.key === 'Escape') {
        menuAberto.value = false
      }
    }

    onMounted(() => {
      mediaQuery = window.matchMedia(MOBILE_QUERY)
      mediaQuery.addEventListener('change', aoMudarViewport)
      window.addEventListener('keydown', aoPressionarTecla)
    })

    onBeforeUnmount(() => {
      mediaQuery?.removeEventListener('change', aoMudarViewport)
      window.removeEventListener('keydown', aoPressionarTecla)
    })

    watch(() => route.fullPath, () => {
      menuAberto.value = false
    })

    function alternarMenu() {
      menuAberto.value = !menuAberto.value
    }

    function fecharMenu() {
      menuAberto.value = false
    }

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

    const isSuperuser = computed(() => store.getters.isSuperuser)
    const hasPermission = (perm) => store.getters.hasPermission(perm)

    return {
      userName,
      logout,
      temaAtual,
      alternarTema,
      logoNavBar,
      isSuperuser,
      hasPermission,
      menuAberto,
      alternarMenu,
      fecharMenu
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 260px;
  min-width: 260px;
  background: var(--azulquintal);
  display: flex;
  flex-direction: column;
  z-index: 100;
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
  max-height: 152px;
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

.navbar-overlay {
  display: none;
}

.navbar-fab {
  display: none;
}

@media (max-width: 900px) {
  .navbar {
    width: 80vw;
    max-width: 300px;
    min-width: 0;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }

  .navbar--aberto {
    transform: translateX(0);
    box-shadow: 0 0 24px rgba(0, 0, 0, 0.35);
  }

  .navbar-logo {
    max-height: 104px;
  }

  .navbar-links {
    overflow-y: auto;
  }

  .navbar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 90;
    /* evita arrastar o conteúdo por trás do drawer */
    touch-action: none;
  }

  .navbar-fab {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    right: 1rem;
    bottom: max(1rem, env(safe-area-inset-bottom, 1rem));
    width: 3.5rem;
    height: 3.5rem;
    padding: 0.4rem;
    border: none;
    border-radius: 50%;
    background: var(--azulquintal);
    color: var(--texto-sobre-azul);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    z-index: 110;
    transition: transform 0.2s;
  }

  .navbar-fab:active {
    transform: scale(0.94);
  }

  .navbar-fab-logo {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .navbar-fab .pi {
    font-size: 1.4rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .navbar,
  .navbar-fab {
    transition: none;
  }
}
</style>
