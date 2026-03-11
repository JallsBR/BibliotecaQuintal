<template>
  <div class="home-page">
    <h1 class="home-title">Biblioteca Quintal</h1>
    <p class="home-subtitle">Bem-vindo ao sistema.</p>
    <RouterLink to="/logout" class="p-button p-button-outlined">Sair</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.home-page {
  padding: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.home-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--texto-primario);
  margin: 0 0 0.5rem;
}

.home-subtitle {
  color: var(--texto-secundario);
  margin: 0 0 1.5rem;
}
</style>
