<template>
  <div class="page">
    <h1 class="page-title">Reservas</h1>
    <p class="page-subtitle">Reservas em aberto e histórico.</p>

    <BaseDataTable
      :items="reservas"
      :loading="loading"
      :dataKey="dataKey"
      :totalRecords="totalRecords"
      :rows="rows"
      :lazy="lazy"
      :reorderableColumns="reorderableColumns"
    >
      <template #toolbar>
        <div class="table-toolbar" style="margin-top: 1rem;">
          <Button v-if="hasPermission('leitor.view_reserva')" label="Buscar" size="small" icon="pi pi-search" @click="(e) => popoverBuscaRef?.toggle(e)" />
          <Button v-if="hasPermission('leitor.add_reserva')" label="Incluir" size="small" icon="pi pi-plus" @click="abrirDialogIncluir" />
        </div>

        <Popover ref="popoverBuscaRef" :style="{ width: '35%' }">
          <div class="filtro-popover">
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo filtro-campo--full">
                <BaseSelect
                  id="filtro-tipo"
                  v-model="filtroTipo"
                  :options="opcoesTipoBusca"
                  optionLabel="label"
                  optionValue="value"
                  class="w-full"
                />
                <label for="filtro-tipo">Exibir</label>
              </FloatLabel>
            </div>
            <div class="filtro-linha">
              <FloatLabel class="filtro-campo">
                <BaseSelect
                  id="filtro-leitor"
                  v-model="filtroLeitor"
                  :options="opcoesLeitores"
                  optionLabel="nome"
                  optionValue="id"
                  showClear
                  class="w-full"
                />
                <label for="filtro-leitor">Leitor</label>
              </FloatLabel>
              <FloatLabel class="filtro-campo">
                <BaseSelect
                  id="filtro-livro"
                  v-model="filtroLivro"
                  :options="opcoesLivros"
                  optionLabel="titulo"
                  optionValue="id"
                  showClear
                  class="w-full"
                />
                <label for="filtro-livro">Livro</label>
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
        <Column v-if="hasPermission('leitor.view_reserva')" field="leitor_nome" header="Leitor" sortable />
        <Column field="livro_titulo" header="Livro" sortable />
        <Column field="data_reserva" header="Data reserva" sortable>
          <template #body="slotProps">
            {{ formatarData(slotProps.data.data_reserva) }}
          </template>
        </Column>
        <Column field="data_expiracao" header="Data expiração" sortable>
          <template #body="slotProps">
            {{ formatarData(slotProps.data.data_expiracao) }}
          </template>
        </Column>
        <Column header="Expirada" :style="{ width: '100px', maxWidth: '100px' }">
          <template #body="slotProps">
            <span v-if="estaExpirada(slotProps.data)" class="tag-expirada">Expirada</span>
            <span v-else class="texto-sem-destaque">—</span>
          </template>
        </Column>
        <Column v-if="hasPermission('leitor.view_reserva')" header="Ações" :style="{ width: '100px', maxWidth: '100px' }">
          <template #body="slotProps">
            <Button
              v-if="slotProps.data.ativo && hasPermission('leitor.change_reserva')"
              label="Cancelar"
              size="small"
              severity="danger"
              @click="abrirConfirmacaoCancelar(slotProps.data)"
            />
            <span v-else class="texto-sem-destaque">—</span>
          </template>
        </Column>
      </template>
    </BaseDataTable>

    <ReservaDialog v-model:visible="dialogIncluirVisible" @save="onReservaSalva" />

    <BaseConfirmDialog
      :visible="confirmCancelVisible"
      title="Cancelar reserva"
      :message="confirmCancelMessage"
      confirmLabel="Cancelar reserva"
      cancelLabel="Voltar"
      confirmSeverity="danger"
      :loading="confirmCancelLoading"
      @update:visible="(v) => (confirmCancelVisible = v)"
      @confirm="confirmarCancelamento"
      @cancel="fecharConfirmacaoCancelar"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import BaseDataTable from '@/components/BaseDataTable.vue'
import BaseConfirmDialog from '@/components/BaseConfirmDialog.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Popover from 'primevue/popover'
import FloatLabel from 'primevue/floatlabel'
import leitorService from '@/services/leitorService'
import livroService from '@/services/livroService'
import ReservaDialog from './ReservaDialog.vue'
import { PAGE_SIZE } from '@/constants/pagination'

const store = useStore()
const hasPermission = (perm) => store.getters.hasPermission(perm)
const toast = useToast()

const reservas = ref([])
const loading = ref(false)
const dataKey = 'id'
const totalRecords = ref(0)
const rows = PAGE_SIZE
const lazy = ref(false)
const reorderableColumns = false

