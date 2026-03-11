<template>
  <div class="auth-page">
    <Card class="auth-card" style="width: 650px;">
      <template #content>
        <form @submit.prevent="handleLogin">
          <div class="auth-header">
            <img src="/logoHAzul.png" alt="Logo" class="auth-logo" />
          </div>

          <Message v-if="error" severity="error" :closable="false" class="auth-error">
            Credenciais não encontradas. Tente novamente.
          </Message>

          <div class="field mb-3">
            <label for="email" class="field-label">Email</label>
            <InputText
              id="email"
              v-model="email"
              type="email"
              class="w-full"
              placeholder="seu@email.com"
              autocomplete="email"
            />
          </div>

          <div class="field mb-3">
            <label for="password" class="field-label">Senha</label>
            <Password
              id="password"
              v-model="password"
              class="w-full"
              placeholder="Sua senha"
              :feedback="false"
              toggleMask
              fluid
              inputClass="w-full"
            />
          </div>

          <Button
            type="submit"
            :label="loading ? 'Entrando...' : 'Entrar'"
            class="w-full"
            :loading="loading"
            :disabled="loading"
          />

          <div class="auth-footer">
            <span class="auth-footer-text">Não tem cadastro? </span>
            <RouterLink to="/signup" class="auth-link">Registre-se</RouterLink>
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script>
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { RouterLink } from 'vue-router'
export default {
  name: 'SignInPage',
  components: {
    Card,
    InputText,
    Password,
    Button,
    Message,
    RouterLink
  },
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },

  computed: {
    loading() {
      return this.$store.getters.isLoading
    }
  },

  methods: {
    async handleLogin() {
      this.error = null
      const success = await this.$store.dispatch('login', {
        email: this.email,
        password: this.password
      })

      if (success) {
        this.$router.push({ name: 'home' })
      } else {
        this.error = true
        this.$toast.add({
          severity: 'error',
          summary: 'Erro ao entrar',
          detail: 'Credenciais não encontradas. Tente novamente.',
          life: 5000
        })
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background: var(--bg-primario);
}

.auth-card {
  width: 100%;
  max-width: 400px;
}

.auth-card :deep(.p-card-content) {
  padding: 0;
}

.auth-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.auth-logo {
  width: 100%;
  max-width: 200px;
  display: block;
  margin: 0 auto;
  object-fit: contain;
  padding: 1rem 0;
}

.auth-error {
  margin-bottom: 1rem;
}

.field-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--texto-primario);
}

.mb-3 {
  margin-bottom: 1rem;
}

.w-full {
  width: 100%;
}

.auth-card :deep(.p-password) {
  width: 100%;
}
.auth-card :deep(.p-password .p-password-input),
.auth-card :deep(.p-password .p-inputtext) {
  flex: 1 1 auto;
  min-width: 0;
}

.auth-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.auth-footer-text {
  color: var(--texto-secundario);
  font-size: 0.9375rem;
}

.auth-link {
  color: var(--sucesso);
  text-decoration: none;
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
