# Slide Deck Structure

## Overview

The slide deck has been reorganized to separate concerns:
- **slides/** directory contains individual Vue components for each slide
- **components/** directory contains reusable chart/UI components
- **slides-new.md** is a clean markdown file that just instantiates slide components

## Architecture

### Base Layout: SlideLayout.vue

All slides use the `SlideLayout` component which provides:
- WebGL animated backgrounds (`sphere` or `dots`)
- Consistent slide container structure
- Z-index management for content over backgrounds

```vue
<SlideLayout background="sphere">
  <!-- Your slide content here -->
</SlideLayout>
```

### Individual Slide Components

Each slide lives in `slides/` directory:
- `TitleSlide.vue` - Opening slide with animated sphere background
- `SyntheticDataSlide.vue` - Explains synthetic data approach
- `BaselineSlide.vue` - Shows baseline growth trend
- `WeeklySeasonalitySlide.vue` - Weekly pattern explanation
- `TimelineSlide.vue` - Interactive 6-year demand timeline
- `ComponentsStackSlide.vue` - Shows all 13 components stacked
- `ModelComparisonSlide.vue` - Bar chart of model performance
- `FinalResultsSlide.vue` - Results table

### Reusable Components

Components in `components/` directory:
- `SlideLayout.vue` - Base layout with WebGL backgrounds
- `DataSphereBackground.vue` - 3D particle sphere animation
- `MorphingDotsBackground.vue` - Morphing dots animation
- `TwoColumnSlide.vue` - Two-column layout for charts
- `AnimatedTimeline.vue` - Timeline chart component
- `ComponentsStack.vue` - Stacked area chart
- `ModelBars.vue` - Bar chart for model comparison
- `ForecastCone.vue` - Forecast with confidence intervals
- `ModelPredictions.vue` - Model predictions chart

## Usage

### Development
```bash
# Run the new slide deck
npx slidev slides-new.md

# Or use the npm script (still uses old slides.md)
npm run dev
```

### Building
```bash
# Build for production
npx slidev build slides-new.md --base /market-forcasting/ --out docs
```

### Creating New Slides

1. Create a new Vue file in `slides/` directory:

```vue
<template>
  <SlideLayout background="sphere">
    <h1>My Slide Title</h1>
    <p>Slide content here...</p>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
// Import other components as needed
</script>

<style scoped>
/* Slide-specific styles */
</style>
```

2. Add it to `slides-new.md`:

```md
---

<MyNewSlide />

---
```

## Benefits

✅ **Clean separation** - HTML/logic in Vue, structure in markdown
✅ **Reusable backgrounds** - All slides use consistent WebGL animations
✅ **Better organization** - Each slide is a self-contained component
✅ **Easier maintenance** - No giant markdown file with embedded HTML
✅ **Type safety** - Full Vue 3 Composition API support
✅ **IDE support** - Better autocomplete and error checking

## Migration Status

- ✅ Created base SlideLayout with WebGL background support
- ✅ Extracted 8 key slides into Vue components
- ✅ Created slides-new.md with simplified structure
- ✅ Tested on localhost:3031
- ⏳ Remaining slides can be migrated incrementally
- ⏳ Update build scripts to use slides-new.md

## Next Steps

1. Migrate remaining slides from slides.md to individual components
2. Update package.json scripts to use slides-new.md by default
3. Test production build with new structure
4. Consider renaming slides-new.md to slides.md (backup old one first)
