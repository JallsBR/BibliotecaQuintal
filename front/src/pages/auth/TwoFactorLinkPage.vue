<template>
  <div class="auth-page">
    <Card class="auth-card">
      <template #content>
        <div class="auth-header">
          <img :src="logoSrc" alt="Biblioteca Quintal" class="auth-logo" />
        </div>

        <Message v-if="erro" severity="error" :closable="false" class="auth-error">
          {{ erro }}
        </Message>
        <Message v-else severity="info" :closable="false" class="auth-error">
          {{ mensagem }}
        </Message>

        <Button
          v-if="erro"
          label="Ir para o login"
          class="w-full"
          @click="$router.push({ name: 'signin' })"
        />
      </template>
    </Card>
  </div>
</template>

<script>
import Card from 'primevue/card'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { LOGO_PRETO } from '@/utils/logo'

export default {
  name: 'TwoFactorLinkPage',
  components: { Card, Button, Message },
  data() {
    return {
      mensagem: 'Concluindo autenticação…',
      erro: null
    }
  },
  computed: {
    logoSrc() {
      return LOGO_PRETO
    }
  },
  async mounted() {
    const challengeId = (this.$route.query.c || '').toString().trim()
    const linkToken = (this.$route.query.t || '').toString().trim()

    if (!challengeId || !linkToken) {
      this.erro = 'Link inválido ou incompleto. Faça login novamente.'
      return
    }

    if (this.$store.getters.isAuthenticated) {
      this.$router.replace({ name: 'home' })
      return
    }

    const ok = await this.$store.dispatch('verifyTwoFactor', {
      challenge_id: challengeId,
      link_token: linkToken
    })

    if (ok) {
      this.mensagem = 'Login concluído. Redirecionando…'
      this.$router.replace({ name: 'home' })
      return
    }

    this.erro =
      'Não foi possível autenticar com este link. Ele pode ter expirado ou já ter sido usado.'
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

.w-full {
  width: 100%;
}
</style>
