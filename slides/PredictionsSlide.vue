<template>
  <SlideLayout background="dots">
    <h1>Predictions vs Actual</h1>
    <p class="subtitle">How well does Prophet track actual demand?</p>

    <div style="height: 450px; width: 100%">
      <ModelPredictions />
    </div>

    <div class="mt-2 text-xs text-gray-400 text-center">
      6 years of data (2019-2024) • Use slider or scroll to zoom • Click legend to toggle series
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
import ModelPredictions from "../components/ModelPredictions.vue";
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
