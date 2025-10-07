<template>
  <div class="global-background-scale-wrapper">
    <GlobalBackgroundManager />
  </div>
  <BackgroundSelector />
</template>

<script setup>
import { onMounted } from "vue";
import GlobalBackgroundManager from "./components/GlobalBackgroundManager.vue";
import BackgroundSelector from "./components/BackgroundSelector.vue";

onMounted(() => {
  const wrapper = document.querySelector(".global-background-scale-wrapper");
  if (wrapper) {
    const scale = 0.888154;
    const inverseScale = 1 / scale;
    wrapper.style.transform = `scale(${inverseScale})`;
    wrapper.style.transformOrigin = "top left";
    console.log("Applied scale compensation:", inverseScale);
  }
});
</script>

<style>
.global-background-scale-wrapper {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: -1 !important;
  pointer-events: none !important;
  transform-origin: top left !important;
  /* Scale will be applied via JavaScript */
}

/* Ensure children don't interfere */
.global-background-scale-wrapper > * {
  pointer-events: none !important;
}

/* Except the selector which needs to be interactive */
.background-selector {
  pointer-events: auto !important;
}
</style>