const OPCOES_TIPO_BUSCA = [
  { value: 'aberto', label: 'Reservas em aberto' },
  { value: 'historico', label: 'Histórico' }
]

const popoverBuscaRef = ref(null)
const filtroTipo = ref('aberto')
const opcoesTipoBusca = OPCOES_TIPO_BUSCA
const filtroLeitor = ref(null)
const filtroLivro = ref(null)
const opcoesLeitores = ref([])
const opcoesLivros = ref([])
const dialogIncluirVisible = ref(false)
const confirmCancelVisible = ref(false)
const confirmCancelLoading = ref(false)
const reservaParaCancelar = ref(null)

const confirmCancelMessage = computed(() => {
  if (!reservaParaCancelar.value) return 'Deseja cancelar esta reserva?'
  const r = reservaParaCancelar.value
  return `Cancelar a reserva de "${r.livro_titulo || 'livro'}" para ${r.leitor_nome || 'o leitor'}?`
})

function formatarData(val) {
  if (!val) return '—'
  const d = typeof val === 'string' ? new Date(val + 'T12:00:00') : val
  if (isNaN(d.getTime())) return val
  return d.toLocaleDateString('pt-BR')
}

function estaExpirada(res) {
  if (!res?.data_expiracao) return false
  const hoje = new Date()
  hoje.setHours(0, 0, 0, 0)
  const exp = typeof res.data_expiracao === 'string'
    ? new Date(res.data_expiracao + 'T12:00:00')
    : new Date(res.data_expiracao)
  exp.setHours(0, 0, 0, 0)
  return hoje > exp
}

function montarParametrosBusca() {
  const params = {}
  if (filtroTipo.value === 'aberto') params['ativo'] = true
  if (filtroLeitor.value != null) params['leitor'] = filtroLeitor.value
  if (filtroLivro.value != null) params['livro'] = filtroLivro.value
  return params
}

function abrirConfirmacaoCancelar(res) {
  reservaParaCancelar.value = res
  confirmCancelVisible.value = true
}

function fecharConfirmacaoCancelar() {
  confirmCancelVisible.value = false
  reservaParaCancelar.value = null
}

async function confirmarCancelamento() {
  if (!reservaParaCancelar.value?.id) return
  confirmCancelLoading.value = true
  try {
    const res = reservaParaCancelar.value
    const payload = {
      leitor: res.leitor,
      livro: res.livro,
      data_reserva: res.data_reserva,
      data_expiracao: res.data_expiracao ?? res.data_reserva,
      ativo: false
    }
    await leitorService.reservas.update(res.id, payload)
    toast.add({
      severity: 'success',
      summary: 'Reserva cancelada',
      detail: 'A reserva foi cancelada.',
      life: 3000
    })
    await carregarReservas(montarParametrosBusca())
    fecharConfirmacaoCancelar()
  } catch (e) {
    console.error('Erro ao cancelar reserva:', e)
    const detail = e?.response?.data
      ? typeof e.response.data === 'object'
        ? Object.entries(e.response.data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
            .join(' | ')
        : e.response.data
      : 'Não foi possível cancelar a reserva.'
    toast.add({ severity: 'error', summary: 'Erro ao cancelar', detail, life: 5000 })
  } finally {
    confirmCancelLoading.value = false
  }
}

function abrirDialogIncluir() {
  dialogIncluirVisible.value = true
}

async function onReservaSalva() {
  await carregarReservas(montarParametrosBusca())
}

async function aplicarFiltros() {
  await carregarReservas(montarParametrosBusca())
  popoverBuscaRef.value?.hide()
}

async function limparFiltros() {
  filtroTipo.value = 'aberto'
  filtroLeitor.value = null
  filtroLivro.value = null
  await carregarReservas(montarParametrosBusca())
  popoverBuscaRef.value?.hide()
}

async function carregarOpcoesFiltro() {
  try {
    const [dataLeitores, dataLivros] = await Promise.all([
      leitorService.leitores.getAll(),
      livroService.livros.getAll()
    ])
    opcoesLeitores.value = Array.isArray(dataLeitores) ? dataLeitores : dataLeitores?.results ?? []
    opcoesLivros.value = Array.isArray(dataLivros) ? dataLivros : dataLivros?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar opções do filtro:', e)
  }
}

async function carregarReservas(params = {}) {
  loading.value = true
  try {
    const data = await leitorService.reservas.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    reservas.value = list
    totalRecords.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar reservas:', e)
    reservas.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  carregarOpcoesFiltro()
  carregarReservas(montarParametrosBusca())
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

.tag-expirada {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background: var(--perigo);
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
}

.texto-sem-destaque {
  color: var(--text-color-secondary);
}
</style>
