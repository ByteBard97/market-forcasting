<template>
  <SlideLayout>
    <div class="flex flex-col items-center justify-center h-full text-center">
      <h1 class="text-5xl mb-8">Dive Deeper</h1>

      <div class="pt-12">
        <a
          href="http://localhost:3030/"
          class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
        >
          View Live Presentation →
        </a>
      </div>

      <div class="mt-8 text-sm">
        <p>Explore interactive components, compare regions, analyze segments</p>
        <p class="text-xs text-gray-400 mt-2">
          All code, data, and analysis available in the project repository
        </p>
      </div>

      <div class="mt-12 text-xs text-gray-500">
        <p>Generated with synthetic data (13 multiplicative components)</p>
        <p>Models: Prophet, XGBoost, LightGBM, AutoARIMA, AutoETS, Naive baselines</p>
        <p>Validation: Walk-forward, 7-day horizon, actual lags</p>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
</script>
