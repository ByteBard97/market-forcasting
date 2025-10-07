import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// Global singleton state
const currentBackground = ref('datasphere')
const currentSlideNumber = ref(1)

export function useSlideBackground() {
  return {
    currentBackground,
    currentSlideNumber,
    setBackground(type) {
      currentBackground.value = type
    },
    setSlideNumber(num) {
      currentSlideNumber.value = num
    }
  }
}

// Auto-detect slide changes
export function setupSlideBackgroundWatcher() {
  const route = useRoute()

  watch(() => route.path, (newPath) => {
    const match = newPath.match(/\/(\d+)/)
    if (match) {
      currentSlideNumber.value = parseInt(match[1])
    }
  }, { immediate: true })
}
