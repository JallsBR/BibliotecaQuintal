<template>
  <Dialog
    v-model:visible="visibleModel"
    modal
    :header="title"
    :style="{ width: '30rem' }"
  >
    <p class="confirm-message">
      {{ message }}
    </p>

    <template #footer>
      <div class="confirm-actions">
        <Button
          type="button"
          :label="cancelLabel"
          severity="secondary"
          :disabled="loading"
          @click="onCancel"
        />
        <Button
          type="button"
          :label="confirmLabel"
          :severity="confirmSeverity"
          :loading="loading"
          @click="onConfirm"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'

const props = defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: 'Confirmação' },
  message: { type: String, default: 'Deseja realmente executar esta ação?' },
  confirmLabel: { type: String, default: 'Confirmar' },
  cancelLabel: { type: String, default: 'Cancelar' },
  confirmSeverity: { type: String, default: 'danger' },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['update:visible', 'confirm', 'cancel'])

const visibleModel = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v)
})

function onConfirm() {
  emit('confirm')
}

function onCancel() {
  emit('cancel')
  emit('update:visible', false)
}
</script>

<style scoped>
.confirm-message {
  margin: 0 0 1rem;
  color: var(--texto-primario);
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>

