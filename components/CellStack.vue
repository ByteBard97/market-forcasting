<template>
  <div class="cell-stack" :style="stackStyle">
    <slot />
  </div>
</template>

<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  gap: {
    type: String,
    default: '0.4rem'
  }
})

const slots = useSlots()

// Count the number of cells in the slot
const cellCount = computed(() => {
  const children = slots.default?.() || []
  return children.length || 1
})

const stackStyle = computed(() => ({
  display: 'grid',
  gridTemplateRows: `repeat(${cellCount.value}, 1fr)`,
  gap: props.gap,
  height: '100%',
  minHeight: 0,
  containerType: 'size' // Enable cqh for cells
}))
</script>

<style scoped>
.cell-stack {
  width: 100%;
  overflow: hidden;
}
</style>
