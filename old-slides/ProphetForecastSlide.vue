<template>
  <SlideLayout>
    <h1>Prophet Forecast</h1>
    <p class="subtitle">Model captures trend + seasonality + holiday effects + exogenous factors</p>

    <div class="grid grid-cols-2 gap-8 mt-4">
      <div class="text-sm">
        <h3 class="font-bold mb-2">Features Used:</h3>
        <ul class="space-y-0.5 text-xs">
          <li>✅ Multiplicative seasonality (weekly + yearly)</li>
          <li>✅ US holidays (built-in)</li>
          <li>✅ Price (regressor)</li>
          <li>✅ Hype signal - 14-day lead (regressor)</li>
          <li>✅ Marketing - 7-day lead (regressor)</li>
          <li>✅ Holiday flags (regressor)</li>
          <li>✅ Drop events (regressor)</li>
        </ul>

        <h3 class="font-bold mt-3 mb-1.5">Final Metrics (7-day):</h3>
        <ul class="space-y-0.5 text-xs">
          <li><strong>MAE:</strong> 23.34 pairs/day</li>
          <li><strong>MAPE:</strong> 127.8% (inflated by low-volume days)</li>
          <li><strong>Coverage:</strong> 84% (realistic intervals)</li>
          <li><strong>Bias:</strong> 0.01 (unbiased!)</li>
        </ul>
      </div>

      <div>
        <div style="height: 400px; width: 100%">
          <ForecastCone />
        </div>

        <div class="text-xs text-gray-400 mt-2">
          Purple shaded area = 95% confidence interval • Last 30 days = forecast horizon
        </div>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
import ForecastCone from "../components/ForecastCone.vue";
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
