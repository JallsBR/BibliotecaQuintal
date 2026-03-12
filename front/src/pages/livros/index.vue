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
          <Button label="Buscar" icon="pi pi-search" @click="buscar" />
          <Button label="Incluir" icon="pi pi-plus" @click="incluir" />
          <Button icon="pi pi-spin pi-cog" severity="info" @click="() => {}" />
        </div>
      </template>
      <template #columns>
        <Column field="titulo" header="Título" />
        <Column field="qtd_paginas" header="Quantidade de Páginas" />
        <Column field="qtd_disponivel" header="Quantidade Disponível" />
        <Column field="autor" header="Autor" />
        <Column field="editora" header="Editora" />
        <Column field="categoria" header="Categoria" />
        <Column header="Ações">
          <template #body="slotProps">
            <div class="col-acoes">
              <Button label="Editar" severity="success" size="small" @click="editarLivro(slotProps.data)" />
              <Button label="Excluir" severity="danger" size="small" @click="excluirLivro(slotProps.data)" />
            </div>
          </template>
        </Column>
      </template>
    </BaseDataTable>

    <LivroDialog v-model:visible="dialogVisible" @save="onLivroSalvo" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseDataTable from '@/components/BaseDataTable.vue'
import Column from 'primevue/column'
import Button from 'primevue/button'
import LivroDialog from './LivroDialog.vue'
import livroService from '@/services/livroService'
import { PAGE_SIZE } from '@/constants/pagination'

const livros = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dataKey = 'id'
const totalRecords = ref(0)
const rows = PAGE_SIZE
const lazy = ref(false)
const reorderableColumns = false

async function carregarLivros() {
  loading.value = true
  try {
    const data = await livroService.livros.getAll()
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

function buscar() {
  carregarLivros()
}

function incluir() {
  dialogVisible.value = true
}

async function onLivroSalvo(payload) {
  try {
    if (payload.imagemFile) {
      await livroService.livros.createWithFile(payload)
    } else {
      await livroService.livros.create(payload)
    }
    await carregarLivros()
  } catch (e) {
    console.error('Erro ao incluir livro:', e)
  }
}

function editarLivro(livro) {
  // TODO: abrir modal/dialog de edição
  console.log('Editar livro:', livro)
}

async function excluirLivro(livro) {
  if (!confirm(`Excluir o livro "${livro.titulo}"?`)) return
  try {
    await livroService.livros.delete(livro.id)
    livros.value = livros.value.filter((l) => l.id !== livro.id)
    totalRecords.value = Math.max(0, totalRecords.value - 1)
  } catch (e) {
    console.error('Erro ao excluir livro:', e)
  }
}

onMounted(carregarLivros)
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
</style>
