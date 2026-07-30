import { computed, readonly, ref } from 'vue'
import { atualizarFavicon, getLogoPorTema, getTemaAtual } from '@/utils/logo'

const TEMA_KEY = 'tema'

// Estado único do módulo: qualquer componente que use o composable
// enxerga a mesma troca de tema
const tema = ref(getTemaAtual())

export function useTema() {
  const logo = computed(() => getLogoPorTema(tema.value))

  function definirTema(novoTema) {
    document.documentElement.setAttribute('data-tema', novoTema)
    localStorage.setItem(TEMA_KEY, novoTema)
    tema.value = novoTema
    atualizarFavicon(novoTema)
  }

  function alternarTema() {
    definirTema(tema.value === 'escuro' ? 'claro' : 'escuro')
  }

  return { tema: readonly(tema), logo, definirTema, alternarTema }
}
