<template>
  <div class="metric-cell" ref="cellEl" :class="`align-${align}`">
    <div class="single-line" ref="textEl">
      <span class="label">{{ line1 }}</span>
      <span class="value">{{ line2 }}</span>
      <span class="subtext">{{ line3 }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { autoTextSize } from 'auto-text-size'

const props = defineProps({
  line1: { type: String, required: true },
  line2: { type: String, required: true },
  line3: { type: String, required: true },
  align: {
    type: String,
    default: 'center',
    validator: (val) => ['left', 'center', 'right'].includes(val)
  }
})

const cellEl = ref(null)
const textEl = ref(null)
let cleanup = null

async function fitText() {
  if (!textEl.value || !cellEl.value) return

  await nextTick()

  // Set a much larger maxFontSize to allow upscaling
  // The library will automatically shrink to fit width constraints
  const maxSizeFromHeight = cellEl.value.clientHeight * 1.5

  // Clean up previous instance
  if (cleanup) cleanup()

  // Apply auto-text-size with correct parameters
  cleanup = autoTextSize({
    innerEl: textEl.value,
    containerEl: cellEl.value,
    mode: 'boxoneline',  // Single line that fills both width and height
    minFontSizePx: 8,
    maxFontSizePx: maxSizeFromHeight,
    fontSizePrecisionPx: 0.5
  })

  console.log(`auto-text-size applied for [${props.line1}]`)
}

onMounted(() => {
  fitText()
})

onUnmounted(() => {
  if (cleanup) cleanup()
})

// Re-fit when content changes
watch([() => props.line1, () => props.line2, () => props.line3], () => {
  fitText()
})
</script>

<style scoped>
.metric-cell {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.6rem 0.7rem;

  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap: 0.4rem;

  height: 100%;
  min-height: 0;
  overflow: hidden; /* Hide overflow while we calculate */
}

.single-line {
  white-space: nowrap;
  display: inline-block;
  width: 100%;
  line-height: 1.1;
}

.label {
  opacity: 0.7;
  font-weight: 400;
  font-size: 0.67em; /* 2/3 the size of the value */
}

.value {
  font-weight: 700;
  margin: 0 0.3em;
  font-size: 1em; /* Base size */
}

.subtext {
  opacity: 0.6;
  font-weight: 400;
  font-size: 0.67em; /* 2/3 the size of the value */
}

/* Alignment classes */
.align-left .single-line {
  text-align: left;
}

.align-center .single-line {
  text-align: center;
}

.align-right .single-line {
  text-align: right;
}
</style>
