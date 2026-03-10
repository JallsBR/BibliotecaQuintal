<template>
  <div class="signup-page">
    <Card class="signup-card">
      <template #content>
        <form @submit.prevent="handleSignup">
          <div class="signup-header">
            <h2 class="brand-title">Biblioteca <span>Quintal</span></h2>
            <p class="signup-subtitle">Cadastro</p>
          </div>

          <Message v-if="error" severity="error" :closable="false" class="signup-error">
            {{ error }}
          </Message>

          <div class="field mb-3">
            <label for="username" class="field-label">Usuário</label>
            <InputText
              id="username"
              v-model="username"
              type="text"
              class="w-full"
              placeholder="Nome de usuário"
              required
            />
          </div>

          <div class="field mb-3">
            <label for="email" class="field-label">Email</label>
            <InputText
              id="email"
              v-model="email"
              type="email"
              class="w-full"
              placeholder="seu@email.com"
              required
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
              inputClass="w-full"
              required
            />
          </div>

          <Button
            type="submit"
            :label="loading ? 'Cadastrando...' : 'Cadastrar'"
            class="w-full"
            :loading="loading"
            :disabled="loading"
          />

          <div class="signup-footer">
            <span class="signup-footer-text">Já possui conta? </span>
            <RouterLink to="/signin" class="signup-link">Entrar</RouterLink>
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script>
import api from '@/services/APIService'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { RouterLink } from 'vue-router'

export default {
  name: 'SigupPage',
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
      username: '',
      email: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleSignup() {
      this.error = ''
      this.loading = true
      try {
        await api.post('/auth/signup', {
          username: this.username,
          email: this.email,
          password: this.password
        })
        const success = await this.$store.dispatch('login', {
          email: this.email,
          password: this.password
        })
        if (success) {
          this.$router.push({ name: 'home' })
        }
      } catch (err) {
        if (err.response?.data?.detail) {
          this.error = err.response.data.detail
        } else if (typeof err.response?.data === 'object') {
          const firstError = Object.values(err.response.data)[0]
          this.error = Array.isArray(firstError) ? firstError[0] : firstError
        } else {
          this.error = 'Erro ao cadastrar. Tente novamente.'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background: var(--p-surface-ground);
}

.signup-card {
  width: 100%;
  max-width: 400px;
}

.signup-card :deep(.p-card-content) {
  padding: 0;
}

.signup-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.signup-subtitle {
  margin: 0.25rem 0 0;
  font-size: 1rem;
  color: var(--p-text-muted-color);
}

.signup-error {
  margin-bottom: 1rem;
}

.field-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--p-text-color);
}

.mb-3 {
  margin-bottom: 1rem;
}

.w-full {
  width: 100%;
}

.signup-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.signup-footer-text {
  color: var(--p-text-muted-color);
  font-size: 0.9375rem;
}

.signup-link {
  color: var(--p-primary-color);
  text-decoration: none;
  font-weight: 500;
}

.signup-link:hover {
  text-decoration: underline;
}

.brand-title {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--p-text-color);
  letter-spacing: 0.5px;
  margin: 0;
}

.brand-title span {
  color: var(--p-primary-color);
  font-weight: 700;
}
</style>
