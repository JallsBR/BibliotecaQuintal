import axios from 'axios'
import store from '../store'
import router from '../router'

const API_URL = import.meta.env.VITE_API_BASE || '/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh')

      if (!refreshToken) {
        await handleLogout()
        return Promise.reject(error)
      }

      try {
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken
        })
        const { access } = response.data
        localStorage.setItem('access', access)
        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        await handleLogout()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

async function handleLogout() {
  store.commit('LOGOUT')
  await router.push({ name: 'signin' })
}

export default api
