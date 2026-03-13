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
      
      <Tabs v-model:value="tabAtiva" class="dialog-tabs">
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

                <div class="dialog-field" @click="onAutorSelectAreaClick">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <Select
                      ref="selectAutorRef"
                      id="livro-autor"
                      v-model="form.autor"
                      :options="autores"
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
                    <label for="autor-nome">Inserir Autor</label>
                  </FloatLabel>
                </div>
                <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarAutor" />
                <Button
                  type="button"
                  label="Buscar"
                  icon="pi pi-search"
                  size="small"
                  class="dialog-autor-button"
                  @click="(e) => popoverPesquisaAutorRef?.toggle(e)"
                />
                <Popover ref="popoverPesquisaAutorRef">
                  <div class="dialog-popover-pesquisa">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText
                        id="pesquisa-autor"
                        v-model="filtroPesquisaAutor"
                        class="dialog-input"
                        autocomplete="off"
                        @keyup.enter="aplicarPesquisaAutor"
                      />
                      <label for="pesquisa-autor">Pesquisar Autor</label>
                    </FloatLabel>
                    <div class="dialog-popover-actions">
                      <Button type="button" label="Buscar" size="small" @click="aplicarPesquisaAutor" />
                      <Button type="button" label="Limpar" severity="secondary" size="small" @click="limparPesquisaAutor" />
                    </div>
                  </div>
                </Popover>
              </div>

              <BaseDataTable
                :items="autoresFiltrados"
                :loading="loadingAutores"
                dataKey="id"
                :totalRecords="autoresFiltrados.length"
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
                          @click="abrirConfirmacaoExcluirAutor(slotProps.data)"
                        />
                      </div>
                    </template>
                  </Column>
                </template>
              </BaseDataTable>

              <BaseConfirmDialog
                :visible="confirmDeleteAutorVisible"
                title="Excluir autor"
                :message="confirmDeleteAutorMessage"
                confirmLabel="Excluir"
                cancelLabel="Cancelar"
                confirmSeverity="danger"
                :loading="confirmDeleteAutorLoading"
                @update:visible="(v) => (confirmDeleteAutorVisible = v)"
                @confirm="confirmarExclusaoAutor"
                @cancel="cancelarExclusaoAutor"
              />
            </div>
          </TabPanel>

          <TabPanel value="editora">
            <div class="dialog-autor">
              <div class="dialog-row dialog-autor-row">
                <div class="dialog-field dialog-autor-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="editora-nome" v-model="editoraForm.nome" class="dialog-input" />
                    <label for="editora-nome">Inserir Editora</label>
                  </FloatLabel>
                </div>
                <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarEditora" />
                <Button
                  type="button"
                  label="Buscar"
                  icon="pi pi-search"
                  size="small"
                  class="dialog-autor-button"
                  @click="(e) => popoverPesquisaEditoraRef?.toggle(e)"
                />
                <Popover ref="popoverPesquisaEditoraRef">
                  <div class="dialog-popover-pesquisa">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText
                        id="pesquisa-editora"
                        v-model="filtroPesquisaEditora"
                        class="dialog-input"
                        autocomplete="off"
                      />
                      <label for="pesquisa-editora">Pesquisar Editora</label>
                    </FloatLabel>
                    <div class="dialog-popover-actions">
                      <Button type="button" label="Fechar" size="small" @click="popoverPesquisaEditoraRef?.hide()" />
                      <Button
                        type="button"
                        label="Limpar"
                        severity="secondary"
                        size="small"
                        @click="limparPesquisaEditora"
                      />
                    </div>
                  </div>
                </Popover>
              </div>

              <BaseDataTable
                :items="editorasFiltradas"
                :loading="loadingEditoras"
                dataKey="id"
                :totalRecords="editorasFiltradas.length"
                :rows="editorasRows"
                :lazy="false"
                :reorderableColumns="false"
                class="dialog-autor-table"
              >
                <template #columns>
                  <Column field="nome" header="Editora" />
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
                          @click="editarEditora(slotProps.data)"
                        />
                        <Button
                          label="Excluir"
                          severity="danger"
                          size="small"
                          @click="abrirConfirmacaoExcluirEditora(slotProps.data)"
                        />
                      </div>
                    </template>
                  </Column>
                </template>
              </BaseDataTable>

              <BaseConfirmDialog
                :visible="confirmDeleteEditoraVisible"
                title="Excluir editora"
                :message="confirmDeleteEditoraMessage"
                confirmLabel="Excluir"
                cancelLabel="Cancelar"
                confirmSeverity="danger"
                :loading="confirmDeleteEditoraLoading"
                @update:visible="(v) => (confirmDeleteEditoraVisible = v)"
                @confirm="confirmarExclusaoEditora"
                @cancel="cancelarExclusaoEditora"
              />
            </div>
          </TabPanel>

          <TabPanel value="categoria">
            <div class="dialog-autor">
              <div class="dialog-row dialog-autor-row">
                <div class="dialog-field dialog-autor-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="categoria-nome" v-model="categoriaForm.nome" class="dialog-input" />
                    <label for="categoria-nome">Inserir Categoria</label>
                  </FloatLabel>
                </div>
                <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarCategoria" />
                <Button
                  type="button"
                  label="Buscar"
                  icon="pi pi-search"
                  size="small"
                  class="dialog-autor-button"
                  @click="(e) => popoverPesquisaCategoriaRef?.toggle(e)"
                />
                <Popover ref="popoverPesquisaCategoriaRef">
                  <div class="dialog-popover-pesquisa">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText
                        id="pesquisa-categoria"
                        v-model="filtroPesquisaCategoria"
                        class="dialog-input"
                        autocomplete="off"
                      />
                      <label for="pesquisa-categoria">Pesquisar Categoria</label>
                    </FloatLabel>
                    <div class="dialog-popover-actions">
                      <Button type="button" label="Fechar" size="small" @click="popoverPesquisaCategoriaRef?.hide()" />
                      <Button
                        type="button"
                        label="Limpar"
                        severity="secondary"
                        size="small"
                        @click="limparPesquisaCategoria"
                      />
                    </div>
                  </div>
                </Popover>
              </div>

              <BaseDataTable
                :items="categoriasFiltradas"
                :loading="loadingCategorias"
                dataKey="id"
                :totalRecords="categoriasFiltradas.length"
                :rows="categoriasRows"
                :lazy="false"
                :reorderableColumns="false"
                class="dialog-autor-table"
              >
                <template #columns>
                  <Column field="nome" header="Categoria" />
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
                          @click="editarCategoria(slotProps.data)"
                        />
                        <Button
                          label="Excluir"
                          severity="danger"
                          size="small"
                          @click="abrirConfirmacaoExcluirCategoria(slotProps.data)"
                        />
                      </div>
                    </template>
                  </Column>
                </template>
              </BaseDataTable>

              <BaseConfirmDialog
                :visible="confirmDeleteCategoriaVisible"
                title="Excluir categoria"
                :message="confirmDeleteCategoriaMessage"
                confirmLabel="Excluir"
                cancelLabel="Cancelar"
                confirmSeverity="danger"
                :loading="confirmDeleteCategoriaLoading"
                @update:visible="(v) => (confirmDeleteCategoriaVisible = v)"
                @confirm="confirmarExclusaoCategoria"
                @cancel="cancelarExclusaoCategoria"
              />
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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
import BaseConfirmDialog from '@/components/BaseConfirmDialog.vue'
import Column from 'primevue/column'
import Popover from 'primevue/popover'
import { useToast } from 'primevue/usetoast'
import livroService from '@/services/livroService'

