<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { Chart, LineController, LineElement, PointElement, LinearScale, TimeScale, Title, Tooltip, Legend } from 'chart.js';
import 'chartjs-adapter-date-fns';

Chart.register(LineController, LineElement, PointElement, LinearScale, TimeScale, Title, Tooltip, Legend);

const chartCanvas = ref(null);
let chartInstance = null;

onMounted(async () => {
  try {
    const response = await fetch('/data/AirJordan_NA_DTC.json');
    const data = await response.json();

    // Sample every 7 days for performance
    const dates = data.calendar.ds.filter((_, i) => i % 7 === 0);
    const weekly = data.ground_truth.weekly.filter((_, i) => i % 7 === 0);
    const yearly = data.ground_truth.yearly.filter((_, i) => i % 7 === 0);
    const holiday = data.ground_truth.holiday.filter((_, i) => i % 7 === 0);
    const promo = data.ground_truth.promo.filter((_, i) => i % 7 === 0);

    const ctx = chartCanvas.value.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Weekly Seasonality',
            data: weekly,
            borderColor: 'rgb(59, 130, 246)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
          },
          {
            label: 'Yearly Seasonality',
            data: yearly,
            borderColor: 'rgb(168, 85, 247)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
          },
          {
            label: 'Holiday Effect',
            data: holiday,
            borderColor: 'rgb(239, 68, 68)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0,
          },
          {
            label: 'Promotions',
            data: promo,
            borderColor: 'rgb(34, 197, 94)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          legend: {
            labels: {
              color: '#e5e7eb',
              font: { size: 11 },
              boxWidth: 12
            }
          },
          tooltip: {
            backgroundColor: 'rgba(17, 24, 39, 0.9)',
            titleColor: '#e5e7eb',
            bodyColor: '#e5e7eb',
            borderColor: 'rgba(59, 130, 246, 0.5)',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + 'x';
              }
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'month',
              displayFormats: {
                month: 'MMM yyyy'
              }
            },
            ticks: {
              color: '#9ca3af',
              font: { size: 9 }
            },
            grid: {
              color: 'rgba(156, 163, 175, 0.1)'
            }
          },
          y: {
            beginAtZero: false,
            ticks: {
              color: '#9ca3af',
              font: { size: 9 },
              callback: function(value) {
                return value.toFixed(1) + 'x';
              }
            },
            grid: {
              color: 'rgba(156, 163, 175, 0.1)'
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error loading chart data:', error);
  }
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
