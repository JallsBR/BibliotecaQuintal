<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    header="Leitor"
    :style="{ width: '65rem' }"
    :contentStyle="{ overflowY: 'auto', maxHeight: '100vh' }"
    @hide="aoFechar"
    @show="aoAbrirDialog"
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
                    <label for="leitor-nome">Nome <span class="dialog-required">*</span></label>
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
                    <label for="leitor-telefone">Telefone <span class="dialog-required">*</span></label>
                  </FloatLabel>
                </div>
              </div>
              <div class="dialog-row">
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <BaseSelect
                      v-model="form.sexo"
                      inputId="leitor-sexo"
                      :options="opcoesSexo"
                      optionLabel="label"
                      optionValue="value"
                      showClear
                      class="dialog-input"
                    />
                    <label for="leitor-sexo">Sexo</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-profissao" v-model="form.profissao" class="dialog-input" autocomplete="off" />
                    <label for="leitor-profissao">Profissão</label>
                  </FloatLabel>
                </div>
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText
                      id="leitor-cep"
                      v-model="form.cep"
                      class="dialog-input"
                      maxlength="10"
                      autocomplete="off"
                      @blur="buscarCep"
                    />
                    <label for="leitor-cep">CEP</label>
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
                    <InputText id="leitor-endereco" v-model="form.endereco" class="dialog-input" autocomplete="off" />
                    <label for="leitor-endereco">Endereço</label>
                  </FloatLabel>
                </div>                      
                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-complemento" v-model="form.complemento" class="dialog-input" autocomplete="off" />
                    <label for="leitor-complemento">Complemento</label>
                  </FloatLabel>
                </div>         
              </div>

              <div class="dialog-row">

                <div class="dialog-field">
                  <FloatLabel variant="on" class="dialog-input-wrap">
                    <InputText id="leitor-bairro" v-model="form.bairro" class="dialog-input" autocomplete="off" />
                    <label for="leitor-bairro">Bairro</label>
                  </FloatLabel>
                </div>
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
                      <DatePicker
                        v-model="emprestimoForm.data_emprestimo"
                        inputId="emp-data-emp"
                        dateFormat="dd/mm/yy"
                        showIcon
                        iconDisplay="input"
                        class="dialog-input"
                      />
                      <label for="emp-data-emp">Data empréstimo</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <DatePicker
                        v-model="emprestimoForm.data_devolucao"
                        inputId="emp-data-dev"
                        dateFormat="dd/mm/yy"
                        showIcon
                        iconDisplay="input"
                        class="dialog-input"
                      />
                      <label for="emp-data-dev">Data devolução</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field" style="max-width: 100px;">
                      <Checkbox id="emp-devolvido" v-model="emprestimoForm.devolvido" :binary="true" inputId="emp-devolvido" />
                      <label for="emp-devolvido">Devolvido</label>
                  </div>
                  <div class="dialog-row dialog-autor-row">
                  <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarEmprestimo" />
                </div>
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
                    <Column field="livro" header="Livro" sortable>
                      <template #body="slotProps">
                        {{ nomeLivro(slotProps.data.livro) }}
                      </template>
                    </Column>
                    <Column field="data_emprestimo" header="Data empréstimo" sortable>
                      <template #body="slotProps">
                        {{ formatarApenasData(slotProps.data.data_emprestimo) }}
                      </template>
                    </Column>
                    <Column field="data_devolucao" header="Data devolução" sortable>
                      <template #body="slotProps">
                        {{ formatarApenasData(slotProps.data.data_devolucao) }}
                      </template>
                    </Column>
                    <Column field="devolvido" header="Devolvido" sortable>
                      <template #body="slotProps">
                        {{ slotProps.data.devolvido ? 'Sim' : 'Não' }}
                      </template>
                    </Column>
                    <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }" bodyClass="dialog-col-acoes" headerClass="dialog-col-acoes">
                      <template #body="slotProps">
                        <div class="dialog-col-acoes">
                          <Button v-if="hasPermission('leitor.change_emprestimo')" label="Editar" size="small" @click="editarEmprestimo(slotProps.data)" />
                          <Button v-if="hasPermission('leitor.delete_emprestimo')" label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluirEmprestimo(slotProps.data)" />
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
                      <DatePicker
                        v-model="reservaForm.data_reserva"
                        inputId="res-data-reserva"
                        dateFormat="dd/mm/yy"
                        showIcon
                        iconDisplay="input"
                        class="dialog-input"
                      />
                      <label for="res-data-reserva">Data reserva</label>
                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <DatePicker
                        v-model="reservaForm.data_expiracao"
                        inputId="res-data-exp"
                        dateFormat="dd/mm/yy"
                        showIcon
                        iconDisplay="input"
                        class="dialog-input"
                      />
                      <label for="res-data-exp">Data expiração</label>
                    </FloatLabel>
                  </div>                
                  <div class="dialog-row dialog-autor-row">
                    <Button type="button" label="Salvar" size="small" class="dialog-autor-button" @click="salvarReserva" />
                  </div>
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
                    <Column field="livro" header="Livro" sortable>
                      <template #body="slotProps">
                        {{ nomeLivro(slotProps.data.livro) }}
                      </template>
                    </Column>
                    <Column field="data_reserva" header="Data reserva" sortable>
                      <template #body="slotProps">
                        {{ formatarApenasData(slotProps.data.data_reserva) }}
                      </template>
                    </Column>
                    <Column field="data_expiracao" header="Data expiração" sortable>
                      <template #body="slotProps">
                        {{ formatarApenasData(slotProps.data.data_expiracao) }}
                      </template>
                    </Column>
                    <Column header="Ações" :style="{ width: '180px', maxWidth: '180px' }" bodyClass="dialog-col-acoes" headerClass="dialog-col-acoes">
                      <template #body="slotProps">
                        <div class="dialog-col-acoes">
                          <Button v-if="hasPermission('leitor.change_reserva')" label="Editar" size="small" @click="editarReserva(slotProps.data)" />
                          <Button v-if="hasPermission('leitor.delete_reserva')" label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluirReserva(slotProps.data)" />
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

          <!-- Tab Recompensas: resgates do leitor (recompensa + data do resgate) -->
          <TabPanel value="recompensas">
            <div class="dialog-autor">
              <p v-if="!leitorId" class="texto-aviso">Salve o leitor antes de cadastrar resgates de recompensa.</p>
              <template v-else>
                <div class="dialog-row dialog-autor-row" style="margin-top: 1rem;">
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <BaseSelect
                        id="resgate-recompensa"
                        v-model="recompensaResgateForm.recompensa"
                        :options="recompensasFiltradas"
                        optionLabel="nome"
                        optionValue="id"
                        showClear
                        placeholder="Selecione a recompensa"
                        class="dialog-input"
                      />

                    </FloatLabel>
                  </div>
                  <div class="dialog-field dialog-autor-field">
                    <FloatLabel variant="on" class="dialog-input-wrap">
                      <DatePicker
                        id="resgate-data"
                        v-model="recompensaResgateForm.data_resgate"
                        dateFormat="dd/mm/yy"
                        showIcon
                        iconDisplay="input"
                        class="dialog-input"
                      />
                      <label for="resgate-data">Data do resgate</label>
                    </FloatLabel>
                  </div>
                  <Button type="button" :label="resgateEditandoId ? 'Atualizar' : 'Resgatar'" size="small" class="dialog-autor-button" @click="salvarRecompensaResgate" />
                  <Button v-if="resgateEditandoId" type="button" label="Cancelar" severity="secondary" size="small" class="dialog-autor-button" @click="cancelarEdicaoResgate" />
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
                  :items="recompensasResgatadasLista"
                  :loading="loadingRecompensasResgatadas"
                  dataKey="id"
                  :totalRecords="recompensasResgatadasLista.length"
                  :rows="recompensasRows"
                  :lazy="false"
                  :reorderableColumns="false"
                  class="dialog-autor-table"
                >
                  <template #columns>
                    <Column field="recompensa_nome" header="Nome" sortable />
                    <Column field="recompensa_descricao" header="Descrição" sortable />
                    <Column field="recompensa_pontuacao" header="Pontuação" sortable :style="{ width: '150px', maxWidth: '150px' }" />
                    <Column field="data_resgate" header="Data resgate" sortable :style="{ width: '150px', maxWidth: '150px' }">
                      <template #body="slotProps">
                        {{ formatarApenasData(slotProps.data.data_resgate) }}
                      </template>
                    </Column>
                    <Column header="Ações" :style="{ width: '160px', maxWidth: '160px' }" bodyClass="dialog-col-acoes" headerClass="dialog-col-acoes">
                      <template #body="slotProps">
                        <div class="dialog-col-acoes">
                          <Button v-if="hasPermission('leitor.delete_recompensa')" label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluirResgate(slotProps.data)" />
                        </div>
                      </template>
                    </Column>
                  </template>
                </BaseDataTable>
                <BaseConfirmDialog
                  :visible="confirmDeleteResgateVisible"
                  title="Excluir resgate"
                  :message="confirmDeleteResgateMessage"
                  confirmLabel="Excluir"
                  cancelLabel="Cancelar"
                  confirmSeverity="danger"
                  :loading="confirmDeleteResgateLoading"
                  @update:visible="(v) => (confirmDeleteResgateVisible = v)"
                  @confirm="confirmarExclusaoResgate"
                  @cancel="cancelarExclusaoResgate"
                />
              </template>
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
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

