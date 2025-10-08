<!-- PriceElasticitySlide.vue -->
<template>
  <SlideLayout>
    <header class="slide-header">
      <h1>How Price Affects Demand</h1>
      <p class="subtitle">
        Interactive demo: adjust the price and see demand change
      </p>
    </header>

    <div class="demo">
      <!-- LEFT COLUMN -->
      <section class="left">
        <div class="card price-control">
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
            <span>$140</span><span>MSRP: $180</span><span>$210</span>
          </div>
        </div>

        <CellStack class="card grow">
          <MetricCell
            align="left"
            line1="Demand Multiplier"
            :line2="`${multiplier.toFixed(2)}×`"
            :line3="changeText"
          />
          <MetricCell
            align="left"
            line1="Daily Pairs"
            :line2="`${dailyPairs}`"
            line3="at baseline 60/day"
          />
          <MetricCell
            align="left"
            line1="Revenue Impact"
            :line2="`${revenueChange > 0 ? '+' : ''}${revenueChange}%`"
            line3="vs. MSRP"
          />
          <MetricCell
            align="left"
            line1="💡 Insight"
            :line2="insight"
            line3=""
          />
        </CellStack>
      </section>

      <!-- RIGHT COLUMN -->
      <section class="right">
        <!-- Pure responsive SVG: fills the cell, no JS scaling needed -->
        <svg
          class="chart"
          viewBox="0 0 400 300"
          preserveAspectRatio="xMidYMid meet"
        >
          <!-- grid -->
          <g class="grid">
            <line
              v-for="i in 5"
              :key="'h-' + i"
              :x1="60"
              :y1="40 + i * 50"
              :x2="380"
              :y2="40 + i * 50"
              stroke="rgba(255,255,255,0.1)"
              stroke-dasharray="2,2"
            />
            <line
              v-for="i in 6"
              :key="'v-' + i"
              :x1="60 + i * 53"
              :y1="40"
              :x2="60 + i * 53"
              :y2="290"
              stroke="rgba(255,255,255,0.2)"
              stroke-dasharray="4,4"
            />
          </g>

          <!-- axes -->
          <line
            x1="60"
            y1="290"
            x2="380"
            y2="290"
            stroke="#e5e7eb"
            stroke-width="2"
          />
          <line
            x1="60"
            y1="40"
            x2="60"
            y2="290"
            stroke="#e5e7eb"
            stroke-width="2"
          />

          <!-- Axis labels only - no ticks -->
          <text x="220" y="295" fill="#9ca3af" text-anchor="middle" font-size="9">
            Price →
          </text>
          <text x="40" y="165" fill="#9ca3af" text-anchor="middle" font-size="9" transform="rotate(-90 40 165)">
            ← Demand
          </text>

          <!-- curve + fill -->
          <path :d="curvePath" fill="none" stroke="#60a5fa" stroke-width="2.5" />
          <path :d="curvePath" fill="url(#gradient)" opacity="0.15" />

          <!-- current point -->
          <circle
            :cx="currentX"
            :cy="currentY"
            r="6"
            fill="#10b981"
            stroke="#fff"
            stroke-width="2"
            class="current-point"
          />
          <text
            :x="currentX"
            :y="currentY - 12"
            fill="#10b981"
            text-anchor="middle"
            font-size="10"
            font-weight="bold"
          >
            You
          </text>

          <defs>
            <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3" />
              <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </section>
    </div>
  </SlideLayout>
</template>

<script setup>
import { ref, computed } from "vue";
import SlideLayout from "../components/SlideLayout.vue";

const price = ref(180);
const MSRP = 180;
const ELASTICITY = -1.2;

const multiplier = computed(() => Math.pow(price.value / MSRP, ELASTICITY));
const dailyPairs = computed(() => Math.round(60 * multiplier.value));
const revenueChange = computed(() => {
  const msrpRevenue = MSRP * 60;
  const currentRevenue = price.value * dailyPairs.value;
  return Math.round(((currentRevenue - msrpRevenue) / msrpRevenue) * 100);
});

const changeText = computed(() => {
  const d = price.value - MSRP;
  if (d === 0) return "at MSRP";
  const pct = Math.round((Math.abs(d) / MSRP) * 100);
  return d > 0 ? `${pct}% above MSRP` : `${pct}% below MSRP`;
});
const changeClass = computed(() =>
  price.value > MSRP ? "negative" : price.value < MSRP ? "positive" : "neutral"
);

const insight = computed(() => {
  if (price.value < 160)
    return "Deep discount drives high volume, but may hurt brand perception";
  if (price.value < 175)
    return "Moderate discount increases volume with minimal brand risk";
  if (price.value <= 185) return "Sweet spot: balances demand and margin";
  if (price.value <= 195)
    return "Premium pricing reduces volume but maintains margins";
  return "High price may severely limit demand";
});
const insightClass = computed(() =>
  price.value >= 175 && price.value <= 185
    ? "sweet-spot"
    : price.value < 160 || price.value > 200
      ? "warning"
      : "neutral"
);

const curvePath = computed(() => {
  const pts = [];
  for (let p = 140; p <= 210; p += 2) {
    const x = 60 + ((p - 140) / 70) * 320;
    const mult = Math.pow(p / MSRP, ELASTICITY);
    const demand = mult * 100;
    const y = 250 - demand * 1.5;
    pts.push(`${x},${y}`);
  }
  return `M${pts.join(" L")} L380,290 L60,290 Z`;
});
const currentX = computed(() => 60 + ((price.value - 140) / 70) * 320);
const currentY = computed(() => 250 - multiplier.value * 100 * 1.5);
</script>

<style scoped>
/* --- overall header + grid --- */
.slide-header {
  flex-shrink: 0;
  margin-bottom: 0.75rem;
}
.slide-header h1 {
  margin: 0 0 0.5rem 0;
}
.subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}

/* 2-column grid that fills the slide */
.demo {
  display: grid;
  grid-template-columns: 1fr 1fr; /* even split */
  gap: 1.5rem;
  height: 100%;
  min-height: 0; /* allow grid children to shrink */
}

/* columns */
.left,
.right {
  min-height: 0;
}

/* left column stacks two blocks:
   1) fixed-height price control (auto)
   2) growable/scrollable metrics+insight (1fr) */
.left {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 0.75rem;
  min-height: 0;
}

.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.5rem;
  min-height: 0;
}

/* grow to fill space */
.grow {
  min-height: 0;
}

/* controls */
.control-label {
  display: block;
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 0.5rem;
}
.price-display {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 0.4rem;
  text-align: center;
}
.price-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: linear-gradient(90deg, #10b981, #3b82f6, #ef4444);
  margin-bottom: 0.5rem;
}
.price-range {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  opacity: 0.6;
}

/* metrics */
.metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.4rem;
  min-height: 0;
}
.metric-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.4rem;
}
.metric-label {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-bottom: 0.25rem;
}
.metric-value {
  font-size: 1rem;
  font-weight: 700;
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

/* insight */
.insight-box {
  margin-top: 0.4rem;
  font-size: 0.75rem;
  line-height: 1.3;
  border-radius: 6px;
  padding: 0.4rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
}
.insight-box.sweet-spot {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
}
.insight-box.warning {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

/* right column chart fills its cell */
.right {
  display: flex;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
}
.chart {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.3));
}
.current-point {
  filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.5));
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%,
  100% {
    r: 8;
  }
  50% {
    r: 10;
  }
}
</style>
