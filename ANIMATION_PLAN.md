# Animation Implementation Plan
## Making the Executive Deck Truly Slick

---

## Priority System
- ★★★ = Must-have, maximum wow factor
- ★★ = High impact, very impressive
- ★ = Nice-to-have, polish

---

## Phase 1: Interactive "Wow" Elements (2-3 hours)

### 1. ★★★ Price Elasticity Slider (Slide 10)
**Tech:** Vue 3 + GSAP + ECharts

**Implementation:**
```vue
<template>
  <div class="price-elasticity">
    <div class="slider-container">
      <label>Price: ${{ price }}</label>
      <input
        type="range"
        v-model="price"
        min="140"
        max="210"
        @input="updateDemand"
      />
    </div>
    <div class="visualization">
      <EChart :option="chartOption" />
      <div class="formula">
        demand_multiplier = ({{ price }} / 180) ^ -1.2 = {{ multiplier.toFixed(2) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { gsap } from 'gsap'

const price = ref(180)
const multiplier = computed(() => Math.pow(price.value / 180, -1.2))

watch(multiplier, (newVal) => {
  // Animate the chart update with GSAP
  gsap.to(chartData, {
    duration: 0.5,
    value: newVal,
    ease: 'power2.out'
  })
})
</script>
```

**Visual Details:**
- Smooth slider with custom styling (gradient track)
- Demand bar animates height (GSAP)
- Elasticity curve shows current position (glowing dot)
- Formula updates in real-time with number animations

---

### 2. ★★★ Component Toggle Wall (Slide 18)
**Tech:** Vue 3 + ECharts + checkbox toggles

**Implementation:**
```vue
<template>
  <div class="component-wall">
    <div class="controls">
      <label v-for="component in components" :key="component.name">
        <input
          type="checkbox"
          v-model="component.enabled"
          @change="updateChart"
        />
        <span :style="{ color: component.color }">
          {{ component.name }}
        </span>
      </label>
    </div>
    <div class="chart">
      <EChart :option="stackedAreaOption" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const components = ref([
  { name: 'Baseline', enabled: true, color: '#666', data: [...] },
  { name: 'Weekly', enabled: true, color: '#3b82f6', data: [...] },
  { name: 'Yearly', enabled: true, color: '#f59e0b', data: [...] },
  { name: 'Holidays', enabled: true, color: '#ef4444', data: [...] },
  // ... 9 more components
])

const stackedAreaOption = computed(() => {
  const series = components.value
    .filter(c => c.enabled)
    .map(c => ({
      name: c.name,
      type: 'line',
      stack: 'total',
      areaStyle: {},
      data: c.data,
      itemStyle: { color: c.color }
    }))

  return { series, /* ... */ }
})
</script>
```

**Visual Details:**
- Checkboxes styled as toggle switches
- Smooth area transitions when toggling (ECharts animation)
- Hover highlights corresponding area
- "Final Demand" line on top (always visible)

---

### 3. ★★ Animated Timeline with Events (Slides 7-9)
**Tech:** Vue 3 + GSAP + ScrollTrigger

**Implementation:**
```vue
<template>
  <div class="timeline-container" ref="timelineRef">
    <svg class="timeline-svg">
      <!-- Demand line path -->
      <path ref="demandPath" :d="demandPathD" />

      <!-- Event markers -->
      <g v-for="event in events" :key="event.id">
        <circle
          :cx="event.x"
          :cy="event.y"
          :r="event.radius"
          :fill="event.color"
          @mouseenter="showTooltip(event)"
        />
        <text :x="event.x" :y="event.y - 20">{{ event.icon }}</text>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

const events = ref([
  { id: 1, date: '2019-11-29', type: 'holiday', icon: '🎄', name: 'Black Friday' },
  { id: 2, date: '2020-03-15', type: 'drop', icon: '👟', name: 'AJ1 Retro Chicago' },
  // ... more events
])

onMounted(() => {
  // Animate timeline scrolling
  gsap.to(timelineRef.value, {
    scrollTrigger: {
      trigger: timelineRef.value,
      start: 'top center',
      end: 'bottom center',
      scrub: 1
    },
    x: '-50%',
    ease: 'none'
  })

  // Animate events popping in
  events.value.forEach((event, i) => {
    gsap.from(`#event-${event.id}`, {
      scale: 0,
      opacity: 0,
      delay: i * 0.1,
      duration: 0.5,
      ease: 'back.out'
    })
  })
})
</script>
```

**Visual Details:**
- Timeline scrolls horizontally (smooth)
- Events pop in sequentially (staggered)
- Hover shows tooltip with details
- Demand line draws from left to right
- Icons bounce on appearance

---

## Phase 2: Manim Mathematical Beauty (3-4 hours)

### 4. ★★★ Fourier Series Build-up (Slide 21)
**Manim Script:**

```python
from manim import *

