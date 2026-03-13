<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Leitor"
    :style="{ width: '65rem' }"
    :contentStyle="{ overflow: 'visible' }"
    @hide="limparFormulario"
    @show="carregarOpcoes"
  >
    <div class="dialog-body">
      <Tabs v-model:value="tabAtiva" class="dialog-tabs">
        <TabList>
          <Tab value="leitor">Leitores</Tab>
          <Tab value="emprestimo">Empréstimo</Tab>
          <Tab value="reservas">Reservas</Tab>
          <Tab value="recompensas">Recompensas</Tab>
        </TabList>
        <TabPanels>
          <!-- Tab Leitores: formulário do leitor -->
          <TabPanel value="leitor">
            <div class="dialog-body">
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-nome" v-model="form.nome" class="dialog-input" autocomplete="off" />
                    <label for="leitor-nome">Nome</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-email" v-model="form.email" class="dialog-input" type="email" autocomplete="off" />
                    <label for="leitor-email">E-mail</label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <DatePicker
                      v-model="form.data_nascimento"
                      inputId="leitor-data-nasc"
                      dateFormat="dd/mm/yy"
                      showIcon
                      iconDisplay="input"
                      class="dialog-input"
                    />
                    <label for="leitor-data-nasc">Data de nascimento</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-cpf" v-model="form.cpf" class="dialog-input" maxlength="11" autocomplete="off" />
                    <label for="leitor-cpf">CPF</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-telefone" v-model="form.telefone" class="dialog-input" autocomplete="off" />
                    <label for="leitor-telefone">Telefone</label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-sexo" v-model="form.sexo" class="dialog-input" autocomplete="off" />
                    <label for="leitor-sexo">Sexo</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-profissao" v-model="form.profissao" class="dialog-input" autocomplete="off" />
                    <label for="leitor-profissao">Profissão</label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-endereco" v-model="form.endereco" class="dialog-input" autocomplete="off" />
                    <label for="leitor-endereco">Endereço</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-numero" v-model="form.numero" class="dialog-input" autocomplete="off" />
                    <label for="leitor-numero">Número</label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-complemento" v-model="form.complemento" class="dialog-input" autocomplete="off" />
                    <label for="leitor-complemento">Complemento</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-bairro" v-model="form.bairro" class="dialog-input" autocomplete="off" />
                    <label for="leitor-bairro">Bairro</label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-cidade" v-model="form.cidade" class="dialog-input" autocomplete="off" />
                    <label for="leitor-cidade">Cidade</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-estado" v-model="form.estado" class="dialog-input" autocomplete="off" />
                    <label for="leitor-estado">Estado</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-cep" v-model="form.cep" class="dialog-input" maxlength="10" autocomplete="off" />
                    <label for="leitor-cep">CEP</label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field dialog-field--checkbox">
                  <div class="dialog-input-wrap dialog-input-wrap--inline dialog-checkbox-wrap">
                    <Checkbox id="leitor-ativo" v-model="form.ativo" :binary="true" inputId="leitor-ativo" />
                    <label for="leitor-ativo" class="dialog-checkbox-label">Ativo</label>
                  </div>
                </div>
              </div>
              <div class="dialog-actions dialog-actions--inside-tab">
                <Button type="button" label="Salvar" size="small" @click="salvar" />
              </div>
            </div>
          </TabPanel>

          <!-- Tab Empréstimo -->
          <TabPanel value="emprestimo">
            <div class="dialog-autor" style="margin-top: 1rem;">
              <div v-if="!leitorId" class="dialog-aviso">Salve o leitor antes de cadastrar empréstimos.</div>
              <template v-else>
                <div class="dialog-row dialog-autor-row">
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <BaseSelect
                        id="emp-livro"
                        v-model="emprestimoForm.livro"
                        :options="opcoesLivros"
                        optionLabel="titulo"
                        optionValue="id"
                        placeholder="Livro"
                        showClear
                        class="dialog-input"
                      />
                      <label for="emp-livro">Livro</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText id="emp-data-emp" v-model="emprestimoForm.data_emprestimo" class="dialog-input" type="datetime-local" />
                      <label for="emp-data-emp">Data empréstimo</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText id="emp-data-dev" v-model="emprestimoForm.data_devolucao" class="dialog-input" type="datetime-local" />
                      <label for="emp-data-dev">Data devolução</label>
                    </FloatLabel>
                  </div>
                </div>
                <div class="dialog-row dialog-autor-row">
                  <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarEmprestimo" />
                </div>
                <BaseDataTable
                  :items="emprestimosLista"
                  :loading="loadingEmprestimos"
                  dataKey="id"
                  :totalRecords="emprestimosLista.length"
                  :rows="10"
                  :lazy="false"
                  :reorderableColumns="false"
                  class="dialog-autor-table"
                >
                  <template #columns>
                    <Column header="Livro">
                      <template #body="slotProps">
                        {{ nomeLivro(slotProps.data.livro) }}
                      </template>
                    </Column>
                    <Column header="Data empréstimo">
                      <template #body="slotProps">
                        {{ formatarData(slotProps.data.data_emprestimo) }}
                      </template>
                    </Column>
                    <Column header="Data devolução">
                      <template #body="slotProps">
                        {{ formatarData(slotProps.data.data_devolucao) }}
                      </template>
                    </Column>
                    <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }" bodyClass="dialog-col-acoes" headerClass="dialog-col-acoes">
                      <template #body="slotProps">
                        <div class="dialog-col-acoes">
                          <Button label="Editar" severity="success" size="small" @click="editarEmprestimo(slotProps.data)" />
                          <Button label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluirEmprestimo(slotProps.data)" />
                        </div>
                      </template>
                    </Column>
                  </template>
                </BaseDataTable>
                <BaseConfirmDialog
                  :visible="confirmDeleteEmprestimoVisible"
                  title="Excluir empréstimo"
                  :message="confirmDeleteEmprestimoMessage"
                  confirmLabel="Excluir"
                  cancelLabel="Cancelar"
                  confirmSeverity="danger"
                  :loading="confirmDeleteEmprestimoLoading"
                  @update:visible="(v) => (confirmDeleteEmprestimoVisible = v)"
                  @confirm="confirmarExclusaoEmprestimo"
                  @cancel="cancelarExclusaoEmprestimo"
                />
              </template>
            </div>
          </TabPanel>

          <!-- Tab Reservas -->
          <TabPanel value="reservas">
            <div class="dialog-autor" style="margin-top: 1rem;">
              <div v-if="!leitorId" class="dialog-aviso">Salve o leitor antes de cadastrar reservas.</div>
              <template v-else>
                <div class="dialog-row dialog-autor-row">
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <BaseSelect
                        id="res-livro"
                        v-model="reservaForm.livro"
                        :options="opcoesLivros"
                        optionLabel="titulo"
                        optionValue="id"
                        placeholder="Livro"
                        showClear
                        class="dialog-input"
                      />
                      <label for="res-livro">Livro</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText id="res-data-reserva" v-model="reservaForm.data_reserva" class="dialog-input" type="datetime-local" />
                      <label for="res-data-reserva">Data reserva</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText id="res-data-exp" v-model="reservaForm.data_expiracao" class="dialog-input" type="datetime-local" />
                      <label for="res-data-exp">Data expiração</label>
                    </FloatLabel>
                  </div>
                </div>
                <div class="dialog-row dialog-autor-row">
                  <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarReserva" />
                </div>
                <BaseDataTable
                  :items="reservasLista"
                  :loading="loadingReservas"
                  dataKey="id"
                  :totalRecords="reservasLista.length"
                  :rows="10"
                  :lazy="false"
                  :reorderableColumns="false"
                  class="dialog-autor-table"
                >
                  <template #columns>
                    <Column header="Livro">
                      <template #body="slotProps">
                        {{ nomeLivro(slotProps.data.livro) }}
                      </template>
                    </Column>
                    <Column header="Data reserva">
                      <template #body="slotProps">
                        {{ formatarData(slotProps.data.data_reserva) }}
                      </template>
                    </Column>
                    <Column header="Data expiração">
                      <template #body="slotProps">
                        {{ formatarData(slotProps.data.data_expiracao) }}
                      </template>
                    </Column>
                    <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }" bodyClass="dialog-col-acoes" headerClass="dialog-col-acoes">
                      <template #body="slotProps">
                        <div class="dialog-col-acoes">
                          <Button label="Editar" severity="success" size="small" @click="editarReserva(slotProps.data)" />
                          <Button label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluirReserva(slotProps.data)" />
                        </div>
                      </template>
                    </Column>
                  </template>
                </BaseDataTable>
                <BaseConfirmDialog
                  :visible="confirmDeleteReservaVisible"
                  title="Excluir reserva"
                  :message="confirmDeleteReservaMessage"
                  confirmLabel="Excluir"
                  cancelLabel="Cancelar"
                  confirmSeverity="danger"
                  :loading="confirmDeleteReservaLoading"
                  @update:visible="(v) => (confirmDeleteReservaVisible = v)"
                  @confirm="confirmarExclusaoReserva"
                  @cancel="cancelarExclusaoReserva"
                />
              </template>
            </div>
          </TabPanel>

          <!-- Tab Recompensas (CRUD de recompensas, como Autor no LivroDialog) -->
          <TabPanel value="recompensas">
            <div class="dialog-autor">
              <div class="dialog-row dialog-autor-row" style="margin-top: 1rem;">
                <div class="dialog-field dialog-autor-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="rec-nome" v-model="recompensaForm.nome" class="dialog-input" />
                    <label for="rec-nome">Nome</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field dialog-autor-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="rec-descricao" v-model="recompensaForm.descricao" class="dialog-input" />
                    <label for="rec-descricao">Descrição</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field dialog-autor-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputNumber id="rec-pontuacao" v-model="recompensaForm.pontuacao" class="dialog-input" :min="0" />
                    <label for="rec-pontuacao">Pontuação</label>
                  </FloatLabel>
                </div>
                <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarRecompensa" />
                <Button type="button" label="Buscar" icon="pi pi-search" size="small" class="dialog-autor-button" @click="(e) => popoverPesquisaRecompensaRef?.toggle(e)" />
                <Popover ref="popoverPesquisaRecompensaRef">
                  <div class="dialog-popover-pesquisa">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <InputText id="pesquisa-recompensa" v-model="filtroPesquisaRecompensa" class="dialog-input" autocomplete="off" />
                      <label for="pesquisa-recompensa">Pesquisar recompensa</label>
                    </FloatLabel>
                    <div class="dialog-popover-actions">
                      <Button type="button" label="Limpar" severity="secondary" size="small" @click="limparPesquisaRecompensa" />
                    </div>
                  </div>
                </Popover>
              </div>
              <BaseDataTable
                :items="recompensasFiltradas"
                :loading="loadingRecompensas"
                dataKey="id"
                :totalRecords="recompensasFiltradas.length"
                :rows="recompensasRows"
                :lazy="false"
                :reorderableColumns="false"
                class="dialog-autor-table"
              >
                <template #columns>
                  <Column field="nome" header="Nome" />
                  <Column field="descricao" header="Descrição" />
                  <Column field="pontuacao" header="Pontuação" :style="{ width: '100px', maxWidth: '100px' }" />
                  <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }" bodyClass="dialog-col-acoes" headerClass="dialog-col-acoes">
                    <template #body="slotProps">
                      <div class="dialog-col-acoes">
                        <Button label="Editar" severity="success" size="small" @click="editarRecompensa(slotProps.data)" />
                        <Button label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluirRecompensa(slotProps.data)" />
                      </div>
                    </template>
                  </Column>
                </template>
              </BaseDataTable>
              <BaseConfirmDialog
                :visible="confirmDeleteRecompensaVisible"
                title="Excluir recompensa"
                :message="confirmDeleteRecompensaMessage"
                confirmLabel="Excluir"
                cancelLabel="Cancelar"
                confirmSeverity="danger"
                :loading="confirmDeleteRecompensaLoading"
                @update:visible="(v) => (confirmDeleteRecompensaVisible = v)"
                @confirm="confirmarExclusaoRecompensa"
                @cancel="cancelarExclusaoRecompensa"
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
import DatePicker from 'primevue/datepicker'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import BaseDataTable from '@/components/BaseDataTable.vue'
import BaseConfirmDialog from '@/components/BaseConfirmDialog.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import Column from 'primevue/column'
import Popover from 'primevue/popover'
import { useToast } from 'primevue/usetoast'
import leitorService from '@/services/leitorService'
import livroService from '@/services/livroService'

