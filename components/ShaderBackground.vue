<template>
  <canvas ref="canvasEl" class="shader-canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const canvasEl = ref(null);
let sandbox = null;

onMounted(async () => {
  if (canvasEl.value) {
    try {
      // Dynamically import GlslCanvas
      const GlslCanvas = (await import('glslCanvas')).default;

      // Fetch the shader code
      const response = await fetch('/shaders/background.frag');
      const fragmentShader = await response.text();

      // Initialize glslCanvas
      sandbox = new GlslCanvas(canvasEl.value);
      sandbox.load(fragmentShader);

      console.log('Shader loaded successfully');
    } catch (error) {
      console.error('Error loading shader:', error);
    }
  }
});

onUnmounted(() => {
  if (sandbox && sandbox.destroy) {
    sandbox.destroy();
  }
});
</script>

<style scoped>
.shader-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  display: block;
}
</style>
