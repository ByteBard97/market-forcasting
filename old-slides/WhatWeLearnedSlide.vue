<template>
  <SlideLayout>
    <h1>What We Learned</h1>
    <p class="subtitle">The complete journey from data to production-ready model</p>

    <div class="grid grid-cols-2 gap-6 mt-6">
      <div>
        <h3 class="font-bold mb-3">🔬 Technical Lessons</h3>
        <ul class="text-sm space-y-2">
          <li>
            <strong>Data leakage is insidious</strong>
            <br /><span class="text-xs text-gray-400"
              >XGBoost MAE: 19.99 → 29.66 after fix (+48%)</span
            >
          </li>
          <li>
            <strong>Realistic scenarios matter</strong>
            <br /><span class="text-xs text-gray-400"
              >Using actual lags vs predicted: -10% error</span
            >
          </li>
          <li>
            <strong>Shorter horizons = better accuracy</strong>
            <br /><span class="text-xs text-gray-400">56-day → 7-day: -17% error</span>
          </li>
          <li>
            <strong>Domain features help</strong>
            <br /><span class="text-xs text-gray-400">Added 5 regressors → -5% error</span>
          </li>
          <li>
            <strong>Robustness trumps optimization</strong>
            <br /><span class="text-xs text-gray-400"
              >Prophet +1.9% with harder data (resilient!)</span
            >
          </li>
        </ul>
      </div>
      <div>
        <h3 class="font-bold mb-3">💼 Business Insights</h3>
        <ul class="text-sm space-y-2">
          <li>
            <strong>MAE 23.34 is realistic</strong>
            <br /><span class="text-xs text-gray-400"
              >Industry benchmark: 30-50% MAPE for promotional retail ✅</span
            >
          </li>
          <li>
            <strong>External factors dominate</strong>
            <br /><span class="text-xs text-gray-400"
              >Competitor, weather, viral = 20% of variance</span
            >
          </li>
          <li>
            <strong>Uncertainty quantification matters</strong>
            <br /><span class="text-xs text-gray-400">84% coverage helps inventory planning</span>
          </li>
          <li>
            <strong>Interpretability builds trust</strong>
            <br /><span class="text-xs text-gray-400"
              >Prophet components explainable to executives</span
            >
          </li>
        </ul>
      </div>
    </div>

    <div class="mt-6 p-4 bg-green-900 bg-opacity-20 rounded text-center">
      <strong>Recommendation:</strong> Prophet with exogenous regressors is production-ready
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