const props = defineProps({
  visible: { type: Boolean, default: false },
  leitor: { type: Object, default: null }
})

const emit = defineEmits(['update:visible', 'save'])

const visibleModel = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v)
})

const tabAtiva = ref('leitor')
const form = ref(getFormDefault())
const opcoesLivros = ref([])

const leitorId = computed(() => props.leitor?.id ?? form.value.id ?? null)

// Empréstimos
const emprestimosLista = ref([])
const loadingEmprestimos = ref(false)
const emprestimoForm = ref(getEmprestimoFormDefault())
const emprestimoEditandoId = ref(null)

const confirmDeleteEmprestimoVisible = ref(false)
const confirmDeleteEmprestimoLoading = ref(false)
const emprestimoParaExcluir = ref(null)
const confirmDeleteEmprestimoMessage = computed(() => {
  if (!emprestimoParaExcluir.value) return 'Confirma a exclusão deste empréstimo?'
  return 'Excluir este empréstimo?'
})

// Reservas
const reservasLista = ref([])
const loadingReservas = ref(false)
const reservaForm = ref(getReservaFormDefault())
const reservaEditandoId = ref(null)

const confirmDeleteReservaVisible = ref(false)
const confirmDeleteReservaLoading = ref(false)
const reservaParaExcluir = ref(null)
const confirmDeleteReservaMessage = computed(() => {
  if (!reservaParaExcluir.value) return 'Confirma a exclusão desta reserva?'
  return 'Excluir esta reserva?'
})

