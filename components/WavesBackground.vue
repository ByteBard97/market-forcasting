<template>
  <div ref="vantaRef" class="waves-background"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const vantaRef = ref(null)
let vantaEffect = null

onMounted(async () => {
  // Load Three.js (required by Vanta)
  if (!window.THREE) {
    await loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js')
  }

  // Load Vanta.js Waves effect
  if (!window.VANTA) {
    await loadScript('https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js')
  }

  // Initialize Vanta effect
  try {
    vantaEffect = window.VANTA.WAVES({
      el: vantaRef.value,
      THREE: window.THREE,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x1e3c72,
      shininess: 60.00,
      waveHeight: 30.00,
      waveSpeed: 1.00,
      zoom: 0.65
    })
  } catch (error) {
    console.error('Vanta.js initialization failed:', error)
  }
})

onUnmounted(() => {
  if (vantaEffect) {
    vantaEffect.destroy()
  }
})

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = src
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}
</script>

<style scoped>
.waves-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
