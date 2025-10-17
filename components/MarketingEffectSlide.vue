<template>
  <SlideLayout background="dots">
    <h1>Step 5: Marketing Effect</h1>
    <p class="subtitle">Campaigns need lead time to work</p>

    <TwoColumnSlide
      chart-id="marketing-effect-chart"
      :chart-data="marketingEffectChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Marketing → Demand</h3>
        <div class="text-sm space-y-3">
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            IR = [0.05, 0.1, ..., 1.0, ..., 0.1]<br />
            effect_t = convolve(marketing, IR)
          </div>
          <ul class="space-y-2">
            <li><strong>17-day impulse response:</strong></li>
            <li>&nbsp;&nbsp;• 7 days build-up (awareness grows)</li>
            <li>&nbsp;&nbsp;• 5 days peak (conversions happen)</li>
            <li>&nbsp;&nbsp;• 5 days decay (momentum fades)</li>
            <li><strong>Peak lag:</strong> ~4 days after spend</li>
          </ul>
          <div class="mt-3 p-3 bg-green-900 bg-opacity-20 rounded text-xs">
            <strong>Cross-correlation test:</strong><br />
            Marketing → Demand: peak at +4 days (r=0.16)<br />
            <span class="text-green-400">✓ Confirms marketing LEADS demand</span>
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
import TwoColumnSlide from "../components/TwoColumnSlide.vue";

const marketingEffectChartData = () => {
  const days = 60;
  const marketing_raw = Array(days).fill(1.0);
  for (let i = 20; i <= 30; i++) marketing_raw[i] = 2.0;

  // Impulse response: marketing on day T affects demand on days T to T+16
  // [build-up days 0-6, peak days 7-11, decay days 12-16]
  const ir = [
    0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0, 1.0, 0.9, 0.7, 0.5,
    0.3, 0.2, 0.1,
  ];
  const effect = Array(days).fill(0);

  // Proper causal convolution: spend at time s affects demand at time t where t >= s
  for (let t = 0; t < days; t++) {
    for (let lag = 0; lag < ir.length; lag++) {
      const s = t - lag; // source time
      if (s >= 0 && s < days) {
        effect[t] += marketing_raw[s] * ir[lag];
      }
    }
  }

  const dates = Array.from({ length: days }, (_, i) => `Day ${i}`);

  // Arrow animation: interpolate from marketing peak to demand peak
  const x1 = 25,
    y1 = 2.5; // Marketing peak
  const x2 = 34,
    y2 = 15.0; // Demand peak (actual peak is around day 34)
  const numFrames = 20;

  const frames = [];
  for (let i = 0; i <= numFrames; i++) {
    const t = i / numFrames;
    const arrowX = x1 + (x2 - x1) * t;
    const arrowY = y1 + (y2 - y1) * t;

    frames.push({
      name: `frame${i}`,
      layout: {
        annotations: [
          {
            x: `Day ${Math.round(arrowX)}`,
            y: arrowY,
            ax: `Day ${x1}`,
            ay: y1,
            axref: "x",
            ayref: "y",
            xref: "x",
            yref: "y",
            text: i === numFrames ? "~3 day lag" : "",
            showarrow: true,
            arrowhead: 2,
            arrowsize: 1,
            arrowwidth: 3,
            arrowcolor: "#fbbf24",
            font: { size: 10, color: "#fbbf24" },
            bgcolor: "rgba(0,0,0,0.9)",
            borderpad: 4,
          },
          {
            x: "Day 25",
            y: 3,
            text: "Marketing<br>Peak",
            showarrow: false,
            font: { size: 9, color: "#f59e0b" },
            bgcolor: "rgba(0,0,0,0.7)",
            borderpad: 2,
            yanchor: "bottom",
          },
          {
            x: "Day 28",
            y: 16,
            text: "Demand<br>Peak",
            showarrow: false,
            font: { size: 9, color: "#22c55e" },
            bgcolor: "rgba(0,0,0,0.7)",
            borderpad: 2,
            yanchor: "bottom",
          },
        ],
      },
    });
  }

  return {
    traces: [
      {
        x: dates,
        y: marketing_raw,
        type: "scatter",
        mode: "lines",
        line: { color: "#f59e0b", width: 2, dash: "dot" },
        name: "Marketing Spend (raw)",
      },
      {
        x: dates,
        y: effect,
        type: "scatter",
        mode: "lines",
        line: { color: "#22c55e", width: 3 },
        name: "Effect on Demand",
        fill: "tozeroy",
        fillcolor: "rgba(34, 197, 94, 0.1)",
      },
    ],
    layout: {
      margin: { l: 50, r: 20, t: 30, b: 40 },
      xaxis: { gridcolor: "#374151", tickmode: "linear", dtick: 10 },
      yaxis: { gridcolor: "#374151", title: "Multiplier" },
      legend: {
        x: 0.5,
        xanchor: "center",
        y: 1.05,
        orientation: "h",
        font: { size: 9 },
      },
    },
    config: {},
    frames: frames,
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
