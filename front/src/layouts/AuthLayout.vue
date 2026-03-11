<template>
  <div class="auth-layout">
    <NavBar />
    <div class="auth-main">
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

export default {
  name: 'AuthLayout',
  components: {
    FooterApp,
    NavBar,
    AuthUserCard
  }
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
}

.auth-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 100vh;
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
}
</style>