const emit = defineEmits(['update:visible', 'save', 'hide'])

const visibleModel = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v)
})

const tabAtiva = ref('leitor')
const form = ref(getFormDefault())
const opcoesLivros = ref([])

const opcoesSexo = [
  { value: 'M', label: 'Masculino' },
  { value: 'F', label: 'Feminino' },
  { value: 'O', label: 'Outro' }
]

/** Normaliza sexo para o valor esperado pela API (M, F, O). Aceita label vindo do backend. */
function normalizarSexo(val) {
  if (val == null || val === '') return null
  const labelToValue = { Masculino: 'M', Feminino: 'F', Outro: 'O' }
  return labelToValue[val] ?? val
}

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

// Recompensas: catálogo (para seleção) e resgates do leitor
const opcoesRecompensas = ref([])
const recompensasResgatadasLista = ref([])
const loadingRecompensasResgatadas = ref(false)
const loadingCatalogoRecompensas = ref(false)
const recompensasRows = 10
const resgateEditandoId = ref(null)
const recompensaResgateForm = ref(getRecompensaResgateFormDefault())
const popoverPesquisaRecompensaRef = ref(null)
const filtroPesquisaRecompensa = ref('')

const confirmDeleteResgateVisible = ref(false)
const confirmDeleteResgateLoading = ref(false)
const resgateParaExcluir = ref(null)
const confirmDeleteResgateMessage = computed(() => {
  if (!resgateParaExcluir.value) return 'Confirma a exclusão deste resgate?'
  return `Excluir o resgate de "${resgateParaExcluir.value.recompensa_nome}"?`
})

