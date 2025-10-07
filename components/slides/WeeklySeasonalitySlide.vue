<template>
  <SlideLayout background="sphere">
    <h1>Step 2: Weekly Seasonality</h1>
    <p class="subtitle">Weekend uplift for retail traffic</p>

    <TwoColumnSlide
      chart-id="weekly-chart"
      :chart-data="weeklyChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Weekly Pattern</h3>
        <div class="text-sm space-y-3">
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            weekly_t = 1.25  if weekend<br/>
            weekly_t = 0.95  if weekday
          </div>
          <ul class="space-y-2">
            <li><strong>Weekdays (M-F):</strong> 0.95× multiplier (5% dip)</li>
            <li><strong>Weekends (S-S):</strong> 1.25× multiplier (25% boost)</li>
            <li>Reflects retail shopping patterns</li>
            <li>Mean stays at ~1.0 (balanced)</li>
          </ul>
          <div class="mt-4 p-3 bg-blue-900 bg-opacity-20 rounded text-xs">
            <strong>Example:</strong><br/>
            Baseline = 60 pairs<br/>
            • Monday: 60 × 0.95 = 57 pairs<br/>
            • Saturday: 60 × 1.25 = 75 pairs
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../SlideLayout.vue'
import TwoColumnSlide from '../TwoColumnSlide.vue'

const weeklyChartData = () => {
  const days = 28;
  const dates = Array.from({length: days}, (_, i) => {
    const d = new Date('2024-01-01');
    d.setDate(d.getDate() + i);
    return d.toISOString().split('T')[0];
  });

  const weekly = dates.map((_, i) => {
    const dayOfWeek = new Date(dates[i]).getDay();
    return (dayOfWeek === 0 || dayOfWeek === 6) ? 1.25 : 0.95;
  });

  return {
    traces: [{
      x: dates,
      y: weekly,
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: '#60a5fa', width: 2 },
      marker: { size: 6, color: '#60a5fa' },
      name: 'Weekly Multiplier'
    }],
    layout: {
      margin: { l: 50, r: 20, t: 20, b: 60 },
      xaxis: { gridcolor: '#374151', tickangle: -45 },
      yaxis: { gridcolor: '#374151', title: 'Multiplier', range: [0.8, 1.4] },
      shapes: [{
        type: 'line',
        x0: dates[0],
        x1: dates[dates.length-1],
        y0: 1.0,
        y1: 1.0,
        line: { color: '#f59e0b', width: 1, dash: 'dash' }
      }],
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
