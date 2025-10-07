<template>
  <div class="background-selector">
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
import { ref } from 'vue'
import { useBackgroundStore } from '../composables/useBackgroundStore'

const { currentBackground, setBackground } = useBackgroundStore()

const backgrounds = [
  { type: 'ribbons', label: 'Ribbons', description: 'Flowing ribbons' },
  { type: 'waves', label: 'Waves', description: '3D waves' },
  { type: 'particles', label: 'Particles', description: 'Particle system' },
  { type: 'octograms', label: 'Octograms', description: 'Tunnel shader' },
  { type: 'shader', label: 'Shader', description: 'WebGL shader' },
  { type: 'none', label: 'None', description: 'No background' }
]

function selectBackground(type) {
  setBackground(type)
}
</script>

<style scoped>
.background-selector {
  position: fixed;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  gap: 4px;
  padding: 6px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.bg-btn {
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 7px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.bg-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.bg-btn.active {
  background: rgba(100, 150, 255, 0.5);
  border-color: rgba(100, 150, 255, 0.8);
}

.bg-desc {
  font-size: 5px;
  opacity: 0.7;
}
</style>
