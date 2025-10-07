<template>
  <div class="standalone-bg-container">
    <component
      v-if="currentBackground && backgroundComponent"
      :is="backgroundComponent"
      :key="currentBackground"
      class="standalone-bg"
    />
  </div>
</template>

<script>
// Use regular script block instead of setup to avoid Slidev transformation
import { computed } from "vue";
import { useSlideBackground } from "../composables/useSlideBackground";
import DataSphereBackground from "./DataSphereBackground.vue";
import MorphingDotsBackground from "./MorphingDotsBackground.vue";
import PerlinNoiseBackground from "./PerlinNoiseBackground.vue";
import SurfaceLinesBackground from "./SurfaceLinesBackground.vue";
import DistortedCubeBackground from "./DistortedCubeBackground.vue";
import TentacleBackground from "./TentacleBackground.vue";

export default {
  name: "StandaloneBackgroundManager",
  components: {
    DataSphereBackground,
    MorphingDotsBackground,
    PerlinNoiseBackground,
    SurfaceLinesBackground,
    DistortedCubeBackground,
    TentacleBackground,
  },
  setup() {
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
        case "none":
          return null;
        default:
          return DataSphereBackground;
      }
    });

    return {
      currentBackground,
      backgroundComponent,
    };
  },
};
</script>

<style scoped>
.standalone-bg-container {
  position: fixed;
  top: 0;
  left: 0;
  width: calc(100vw * 1.126126); /* Compensate for 0.888154 scale */
  height: calc(100vh * 1.126126);
  transform-origin: top left;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

.standalone-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
