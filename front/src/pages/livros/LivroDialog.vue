<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Incluir livro"
    :style="{ width: '65rem' }"
    :contentStyle="{ overflow: 'visible' }"
    @hide="limparFormulario"
    @show="carregarOpcoes"
  >
    <div class="dialog-body">
      <div class="dialog-row"></div>

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


      <div class="dialog-field dialog-field--vertical">
        <FloatLabel variant="on" class="dialog-input-wrap">
          <Textarea id="livro-descricao" v-model="form.descricao" class="dialog-input" rows="3" autoResize />
          <label for="livro-descricao">Descrição</label>
        </FloatLabel>
      </div>


      <!-- Categoria -->
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

      <!-- Qtd. páginas | Ano publicação -->
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
      </div>

      <!-- Qtd. disponível | Qtd. emprestados -->
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
      </div>

      <!-- Pontuação | Idioma -->
      <div class="dialog-row">
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <InputNumber id="livro-pontuacao" v-model="form.pontuacao" class="dialog-input" :min="0" showButtons />
            <label for="livro-pontuacao">Pontuação</label>
          </FloatLabel>
        </div>
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <InputText id="livro-idioma" v-model="form.idioma" class="dialog-input" autocomplete="off" />
            <label for="livro-idioma">Idioma</label>
          </FloatLabel>
        </div>
      </div>

      <!-- ISBN -->
      <div class="dialog-field">
        <FloatLabel variant="on" class="dialog-input-wrap">
          <InputText id="livro-isbn" v-model="form.isbn" class="dialog-input" maxlength="13" autocomplete="off" />
          <label for="livro-isbn">ISBN</label>
        </FloatLabel>
      </div>

      <!-- Ativo -->
      <div class="dialog-field dialog-field--checkbox">
        <FloatLabel variant="on" class="dialog-input-wrap dialog-input-wrap--inline">
          <Checkbox id="livro-ativo" v-model="form.ativo" :binary="true" inputId="livro-ativo" />
          <label for="livro-ativo">Ativo</label>
        </FloatLabel>
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
import FloatLabel from 'primevue/floatlabel'
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
  overflow: visible;
}

.dialog-field {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
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
}

.dialog-input-wrap :deep(.p-floatlabel) {
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

.dialog-row {
  display: flex;
  gap: 1rem;
}

.dialog-row .dialog-field {
  flex: 1;
  margin-bottom: 1rem;
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
