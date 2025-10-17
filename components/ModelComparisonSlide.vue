<template>
  <SlideLayout background="dots">
    <h1>Model Comparison</h1>
    <p class="subtitle">
      <strong>Which model handles this complexity best?</strong>
    </p>

    <div style="height: 450px; width: 100%">
      <ModelBars />
    </div>

    <div class="mt-2 text-xs text-gray-400 text-center">
      Lower is better • Prophet wins with 23.34 MAE (19% better than #2)
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
import ModelBars from "../components/ModelBars.vue";
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
