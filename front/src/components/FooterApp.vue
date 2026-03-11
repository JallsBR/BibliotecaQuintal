<template>
  <footer class="footer-app">
    <span class="footer-text">Biblioteca Quintal - Todos os direitos reservados - 2026 - O5o software house</span>
  </footer>
</template>

<script>
export default {
  name: 'FooterApp'
}
</script>

<style scoped>
.footer-app {
  padding: 0.75rem 1rem;
  margin-top: auto;
  text-align: center;
  background: var(--bg-primario);
  border-top: 1px solid color-mix(in srgb, var(--texto-secundario) 25%, transparent);
  color: var(--texto-secundario);
  font-size: 0.875rem;
}

.footer-text {
  font-weight: 500;
}
</style>
