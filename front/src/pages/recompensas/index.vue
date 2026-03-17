<template>
  <div class="page">
    <h1 class="page-title">Recompensas</h1>
    <p class="page-subtitle">Gerencie as recompensas disponíveis para leitores.</p>

    <BaseDataTable
      :items="recompensas"
      :loading="loading"
      :dataKey="dataKey"
      :totalRecords="totalRecords"
      :rows="rows"
      :first="first"
      :lazy="lazy"
      :reorderableColumns="reorderableColumns"
      @page="onPage"
    >
      <template #toolbar>
        <div class="table-toolbar" style="margin-top: 1rem;">
          <Button v-if="hasPermission('leitor.view_recompensa')" label="Buscar" size="small" icon="pi pi-search" @click="(e) => popoverBuscaRef?.toggle(e)" />
          <Button v-if="hasPermission('leitor.add_recompensa')" label="Incluir" size="small" icon="pi pi-plus" @click="abrirDialogIncluir" />
        </div>

        <Popover ref="popoverBuscaRef" :style="{ width: '35%' }">
          <div class="filtro-popover">
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo filtro-campo--full">
                <InputText id="filtro-nome" v-model="filtroNome" class="w-full" placeholder="Buscar por nome" />
                <label for="filtro-nome">Nome</label>
              </FloatLabel>
            </div>
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo">
                <InputNumber
                  id="filtro-pontuacao-min"
                  v-model="filtroPontuacaoMin"
                  :min="0"
                  class="w-full"
                />
                <label for="filtro-pontuacao-min">Pontuação mín.</label>
              </FloatLabel>
              <FloatLabel class="filtro-campo">
                <InputNumber
                  id="filtro-pontuacao-max"
                  v-model="filtroPontuacaoMax"
                  :min="0"
                  class="w-full"
                />
                <label for="filtro-pontuacao-max">Pontuação máx.</label>
              </FloatLabel>
            </div>
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo filtro-campo--full">
                <BaseSelect
                  id="filtro-ativo"
                  v-model="filtroAtivo"
                  :options="opcoesAtivo"
                  optionLabel="label"
                  optionValue="value"
                  class="w-full"
                />
                <label for="filtro-ativo">Status</label>
              </FloatLabel>
            </div>
            <div class="filtro-acoes">
              <Button label="Aplicar" icon="pi pi-check" size="small" @click="aplicarFiltros" />
              <Button label="Limpar" icon="pi pi-filter-slash" size="small" severity="secondary" @click="limparFiltros" />
            </div>
          </div>
        </Popover>
      </template>
      <template #columns>
        <Column field="nome" header="Nome" sortable :style="{ width: '180px', maxWidth: '180px' }" />
        <Column field="descricao" header="Descrição" sortable :style="{ width: '280px', maxWidth: '280px' }">
          <template #body="slotProps">
            {{ truncarDescricao(slotProps.data.descricao) }}
          </template>
        </Column>
        <Column field="pontuacao" header="Pontuação" sortable :style="{ width: '100px', maxWidth: '100px' }" />
        <Column field="ativo" header="Ativo" sortable :style="{ width: '90px', maxWidth: '90px' }">
          <template #body="slotProps">
            <span v-if="slotProps.data.ativo" class="p-tag p-tag-success">Sim</span>
            <span v-else class="p-tag p-tag-danger">Não</span>
          </template>
        </Column>
        <Column v-if="hasPermission('leitor.view_recompensa')" header="Ações" :style="{ width: '100px', maxWidth: '100px' }">
          <template #body="slotProps">
            <div class="col-acoes">
              <Button v-if="hasPermission('leitor.change_recompensa')" label="Editar" size="small" @click="editarRecompensa(slotProps.data)" />
              <Button v-if="hasPermission('leitor.delete_recompensa')" label="Excluir" severity="danger" size="small" @click="excluirRecompensa(slotProps.data)" />
            </div>
          </template>
        </Column>
      </template>
    </BaseDataTable>

    <RecompensaDialog
      v-model:visible="dialogVisible"
      :recompensa="recompensaEditando"
      @save="onRecompensaSalvo"
    />

    <BaseConfirmDialog
      v-model:visible="confirmDeleteVisible"
      title="Excluir recompensa"
      :message="confirmDeleteMessage"
      confirm-label="Excluir"
      cancel-label="Cancelar"
      confirm-severity="danger"
      :loading="confirmDeleteLoading"
      @confirm="confirmarExclusao"
      @cancel="cancelarExclusao"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import BaseDataTable from '@/components/BaseDataTable.vue'

const store = useStore()
const hasPermission = (perm) => store.getters.hasPermission(perm)
import BaseConfirmDialog from '@/components/BaseConfirmDialog.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Popover from 'primevue/popover'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import RecompensaDialog from './RecompensaDialog.vue'
import leitorService from '@/services/leitorService'
import { PAGE_SIZE } from '@/constants/pagination'

