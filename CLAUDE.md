# Claude Code Development Notes

## Critical Slidev Layout Constraints

### THE CARDINAL RULE: Slides Cannot Scroll
**Slidev slides have a FIXED viewport. Content CANNOT scroll south off-screen.**

This is the most common mistake when building slide components. HTML naturally flows downward and can scroll, but Slidev slides are presentation slides with fixed dimensions.

---

## How to Build Slide Components Correctly

### 1. SlideLayout Structure
`SlideLayout.vue` provides the base container with these critical properties:

```css
.slide-container {
  container-type: size;  /* Enables cqh/cqw units for children */
}

.slide-content {
  display: flex;
  flex-direction: column;
  overflow: hidden;  /* CRITICAL: Prevents south overflow */
  height: 100%;
}
```

### 2. The Correct Slide Content Pattern

Every slide should follow this structure:

```vue
<template>
  <SlideLayout>
    <!-- HEADER: Fixed size, never shrinks -->
    <div class="slide-header">
      <h1>Your Title</h1>
      <p class="subtitle">Your subtitle</p>
    </div>

    <!-- BODY: Takes remaining space, can use cqh/cqw -->
    <div class="slide-body">
      <!-- Your interactive content here -->
    </div>
  </SlideLayout>
</template>

<style scoped>
.slide-header {
  flex-shrink: 0;  /* Header keeps natural size */
  margin-bottom: 1rem;
}

.slide-body {
  flex: 1;  /* Takes all remaining vertical space */
  min-height: 0;  /* CRITICAL: Allows flex child to shrink below content size */
  container-type: size;  /* Enable cqh/cqw for nested children */
}
</style>
```

### 3. Understanding Container Query Units

**Container query units (cqh/cqw) work differently than viewport units (vh/vw):**

- `vh/vw` - Relative to the **viewport** (doesn't work properly in Slidev)
- `cqh/cqw` - Relative to the **nearest parent with `container-type: size`**

**Example:**
```css
.parent {
  container-type: size;  /* Must be set! */
  height: 100%;
}

.child {
  height: 80cqh;  /* 80% of .parent's height */
  width: 90cqw;   /* 90% of .parent's width */
}
```

**Key rules:**
1. The parent MUST have `container-type: size` (or `inline-size`)
2. `100cqh` = 100% of container height
3. `100cqw` = 100% of container width
4. These units cascade to the nearest container ancestor

---

## Common Anti-Patterns (DON'T DO THIS)

### ❌ Writing HTML that can scroll
```vue
<!-- BAD: Content will overflow -->
<SlideLayout>
  <div style="height: 800px">
    <!-- This will push content off screen -->
  </div>
</SlideLayout>
```

### ❌ Using vh/vw units
```css
/* BAD: Doesn't work in Slidev */
.content {
  height: 60vh;
}
```

### ❌ Not constraining flex children
```css
/* BAD: Content will overflow */
.slide-body {
  flex: 1;
  /* Missing min-height: 0 - content can expand beyond flex bounds */
}
```

### ❌ Forgetting container-type
```css
/* BAD: cqh/cqw won't work */
.parent {
  height: 100%;
  /* Missing container-type: size */
}

.child {
  height: 80cqh;  /* Will not work! */
}
```

---

## Correct Patterns (DO THIS)

### ✅ Use flex layout with proper constraints
```css
.slide-body {
  flex: 1;
  min-height: 0;  /* Critical! */
  overflow: hidden;  /* Prevents overflow */
  container-type: size;  /* Enables cqh/cqw */
}
```

### ✅ Use cqh/cqw for sizing
```css
.demo-container {
  height: 75cqh;  /* 75% of parent container height */
  width: 90cqw;   /* 90% of parent container width */
}
```

### ✅ Structure with fixed header + flexible body
```vue
<div class="slide-header">
  <!-- Fixed size header -->
</div>
<div class="slide-body">
  <!-- Flexible body that takes remaining space -->
</div>
```

---

## The Flex Layout Trinity

These three properties work together to prevent overflow:

```css
.container {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  flex-shrink: 0;  /* Never shrinks */
}

.body {
  flex: 1;          /* Takes remaining space */
  min-height: 0;    /* Can shrink below content size */
  overflow: hidden; /* Prevents overflow */
}
```

**Why `min-height: 0` is critical:**
- By default, flex items have `min-height: auto`
- This means they won't shrink below their content's natural size
- Setting `min-height: 0` allows the flex item to shrink, preventing overflow

---

## Debugging Overflow Issues

If content is overflowing:

1. **Check for container-type**: Does the parent have `container-type: size`?
2. **Check for min-height: 0**: Do flex children have this property?
3. **Check for overflow: hidden**: Is overflow prevention in place?
4. **Check for vh/vw units**: Replace with cqh/cqw
5. **Check for fixed heights**: Are you using absolute px heights that don't fit?

**Browser DevTools trick:**
```css
/* Temporarily add to see what's overflowing */
* {
  outline: 1px solid red;
}
```

---

## Example: Interactive Chart Slide

```vue
<template>
  <SlideLayout>
    <div class="slide-header">
      <h1>Chart Title</h1>
      <p class="subtitle">Chart description</p>
    </div>

    <div class="chart-container">
      <svg ref="chartSvg" viewBox="0 0 400 300">
        <!-- Chart content -->
      </svg>
    </div>
  </SlideLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const chartSvg = ref(null)

function scaleChart() {
  if (!chartSvg.value) return
  const container = chartSvg.value.parentElement

  const scaleX = container.clientWidth / 400
  const scaleY = container.clientHeight / 300
  const scale = Math.min(scaleX, scaleY)

  chartSvg.value.style.transform = `scale(${scale})`
}

onMounted(() => {
  setTimeout(scaleChart, 100)
  window.addEventListener('resize', scaleChart)
})
</script>

<style scoped>
.slide-header {
  flex-shrink: 0;
  margin-bottom: 1rem;
}

.chart-container {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

svg {
  width: 400px;
  height: 300px;
  transform-origin: center;
}
</style>
```

---

## The REAL Solution: Don't Fight the Web

After many failed attempts with transforms, container queries, and AutoFit components:

### The web defaults to scrolling. Presentations need fitting.

**The only reliable approaches:**

### 1. Make content naturally smaller (BEST)
- Use smaller font sizes
- Reduce padding/margins
- Use compact layouts
- Accept that slides have limited space

### 2. CSS `zoom` property (Chrome/Edge only)
```css
.slide-content {
  zoom: 0.8; /* Scales everything down, keeps text crisp */
}
```

### 3. Transform scaling (LAST RESORT - makes text fuzzy)
```css
.slide-content {
  transform: scale(0.8);
  transform-origin: top left;
}
```

### 4. What DOESN'T work:
- ❌ Container query units (cqh/cqw) - too finicky, parent must be set up perfectly
- ❌ AutoFit/AutoScale components - transform scaling makes text blurry
- ❌ Viewport units (vh/vw) - don't work in Slidev's nested iframes
- ❌ Trying to measure and scale dynamically - causes layout thrashing

## Summary

**Stop thinking in scrollable web pages. Start thinking in fixed presentation slides.**

The ONLY reliable solution: **Make your content naturally smaller using CSS sizing.**

Every piece of content must be:
1. Sized appropriately with rem/px units
2. Using flex layout with proper min-height
3. Protected by `overflow: hidden` (but this hides problems, doesn't solve them)
4. **Designed to fit** - not trying to auto-scale to fit

When in doubt, remember: **Slides are fixed viewports. Design content that fits, don't try to force-fit content.**
