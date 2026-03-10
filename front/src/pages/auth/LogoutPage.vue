<template>
  <div class="logout-page">Saindo...</div>
</template>

<script>
export default {
  name: 'LogoutPage',
  mounted() {
    this.$store.dispatch('logout')
  }
}
</script>

<style scoped>
.logout-page {
  padding: 2rem;
  text-align: center;
  color: var(--p-text-muted-color);
}
</style>