const recompensasFiltradas = computed(() => {
  const lista = opcoesRecompensas.value ?? []
  const termo = filtroPesquisaRecompensa.value?.trim().toLowerCase() || ''
  if (!termo) return lista
  return lista.filter((r) => (r.nome || '').toLowerCase().includes(termo) || (r.descricao || '').toLowerCase().includes(termo))
})

function getRecompensaResgateFormDefault() {
  return { recompensa: null, data_resgate: new Date() }
}

const toast = useToast()
const loadingCep = ref(false)

function normalizarCep(cep) {
  if (!cep || typeof cep !== 'string') return ''
  return cep.replace(/\D/g, '').slice(0, 8)
}

async function buscarCep() {
  const cepLimpo = normalizarCep(form.value.cep)
  if (cepLimpo.length !== 8) return
  loadingCep.value = true
  try {
    const data = await leitorService.cep.consultar(cepLimpo)
    if (data) {
      form.value.endereco = data.endereco ?? form.value.endereco
      form.value.complemento = data.complemento ?? form.value.complemento
      form.value.bairro = data.bairro ?? form.value.bairro
      form.value.cidade = data.cidade ?? form.value.cidade
      form.value.estado = data.estado ?? form.value.estado
      if (data.cep_formatado) form.value.cep = data.cep_formatado
      toast.add({ severity: 'success', summary: 'Endereço preenchido', detail: 'CEP encontrado.', life: 2000 })
    } else {
      toast.add({ severity: 'warn', summary: 'CEP não encontrado', detail: 'Verifique o CEP e tente novamente.', life: 4000 })
    }
  } catch (e) {
    const msg = e?.response?.data?.detail || e?.message || 'Erro ao consultar CEP.'
    toast.add({ severity: 'error', summary: 'Erro ao buscar CEP', detail: msg, life: 5000 })
  } finally {
    loadingCep.value = false
  }
}

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
  return { livro: null, data_emprestimo: new Date(), data_devolucao: null, devolvido: false }
}

function getReservaFormDefault() {
  return { livro: null, data_reserva: new Date(), data_expiracao: null }
}

