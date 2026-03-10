<template>
  <div class="public-layout">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'PublicLayout'
}
</script>

<style scoped>
.public-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
