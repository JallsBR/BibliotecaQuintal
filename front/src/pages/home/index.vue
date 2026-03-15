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
    </div>

    <div class="home-loading" v-else>
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: var(--azulquintal)"></i>
      <p>Carregando...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import leitorService from '@/services/leitorService'
import livroService from '@/services/livroService'

const loading = ref(true)
const countLivros = ref(0)
const countLeitores = ref(0)
const countEmprestimosAbertos = ref(0)
const countReservas = ref(0)
const countRecompensas = ref(0)

async function getCount(service, params = {}) {
  try {
    const data = await service.getAll({ ...params, page_size: 1 })
    return data?.count ?? (Array.isArray(data) ? data.length : data?.results?.length ?? 0)
  } catch {
    return 0
  }
}

async function carregarContagens() {
  loading.value = true
  try {
    const [livros, leitores, emprestimos, reservas, recompensas] = await Promise.all([
      getCount(livroService.livros),
      getCount(leitorService.leitores),
      getCount(leitorService.emprestimos, { devolvido: false }),
      getCount(leitorService.reservas, { ativo: true }),
      getCount(leitorService.recompensas)
    ])
    countLivros.value = livros
    countLeitores.value = leitores
    countEmprestimosAbertos.value = emprestimos
    countReservas.value = reservas
    countRecompensas.value = recompensas
  } catch (e) {
    console.error('Erro ao carregar contagens:', e)
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