class FourierSeasonality(Scene):
    def construct(self):
        # Setup axes
        axes = Axes(
            x_range=[0, 365, 30],
            y_range=[-2, 2, 0.5],
            axis_config={"color": BLUE}
        )
        labels = axes.get_axis_labels(x_label="Days", y_label="Seasonality")

        # Air Jordan actual seasonality (target)
        target_data = [
            # Summer dip, back-to-school peak, holiday surge
            # ... realistic seasonal pattern
        ]
        target_curve = axes.plot_line_graph(
            x_values=range(365),
            y_values=target_data,
            line_color=YELLOW,
            stroke_width=3
        )
        target_label = Text("Target: Air Jordan Seasonality").next_to(axes, UP)

        # Show target briefly
        self.play(Create(axes), Write(labels), Write(target_label))
        self.play(Create(target_curve))
        self.wait(1)
        self.play(FadeOut(target_curve))

        # Build Fourier series
        harmonics = []
        sum_curve = None

        for n in range(1, 6):  # 5 harmonics
            # Create harmonic
            harmonic_func = lambda t: np.sin(2 * np.pi * n * t / 365)
            harmonic_curve = axes.plot(
                harmonic_func,
                color=interpolate_color(BLUE, RED, n/6)
            )
            harmonic_label = MathTex(f"+ \\sin(2\\pi \\cdot {n}t/365)").to_edge(RIGHT)

            # Show individual harmonic
            self.play(Create(harmonic_curve), Write(harmonic_label))
            self.wait(0.5)

            harmonics.append(harmonic_func)

            # Update sum
            if sum_curve:
                self.play(FadeOut(sum_curve))

            sum_func = lambda t: sum(h(t) for h in harmonics)
            sum_curve = axes.plot(sum_func, color=GREEN, stroke_width=4)

            self.play(
                FadeOut(harmonic_curve),
                FadeOut(harmonic_label),
                Create(sum_curve)
            )
            self.wait(0.5)

        # Show final approximation vs target
        self.play(FadeIn(target_curve))
        self.wait(2)

        # Highlight fit quality
        fit_label = Text("5 harmonics ≈ complex seasonality!", color=GREEN).to_edge(DOWN)
        self.play(Write(fit_label))
        self.wait(2)
```

**Render settings:**
- Transparent background (`-t` flag)
- High quality (`-qh`)
- WebM format (browser-friendly)
- 1920x1080 resolution

**Command:**
```bash
manim -qh -t --format webm fourier_seasonality.py FourierSeasonality
```

---

### 5. ★★ Multiplicative Composition (Slide 17)
**Manim Script:**

```python
class MultiplicativeComposition(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 100, 10], y_range=[0, 150, 25])

        # Start with baseline
        baseline = axes.plot(lambda t: 50 + 0.25*t, color=GRAY)
        baseline_label = Text("baseline_t = 50 + 0.25t").to_edge(UP)

        self.play(Create(axes), Create(baseline), Write(baseline_label))
        self.wait(1)

        # Multiply by weekly (×)
        weekly = axes.plot(
            lambda t: (50 + 0.25*t) * (1 + 0.2*np.sin(2*np.pi*t/7)),
            color=BLUE
        )
        multiply_symbol = MathTex("\\times").next_to(baseline_label, RIGHT)
        weekly_label = Text("weekly_t").next_to(multiply_symbol, RIGHT)

        self.play(
            Transform(baseline, weekly),
            Write(multiply_symbol),
            Write(weekly_label)
        )
        self.wait(1)

        # Continue with yearly, holidays, etc.
        # Each multiplication shows the curve evolving

        # ... 5-6 more components

        # Final complex demand curve
        final_label = Text("= complex demand!", color=GREEN).to_edge(DOWN)
        self.play(Write(final_label))
        self.wait(2)
```

---

### 6. ★ Changepoint Detection (Slide 22)
**Manim Script:**

```python
class ChangepointDetection(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 6, 1], y_range=[40, 80, 10])
        axes.add_coordinates()

        # Actual data (with trend changes)
        data_points = [
            (0, 50), (1, 52), (2, 54),  # Slow growth
            (2, 54), (3, 60), (4, 66),  # Accelerated growth (changepoint!)
            (4, 66), (5, 70), (6, 74)   # Moderate growth
        ]
        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=YELLOW)
            for x, y in data_points
        ])

        self.play(Create(axes), *[GrowFromCenter(dot) for dot in dots])
        self.wait(1)

        # Bad fit: single line
        single_line = axes.plot(lambda t: 50 + 4*t, color=RED)
        bad_label = Text("Single trend: poor fit", color=RED).to_edge(UP)

        self.play(Create(single_line), Write(bad_label))
        self.wait(1)
        self.play(FadeOut(single_line), FadeOut(bad_label))

        # Good fit: piecewise with changepoint
        changepoint_x = 2
        changepoint_line = DashedLine(
            axes.c2p(changepoint_x, 40),
            axes.c2p(changepoint_x, 80),
            color=GREEN
        )
        changepoint_label = Text("Changepoint detected!", color=GREEN).next_to(changepoint_line, UP)

        line1 = axes.plot(lambda t: 50 + 2*t, x_range=[0, 2], color=BLUE)
        line2 = axes.plot(lambda t: 48 + 6*t, x_range=[2, 4], color=BLUE)
        line3 = axes.plot(lambda t: 58 + 4*t, x_range=[4, 6], color=BLUE)

        self.play(
            Create(line1),
            Create(line2),
            Create(line3),
            Create(changepoint_line),
            Write(changepoint_label)
        )
        self.wait(2)
