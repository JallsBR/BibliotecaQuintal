<template>
  <div class="auth-page">
    <Card class="auth-card" style="width: 650px;">
      <template #content>
        <form @submit.prevent="handleSignup">
          <div class="auth-header">
            <img src="/logoHAzul.png" alt="Logo" class="auth-logo" />
          </div>

          <Message v-if="error" severity="error" :closable="false" class="auth-error">
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
              fluid
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

          <div class="auth-footer">
            <span class="auth-footer-text">Já possui conta? </span>
            <RouterLink to="/signin" class="auth-link">Entrar</RouterLink>
          </div>
        </form>
      </template>
    </Card>

    <Dialog
      v-model:visible="loading"
      modal
      :closable="false"
      :closeOnEscape="false"
      class="auth-loading-dialog"
    >
      <template #header>
        <span class="auth-loading-title">Configurando novo usuário</span>
      </template>
      <div class="auth-loading-content">
        <ProgressBar :value="progresso" :showValue="true" />
      </div>
    </Dialog>
  </div>
</template>

<script>
import api from '@/services/APIService'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'
import Dialog from 'primevue/dialog'
import ProgressBar from 'primevue/progressbar'
import { RouterLink } from 'vue-router'

const PROGRESSO_MAX_ANTES = 85
const PROGRESSO_INTERVALO_MS = 150
const PROGRESSO_INCREMENTO = 2

export default {
  name: 'SignUpPage',
  components: {
    Card,
    InputText,
    Password,
    Button,
    Message,
    Dialog,
    ProgressBar,
    RouterLink
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: '',
      loading: false,
      progresso: 0,
      progressoTimer: null
    }
  },
  methods: {
    iniciarProgresso() {
      this.progresso = 0
      this.progressoTimer = setInterval(() => {
        if (this.progresso < PROGRESSO_MAX_ANTES) {
          this.progresso = Math.min(this.progresso + PROGRESSO_INCREMENTO, PROGRESSO_MAX_ANTES)
        }
      }, PROGRESSO_INTERVALO_MS)
    },
    pararProgresso() {
      if (this.progressoTimer) {
        clearInterval(this.progressoTimer)
        this.progressoTimer = null
      }
    },
    async handleSignup() {
      this.error = ''
      this.loading = true
      this.iniciarProgresso()

      try {
        await api.post('/auth/signup', {
          username: this.username,
          email: this.email,
          password: this.password
        })

        this.progresso = 90
        const success = await this.$store.dispatch('login', {
          email: this.email,
          password: this.password
        })

        this.progresso = 100
        this.pararProgresso()
        await new Promise(r => setTimeout(r, 400))

        if (success) {
          this.loading = false
          this.$router.push({ name: 'home' })
        } else {
          this.loading = false
        }
      } catch (err) {
        this.pararProgresso()
        this.loading = false
        if (err.response?.data?.detail) {
          this.error = err.response.data.detail
        } else if (typeof err.response?.data === 'object') {
          const firstError = Object.values(err.response.data)[0]
          this.error = Array.isArray(firstError) ? firstError[0] : firstError
        } else {
          this.error = 'Ocorreu um erro inesperado. Tente novamente.'
        }
        this.$toast.add({
          severity: 'error',
          summary: 'Erro no cadastro',
          detail: this.error,
          life: 6000
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

.auth-loading-dialog :deep(.p-dialog-header) {
  padding-bottom: 0.5rem;
}
.auth-loading-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--texto-primario);
}
.auth-loading-content {
  padding: 0.5rem 0 0;
  min-width: 280px;
}
</style>