const toast = useToast()

const recompensas = ref([])
const loading = ref(false)
const dataKey = 'id'
const totalRecords = ref(0)
const first = ref(0)
const rows = PAGE_SIZE
const lazy = ref(true)
const reorderableColumns = false

const OPCOES_ATIVO = [
  { value: null, label: 'Todos' },
  { value: true, label: 'Apenas ativos' },
  { value: false, label: 'Apenas inativos' }
]

const popoverBuscaRef = ref(null)
const filtroNome = ref('')
const filtroPontuacaoMin = ref(null)
const filtroPontuacaoMax = ref(null)
const filtroAtivo = ref(null)
const opcoesAtivo = OPCOES_ATIVO

const dialogVisible = ref(false)
const recompensaEditando = ref(null)

const confirmDeleteVisible = ref(false)
const confirmDeleteLoading = ref(false)
const recompensaParaExcluir = ref(null)

const confirmDeleteMessage = computed(() => {
  if (!recompensaParaExcluir.value) return 'Confirma a exclusão desta recompensa?'
  return `Excluir a recompensa "${recompensaParaExcluir.value.nome}"?`
})

function truncarDescricao(val, max = 60) {
  if (!val) return '—'
  const s = String(val).trim()
  if (s.length <= max) return s
  return s.slice(0, max) + '…'
}

function montarParametrosBusca() {
  const params = {}
  if (filtroNome.value?.trim()) params['nome__icontains'] = filtroNome.value.trim()
  if (filtroPontuacaoMin.value != null) params['pontuacao__gte'] = filtroPontuacaoMin.value
  if (filtroPontuacaoMax.value != null) params['pontuacao__lte'] = filtroPontuacaoMax.value
  if (filtroAtivo.value === true || filtroAtivo.value === false) params['ativo'] = filtroAtivo.value
  return params
}

async function aplicarFiltros() {
  first.value = 0
  await carregarRecompensas({ ...montarParametrosBusca(), page: 1, page_size: rows })
  popoverBuscaRef.value?.hide()
}

function abrirDialogIncluir() {
  recompensaEditando.value = null
  dialogVisible.value = true
}

async function onRecompensaSalvo() {
  first.value = 0
  await carregarRecompensas({ ...montarParametrosBusca(), page: 1, page_size: rows })
}

async function limparFiltros() {
  filtroNome.value = ''
  filtroPontuacaoMin.value = null
  filtroPontuacaoMax.value = null
  filtroAtivo.value = null
  first.value = 0
  await carregarRecompensas({ page: 1, page_size: rows })
  popoverBuscaRef.value?.hide()
}

function editarRecompensa(rec) {
  recompensaEditando.value = rec
  dialogVisible.value = true
}

function excluirRecompensa(rec) {
  recompensaParaExcluir.value = rec
  confirmDeleteVisible.value = true
}

async function confirmarExclusao() {
  if (!recompensaParaExcluir.value) return
  confirmDeleteLoading.value = true
  try {
    await leitorService.recompensas.delete(recompensaParaExcluir.value.id)
    recompensas.value = recompensas.value.filter((r) => r.id !== recompensaParaExcluir.value.id)
    totalRecords.value = Math.max(0, totalRecords.value - 1)
    toast.add({
      severity: 'success',
      summary: 'Recompensa excluída',
      detail: 'A recompensa foi removida com sucesso.',
      life: 3000
    })
  } catch (e) {
    console.error('Erro ao excluir recompensa:', e)
    const detail = e?.response?.data?.detail
      ? (Array.isArray(e.response.data.detail) ? e.response.data.detail[0] : e.response.data.detail)
      : 'Não foi possível excluir a recompensa.'
    toast.add({ severity: 'error', summary: 'Erro ao excluir', detail, life: 5000 })
  } finally {
    confirmDeleteLoading.value = false
    confirmDeleteVisible.value = false
    recompensaParaExcluir.value = null
  }
}

function cancelarExclusao() {
  confirmDeleteVisible.value = false
  recompensaParaExcluir.value = null
}

async function carregarRecompensas(params = {}) {
  loading.value = true
  try {
    const data = await leitorService.recompensas.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    recompensas.value = list
    totalRecords.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar recompensas:', e)
    recompensas.value = []
  } finally {
    loading.value = false
  }
}

function onPage(event) {
  first.value = event.first
  carregarRecompensas({ ...montarParametrosBusca(), page: event.page + 1, page_size: event.rows })
}

onMounted(() => {
  carregarRecompensas({ page: 1, page_size: rows })
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
  margin-bottom: 1rem;
}

.filtro-campo {
  width: 100%;
}

.filtro-campo--full {
  grid-column: 1 / -1;
}

.filtro-acoes {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
</style>
