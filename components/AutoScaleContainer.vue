<template>
  <div ref="container" class="auto-scale-container">
    <div ref="content" class="auto-scale-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const container = ref(null)
const content = ref(null)

const props = defineProps({
  scaleWidth: {
    type: Boolean,
    default: false
  }
})

function scaleToFit() {
  if (!container.value || !content.value) return

  // Reset transform to get natural size
  content.value.style.transform = 'none'

  const containerHeight = container.value.clientHeight
  const contentHeight = content.value.scrollHeight

  // Only scale height unless scaleWidth is true
  const scaleY = containerHeight / contentHeight
  const scale = Math.min(scaleY, 1) // Never scale up, only down

  content.value.style.transform = `scaleY(${scale})`
  content.value.style.transformOrigin = 'top center'
}

onMounted(() => {
  // Initial scale after a brief delay to ensure layout is settled
  setTimeout(scaleToFit, 50)

  // Rescale on window resize
  window.addEventListener('resize', scaleToFit)

  // Watch for content changes (optional but helpful)
  const observer = new ResizeObserver(scaleToFit)
  if (content.value) {
    observer.observe(content.value)
  }

  onUnmounted(() => {
    window.removeEventListener('resize', scaleToFit)
    observer.disconnect()
  })
})
</script>

<style scoped>
.auto-scale-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
}

.auto-scale-content {
  width: fit-content;
  height: fit-content;
  transform-origin: top left;
}
</style>
