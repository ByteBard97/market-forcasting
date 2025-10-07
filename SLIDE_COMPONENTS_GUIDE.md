# Slide Components Guide
## Reusable Layouts & Patterns

---

## Available Reusable Components

### 1. **SlideLayout** - Base wrapper for all slides
**Path:** `/components/SlideLayout.vue`

**Usage:**
```vue
<SlideLayout>
  <!-- Your slide content here -->
</SlideLayout>
```

**Props:**
- `background`: String (optional) - Background type (documented but not actively used - user controls via BackgroundSelector)
- `noPadding`: Boolean - Remove default 2rem padding

**When to use:** Wrap EVERY slide with this

---

### 2. **TwoColumnSlide** - Text left, Plotly chart right
**Path:** `/components/TwoColumnSlide.vue`

**Usage:**
```vue
<TwoColumnSlide
  title="Optional Title"
  subtitle="Optional Subtitle"
  chart-id="unique-chart-id"
  :chart-data="chartDataFunction"
>
  <template #content>
    <!-- Left column content (text, lists, formulas) -->
  </template>
</TwoColumnSlide>
```

**Props:**
- `title`: String (optional) - H1 title above columns
- `subtitle`: String (optional) - Subtitle text
- `chartId`: String (required) - Unique ID for Plotly
- `chartData`: Function (required) - Returns `{ traces, layout, config, frames? }`

**When to use:** Component explanation slides (baseline, weekly, yearly, etc.)

**Example chartData function:**
```javascript
const chartDataFunction = () => {
  return {
    traces: [{
      x: dates,
      y: values,
      type: 'scatter',
      mode: 'lines',
      line: { color: '#60a5fa', width: 3 }
    }],
    layout: {
      margin: { l: 50, r: 20, t: 10, b: 35 },
      xaxis: { gridcolor: '#374151', title: 'Date' },
      yaxis: { gridcolor: '#374151', title: 'Value' },
      showlegend: false
    },
    config: {}
  }
}
```

---

## Common Slide Patterns

### Pattern A: Text-Only Slide (Conceptual)
**Used for:** Business challenge, data problem, explanations

```vue
<template>
  <SlideLayout>
    <h1>Slide Title</h1>
    <p class="subtitle">Subtitle text</p>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="text-xl font-bold mb-4 text-blue-400">Section 1</h3>
        <ul class="text-sm space-y-2">
          <li>✓ Point 1</li>
          <li>✓ Point 2</li>
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-bold mb-4 text-green-400">Section 2</h3>
        <ul class="text-sm space-y-2">
          <li>⚠ Point 1</li>
          <li>⚠ Point 2</li>
        </ul>
      </div>
    </div>

    <div class="mt-8 p-4 bg-blue-900 bg-opacity-20 rounded text-sm">
      <strong>Key takeaway</strong>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
```

---

### Pattern B: Component Explanation (Text + Chart)
**Used for:** Baseline, weekly, yearly, all synthetic data components

```vue
<template>
  <SlideLayout>
    <h1>Step N: Component Name</h1>
    <p class="subtitle">One-line description</p>

    <TwoColumnSlide
      chart-id="component-chart"
      :chart-data="componentChartData"
    >
      <template #content>
        <h3 class="text-lg font-bold mb-3">Component Details</h3>
        <div class="text-sm space-y-3">
          <!-- Formula -->
          <div class="bg-gray-800 p-3 rounded font-mono text-xs">
            formula here
          </div>

          <!-- Key points -->
          <ul class="space-y-2">
            <li>Point 1</li>
            <li>Point 2</li>
          </ul>

          <!-- Callout box -->
          <div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-xs">
            <strong>Why this matters:</strong><br />
            Explanation
          </div>
        </div>
      </template>
    </TwoColumnSlide>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
import TwoColumnSlide from '../components/TwoColumnSlide.vue'

const componentChartData = () => {
  // Generate data
  const dates = [/* ... */]
  const values = [/* ... */]

  return {
    traces: [{ x: dates, y: values, /* ... */ }],
    layout: { /* ... */ },
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
```

