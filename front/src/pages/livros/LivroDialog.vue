<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Incluir livro"
    :style="{ width: '65rem' }"
    @hide="limparFormulario"
    @show="carregarOpcoes"
  >
    <div class="dialog-body">
      <div class="dialog-field">
        <label for="livro-titulo" class="dialog-label">Título</label>
        <InputText id="livro-titulo" v-model="form.titulo" class="dialog-input" autocomplete="off" />
      </div>

      <div class="dialog-field dialog-field--vertical">
        <label for="livro-descricao" class="dialog-label">Descrição</label>
        <Textarea id="livro-descricao" v-model="form.descricao" class="dialog-input" rows="3" autoResize />
      </div>

      <div class="dialog-row">
        <div class="dialog-field">
          <label for="livro-autor" class="dialog-label">Autor</label>
          <Select
            id="livro-autor"
            v-model="form.autor"
            :options="opcoesAutores"
            optionLabel="nome"
            optionValue="id"
            placeholder="Selecione"
            class="dialog-input"
            showClear
            editable
          />
        </div>
        <div class="dialog-field">
          <label for="livro-editora" class="dialog-label">Editora</label>
          <Select
            id="livro-editora"
            v-model="form.editora"
            :options="opcoesEditoras"
            optionLabel="nome"
            optionValue="id"
            placeholder="Selecione"
            class="dialog-input"
            showClear
            editable
          />
        </div>
      </div>

      <div class="dialog-field">
        <label for="livro-categoria" class="dialog-label">Categoria</label>
        <Select
          id="livro-categoria"
          v-model="form.categoria"
          :options="opcoesCategorias"
          optionLabel="nome"
          optionValue="id"
          placeholder="Selecione"
          class="dialog-input"
          showClear
          editable
        />
      </div>

      <div class="dialog-row">
        <div class="dialog-field">
          <label for="livro-qtd-paginas" class="dialog-label">Qtd. páginas</label>
          <InputNumber id="livro-qtd-paginas" v-model="form.qtd_paginas" class="dialog-input" :min="1" showButtons />
        </div>
        <div class="dialog-field">
          <label for="livro-ano" class="dialog-label">Ano publicação</label>
          <InputNumber id="livro-ano" v-model="form.ano_publicacao" class="dialog-input" :min="1900" :max="anoAtual" showButtons />
        </div>
      </div>

      <div class="dialog-row">
        <div class="dialog-field">
          <label for="livro-qtd-disponivel" class="dialog-label">Qtd. disponível</label>
          <InputNumber id="livro-qtd-disponivel" v-model="form.qtd_disponivel" class="dialog-input" :min="0" showButtons />
        </div>
        <div class="dialog-field">
          <label for="livro-qtd-emprestados" class="dialog-label">Qtd. emprestados</label>
          <InputNumber id="livro-qtd-emprestados" v-model="form.qtd_emprestados" class="dialog-input" :min="0" showButtons />
        </div>
      </div>

      <div class="dialog-row">
        <div class="dialog-field">
          <label for="livro-pontuacao" class="dialog-label">Pontuação</label>
          <InputNumber id="livro-pontuacao" v-model="form.pontuacao" class="dialog-input" :min="0" showButtons />
        </div>
        <div class="dialog-field">
          <label for="livro-idioma" class="dialog-label">Idioma</label>
          <InputText id="livro-idioma" v-model="form.idioma" class="dialog-input" autocomplete="off" />
        </div>
      </div>

      <div class="dialog-field">
        <label for="livro-isbn" class="dialog-label">ISBN</label>
        <InputText id="livro-isbn" v-model="form.isbn" class="dialog-input" maxlength="13" autocomplete="off" />
      </div>

      <div class="dialog-field dialog-field--checkbox">
        <Checkbox id="livro-ativo" v-model="form.ativo" :binary="true" inputId="livro-ativo" />
        <label for="livro-ativo" class="dialog-label-inline">Ativo</label>
      </div>

      <div class="dialog-field dialog-field--vertical">
        <label class="dialog-label">Imagem</label>
        <FileUpload
          mode="basic"
          accept="image/*"
          :maxFileSize="2000000"
          chooseLabel="Escolher imagem"
          @select="onImagemSelect"
        />
        <small v-if="form.imagemFile" class="dialog-file-name">{{ form.imagemFile.name }}</small>
      </div>
    </div>

    <template #footer>
      <div class="dialog-actions">
        <Button type="button" label="Cancelar" severity="secondary" @click="fechar" />
        <Button type="button" label="Salvar" @click="salvar" />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import FileUpload from 'primevue/fileupload'
import Button from 'primevue/button'
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
    opcoesAutores.value = Array.isArray(autores) ? autores : autores?.results ?? []
    opcoesEditoras.value = Array.isArray(editoras) ? editoras : editoras?.results ?? []
    opcoesCategorias.value = Array.isArray(categorias) ? categorias : categorias?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar opções:', e)
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
  max-height: 70vh;
  overflow-y: auto;
}

.dialog-field {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.dialog-field--vertical {
  flex-direction: column;
  align-items: stretch;
}

.dialog-field--vertical .dialog-label {
  width: auto;
}

.dialog-field--checkbox {
  align-items: center;
}

.dialog-row {
  display: flex;
  gap: 1rem;
}

.dialog-row .dialog-field {
  flex: 1;
  margin-bottom: 1rem;
}

.dialog-label {
  font-weight: 600;
  width: 7rem;
  flex-shrink: 0;
  color: var(--texto-primario);
}

.dialog-label-inline {
  font-weight: 600;
  color: var(--texto-primario);
  margin-left: 0.5rem;
}

.dialog-input {
  flex: 1;
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
</style>
