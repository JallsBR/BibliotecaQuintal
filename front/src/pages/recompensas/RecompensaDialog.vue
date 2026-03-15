<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    :header="recompensaEditando ? 'Editar recompensa' : 'Nova recompensa'"
    :style="{ width: '36rem' }"
    :contentStyle="{ overflow: 'visible' }"
    @hide="limparFormulario"
  >
    <div class="dialog-body">
      <div class="dialog-row">
        <div class="dialog-field dialog-field--full">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <InputText
              id="rec-nome"
              v-model="form.nome"
              class="dialog-input"
              maxlength="100"
            />
            <label for="rec-nome">Nome <span class="dialog-required">*</span></label>
          </FloatLabel>
        </div>
      </div>
      <div class="dialog-row">
        <div class="dialog-field dialog-field--full">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <Textarea
              id="rec-descricao"
              v-model="form.descricao"
              class="dialog-input"
              rows="3"
              autoResize
            />
            <label for="rec-descricao">Descrição</label>
          </FloatLabel>
        </div>
      </div>
      <div class="dialog-row">
        <div class="dialog-field">
          <FloatLabel variant="on" class="dialog-input-wrap">
            <InputNumber
              id="rec-pontuacao"
              v-model="form.pontuacao"
              :min="0"
              class="dialog-input"
            />
            <label for="rec-pontuacao">Pontuação</label>
          </FloatLabel>
        </div>
        <div class="dialog-field dialog-field--checkbox">
          <div class="checkbox-wrap">
            <Checkbox v-model="form.ativo" :binary="true" inputId="rec-ativo" />
            <label for="rec-ativo">Ativo</label>
          </div>
        </div>
      </div>
      <div class="dialog-row dialog-row--acoes">
        <Button type="button" label="Salvar" size="small" :loading="salvando" @click="salvar" />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import Dialog from 'primevue/dialog'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import leitorService from '@/services/leitorService'

const props = defineProps({
  visible: { type: Boolean, default: false },
  recompensa: { type: Object, default: null }
})

const emit = defineEmits(['update:visible', 'save'])

const visibleModel = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v)
})

const recompensaEditando = computed(() => props.recompensa != null && props.recompensa.id != null)

const toast = useToast()
const form = ref(getFormDefault())
const salvando = ref(false)

function getFormDefault() {
  return {
    nome: '',
    descricao: '',
    pontuacao: 0,
    ativo: true
  }
}

watch(
  () => [props.visible, props.recompensa],
  () => {
    if (props.visible && props.recompensa?.id) {
      form.value = {
        nome: props.recompensa.nome ?? '',
        descricao: props.recompensa.descricao ?? '',
        pontuacao: props.recompensa.pontuacao ?? 0,
        ativo: props.recompensa.ativo ?? true
      }
    } else if (props.visible) {
      form.value = getFormDefault()
    }
  },
  { immediate: true }
)

function limparFormulario() {
  form.value = getFormDefault()
}

async function salvar() {
  const nome = (form.value.nome ?? '').toString().trim()
  if (!nome) {
    toast.add({
      severity: 'warn',
      summary: 'Campos obrigatórios',
      detail: 'Informe o nome da recompensa.',
      life: 3000
    })
    return
  }
  salvando.value = true
  try {
    const payload = {
      nome,
      descricao: (form.value.descricao ?? '').toString().trim() || null,
      pontuacao: form.value.pontuacao ?? 0,
      ativo: form.value.ativo ?? true
    }
    if (recompensaEditando.value) {
      await leitorService.recompensas.update(props.recompensa.id, payload)
      toast.add({
        severity: 'success',
        summary: 'Recompensa atualizada',
        detail: 'A recompensa foi atualizada com sucesso.',
        life: 3000
      })
    } else {
      await leitorService.recompensas.create(payload)
      toast.add({
        severity: 'success',
        summary: 'Recompensa cadastrada',
        detail: 'A recompensa foi registrada com sucesso.',
        life: 3000
      })
    }
    emit('save')
    visibleModel.value = false
  } catch (e) {
    console.error('Erro ao salvar recompensa:', e)
    const data = e?.response?.data
    let detail = 'Não foi possível salvar a recompensa.'
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
    toast.add({ severity: 'error', summary: 'Erro ao salvar recompensa', detail, life: 5000 })
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

.dialog-field--full {
  flex: 1 1 100%;
}

.dialog-field--checkbox {
  display: flex;
  align-items: flex-end;
  padding-bottom: 0.5rem;
}

.checkbox-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
