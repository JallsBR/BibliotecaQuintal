<template>
  <Select
    ref="selectRef"
    v-bind="selectProps"
    v-on="selectListeners"
    @click="onClick"
  />
</template>

<script setup>
import { ref, useAttrs, computed } from 'vue'
import Select from 'primevue/select'

const attrs = useAttrs()

const selectRef = ref(null)

const selectProps = computed(() => ({
  filter: true,
  filterPlaceholder: 'Buscar...',
  filterMatchMode: 'contains',
  ...attrs
}))

const selectListeners = {}

function onClick(event) {
  const t = event.target
  const isInput = t.tagName === 'INPUT'
  const isComboboxSpan = t.tagName === 'SPAN' && t.getAttribute('role') === 'combobox'
  if ((isInput || isComboboxSpan) && selectRef.value?.show) {
    selectRef.value.show(true)
  }
}
</script>
