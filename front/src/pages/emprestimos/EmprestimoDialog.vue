<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Novo empréstimo"
    :style="{ width: '36rem' }"
    :contentStyle="{ overflow: 'visible' }"
    @hide="limparFormulario"
    @show="carregarOpcoes"
  >
    <div class="dialog-body">
      <div class="dialog-row">
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <BaseSelect
              id="emp-leitor"
              v-model="form.leitor"
              :options="opcoesLeitores"
              optionLabel="nome"
              optionValue="id"
              showClear
              class="dialog-input"
            />
            <label for="emp-leitor">Leitor <span class="dialog-required">*</span></label>
          </FloatLabel>
        </div>
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <BaseSelect
              id="emp-livro"
              v-model="form.livro"
              :options="opcoesLivros"
              optionLabel="titulo"
              optionValue="id"
              showClear
              class="dialog-input"
            />
            <label for="emp-livro">Livro <span class="dialog-required">*</span></label>
          </FloatLabel>
        </div>
      </div>
      <div class="dialog-row">
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <DatePicker
              v-model="form.data_emprestimo"
              inputId="emp-data-emp"
              dateFormat="dd/mm/yy"
              showIcon
              iconDisplay="input"
              class="dialog-input"
            />
            <label for="emp-data-emp">Data de empréstimo</label>
          </FloatLabel>
        </div>
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <DatePicker
              v-model="form.data_devolucao"
              inputId="emp-data-dev"
              dateFormat="dd/mm/yy"
              showIcon
              iconDisplay="input"
              class="dialog-input"
            />
            <label for="emp-data-dev">Data de devolução</label>
          </FloatLabel>
        </div>
      </div>
      <div class="dialog-row dialog-row--acoes">
        <Button type="button" label="Salvar" size="small" :loading="salvando" @click="salvar" />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import Dialog from 'primevue/dialog'
import FloatLabel from 'primevue/floatlabel'
import DatePicker from 'primevue/datepicker'
import Button from 'primevue/button'
import BaseSelect from '@/components/BaseSelect.vue'
import leitorService from '@/services/leitorService'
import livroService from '@/services/livroService'

const props = defineProps({
  visible: { type: Boolean, default: false }
})

const emit = defineEmits(['update:visible', 'save'])

const visibleModel = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v)
})

const toast = useToast()
const form = ref(getFormDefault())
const opcoesLeitores = ref([])
const opcoesLivros = ref([])
const salvando = ref(false)

function getFormDefault() {
  return {
    leitor: null,
    livro: null,
    data_emprestimo: new Date(),
    data_devolucao: null
  }
}

function toDateOnly(val) {
  if (!val) return null
  const d = val instanceof Date ? val : new Date(val)
  if (isNaN(d.getTime())) return null
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

function limparFormulario() {
  form.value = getFormDefault()
}

async function carregarOpcoes() {
  try {
    const [dataLeitores, dataLivros] = await Promise.all([
      leitorService.leitores.getAll(),
      livroService.livros.getAll()
    ])
    opcoesLeitores.value = Array.isArray(dataLeitores) ? dataLeitores : dataLeitores?.results ?? []
    opcoesLivros.value = Array.isArray(dataLivros) ? dataLivros : dataLivros?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar opções:', e)
  }
}

async function salvar() {
  if (form.value.leitor == null || form.value.leitor === '') {
    toast.add({ severity: 'warn', summary: 'Campos obrigatórios', detail: 'Selecione o leitor.', life: 3000 })
    return
  }
  if (form.value.livro == null || form.value.livro === '') {
    toast.add({ severity: 'warn', summary: 'Campos obrigatórios', detail: 'Selecione o livro.', life: 3000 })
    return
  }
  salvando.value = true
  try {
    const dataEmp = form.value.data_emprestimo || new Date()
    const dataDev = form.value.data_devolucao
    const payload = {
      leitor: form.value.leitor,
      livro: form.value.livro,
      data_emprestimo: toDateOnly(dataEmp),
      data_devolucao: dataDev ? toDateOnly(dataDev) : null,
      devolvido: false
    }
    await leitorService.emprestimos.create(payload)
    toast.add({ severity: 'success', summary: 'Empréstimo cadastrado', detail: 'O empréstimo foi registrado com sucesso.', life: 3000 })
    emit('save')
    visibleModel.value = false
  } catch (e) {
    console.error('Erro ao salvar empréstimo:', e)
    const data = e?.response?.data
    let detail = 'Não foi possível salvar o empréstimo.'
    if (data) {
      if (Array.isArray(data.non_field_errors) && data.non_field_errors.length) {
        detail = data.non_field_errors[0]
      } else if (data.detail) {
        detail = Array.isArray(data.detail) ? data.detail[0] : data.detail
      } else {
        const firstKey = Object.keys(data)[0]
        const val = firstKey && data[firstKey]
        if (Array.isArray(val) && val.length) detail = val[0]
        else if (typeof val === 'string') detail = val
      }
    }
    toast.add({ severity: 'error', summary: 'Erro ao salvar empréstimo', detail, life: 5000 })
  } finally {
    salvando.value = false
  }
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

.dialog-row {
  display: flex;
  gap: 1rem;
}

.dialog-row .dialog-field {
  flex: 1;
  margin-bottom: 1rem;
}

.dialog-field {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.dialog-input-wrap {
  flex: 1;
  min-width: 0;
  width: 100%;
}

.dialog-input {
  flex: 1;
  width: 100%;
}

.dialog-row--acoes {
  margin-top: 0.5rem;
  margin-bottom: 0;
}

.dialog-required {
  color: var(--p-danger);
}
</style>
