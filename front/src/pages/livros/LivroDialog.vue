<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Incluir Informações do Livro"
    :style="{ width: '65rem' }"
    :contentStyle="{ overflowY: 'auto', maxHeight: '100vh' }"
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
                    <InputText
                      id="livro-isbn"
                      v-model="form.isbn"
                      class="dialog-input"
                      maxlength="13"
                      autocomplete="off"
                      @blur="buscarLivroPorIsbn"
                    />
                    <label for="livro-isbn">ISBN</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="livro-titulo" v-model="form.titulo" class="dialog-input" autocomplete="off" />
                    <label for="livro-titulo">Título</label>
                  </FloatLabel>
                </div>

                <div class="dialog-field dialog-multiselect-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <MultiSelect
                      id="livro-autores"
                      v-model="form.autores"
                      :options="autores"
                      optionLabel="nome"
                      optionValue="id"
                      class="dialog-input dialog-input--multiselect"
                      display="chip"
                      showClear
                      filter
                    />
                    <label for="livro-autores">Autores</label>
                  </FloatLabel>
                </div>

                
              </div>

              <div class="dialog-field dialog-field--vertical">
                <FloatLabel variant="on" class="dialog-input-wrap">
                  <Textarea
                    id="livro-descricao"
                    v-model="form.descricao"
                    class="dialog-input dialog-input--descricao"
                    rows="3"
                  />
                  <label for="livro-descricao">Descrição</label>
                </FloatLabel>
              </div>

              <!-- Categoria / Idioma / ISBN -->
              <div class="dialog-row">
                <div class="dialog-field" @click="onEditoraSelectAreaClick">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <Select
                      ref="selectEditoraRef"
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
                <div class="dialog-field dialog-multiselect-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <MultiSelect
                      id="livro-categorias"
                      v-model="form.categorias"
                      :options="opcoesCategorias"
                      optionLabel="nome"
                      optionValue="id"
                      class="dialog-input dialog-input--multiselect"
                      display="chip"
                      showClear
                      filter
                    />
                    <label for="livro-categorias">Categorias</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="livro-idioma" v-model="form.idioma" class="dialog-input" autocomplete="off" />
                    <label for="livro-idioma">Idioma</label>
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
                    <InputNumber
                    id="livro-ano"
                    v-model="form.ano_publicacao"
                    class="dialog-input"
                    :min="1900"
                    :max="anoAtual"
                    :useGrouping="false"
                    showButtons
                  />
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

              <!-- Qtd. total (editável) | Qtd. disponível (calculado) | Qtd. emprestados (calculado) | Ativo -->
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber
                      id="livro-qtd-total"
                      v-model="form.qtd_total"
                      class="dialog-input"
                      :min="0"
                      showButtons
                      :useGrouping="false"
                    />
                    <label for="livro-qtd-total">Qtd. total</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber
                      id="livro-qtd-disponivel"
                      v-model="form.qtd_disponivel"
                      class="dialog-input"
                      :min="0"
                      :useGrouping="false"
                      disabled
                    />
                    <label for="livro-qtd-disponivel">Qtd. disponível</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber
                      id="livro-qtd-emprestados"
                      v-model="form.qtd_emprestados"
                      class="dialog-input"
                      :min="0"
                      :useGrouping="false"
                      disabled
                    />
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
                <div class="dialog-row dialog-row--imagem">
                  <div class="dialog-field dialog-field--imagem-url">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText
                        id="livro-imagem-url"
                        v-model="form.imagem_url"
                        class="dialog-input"
                        autocomplete="off"
                        placeholder="https://exemplo.com/capa.jpg"
                      />
                      <label for="livro-imagem-url">URL da imagem (opcional)</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-field--imagem-atual-btn">
                    <Button
                      type="button"
                      label="Imagem atual"
                      :disabled="!imagemExistente"
                      @click="abrirImagemAtual"
                    />
                  </div>
                  <div class="dialog-field dialog-field--imagem-upload">
                    <FileUpload
                      mode="basic"
                      accept="image/*"
                      :maxFileSize="2000000"
                      chooseLabel="Escolher imagem"
                      style="margin-left: -12rem;"
                      @select="onImagemSelect"
                    />
                  </div>
                </div>
              </div>

              <div class="dialog-actions dialog-actions--inside-tab">
                <Button type="button" label="Salvar" size="small" @click="salvar" />
              </div>
            </div>
          </TabPanel>

          <TabPanel value="autor">
            <div class="dialog-autor">
              <div class="dialog-row dialog-autor-row" style="margin-top: 1rem;">
                <div class="dialog-field dialog-autor-field" >
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
                :totalRecords="autoresTotal"
                :rows="autoresRows"
                :first="firstAutores"
                :lazy="true"
                :reorderableColumns="false"
                class="dialog-autor-table"
                @page="onPageAutores"
              >
                <template #columns>
                  <Column field="nome" header="Autor" sortable />
                  <Column
                    header="Ações"
                    :style="{ width: '180px', maxWidth: '180px' }"
                    bodyClass="dialog-col-acoes"
                    headerClass="dialog-col-acoes"
                  >
                    <template #body="slotProps">
                      <div class="dialog-col-acoes">
                        <Button
                          v-if="hasPermission('livros.change_autor')"
                          label="Editar"
                          size="small"
                          @click="editarAutor(slotProps.data)"
                        />
                        <Button
                          v-if="hasPermission('livros.delete_autor')"
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
              <div class="dialog-row dialog-autor-row" style="margin-top: 1rem;">
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
                :totalRecords="editorasTotal"
                :rows="editorasRows"
                :first="firstEditoras"
                :lazy="true"
                :reorderableColumns="false"
                class="dialog-autor-table"
                @page="onPageEditoras"
              >
                <template #columns>
                  <Column field="nome" header="Editora" sortable />
                  <Column
                    header="Ações"
                    :style="{ width: '180px', maxWidth: '180px' }"
                    bodyClass="dialog-col-acoes"
                    headerClass="dialog-col-acoes"
                  >
                    <template #body="slotProps">
                      <div class="dialog-col-acoes">
                        <Button
                          v-if="hasPermission('livros.change_editora')"
                          label="Editar"
                          size="small"
                          @click="editarEditora(slotProps.data)"
                        />
                        <Button
                          v-if="hasPermission('livros.delete_editora')"
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
              <div class="dialog-row dialog-autor-row" style="margin-top: 1rem;">
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
                :totalRecords="categoriasTotal"
                :rows="categoriasRows"
                :first="firstCategorias"
                :lazy="true"
                :reorderableColumns="false"
                class="dialog-autor-table"
                @page="onPageCategorias"
              >
                <template #columns>
                  <Column field="nome" header="Categoria" sortable />
                  <Column
                    header="Ações"
                    :style="{ width: '180px', maxWidth: '180px' }"
                    bodyClass="dialog-col-acoes"
                    headerClass="dialog-col-acoes"
                  >
                    <template #body="slotProps">
                      <div class="dialog-col-acoes">
                        <Button
                          v-if="hasPermission('livros.change_categoria')"
                          label="Editar"
                          size="small"
                          @click="editarCategoria(slotProps.data)"
                        />
                        <Button
                          v-if="hasPermission('livros.delete_categoria')"
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
  <Dialog
    v-model:visible="imagemDialogVisible"
    modal
    header="Imagem atual do livro"
    :style="{ width: '26rem' }"
    :contentStyle="{ overflowY: 'auto', maxHeight: '100vh' }"
  >
    <div class="dialog-imagem-atual-wrap" v-if="imagemExistente">
      <img :src="imagemExistente" alt="Imagem atual do livro" class="dialog-imagem-atual" />
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import Dialog from 'primevue/dialog'

