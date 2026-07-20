<template>
  <div class="page">
    <h1 class="page-title">Acervo</h1>
    <p class="page-subtitle">Explore o acervo em cartões visuais.</p>

    <div class="toolbar">
      <Button
        label="Buscar"
        size="small"
        icon="pi pi-search"
        @click="(e) => popoverBuscaRef?.toggle(e)"
      />
    </div>

    <Popover ref="popoverBuscaRef" :style="{ width: '35%' }">
      <div class="filtro-popover">
        <div class="filtro-linha">
          <FloatLabel class="filtro-campo">
            <InputText id="filtro-titulo" v-model="filtroTitulo" class="w-full" />
            <label for="filtro-titulo">Título</label>
          </FloatLabel>

          <FloatLabel class="filtro-campo">
            <BaseSelect
              id="filtro-autor"
              v-model="filtroAutor"
              :options="opcoesAutores"
              optionLabel="nome"
              optionValue="id"
              showClear
              class="w-full"
            />
            <label for="filtro-autor">Autor</label>
          </FloatLabel>
        </div>

        <div class="filtro-linha filtro-linha--3">
          <FloatLabel class="filtro-campo">
            <InputText id="filtro-idioma" v-model="filtroIdioma" class="w-full" />
            <label for="filtro-idioma">Idioma</label>
          </FloatLabel>
          <FloatLabel class="filtro-campo">
            <BaseSelect
              id="filtro-editora"
              v-model="filtroEditora"
              :options="opcoesEditoras"
              optionLabel="nome"
              optionValue="id"
              showClear
              class="w-full"
            />
            <label for="filtro-editora">Editora</label>
          </FloatLabel>
          <FloatLabel class="filtro-campo">
            <BaseSelect
              id="filtro-categoria"
              v-model="filtroCategoria"
              :options="opcoesCategorias"
              optionLabel="nome"
              optionValue="id"
              showClear
              class="w-full"
            />
            <label for="filtro-categoria">Categoria</label>
          </FloatLabel>
        </div>

        <div class="filtro-linha">
          <FloatLabel class="filtro-campo">
            <InputNumber id="filtro-ano-de" v-model="filtroAnoDe" :min="1900" :max="anoAtual" class="w-full" />
            <label for="filtro-ano-de">Ano publicação &ge;</label>
          </FloatLabel>
          <FloatLabel class="filtro-campo">
            <InputNumber id="filtro-ano-ate" v-model="filtroAnoAte" :min="1900" :max="anoAtual" class="w-full" />
            <label for="filtro-ano-ate">Ano publicação &le;</label>
          </FloatLabel>
        </div>

        <div class="filtro-switches">
          <div class="filtro-switch">
            <Checkbox v-model="filtroAtivo" :binary="true" inputId="filtro-ativo" />
            <label for="filtro-ativo">Apenas ativos</label>
          </div>
          <div class="filtro-switch">
            <Checkbox v-model="filtroDisponivel" :binary="true" inputId="filtro-disponivel" />
            <label for="filtro-disponivel">Apenas disponíveis</label>
          </div>
        </div>

        <div class="filtro-acoes">
          <Button label="Aplicar" icon="pi pi-check" size="small" @click="aplicarFiltros" />
          <Button label="Limpar" icon="pi pi-filter-slash" size="small" severity="secondary" @click="limparFiltros" />
        </div>
      </div>
    </Popover>

    <div v-if="loading" class="galeria-loading">Carregando...</div>
    <div v-else class="cards-container">
      <div
        v-for="livro in livros"
        :key="livro.id"
        class="livro-card"
        @click="abrirDetalhes(livro)"
      >
        <div class="livro-card-image-wrap">
          <img
            :src="getImagemLivro(livro)"
            alt="Capa do livro"
            class="livro-card-image"
          />
        </div>
        <div class="livro-card-content">
          <h3 class="livro-card-title">{{ livro.titulo }}</h3>
          <p class="livro-card-author">
            {{ formatarAutores(livro.autores_nomes) }}
          </p>
        </div>
      </div>
    </div>

    <Paginator
      v-if="totalRecords > 0"
      :rows="rows"
      :totalRecords="totalRecords"
      :first="first"
      template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport"
      currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} livros"
      @page="onPage"
      class="galeria-paginator"
    />

    <Dialog v-model:visible="dialogVisible" modal header="Detalhes do livro" :style="{ width: '40rem' }">
      <div v-if="livroSelecionado" class="dialog-detalhes">
        <div class="dialog-detalhes-header">
          <img
            :src="getImagemLivro(livroSelecionado)"
            alt="Capa do livro"
            class="dialog-detalhes-image"
          />
          <div class="dialog-detalhes-main">
            <h2>{{ livroSelecionado.titulo }}</h2>
            <p class="dialog-detalhes-autores">
              {{ formatarAutores(livroSelecionado.autores_nomes) }}
            </p>
            <p class="dialog-detalhes-editora">
              <strong>Editora:</strong> {{ livroSelecionado.editora_nome || '—' }}
            </p>
            <p class="dialog-detalhes-info">
              <span v-if="livroSelecionado.ano_publicacao">Ano: {{ livroSelecionado.ano_publicacao }}</span>
              <span v-if="livroSelecionado.qtd_paginas"> · Páginas: {{ livroSelecionado.qtd_paginas }}</span>
              <span v-if="livroSelecionado.idioma"> · Idioma: {{ livroSelecionado.idioma }}</span>
            </p>
          </div>
        </div>
        <div class="dialog-detalhes-body">
          <p v-if="livroSelecionado.descricao">
            {{ livroSelecionado.descricao }}
          </p>
          <p v-else class="dialog-detalhes-sem-descricao">
            Nenhuma descrição cadastrada para este livro.
          </p>
          <p class="dialog-detalhes-categorias" v-if="Array.isArray(livroSelecionado.categorias_nomes) && livroSelecionado.categorias_nomes.length">
            <strong>Categorias:</strong> {{ livroSelecionado.categorias_nomes.join(', ') }}
          </p>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Popover from 'primevue/popover'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import BaseSelect from '@/components/BaseSelect.vue'
