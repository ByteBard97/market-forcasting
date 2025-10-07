<template>
  <SlideLayout background="dots">
    <h1>After Fixing: Honest Evaluation</h1>
    <p class="subtitle">Error increased 48% when we removed the "cheat"</p>

    <div class="grid grid-cols-2 gap-8 mt-6">
      <div>
        <h3 class="font-bold mb-4">Results After Fix (56-day)</h3>
        <table class="text-sm w-full">
          <thead>
            <tr class="border-b border-gray-600">
              <th class="text-left py-2">Model</th>
              <th class="text-right">MAE</th>
              <th class="text-right">Change</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-green-400">
              <td>Prophet</td>
              <td class="text-right font-mono">27.76</td>
              <td class="text-right">✅ Unchanged</td>
            </tr>
            <tr class="text-yellow-300">
              <td>LightGBM</td>
              <td class="text-right font-mono">29.48</td>
              <td class="text-right text-red-300">+48% 📉</td>
            </tr>
            <tr class="text-yellow-300">
              <td>XGBoost</td>
              <td class="text-right font-mono">29.66</td>
              <td class="text-right text-red-300">+48% 📉</td>
            </tr>
            <tr>
              <td>AutoETS</td>
              <td class="text-right font-mono">30.42</td>
              <td class="text-right">-</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <h3 class="font-bold mb-4">Key Insights</h3>
        <ul class="text-sm space-y-3">
          <li>✅ <strong>Prophet wins</strong> when validation is fair</li>
          <li>📉 ML models struggled without seeing the future</li>
          <li>🔍 But there's more to the story...</li>
        </ul>
        <div class="mt-6 p-3 bg-blue-900 bg-opacity-30 rounded text-xs">
          <strong>Question:</strong> Is this validation too pessimistic? In production, don't we have
          yesterday's actual sales?
        </div>
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