const props = defineProps({
  visible: { type: Boolean, default: false },
  livro: { type: Object, default: null }
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
const tabAtiva = ref('livro')
const popoverPesquisaAutorRef = ref(null)
const filtroPesquisaAutor = ref('')
const selectAutorRef = ref(null)

const confirmDeleteAutorVisible = ref(false)
const confirmDeleteAutorLoading = ref(false)
const autorParaExcluir = ref(null)

const confirmDeleteAutorMessage = computed(() => {
  if (!autorParaExcluir.value) return 'Confirma a exclusão deste autor?'
  return `Excluir o autor ${autorParaExcluir.value.nome}?`
})

const editoras = ref([])
const loadingEditoras = ref(false)
const editorasRows = 10
const editoraEditandoId = ref(null)
const editoraForm = ref({ nome: '' })
const popoverPesquisaEditoraRef = ref(null)
const filtroPesquisaEditora = ref('')

const confirmDeleteEditoraVisible = ref(false)
const confirmDeleteEditoraLoading = ref(false)
const editoraParaExcluir = ref(null)

const confirmDeleteEditoraMessage = computed(() => {
  if (!editoraParaExcluir.value) return 'Confirma a exclusão desta editora?'
  return `Excluir a editora ${editoraParaExcluir.value.nome}?`
})

const categorias = ref([])
const loadingCategorias = ref(false)
const categoriasRows = 10
const categoriaEditandoId = ref(null)
const categoriaForm = ref({ nome: '' })
const popoverPesquisaCategoriaRef = ref(null)
const filtroPesquisaCategoria = ref('')

const confirmDeleteCategoriaVisible = ref(false)
const confirmDeleteCategoriaLoading = ref(false)
const categoriaParaExcluir = ref(null)

const confirmDeleteCategoriaMessage = computed(() => {
  if (!categoriaParaExcluir.value) return 'Confirma a exclusão desta categoria?'
  return `Excluir a categoria ${categoriaParaExcluir.value.nome}?`
})

const toast = useToast()

function onAutorSelectAreaClick(e) {
  const t = e.target
  const isInput = t.tagName === 'INPUT'
  const isComboboxSpan = t.tagName === 'SPAN' && t.getAttribute('role') === 'combobox'
  if (isInput || isComboboxSpan) selectAutorRef.value?.show(true)
}

const autoresFiltrados = computed(() => {
  const lista = autores.value ?? []
  const termo = filtroPesquisaAutor.value?.trim().toLowerCase() || ''
  if (!termo) return lista
  return lista.filter((a) => (a.nome || '').toLowerCase().includes(termo))
})

const editorasFiltradas = computed(() => {
  const lista = editoras.value ?? []
  const termo = filtroPesquisaEditora.value?.trim().toLowerCase() || ''
  if (!termo) return lista
  return lista.filter((e) => (e.nome || '').toLowerCase().includes(termo))
})

const categoriasFiltradas = computed(() => {
  const lista = categorias.value ?? []
  const termo = filtroPesquisaCategoria.value?.trim().toLowerCase() || ''
  if (!termo) return lista
  return lista.filter((c) => (c.nome || '').toLowerCase().includes(termo))
})

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

function preencherFormComLivro(livro) {
  if (!livro) {
    form.value = getFormDefault()
    return
  }

  form.value = {
    titulo: livro.titulo ?? '',
    descricao: livro.descricao ?? '',
    pontuacao: livro.pontuacao ?? null,
    qtd_paginas: livro.qtd_paginas ?? null,
    ano_publicacao: livro.ano_publicacao ?? null,
    qtd_disponivel: livro.qtd_disponivel ?? null,
    qtd_emprestados: livro.qtd_emprestados ?? null,
    idioma: livro.idioma ?? '',
    isbn: livro.isbn ?? '',
    ativo: livro.ativo ?? true,
    autor: livro.autor?.id ?? livro.autor ?? null,
    editora: livro.editora?.id ?? livro.editora ?? null,
    categoria: livro.categoria?.id ?? livro.categoria ?? null,
    imagemFile: null
  }
}

async function carregarOpcoes() {
  try {
    const [resAutores, resEditoras, resCategorias] = await Promise.all([
      livroService.autores.getAll(),
      livroService.editoras.getAll(),
      livroService.categorias.getAll()
    ])
    const listaAutores = Array.isArray(resAutores) ? resAutores : resAutores?.results ?? []
    opcoesAutores.value = listaAutores
    autores.value = listaAutores
    autoresTotal.value = resAutores?.count ?? listaAutores.length

    const listaEditoras = Array.isArray(resEditoras) ? resEditoras : resEditoras?.results ?? []
    opcoesEditoras.value = listaEditoras
    editoras.value = listaEditoras

    const listaCategorias = Array.isArray(resCategorias) ? resCategorias : resCategorias?.results ?? []
    opcoesCategorias.value = listaCategorias
    categorias.value = listaCategorias
  } catch (e) {
    console.error('Erro ao carregar opções:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao carregar dados',
      detail: 'Não foi possível carregar autores, editoras e categorias.',
      life: 5000
    })
  }
}

async function carregarAutores(params = {}) {
  loadingAutores.value = true
  try {
    const data = await livroService.autores.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    autores.value = list
    autoresTotal.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar autores:', e)
    autores.value = []
    toast.add({
      severity: 'error',
      summary: 'Erro ao carregar autores',
      detail: 'Não foi possível carregar a lista de autores.',
      life: 5000
    })
  } finally {
    loadingAutores.value = false
  }
}

const aplicarPesquisaAutor = () => {
  popoverPesquisaAutorRef.value?.hide()
}

const limparPesquisaAutor = () => {
  filtroPesquisaAutor.value = ''
  popoverPesquisaAutorRef.value?.hide()
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
    toast.add({
      severity: 'success',
      summary: 'Autor salvo',
      detail: 'Os dados do autor foram salvos com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao salvar autor:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao salvar autor',
      detail: 'Não foi possível salvar o autor.',
      life: 5000
    })
  }
}

