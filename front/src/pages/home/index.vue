<template>
  <div class="home-page">
    <h1 class="home-title">Biblioteca Quintal</h1>
    <p class="home-subtitle">Bem-vindo ao sistema. Acesse rapidamente os módulos abaixo.</p>

    <div class="home-cards" v-if="!loading">
      <RouterLink
        v-for="card in cards"
        :key="card.rota"
        :to="card.rota"
        class="home-card"
      >
        <div class="home-card-icon">
          <i :class="card.icone"></i>
        </div>
        <div class="home-card-body">
          <h3 class="home-card-title">{{ card.titulo }}</h3>
          <p class="home-card-descricao">{{ card.descricao }}</p>
          <p class="home-card-count">{{ card.countFormatted }}</p>
        </div>
        <i class="pi pi-chevron-right home-card-arrow"></i>
      </RouterLink>
      <div v-if="countEmprestimosEmAtraso > 0" class="home-card home-card--no-link">
        <div class="home-card-icon home-card-icon--atraso">
          <i class="pi pi-book"></i>
        </div>
        <div class="home-card-body">
          <h3 class="home-card-title">Devoluções em atraso</h3>
          <p class="home-card-descricao">Empréstimos com data de devolução já passada e ainda não devolvidos</p>
          <p class="home-card-count">{{ countEmprestimosEmAtraso }} em atraso</p>
        </div>
      </div>
    </div>

    <div class="home-loading" v-else>
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: var(--azulquintal)"></i>
      <p>Carregando...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getStats } from '@/services/dashboardService'

const loading = ref(true)
const countLivros = ref(0)
const countLeitores = ref(0)
const countEmprestimosAbertos = ref(0)
const countEmprestimosEmAtraso = ref(0)
const countReservas = ref(0)
const countRecompensas = ref(0)

async function carregarContagens() {
  loading.value = true
  try {
    const stats = await getStats()
    countLivros.value = stats.livros
    countLeitores.value = stats.leitores
    countEmprestimosAbertos.value = stats.emprestimos_abertos
    countEmprestimosEmAtraso.value = stats.emprestimos_em_atraso
    countReservas.value = stats.reservas_ativas
    countRecompensas.value = stats.recompensas
  } catch (e) {
    console.error('Erro ao carregar contagens do dashboard:', e)
  } finally {
    loading.value = false
  }
}

const cards = computed(() => [
  {
    rota: '/livros',
    titulo: 'Livros',
    descricao: 'Acervo de livros',
    icone: 'pi pi-book',
    count: countLivros.value,
    countFormatted: `${countLivros.value} livro${countLivros.value !== 1 ? 's' : ''} cadastrado${countLivros.value !== 1 ? 's' : ''}`
  },
  {
    rota: '/leitores',
    titulo: 'Leitores',
    descricao: 'Cadastro de leitores',
    icone: 'pi pi-users',
    count: countLeitores.value,
    countFormatted: `${countLeitores.value} leitor${countLeitores.value !== 1 ? 'es' : ''} cadastrado${countLeitores.value !== 1 ? 's' : ''}`
  },
  {
    rota: '/emprestimos',
    titulo: 'Empréstimos',
    descricao: 'Empréstimos em aberto',
    icone: 'pi pi-send',
    count: countEmprestimosAbertos.value,
    countFormatted: `${countEmprestimosAbertos.value} empréstimo${countEmprestimosAbertos.value !== 1 ? 's' : ''} em aberto`
  },
  {
    rota: '/reservas',
    titulo: 'Reservas',
    descricao: 'Reservas ativas',
    icone: 'pi pi-clock',
    count: countReservas.value,
    countFormatted: `${countReservas.value} reserva${countReservas.value !== 1 ? 's' : ''} ativa${countReservas.value !== 1 ? 's' : ''}`
  },
  {
    rota: '/recompensas',
    titulo: 'Recompensas',
    descricao: 'Recompensas disponíveis',
    icone: 'pi pi-gift',
    count: countRecompensas.value,
    countFormatted: `${countRecompensas.value} recompensa${countRecompensas.value !== 1 ? 's' : ''} disponíveis`
  }
])

onMounted(carregarContagens)
</script>

<style scoped>
.home-page {
  padding: 1.5rem;
  padding-top: 0;
}

.home-title {
  font-size: 3rem;
  font-weight: 600;
  color: var(--azulquintal);
  margin: 0 0 0.5rem;
}

.home-subtitle {
  color: var(--texto-secundario);
  margin: 0 0 2rem;
}

.home-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}

.home-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: var(--bg-secundario);
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  border: 1px solid transparent;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.home-card:hover {
  border-color: var(--azulquintal);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.home-card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  background: var(--azulquintal);
  color: var(--texto-sobre-azul);
  border-radius: 10px;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.home-card-icon i {
  font-size: inherit;
}

.home-card-body {
  flex: 1;
  min-width: 0;
}

.home-card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--azulquintal);
  margin: 0 0 0.25rem;
}

.home-card-descricao {
  font-size: 0.875rem;
  color: var(--texto-secundario);
  margin: 0 0 0.5rem;
}

.home-card-count {
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--texto-primario);
  margin: 0;
}

.home-card-arrow {
  color: var(--texto-secundario);
  font-size: 1rem;
  flex-shrink: 0;
}

.home-card--no-link {
  cursor: default;
  pointer-events: auto;
}

.home-card--no-link:hover {
  border-color: transparent;
  box-shadow: none;
}

.home-card-icon--atraso {
  background: var(--p-red-500, #ef4444);
  color: white;
}

.home-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem 2rem;
  color: var(--texto-secundario);
}
</style>
