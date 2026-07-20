import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'
import './assets/theme-global.css'
import { atualizarFavicon } from './utils/logo'

const app = createApp(App)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: 'p',
      darkModeSelector: '[data-tema="escuro"]'
    }
  }
})
app.use(ToastService)
app.use(router)
app.use(store)

// Aplica tema salvo antes do mount para evitar flash
const temaSalvo = localStorage.getItem('tema') || 'claro'
document.documentElement.setAttribute('data-tema', temaSalvo)
atualizarFavicon(temaSalvo)

app.mount('#app')
