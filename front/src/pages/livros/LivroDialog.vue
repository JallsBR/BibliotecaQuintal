<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Incluir Informações do Livro"
    :style="{ width: '65rem' }"
    :contentStyle="{ overflow: 'visible' }"
    @hide="limparFormulario"
    @show="carregarOpcoes"
  >
    <div class="dialog-body">
      
      <Tabs value="livro" class="dialog-tabs">
        <TabList>
          <Tab value="livro">Livro</Tab>
          <Tab value="autor">Autor</Tab>
          <Tab value="editora">Editora</Tab>
          <Tab value="categoria">Categoria</Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="livro">
            <div class="dialog-body">
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="livro-titulo" v-model="form.titulo" class="dialog-input" autocomplete="off" />
                    <label for="livro-titulo">Título</label>
                  </FloatLabel>
                </div>

                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <Select
                      id="livro-autor"
                      v-model="form.autor"
                      :options="opcoesAutores"
                      optionLabel="nome"
                      optionValue="id"
                      class="dialog-input"
                      showClear
                      editable
                    />
                    <label for="livro-autor">Autor</label>
                  </FloatLabel>
                </div>

                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <Select
                      id="livro-editora"
                      v-model="form.editora"
                      :options="opcoesEditoras"
                      optionLabel="nome"
                      optionValue="id"
                      class="dialog-input"
                      showClear
                      editable
                    />
                    <label for="livro-editora">Editora</label>
                  </FloatLabel>
                </div>
              </div>

              <div class="dialog-field dialog-field--vertical">
                <FloatLabel variant="on" class="dialog-input-wrap">
                  <Textarea id="livro-descricao" v-model="form.descricao" class="dialog-input" rows="3" autoResize />
                  <label for="livro-descricao">Descrição</label>
                </FloatLabel>
              </div>

              <!-- Categoria / Idioma / ISBN -->
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <Select
                      id="livro-categoria"
                      v-model="form.categoria"
                      :options="opcoesCategorias"
                      optionLabel="nome"
                      optionValue="id"
                      class="dialog-input"
                      showClear
                      editable
                    />
                    <label for="livro-categoria">Categoria</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="livro-idioma" v-model="form.idioma" class="dialog-input" autocomplete="off" />
                    <label for="livro-idioma">Idioma</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="livro-isbn" v-model="form.isbn" class="dialog-input" maxlength="13" autocomplete="off" />
                    <label for="livro-isbn">ISBN</label>
                  </FloatLabel>
                </div>
              </div>

              <!-- Qtd. páginas | Ano publicação | Pontuação -->
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber id="livro-qtd-paginas" v-model="form.qtd_paginas" class="dialog-input" :min="1" showButtons />
                    <label for="livro-qtd-paginas">Qtd. páginas</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber id="livro-ano" v-model="form.ano_publicacao" class="dialog-input" :min="1900" :max="anoAtual" showButtons />
                    <label for="livro-ano">Ano publicação</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber id="livro-pontuacao" v-model="form.pontuacao" class="dialog-input" :min="0" showButtons />
                    <label for="livro-pontuacao">Pontuação</label>
                  </FloatLabel>
                </div>
              </div>

              <!-- Qtd. disponível | Qtd. emprestados | Ativo -->
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber id="livro-qtd-disponivel" v-model="form.qtd_disponivel" class="dialog-input" :min="0" showButtons />
                    <label for="livro-qtd-disponivel">Qtd. disponível</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber id="livro-qtd-emprestados" v-model="form.qtd_emprestados" class="dialog-input" :min="0" showButtons />
                    <label for="livro-qtd-emprestados">Qtd. emprestados</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field dialog-field--checkbox">
                  <div class="dialog-input-wrap dialog-input-wrap--inline dialog-checkbox-wrap">
                    <Checkbox id="livro-ativo" v-model="form.ativo" :binary="true" inputId="livro-ativo" />
                    <label for="livro-ativo" class="dialog-checkbox-label">Ativo</label>
                  </div>
                </div>
              </div>

              <!-- Imagem -->
              <div class="dialog-field dialog-field--vertical">
                <span class="dialog-label">Imagem</span>
                <FileUpload
                  mode="basic"
                  accept="image/*"
                  :maxFileSize="2000000"
                  chooseLabel="Escolher imagem"
                  @select="onImagemSelect"
                />
                <small v-if="form.imagemFile" class="dialog-file-name">{{ form.imagemFile.name }}</small>
              </div>

              <div class="dialog-actions dialog-actions--inside-tab">
                <Button type="button" label="Salvar" @click="salvar" />
              </div>
            </div>
          </TabPanel>

          <TabPanel value="autor">
            <div class="dialog-autor">
              <div class="dialog-row dialog-autor-row">
                <div class="dialog-field dialog-autor-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="autor-nome" v-model="autorForm.nome" class="dialog-input" />
                    <label for="autor-nome">Autor</label>
                  </FloatLabel>
                </div>
                <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarAutor" />
                <Button
                  type="button"
                  label="Buscar"
                  icon="pi pi-search"
                  size="small"
                  class="dialog-autor-button"
                  @click="carregarAutores"
                />
              </div>

              <BaseDataTable
                :items="autores"
                :loading="loadingAutores"
                dataKey="id"
                :totalRecords="autoresTotal"
                :rows="autoresRows"
                :lazy="false"
                :reorderableColumns="false"
                class="dialog-autor-table"
              >
                <template #columns>
                  <Column field="nome" header="Autor" />
                  <Column
                    header="Ações"
                    :style="{ width: '180px', maxWidth: '180px' }"
                    bodyClass="dialog-col-acoes"
                    headerClass="dialog-col-acoes"
                  >
                    <template #body="slotProps">
                      <div class="dialog-col-acoes">
                        <Button
                          label="Editar"
                          severity="success"
                          size="small"
                          @click="editarAutor(slotProps.data)"
                        />
                        <Button
                          label="Excluir"
                          severity="danger"
                          size="small"
                          @click="excluirAutor(slotProps.data)"
                        />
                      </div>
                    </template>
                  </Column>
                </template>
              </BaseDataTable>
            </div>
          </TabPanel>

          <TabPanel value="editora">
            <p>Conteúdo de Editora (a definir).</p>
          </TabPanel>

          <TabPanel value="categoria">
            <p>Conteúdo de Categoria (a definir).</p>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import Dialog from 'primevue/dialog'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import BaseDataTable from '@/components/BaseDataTable.vue'
