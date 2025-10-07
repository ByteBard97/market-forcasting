<template>
  <div ref="wrapper" class="chart-wrapper">
    <v-chart
      v-if="isReady && option?.series?.length"
      class="chart"
      :option="option"
      :init-options="initOptions"
      autoresize
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent])

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
    const response = await fetch(`${baseUrl}data/AirJordan_NA_DTC.json?t=${Date.now()}`)
    const data = await response.json()

    const dates = data.calendar.ds.filter((_, i) => i % 7 === 0)
    const weekly = data.ground_truth.weekly.filter((_, i) => i % 7 === 0)
    const yearly = data.ground_truth.yearly.filter((_, i) => i % 7 === 0)
    const holiday = data.ground_truth.holiday.filter((_, i) => i % 7 === 0)
    const competitor = data.ground_truth.competitor.filter((_, i) => i % 7 === 0)
    const viral = data.ground_truth.viral.filter((_, i) => i % 7 === 0)

    option.value = {
      backgroundColor: 'transparent',
      animation: true,
      animationDuration: 1500,
      animationEasing: 'cubicInOut',
      grid: { left: '3%', right: '4%', bottom: '12%', top: '15%', containLabel: true },
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        borderColor: 'rgba(59, 130, 246, 0.5)',
        textStyle: { color: '#e5e7eb', fontSize: 11 },
        axisPointer: { type: 'cross', lineStyle: { color: '#374151' } },
        formatter: (params) => {
          let html = `<div style="font-size:11px;margin-bottom:4px">${params[0].axisValue}</div>`
          params.forEach(p => {
            const val = typeof p.value === 'number' ? p.value.toFixed(2) : p.value
            html += `<div style="margin-top:2px"><span style="color:${p.color}">●</span> ${p.seriesName}: <strong>${val}x</strong></div>`
          })
          return html
        }
      },
      legend: {
        data: ['Weekly', 'Yearly', 'Holidays', 'Competitor', 'Viral'],
        textStyle: { color: '#9ca3af', fontSize: 11 },
        top: 0,
        itemGap: 15,
        selected: {
          'Weekly': true,
          'Yearly': true,
          'Holidays': true,
          'Competitor': true,
          'Viral': true
        },
        selectedMode: 'multiple',
        selector: false
      },
      xAxis: {
        type: 'category',
        data: dates,
        axisLine: { lineStyle: { color: '#374151' } },
        axisLabel: {
          color: '#9ca3af',
          fontSize: 9,
          rotate: 45,
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
        axisLabel: { color: '#9ca3af', fontSize: 9, formatter: (v) => `${Number(v).toFixed(1)}x` },
        splitLine: { lineStyle: { color: '#1f2937', type: 'dashed' } }
      },
      series: [
        { name: 'Weekly', type: 'line', data: weekly, smooth: true, lineStyle: { width: 2, color: '#3b82f6' }, itemStyle: { color: '#3b82f6' }, showSymbol: false, emphasis: { focus: 'series' } },
        { name: 'Yearly', type: 'line', data: yearly, smooth: true, lineStyle: { width: 2, color: '#a855f7' }, itemStyle: { color: '#a855f7' }, showSymbol: false, emphasis: { focus: 'series' } },
        { name: 'Holidays', type: 'line', data: holiday, step: 'end', lineStyle: { width: 2, color: '#ef4444' }, itemStyle: { color: '#ef4444' }, showSymbol: false, emphasis: { focus: 'series' } },
        { name: 'Competitor', type: 'line', data: competitor, smooth: true, lineStyle: { width: 2, color: '#22c55e' }, itemStyle: { color: '#22c55e' }, showSymbol: false, emphasis: { focus: 'series' } },
        { name: 'Viral', type: 'line', data: viral, smooth: true, lineStyle: { width: 2, color: '#f59e0b' }, itemStyle: { color: '#f59e0b' }, showSymbol: false, emphasis: { focus: 'series' } }
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
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
</style>
