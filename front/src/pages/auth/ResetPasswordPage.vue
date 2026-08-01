<template>
  <div class="auth-page">
    <Card class="auth-card">
      <template #content>
        <form @submit.prevent="salvar">
          <div class="auth-header">
            <img :src="logoSrc" alt="Biblioteca Quintal" class="auth-logo" />
          </div>

          <Message v-if="linkInvalido" severity="error" :closable="false" class="auth-error">
            Link inválido ou incompleto. Solicite uma nova redefinição.
          </Message>

          <template v-else>
            <Message severity="info" :closable="false" class="auth-error">
              Defina uma nova senha para a sua conta.
            </Message>

            <Message v-if="erro" severity="error" :closable="false" class="auth-error">
              {{ erro }}
            </Message>
            <Message v-if="sucesso" severity="success" :closable="false" class="auth-error">
              {{ sucesso }}
            </Message>

            <div class="field mb-3">
              <label for="nova-senha" class="field-label">Nova senha</label>
              <Password
                id="nova-senha"
                v-model="newPassword"
                class="w-full"
                toggleMask
                fluid
                inputClass="w-full"
                autocomplete="new-password"
                :disabled="loading || !!sucesso"
              />
            </div>

            <div class="field mb-3">
              <label for="nova-senha2" class="field-label">Confirmar nova senha</label>
              <Password
                id="nova-senha2"
                v-model="newPasswordConfirm"
                class="w-full"
                :feedback="false"
                toggleMask
                fluid
                inputClass="w-full"
                autocomplete="new-password"
                :disabled="loading || !!sucesso"
              />
            </div>

            <Button
              type="submit"
              :label="loading ? 'Salvando...' : 'Salvar nova senha'"
              class="w-full"
              :loading="loading"
              :disabled="loading || !!sucesso"
            />
          </template>

          <div class="auth-footer">
            <RouterLink to="/signin" class="auth-link">Voltar ao login</RouterLink>
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script>
import Card from 'primevue/card'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { RouterLink } from 'vue-router'
import { LOGO_PRETO } from '@/utils/logo'
import api from '@/services/APIService'

export default {
  name: 'ResetPasswordPage',
  components: { Card, Password, Button, Message, RouterLink },
  data() {
    return {
      challengeId: '',
      token: '',
      newPassword: '',
      newPasswordConfirm: '',
      loading: false,
      erro: null,
      sucesso: null,
      linkInvalido: false
    }
  },
  computed: {
    logoSrc() {
      return LOGO_PRETO
    }
  },
  mounted() {
    this.challengeId = (this.$route.query.c || '').toString().trim()
    this.token = (this.$route.query.t || '').toString().trim()
    if (!this.challengeId || !this.token) {
      this.linkInvalido = true
    }
  },
  methods: {
    formatarErro(data) {
      if (!data || typeof data !== 'object') return 'Não foi possível redefinir a senha.'
      if (data.detail) return String(data.detail)
      const partes = []
      for (const [campo, val] of Object.entries(data)) {
        if (campo === 'detail') continue
        partes.push(Array.isArray(val) ? val.join(' ') : String(val))
      }
      return partes.join(' ') || 'Verifique os dados informados.'
    },
    async salvar() {
      this.erro = null
      if (this.newPassword !== this.newPasswordConfirm) {
        this.erro = 'A nova senha e a confirmação devem ser iguais.'
        return
      }
      if (!this.newPassword) {
        this.erro = 'Informe a nova senha.'
        return
      }
      this.loading = true
      try {
        const { data } = await api.post('/auth/password-reset/confirm', {
          challenge_id: this.challengeId,
          token: this.token,
          new_password: this.newPassword,
          new_password_confirm: this.newPasswordConfirm
        })
        this.sucesso = data?.detail || 'Senha redefinida com sucesso.'
        this.newPassword = ''
        this.newPasswordConfirm = ''
        this.$toast.add({
          severity: 'success',
          summary: 'Senha',
          detail: this.sucesso,
          life: 5000
        })
        this.$router.replace({ name: 'signin' })
      } catch (e) {
        this.erro = this.formatarErro(e?.response?.data)
      } finally {
        this.loading = false
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

.auth-footer {
  margin-top: 1.5rem;
  text-align: center;
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
