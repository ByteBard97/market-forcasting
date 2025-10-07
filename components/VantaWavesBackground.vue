<template>
  <div ref="vantaRef" class="vanta-background"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const vantaRef = ref(null)
let vantaEffect = null
let resizeHandler = null

onMounted(async () => {
  console.log('VantaWaves: Starting mount...')
  try {
    if (!vantaRef.value) {
      console.error('VantaWaves: No ref element')
      return
    }

    // Import THREE - need to get the module's default export
    const THREEModule = await import('three')
    const THREE = THREEModule.default || THREEModule
    console.log('VantaWaves: THREE loaded', THREE)
    console.log('VantaWaves: THREE.REVISION', THREE.REVISION)

    // Import VANTA
    const VANTA = await import('vanta/dist/vanta.waves.min.js')
    console.log('VantaWaves: VANTA loaded', VANTA)

    // Get the effect function
    const effect = VANTA.default || VANTA
    console.log('VantaWaves: Effect function', typeof effect)

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
      color: 0x1a1a2e,
      shininess: 30.00,
      waveHeight: 15.00,
      waveSpeed: 0.75,
      zoom: 0.85
    })

    console.log('VantaWaves: Effect created', vantaEffect)

    // Force resize after creation
    if (vantaEffect && vantaEffect.resize) {
      setTimeout(() => {
        vantaEffect.resize()
      }, 100)
    }

    // Add resize listener
    resizeHandler = () => {
      if (vantaEffect && vantaEffect.resize) {
        vantaEffect.resize()
      }
    }
    window.addEventListener('resize', resizeHandler)
  } catch (error) {
    console.error('VantaWaves: Error during mount:', error)
  }
})

onUnmounted(() => {
  console.log('VantaWaves: Unmounting...')
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
  if (vantaEffect && typeof vantaEffect.destroy === 'function') {
    vantaEffect.destroy()
  }
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
