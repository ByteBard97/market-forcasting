<template>
  <SlideLayout>
    <h1>Step 4: Holiday Effects</h1>
    <p class="subtitle">Black Friday & Christmas drive massive spikes</p>

    <TwoColumnSlide
      chart-id="holiday-chart"
      :chart-data="holidayChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Major Shopping Holidays</h3>
        <div class="text-sm space-y-3">
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            Black Friday: +150% spike<br/>
            Christmas: +80% spike<br/>
            Memorial Day: +30% spike
          </div>

          <ul class="space-y-2">
            <li>🎄 <strong>Black Friday</strong> - Biggest day of the year</li>
            <li>🎁 <strong>Christmas week</strong> - Extended shopping period</li>
            <li>🏖️ <strong>Summer holidays</strong> - Moderate boost</li>
            <li>📅 <strong>Predictable</strong> - Same dates every year</li>
          </ul>

          <div class="mt-4 p-3 bg-red-900 bg-opacity-20 rounded text-xs">
            <strong>Stockout risk:</strong><br />
            These are the days you CANNOT run out of inventory
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
import TwoColumnSlide from '../components/TwoColumnSlide.vue'

const holidayChartData = () => {
  // Generate 2 years of data to show holiday pattern
  const days = 730
  const dates = []
  const demand = []
  const holidayMarkers = []

  const startDate = new Date('2023-01-01')

  for (let i = 0; i < days; i++) {
    const date = new Date(startDate)
    date.setDate(date.getDate() + i)
    dates.push(date.toISOString().split('T')[0])

    // Baseline
    let value = 60

    // Check for holidays
    const month = date.getMonth()
    const day = date.getDate()

    // Black Friday (late November)
    if (month === 10 && day >= 23 && day <= 27) {
      value += 90 // +150%
      if (day === 24) holidayMarkers.push({ date: dates[i], value: value, name: 'Black Friday' })
    }
    // Christmas (December)
    else if (month === 11 && day >= 20 && day <= 26) {
      value += 48 // +80%
      if (day === 25) holidayMarkers.push({ date: dates[i], value: value, name: 'Christmas' })
    }
    // Memorial Day (late May)
    else if (month === 4 && day >= 25 && day <= 31) {
      value += 18 // +30%
      if (day === 29) holidayMarkers.push({ date: dates[i], value: value, name: 'Memorial Day' })
    }

    demand.push(value)
  }

  return {
    traces: [
      {
        x: dates,
        y: demand,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#ef4444', width: 2 },
        name: 'Demand with Holidays',
        fill: 'tozeroy',
        fillcolor: 'rgba(239, 68, 68, 0.1)'
      },
      {
        x: holidayMarkers.map(h => h.date),
        y: holidayMarkers.map(h => h.value),
        type: 'scatter',
        mode: 'markers+text',
        marker: { color: '#fbbf24', size: 12, symbol: 'star' },
        text: holidayMarkers.map(h => h.name),
        textposition: 'top',
        textfont: { size: 9, color: '#fbbf24' },
        name: 'Holidays'
      }
    ],
    layout: {
      margin: { l: 50, r: 20, t: 10, b: 35 },
      xaxis: { gridcolor: '#374151', title: 'Date' },
      yaxis: { gridcolor: '#374151', title: 'Pairs per Day', range: [0, 180] },
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
