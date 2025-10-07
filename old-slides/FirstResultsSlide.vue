<template>
  <SlideLayout background="dots">
    <h1>First Results: Too Good to Be True?</h1>
    <p class="subtitle">Initial benchmark looked impressive...</p>

    <div class="grid grid-cols-2 gap-8 mt-6">
      <div>
        <h3 class="text-lg font-bold mb-4">Initial Results (56-day horizon)</h3>
        <table class="text-sm w-full">
          <thead>
            <tr class="border-b border-gray-600">
              <th class="text-left py-2">Model</th>
              <th class="text-right">MAE</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-green-400">
              <td>LightGBM</td>
              <td class="text-right font-mono">19.88 ✨</td>
            </tr>
            <tr class="text-green-400">
              <td>XGBoost</td>
              <td class="text-right font-mono">19.99 ✨</td>
            </tr>
            <tr>
              <td>Prophet</td>
              <td class="text-right font-mono">27.76 😞</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <h3 class="text-lg font-bold mb-4 text-red-400">🚨 Problem Discovered</h3>
        <div class="text-sm space-y-3">
          <p><strong>Question:</strong> Why are ML models <em>so much better</em>?</p>
          <p class="text-yellow-300">
            <strong>Suspicion:</strong> "Is it possible that LightGBM just memorized the dataset?"
          </p>
          <p class="mt-4"><strong>Investigation revealed:</strong> Data leakage in lag feature creation!</p>
        </div>
      </div>
    </div>

    <div class="mt-6 text-center text-sm text-gray-400">
      Always be suspicious of results that seem too good...
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
