<template>
  <SlideLayout>
    <h1>Step 5: New Sneaker Drops</h1>
    <p class="subtitle">Limited releases create hype-driven demand spikes</p>

    <TwoColumnSlide
      chart-id="drop-chart"
      :chart-data="dropChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Product Launch Events</h3>
        <div class="text-sm space-y-3">
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            AJ1 "Chicago": +100% for 2 weeks<br/>
            AJ11 "Concord": +150% for 1 week<br/>
            Limited collabs: +200% for 3 days
          </div>

          <ul class="space-y-2">
            <li>👟 <strong>Limited editions</strong> - Scarcity drives demand</li>
            <li>📱 <strong>Social hype</strong> - Instagram/TikTok buzz</li>
            <li>⏱️ <strong>Sharp spike</strong> - Peak on drop day</li>
            <li>📉 <strong>Gradual decay</strong> - Returns to baseline over 1-3 weeks</li>
          </ul>

          <div class="mt-4 p-3 bg-green-900 bg-opacity-20 rounded text-xs">
            <strong>Strategic opportunity:</strong><br />
            Plan inventory around known drop dates
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
import TwoColumnSlide from '../components/TwoColumnSlide.vue'

const dropChartData = () => {
  const days = 365
  const dates = []
  const demand = []
  const dropMarkers = []

  const startDate = new Date('2024-01-01')

  // Define drop events
  const drops = [
    { day: 45, peak: 120, duration: 14, name: 'AJ1 Chicago' },
    { day: 150, peak: 150, duration: 7, name: 'AJ11 Concord' },
    { day: 260, peak: 180, duration: 3, name: 'Collab Drop' }
  ]

  for (let i = 0; i < days; i++) {
    const date = new Date(startDate)
    date.setDate(date.getDate() + i)
    dates.push(date.toISOString().split('T')[0])

    let value = 60 // baseline

    // Check if within any drop window
    drops.forEach(drop => {
      if (i >= drop.day && i < drop.day + drop.duration) {
        const daysFromDrop = i - drop.day
        // Gradual exponential decay
        const multiplier = Math.exp(-0.2 * daysFromDrop)
        value += drop.peak * multiplier

        if (i === drop.day) {
          dropMarkers.push({ date: dates[i], value: value, name: drop.name })
        }
      }
    })

    demand.push(value)
  }

  return {
    traces: [
      {
        x: dates,
        y: demand,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#10b981', width: 2 },
        name: 'Demand with Drops',
        fill: 'tozeroy',
        fillcolor: 'rgba(16, 185, 129, 0.1)'
      },
      {
        x: dropMarkers.map(d => d.date),
        y: dropMarkers.map(d => d.value),
        type: 'scatter',
        mode: 'markers+text',
        marker: { color: '#fbbf24', size: 12, symbol: 'triangle-up' },
        text: dropMarkers.map(d => d.name),
        textposition: 'top',
        textfont: { size: 9, color: '#fbbf24' },
        name: 'Drops'
      }
    ],
    layout: {
      margin: { l: 50, r: 20, t: 30, b: 50 },
      xaxis: { gridcolor: '#374151', title: '' },
      yaxis: { gridcolor: '#374151', title: 'Pairs per Day', range: [40, 260] },
      showlegend: false
    },
    config: {}
  }
}
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