// Recompensas
const recompensas = ref([])
const loadingRecompensas = ref(false)
const recompensasRows = 10
const recompensaEditandoId = ref(null)
const recompensaForm = ref({ nome: '', descricao: '', pontuacao: 0 })
const popoverPesquisaRecompensaRef = ref(null)
const filtroPesquisaRecompensa = ref('')

const confirmDeleteRecompensaVisible = ref(false)
const confirmDeleteRecompensaLoading = ref(false)
const recompensaParaExcluir = ref(null)
const confirmDeleteRecompensaMessage = computed(() => {
  if (!recompensaParaExcluir.value) return 'Confirma a exclusão desta recompensa?'
  return `Excluir a recompensa ${recompensaParaExcluir.value.nome}?`
})

const recompensasFiltradas = computed(() => {
  const lista = recompensas.value ?? []
  const termo = filtroPesquisaRecompensa.value?.trim().toLowerCase() || ''
  if (!termo) return lista
  return lista.filter((r) => (r.nome || '').toLowerCase().includes(termo) || (r.descricao || '').toLowerCase().includes(termo))
})

const toast = useToast()

function getFormDefault() {
  return {
    id: null,
    nome: '',
    email: '',
    data_nascimento: null,
    cpf: '',
    telefone: '',
    sexo: '',
    profissao: '',
    endereco: '',
    numero: '',
    complemento: '',
    bairro: '',
    cidade: '',
    estado: '',
    pais: '',
    cep: '',
    ativo: true
  }
}

