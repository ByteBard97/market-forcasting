<template>
  <canvas ref="canvas" class="ribbons-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let animationId = null

onMounted(() => {
  const ctx = canvas.value.getContext('2d')

  canvas.value.width = window.innerWidth
  canvas.value.height = window.innerHeight

  let time = 0
  const ribbons = []

  // Create flowing ribbons
  for (let i = 0; i < 5; i++) {
    ribbons.push({
      y: Math.random() * canvas.value.height,
      amplitude: 50 + Math.random() * 100,
      wavelength: 0.001 + Math.random() * 0.002,
      speed: 0.5 + Math.random() * 1.5,
      thickness: 100 + Math.random() * 200,
      opacity: 0.1 + Math.random() * 0.2,
      color: `hsl(${200 + Math.random() * 160}, 70%, 50%)`
    })
  }

  function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
    ctx.fillRect(0, 0, canvas.value.width, canvas.value.height)

    ctx.globalCompositeOperation = 'screen'

    ribbons.forEach((ribbon) => {
      ctx.beginPath()

      for (let x = -100; x <= canvas.value.width + 100; x += 10) {
        const y = ribbon.y +
          Math.sin(x * ribbon.wavelength + time * ribbon.speed) * ribbon.amplitude +
          Math.cos(x * ribbon.wavelength * 0.5 + time * ribbon.speed * 0.7) * ribbon.amplitude * 0.5

        if (x === -100) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      }

      ctx.lineTo(canvas.value.width + 100, canvas.value.height)
      ctx.lineTo(-100, canvas.value.height)
      ctx.closePath()

      const gradient = ctx.createLinearGradient(0, 0, canvas.value.width, canvas.value.height)
      gradient.addColorStop(0, ribbon.color.replace('50%', '60%').replace(')', `, ${ribbon.opacity})`))
      gradient.addColorStop(0.5, ribbon.color.replace('50%', '50%').replace(')', `, ${ribbon.opacity * 1.5})`))
      gradient.addColorStop(1, ribbon.color.replace('50%', '40%').replace(')', `, ${ribbon.opacity})`))

      ctx.fillStyle = gradient
      ctx.shadowBlur = 20
      ctx.shadowColor = ribbon.color
      ctx.fill()
    })

    ctx.globalCompositeOperation = 'source-over'

    time += 0.01
    animationId = requestAnimationFrame(draw)
  }

  draw()

  // Handle window resize
  const handleResize = () => {
    canvas.value.width = window.innerWidth
    canvas.value.height = window.innerHeight
  }

  window.addEventListener('resize', handleResize)

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.ribbons-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: #000;
}
</style>
