<template>
  <div class="global-background-container">
    <component
      v-if="currentBackground && backgroundComponent"
      :is="backgroundComponent"
      :key="currentBackground"
      class="global-background"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useSlideBackground } from "../composables/useSlideBackground";
import DataSphereBackground from "./DataSphereBackground.vue";
import MorphingDotsBackground from "./MorphingDotsBackground.vue";
import PerlinNoiseBackground from "./PerlinNoiseBackground.vue";
import SurfaceLinesBackground from "./SurfaceLinesBackground.vue";
import DistortedCubeBackground from "./DistortedCubeBackground.vue";
import TentacleBackground from "./TentacleBackground.vue";
import VantaWavesBackground from "./VantaWavesBackground.vue";
import VantaBirdsBackground from "./VantaBirdsBackground.vue";
import VantaNetBackground from "./VantaNetBackground.vue";
import VantaCloudsBackground from "./VantaCloudsBackground.vue";
import VantaFogBackground from "./VantaFogBackground.vue";

const { currentBackground } = useSlideBackground();

const backgroundComponent = computed(() => {
  switch (currentBackground.value) {
    case "datasphere":
      return DataSphereBackground;
    case "morphing":
      return MorphingDotsBackground;
    case "perlin":
      return PerlinNoiseBackground;
    case "surfacelines":
      return SurfaceLinesBackground;
    case "distortedcube":
      return DistortedCubeBackground;
    case "tentacle":
      return TentacleBackground;
    case "vanta-waves":
      return VantaWavesBackground;
    case "vanta-birds":
      return VantaBirdsBackground;
    case "vanta-net":
      return VantaNetBackground;
    case "vanta-clouds":
      return VantaCloudsBackground;
    case "vanta-fog":
      return VantaFogBackground;
    case "none":
      return null;
    default:
      return DataSphereBackground;
  }
});
</script>

<style scoped>
.global-background-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

.global-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  min-width: 100vw;
  min-height: 100vh;
}
</style>
