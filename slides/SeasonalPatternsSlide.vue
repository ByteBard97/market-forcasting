<template>
  <SlideLayout background="dots">
    <h1>Seasonal Patterns</h1>
    <p class="subtitle">Weekly, monthly, and yearly cycles shape baseline demand</p>

    <div class="container-cq grid grid-cols-2 gap-4" style="height: 34vh">
      <div>
        <h3 class="text-lg font-bold">Yearly Seasonality</h3>
        <ul class="text-sm mt-4">
          <li>Summer peaks (June-July)</li>
          <li>Back-to-school surge (August)</li>
          <li>Holiday season (Nov-Dec)</li>
          <li>Post-holiday dip (January)</li>
        </ul>
      </div>
      <div>
        <h3 class="text-lg font-bold">Weekly Pattern</h3>
        <ul class="text-sm mt-4">
          <li>Weekend traffic (Retail): +25%</li>
          <li>Monday slump: -5%</li>
          <li>DTC smoother weekdays</li>
          <li>Correlated with foot traffic</li>
        </ul>
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