const store = useStore()
const hasPermission = (perm) => store.getters.hasPermission(perm)
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import MultiSelect from 'primevue/multiselect'
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
const firstAutores = ref(0)
const autoresRows = 10
const autorEditandoId = ref(null)
const autorForm = ref({ nome: '' })
const tabAtiva = ref('livro')
const popoverPesquisaAutorRef = ref(null)
const filtroPesquisaAutor = ref('')
const selectAutorRef = ref(null)
const selectEditoraRef = ref(null)

const confirmDeleteAutorVisible = ref(false)
const confirmDeleteAutorLoading = ref(false)
const autorParaExcluir = ref(null)

const confirmDeleteAutorMessage = computed(() => {
  if (!autorParaExcluir.value) return 'Confirma a exclusão deste autor?'
  return `Excluir o autor ${autorParaExcluir.value.nome}?`
})

const editoras = ref([])
const loadingEditoras = ref(false)
const editorasTotal = ref(0)
const firstEditoras = ref(0)
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
const categoriasTotal = ref(0)
const firstCategorias = ref(0)
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
const loadingIsbn = ref(false)

const imagemDialogVisible = ref(false)

const imagemExistente = computed(() => {
  const livro = props.livro
  if (!livro) return null
  return livro.imagem || livro.imagem_url || null
})

