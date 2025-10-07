<template>
  <SlideLayout>
    <h1>The Business Challenge</h1>
    <p class="subtitle">Why accurate demand forecasting matters for sneakers</p>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="text-xl font-bold mb-4 text-red-400">The Problem</h3>
        <ul class="text-sm space-y-2">
          <li>💰 <strong>Stockouts</strong> - Lost sales during hype drops</li>
          <li>📉 <strong>Brand damage</strong> - Frustrated customers leave</li>
          <li>🏪 <strong>Empty shelves</strong> - Competitors win the sale</li>
          <li>⏰ <strong>Missed timing</strong> - Can't restock fast enough</li>
        </ul>
        <div class="mt-4 p-3 bg-red-900 bg-opacity-20 rounded text-xs">
          <strong>Cost of stockout:</strong> $180 lost per pair + customer trust
        </div>
      </div>
      <div>
        <h3 class="text-xl font-bold mb-4 text-yellow-400">The Other Problem</h3>
        <ul class="text-sm space-y-2">
          <li>📦 <strong>Overstock</strong> - Capital tied up in inventory</li>
          <li>💸 <strong>Markdowns</strong> - Have to discount to clear</li>
          <li>🏢 <strong>Storage costs</strong> - Warehouse space isn't free</li>
          <li>📊 <strong>Margin erosion</strong> - 30% off kills profitability</li>
        </ul>
        <div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-xs">
          <strong>Cost of overstock:</strong> 20-40% margin loss on clearance
        </div>
      </div>
    </div>

    <div class="mt-8 p-4 bg-blue-900 bg-opacity-20 rounded text-center">
      <strong class="text-lg">The Solution: Predict demand accurately</strong><br />
      <span class="text-sm opacity-80">Know what to stock, when, and how much</span>
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
