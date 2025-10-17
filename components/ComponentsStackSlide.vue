<template>
  <SlideLayout background="sphere">
    <h1>How the Pieces Combine</h1>
    <p class="subtitle">
      <strong>13 multiplicative components</strong> create realistic demand
      patterns
    </p>

    <div style="height: 450px; width: 100%">
      <ComponentsStack />
    </div>

    <div class="mt-2 text-xs text-gray-400 text-center">
      Click legend to isolate components • Hover for multiplier values
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
import ComponentsStack from "../components/ComponentsStack.vue";
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
