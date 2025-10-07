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
    const response = await fetch(`/data/AirJordan_NA_DTC.json?t=${Date.now()}`)
    const data = await response.json()

    // Sample every 7 days for full dataset visibility
    const dates = data.calendar.ds.filter((_, i) => i % 7 === 0)
    const actual = data.observed.units.filter((_, i) => i % 7 === 0)
    const prophet = data.prophet.yhat.filter((_, i) => i % 7 === 0)

    option.value = {
      backgroundColor: 'transparent',
      animation: true,
      animationDuration: 1500,
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '12%',
        containLabel: true
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
          height: 20,
          bottom: 5,
          borderColor: '#374151',
          fillerColor: 'rgba(59, 130, 246, 0.2)',
          handleStyle: {
            color: '#3b82f6'
          },
          textStyle: {
            color: '#9ca3af',
            fontSize: 10
          }
        },
        {
          type: 'inside',
          start: 0,
          end: 100
        }
      ],
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        borderColor: 'rgba(59, 130, 246, 0.5)',
        textStyle: { color: '#e5e7eb' },
        formatter: (params) => {
          let html = `<div style="font-size:11px;margin-bottom:4px">${params[0].axisValue}</div>`
          params.forEach(p => {
            const val = Math.round(p.value)
            html += `<div style="margin-top:2px"><span style="color:${p.color}">●</span> ${p.seriesName}: <strong>${val}</strong> pairs</div>`
          })
          return html
        }
      },
      legend: {
        data: ['Actual', 'Prophet'],
        textStyle: { color: '#9ca3af', fontSize: 11 },
        top: 0,
        itemGap: 20,
        selectedMode: 'multiple'
      },
      xAxis: {
        type: 'category',
        data: dates,
        axisLine: { lineStyle: { color: '#374151' } },
        axisLabel: {
          color: '#9ca3af',
          fontSize: 9,
          formatter: (value) => {
            const d = new Date(value)
            return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`
          }
        },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'Demand (pairs)',
        nameTextStyle: { color: '#9ca3af', fontSize: 10 },
        axisLine: { lineStyle: { color: '#374151' } },
        axisLabel: { color: '#9ca3af', fontSize: 9 },
        splitLine: { lineStyle: { color: '#1f2937', type: 'dashed' } }
      },
      series: [
        {
          name: 'Actual',
          type: 'line',
          data: actual,
          lineStyle: { width: 2.5, color: '#3b82f6' },
          itemStyle: { color: '#3b82f6' },
          showSymbol: false,
          emphasis: { focus: 'series' }
        },
        {
          name: 'Prophet',
          type: 'line',
          data: prophet,
          lineStyle: { width: 2, color: '#a855f7', type: 'dashed' },
          itemStyle: { color: '#a855f7' },
          showSymbol: false,
          emphasis: { focus: 'series' }
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
