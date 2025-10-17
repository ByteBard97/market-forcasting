<template>
  <div ref="wrapper" class="chart-wrapper">
    <v-chart v-if="isReady && option.series" class="chart" :option="option" :init-options="initOptions" autoresize />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent])

const wrapper = ref(null)
const initOptions = { renderer: 'canvas' }
const option = ref({})
const isReady = ref(false)

let ro

onMounted(async () => {
  await initChart()
  await nextTick()

  const el = wrapper.value
  if (!el) return

  if (el.clientWidth > 0 && el.clientHeight > 0) {
    isReady.value = true
    return
  }

  ro = new ResizeObserver(entries => {
    for (const e of entries) {
      const w = e.contentBoxSize?.[0]?.inlineSize ?? el.clientWidth
      const h = e.contentBoxSize?.[0]?.blockSize ?? el.clientHeight
      if (w > 0 && h > 0) {
        isReady.value = true
        ro?.disconnect()
        ro = null
      }
    }
  })
  ro.observe(el)
})

onUnmounted(() => {
  ro?.disconnect()
})

async function initChart() {
  try {
    const baseUrl = import.meta.env.BASE_URL || '/'
    const response = await fetch(`${baseUrl}data/AirJordan_NA_DTC.json`)
    const data = await response.json()

  // Get last 180 days for visualization
  const startIdx = data.calendar.ds.length - 180
  const dates = data.calendar.ds.slice(startIdx)
  const demand = data.observed.units.slice(startIdx)

  // Create forecast cone (last 30 days)
  const forecastStart = dates.length - 30
  const actualDates = dates.slice(0, forecastStart)
  const forecastDates = dates.slice(forecastStart)
  const actualDemand = demand.slice(0, forecastStart)
  const forecastDemand = demand.slice(forecastStart)

  // Generate prediction intervals (simulated)
  const upperBound = forecastDemand.map((v, i) => v * (1 + 0.15 + i * 0.01))
  const lowerBound = forecastDemand.map((v, i) => v * (1 - 0.15 - i * 0.01))

  option.value = {
    backgroundColor: 'transparent',
    animation: true,
    animationDuration: 2000,
    animationEasing: 'cubicOut',
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '12%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      borderColor: 'rgba(59, 130, 246, 0.5)',
      textStyle: { color: '#e5e7eb' },
      formatter: (params) => {
        let html = `<div style="font-size:12px">${params[0].axisValue}</div>`
        params.forEach(p => {
          if (p.seriesName !== 'Upper' && p.seriesName !== 'Lower') {
            html += `<div style="margin-top:4px"><span style="color:${p.color}">●</span> ${p.seriesName}: <strong>${Math.round(p.value)}</strong> pairs</div>`
          }
        })
        return html
      }
    },
    legend: {
      data: ['Actual', 'Forecast'],
      textStyle: { color: '#9ca3af', fontSize: 11 },
      top: 0
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#374151' } },
      axisLabel: {
        color: '#9ca3af',
        fontSize: 10,
        formatter: (value) => {
          const d = new Date(value)
          return `${d.getMonth()+1}/${d.getDate()}`
        }
      },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#374151' } },
      axisLabel: {
        color: '#9ca3af',
        fontSize: 10,
        formatter: (v) => Math.round(v) + ' pairs'
      },
      splitLine: { lineStyle: { color: '#1f2937', type: 'dashed' } }
    },
    series: [
      {
        name: 'Actual',
        type: 'line',
        data: actualDemand,
        smooth: true,
        lineStyle: { width: 3, color: '#3b82f6' },
        itemStyle: { color: '#3b82f6' },
        showSymbol: false,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
            ]
          }
        }
      },
      {
        name: 'Forecast',
        type: 'line',
        data: new Array(forecastStart).fill(null).concat(forecastDemand),
        smooth: true,
        lineStyle: { width: 3, color: '#a855f7', type: 'dashed' },
        itemStyle: { color: '#a855f7' },
        showSymbol: false
      },
      {
        name: 'Upper',
        type: 'line',
        data: new Array(forecastStart).fill(null).concat(upperBound),
        lineStyle: { opacity: 0 },
        stack: 'confidence',
        symbol: 'none',
        silent: true
      },
      {
        name: 'Lower',
        type: 'line',
        data: new Array(forecastStart).fill(null).concat(lowerBound),
        lineStyle: { opacity: 0 },
        areaStyle: {
          color: 'rgba(168, 85, 247, 0.15)'
        },
        stack: 'confidence',
        symbol: 'none',
        silent: true
      }
    ]
  }
  } catch (error) {
    console.error('Error loading chart data:', error)
  }
}
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
