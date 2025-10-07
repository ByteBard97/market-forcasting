<template>
  <SlideLayout background="dots">
    <h1>Inventory Reality</h1>
    <p class="subtitle">Stockouts happen—especially during peaks</p>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="font-bold mb-4">📦 The Challenge</h3>
        <ul class="text-sm space-y-3">
          <li>
            <strong>Growth outpaces capacity:</strong> 12% annual demand growth vs. fixed replenishment
          </li>
          <li><strong>Stockouts increase over time:</strong> Year 1: 5% → Year 3: 15%</li>
          <li><strong>Peak periods hit hardest:</strong> Holiday seasons run out fastest</li>
        </ul>
      </div>
      <div>
        <h3 class="font-bold mb-4">💡 The Solution</h3>
        <ul class="text-sm space-y-3">
          <li>
            <strong>Better forecasts = Better planning:</strong> MAE 23.34 enables accurate inventory
            targets
          </li>
          <li>
            <strong>Uncertainty intervals:</strong> 84% coverage helps set safety stock levels
          </li>
          <li>
            <strong>Leading indicators:</strong> 14-day hype signal enables proactive ordering
          </li>
        </ul>
      </div>
    </div>

    <div class="mt-6 p-4 bg-blue-900 bg-opacity-30 rounded text-sm">
      <strong>Impact:</strong> Reducing forecast error from 30% to 23% (23% improvement) could cut
      stockouts by 30-40% through better demand planning
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
