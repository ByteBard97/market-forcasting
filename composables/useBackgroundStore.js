import { ref } from 'vue'

// Global reactive state for background selection
const currentBackground = ref('ribbons')

export function useBackgroundStore() {
  function setBackground(type) {
    currentBackground.value = type
  }

  return {
    currentBackground,
    setBackground
  }
}