function getEmprestimoFormDefault() {
  return { livro: null, data_emprestimo: '', data_devolucao: '' }
}

function getReservaFormDefault() {
  return { livro: null, data_reserva: '', data_expiracao: '' }
}

function preencherFormComLeitor(leitor) {
  if (!leitor) {
    form.value = getFormDefault()
    return
  }
  const dataNasc = leitor.data_nascimento
  const dataNascDate = !dataNasc ? null : dataNasc instanceof Date ? dataNasc : new Date(typeof dataNasc === 'string' ? dataNasc.slice(0, 10) : dataNasc)
  form.value = {
    id: leitor.id,
    nome: leitor.nome ?? '',
    email: leitor.email ?? '',
    data_nascimento: dataNascDate,
    cpf: leitor.cpf ?? '',
    telefone: leitor.telefone ?? '',
    sexo: leitor.sexo ?? '',
    profissao: leitor.profissao ?? '',
    endereco: leitor.endereco ?? '',
    numero: leitor.numero ?? '',
    complemento: leitor.complemento ?? '',
    bairro: leitor.bairro ?? '',
    cidade: leitor.cidade ?? '',
    estado: leitor.estado ?? '',
    pais: leitor.pais ?? '',
    cep: leitor.cep ?? '',
    ativo: leitor.ativo ?? true
  }
}

