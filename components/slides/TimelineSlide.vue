<template>
  <SlideLayout background="dots">
    <h1>The Signal: 6 Years of Demand</h1>
    <p class="subtitle">Interactive view of Air Jordan sales patterns with product drop events</p>

    <div style="height: 450px; width: 100%;">
      <AnimatedTimeline />
    </div>

    <div class="mt-2 text-xs text-gray-400">
      🚀 = Product Drop Events • Hover to explore • Gradient shows growth over time
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../SlideLayout.vue'
import AnimatedTimeline from '../AnimatedTimeline.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
