<template>
  <div class="auth-user-card">
    <i class="pi pi-user"></i>
    <span class="auth-user-card__name">{{ userName }}</span>
  </div>
</template>

<script>
import { computed } from 'vue'
import store from '../store'

export default {
  name: 'AuthUserCard',
  setup() {
    const userName = computed(() => {
      const user = store.state?.user
      if (user?.nome) return user.nome
      if (user?.username) return user.username
      if (user?.email) return user.email
      return 'Usuário'
    })
    return { userName }
  }
}
</script>

<style scoped>
.auth-user-card {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--azulquintal);
  color: var(--texto-sobre-azul);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.auth-user-card .pi {
  font-size: 1rem;
  flex-shrink: 0;
}

.auth-user-card__name {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