function preencherFormComLeitor(leitor) {
  if (!leitor) {
    form.value = getFormDefault()
    return
  }
  const dataNasc = parseDateLocal(leitor.data_nascimento)
  form.value = {
    id: leitor.id,
    nome: leitor.nome ?? '',
    email: leitor.email ?? '',
    data_nascimento: dataNasc,
    cpf: leitor.cpf ?? '',
    telefone: leitor.telefone ?? '',
    sexo: normalizarSexo(leitor.sexo) ?? '',
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

/** Converte Date ou string para YYYY-MM-DD (apenas data para a API). */
function toDateOnly(val) {
  if (!val) return null
  const d = val instanceof Date ? val : new Date(val)
  if (isNaN(d.getTime())) return null
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

/** Parse da API (YYYY-MM-DD ou ISO) para Date em horário local (evita deslocamento no DatePicker). */
function parseDateLocal(val) {
  if (!val) return null
  if (val instanceof Date) return val
  const s = typeof val === 'string' ? val.slice(0, 10) : val
  const [y, m, d] = String(s).split('-').map(Number)
  if (!y || !m || !d) return null
  const date = new Date(y, m - 1, d)
  return isNaN(date.getTime()) ? null : date
}

function formatarData(val) {
  if (!val) return ''
  const d = new Date(val)
  if (isNaN(d.getTime())) return String(val)
  return d.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}

function formatarApenasData(val) {
  if (!val) return ''
  const d = parseDateLocal(val) || new Date(val)
  if (isNaN(d.getTime())) return String(val)
  return d.toLocaleDateString('pt-BR', { dateStyle: 'short' })
}

function nomeLivro(livroId) {
  if (!livroId) return ''
  const livro = opcoesLivros.value.find((l) => l.id === livroId)
  return livro?.titulo ?? livroId
}

async function aoAbrirDialog() {
  if (props.leitor) {
    tabAtiva.value = 'leitor'
    preencherFormComLeitor(props.leitor)
  }
  await carregarOpcoes()
}

async function carregarOpcoes() {
  try {
    const [livros, recompensasCatalog] = await Promise.all([
      livroService.livros.getAll(),
      leitorService.recompensas.getAll({ ativo: true })
    ])
    const listaLivros = Array.isArray(livros) ? livros : livros?.results ?? []
    opcoesLivros.value = listaLivros
    opcoesRecompensas.value = Array.isArray(recompensasCatalog) ? recompensasCatalog : recompensasCatalog?.results ?? []
    if (leitorId.value) {
      await Promise.all([carregarEmprestimos(), carregarReservas(), carregarRecompensasResgatadas()])
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

async function carregarRecompensasResgatadas() {
  if (!leitorId.value) return
  loadingRecompensasResgatadas.value = true
  try {
    const data = await leitorService.leitorRecompensas.getAll({ leitor: leitorId.value })
    recompensasResgatadasLista.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar resgates:', e)
    recompensasResgatadasLista.value = []
  } finally {
    loadingRecompensasResgatadas.value = false
  }
}

function aoFechar() {
  limparFormulario()
  emit('hide')
}

function limparFormulario() {
  form.value = getFormDefault()
  emprestimoForm.value = getEmprestimoFormDefault()
  reservaForm.value = getReservaFormDefault()
  recompensaResgateForm.value = getRecompensaResgateFormDefault()
  emprestimoEditandoId.value = null
  reservaEditandoId.value = null
  resgateEditandoId.value = null
  tabAtiva.value = 'leitor'
}

function salvar() {
  const nome = (form.value.nome || '').trim()
  const telefone = (form.value.telefone || '').trim()
  if (!nome || !telefone) {
    toast.add({
      severity: 'warn',
      summary: 'Campos obrigatórios',
      detail: 'Informe pelo menos o nome e o telefone do leitor.',
      life: 3000
    })
    return
  }
  const dataNascStr = toDateOnly(form.value.data_nascimento)
  const payload = {
    nome: nome || null,
    email: form.value.email || null,
    data_nascimento: dataNascStr,
    cpf: form.value.cpf || null,
    telefone: telefone || null,
    sexo: normalizarSexo(form.value.sexo) || null,
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
    const dataEmp = emprestimoForm.value.data_emprestimo || new Date()
    let dataDev = emprestimoForm.value.data_devolucao || null
    if (emprestimoForm.value.devolvido && !dataDev) dataDev = new Date()

    const payload = {
      leitor: leitorId.value,
      livro: emprestimoForm.value.livro,
      data_emprestimo: toDateOnly(dataEmp),
      data_devolucao: dataDev ? toDateOnly(dataDev) : null,
      devolvido: !!emprestimoForm.value.devolvido
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
    const data = e?.response?.data
    let detail = 'Não foi possível salvar.'
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
  }
}

function editarEmprestimo(emp) {
  emprestimoEditandoId.value = emp.id
  emprestimoForm.value = {
    livro: emp.livro,
    data_emprestimo: parseDateLocal(emp.data_emprestimo),
    data_devolucao: parseDateLocal(emp.data_devolucao),
    devolvido: !!emp.devolvido
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
    const hoje = new Date()
    const payload = {
      leitor: leitorId.value,
      livro: reservaForm.value.livro,
      data_reserva: toDateOnly(reservaForm.value.data_reserva) || toDateOnly(hoje),
      data_expiracao: reservaForm.value.data_expiracao ? toDateOnly(reservaForm.value.data_expiracao) : null
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
    data_reserva: parseDateLocal(res.data_reserva),
    data_expiracao: parseDateLocal(res.data_expiracao)
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

async function salvarRecompensaResgate() {
  if (!leitorId.value || !recompensaResgateForm.value.recompensa) {
    toast.add({ severity: 'warn', summary: 'Campo obrigatório', detail: 'Selecione a recompensa.', life: 3000 })
    return
  }
  const dataResgate = recompensaResgateForm.value.data_resgate || new Date()
  try {
    const payload = {
      leitor: leitorId.value,
      recompensa: recompensaResgateForm.value.recompensa,
      data_resgate: typeof dataResgate === 'object' && dataResgate instanceof Date
        ? `${dataResgate.getFullYear()}-${String(dataResgate.getMonth() + 1).padStart(2, '0')}-${String(dataResgate.getDate()).padStart(2, '0')}`
        : dataResgate
    }
    if (resgateEditandoId.value) {
      await leitorService.leitorRecompensas.update(resgateEditandoId.value, payload)
      toast.add({ severity: 'success', summary: 'Data do resgate atualizada', life: 3000 })
    } else {
      await leitorService.leitorRecompensas.create(payload)
      toast.add({ severity: 'success', summary: 'Resgate cadastrado', life: 3000 })
    }
    recompensaResgateForm.value = getRecompensaResgateFormDefault()
    resgateEditandoId.value = null
    await carregarRecompensasResgatadas()
  } catch (e) {
    const detail = e?.response?.data?.recompensa?.[0] ?? e?.response?.data?.detail ?? 'Não foi possível salvar.'
    toast.add({ severity: 'error', summary: 'Erro ao salvar resgate', detail, life: 5000 })
  }
}

function editarResgateData(resgate) {
  resgateEditandoId.value = resgate.id
  const dataResgate = resgate.data_resgate
  const dataObj = dataResgate
    ? (typeof dataResgate === 'string' ? new Date(dataResgate + 'T12:00:00') : dataResgate)
    : new Date()
  recompensaResgateForm.value = {
    recompensa: resgate.recompensa,
    data_resgate: dataObj
  }
}

function cancelarEdicaoResgate() {
  resgateEditandoId.value = null
  recompensaResgateForm.value = getRecompensaResgateFormDefault()
}

function abrirConfirmacaoExcluirResgate(resgate) {
  resgateParaExcluir.value = resgate
  confirmDeleteResgateVisible.value = true
}

async function confirmarExclusaoResgate() {
  if (!resgateParaExcluir.value) return
  confirmDeleteResgateLoading.value = true
  try {
    await leitorService.leitorRecompensas.delete(resgateParaExcluir.value.id)
    await carregarRecompensasResgatadas()
    toast.add({ severity: 'success', summary: 'Resgate excluído', life: 3000 })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erro ao excluir resgate', life: 5000 })
  } finally {
    confirmDeleteResgateLoading.value = false
    confirmDeleteResgateVisible.value = false
    resgateParaExcluir.value = null
  }
}

function cancelarExclusaoResgate() {
  confirmDeleteResgateVisible.value = false
  resgateParaExcluir.value = null
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
  if (valor === 'recompensas' && leitorId.value) carregarRecompensasResgatadas()
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

.dialog-required {
  color: var(--p-danger);
}

.texto-aviso {
  color: var(--texto-secundario);
  font-size: 0.9375rem;
  margin: 1rem 0;
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
