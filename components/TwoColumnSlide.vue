<template>
  <div>
    <h1 v-if="title" class="text-3xl font-bold mb-4">{{ title }}</h1>
    <p v-if="subtitle" class="text-lg mb-6 opacity-80">{{ subtitle }}</p>

    <div class="grid grid-cols-2 gap-6" style="height: 25vh;">
      <div>
        <slot name="content"></slot>
      </div>
      <div class="graph-container glass-background">
        <div :id="chartId"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onActivated, nextTick } from 'vue';
import Plotly from 'plotly.js-dist-min';

const props = defineProps({
  title: String,
  subtitle: String,
  chartId: {
    type: String,
    required: true
  },
  chartData: {
    type: Function,
    required: true
  }
});

onMounted(async () => {
  // Wait for DOM to be fully ready and container sized
  await nextTick();
  await new Promise(resolve => setTimeout(resolve, 300));

  // Call the chartData function to get trace, layout, config, and optional frames
  const { traces, layout, config, frames } = props.chartData();

  // Ensure layout has proper defaults
  const finalLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#e5e7eb', size: 10 },
    autosize: true,
    ...layout
  };

  const finalConfig = {
    responsive: true,
    displayModeBar: false,
    ...config
  };

  // Get the chart element
  const chartElement = document.getElementById(props.chartId);
  if (!chartElement) return;

  // Create plot with frames if they exist
  if (frames && frames.length > 0) {
    await Plotly.newPlot(props.chartId, traces, finalLayout, finalConfig);
    await Plotly.addFrames(props.chartId, frames);

    // Function to play animation with pause and loop
    const playAnimation = async () => {
      await Plotly.animate(props.chartId, null, {
        frame: { duration: 80, redraw: true },
        transition: { duration: 40 },
        mode: 'immediate'
      });
      // Pause for 1 second, then loop
      setTimeout(() => {
        Plotly.animate(props.chartId, ['frame0'], {
          frame: { duration: 0, redraw: true },
          transition: { duration: 0 }
        }).then(playAnimation);
      }, 1000);
    };

    playAnimation();
  } else {
    Plotly.newPlot(props.chartId, traces, finalLayout, finalConfig);
  }

  // Add resize observer to handle container size changes
  const resizeObserver = new ResizeObserver(() => {
    Plotly.Plots.resize(props.chartId);
  });

  const container = chartElement.parentElement;
  if (container) {
    resizeObserver.observe(container);
  }
});

// Handle slide activation (when navigating between slides)
onActivated(async () => {
  await nextTick();
  await new Promise(resolve => setTimeout(resolve, 200));

  const chartElement = document.getElementById(props.chartId);
  if (chartElement && chartElement.layout) {
    Plotly.Plots.resize(props.chartId);
  }
});
</script>

<style scoped>
.glass-background {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 12px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
</style>
