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

    const VANTA = await import('vanta/dist/vanta.birds.min.js')
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
      backgroundColor: 0x1a1a2e,
      color1: 0xff00ff,
      color2: 0x00ffff,
      colorMode: 'lerp',
      birdSize: 1.40,
      wingSpan: 25.00,
      speedLimit: 5.00,
      separation: 35.00,
      alignment: 15.00,
      cohesion: 15.00,
      quantity: 3.00
    })

    if (vantaEffect && vantaEffect.resize) {
      setTimeout(() => vantaEffect.resize(), 100)
    }

    resizeHandler = () => {
      if (vantaEffect && vantaEffect.resize) vantaEffect.resize()
    }
    window.addEventListener('resize', resizeHandler)
  } catch (error) {
    console.error('VantaBirds: Error', error)
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