function formatarData(val) {
  if (!val) return ''
  const d = new Date(val)
  if (isNaN(d.getTime())) return String(val)
  return d.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}

function nomeLivro(livroId) {
  if (!livroId) return ''
  const livro = opcoesLivros.value.find((l) => l.id === livroId)
  return livro?.titulo ?? livroId
}

async function carregarOpcoes() {
  try {
    const [livros] = await Promise.all([livroService.livros.getAll()])
    const listaLivros = Array.isArray(livros) ? livros : livros?.results ?? []
    opcoesLivros.value = listaLivros
    await carregarRecompensas()
    if (leitorId.value) {
      await carregarEmprestimos()
      await carregarReservas()
    }
  } catch (e) {
    console.error('Erro ao carregar opções:', e)
    toast.add({ severity: 'error', summary: 'Erro ao carregar dados', detail: 'Não foi possível carregar os dados.', life: 5000 })
  }
}

async function carregarEmprestimos() {
  if (!leitorId.value) return
  loadingEmprestimos.value = true
  try {
    const data = await leitorService.emprestimos.getAll({ leitor: leitorId.value })
    emprestimosLista.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar empréstimos:', e)
    emprestimosLista.value = []
  } finally {
    loadingEmprestimos.value = false
  }
}

async function carregarReservas() {
  if (!leitorId.value) return
  loadingReservas.value = true
  try {
    const data = await leitorService.reservas.getAll({ leitor: leitorId.value })
    reservasLista.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar reservas:', e)
    reservasLista.value = []
  } finally {
    loadingReservas.value = false
  }
}

async function carregarRecompensas() {
  loadingRecompensas.value = true
  try {
    const data = await leitorService.recompensas.getAll()
    recompensas.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar recompensas:', e)
    recompensas.value = []
  } finally {
    loadingRecompensas.value = false
  }
}

function limparFormulario() {
  form.value = getFormDefault()
  emprestimoForm.value = getEmprestimoFormDefault()
  reservaForm.value = getReservaFormDefault()
  recompensaForm.value = { nome: '', descricao: '', pontuacao: 0 }
  emprestimoEditandoId.value = null
  reservaEditandoId.value = null
  recompensaEditandoId.value = null
  tabAtiva.value = 'leitor'
}

function salvar() {
  const dataNasc = form.value.data_nascimento
  const dataNascStr = dataNasc instanceof Date ? dataNasc.toISOString().slice(0, 10) : (dataNasc || null)
  const payload = {
    nome: form.value.nome || null,
    email: form.value.email || null,
    data_nascimento: dataNascStr,
    cpf: form.value.cpf || null,
    telefone: form.value.telefone || null,
    sexo: form.value.sexo || null,
    profissao: form.value.profissao || null,
    endereco: form.value.endereco || null,
    numero: form.value.numero || null,
    complemento: form.value.complemento || null,
    bairro: form.value.bairro || null,
    cidade: form.value.cidade || null,
    estado: form.value.estado || null,
    pais: form.value.pais || null,
    cep: form.value.cep || null,
    ativo: form.value.ativo ?? true
  }
  emit('save', payload)
  visibleModel.value = false
}