function abrirImagemAtual() {
  if (!imagemExistente.value) return
  imagemDialogVisible.value = true
}

function onAutorSelectAreaClick(e) {
  const t = e.target
  const isInput = t.tagName === 'INPUT'
  const isComboboxSpan = t.tagName === 'SPAN' && t.getAttribute('role') === 'combobox'
  if (isInput || isComboboxSpan) selectAutorRef.value?.show(true)
}

function onEditoraSelectAreaClick(e) {
  const t = e.target
  const isInput = t.tagName === 'INPUT'
  const isComboboxSpan = t.tagName === 'SPAN' && t.getAttribute('role') === 'combobox'
  if (isInput || isComboboxSpan) selectEditoraRef.value?.show(true)
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
    qtd_total: 1,
    qtd_disponivel: null,
    qtd_emprestados: null,
    idioma: '',
    isbn: '',
    ativo: true,
    autores: [],
    editora: null,
    categorias: [],
    imagemFile: null,
    imagem_url: ''
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
    qtd_total: livro.qtd_total ?? 1,
    qtd_disponivel: livro.qtd_disponivel ?? null,
    qtd_emprestados: livro.qtd_emprestados ?? null,
    idioma: livro.idioma ?? '',
    isbn: livro.isbn ?? '',
    ativo: livro.ativo ?? true,
    autores: Array.isArray(livro.autores) ? livro.autores : [],
    editora: livro.editora?.id ?? livro.editora ?? null,
    categorias: Array.isArray(livro.categorias) ? livro.categorias : [],
    imagemFile: null,
    imagem_url: livro.imagem_url ?? ''
  }
}