import Checkbox from 'primevue/checkbox'
import Dialog from 'primevue/dialog'
import Paginator from 'primevue/paginator'
import livroService from '@/services/livroService'
import { getLogoAtual } from '@/utils/logo'

const store = useStore()
const hasPermission = (perm) => store.getters.hasPermission(perm)

const livros = ref([])
const loading = ref(false)
const totalRecords = ref(0)
const first = ref(0)
const rows = 25

const popoverBuscaRef = ref(null)
const filtroTitulo = ref('')
const filtroIdioma = ref('')
const filtroAnoDe = ref(null)
const filtroAnoAte = ref(null)
const filtroAutor = ref(null)
const filtroEditora = ref(null)
const filtroCategoria = ref(null)
const filtroAtivo = ref(false)
const filtroDisponivel = ref(false)

const opcoesAutores = ref([])
const opcoesEditoras = ref([])
const opcoesCategorias = ref([])

const dialogVisible = ref(false)
const livroSelecionado = ref(null)

const toast = useToast()
const anoAtual = new Date().getFullYear()

const logoFallback = getLogoAtual()

function getImagemLivro(livro) {
  if (livro.imagem) {
    return livro.imagem
  }
  if (livro.imagem_url) {
    return livro.imagem_url
  }
  return logoFallback
}

function formatarAutores(autoresNomes) {
  if (Array.isArray(autoresNomes) && autoresNomes.length) {
    return autoresNomes.join(', ')
  }
  return 'Autor não informado'
}

async function carregarLivros(params = {}) {
  loading.value = true
  try {
    const page = params.page ?? currentPage.value
    const query = { ...params, page, page_size: rows }
    const data = await livroService.livros.getAll(query)
    const list = Array.isArray(data) ? data : data?.results ?? []
    livros.value = list
    totalRecords.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar livros:', e)
    livros.value = []
    totalRecords.value = 0
    toast.add({
      severity: 'error',
      summary: 'Erro ao carregar livros',
      detail: 'Não foi possível carregar os livros do acervo.',
      life: 4000
    })
  } finally {
    loading.value = false
  }
}

const currentPage = ref(1)

function onPage(event) {
  first.value = event.first
  currentPage.value = event.page + 1
  const params = montarParametrosBusca()
  params.page = currentPage.value
  params.page_size = rows
  carregarLivros(params)
}

async function carregarFiltros() {
  try {
    const [autores, editoras, categorias] = await Promise.all([
      livroService.autores.getAll(),
      livroService.editoras.getAll(),
      livroService.categorias.getAll()
    ])
    opcoesAutores.value = Array.isArray(autores) ? autores : autores?.results ?? []
    opcoesEditoras.value = Array.isArray(editoras) ? editoras : editoras?.results ?? []
    opcoesCategorias.value = Array.isArray(categorias) ? categorias : categorias?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar filtros de livros:', e)
  }
}

