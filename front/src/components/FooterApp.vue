<template>
  <footer class="footer-app">
    <span class="footer-text">Biblioteca Quintal</span>
  </footer>
</template>

<script>
export default {
  name: 'FooterApp'
}
</script>

<style scoped>
.footer-app {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.75rem 1rem;
  text-align: center;
  background: var(--p-surface-section);
  border-top: 1px solid var(--p-surface-border);
  color: var(--p-text-muted-color);
  font-size: 0.875rem;
}

.footer-text {
  font-weight: 500;
}
</style>
