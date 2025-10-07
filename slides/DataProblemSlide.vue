<template>
  <SlideLayout>
    <h1>The Data Challenge</h1>
    <p class="subtitle">Real data is messy - synthetic data is perfect for learning</p>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="text-xl font-bold mb-4 text-red-400">Real Data Problems</h3>
        <ul class="text-sm space-y-2">
          <li>🔒 <strong>Proprietary</strong> - Nike won't share theirs!</li>
          <li>🌪️ <strong>Messy</strong> - Returns, cancellations, system glitches</li>
          <li>❓ <strong>Incomplete</strong> - Missing competitor data, social signals</li>
          <li>🎰 <strong>Unknown truth</strong> - Don't know what truly drives demand</li>
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-bold mb-4 text-green-400">Synthetic Data Benefits</h3>
        <ul class="text-sm space-y-2">
          <li>✅ <strong>Ground truth</strong> - We know exactly what drives demand</li>
          <li>✅ <strong>Test fairly</strong> - Can forecasting models recover the patterns?</li>
          <li>✅ <strong>Causal structure</strong> - Marketing → demand with realistic lags</li>
          <li>✅ <strong>No legal issues</strong> - Perfect for demos & teaching</li>
        </ul>
      </div>
    </div>

    <div class="mt-8 p-4 bg-blue-900 bg-opacity-20 rounded">
      <strong>Our Approach:</strong> Build realistic Air Jordan demand from 13 additive components<br />
      <span class="text-sm opacity-80">Each component represents a real business driver</span>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