```

---

## Phase 3: Polish & Transitions (2-3 hours)

### 7. ★★ Model Comparison Bar Race (Slide 25)
**Tech:** ECharts + custom animation

```javascript
// Bar race animation
const models = [
  { name: 'Naive', mae: 35.12 },
  { name: 'Linear', mae: 34.89 },
  { name: 'LightGBM', mae: 33.67 },
  { name: 'XGBoost', mae: 32.19 },
  { name: 'Seasonal Naive', mae: 31.84 },
  { name: 'ARIMA', mae: 29.45 },
  { name: 'Prophet', mae: 27.76 }
]

// Animate bars growing in sequence
let delay = 0
models.forEach((model, i) => {
  setTimeout(() => {
    // Add model to chart with animation
    chart.setOption({
      series: [{
        data: models.slice(0, i+1),
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }]
    })

    // Highlight Prophet (winner)
    if (model.name === 'Prophet') {
      setTimeout(() => {
        // Flash gold, confetti, winner effect
        triggerWinnerAnimation()
      }, 500)
    }
  }, delay)
  delay += 800
})
```

---

### 8. ★ Smooth Chart Morphing (Multiple slides)
**Tech:** D3.js transitions

```javascript
// Morph from line chart to area chart
const transition = d3.transition()
  .duration(1000)
  .ease(d3.easeCubicInOut)

d3.select('.chart-path')
  .transition(transition)
  .attr('d', newPathData)
  .attr('fill', 'url(#gradient)')  // Add area fill
```

---

### 9. ★ Background Particle Flow (Global)
**Tech:** Three.js particle system

```javascript
// Create particle system that reacts to slide content
const particles = new THREE.Points(geometry, material)

// Animate particles based on slide theme
function updateParticles(slideTheme) {
  switch(slideTheme) {
    case 'seasonal':
      // Particles flow in circular pattern
      animateCircular()
      break
    case 'trend':
      // Particles flow upward
      animateUpward()
      break
    case 'forecast':
      // Particles scatter forward
      animateForward()
      break
  }
}
```

---

## Animation Rendering Plan

### Manim Animations to Create:
1. **fourier_seasonality.py** → `videos/FourierSeasonality.webm`
2. **multiplicative_composition.py** → `videos/MultiplicativeComposition.webm`
3. **changepoint_detection.py** → `videos/ChangepointDetection.webm`

### Rendering Commands:
```bash
# High quality, transparent, WebM format
manim -qh -t --format webm animations.py FourierSeasonality
manim -qh -t --format webm animations.py MultiplicativeComposition
manim -qh -t --format webm animations.py ChangepointDetection
```

---

## Implementation Checklist

### Phase 1: Interactive Elements
- [ ] Price elasticity slider component
- [ ] Component toggle wall component
- [ ] Animated timeline component
- [ ] Test interactivity on mobile

### Phase 2: Manim Animations
- [ ] Write Fourier series script
- [ ] Write multiplicative composition script
- [ ] Write changepoint script
- [ ] Render all at high quality
- [ ] Add to `/videos/` directory

### Phase 3: Polish
- [ ] Model comparison bar race
- [ ] Smooth chart transitions
- [ ] Background particle system
- [ ] Video playback controls (play/pause/replay)
- [ ] Loading states for heavy animations

### Testing
- [ ] Test on Chrome (primary)
- [ ] Test on Safari (exec might use Mac)
- [ ] Test on mobile (iPad view)
- [ ] Performance check (60fps target)
- [ ] Accessibility (keyboard controls)

---

## Performance Targets

- **Page load:** < 2 seconds
- **Animation FPS:** 60fps (smooth)
- **Interactive response:** < 100ms
- **Video load:** Progressive (stream, don't block)
- **Bundle size:** < 5MB (code split by slide)

---

## Visual Style Guide

### Colors
- **Primary:** #3b82f6 (blue - demand line)
- **Secondary:** #f59e0b (orange - seasonality)
- **Accent:** #10b981 (green - predictions)
- **Warning:** #ef4444 (red - stockouts, errors)
- **Neutral:** #6b7280 (gray - baselines)

### Typography
- **Headings:** Poppins 600
- **Body:** Barlow 400/500
- **Code:** SF Mono

### Animation Easing
- **Entry:** `cubic-bezier(0.34, 1.56, 0.64, 1)` (back.out)
- **Exit:** `cubic-bezier(0.55, 0.055, 0.675, 0.19)` (cubic.in)
- **Morph:** `cubic-bezier(0.65, 0, 0.35, 1)` (cubic.inOut)

---

## Success Metrics

After presenting to landlord:
- ✅ He asks "How did you make that?" (technical interest)
- ✅ He interacts with slider/toggles (engagement)
- ✅ He mentions showing it to colleagues (viral potential)
- ✅ He understands Fourier/convolution (educational success)
- ✅ No performance issues (smooth throughout)
