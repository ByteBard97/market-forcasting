<template>
  <div ref="wrapper" class="chart-wrapper">
    <v-chart v-if="isReady && option.series" class="chart" :option="option" :init-options="initOptions" autoresize />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent])

const wrapper = ref(null)
const initOptions = { renderer: 'canvas' }
const isReady = ref(false)

let ro

const modelData = {
  models: ['Prophet', 'LightGBM', 'XGBoost', 'AutoETS', 'AutoARIMA', 'Seasonal\nNaive', 'Naive'],
  mae: [23.34, 28.90, 29.83, 33.13, 33.32, 34.34, 37.99]
}

const option = ref({
  backgroundColor: 'transparent',
  animation: true,
  animationDuration: 1500,
  animationEasing: 'elasticOut',
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '8%',
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(17, 24, 39, 0.95)',
    borderColor: 'rgba(59, 130, 246, 0.5)',
    textStyle: { color: '#e5e7eb' },
    axisPointer: { type: 'shadow' },
    formatter: (params) => {
      const p = params[0]
      let extra = p.dataIndex === 0 ? '<div style="color:#22c55e;margin-top:4px">🏆 Winner!</div>' : ''
      return `<div style="font-size:12px"><strong>${p.name}</strong></div>
              <div style="margin-top:4px">MAE: <strong>${p.value.toFixed(2)}</strong> pairs/day</div>${extra}`
    }
  },
  xAxis: {
    type: 'category',
    data: modelData.models,
    axisLine: { lineStyle: { color: '#374151' } },
    axisLabel: {
      color: '#9ca3af',
      fontSize: 11,
      interval: 0
    },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    name: 'MAE (pairs/day)',
    nameTextStyle: { color: '#9ca3af', fontSize: 11 },
    axisLine: { lineStyle: { color: '#374151' } },
    axisLabel: {
      color: '#9ca3af',
      fontSize: 10
    },
    splitLine: { lineStyle: { color: '#1f2937', type: 'dashed' } }
  },
  series: [
    {
      type: 'bar',
      data: modelData.mae.map((v, i) => ({
        value: v,
        itemStyle: {
          color: i === 0 ? {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: '#22c55e' },
              { offset: 1, color: '#16a34a' }
            ]
          } : {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: i < 3 ? '#3b82f6' : '#6b7280' },
              { offset: 1, color: i < 3 ? '#1d4ed8' : '#4b5563' }
            ]
          },
          borderRadius: [4, 4, 0, 0]
        }
      })),
      barWidth: '60%',
      label: {
        show: true,
        position: 'top',
        color: '#e5e7eb',
        fontSize: 11,
        formatter: '{c}'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          shadowColor: 'rgba(59, 130, 246, 0.5)'
        }
      }
    }
  ]
})

onMounted(async () => {
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
