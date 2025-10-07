<template>
  <div ref="vantaRef" class="vanta-background"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const vantaRef = ref(null)
let vantaEffect = null
let resizeHandler = null

onMounted(async () => {
  try {
    if (!vantaRef.value) return

    const THREEModule = await import('three')
    const THREE = THREEModule.default || THREEModule

    const VANTA = await import('vanta/dist/vanta.net.min.js')
    const effect = VANTA.default || VANTA

    vantaEffect = effect({
      el: vantaRef.value,
      THREE: THREE,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x3f8cff,
      backgroundColor: 0x0a0a0a,
      points: 10.00,
      maxDistance: 20.00,
      spacing: 15.00,
      showDots: true
    })

    if (vantaEffect && vantaEffect.resize) {
      setTimeout(() => vantaEffect.resize(), 100)
    }

    resizeHandler = () => {
      if (vantaEffect && vantaEffect.resize) vantaEffect.resize()
    }
    window.addEventListener('resize', resizeHandler)
  } catch (error) {
    console.error('VantaNet: Error', error)
  }
})

onUnmounted(() => {
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  if (vantaEffect && vantaEffect.destroy) vantaEffect.destroy()
})
</script>

<style>
.vanta-background {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: -1 !important;
}

.vanta-background canvas {
  width: 100% !important;
  height: 100% !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
}
</style>
