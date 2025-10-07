<template>
  <SlideLayout background="sphere">
    <h1>Final Results: Best of Both Worlds</h1>
    <p class="subtitle"><strong>With realistic validation</strong> (7-day horizon, actual lags, exogenous regressors)</p>

    <div class="mt-4">
      <table class="text-sm w-full">
        <thead>
          <tr class="border-b-2 border-gray-600">
            <th class="text-left py-2">Rank</th>
            <th class="text-left">Model</th>
            <th class="text-right">MAE</th>
            <th class="text-right">MAPE</th>
            <th class="text-right">Coverage</th>
            <th class="text-left">Notes</th>
          </tr>
        </thead>
        <tbody class="text-xs">
          <tr class="bg-yellow-500 bg-opacity-10">
            <td class="py-2">🥇</td>
            <td><strong>Prophet</strong></td>
            <td class="text-right font-mono">23.34</td>
            <td class="text-right font-mono">127.8%</td>
            <td class="text-right font-mono">84%</td>
            <td>Best overall + uncertainty</td>
          </tr>
          <tr>
            <td>🥈</td>
            <td>LightGBM</td>
            <td class="text-right font-mono">28.90</td>
            <td class="text-right font-mono">107.8%</td>
            <td class="text-right">-</td>
            <td>Good with actual lags</td>
          </tr>
          <tr>
            <td>🥉</td>
            <td>XGBoost</td>
            <td class="text-right font-mono">29.83</td>
            <td class="text-right font-mono">109.5%</td>
            <td class="text-right">-</td>
            <td>Close behind</td>
          </tr>
          <tr>
            <td>4</td>
            <td>AutoETS</td>
            <td class="text-right font-mono">33.13</td>
            <td class="text-right font-mono">81.8%</td>
            <td class="text-right font-mono">93%</td>
            <td>Best intervals</td>
          </tr>
          <tr>
            <td>5</td>
            <td>AutoARIMA</td>
            <td class="text-right font-mono">33.32</td>
            <td class="text-right font-mono">96.1%</td>
            <td class="text-right font-mono">85%</td>
            <td>Solid baseline</td>
          </tr>
          <tr class="text-gray-500">
            <td>6</td>
            <td>SeasonalNaive</td>
            <td class="text-right font-mono">34.34</td>
            <td class="text-right font-mono">88.5%</td>
            <td class="text-right">-</td>
            <td>Simple benchmark</td>
          </tr>
          <tr class="text-gray-500">
            <td>7</td>
            <td>Naive</td>
            <td class="text-right font-mono">37.99</td>
            <td class="text-right font-mono">81.7%</td>
            <td class="text-right">-</td>
            <td>Baseline</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4 grid grid-cols-2 gap-4 text-xs">
      <div class="p-2 bg-blue-900 bg-opacity-20 rounded">
        <strong>MAE = 23.34 means:</strong> Off by ~23 pairs/day on average (for 50-80 pairs/day typical sales = 29-46% error)
      </div>
      <div class="p-2 bg-green-900 bg-opacity-20 rounded">
        <strong>Coverage = 84% means:</strong> Confidence intervals capture 84% of actuals (target: 95%, but 84% is realistic)
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../SlideLayout.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
