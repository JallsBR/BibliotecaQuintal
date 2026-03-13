<template>
  <div class="page">
    <h1 class="page-title">Livros</h1>
    <p class="page-subtitle">Gerencie o acervo de livros.</p>

    <BaseDataTable
      :items="livros"
      :loading="loading"
      :dataKey="dataKey"
      :totalRecords="totalRecords"
      :rows="rows"
      :lazy="lazy"
      :reorderableColumns="reorderableColumns"
    >
      <template #toolbar>
        <div class="table-toolbar">
          <Button label="Buscar" icon="pi pi-search" @click="(e) => popoverBuscaRef?.toggle(e)" />
          <Button label="Incluir" icon="pi pi-plus" @click="incluir" />
          <Button icon="pi pi-spin pi-cog" severity="info" @click="() => {}" />
        </div>

        <Popover ref="popoverBuscaRef" :style="{ width: '35%' }">
          <div class="filtro-popover">
            <div class="filtro-linha" >
              <FloatLabel class="filtro-campo">
                <InputText id="filtro-titulo" v-model="filtroTitulo" class="w-full" />
                <label for="filtro-titulo">Título</label>
              </FloatLabel>

              <FloatLabel class="filtro-campo">
                <Select
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
                <Select
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
                <Select
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
      </template>
      <template #columns>
        <Column field="id" header="ID" :style="{ width: '75px', maxWidth: '75px' }" />
        <Column field="titulo" header="Título" :style="{ width: '200px', maxWidth: '200px' }" />
        <Column header="Autor">
          <template #body="slotProps">
            {{ slotProps.data.autor_nome ?? slotProps.data.autor?.nome ?? slotProps.data.autor ?? '' }}
          </template>
        </Column>
        <Column header="Editora">
          <template #body="slotProps">
            {{ slotProps.data.editora_nome ?? slotProps.data.editora?.nome ?? slotProps.data.editora ?? '' }}
          </template>
        </Column>
        <Column header="Categoria">
          <template #body="slotProps">
            {{ slotProps.data.categoria_nome ?? slotProps.data.categoria?.nome ?? slotProps.data.categoria ?? '' }}
          </template>
        </Column>
        <Column field="qtd_paginas" header="Qtd Páginas" :style="{ width: '115px', maxWidth: '115px' }" />
        <Column field="qtd_disponivel" header="Qtd Disponível" :style="{ width: '115px', maxWidth: '115px' }" />

        <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }">
          <template #body="slotProps">
            <div class="col-acoes">
              <Button label="Editar" severity="success" size="small" @click="editarLivro(slotProps.data)" />
              <Button label="Excluir" severity="danger" size="small" @click="excluirLivro(slotProps.data)" />
            </div>
          </template>
        </Column>
      </template>
    </BaseDataTable>

    <LivroDialog v-model:visible="dialogVisible" :livro="livroEditando" @save="onLivroSalvo" />

    <BaseConfirmDialog
      :visible="confirmDeleteLivroVisible"
      title="Excluir livro"
      :message="confirmDeleteLivroMessage"
      confirmLabel="Excluir"
      cancelLabel="Cancelar"
      confirmSeverity="danger"
      :loading="confirmDeleteLivroLoading"
      @update:visible="(v) => (confirmDeleteLivroVisible = v)"
      @confirm="confirmarExclusaoLivro"
      @cancel="cancelarExclusaoLivro"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import BaseDataTable from '@/components/BaseDataTable.vue'
import BaseConfirmDialog from '@/components/BaseConfirmDialog.vue'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Popover from 'primevue/popover'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import LivroDialog from './LivroDialog.vue'
import livroService from '@/services/livroService'
import { PAGE_SIZE } from '@/constants/pagination'

const livros = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const livroEditando = ref(null)
const dataKey = 'id'
const totalRecords = ref(0)
const rows = PAGE_SIZE
const lazy = ref(false)
const reorderableColumns = false

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

const confirmDeleteLivroVisible = ref(false)
const confirmDeleteLivroLoading = ref(false)
const livroParaExcluir = ref(null)

const confirmDeleteLivroMessage = computed(() => {
  if (!livroParaExcluir.value) return 'Confirma a exclusão deste livro?'
  return `Excluir o livro ${livroParaExcluir.value.titulo}?`
})

const toast = useToast()

const anoAtual = new Date().getFullYear()

async function carregarLivros(params = {}) {
  loading.value = true
  try {
    const data = await livroService.livros.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    livros.value = list
    totalRecords.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar livros:', e)
    livros.value = []
  } finally {
    loading.value = false
  }
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
  if (filtroAutor.value) params['autor'] = filtroAutor.value
  if (filtroEditora.value) params['editora'] = filtroEditora.value
  if (filtroCategoria.value) params['categoria'] = filtroCategoria.value
  if (filtroAtivo.value) params['ativo'] = true
  if (filtroDisponivel.value) params['is_disponivel'] = true
  return params
}

async function aplicarFiltros() {
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
  await carregarLivros()
  popoverBuscaRef.value?.hide()
}

function incluir() {
  livroEditando.value = null
  dialogVisible.value = true
}

async function onLivroSalvo(payload) {
  try {
    if (livroEditando.value && livroEditando.value.id) {
      await livroService.livros.update(livroEditando.value.id, payload)
    } else {
      if (payload.imagemFile) {
        await livroService.livros.createWithFile(payload)
      } else {
        await livroService.livros.create(payload)
      }
    }
    await carregarLivros()
    toast.add({
      severity: 'success',
      summary: 'Livro salvo',
      detail: 'O livro foi salvo com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao incluir livro:', e)
    const backendErrors = e?.response?.data
    let detail = 'Não foi possível salvar o livro.'

    if (backendErrors && typeof backendErrors === 'object') {
      const parts = []
      for (const [field, messages] of Object.entries(backendErrors)) {
        const textoCampo = Array.isArray(messages) ? messages.join(' ') : String(messages)
        parts.push(`${field}: ${textoCampo}`)
      }
      if (parts.length > 0) {
        detail = parts.join(' | ')
      }
    }

    toast.add({
      severity: 'error',
      summary: 'Erro ao salvar livro',
      detail,
      life: 5000
    })
  }
}

function editarLivro(livro) {
  livroEditando.value = livro
  dialogVisible.value = true
}

function excluirLivro(livro) {
  livroParaExcluir.value = livro
  confirmDeleteLivroVisible.value = true
}

async function confirmarExclusaoLivro() {
  if (!livroParaExcluir.value) return
  confirmDeleteLivroLoading.value = true
  try {
    await livroService.livros.delete(livroParaExcluir.value.id)
    livros.value = livros.value.filter((l) => l.id !== livroParaExcluir.value.id)
    totalRecords.value = Math.max(0, totalRecords.value - 1)
  } catch (e) {
    console.error('Erro ao excluir livro:', e)
  } finally {
    confirmDeleteLivroLoading.value = false
    confirmDeleteLivroVisible.value = false
    livroParaExcluir.value = null
  }
}

function cancelarExclusaoLivro() {
  confirmDeleteLivroVisible.value = false
  livroParaExcluir.value = null
}

onMounted(async () => {
  await Promise.all([carregarLivros(), carregarFiltros()])
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

.table-toolbar {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.col-acoes {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
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
  margin-bottom: 1.0rem;
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
</style>