function toDateTimeLocal(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  if (isNaN(d.getTime())) return ''
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function salvarEmprestimo() {
  if (!leitorId.value || !emprestimoForm.value.livro) {
    toast.add({ severity: 'warn', summary: 'Campos obrigatórios', detail: 'Selecione o livro.', life: 3000 })
    return
  }
  try {
    const payload = {
      leitor: leitorId.value,
      livro: emprestimoForm.value.livro,
      data_emprestimo: emprestimoForm.value.data_emprestimo ? new Date(emprestimoForm.value.data_emprestimo).toISOString() : new Date().toISOString(),
      data_devolucao: emprestimoForm.value.data_devolucao ? new Date(emprestimoForm.value.data_devolucao).toISOString() : new Date().toISOString()
    }
    if (emprestimoEditandoId.value) {
      await leitorService.emprestimos.update(emprestimoEditandoId.value, payload)
      toast.add({ severity: 'success', summary: 'Empréstimo atualizado', life: 3000 })
    } else {
      await leitorService.emprestimos.create(payload)
      toast.add({ severity: 'success', summary: 'Empréstimo cadastrado', life: 3000 })
    }
    emprestimoForm.value = getEmprestimoFormDefault()
    emprestimoEditandoId.value = null
    await carregarEmprestimos()
  } catch (e) {
    console.error('Erro ao salvar empréstimo:', e)
    toast.add({ severity: 'error', summary: 'Erro ao salvar empréstimo', detail: e?.response?.data?.detail || 'Não foi possível salvar.', life: 5000 })
  }
}

function editarEmprestimo(emp) {
  emprestimoEditandoId.value = emp.id
  emprestimoForm.value = {
    livro: emp.livro,
    data_emprestimo: toDateTimeLocal(emp.data_emprestimo),
    data_devolucao: toDateTimeLocal(emp.data_devolucao)
  }
}

function abrirConfirmacaoExcluirEmprestimo(emp) {
  emprestimoParaExcluir.value = emp
  confirmDeleteEmprestimoVisible.value = true
}

async function confirmarExclusaoEmprestimo() {
  if (!emprestimoParaExcluir.value) return
  confirmDeleteEmprestimoLoading.value = true
  try {
    await leitorService.emprestimos.delete(emprestimoParaExcluir.value.id)
    await carregarEmprestimos()
    toast.add({ severity: 'success', summary: 'Empréstimo excluído', life: 3000 })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erro ao excluir empréstimo', life: 5000 })
  } finally {
    confirmDeleteEmprestimoLoading.value = false
    confirmDeleteEmprestimoVisible.value = false
    emprestimoParaExcluir.value = null
  }
}

function cancelarExclusaoEmprestimo() {
  confirmDeleteEmprestimoVisible.value = false
  emprestimoParaExcluir.value = null
}

async function salvarReserva() {
  if (!leitorId.value || !reservaForm.value.livro) {
    toast.add({ severity: 'warn', summary: 'Campos obrigatórios', detail: 'Selecione o livro.', life: 3000 })
    return
  }
  try {
    const payload = {
      leitor: leitorId.value,
      livro: reservaForm.value.livro,
      data_reserva: reservaForm.value.data_reserva ? new Date(reservaForm.value.data_reserva).toISOString() : new Date().toISOString(),
      data_expiracao: reservaForm.value.data_expiracao ? new Date(reservaForm.value.data_expiracao).toISOString() : new Date().toISOString()
    }
    if (reservaEditandoId.value) {
      await leitorService.reservas.update(reservaEditandoId.value, payload)
      toast.add({ severity: 'success', summary: 'Reserva atualizada', life: 3000 })
    } else {
      await leitorService.reservas.create(payload)
      toast.add({ severity: 'success', summary: 'Reserva cadastrada', life: 3000 })
    }
    reservaForm.value = getReservaFormDefault()
    reservaEditandoId.value = null
    await carregarReservas()
  } catch (e) {
    console.error('Erro ao salvar reserva:', e)
    toast.add({ severity: 'error', summary: 'Erro ao salvar reserva', detail: e?.response?.data?.detail || 'Não foi possível salvar.', life: 5000 })
  }
}

function editarReserva(res) {
  reservaEditandoId.value = res.id
  reservaForm.value = {
    livro: res.livro,
    data_reserva: toDateTimeLocal(res.data_reserva),
    data_expiracao: toDateTimeLocal(res.data_expiracao)
  }
}

function abrirConfirmacaoExcluirReserva(res) {
  reservaParaExcluir.value = res
  confirmDeleteReservaVisible.value = true
}

async function confirmarExclusaoReserva() {
  if (!reservaParaExcluir.value) return
  confirmDeleteReservaLoading.value = true
  try {
    await leitorService.reservas.delete(reservaParaExcluir.value.id)
    await carregarReservas()
    toast.add({ severity: 'success', summary: 'Reserva excluída', life: 3000 })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erro ao excluir reserva', life: 5000 })
  } finally {
    confirmDeleteReservaLoading.value = false
    confirmDeleteReservaVisible.value = false
    reservaParaExcluir.value = null
  }
}

function cancelarExclusaoReserva() {
  confirmDeleteReservaVisible.value = false
  reservaParaExcluir.value = null
}

async function salvarRecompensa() {
  if (!recompensaForm.value.nome) return
  try {
    const payload = { nome: recompensaForm.value.nome, descricao: recompensaForm.value.descricao ?? null, pontuacao: recompensaForm.value.pontuacao ?? 0 }
    if (recompensaEditandoId.value) {
      await leitorService.recompensas.update(recompensaEditandoId.value, payload)
      toast.add({ severity: 'success', summary: 'Recompensa atualizada', life: 3000 })
    } else {
      await leitorService.recompensas.create(payload)
      toast.add({ severity: 'success', summary: 'Recompensa cadastrada', life: 3000 })
    }
    recompensaForm.value = { nome: '', descricao: '', pontuacao: 0 }
    recompensaEditandoId.value = null
    await carregarRecompensas()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erro ao salvar recompensa', life: 5000 })
  }
}

function editarRecompensa(rec) {
  recompensaEditandoId.value = rec.id
  recompensaForm.value = { nome: rec.nome ?? '', descricao: rec.descricao ?? '', pontuacao: rec.pontuacao ?? 0 }
}

function abrirConfirmacaoExcluirRecompensa(rec) {
  recompensaParaExcluir.value = rec
  confirmDeleteRecompensaVisible.value = true
}

async function confirmarExclusaoRecompensa() {
  if (!recompensaParaExcluir.value) return
  confirmDeleteRecompensaLoading.value = true
  try {
    await leitorService.recompensas.delete(recompensaParaExcluir.value.id)
    await carregarRecompensas()
    toast.add({ severity: 'success', summary: 'Recompensa excluída', life: 3000 })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erro ao excluir recompensa', life: 5000 })
  } finally {
    confirmDeleteRecompensaLoading.value = false
    confirmDeleteRecompensaVisible.value = false
    recompensaParaExcluir.value = null
  }
}

function cancelarExclusaoRecompensa() {
  confirmDeleteRecompensaVisible.value = false
  recompensaParaExcluir.value = null
}

function limparPesquisaRecompensa() {
  filtroPesquisaRecompensa.value = ''
  popoverPesquisaRecompensaRef.value?.hide()
}

watch(
  () => props.leitor,
  (novo) => {
    if (novo) {
      tabAtiva.value = 'leitor'
      preencherFormComLeitor(novo)
    } else {
      form.value = getFormDefault()
    }
  },
  { immediate: true }
)

watch(tabAtiva, (valor) => {
  if (valor === 'emprestimo' && leitorId.value) carregarEmprestimos()
  if (valor === 'reservas' && leitorId.value) carregarReservas()
  if (valor === 'recompensas') carregarRecompensas()
})
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
  padding: 0;
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

.dialog-row .dialog-field {
  flex: 1;
  margin-bottom: 1rem;
}

.dialog-input {
  flex: 1;
  width: 100%;
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

.dialog-autor-table {
  margin-top: 1rem;
}

.dialog-col-acoes {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
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

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.dialog-actions--inside-tab {
  margin-top: 0.5rem;
}

.dialog-aviso {
  color: var(--texto-secundario);
  padding: 1rem;
  font-style: italic;
}

</style>
