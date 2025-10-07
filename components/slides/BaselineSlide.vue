<template>
  <SlideLayout background="dots">
    <h1>Step 1: The Baseline</h1>
    <p class="subtitle">Start with slow, steady growth</p>

    <TwoColumnSlide
      title=""
      subtitle=""
      chart-id="baseline-chart"
      :chart-data="baselineChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Baseline Trend</h3>
        <div class="text-sm space-y-3">
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            baseline_t = 50 × (1.0003)^t
          </div>
          <ul class="space-y-2">
            <li>Starts at <strong>50 pairs/day</strong></li>
            <li>Grows <strong>~12% per year</strong></li>
            <li>Ends at <strong>~97 pairs/day</strong> (after 6 years)</li>
            <li>Represents organic brand growth</li>
          </ul>
          <div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-xs">
            <strong>Why multiplicative?</strong><br/>
            In retail, a 10% promo on 100 units ≠ 10% promo on 50 units.<br/>
            Effects scale with baseline level.
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../SlideLayout.vue'
import TwoColumnSlide from '../TwoColumnSlide.vue'

const baselineChartData = () => {
  const n = 2192;
  const t = Array.from({length: n}, (_, i) => i);
  const dates = t.map(i => {
    const d = new Date('2019-01-01');
    d.setDate(d.getDate() + i);
    return d.toISOString().split('T')[0];
  });
  const baseline = t.map(i => 50 * Math.pow(1.0003, i));

  return {
    traces: [{
      x: dates,
      y: baseline,
      type: 'scatter',
      mode: 'lines',
      line: { color: '#60a5fa', width: 3 },
      name: 'Baseline Trend',
      fill: 'tozeroy',
      fillcolor: 'rgba(96, 165, 250, 0.1)'
    }],
    layout: {
      margin: { l: 50, r: 20, t: 10, b: 35 },
      xaxis: { gridcolor: '#374151', title: 'Date' },
      yaxis: { gridcolor: '#374151', title: 'Pairs per Day', range: [0, 120] },
      showlegend: false
    },
    config: {}
  };
};
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
