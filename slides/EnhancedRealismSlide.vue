<template>
  <SlideLayout background="dots">
    <h1>Enhanced Realism: New Components</h1>
    <p class="subtitle">We added 3 real-world factors executives face daily</p>

    <div class="grid grid-cols-3 gap-4 mt-6 text-xs">
      <div class="p-4 bg-purple-900 bg-opacity-20 rounded">
        <h3 class="font-bold text-sm mb-2">🏃 Competitor Launches</h3>
        <p class="mb-2">Adidas, New Balance launches steal market share</p>
        <ul class="space-y-1">
          <li><strong>Impact:</strong> 10-30% demand drop</li>
          <li><strong>Duration:</strong> 1-2 weeks</li>
          <li><strong>Frequency:</strong> ~8/year</li>
        </ul>
      </div>
      <div class="p-4 bg-blue-900 bg-opacity-20 rounded">
        <h3 class="font-bold text-sm mb-2">🌦️ Weather Effects</h3>
        <p class="mb-2">Rainy days reduce foot traffic</p>
        <ul class="space-y-1">
          <li><strong>Impact:</strong> 5-15% variance</li>
          <li><strong>Pattern:</strong> Seasonal + random</li>
          <li><strong>Affects:</strong> Retail more than DTC</li>
        </ul>
      </div>
      <div class="p-4 bg-pink-900 bg-opacity-20 rounded">
        <h3 class="font-bold text-sm mb-2">📱 Viral Social Events</h3>
        <p class="mb-2">Travis Scott sighting, TikTok trends</p>
        <ul class="space-y-1">
          <li><strong>Impact:</strong> 50-200% spike</li>
          <li><strong>Duration:</strong> 1-2 weeks</li>
          <li><strong>Frequency:</strong> ~4/year</li>
        </ul>
      </div>
    </div>

    <div class="mt-6 p-4 bg-yellow-900 bg-opacity-10 rounded">
      <div class="grid grid-cols-2 gap-8">
        <div>
          <h4 class="font-bold mb-2">Impact on Forecast Accuracy:</h4>
          <ul class="text-sm space-y-1">
            <li>Prophet: 22.90 → 23.34 MAE (<strong>+1.9%</strong> only!) ✅</li>
            <li>XGBoost: 26.58 → 29.83 MAE (+12.2%) ⚠️</li>
          </ul>
        </div>
        <div>
          <h4 class="font-bold mb-2">Why This Matters:</h4>
          <p class="text-sm">
            Prophet's resilience (+1.9% despite 20% more variance) demonstrates
            <strong>production readiness</strong>
          </p>
        </div>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
