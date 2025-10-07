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
import { GridComponent, TooltipComponent, LegendComponent, MarkLineComponent, MarkPointComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, MarkLineComponent, MarkPointComponent])

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
    const response = await fetch('/data/AirJordan_NA_DTC.json')
    const data = await response.json()

  // Sample every 7 days for performance
  const dates = data.calendar.ds.filter((_, i) => i % 7 === 0)
  const demand = data.observed.units.filter((_, i) => i % 7 === 0)
  const baseline = data.ground_truth.baseline.filter((_, i) => i % 7 === 0)
  const dropFlags = data.events.drop_flag.filter((_, i) => i % 7 === 0)

  // Find major events for markers
  const dropEvents = []
  dropFlags.forEach((v, i) => {
    if (v === 1) {
      dropEvents.push({ xAxis: dates[i], name: '🚀', value: demand[i] })
    }
  })

  option.value = {
    backgroundColor: 'transparent',
    animation: true,
    animationDuration: 2000,
    animationEasing: 'elasticOut',
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '12%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      borderColor: 'rgba(59, 130, 246, 0.5)',
      textStyle: { color: '#e5e7eb' },
      axisPointer: {
        type: 'cross',
        lineStyle: { color: '#374151', type: 'dashed' }
      }
    },
    legend: {
      data: ['Actual Demand', 'Baseline Trend'],
      textStyle: { color: '#9ca3af', fontSize: 12 },
      top: 0,
      itemGap: 20
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
          return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`
        }
      },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#374151' } },
      axisLabel: {
        color: '#9ca3af',
        fontSize: 10
      },
      splitLine: { lineStyle: { color: '#1f2937', type: 'dashed' } }
    },
    series: [
      {
        name: 'Actual Demand',
        type: 'line',
        data: demand,
        smooth: true,
        lineStyle: {
          width: 3,
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 1, y2: 0,
            colorStops: [
              { offset: 0, color: '#3b82f6' },
              { offset: 0.5, color: '#8b5cf6' },
              { offset: 1, color: '#ec4899' }
            ]
          }
        },
        itemStyle: { color: '#3b82f6' },
        showSymbol: false,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.4)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.02)' }
            ]
          }
        },
        markPoint: {
          symbol: 'pin',
          symbolSize: 40,
          data: dropEvents.slice(0, 5),
          label: {
            fontSize: 16,
            color: '#fff'
          }
        }
      },
      {
        name: 'Baseline Trend',
        type: 'line',
        data: baseline,
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#a855f7',
          type: 'dashed'
        },
        itemStyle: { color: '#a855f7' },
        showSymbol: false
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
  min-height: 400px;
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
