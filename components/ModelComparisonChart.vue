<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

const chartCanvas = ref(null);
let chartInstance = null;

const modelData = {
  labels: ['Prophet', 'LightGBM', 'XGBoost', 'AutoETS', 'AutoARIMA', 'Seasonal\nNaive', 'Naive'],
  mae: [23.34, 28.90, 29.83, 33.13, 33.32, 34.34, 37.99],
  colors: [
    'rgb(34, 197, 94)',   // Prophet - green
    'rgb(59, 130, 246)',  // LightGBM - blue
    'rgb(168, 85, 247)',  // XGBoost - purple
    'rgb(251, 146, 60)',  // AutoETS - orange
    'rgb(236, 72, 153)',  // AutoARIMA - pink
    'rgb(148, 163, 184)', // SeasonalNaive - gray
    'rgb(100, 116, 139)'  // Naive - dark gray
  ]
};

onMounted(() => {
  const ctx = chartCanvas.value.getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: modelData.labels,
      datasets: [{
        label: 'MAE (pairs/day)',
        data: modelData.mae,
        backgroundColor: modelData.colors,
        borderColor: modelData.colors.map(c => c.replace('rgb', 'rgba').replace(')', ', 0.8)')),
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(17, 24, 39, 0.9)',
          titleColor: '#e5e7eb',
          bodyColor: '#e5e7eb',
          borderColor: 'rgba(59, 130, 246, 0.5)',
          borderWidth: 1,
          callbacks: {
            label: function(context) {
              return 'MAE: ' + context.parsed.y.toFixed(2) + ' pairs/day';
            },
            afterLabel: function(context) {
              if (context.dataIndex === 0) {
                return '🏆 Winner!';
              }
              return '';
            }
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#9ca3af',
            font: { size: 11 }
          },
          grid: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: '#9ca3af',
            font: { size: 10 },
            callback: function(value) {
              return value + ' pairs';
            }
          },
          grid: {
            color: 'rgba(156, 163, 175, 0.1)'
          },
          title: {
            display: true,
            text: 'Mean Absolute Error (lower is better)',
            color: '#e5e7eb',
            font: { size: 12 }
          }
        }
      }
    }
  });
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