function editarAutor(autor) {
  autorEditandoId.value = autor.id
  autorForm.value = { nome: autor.nome }
}

function abrirConfirmacaoExcluirAutor(autor) {
  autorParaExcluir.value = autor
  confirmDeleteAutorVisible.value = true
}

async function confirmarExclusaoAutor() {
  if (!autorParaExcluir.value) return
  confirmDeleteAutorLoading.value = true
  try {
    await livroService.autores.delete(autorParaExcluir.value.id)
    await carregarAutores()
    await carregarOpcoes()
    toast.add({
      severity: 'success',
      summary: 'Autor excluído',
      detail: 'O autor foi excluído com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao excluir autor:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao excluir autor',
      detail: 'Não foi possível excluir o autor.',
      life: 5000
    })
  } finally {
    confirmDeleteAutorLoading.value = false
    confirmDeleteAutorVisible.value = false
    autorParaExcluir.value = null
  }
}

function cancelarExclusaoAutor() {
  confirmDeleteAutorVisible.value = false
  autorParaExcluir.value = null
}

async function carregarEditoras() {
  loadingEditoras.value = true
  try {
    const data = await livroService.editoras.getAll()
    const list = Array.isArray(data) ? data : data?.results ?? []
    editoras.value = list
  } catch (e) {
    console.error('Erro ao carregar editoras:', e)
    editoras.value = []
    toast.add({
      severity: 'error',
      summary: 'Erro ao carregar editoras',
      detail: 'Não foi possível carregar a lista de editoras.',
      life: 5000
    })
  } finally {
    loadingEditoras.value = false
  }
}

