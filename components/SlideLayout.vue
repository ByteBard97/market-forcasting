<template>
  <div class="slide-container">
    <div class="slide-content" :class="{ 'no-padding': noPadding }">
      <slot />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  background: {
    type: String,
    default: 'sphere', // Note: background is now controlled by user via BackgroundSelector
    validator: (value) => [null, 'sphere', 'dots', 'datasphere', 'morphing', 'perlin', 'surfacelines', 'distortedcube', 'tentacle', 'vanta-waves', 'vanta-birds', 'vanta-net', 'vanta-clouds', 'vanta-fog', 'none'].includes(value)
  },
  noPadding: {
    type: Boolean,
    default: false
  }
})
// Background is now controlled globally by user via BackgroundSelector buttons
// The background prop is kept for documentation but not used
</script>

<style scoped>
.slide-container {
  position: relative;
  width: 100%;
  height: 100%;
  container-type: size; /* Enable cqh/cqw for all slide content */
}

.slide-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.slide-content {
  position: relative;
  z-index: 1;
  padding: 2rem 2rem 0rem 2rem; /* Bottom padding set to 0 */
  width: 100%;
  height: 100%;
  overflow: hidden; /* Prevent content from pushing south off screen */
  display: flex;
  flex-direction: column;
}

.slide-content.no-padding {
  padding: 0;
}
</style>
