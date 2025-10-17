<template>
  <SlideLayout>
    <h1>Building Seasonality from Simple Waves</h1>
    <p class="subtitle">Complex patterns emerge from adding simple sine waves</p>

    <div class="wave-container">
      <!-- Individual waves -->
      <div class="wave-row" v-for="(wave, i) in waves" :key="i">
        <div class="wave-label">
          <span class="wave-name" :style="{ color: wave.color }">{{ wave.name }}</span>
          <span class="wave-desc">{{ wave.description }}</span>
          <span class="wave-freq">f = {{ wave.frequency }}×</span>
        </div>
        <canvas :ref="el => waveCanvases[i] = el" class="wave-canvas" :style="{ borderColor: wave.color }"></canvas>
      </div>

      <!-- Result wave -->
      <div class="wave-row result-row">
        <div class="wave-label">
          <span class="wave-name result-name">Combined Pattern</span>
          <span class="wave-desc">Sum of all waves above</span>
        </div>
        <canvas ref="resultCanvas" class="wave-canvas result-canvas"></canvas>
      </div>
    </div>

    <div class="explanation">
      Each point on the final wave = sum of points from waves above
    </div>
  </SlideLayout>
</template>

<script setup>
import { ref, onMounted, onUnmounted, onActivated, nextTick } from 'vue'
import SlideLayout from '../components/SlideLayout.vue'

const waveCanvases = ref([])
const resultCanvas = ref(null)
let animationId = null

// Define waves (frequency, amplitude, phase, color)
const waves = [
  {
    name: 'Annual Cycle',
    description: '1 peak per year',
    frequency: 1,
    amplitude: 30,
    phase: 0,
    color: '#60a5fa'
  },
  {
    name: 'Semi-Annual',
    description: '2 peaks per year',
    frequency: 2,
    amplitude: 15,
    phase: 0.5,
    color: '#f59e0b'
  },
  {
    name: 'Quarterly',
    description: '4 peaks per year',
    frequency: 4,
    amplitude: 8,
    phase: 0,
    color: '#10b981'
  }
]

let time = 0

const drawWave = (canvas, wave, showPoints = false) => {
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const width = canvas.width
  const height = canvas.height
  const centerY = height / 2

  ctx.clearRect(0, 0, width, height)

  // Draw center line
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(0, centerY)
  ctx.lineTo(width, centerY)
  ctx.stroke()

  // Draw wave
  ctx.strokeStyle = wave.color
  ctx.lineWidth = 3
  ctx.beginPath()

  const points = []
  for (let x = 0; x < width; x += 2) {
    const t = (x / width) * Math.PI * 4 + time // 2 full cycles shown
    const y = Math.sin(wave.frequency * t + wave.phase) * wave.amplitude
    const canvasY = centerY - y

    if (x === 0) {
      ctx.moveTo(x, canvasY)
    } else {
      ctx.lineTo(x, canvasY)
    }

    if (showPoints && x % 60 === 0) {
      points.push({ x, y: canvasY })
    }
  }
  ctx.stroke()

  // Draw frequency markers (vertical lines at peaks)
  ctx.strokeStyle = wave.color
  ctx.lineWidth = 1
  ctx.globalAlpha = 0.2
  for (let x = 0; x < width; x += 2) {
    const t = (x / width) * Math.PI * 4 + time
    const y = Math.sin(wave.frequency * t + wave.phase) * wave.amplitude
    const prevT = ((x - 2) / width) * Math.PI * 4 + time
    const prevY = Math.sin(wave.frequency * prevT + wave.phase) * wave.amplitude

    // Detect peak (sign change in derivative)
    if (x > 0 && prevY > y && prevY > 0) {
      ctx.beginPath()
      ctx.moveTo(x - 2, 0)
      ctx.lineTo(x - 2, height)
      ctx.stroke()
    }
  }
  ctx.globalAlpha = 1.0

  // Draw point markers for visual addition
  if (showPoints) {
    ctx.fillStyle = wave.color
    points.forEach(p => {
      ctx.beginPath()
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2)
      ctx.fill()
    })
  }
}

const drawResultWave = (canvas) => {
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const width = canvas.width
  const height = canvas.height
  const centerY = height / 2

  ctx.clearRect(0, 0, width, height)

  // Draw center line
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(0, centerY)
  ctx.lineTo(width, centerY)
  ctx.stroke()

  // Draw summed wave
  ctx.strokeStyle = '#a855f7'
  ctx.lineWidth = 3
  ctx.beginPath()

  for (let x = 0; x < width; x += 2) {
    const t = (x / width) * Math.PI * 4 + time

    // Sum all waves
    let sumY = 0
    waves.forEach(wave => {
      sumY += Math.sin(wave.frequency * t + wave.phase) * wave.amplitude
    })

    const canvasY = centerY - sumY

    if (x === 0) {
      ctx.moveTo(x, canvasY)
    } else {
      ctx.lineTo(x, canvasY)
    }
  }
  ctx.stroke()

  // Fill area under curve
  ctx.fillStyle = 'rgba(168, 85, 247, 0.1)'
  ctx.lineTo(width, centerY)
  ctx.lineTo(0, centerY)
  ctx.closePath()
  ctx.fill()
}

