<template>
  <div class="auth-page">
    <Card class="auth-card" style="width: 650px;">
      <template #content>
        <form v-if="passo === 'login'" @submit.prevent="handleLogin">
          <div class="auth-header">
            <img :src="logoSrc" alt="Biblioteca Quintal" class="auth-logo" />
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

          <p class="auth-forgot">
            <button type="button" class="auth-link auth-link-btn" @click="abrirEsqueciSenha">
              Esqueceu a senha?
            </button>
          </p>

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

        <form v-else-if="passo === 'forgot'" @submit.prevent="handleForgotPassword">
          <div class="auth-header">
            <img :src="logoSrc" alt="Biblioteca Quintal" class="auth-logo" />
          </div>

          <Message severity="info" :closable="false" class="auth-error">
            Informe o e-mail da conta. Se existir, enviaremos um link para redefinir a senha.
          </Message>

          <Message v-if="erroForgot" severity="error" :closable="false" class="auth-error">
            {{ erroForgot }}
          </Message>
          <Message v-if="sucessoForgot" severity="success" :closable="false" class="auth-error">
            {{ sucessoForgot }}
          </Message>

          <div class="field mb-3">
            <label for="email-forgot" class="field-label">Email</label>
            <InputText
              id="email-forgot"
              v-model="emailForgot"
              type="email"
              class="w-full"
              placeholder="seu@email.com"
              autocomplete="email"
              :disabled="loading || !!sucessoForgot"
            />
          </div>

          <Button
            type="submit"
            :label="loading ? 'Enviando...' : 'Enviar link'"
            class="w-full"
            :loading="loading"
            :disabled="loading || !emailForgot.trim() || !!sucessoForgot"
          />

          <div class="auth-footer">
            <button type="button" class="auth-link auth-link-btn" @click="voltarLogin">
              Voltar ao login
            </button>
          </div>
        </form>

        <form v-else @submit.prevent="handleVerify2fa">
          <div class="auth-header">
            <img :src="logoSrc" alt="Biblioteca Quintal" class="auth-logo" />
          </div>

          <Message severity="info" :closable="false" class="auth-error">
            Enviamos um código e um link para o e-mail cadastrado. Digite o código abaixo ou
            abra o link “Entrar agora”.
          </Message>

          <Message v-if="error2fa" severity="error" :closable="false" class="auth-error">
            Código inválido ou expirado. Tente novamente.
          </Message>

          <div class="field mb-3">
            <label for="otp-code" class="field-label">Código de verificação</label>
            <InputText
              id="otp-code"
              v-model="otpCode"
              type="text"
              inputmode="numeric"
              maxlength="6"
              class="w-full"
              placeholder="000000"
              autocomplete="one-time-code"
            />
          </div>

          <Button
            type="submit"
            :label="loading ? 'Verificando...' : 'Verificar código'"
            class="w-full"
            :loading="loading"
            :disabled="loading || otpCode.trim().length !== 6"
          />

          <div class="auth-footer">
            <button type="button" class="auth-link auth-link-btn" @click="voltarLogin">
              Voltar ao login
            </button>
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
import { LOGO_PRETO } from '@/utils/logo'
import api from '@/services/APIService'

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
      passo: 'login',
      email: '',
      password: '',
      error: null,
      error2fa: null,
      challengeId: null,
      otpCode: '',
      emailForgot: '',
      erroForgot: null,
      sucessoForgot: null
    }
  },

  computed: {
    loading() {
      return this.$store.getters.isLoading
    },
    logoSrc() {
      return LOGO_PRETO
    }
  },

  methods: {
    abrirEsqueciSenha() {
      this.passo = 'forgot'
      this.emailForgot = this.email.trim()
      this.erroForgot = null
      this.sucessoForgot = null
      this.error = null
    },

    async handleForgotPassword() {
      this.erroForgot = null
      this.sucessoForgot = null
      this.$store.commit('SET_LOADING', true)
      try {
        const { data } = await api.post('/auth/password-reset/request', {
          email: this.emailForgot.trim()
        })
        this.sucessoForgot =
          data?.detail ||
          'Se existir uma conta com esses dados, enviamos um e-mail com instruções.'
        this.$toast.add({
          severity: 'success',
          summary: 'E-mail',
          detail: this.sucessoForgot,
          life: 6000
        })
      } catch (e) {
        const data = e?.response?.data
        this.erroForgot =
          data?.detail ||
          data?.login?.[0] ||
          data?.email?.[0] ||
          'Não foi possível solicitar a redefinição. Tente novamente.'
      } finally {
        this.$store.commit('SET_LOADING', false)
      }
    },

    async handleLogin() {
      this.error = null
      this.error2fa = null
      const result = await this.$store.dispatch('login', {
        email: this.email,
        password: this.password
      })

      if (result?.requires_2fa && result.challenge_id) {
        this.passo = '2fa'
        this.challengeId = result.challenge_id
        this.otpCode = ''
        this.$toast.add({
          severity: 'info',
          summary: 'Verificação em dois fatores',
          detail: 'Enviamos um código para o seu e-mail.',
          life: 5000
        })
        return
      }

      if (result?.ok) {
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
    },

    async handleVerify2fa() {
      this.error2fa = null
      const success = await this.$store.dispatch('verifyTwoFactor', {
        challenge_id: this.challengeId,
        code: this.otpCode.trim()
      })

      if (success) {
        this.$router.push({ name: 'home' })
      } else {
        this.error2fa = true
        this.$toast.add({
          severity: 'error',
          summary: 'Código inválido',
          detail: 'Código inválido ou expirado. Tente novamente.',
          life: 5000
        })
      }
    },

    voltarLogin() {
      this.passo = 'login'
      this.challengeId = null
      this.otpCode = ''
      this.error2fa = null
      this.password = ''
      this.erroForgot = null
      this.sucessoForgot = null
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
  max-width: 400px;
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

.auth-forgot {
  margin: -0.25rem 0 1rem;
  text-align: right;
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
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font: inherit;
}

.auth-link:hover {
  text-decoration: underline;
}

.auth-link-btn {
  display: inline;
}
</style>