function limparPesquisaEditora() {
  filtroPesquisaEditora.value = ''
}

async function salvarEditora() {
  if (!editoraForm.value.nome) return
  try {
    if (editoraEditandoId.value) {
      await livroService.editoras.update(editoraEditandoId.value, { nome: editoraForm.value.nome })
    } else {
      await livroService.editoras.create({ nome: editoraForm.value.nome })
    }
    editoraForm.value = { nome: '' }
    editoraEditandoId.value = null
    await carregarEditoras()
    await carregarOpcoes()
    toast.add({
      severity: 'success',
      summary: 'Editora salva',
      detail: 'Os dados da editora foram salvos com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao salvar editora:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao salvar editora',
      detail: 'Não foi possível salvar a editora.',
      life: 5000
    })
  }
}

function editarEditora(editora) {
  editoraEditandoId.value = editora.id
  editoraForm.value = { nome: editora.nome }
}

function abrirConfirmacaoExcluirEditora(editora) {
  editoraParaExcluir.value = editora
  confirmDeleteEditoraVisible.value = true
}

async function confirmarExclusaoEditora() {
  if (!editoraParaExcluir.value) return
  confirmDeleteEditoraLoading.value = true
  try {
    await livroService.editoras.delete(editoraParaExcluir.value.id)
    await carregarEditoras()
    await carregarOpcoes()
    toast.add({
      severity: 'success',
      summary: 'Editora excluída',
      detail: 'A editora foi excluída com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao excluir editora:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao excluir editora',
      detail: 'Não foi possível excluir a editora.',
      life: 5000
    })
  } finally {
    confirmDeleteEditoraLoading.value = false
    confirmDeleteEditoraVisible.value = false
    editoraParaExcluir.value = null
  }
}

