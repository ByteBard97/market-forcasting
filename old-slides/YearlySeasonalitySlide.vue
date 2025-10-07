<template>
  <SlideLayout background="dots">
    <h1>Step 3: Yearly Seasonality</h1>
    <p class="subtitle">Summer peaks and holiday surges</p>

    <TwoColumnSlide
      chart-id="yearly-chart"
      :chart-data="yearlyChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Annual Cycle</h3>
        <div class="text-sm space-y-3">
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            yearly_t = 0.15×sin(2π×t/365) + <br />
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.10×sin(4π×t/365) + 1.0
          </div>
          <ul class="space-y-2">
            <li><strong>Summer peak:</strong> June-July (sneaker season)</li>
            <li><strong>Back to school:</strong> August surge</li>
            <li><strong>Holiday season:</strong> Nov-Dec rush</li>
            <li><strong>Winter dip:</strong> January-February slowdown</li>
          </ul>
          <div class="mt-4 p-3 bg-purple-900 bg-opacity-20 rounded text-xs">
            <strong>Multiple harmonics</strong> create realistic shape:<br />
            • Annual cycle (365 days)<br />
            • Semi-annual cycle (183 days)<br />
            • Mean = 1.0, Range = [0.82, 1.24]
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
import TwoColumnSlide from "../components/TwoColumnSlide.vue";

const yearlyChartData = () => {
  const days = 730;
  const dates = Array.from({ length: days }, (_, i) => {
    const d = new Date("2023-01-01");
    d.setDate(d.getDate() + i);
    return d.toISOString().split("T")[0];
  });

  const yearly = dates.map((_, i) => {
    const t = i;
    return (
      0.15 * Math.sin((2 * Math.PI * t) / 365.25 - Math.PI / 2) +
      0.1 * Math.sin((4 * Math.PI * t) / 365.25 + Math.PI / 4) +
      1.0
    );
  });

  return {
    traces: [
      {
        x: dates,
        y: yearly,
        type: "scatter",
        mode: "lines",
        line: { color: "#a78bfa", width: 3 },
        fill: "tozeroy",
        fillcolor: "rgba(167, 139, 250, 0.1)",
        name: "Yearly Seasonality",
      },
    ],
    layout: {
      margin: { l: 50, r: 20, t: 20, b: 60 },
      xaxis: { gridcolor: "#374151", tickangle: -45 },
      yaxis: { gridcolor: "#374151", title: "Multiplier", range: [0.7, 1.3] },
      shapes: [
        {
          type: "line",
          x0: dates[0],
          x1: dates[dates.length - 1],
          y0: 1.0,
          y1: 1.0,
          line: { color: "#f59e0b", width: 1, dash: "dash" },
        },
      ],
      showlegend: false,
    },
    config: {},
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
