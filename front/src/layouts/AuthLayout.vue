<template>
  <div class="auth-layout">
    <NavBar />
    <div class="auth-main">
      <header class="mobile-topbar">
        <img :src="logoTopbar" alt="Biblioteca Quintal" class="mobile-topbar__logo" />
        <AuthUserCard />
      </header>
      <header class="auth-header">
        <AuthUserCard />
      </header>
      <div class="container mt-4 auth-content">
        <router-view />
      </div>
      <FooterApp />
    </div>
  </div>
</template>

<script>
import FooterApp from '../components/FooterApp.vue'
import NavBar from '../components/NavBar.vue'
import AuthUserCard from '../components/AuthUserCard.vue'
import { useTema } from '@/composables/useTema'

export default {
  name: 'AuthLayout',
  components: {
    FooterApp,
    NavBar,
    AuthUserCard
  },
  setup() {
    const { logo: logoTopbar } = useTema()
    return { logoTopbar }
  }
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
}

.auth-main {
  margin-left: 260px;
  min-height: 100vh;
  height: 100vh;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

.auth-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0.75rem 1rem;
  flex-shrink: 0;
}

.auth-content {
  padding-bottom: 1rem;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.mobile-topbar {
  display: none;
}

/* Breakpoint espelhado em NavBar.vue: abaixo dele o menu vira drawer */
@media (max-width: 900px) {
  .auth-main {
    margin-left: 0;
  }

  .mobile-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.5rem 0.875rem;
    background: var(--azulquintal);
    flex-shrink: 0;
  }

  .mobile-topbar__logo {
    height: 44px;
    max-width: 60%;
    object-fit: contain;
    object-position: left center;
  }

  .mobile-topbar :deep(.auth-user-card) {
    background: color-mix(in srgb, var(--texto-sobre-azul) 18%, transparent);
    box-shadow: none;
  }

  .auth-header {
    display: none;
  }

  .auth-content {
    /* espaço para o botão flutuante do menu não cobrir o conteúdo */
    padding-bottom: 5.5rem;
  }
}
</style>