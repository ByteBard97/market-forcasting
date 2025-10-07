<template>
  <SlideLayout>
    <h1>Enter Prophet</h1>
    <p class="subtitle">Facebook's forecasting tool designed for business time series</p>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="text-xl font-bold mb-4 text-blue-400">What is Prophet?</h3>
        <ul class="text-sm space-y-2">
          <li>🏢 <strong>Developed by Meta</strong> (Facebook) in 2017</li>
          <li>📊 <strong>Business-focused</strong> - Built for daily/weekly data</li>
          <li>🎯 <strong>Automatic</strong> - Finds seasonality & trends</li>
          <li>📅 <strong>Handles holidays</strong> - Built-in calendar support</li>
          <li>🔓 <strong>Open source</strong> - Free Python/R library</li>
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-bold mb-4 text-green-400">Why Prophet?</h3>
        <ul class="text-sm space-y-2">
          <li>✓ <strong>Perfect for our data</strong> - Seasonal + trends + events</li>
          <li>✓ <strong>No feature engineering</strong> - Doesn't need lag features</li>
          <li>✓ <strong>Uncertainty built-in</strong> - Gives confidence intervals</li>
          <li>✓ <strong>Interpretable</strong> - Can explain predictions</li>
          <li>✓ <strong>Fast</strong> - Trains in seconds</li>
        </ul>
      </div>
    </div>

    <div class="mt-8 p-4 bg-blue-900 bg-opacity-20 rounded">
      <strong>Prophet's Magic:</strong> It automatically decomposes the time series into:<br />
      <span class="text-sm opacity-80">Trend + Weekly Seasonality + Yearly Seasonality + Holidays</span><br />
      <span class="text-sm opacity-80">(Exactly what we built!)</span>
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
