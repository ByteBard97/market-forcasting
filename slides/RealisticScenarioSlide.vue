<template>
  <SlideLayout background="dots">
    <h1>The Realistic Scenario</h1>
    <p class="subtitle">In production: You have yesterday's actuals when forecasting tomorrow</p>

    <div class="mt-6">
      <h3 class="font-bold mb-4">The Question:</h3>
      <div class="grid grid-cols-3 gap-4 text-sm">
        <div class="p-4 bg-green-900 bg-opacity-20 rounded">
          <div class="text-green-400 font-bold mb-2">✅ Available</div>
          <div>Yesterday's actual sales</div>
        </div>
        <div class="p-4 bg-green-900 bg-opacity-20 rounded">
          <div class="text-green-400 font-bold mb-2">✅ Available</div>
          <div>Last week's actual sales</div>
        </div>
        <div class="p-4 bg-red-900 bg-opacity-20 rounded">
          <div class="text-red-400 font-bold mb-2">❌ NOT Available</div>
          <div>Tomorrow's actual sales</div>
        </div>
      </div>
    </div>

    <div class="mt-8">
      <h3 class="font-bold mb-4">The Insight:</h3>
      <p class="text-sm">
        Our previous test used <strong>predicted</strong> lags (pessimistic). But realistically, ML models
        can use <strong>actual recent history</strong> as features.
      </p>
    </div>

    <div class="mt-6 text-xs text-gray-400 text-center">
      Example: When forecasting Monday, you have Friday/Saturday/Sunday actuals for lag features
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