function cancelarExclusaoEditora() {
  confirmDeleteEditoraVisible.value = false
  editoraParaExcluir.value = null
}

async function carregarCategorias() {
  loadingCategorias.value = true
  try {
    const data = await livroService.categorias.getAll()
    const list = Array.isArray(data) ? data : data?.results ?? []
    categorias.value = list
  } catch (e) {
    console.error('Erro ao carregar categorias:', e)
    categorias.value = []
    toast.add({
      severity: 'error',
      summary: 'Erro ao carregar categorias',
      detail: 'Não foi possível carregar a lista de categorias.',
      life: 5000
    })
  } finally {
    loadingCategorias.value = false
  }
}

function limparPesquisaCategoria() {
  filtroPesquisaCategoria.value = ''
}

async function salvarCategoria() {
  if (!categoriaForm.value.nome) return
  try {
    if (categoriaEditandoId.value) {
      await livroService.categorias.update(categoriaEditandoId.value, { nome: categoriaForm.value.nome })
    } else {
      await livroService.categorias.create({ nome: categoriaForm.value.nome })
    }
    categoriaForm.value = { nome: '' }
    categoriaEditandoId.value = null
    await carregarCategorias()
    await carregarOpcoes()
    toast.add({
      severity: 'success',
      summary: 'Categoria salva',
      detail: 'Os dados da categoria foram salvos com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao salvar categoria:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao salvar categoria',
      detail: 'Não foi possível salvar a categoria.',
      life: 5000
    })
  }
}

function editarCategoria(categoria) {
  categoriaEditandoId.value = categoria.id
  categoriaForm.value = { nome: categoria.nome }
}

function abrirConfirmacaoExcluirCategoria(categoria) {
  categoriaParaExcluir.value = categoria
  confirmDeleteCategoriaVisible.value = true
}

async function confirmarExclusaoCategoria() {
  if (!categoriaParaExcluir.value) return
  confirmDeleteCategoriaLoading.value = true
  try {
    await livroService.categorias.delete(categoriaParaExcluir.value.id)
    await carregarCategorias()
    await carregarOpcoes()
    toast.add({
      severity: 'success',
      summary: 'Categoria excluída',
      detail: 'A categoria foi excluída com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao excluir categoria:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao excluir categoria',
      detail: 'Não foi possível excluir a categoria.',
      life: 5000
    })
  } finally {
    confirmDeleteCategoriaLoading.value = false
    confirmDeleteCategoriaVisible.value = false
    categoriaParaExcluir.value = null
  }
}

function cancelarExclusaoCategoria() {
  confirmDeleteCategoriaVisible.value = false
  categoriaParaExcluir.value = null
}

watch(tabAtiva, (valor) => {
  if (valor === 'autor') carregarAutores()
  if (valor === 'editora') carregarEditoras()
  if (valor === 'categoria') carregarCategorias()
})

watch(
  () => props.livro,
  (novo) => {
    if (novo) {
      tabAtiva.value = 'livro'
      preencherFormComLivro(novo)
    } else {
      form.value = getFormDefault()
    }
  },
  { immediate: true }
)

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

.dialog-popover-pesquisa {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 18rem;
}

.dialog-popover-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
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
