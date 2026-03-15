<template>
  <div class="page">
    <h1 class="page-title">Leitores</h1>
    <p class="page-subtitle">Gerencie os leitores da biblioteca.</p>

    <BaseDataTable
      :items="leitores"
      :loading="loading"
      :dataKey="dataKey"
      :totalRecords="totalRecords"
      :rows="rows"
      :lazy="lazy"
      :reorderableColumns="reorderableColumns"
    >
      <template #toolbar>
        <div class="table-toolbar" style="margin-top: 1rem;">
          <Button label="Buscar" size="small" icon="pi pi-search" @click="(e) => popoverBuscaRef?.toggle(e)" />
          <Button label="Incluir" size="small" icon="pi pi-plus" @click="incluir" />
        </div>

        <Popover ref="popoverBuscaRef" :style="{ width: '35%' }">
          <div class="filtro-popover">
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo">
                <InputText id="filtro-nome" v-model="filtroNome" class="w-full" />
                <label for="filtro-nome">Nome</label>
              </FloatLabel>
              <FloatLabel class="filtro-campo">
                <InputText id="filtro-email" v-model="filtroEmail" class="w-full" />
                <label for="filtro-email">E-mail</label>
              </FloatLabel>
            </div>
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo">
                <InputText id="filtro-cpf" v-model="filtroCpf" class="w-full" />
                <label for="filtro-cpf">CPF</label>
              </FloatLabel>
              <FloatLabel class="filtro-campo">
                <InputText id="filtro-telefone" v-model="filtroTelefone" class="w-full" />
                <label for="filtro-telefone">Telefone</label>
              </FloatLabel>
            </div>
            <div class="filtro-linha">
              <div class="filtro-switches">
                <div class="filtro-switch">
                  <Checkbox v-model="filtroAtivo" :binary="true" inputId="filtro-ativo" />
                  <label for="filtro-ativo">Apenas ativos</label>
                </div>
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
        <Column field="nome" header="Nome" :style="{ width: '200px', maxWidth: '200px' }" />
        <Column field="email" header="E-mail" />
        <Column header="Telefone">
          <template #body="slotProps">
            {{ formatarTelefone(slotProps.data.telefone) }}
          </template>
        </Column>
            <Column field="pontuacao_atual" header="Pontuação" :style="{ width: '100px', maxWidth: '100px' }" />
        <Column header="Ativo" :style="{ width: '90px', maxWidth: '90px' }">
          <template #body="slotProps">
            <span v-if="slotProps.data.ativo" class="p-tag p-tag-success">Sim</span>
            <span v-else class="p-tag p-tag-danger">Não</span>
          </template>
        </Column>
        <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }">
          <template #body="slotProps">
            <div class="col-acoes">
              <Button label="Editar" size="small" @click="editarLeitor(slotProps.data)" />
              <Button label="Excluir" severity="danger" size="small" @click="excluirLeitor(slotProps.data)" />
            </div>
          </template>
        </Column>
      </template>
    </BaseDataTable>

    <LeitorDialog v-model:visible="dialogVisible" :leitor="leitorEditando" @save="onLeitorSalvo" @hide="aoFecharDialog" />

    <BaseConfirmDialog
      :visible="confirmDeleteVisible"
      title="Excluir leitor"
      :message="confirmDeleteMessage"
      confirmLabel="Excluir"
      cancelLabel="Cancelar"
      confirmSeverity="danger"
      :loading="confirmDeleteLoading"
      @update:visible="(v) => (confirmDeleteVisible = v)"
      @confirm="confirmarExclusao"
      @cancel="cancelarExclusao"
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
import Checkbox from 'primevue/checkbox'
import LeitorDialog from './LeitorDialog.vue'
import leitorService from '@/services/leitorService'
import { PAGE_SIZE } from '@/constants/pagination'

const leitores = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const leitorEditando = ref(null)
const dataKey = 'id'
const totalRecords = ref(0)
const rows = PAGE_SIZE
const lazy = ref(false)
const reorderableColumns = false

const popoverBuscaRef = ref(null)
const filtroNome = ref('')
const filtroEmail = ref('')
const filtroCpf = ref('')
const filtroTelefone = ref('')
const filtroAtivo = ref(false)

const confirmDeleteVisible = ref(false)
const confirmDeleteLoading = ref(false)
const leitorParaExcluir = ref(null)