const animate = () => {
  time += 0.01

  // Draw individual waves
  waveCanvases.value.forEach((canvas, i) => {
    if (canvas) {
      drawWave(canvas, waves[i], true)
    }
  })

  // Draw result
  if (resultCanvas.value) {
    drawResultWave(resultCanvas.value)
  }

  animationId = requestAnimationFrame(animate)
}

const setupCanvases = () => {
  console.log('=== setupCanvases called ===')
  console.log('Wave canvases count:', waveCanvases.value.length)
  console.log('Result canvas exists:', !!resultCanvas.value)

  // Setup individual wave canvases
  waveCanvases.value.forEach((canvas, index) => {
    if (canvas) {
      const rect = canvas.getBoundingClientRect()
      console.log(`Wave canvas ${index} rect:`, rect.width, 'x', rect.height)
      canvas.width = rect.width * 2 // High DPI
      canvas.height = rect.height * 2
      canvas.style.width = rect.width + 'px'
      canvas.style.height = rect.height + 'px'
      console.log(`Wave canvas ${index} configured:`, canvas.width, 'x', canvas.height)
    } else {
      console.warn(`Wave canvas ${index} is null!`)
    }
  })

  // Setup result canvas
  if (resultCanvas.value) {
    const rect = resultCanvas.value.getBoundingClientRect()
    console.log('Result canvas rect:', rect.width, 'x', rect.height)
    resultCanvas.value.width = rect.width * 2
    resultCanvas.value.height = rect.height * 2
    resultCanvas.value.style.width = rect.width + 'px'
    resultCanvas.value.style.height = rect.height + 'px'
    console.log('Result canvas configured:', resultCanvas.value.width, 'x', resultCanvas.value.height)
  } else {
    console.warn('Result canvas is null!')
  }
  console.log('=== setupCanvases complete ===')
}

const waitForLayout = async (maxAttempts = 10) => {
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise(resolve => setTimeout(resolve, 100))

    // Check if any canvas has valid dimensions
    const firstCanvas = waveCanvases.value[0]
    if (firstCanvas) {
      const rect = firstCanvas.getBoundingClientRect()
      console.log(`Layout check attempt ${i + 1}: canvas dimensions ${rect.width}x${rect.height}`)
      if (rect.width > 0 && rect.height > 0) {
        console.log('Layout ready!')
        return true
      }
    }
  }
  console.warn('Layout timeout - canvases still have 0 dimensions')
  return false
}

const initializeAnimation = async () => {
  console.log('>>> initializeAnimation START')
  console.log('Before nextTick - waveCanvases:', waveCanvases.value.length, 'resultCanvas:', !!resultCanvas.value)

  await nextTick()
  console.log('After nextTick - waveCanvases:', waveCanvases.value.length, 'resultCanvas:', !!resultCanvas.value)

  // Wait for layout to complete
  const layoutReady = await waitForLayout()
  if (!layoutReady) {
    console.error('Failed to initialize - canvases not laid out')
    return
  }

  console.log('WaveAdditionSlide: Initializing animation', {
    waveCanvasCount: waveCanvases.value.length,
    resultCanvas: resultCanvas.value
  })

  setupCanvases()

  // Cancel any existing animation
  if (animationId) {
    console.log('Canceling existing animation:', animationId)
    cancelAnimationFrame(animationId)
  }

  console.log('Starting animation...')
  animate()
  console.log('>>> initializeAnimation END - animationId:', animationId)
}

onMounted(() => {
  console.log('WaveAdditionSlide mounted')
  initializeAnimation()
})

onActivated(() => {
  console.log('WaveAdditionSlide activated')
  initializeAnimation()
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.subtitle {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 0.2rem;
}

.wave-container {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 0;
  margin-bottom: 0;
  container-type: size;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  padding-right: 10px;
}

.wave-row {
  display: grid;
  grid-template-columns: 170px 1fr;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0;
}

.wave-label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.wave-name {
  font-weight: 600;
  font-size: 0.85rem;
}

.wave-desc {
  font-size: 0.7rem;
  opacity: 0.6;
}

.wave-freq {
  font-size: 0.65rem;
  font-weight: 700;
  font-family: 'Fira Code', monospace;
  opacity: 0.8;
  margin-top: 0.1rem;
}

.wave-canvas {
  width: 100%;
  max-width: 100%;
  height: 13cqh;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.addition-row {
  display: flex;
  justify-content: center;
  padding: 0;
  margin: 0;
}

.addition-symbol {
  font-size: 1.2rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.4);
}

.result-row {
  margin-top: 0.5rem;
  margin-bottom: 0;
  padding-top: 0.5rem;
  border-top: 2px dashed rgba(255, 255, 255, 0.2);
}

.result-name {
  color: #a855f7;
  font-weight: 700;
}

.result-canvas {
  height: 16cqh;
  background: rgba(168, 85, 247, 0.08);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(168, 85, 247, 0.3);
  box-shadow: 0 4px 8px rgba(168, 85, 247, 0.2);
}

.explanation {
  margin-top: 0;
  text-align: center;
  font-size: 0.75rem;
  opacity: 0.7;
  font-style: italic;
}
</style>
