<template>
  <component :is="backgroundComponent" />
</template>

<script setup>
import { computed } from 'vue'
import { useBackgroundStore } from '../composables/useBackgroundStore'
import DataSphereBackground from './DataSphereBackground.vue'
import MorphingDotsBackground from './MorphingDotsBackground.vue'
import PerlinNoiseBackground from './PerlinNoiseBackground.vue'
import SurfaceLinesBackground from './SurfaceLinesBackground.vue'
import DistortedCubeBackground from './DistortedCubeBackground.vue'
import TentacleBackground from './TentacleBackground.vue'
import VantaWavesBackground from './VantaWavesBackground.vue'
import VantaBirdsBackground from './VantaBirdsBackground.vue'
import VantaNetBackground from './VantaNetBackground.vue'
import VantaCloudsBackground from './VantaCloudsBackground.vue'
import VantaFogBackground from './VantaFogBackground.vue'

const props = defineProps({
  type: {
    type: String,
    default: null,
    validator: (value) => value === null || ['datasphere', 'morphing', 'perlin', 'surfacelines', 'distortedcube', 'tentacle', 'vanta-waves', 'vanta-birds', 'vanta-net', 'vanta-clouds', 'vanta-fog', 'none'].includes(value)
  }
})

const { currentBackground } = useBackgroundStore()

const backgroundComponent = computed(() => {
  // If type prop is provided, use it; otherwise use global state
  const bgType = props.type || currentBackground.value

  switch (bgType) {
    case 'datasphere':
      return DataSphereBackground
    case 'morphing':
      return MorphingDotsBackground
    case 'perlin':
      return PerlinNoiseBackground
    case 'surfacelines':
      return SurfaceLinesBackground
    case 'distortedcube':
      return DistortedCubeBackground
    case 'tentacle':
      return TentacleBackground
    case 'vanta-waves':
      return VantaWavesBackground
    case 'vanta-birds':
      return VantaBirdsBackground
    case 'vanta-net':
      return VantaNetBackground
    case 'vanta-clouds':
      return VantaCloudsBackground
    case 'vanta-fog':
      return VantaFogBackground
    case 'none':
      return null
    default:
      return DataSphereBackground
  }
})
</script>