---

### Pattern C: Full-Width Chart/Visualization
**Used for:** Timeline, stacked components, model comparison

```vue
<template>
  <SlideLayout>
    <h1>Slide Title</h1>
    <p class="subtitle">Description</p>

    <div class="chart-container">
      <!-- ECharts, Plotly, or custom viz -->
      <div id="my-chart"></div>
    </div>
  </SlideLayout>
</template>

<script setup>
import { onMounted } from 'vue'
import SlideLayout from '../components/SlideLayout.vue'
// Import chart library

onMounted(() => {
  // Initialize chart
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 60vh;
  margin-top: 2rem;
}
</style>
```

---

### Pattern D: Video/Animation Slide
**Used for:** Convolution, Fourier, manim animations

```vue
<template>
  <SlideLayout>
    <h1>Animation Title</h1>
    <p class="subtitle">What you're about to see</p>

    <div class="video-container">
      <video
        :src="videoPath"
        autoplay
        loop
        muted
        playsinline
      ></video>
    </div>

    <div class="explanation">
      <p>Explanation of what the animation shows</p>
    </div>
  </SlideLayout>
</template>

<script setup>
import { computed } from 'vue'
import SlideLayout from '../components/SlideLayout.vue'

const base = computed(() => {
  const baseUrl = import.meta.env.BASE_URL || '/'
  return baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
})

const videoPath = computed(() => {
  return `${base.value}/videos/ConvolutionAnimation.webm`
})
</script>

<style scoped>
.video-container {
  width: 100%;
  max-width: 900px;
  margin: 2rem auto;
}

video {
  width: 100%;
  border-radius: 12px;
}

.explanation {
  text-align: center;
  max-width: 700px;
  margin: 0 auto;
  font-size: 0.95rem;
  opacity: 0.9;
}
</style>
```

---

## Styling Guidelines

### Colors
```css
/* Primary colors (already used) */
--blue: #60a5fa;      /* Demand lines, primary */
--orange: #f59e0b;    /* Seasonality */
--green: #10b981;     /* Predictions, success */
--red: #ef4444;       /* Stockouts, warnings */
--gray: #6b7280;      /* Baselines, neutral */
--yellow: #fbbf24;    /* Highlights, events */
--purple: #a855f7;    /* Marketing */
```

### Typography Classes
```css
/* Headings */
h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
h2 { font-size: 1.5rem; font-weight: 600; }
h3 { font-size: 1.25rem; font-weight: 600; }

/* Subtitle */
.subtitle { font-size: 1.1rem; opacity: 0.9; margin-bottom: 1rem; }

/* Text sizes */
.text-sm { font-size: 0.875rem; }
.text-xs { font-size: 0.75rem; }
```

### Common Utility Classes
```css
/* Spacing */
.mt-4 { margin-top: 1rem; }
.mt-8 { margin-top: 2rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }
.space-y-2 > * + * { margin-top: 0.5rem; }
.space-y-3 > * + * { margin-top: 0.75rem; }
.gap-8 { gap: 2rem; }

/* Layout */
.grid { display: grid; }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }

/* Backgrounds */
.bg-gray-800 { background-color: #1f2937; }
.bg-blue-900 { background-color: #1e3a8a; }
.bg-yellow-900 { background-color: #78350f; }
.bg-opacity-20 { opacity: 0.2; }

/* Borders */
.rounded { border-radius: 0.375rem; }

/* Fonts */
.font-mono { font-family: monospace; }
.font-bold { font-weight: 700; }
```

### Callout Boxes
```vue
<!-- Info box (blue) -->
<div class="mt-4 p-3 bg-blue-900 bg-opacity-20 rounded text-xs">
  <strong>Note:</strong> Explanation
</div>

<!-- Warning box (yellow) -->
<div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-xs">
  <strong>Why this matters:</strong> Explanation
</div>

<!-- Code box (gray) -->
<div class="bg-gray-800 p-3 rounded font-mono text-xs">
  formula or code
</div>
```

---

## Plotly Chart Defaults

