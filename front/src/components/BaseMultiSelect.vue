<template>
  <MultiSelect
    ref="multiSelectRef"
    v-bind="multiSelectProps"
    v-on="multiSelectListeners"
    @click="onClick"
  />
</template>

<script setup>
import { ref, useAttrs, computed } from 'vue'
import MultiSelect from 'primevue/multiselect'

const attrs = useAttrs()

const multiSelectRef = ref(null)

const multiSelectProps = computed(() => ({
  filter: true,
  filterPlaceholder: 'Buscar...',
  filterMatchMode: 'contains',
  display: 'chip',
  ...attrs
}))

const multiSelectListeners = {}

function onClick(event) {
  const t = event.target
  const isInput = t.tagName === 'INPUT'
  const isComboboxSpan = t.tagName === 'SPAN' && t.getAttribute('role') === 'combobox'
  if ((isInput || isComboboxSpan) && multiSelectRef.value?.show) {
    multiSelectRef.value.show(true)
  }
}
</script>
