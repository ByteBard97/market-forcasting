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

    const VANTA = await import('vanta/dist/vanta.clouds.min.js')
    const effect = VANTA.default || VANTA

    vantaEffect = effect({
      el: vantaRef.value,
      THREE: THREE,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      skyColor: 0x68b8d7,
      cloudColor: 0xadc1de,
      cloudShadowColor: 0x183550,
      sunColor: 0xff9919,
      sunGlareColor: 0xff6633,
      sunlightColor: 0xff9933,
      speed: 1.00
    })

    if (vantaEffect && vantaEffect.resize) {
      setTimeout(() => vantaEffect.resize(), 100)
    }

    resizeHandler = () => {
      if (vantaEffect && vantaEffect.resize) vantaEffect.resize()
    }
    window.addEventListener('resize', resizeHandler)
  } catch (error) {
    console.error('VantaClouds: Error', error)
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
