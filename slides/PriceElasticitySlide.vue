<template>
  <SlideLayout>
    <h1>How Price Affects Demand</h1>
    <p class="subtitle">Interactive demo: adjust the price and see demand change</p>

    <div class="demo-container">
      <!-- Left: Interactive Controls -->
      <div class="controls-panel">
        <div class="price-control">
          <label class="control-label">Set Your Price</label>
          <div class="price-display">${{ price }}</div>
          <input
            type="range"
            v-model.number="price"
            min="140"
            max="210"
            step="5"
            class="price-slider"
          />
          <div class="price-range">
            <span>$140</span>
            <span>MSRP: $180</span>
            <span>$210</span>
          </div>
        </div>

        <div class="metrics">
          <div class="metric-card">
            <div class="metric-label">Demand Multiplier</div>
            <div class="metric-value">{{ multiplier.toFixed(2) }}×</div>
            <div class="metric-change" :class="changeClass">
              {{ changeText }}
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Daily Pairs</div>
            <div class="metric-value">{{ dailyPairs }}</div>
            <div class="metric-subtext">at baseline 60/day</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Revenue Impact</div>
            <div class="metric-value">{{ revenueChange > 0 ? '+' : '' }}{{ revenueChange }}%</div>
            <div class="metric-subtext">vs. MSRP</div>
          </div>
        </div>

        <div class="insight-box" :class="insightClass">
          <strong>💡 Insight:</strong> {{ insight }}
        </div>
      </div>

      <!-- Right: Visual Chart -->
      <div class="chart-panel">
        <svg ref="chartSvg" class="elasticity-chart" viewBox="0 0 400 300">
          <!-- Grid lines -->
          <g class="grid">
            <line v-for="i in 5" :key="'h-' + i"
              :x1="60" :y1="40 + i * 50"
              :x2="380" :y2="40 + i * 50"
              stroke="rgba(255,255,255,0.1)" stroke-dasharray="2,2" />
            <line v-for="i in 6" :key="'v-' + i"
              :x1="60 + i * 53" :y1="40"
              :x2="60 + i * 53" :y2="290"
              stroke="rgba(255,255,255,0.1)" stroke-dasharray="2,2" />
          </g>

          <!-- Axes -->
          <line x1="60" y1="290" x2="380" y2="290" stroke="#9ca3af" stroke-width="2" />
          <line x1="60" y1="40" x2="60" y2="290" stroke="#9ca3af" stroke-width="2" />

          <!-- Labels -->
          <text x="220" y="315" fill="#9ca3af" text-anchor="middle" font-size="12">Price ($)</text>
          <text x="30" y="165" fill="#9ca3af" text-anchor="middle" font-size="12" transform="rotate(-90 30 165)">Demand</text>

          <!-- Price axis labels -->
          <text x="60" y="305" fill="#9ca3af" text-anchor="middle" font-size="10">$140</text>
          <text x="220" y="305" fill="#9ca3af" text-anchor="middle" font-size="10">$180</text>
          <text x="380" y="305" fill="#9ca3af" text-anchor="middle" font-size="10">$210</text>

          <!-- Elasticity curve -->
          <path :d="curvePath" fill="none" stroke="#3b82f6" stroke-width="3" />
          <path :d="curvePath" fill="url(#gradient)" opacity="0.2" />

          <!-- Current point -->
          <circle
            :cx="currentX"
            :cy="currentY"
            r="8"
            fill="#10b981"
            stroke="#fff"
            stroke-width="2"
            class="current-point"
          />
          <text
            :x="currentX"
            :y="currentY - 15"
            fill="#10b981"
            text-anchor="middle"
            font-size="12"
            font-weight="bold"
          >You</text>

          <!-- Gradient definition -->
          <defs>
            <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3" />
              <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import SlideLayout from '../components/SlideLayout.vue'

const price = ref(180)
const MSRP = 180
const ELASTICITY = -1.2 // Price elasticity coefficient

// Calculate demand multiplier
const multiplier = computed(() => Math.pow(price.value / MSRP, ELASTICITY))

// Calculate daily pairs sold
const dailyPairs = computed(() => Math.round(60 * multiplier.value))

// Calculate revenue change vs MSRP
const revenueChange = computed(() => {
  const msrpRevenue = MSRP * 60
  const currentRevenue = price.value * dailyPairs.value
  return Math.round(((currentRevenue - msrpRevenue) / msrpRevenue) * 100)
})

// Change text and class
const changeText = computed(() => {
  const priceDiff = price.value - MSRP
  if (priceDiff === 0) return 'at MSRP'
  const pct = Math.round((Math.abs(priceDiff) / MSRP) * 100)
  return priceDiff > 0 ? `${pct}% above MSRP` : `${pct}% below MSRP`
})

const changeClass = computed(() => {
  if (price.value > MSRP) return 'negative'
  if (price.value < MSRP) return 'positive'
  return 'neutral'
})

// Insight based on current price
const insight = computed(() => {
  if (price.value < 160) {
    return 'Deep discount drives high volume, but may hurt brand perception'
  } else if (price.value < 175) {
    return 'Moderate discount increases volume with minimal brand risk'
  } else if (price.value >= 175 && price.value <= 185) {
    return 'Sweet spot: balances demand and margin'
  } else if (price.value <= 195) {
    return 'Premium pricing reduces volume but maintains margins'
  } else {
    return 'High price may severely limit demand'
  }
})

const insightClass = computed(() => {
  if (price.value >= 175 && price.value <= 185) return 'sweet-spot'
  if (price.value < 160 || price.value > 200) return 'warning'
  return 'neutral'
})

// SVG curve path for elasticity
const curvePath = computed(() => {
  const points = []
  for (let p = 140; p <= 210; p += 2) {
    const x = 60 + ((p - 140) / 70) * 320
    const mult = Math.pow(p / MSRP, ELASTICITY)
    const demand = mult * 100 // Scale for display
    const y = 290 - (demand * 2.5) // Invert Y and scale
    points.push(`${x},${y}`)
  }
  return `M${points.join(' L')} L380,290 L60,290 Z`
})

// Current point position
const currentX = computed(() => 60 + ((price.value - 140) / 70) * 320)
const currentY = computed(() => 290 - (multiplier.value * 100 * 2.5))
</script>

<style scoped>
.subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 1.5rem;
}

.demo-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  height: 70vh;
}

.controls-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.price-control {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
}

.control-label {
  display: block;
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 0.5rem;
}

.price-display {
  font-size: 3rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 1rem;
  text-align: center;
}

.price-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: linear-gradient(to right, #10b981, #3b82f6, #ef4444);
  outline: none;
  -webkit-appearance: none;
  margin-bottom: 0.5rem;
}

.price-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.price-slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: none;
}

.price-range {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  opacity: 0.6;
}

.metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.metric-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem;
}

.metric-label {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
}

.metric-change {
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.metric-change.neutral {
  color: #9ca3af;
}

.metric-subtext {
  font-size: 0.75rem;
  opacity: 0.6;
  margin-top: 0.25rem;
}

.insight-box {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  padding: 1rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.insight-box.sweet-spot {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
}

.insight-box.warning {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.chart-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.elasticity-chart {
  width: 100%;
  height: 100%;
}

.current-point {
  filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.5));
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { r: 8; }
  50% { r: 10; }
}
</style>
