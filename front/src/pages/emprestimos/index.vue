<template>
  <div class="page">
    <h1 class="page-title">Empréstimos</h1>
    <p class="page-subtitle">Empréstimos em aberto (não devolvidos).</p>

    <BaseDataTable
      :items="emprestimos"
      :loading="loading"
      :dataKey="dataKey"
      :totalRecords="totalRecords"
      :rows="rows"
      :lazy="lazy"
      :reorderableColumns="reorderableColumns"
    >
      <template #toolbar>
        <div class="table-toolbar" style="margin-top: 1rem;">
          <Button v-if="hasPermission('leitor.view_emprestimo')" label="Buscar" size="small" icon="pi pi-search" @click="(e) => popoverBuscaRef?.toggle(e)" />
          <Button v-if="hasPermission('leitor.add_emprestimo')" label="Incluir" size="small" icon="pi pi-plus" @click="abrirDialogIncluir" />
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
        <Column v-if="hasPermission('leitor.view_emprestimo')" field="leitor_nome" header="Leitor" sortable />
        <Column field="livro_titulo" header="Livro" sortable />
        <Column field="data_emprestimo" header="Data empréstimo" sortable>
          <template #body="slotProps">
            {{ formatarData(slotProps.data.data_emprestimo) }}
          </template>
        </Column>
        <Column field="data_devolucao" header="Data devolução" sortable>
          <template #body="slotProps">
            {{ formatarData(slotProps.data.data_devolucao) }}
          </template>
        </Column>
        <Column header="Atraso" :style="{ width: '120px', maxWidth: '120px' }">
          <template #body="slotProps">
            <span v-if="diasAtraso(slotProps.data) !== null" class="tag-atraso">
              {{ diasAtraso(slotProps.data) }} {{ diasAtraso(slotProps.data) === 1 ? 'dia' : 'dias' }}
            </span>
            <span v-else class="texto-sem-atraso">—</span>
          </template>
        </Column>
        <Column v-if="hasPermission('leitor.view_emprestimo')" header="Ações" :style="{ width: '100px', maxWidth: '100px' }">
          <template #body="slotProps">
            <Button
              v-if="!slotProps.data.devolvido && hasPermission('leitor.change_emprestimo')"
              label="Devolver"
              size="small"
              :loading="devolvendoId === slotProps.data.id"
              @click="devolver(slotProps.data)"
            />
            <span v-else-if="slotProps.data.devolvido" class="texto-sem-atraso">—</span>
          </template>
        </Column>
      </template>
    </BaseDataTable>

    <EmprestimoDialog v-model:visible="dialogIncluirVisible" @save="onEmprestimoSalvo" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'

const store = useStore()
const hasPermission = (perm) => store.getters.hasPermission(perm)
import BaseDataTable from '@/components/BaseDataTable.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Popover from 'primevue/popover'
import FloatLabel from 'primevue/floatlabel'
import leitorService from '@/services/leitorService'
import livroService from '@/services/livroService'
import EmprestimoDialog from './EmprestimoDialog.vue'
import { PAGE_SIZE } from '@/constants/pagination'

const toast = useToast()

const emprestimos = ref([])
const loading = ref(false)
const dataKey = 'id'
const totalRecords = ref(0)
const rows = PAGE_SIZE
const lazy = ref(false)
const reorderableColumns = false

const OPCOES_TIPO_BUSCA = [
  { value: 'aberto', label: 'Empréstimos em aberto' },
  { value: 'historico', label: 'Histórico' }
]

const popoverBuscaRef = ref(null)
const filtroTipo = ref('aberto')
const opcoesTipoBusca = OPCOES_TIPO_BUSCA
const filtroLeitor = ref(null)
const filtroLivro = ref(null)
const opcoesLeitores = ref([])
const opcoesLivros = ref([])
const devolvendoId = ref(null)
const dialogIncluirVisible = ref(false)

function formatarData(val) {
  if (!val) return '—'
  const d = typeof val === 'string' ? new Date(val + 'T12:00:00') : val
  if (isNaN(d.getTime())) return val
  return d.toLocaleDateString('pt-BR')
}

/**
 * Retorna a quantidade de dias de atraso (após a data de devolução).
 * Retorna null se não houver atraso (ainda no prazo ou sem data_devolucao).
 */
function diasAtraso(emp) {
  if (!emp?.data_devolucao) return null
  const hoje = new Date()
  hoje.setHours(0, 0, 0, 0)
  const devolucao = typeof emp.data_devolucao === 'string'
    ? new Date(emp.data_devolucao + 'T12:00:00')
    : new Date(emp.data_devolucao)
  devolucao.setHours(0, 0, 0, 0)
  const diff = Math.floor((hoje - devolucao) / (1000 * 60 * 60 * 24))
  return diff > 0 ? diff : null
}

function montarParametrosBusca() {
  const params = {}
  if (filtroTipo.value === 'aberto') params['devolvido'] = false
  if (filtroLeitor.value != null) params['leitor'] = filtroLeitor.value
  if (filtroLivro.value != null) params['livro'] = filtroLivro.value
  return params
}

async function devolver(emp) {
  if (!emp?.id) return
  devolvendoId.value = emp.id
  try {
    const payload = {
      leitor: emp.leitor,
      livro: emp.livro,
      data_emprestimo: emp.data_emprestimo,
      data_devolucao: emp.data_devolucao ?? emp.data_emprestimo,
      devolvido: true
    }
    await leitorService.emprestimos.update(emp.id, payload)
    toast.add({
      severity: 'success',
      summary: 'Devolvido',
      detail: 'Empréstimo marcado como devolvido.',
      life: 3000
    })
    await carregarEmprestimos(montarParametrosBusca())
  } catch (e) {
    console.error('Erro ao devolver:', e)
    const detail = e?.response?.data
      ? typeof e.response.data === 'object'
        ? Object.entries(e.response.data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
            .join(' | ')
        : e.response.data
      : 'Não foi possível marcar como devolvido.'
    toast.add({ severity: 'error', summary: 'Erro ao devolver', detail, life: 5000 })
  } finally {
    devolvendoId.value = null
  }
}

async function aplicarFiltros() {
  await carregarEmprestimos(montarParametrosBusca())
  popoverBuscaRef.value?.hide()
}

function abrirDialogIncluir() {
  dialogIncluirVisible.value = true
}

async function onEmprestimoSalvo() {
  await carregarEmprestimos(montarParametrosBusca())
}

async function limparFiltros() {
  filtroTipo.value = 'aberto'
  filtroLeitor.value = null
  filtroLivro.value = null
  await carregarEmprestimos(montarParametrosBusca())
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

async function carregarEmprestimos(params = {}) {
  loading.value = true
  try {
    const data = await leitorService.emprestimos.getAll(params)
    const list = Array.isArray(data) ? data : data?.results ?? []
    emprestimos.value = list
    totalRecords.value = data?.count ?? list.length
  } catch (e) {
    console.error('Erro ao carregar empréstimos:', e)
    emprestimos.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  carregarOpcoesFiltro()
  carregarEmprestimos(montarParametrosBusca())
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

.tag-atraso {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background: var(--perigo);
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
}

.texto-sem-atraso {
  color: var(--text-color-secondary);
}
</style>