### Standard Layout
```javascript
layout: {
  paper_bgcolor: 'rgba(0,0,0,0)',  // Transparent
  plot_bgcolor: 'rgba(0,0,0,0)',   // Transparent
  font: { color: '#e5e7eb', size: 10 },
  margin: { l: 50, r: 20, t: 10, b: 35 },
  xaxis: {
    gridcolor: '#374151',
    title: 'X Label'
  },
  yaxis: {
    gridcolor: '#374151',
    title: 'Y Label'
  },
  showlegend: false,
  autosize: true
}
```

### Standard Config
```javascript
config: {
  responsive: true,
  displayModeBar: false
}
```

### Common Trace Types
```javascript
// Line chart
{
  x: dates,
  y: values,
  type: 'scatter',
  mode: 'lines',
  line: { color: '#60a5fa', width: 3 },
  name: 'Series Name'
}

// Area chart
{
  x: dates,
  y: values,
  type: 'scatter',
  mode: 'lines',
  fill: 'tozeroy',
  fillcolor: 'rgba(96, 165, 250, 0.1)',
  line: { color: '#60a5fa', width: 2 }
}

// Bar chart
{
  x: categories,
  y: values,
  type: 'bar',
  marker: { color: '#60a5fa' }
}
```

---

## File Naming Convention

### Slides
- `TitleSlide.vue` - Opening slide
- `BusinessChallengeSlide.vue` - Conceptual slide
- `BaselineSlide.vue` - Component slide (uses TwoColumnSlide)
- `ComponentsStackSlide.vue` - Full-width viz slide
- `ProphetForecastSlide.vue` - Results slide

### Pattern
- Use PascalCase
- End with `Slide.vue`
- Be descriptive (avoid generic names like `Slide1.vue`)

---

## Import Statements

### Standard imports for most slides
```vue
<script setup>
import SlideLayout from '../components/SlideLayout.vue'
</script>
```

### For component explanation slides
```vue
<script setup>
import SlideLayout from '../components/SlideLayout.vue'
import TwoColumnSlide from '../components/TwoColumnSlide.vue'
</script>
```

### For interactive slides
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import SlideLayout from '../components/SlideLayout.vue'
import { gsap } from 'gsap'
</script>
```

---

## Don't Repeat Yourself (DRY)

### ❌ DON'T create custom layouts for each slide
```vue
<!-- BAD: Custom two-column layout -->
<div class="custom-grid">
  <div class="left-panel">...</div>
  <div class="right-panel">...</div>
</div>
```

### ✅ DO use TwoColumnSlide
```vue
<!-- GOOD: Reuse component -->
<TwoColumnSlide chart-id="my-chart" :chart-data="myData">
  <template #content>...</template>
</TwoColumnSlide>
```

### ❌ DON'T inline styles
```vue
<!-- BAD -->
<div style="margin-top: 2rem; padding: 1rem;">
```

### ✅ DO use utility classes or scoped styles
```vue
<!-- GOOD -->
<div class="mt-8 p-4">

<style scoped>
.my-component {
  margin-top: 2rem;
  padding: 1rem;
}
</style>
```

---

## Quick Reference: Which Pattern?

| Slide Type | Pattern | Example Slides |
|------------|---------|----------------|
| Concept explanation | Pattern A (Text-Only) | Business Challenge, Data Problem |
| Component demo | Pattern B (Text + Chart) | Baseline, Weekly, Yearly, all 13 components |
| Large visualization | Pattern C (Full-Width) | Timeline, Stacked Components, Model Comparison |
| Animation | Pattern D (Video) | Convolution, Fourier, Changepoints |
| Interactive | Custom (but similar to C) | Price Slider, Component Toggles |

---

## Next Steps

When creating new slides:
1. ✅ Copy the appropriate pattern from above
2. ✅ Update content (title, text, data)
3. ✅ Keep the structure intact
4. ✅ Test that it works
5. ✅ Add to slides.md

When you need something new:
1. ❓ Check if existing pattern can be adapted first
2. ❓ If truly unique, create a new reusable component in `/components/`
3. ❓ Document it in this guide