import Column from 'primevue/column'
import livroService from '@/services/livroService'

const props = defineProps({
  visible: { type: Boolean, default: false }
})

const emit = defineEmits(['update:visible', 'save'])

const visibleModel = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v)
})

const anoAtual = new Date().getFullYear()

const opcoesAutores = ref([])
const opcoesEditoras = ref([])
const opcoesCategorias = ref([])

const form = ref(getFormDefault())

const autores = ref([])
const loadingAutores = ref(false)
const autoresTotal = ref(0)
const autoresRows = 10
const autorEditandoId = ref(null)
const autorForm = ref({ nome: '' })

function getFormDefault() {
  return {
    titulo: '',
    descricao: '',
    pontuacao: null,
    qtd_paginas: null,
    ano_publicacao: null,
    qtd_disponivel: null,
    qtd_emprestados: null,
    idioma: '',
    isbn: '',
    ativo: true,
    autor: null,
    editora: null,
    categoria: null,
    imagemFile: null
  }
}

async function carregarOpcoes() {
  try {
    const [autores, editoras, categorias] = await Promise.all([
      livroService.autores.getAll(),
      livroService.editoras.getAll(),
      livroService.categorias.getAll()
    ])
    const listaAutores = Array.isArray(autores) ? autores : autores?.results ?? []
    opcoesAutores.value = listaAutores
    autores.value = listaAutores
    opcoesEditoras.value = Array.isArray(editoras) ? editoras : editoras?.results ?? []
    opcoesCategorias.value = Array.isArray(categorias) ? categorias : categorias?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar opções:', e)
  }
}

async function carregarAutores() {
  loadingAutores.value = true
  try {
    const data = await livroService.autores.getAll()
    const list = Array.isArray(data) ? data : data?.results ?? []
    autores.value = list
    autoresTotal.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar autores:', e)
    autores.value = []
  } finally {
    loadingAutores.value = false
  }
}