function montarParametrosBusca() {
  const params = {}
  if (filtroTitulo.value?.trim()) params['titulo__icontains'] = filtroTitulo.value.trim()
  if (filtroIdioma.value?.trim()) params['idioma__icontains'] = filtroIdioma.value.trim()
  if (filtroAnoDe.value != null) params['ano_publicacao__gte'] = filtroAnoDe.value
  if (filtroAnoAte.value != null) params['ano_publicacao__lte'] = filtroAnoAte.value
  if (filtroAutor.value) params['autores'] = filtroAutor.value
  if (filtroEditora.value) params['editora'] = filtroEditora.value
  if (filtroCategoria.value) params['categorias'] = filtroCategoria.value
  if (filtroAtivo.value) params['ativo'] = true
  if (filtroDisponivel.value) params['is_disponivel'] = true
  return params
}

async function aplicarFiltros() {
  first.value = 0
  currentPage.value = 1
  const params = montarParametrosBusca()
  await carregarLivros(params)
  popoverBuscaRef.value?.hide()
}

async function limparFiltros() {
  filtroTitulo.value = ''
  filtroIdioma.value = ''
  filtroAnoDe.value = null
  filtroAnoAte.value = null
  filtroAutor.value = null
  filtroEditora.value = null
  filtroCategoria.value = null
  filtroAtivo.value = false
  filtroDisponivel.value = false
  first.value = 0
  currentPage.value = 1
  await carregarLivros()
  popoverBuscaRef.value?.hide()
}

function abrirDetalhes(livro) {
  livroSelecionado.value = livro
  dialogVisible.value = true
}

onMounted(async () => {
  await carregarFiltros()
  await carregarLivros({ page: 1, page_size: rows })
})
</script>

<style scoped>
.page {
  padding: 1.5rem;
  padding-top: 0;
}

.page-title {
  font-size: 3rem;
  font-weight: 600;
  color: var(--azulquintal);
  margin: 0 0 0.5rem;
}

.page-subtitle {
  color: var(--texto-primario);
  margin: 0 0 1.5rem;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.galeria-loading {
  padding: 2rem;
  text-align: center;
  color: var(--texto-secundario);
}

.galeria-paginator {
  margin-top: 1.5rem;
  justify-content: center;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 1rem;
}

.livro-card {
  background: var(--bg-secundario);
  border-radius: 12px;
  box-shadow: 0 2px 6px color-mix(in srgb, var(--azulquintal) 12%, transparent);
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.livro-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 14px color-mix(in srgb, var(--azulquintal) 22%, transparent);
}

.livro-card-image-wrap {
  width: 100%;
  padding-top: 140%;
  position: relative;
  overflow: hidden;
}

.livro-card-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.livro-card-content {
  padding: 0.75rem 0.8rem 0.9rem;
}

.livro-card-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--texto-primario);
  margin: 0 0 0.25rem;
}

.livro-card-author {
  font-size: 0.8rem;
  color: var(--texto-secundario);
  margin: 0;
}

.filtro-popover {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 32rem;
}

.filtro-linha {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.filtro-linha--3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.filtro-campo {
  width: 100%;
}

.filtro-switches {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 1.5rem;
}

.filtro-switch {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.filtro-acoes {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.dialog-detalhes {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dialog-detalhes-header {
  display: flex;
  gap: 1rem;
}

.dialog-detalhes-image {
  width: 120px;
  height: 160px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.dialog-detalhes-main h2 {
  margin: 0 0 0.25rem;
  font-size: 1.4rem;
}

.dialog-detalhes-autores {
  margin: 0 0 0.25rem;
  font-size: 0.9rem;
  color: var(--texto-secundario);
}

.dialog-detalhes-editora {
  margin: 0 0 0.25rem;
  font-size: 0.9rem;
}

.dialog-detalhes-info {
  margin: 0;
  font-size: 0.85rem;
  color: var(--texto-secundario);
}

.dialog-detalhes-body {
  font-size: 0.9rem;
  color: var(--texto-primario);
}

.dialog-detalhes-sem-descricao {
  font-style: italic;
  color: var(--texto-secundario);
}

.dialog-detalhes-categorias {
  margin-top: 0.5rem;
  font-size: 0.85rem;
}
</style>

