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
            :line2="insightBold"
            :line3="insightDetail"
          />
        </CellStack>
      </section>

      <!-- RIGHT COLUMN -->
      <section class="right">
        <DemandCurveChart
          :current-price="price"
          :msrp="MSRP"
          :elasticity="ELASTICITY"
          :price-min="140"
          :price-max="210"
        />
      </section>
    </div>
  </SlideLayout>
</template>

<script setup>
import { ref, computed } from "vue";
import SlideLayout from "../components/SlideLayout.vue";
import DemandCurveChart from "../components/DemandCurveChart.vue";

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

const insightBold = computed(() => {
  if (price.value < 160) return "Deep discount:";
  if (price.value < 175) return "Moderate discount:";
  if (price.value <= 185) return "Sweet spot:";
  if (price.value <= 195) return "Premium pricing:";
  return "High price:";
});

const insightDetail = computed(() => {
  if (price.value < 160) return "drives high volume, but may hurt brand perception";
  if (price.value < 175) return "increases volume with minimal brand risk";
  if (price.value <= 185) return "balances demand and margin";
  if (price.value <= 195) return "reduces volume but maintains margins";
  return "may severely limit demand";
});
const insightClass = computed(() =>
  price.value >= 175 && price.value <= 185
    ? "sweet-spot"
    : price.value < 160 || price.value > 200
      ? "warning"
      : "neutral"
);
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
  min-height: 0;
}
</style>