const confirmDeleteMessage = computed(() => {
  if (!leitorParaExcluir.value) return 'Confirma a exclusão deste leitor?'
  return `Excluir o leitor ${leitorParaExcluir.value.nome}?`
})

const toast = useToast()

function formatarTelefone(val) {
  if (!val) return ''
  const digits = String(val).replace(/\D/g, '')
  if (digits.length === 11) return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`
  if (digits.length === 10) return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`
  return val
}

async function carregarLeitores(params = {}) {
  loading.value = true
  try {
    const data = await leitorService.leitores.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    leitores.value = list
    totalRecords.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar leitores:', e)
    leitores.value = []
  } finally {
    loading.value = false
  }
}

function montarParametrosBusca() {
  const params = {}
  if (filtroNome.value?.trim()) params['nome__icontains'] = filtroNome.value.trim()
  if (filtroEmail.value?.trim()) params['email__icontains'] = filtroEmail.value.trim()
  if (filtroCpf.value?.trim()) params['cpf__icontains'] = filtroCpf.value.trim()
  if (filtroTelefone.value?.trim()) params['telefone__icontains'] = filtroTelefone.value.trim()
  if (filtroAtivo.value) params['ativo'] = true
  return params
}

async function aplicarFiltros() {
  const params = montarParametrosBusca()
  await carregarLeitores(params)
  popoverBuscaRef.value?.hide()
}

async function limparFiltros() {
  filtroNome.value = ''
  filtroEmail.value = ''
  filtroCpf.value = ''
  filtroTelefone.value = ''
  filtroAtivo.value = false
  await carregarLeitores()
  popoverBuscaRef.value?.hide()
}

function incluir() {
  leitorEditando.value = null
  dialogVisible.value = true
}

async function aoFecharDialog() {
  await carregarLeitores(montarParametrosBusca())
}

async function onLeitorSalvo(payload) {
  try {
    if (leitorEditando.value?.id) {
      await leitorService.leitores.update(leitorEditando.value.id, payload)
      toast.add({ severity: 'success', summary: 'Leitor atualizado', detail: 'Os dados do leitor foram salvos com sucesso.', life: 3000 })
    } else {
      await leitorService.leitores.create(payload)
      toast.add({ severity: 'success', summary: 'Leitor cadastrado', detail: 'O leitor foi cadastrado com sucesso.', life: 3000 })
    }
    await carregarLeitores()
  } catch (e) {
    console.error('Erro ao salvar leitor:', e)
    const detail = e?.response?.data ? (typeof e.response.data === 'object' ? Object.entries(e.response.data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`).join(' | ') : e.response.data) : 'Não foi possível salvar o leitor.'
    toast.add({ severity: 'error', summary: 'Erro ao salvar leitor', detail, life: 5000 })
  }
}

async function editarLeitor(leitor) {
  if (!leitor?.id) return
  loading.value = true
  try {
    const completo = await leitorService.leitores.getById(leitor.id)
    leitorEditando.value = completo
    dialogVisible.value = true
  } catch (e) {
    console.error('Erro ao carregar leitor:', e)
    toast.add({ severity: 'error', summary: 'Erro', detail: 'Não foi possível carregar os dados do leitor.', life: 5000 })
  } finally {
    loading.value = false
  }
}

function excluirLeitor(leitor) {
  leitorParaExcluir.value = leitor
  confirmDeleteVisible.value = true
}

async function confirmarExclusao() {
  if (!leitorParaExcluir.value) return
  confirmDeleteLoading.value = true
  try {
    await leitorService.leitores.delete(leitorParaExcluir.value.id)
    leitores.value = leitores.value.filter((l) => l.id !== leitorParaExcluir.value.id)
    totalRecords.value = Math.max(0, totalRecords.value - 1)
    toast.add({
      severity: 'success',
      summary: 'Leitor excluído',
      detail: 'O leitor foi excluído com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao excluir leitor:', e)
    toast.add({
      severity: 'error',
      summary: 'Erro ao excluir leitor',
      detail: 'Não foi possível excluir o leitor.',
      life: 5000
    })
  } finally {
    confirmDeleteLoading.value = false
    confirmDeleteVisible.value = false
    leitorParaExcluir.value = null
  }
}

function cancelarExclusao() {
  confirmDeleteVisible.value = false
  leitorParaExcluir.value = null
}

onMounted(() => {
  carregarLeitores()
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
  min-width: 28rem;
}

.filtro-linha {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
  margin-bottom: 0.5rem;
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
