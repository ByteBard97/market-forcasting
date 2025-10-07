<template>
  <SlideLayout background="sphere">
    <h1>Building Realistic Synthetic Data</h1>

    <p class="subtitle">How we generate demand with causal structure</p>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="text-xl font-bold mb-4 text-blue-400">Why Synthetic Data?</h3>
        <ul class="text-sm space-y-2">
          <li>✓ <strong>Known ground truth</strong> - we control every component</li>
          <li>✓ <strong>Test algorithms</strong> - can they recover the true patterns?</li>
          <li>✓ <strong>Causal relationships</strong> - marketing → demand with realistic lags</li>
          <li>✓ <strong>No privacy issues</strong> - perfect for demos & research</li>
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-bold mb-4 text-green-400">The Challenge</h3>
        <ul class="text-sm space-y-2">
          <li>⚠ Must be <strong>realistic</strong> - not just random noise</li>
          <li>⚠ Must have <strong>temporal dynamics</strong> - campaigns need lead time</li>
          <li>⚠ Must be <strong>multiplicative</strong> - components interact</li>
          <li>⚠ Must include <strong>constraints</strong> - stockouts, capacity limits</li>
        </ul>
      </div>
    </div>

    <div class="mt-8 p-4 bg-blue-900 bg-opacity-20 rounded text-sm">
      <strong>Our Approach:</strong> Build demand from 13 multiplicative components with realistic impulse responses
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../SlideLayout.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
