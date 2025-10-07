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
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  gap: 6px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.bg-btn {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 11px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.bg-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.bg-btn.active {
  background: rgba(100, 150, 255, 0.5);
  border-color: rgba(100, 150, 255, 0.8);
}

.bg-desc {
  font-size: 8px;
  opacity: 0.7;
}
</style>
