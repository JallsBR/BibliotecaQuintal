import { createStore } from 'vuex'
import api from '../services/APIService'

export default createStore({
  state: {
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('access') || null,
    loading: false
  },

  getters: {
    isAuthenticated: state => !!state.token,
    getUser: state => state.user,
    isLoading: state => state.loading,
    isSuperuser: state => !!state.user?.is_superuser,
    hasPermission: state => (perm) => {
      if (state.user?.is_superuser) return true
      const perms = state.user?.permissions
      return Array.isArray(perms) && perms.includes(perm)
    }
  },

  mutations: {
    SET_LOADING(state, value) {
      state.loading = value
    },

    SET_AUTH(state, { user, access, refresh }) {
      state.user = user
      state.token = access

      localStorage.setItem('access', access)
      localStorage.setItem('refresh', refresh)
      localStorage.setItem('user', JSON.stringify(user))
    },

    LOGOUT(state) {
      state.user = null
      state.token = null

      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    }
  },

  actions: {
    async login({ commit }, { email, password }) {
      try {
        commit('SET_LOADING', true)

        const response = await api.post('/auth/signin', {
          email,
          password
        })

        const data = response.data || {}

        if (data.requires_2fa && data.challenge_id) {
          return {
            requires_2fa: true,
            challenge_id: data.challenge_id
          }
        }

        const { user, access, refresh } = data

        if (!access || !refresh) {
          throw new Error('Tokens inválidos')
        }

        commit('SET_AUTH', {
          user: user || { username: email, email },
          access,
          refresh
        })

        return { ok: true }
      } catch (error) {
        console.error('Erro no login:', error)
        return { ok: false }
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async verifyTwoFactor({ commit }, { challenge_id, code, link_token }) {
      try {
        commit('SET_LOADING', true)
        const body = { challenge_id }
        if (code != null && String(code).trim() !== '') {
          body.code = String(code).trim()
        } else if (link_token != null && String(link_token).trim() !== '') {
          body.link_token = String(link_token).trim()
        }
        const { data } = await api.post('/auth/2fa/verify', body)
        const { user, access, refresh } = data || {}

        if (!access || !refresh) {
          throw new Error('Tokens inválidos')
        }

        commit('SET_AUTH', {
          user: user || {},
          access,
          refresh
        })
        return true
      } catch (error) {
        console.error('Erro na verificação 2FA:', error)
        return false
      } finally {
        commit('SET_LOADING', false)
      }
    },

    logout({ commit }) {
      commit('LOGOUT')
      window.location.href = '/signin'
    }
  }
})
