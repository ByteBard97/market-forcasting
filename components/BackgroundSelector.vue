<template>
  <div
    class="background-selector"
    :class="{ visible: isVisible }"
    @mouseenter="handleMenuEnter"
    @mouseleave="handleMenuLeave"
  >
    <button
      v-for="bg in backgrounds"
      :key="bg.type"
      :class="{ active: currentBackground === bg.type }"
      @click="selectBackground(bg.type)"
      class="bg-btn"
    >
      {{ bg.label }}
      <span class="bg-desc">{{ bg.description }}</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useBackgroundStore } from '../composables/useBackgroundStore'

const { currentBackground, setBackground } = useBackgroundStore()
const isVisible = ref(false)
let hideTimeout = null
let showTimeout = null
let wasInSouthArea = false

function handleMouseMove(e) {
  const threshold = window.innerHeight - 100
  const inSouthArea = e.clientY > threshold

  if (inSouthArea && !wasInSouthArea) {
    // Just entered south area
    wasInSouthArea = true
    if (hideTimeout) clearTimeout(hideTimeout)

    // Show after 500ms
    showTimeout = setTimeout(() => {
      isVisible.value = true
    }, 500)
  } else if (!inSouthArea && wasInSouthArea) {
    // Just left south area
    wasInSouthArea = false
    if (showTimeout) clearTimeout(showTimeout)

    // Hide after 1 second
    hideTimeout = setTimeout(() => {
      isVisible.value = false
    }, 1000)
  }
}

function handleMenuEnter() {
  wasInSouthArea = true
  if (hideTimeout) clearTimeout(hideTimeout)
  if (showTimeout) clearTimeout(showTimeout)
  isVisible.value = true
}

function handleMenuLeave() {
  wasInSouthArea = false
  hideTimeout = setTimeout(() => {
    isVisible.value = false
  }, 1000)
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  if (hideTimeout) clearTimeout(hideTimeout)
  if (showTimeout) clearTimeout(showTimeout)
})

const backgrounds = [
  { type: 'datasphere', label: 'Data Sphere', description: 'Connected dots' },
  { type: 'morphing', label: 'Morphing', description: 'Morphing dots' },
  { type: 'perlin', label: 'Perlin Noise', description: 'Morphing shape' },
  { type: 'surfacelines', label: 'Surface Lines', description: 'Flowing lines' },
  { type: 'distortedcube', label: 'Distorted Cube', description: 'Wireframe cube' },
  { type: 'tentacle', label: 'Tentacle', description: 'Organic lines' },
  { type: 'none', label: 'None', description: 'No background' }
]

function selectBackground(type) {
  setBackground(type)
}
</script>

<style scoped>
.background-selector {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) translateY(100%);
  z-index: 1000;
  display: flex;
  gap: 4px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  border-radius: 8px 8px 0 0;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-bottom: none;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.background-selector.visible {
  transform: translateX(-50%) translateY(0);
}

.bg-btn {
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.bg-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.bg-btn.active {
  background: rgba(100, 150, 255, 0.4);
  border-color: rgba(100, 150, 255, 0.6);
}

.bg-desc {
  font-size: 7px;
  opacity: 0.6;
}
</style>