async function salvarAutor() {
  if (!autorForm.value.nome) return
  try {
    if (autorEditandoId.value) {
      await livroService.autores.update(autorEditandoId.value, { nome: autorForm.value.nome })
    } else {
      await livroService.autores.create({ nome: autorForm.value.nome })
    }
    autorForm.value = { nome: '' }
    autorEditandoId.value = null
    await carregarAutores()
    await carregarOpcoes()
  } catch (e) {
    console.error('Erro ao salvar autor:', e)
  }
}

function editarAutor(autor) {
  autorEditandoId.value = autor.id
  autorForm.value = { nome: autor.nome }
}

async function excluirAutor(autor) {
  if (!confirm(`Excluir o autor "${autor.nome}"?`)) return
  try {
    await livroService.autores.delete(autor.id)
    await carregarAutores()
    await carregarOpcoes()
  } catch (e) {
    console.error('Erro ao excluir autor:', e)
  }
}

function onImagemSelect(event) {
  const file = event.files?.[0]
  if (file) form.value.imagemFile = file
}

function limparFormulario() {
  form.value = getFormDefault()
}

function fechar() {
  visibleModel.value = false
}

function salvar() {
  const payload = {
    titulo: form.value.titulo || null,
    descricao: form.value.descricao || null,
    pontuacao: form.value.pontuacao ?? null,
    qtd_paginas: form.value.qtd_paginas ?? null,
    ano_publicacao: form.value.ano_publicacao ?? null,
    qtd_disponivel: form.value.qtd_disponivel ?? null,
    qtd_emprestados: form.value.qtd_emprestados ?? null,
    idioma: form.value.idioma || null,
    isbn: form.value.isbn || null,
    ativo: form.value.ativo ?? true,
    autor: form.value.autor ?? null,
    editora: form.value.editora ?? null,
    categoria: form.value.categoria ?? null
  }
  if (form.value.imagemFile) {
    payload.imagemFile = form.value.imagemFile
  }
  emit('save', payload)
  visibleModel.value = false
}
</script>

<style scoped>
.dialog-body {
  overflow: visible;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: -0.25rem;
}

.dialog-tabs {
  padding: 0rem 0 0;
}

.dialog-tabs :deep(.p-tabs-nav) {
  border-radius: 12px 12px 0 0;
}

.dialog-tabs :deep(.p-tabs-panels) {
  padding-top: 0.5rem;
}

.dialog-field {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  width: 100%;
}

.dialog-label {
  font-weight: 600;
  color: var(--texto-primario);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  display: block;
}

.dialog-input-wrap {
  flex: 1;
  min-width: 0;
  width: 100%;
}

.dialog-input-wrap--inline {
  flex: none;
}

.dialog-field--vertical .dialog-input-wrap {
  width: 100%;
}

.dialog-field--vertical {
  flex-direction: column;
  align-items: stretch;
}

.dialog-field--checkbox {
  align-items: center;
}

.dialog-checkbox-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dialog-checkbox-label {
  font-weight: 500;
}

.dialog-row {
  display: flex;
  gap: 1rem;
}



.dialog-autor-left .dialog-field {
  flex: 0 0 50% !important;
  max-width: 50%;
  margin-bottom: 0;
}

.dialog-autor-right {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
}

.dialog-autor-table {
  margin-top: 1rem;
}

.dialog-autor-acoes-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.25rem;
}

.dialog-col-acoes {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.dialog-row .dialog-field {
  flex: 1;
  margin-bottom: 1rem;
}

.dialog-input {
  flex: 1;
  width: 100%;
}

.dialog-file-name {
  color: var(--texto-secundario);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.dialog-actions--inside-tab {
  margin-top: 0.5rem;
}

.dialog-autor .dialog-row {
  align-items: stretch;
}

.dialog-autor .dialog-field {
  margin-bottom: 0;
}

.dialog-autor :deep(.p-inputtext),
.dialog-autor :deep(.p-button) {
  height: 2.5rem;
}
</style>