async function carregarOpcoes() {
  try {
    firstAutores.value = 0
    firstEditoras.value = 0
    firstCategorias.value = 0
    const [resAutores, resEditoras, resCategorias] = await Promise.all([
      livroService.autores.getAll({ page: 1, page_size: autoresRows }),
      livroService.editoras.getAll({ page: 1, page_size: editorasRows }),
      livroService.categorias.getAll({ page: 1, page_size: categoriasRows })
    ])
    const listaAutores = Array.isArray(resAutores) ? resAutores : resAutores?.results ?? []
    opcoesAutores.value = listaAutores
    autores.value = listaAutores
    autoresTotal.value = resAutores?.count ?? listaAutores.length

    const listaEditoras = Array.isArray(resEditoras) ? resEditoras : resEditoras?.results ?? []
    opcoesEditoras.value = listaEditoras
    editoras.value = listaEditoras
    editorasTotal.value = resEditoras?.count ?? listaEditoras.length

    const listaCategorias = Array.isArray(resCategorias) ? resCategorias : resCategorias?.results ?? []
    opcoesCategorias.value = listaCategorias
    categorias.value = listaCategorias
    categoriasTotal.value = resCategorias?.count ?? listaCategorias.length
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

function normalizarIsbn(valor) {
  if (!valor || typeof valor !== 'string') return ''
  return valor.replace(/\D/g, '').slice(0, 13)
}

async function buscarLivroPorIsbn() {
  const isbnLimpo = normalizarIsbn(form.value.isbn)
  if (!isbnLimpo) return

  loadingIsbn.value = true
  try {
    const data = await livroService.livros.consultarIsbn(isbnLimpo)
    if (!data) {
      toast.add({
        severity: 'warn',
        summary: 'Livro não encontrado',
        detail: 'Nenhum livro encontrado para este ISBN.',
        life: 4000
      })
      return
    }

    // Título
    if (!form.value.titulo) {
      form.value.titulo = data.titulo || form.value.titulo
    }

    // Número de páginas
    if (!form.value.qtd_paginas && data.qtd_paginas) {
      form.value.qtd_paginas = data.qtd_paginas
    }

    // Ano de publicação
    if (!form.value.ano_publicacao && data.ano_publicacao) {
      form.value.ano_publicacao = data.ano_publicacao
    }

    // Capa (URL da Open Library; por padrão o backend envia large)
    if (data.imagem_url) {
      form.value.imagem_url = data.imagem_url
    }

    // Editora (backend já garante existência e devolve id)
    if (!form.value.editora && data.editora_id) {
      form.value.editora = data.editora_id
      firstEditoras.value = 0
      await carregarEditoras({ page: 1, page_size: editorasRows })
      // garante que o Select de editora conheça a nova opção
      opcoesEditoras.value = editoras.value ?? []
    }

    // Autores (backend já garante existência e devolve ids)
    if (Array.isArray(data.autores_ids) && data.autores_ids.length > 0) {
      form.value.autores = data.autores_ids
      firstAutores.value = 0
      await carregarAutores({ page: 1, page_size: autoresRows })
    }

    // Descrição e idioma (quando vêm da Open Library)
    if (!form.value.descricao && data.descricao) {
      form.value.descricao = data.descricao
    }
    if (!form.value.idioma && data.idioma) {
      form.value.idioma = data.idioma
    }

    toast.add({
      severity: 'success',
      summary: 'Dados carregados pelo ISBN',
      detail: 'Informações do livro preenchidas a partir do backend.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao buscar livro por ISBN:', e)
    const backendMsg = e?.response?.data?.detail
    const msg = backendMsg || e?.message || 'Erro ao consultar dados do livro pelo ISBN.'
    toast.add({
      severity: 'error',
      summary: 'Erro ao buscar ISBN',
      detail: msg,
      life: 5000
    })
  } finally {
    loadingIsbn.value = false
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
    firstAutores.value = 0
    await carregarAutores({ page: 1, page_size: autoresRows })
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
    firstAutores.value = 0
    await carregarAutores({ page: 1, page_size: autoresRows })
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

function onPageAutores(event) {
  firstAutores.value = event.first
  carregarAutores({ page: event.page + 1, page_size: event.rows })
}

async function carregarEditoras(params = {}) {
  loadingEditoras.value = true
  try {
    const data = await livroService.editoras.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    editoras.value = list
    editorasTotal.value = data?.count ?? list.length
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

function onPageEditoras(event) {
  firstEditoras.value = event.first
  carregarEditoras({ page: event.page + 1, page_size: event.rows })
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
    firstEditoras.value = 0
    await carregarEditoras({ page: 1, page_size: editorasRows })
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
    firstEditoras.value = 0
    await carregarEditoras({ page: 1, page_size: editorasRows })
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

async function carregarCategorias(params = {}) {
  loadingCategorias.value = true
  try {
    const data = await livroService.categorias.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    categorias.value = list
    categoriasTotal.value = data?.count ?? list.length
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

function onPageCategorias(event) {
  firstCategorias.value = event.first
  carregarCategorias({ page: event.page + 1, page_size: event.rows })
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
    firstCategorias.value = 0
    await carregarCategorias({ page: 1, page_size: categoriasRows })
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
    firstCategorias.value = 0
    await carregarCategorias({ page: 1, page_size: categoriasRows })
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
  if (valor === 'autor') {
    firstAutores.value = 0
    carregarAutores({ page: 1, page_size: autoresRows })
  }
  if (valor === 'editora') {
    firstEditoras.value = 0
    carregarEditoras({ page: 1, page_size: editorasRows })
  }
  if (valor === 'categoria') {
    firstCategorias.value = 0
    carregarCategorias({ page: 1, page_size: categoriasRows })
  }
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
    qtd_total: form.value.qtd_total ?? 1,
    idioma: form.value.idioma || null,
    isbn: form.value.isbn || null,
    ativo: form.value.ativo ?? true,
    autores: form.value.autores ?? [],
    editora: form.value.editora ?? null,
    categorias: form.value.categorias ?? [],
    imagem_url: form.value.imagem_url || null
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
  /* evita que tab com datatable gigante estoure a altura do Dialog */
  max-height: 32rem;
  overflow-y: auto;
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

.dialog-row--imagem {
  align-items: flex-end;
  gap: 0.5rem;
}

.dialog-field--imagem-url {
  flex: 2;
}

.dialog-field--imagem-upload {
  flex: 0 0 auto;
}

.dialog-field--imagem-atual-btn {
  flex: 0 0 auto;
}

.dialog-imagem-atual-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-imagem-atual {
  max-width: 100%;
  max-height: 360px;
  border-radius: 8px;
  object-fit: contain;
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

/* Descrição: altura fixa com rolagem interna */
.dialog-input--descricao {
  min-height: 5rem;
  max-height: 8rem;
  overflow-y: auto;
}

/* MultiSelect: altura fixa para não crescer ao adicionar muitos itens (chips) */
.dialog-multiselect-field :deep(.p-multiselect) {
  min-height: 2.5rem;
  max-height: 7rem;
  overflow: hidden;
}

.dialog-multiselect-field :deep(.p-multiselect-label-container) {
  overflow-y: auto;
  min-height: 0;
  flex: 1 1 0;
  min-width: 0;
}

.dialog-multiselect-field :deep(.p-multiselect-label) {
  flex-wrap: wrap;
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
