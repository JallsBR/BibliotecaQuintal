<template>
  <div class="page">
    <h1 class="page-title">Configuração</h1>
    <p class="page-subtitle">Grupos e permissões do sistema.</p>

    <Tabs v-model:value="tabAtiva" class="config-tabs">
      <TabList>
        <Tab value="usuarios">Usuários</Tab>
        <Tab value="grupos-usuario">Grupos do usuário</Tab>
        <Tab value="grupos">Grupos</Tab>
        <Tab value="permissoes">Permissões</Tab>
      </TabList>
      <TabPanels>
        <TabPanel value="usuarios">
          <div class="tab-content">
            <p class="tab-desc">Usuários do sistema. Edite para alterar grupos, staff e autenticação em dois fatores.</p>
            <BaseDataTable
              :items="usuarios"
              :loading="loadingUsuarios"
              dataKey="id"
              :totalRecords="usuarios.length"
              :rows="20"
              :lazy="false"
              :reorderableColumns="false"
            >
              <template #columns>
                <Column field="username" header="Usuário" sortable />
                <Column field="email" header="E-mail" sortable />
                <Column header="Staff" :style="{ width: '80px' }">
                  <template #body="slotProps">
                    <span v-if="slotProps.data.is_staff">Sim</span>
                    <span v-else>—</span>
                  </template>
                </Column>
                <Column header="2FA" :style="{ width: '80px' }">
                  <template #body="slotProps">
                    <span v-if="slotProps.data.two_factor_enabled">Sim</span>
                    <span v-else>—</span>
                  </template>
                </Column>
                <Column header="Grupos">
                  <template #body="slotProps">
                    {{ (slotProps.data.groups_detail || []).map(g => g.name).join(', ') || '—' }}
                  </template>
                </Column>
                <Column header="Ações" :style="{ width: '100px' }">
                  <template #body="slotProps">
                    <Button v-if="hasPermission('users.change_user')" label="Editar" size="small" @click="abrirEditarUsuario(slotProps.data)" />
                  </template>
                </Column>
              </template>
            </BaseDataTable>
          </div>
        </TabPanel>
        <TabPanel value="grupos-usuario">
          <div class="tab-content">
            <p class="tab-desc">Para cada grupo, gerencie quais usuários pertencem a ele.</p>
            <BaseDataTable
              :items="gruposParaUsuario"
              :loading="loadingGrupos"
              dataKey="id"
              :totalRecords="gruposParaUsuario.length"
              :rows="20"
              :lazy="false"
              :reorderableColumns="false"
            >
              <template #columns>
                <Column field="name" header="Grupo" sortable />
                <Column header="Usuários no grupo">
                  <template #body="slotProps">
                    {{ (slotProps.data.user_count ?? 0) }} usuário(s)
                  </template>
                </Column>
                <Column header="Ações" :style="{ width: '180px' }">
                  <template #body="slotProps">
                    <Button v-if="hasPermission('auth.change_group')" label="Gerenciar usuários" size="small" @click="abrirGerenciarUsuarios(slotProps.data)" />
                  </template>
                </Column>
              </template>
            </BaseDataTable>
          </div>
        </TabPanel>
        <TabPanel value="grupos">
          <div class="tab-content">
            <div class="table-toolbar">
              <Button v-if="hasPermission('auth.add_group')" label="Novo grupo" size="small" icon="pi pi-plus" @click="abrirDialogGrupo" />
            </div>
            <BaseDataTable
              :items="grupos"
              :loading="loadingGrupos"
              dataKey="id"
              :totalRecords="grupos.length"
              :rows="20"
              :lazy="false"
              :reorderableColumns="false"
            >
              <template #columns>
                <Column field="name" header="Nome" sortable />
                <Column header="Permissões" :style="{ width: '400px' }">
                  <template #body="slotProps">
                    {{ (slotProps.data.permissions_detail?.length ?? 0) }} permissão(ões)
                  </template>
                </Column>
                <Column header="Ações" :style="{ width: '280px' }">
                  <template #body="slotProps">
                    <div class="col-acoes">
                      <Button v-if="hasPermission('auth.change_group')" label="Editar" size="small" @click="editarGrupo(slotProps.data)" />
                      <Button v-if="hasPermission('auth.change_group')" label="Permissões" size="small" @click="abrirDialogPermissoesGrupo(slotProps.data)" />
                      <Button v-if="hasPermission('auth.delete_group')" label="Excluir" severity="danger" size="small" @click="abrirConfirmacaoExcluir(slotProps.data)" />
                    </div>
                  </template>
                </Column>
              </template>
            </BaseDataTable>
          </div>
        </TabPanel>
        <TabPanel value="permissoes">
          <div class="tab-content">
            <p class="tab-desc">Lista de permissões disponíveis no sistema (somente leitura).</p>
            <BaseDataTable
              :items="permissoesAgrupadas"
              :loading="loadingPermissoes"
              dataKey="id"
              :totalRecords="permissoes.length"
              :rows="50"
              :lazy="false"
              :reorderableColumns="false"
            >
              <template #columns>
                <Column field="content_type_name" header="Modelo / App" sortable />
                <Column field="name" header="Nome" sortable />
                <Column field="codename" header="Código" sortable :style="{ width: '180px' }" />
              </template>
            </BaseDataTable>
          </div>
        </TabPanel>

      </TabPanels>
    </Tabs>

    <Dialog
      v-model:visible="dialogGrupoVisible"
      :header="grupoEditando ? 'Editar grupo' : 'Novo grupo'"
      modal
      :style="{ width: '36rem' }"
      :contentStyle="{ overflow: 'visible' }"
      @hide="limparFormGrupo"
    >
      <div class="dialog-body">
        <div class="dialog-row">
          <div class="dialog-field dialog-field--full">
            <FloatLabel variant="on" class="dialog-input-wrap">
              <InputText id="grupo-nome" v-model="formGrupo.name" class="dialog-input" maxlength="150" />
              <label for="grupo-nome">Nome <span class="dialog-required">*</span></label>
            </FloatLabel>
          </div>
        </div>
        <div class="dialog-row dialog-row--acoes">
          <Button type="button" label="Salvar" size="small" :loading="salvando" @click="salvarGrupo" />
        </div>
      </div>
    </Dialog>

    <Dialog
      v-model:visible="dialogPermissoesGrupoVisible"
      :header="grupoPermissoesEditando ? `Permissões: ${grupoPermissoesEditando.name}` : 'Permissões'"
      modal
      :style="{ width: '70rem', }"
      :contentStyle="{ overflow: 'visible', maxHeight: '80vh' }"
      @hide="limparDialogPermissoesGrupo"
    >
      <div class="dialog-body dialog-permissoes-body">
        <div class="dialog-permissoes-lista dialog-permissoes-grid">
          <div
            v-for="perm in permissoes"
            :key="perm.id"
            class="dialog-permissao-item"
          >
            <Checkbox
              :modelValue="formPermissoesGrupo.includes(perm.id)"
              :binary="true"
              :inputId="`perm-${perm.id}`"
              @update:modelValue="(v) => togglePermissaoGrupo(perm.id, v)"
            />
            <label :for="`perm-${perm.id}`" class="dialog-permissao-label">{{ nomePermissaoPt(perm.name) }}</label>
          </div>
        </div>
        <div class="dialog-row dialog-row--acoes">
          <Button type="button" label="Salvar" size="small" :loading="salvandoPermissoesGrupo" @click="salvarPermissoesGrupo" />
        </div>
      </div>
    </Dialog>

    <Dialog
      v-model:visible="dialogUsuarioVisible"
      header="Editar usuário"
      modal
      :style="{ width: '36rem' }"
      :contentStyle="{ overflow: 'visible' }"
      @hide="limparFormUsuario"
    >
      <div class="dialog-body">
        <div class="dialog-row" v-if="usuarioEditando">
          <div class="dialog-field dialog-field--full">
            <span class="dialog-readonly">{{ usuarioEditando.email }}</span>
          </div>
        </div>
        <div class="dialog-row">
          <div class="dialog-field dialog-field--full">
            <label class="dialog-label">Grupos</label>
            <MultiSelect
              v-model="formUsuario.groups"
              :options="grupos"
              optionLabel="name"
              optionValue="id"
              placeholder="Selecione os grupos"
              class="dialog-input w-full"
              :filter="true"
              filterPlaceholder="Buscar..."
            />
          </div>
        </div>
        <div class="dialog-row">
          <div class="dialog-field dialog-field--full">
            <div class="flex align-items-center gap-4 flex-wrap">
              <div class="flex align-items-center gap-2">
                <Checkbox v-model="formUsuario.is_staff" inputId="usuario-is-staff" :binary="true" />
                <label for="usuario-is-staff">Staff (acesso ao painel)</label>
              </div>
              <div class="flex align-items-center gap-2">
                <Checkbox
                  v-model="formUsuario.two_factor_enabled"
                  inputId="usuario-two-factor"
                  :binary="true"
                />
                <label for="usuario-two-factor">Autenticação em dois fatores (e-mail)</label>
              </div>
            </div>
          </div>
        </div>
        <div class="dialog-row dialog-row--acoes">
          <Button type="button" label="Salvar" size="small" :loading="salvandoUsuario" @click="salvarUsuario" />
        </div>
      </div>
    </Dialog>

    <Dialog
      v-model:visible="dialogGrupoUsuariosVisible"
      :header="grupoUsuariosEditando ? `Usuários no grupo: ${grupoUsuariosEditando.name}` : 'Gerenciar usuários'"
      modal
      :style="{ width: '36rem' }"
      :contentStyle="{ overflow: 'visible' }"
      @hide="limparFormGrupoUsuarios"
      @show="carregarUsuariosDoGrupo"
    >
      <div class="dialog-body">
        <div class="dialog-row">
          <div class="dialog-field dialog-field--full">
            <label class="dialog-label">Usuários neste grupo</label>
            <MultiSelect
              v-model="formGrupoUsuarios.user_ids"
              :options="listaUsuariosParaGrupo"
              optionLabel="email"
              optionValue="id"
              placeholder="Selecione os usuários"
              class="dialog-input w-full"
              :filter="true"
              filterPlaceholder="Buscar..."
            />
          </div>
        </div>
        <div class="dialog-row dialog-row--acoes">
          <Button type="button" label="Salvar" size="small" :loading="salvandoGrupoUsuarios" @click="salvarGrupoUsuarios" />
        </div>
      </div>
    </Dialog>

    <BaseConfirmDialog
      v-model:visible="confirmDeleteVisible"
      title="Excluir grupo"
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
import { ref, onMounted, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'

const store = useStore()
const hasPermission = (perm) => store.getters.hasPermission(perm)
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import BaseDataTable from '@/components/BaseDataTable.vue'
import BaseConfirmDialog from '@/components/BaseConfirmDialog.vue'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import Checkbox from 'primevue/checkbox'
import configService from '@/services/configService'

const toast = useToast()
const tabAtiva = ref('grupos')
const grupos = ref([])
const permissoes = ref([])
const usuarios = ref([])
const loadingGrupos = ref(false)
const loadingPermissoes = ref(false)
const loadingUsuarios = ref(false)
const dialogGrupoVisible = ref(false)
const grupoEditando = ref(null)
const formGrupo = ref({ name: '', permissions: [] })
const salvando = ref(false)
const confirmDeleteVisible = ref(false)
const confirmDeleteLoading = ref(false)
const grupoParaExcluir = ref(null)
const dialogUsuarioVisible = ref(false)
const usuarioEditando = ref(null)
const formUsuario = ref({ groups: [], is_staff: false, two_factor_enabled: false })
const salvandoUsuario = ref(false)
const dialogGrupoUsuariosVisible = ref(false)
const grupoUsuariosEditando = ref(null)
const formGrupoUsuarios = ref({ user_ids: [] })
const listaUsuariosParaGrupo = ref([])
const salvandoGrupoUsuarios = ref(false)
const dialogPermissoesGrupoVisible = ref(false)
const grupoPermissoesEditando = ref(null)
const formPermissoesGrupo = ref([])
const salvandoPermissoesGrupo = ref(false)

const permissoesAgrupadas = computed(() => permissoes.value)
const gruposParaUsuario = computed(() => grupos.value)
const confirmDeleteMessage = computed(() => {
  if (!grupoParaExcluir.value) return 'Confirma a exclusão deste grupo?'
  return `Excluir o grupo "${grupoParaExcluir.value.name}"?`
})

async function carregarGrupos() {
  loadingGrupos.value = true
  try {
    const data = await configService.groups.getAll()
    grupos.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar grupos:', e)
    grupos.value = []
  } finally {
    loadingGrupos.value = false
  }
}

async function carregarPermissoes() {
  loadingPermissoes.value = true
  try {
    const data = await configService.permissions.getAll()
    permissoes.value = Array.isArray(data) ? data : (data?.results ?? [])
  } catch (e) {
    console.error('Erro ao carregar permissões:', e)
    permissoes.value = []
  } finally {
    loadingPermissoes.value = false
  }
}

function abrirDialogGrupo() {
  grupoEditando.value = null
  formGrupo.value = { name: '', permissions: [] }
  dialogGrupoVisible.value = true
}

function editarGrupo(grupo) {
  grupoEditando.value = grupo
  const permIds = (grupo.permissions_detail ?? grupo.permissions ?? []).map((p) => (typeof p === 'object' ? p.id : p))
  formGrupo.value = { name: grupo.name ?? '', permissions: permIds }
  dialogGrupoVisible.value = true
}

function limparFormGrupo() {
  formGrupo.value = { name: '', permissions: [] }
  grupoEditando.value = null
}

async function salvarGrupo() {
  const nome = (formGrupo.value.name ?? '').toString().trim()
  if (!nome) {
    toast.add({ severity: 'warn', summary: 'Campo obrigatório', detail: 'Informe o nome do grupo.', life: 3000 })
    return
  }
  salvando.value = true
  try {
    const payload = { name: nome, permissions: grupoEditando.value ? (formGrupo.value.permissions ?? []) : [] }
    if (grupoEditando.value?.id) {
      await configService.groups.update(grupoEditando.value.id, payload)
      toast.add({ severity: 'success', summary: 'Grupo atualizado', detail: 'O grupo foi atualizado com sucesso.', life: 3000 })
    } else {
      await configService.groups.create(payload)
      toast.add({ severity: 'success', summary: 'Grupo criado', detail: 'O grupo foi criado com sucesso.', life: 3000 })
    }
    dialogGrupoVisible.value = false
    await carregarGrupos()
  } catch (e) {
    console.error('Erro ao salvar grupo:', e)
    const detail = e?.response?.data
      ? typeof e.response.data === 'object'
        ? Object.entries(e.response.data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
            .join(' | ')
        : e.response.data
      : 'Não foi possível salvar o grupo.'
    toast.add({ severity: 'error', summary: 'Erro ao salvar', detail, life: 5000 })
  } finally {
    salvando.value = false
  }
}

function abrirConfirmacaoExcluir(grupo) {
  grupoParaExcluir.value = grupo
  confirmDeleteVisible.value = true
}

async function confirmarExclusao() {
  if (!grupoParaExcluir.value) return
  confirmDeleteLoading.value = true
  try {
    await configService.groups.delete(grupoParaExcluir.value.id)
    grupos.value = grupos.value.filter((g) => g.id !== grupoParaExcluir.value.id)
    toast.add({ severity: 'success', summary: 'Grupo excluído', detail: 'O grupo foi removido.', life: 3000 })
  } catch (e) {
    console.error('Erro ao excluir grupo:', e)
    const detail = e?.response?.data?.detail
      ? (Array.isArray(e.response.data.detail) ? e.response.data.detail[0] : e.response.data.detail)
      : 'Não foi possível excluir o grupo.'
    toast.add({ severity: 'error', summary: 'Erro ao excluir', detail, life: 5000 })
  } finally {
    confirmDeleteLoading.value = false
    confirmDeleteVisible.value = false
    grupoParaExcluir.value = null
  }
}

function cancelarExclusao() {
  confirmDeleteVisible.value = false
  grupoParaExcluir.value = null
}

function nomePermissaoPt(name) {
  if (!name || typeof name !== 'string') return name
  const modeloPt = {
    livro: 'Livro',
    autor: 'Autor',
    editora: 'Editora',
    categoria: 'Categoria',
    leitor: 'Leitor',
    emprestimo: 'Empréstimo',
    reserva: 'Reserva',
    recompensa: 'Recompensa',
    user: 'Usuário',
    group: 'Grupo',
    permission: 'Permissão',
    contenttype: 'Tipo de conteúdo',
    logentry: 'Registro de log'
  }
  let s = name
    .replace(/^Can add\s+/i, 'Pode adicionar ')
    .replace(/^Can change\s+/i, 'Pode alterar ')
    .replace(/^Can delete\s+/i, 'Pode excluir ')
    .replace(/^Can view\s+/i, 'Pode visualizar ')
  const modelo = s.split(/\s+/).pop()?.toLowerCase()
  if (modelo && modeloPt[modelo]) s = s.replace(new RegExp(`\\b${modelo}\\b`, 'i'), modeloPt[modelo])
  return s
}

function abrirDialogPermissoesGrupo(grupo) {
  grupoPermissoesEditando.value = grupo
  const permIds = (grupo.permissions_detail ?? grupo.permissions ?? []).map((p) => (typeof p === 'object' ? p.id : p))
  formPermissoesGrupo.value = [...permIds]
  dialogPermissoesGrupoVisible.value = true
}

function togglePermissaoGrupo(permId, checked) {
  if (checked) {
    if (!formPermissoesGrupo.value.includes(permId)) formPermissoesGrupo.value = [...formPermissoesGrupo.value, permId]
  } else {
    formPermissoesGrupo.value = formPermissoesGrupo.value.filter((id) => id !== permId)
  }
}

function limparDialogPermissoesGrupo() {
  grupoPermissoesEditando.value = null
  formPermissoesGrupo.value = []
}

async function salvarPermissoesGrupo() {
  if (!grupoPermissoesEditando.value?.id) return
  salvandoPermissoesGrupo.value = true
  try {
    await configService.groups.update(grupoPermissoesEditando.value.id, {
      name: grupoPermissoesEditando.value.name,
      permissions: formPermissoesGrupo.value
    })
    toast.add({ severity: 'success', summary: 'Permissões atualizadas', detail: 'As permissões do grupo foram salvas.', life: 3000 })
    dialogPermissoesGrupoVisible.value = false
    await carregarGrupos()
  } catch (e) {
    console.error('Erro ao salvar permissões do grupo:', e)
    const detail = e?.response?.data
      ? typeof e.response.data === 'object'
        ? Object.entries(e.response.data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
            .join(' | ')
        : e.response.data
      : 'Não foi possível salvar as permissões.'
    toast.add({ severity: 'error', summary: 'Erro ao salvar', detail, life: 5000 })
  } finally {
    salvandoPermissoesGrupo.value = false
  }
}

async function carregarUsuarios() {
  loadingUsuarios.value = true
  try {
    const data = await configService.users.getAll()
    usuarios.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (e) {
    console.error('Erro ao carregar usuários:', e)
    usuarios.value = []
  } finally {
    loadingUsuarios.value = false
  }
}

function abrirEditarUsuario(usuario) {
  usuarioEditando.value = usuario
  formUsuario.value = {
    groups: (usuario.groups ?? []).map((g) => (typeof g === 'object' ? g.id : g)),
    is_staff: !!usuario.is_staff,
    two_factor_enabled: !!usuario.two_factor_enabled
  }
  dialogUsuarioVisible.value = true
}

function limparFormUsuario() {
  formUsuario.value = { groups: [], is_staff: false, two_factor_enabled: false }
  usuarioEditando.value = null
}

async function salvarUsuario() {
  if (!usuarioEditando.value?.id) return
  salvandoUsuario.value = true
  try {
    await configService.users.update(usuarioEditando.value.id, {
      groups: formUsuario.value.groups ?? [],
      is_staff: formUsuario.value.is_staff,
      two_factor_enabled: formUsuario.value.two_factor_enabled
    })
    toast.add({ severity: 'success', summary: 'Usuário atualizado', detail: 'Alterações salvas com sucesso.', life: 3000 })
    dialogUsuarioVisible.value = false
    await carregarUsuarios()
  } catch (e) {
    console.error('Erro ao salvar usuário:', e)
    const detail = e?.response?.data
      ? typeof e.response.data === 'object'
        ? Object.entries(e.response.data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
            .join(' | ')
        : e.response.data
      : 'Não foi possível salvar o usuário.'
    toast.add({ severity: 'error', summary: 'Erro ao salvar', detail, life: 5000 })
  } finally {
    salvandoUsuario.value = false
  }
}

function abrirGerenciarUsuarios(grupo) {
  grupoUsuariosEditando.value = grupo
  formGrupoUsuarios.value = { user_ids: [] }
  listaUsuariosParaGrupo.value = []
  dialogGrupoUsuariosVisible.value = true
}

async function carregarUsuariosDoGrupo() {
  if (!grupoUsuariosEditando.value?.id) return
  try {
    const [usersRes, groupUsersRes] = await Promise.all([
      configService.users.getAll(),
      configService.groups.getUsers(grupoUsuariosEditando.value.id)
    ])
    const all = Array.isArray(usersRes) ? usersRes : usersRes?.results ?? []
    listaUsuariosParaGrupo.value = all
    formGrupoUsuarios.value = { user_ids: groupUsersRes?.user_ids ?? [] }
  } catch (e) {
    console.error('Erro ao carregar usuários do grupo:', e)
    listaUsuariosParaGrupo.value = []
  }
}

function limparFormGrupoUsuarios() {
  formGrupoUsuarios.value = { user_ids: [] }
  grupoUsuariosEditando.value = null
  listaUsuariosParaGrupo.value = []
}

async function salvarGrupoUsuarios() {
  if (!grupoUsuariosEditando.value?.id) return
  salvandoGrupoUsuarios.value = true
  try {
    await configService.groups.setUsers(grupoUsuariosEditando.value.id, formGrupoUsuarios.value.user_ids ?? [])
    toast.add({ severity: 'success', summary: 'Grupo atualizado', detail: 'Usuários do grupo salvos com sucesso.', life: 3000 })
    dialogGrupoUsuariosVisible.value = false
    await carregarGrupos()
    if (tabAtiva.value === 'usuarios') await carregarUsuarios()
  } catch (e) {
    console.error('Erro ao salvar usuários do grupo:', e)
    const detail = e?.response?.data?.detail ?? 'Não foi possível salvar.'
    toast.add({ severity: 'error', summary: 'Erro ao salvar', detail, life: 5000 })
  } finally {
    salvandoGrupoUsuarios.value = false
  }
}

watch(tabAtiva, (val) => {
  if (val === 'grupos') carregarGrupos()
  if (val === 'permissoes') carregarPermissoes()
  if (val === 'usuarios') carregarUsuarios()
  if (val === 'grupos-usuario') carregarGrupos()
})

onMounted(() => {
  carregarGrupos()
  carregarPermissoes()
  carregarUsuarios()
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
  color: var(--texto-secundario);
  margin: 0 0 1.5rem;
}

.config-tabs {
  padding: 0;
}

.config-tabs :deep(.p-tabs-nav) {
  border-radius: 12px 12px 0 0;
}

.config-tabs :deep(.p-tabs-panels) {
  padding-top: 1rem;
}

.tab-content {
  background: var(--bg-primario);
  border-radius: 12px;
  padding: 1.25rem;
}

.tab-desc {
  color: var(--texto-secundario);
  font-size: 0.9375rem;
  margin: 0 0 1rem;
}

.table-toolbar {
  margin-bottom: 1rem;
}

.col-acoes {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dialog-row {
  display: flex;
  gap: 1rem;
}

.dialog-field {
  flex: 1;
}

.dialog-field--full {
  flex: 1 1 100%;
}

.dialog-input-wrap {
  width: 100%;
}

.dialog-input {
  width: 100%;
}

.dialog-label {
  font-weight: 600;
  color: var(--texto-primario);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  display: block;
}

.dialog-row--acoes {
  margin-top: 0.5rem;
}

.dialog-required {
  color: var(--p-danger);
}

.dialog-readonly {
  font-size: 0.9375rem;
  color: var(--texto-secundario);
}

.dialog-permissoes-body {
  max-height: 60vh;
}

.dialog-permissoes-lista {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow-y: auto;
  max-height: 50vh;
  padding-right: 0.25rem;
}

.dialog-permissoes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem 1rem;
}

.dialog-permissao-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dialog-permissao-label {
  font-size: 0.9375rem;
  color: var(--texto-primario);
  cursor: pointer;
  user-select: none;
}
</style>
