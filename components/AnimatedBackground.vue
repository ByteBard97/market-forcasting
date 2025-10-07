<template>
  <component :is="backgroundComponent" />
</template>

<script setup>
import { computed } from 'vue'
import { useBackgroundStore } from '../composables/useBackgroundStore'
import ParticlesBackground from './ParticlesBackground.vue'
import ShaderBackground from './ShaderBackground.vue'
import RibbonsBackground from './RibbonsBackground.vue'
import WavesBackground from './WavesBackground.vue'
import OctogramsBackground from './OctogramsBackground.vue'

const props = defineProps({
  type: {
    type: String,
    default: null,
    validator: (value) => value === null || ['particles', 'shader', 'ribbons', 'waves', 'octograms', 'none'].includes(value)
  }
})

const { currentBackground } = useBackgroundStore()

const backgroundComponent = computed(() => {
  // If type prop is provided, use it; otherwise use global state
  const bgType = props.type || currentBackground.value

  switch (bgType) {
    case 'particles':
      return ParticlesBackground
    case 'shader':
      return ShaderBackground
    case 'ribbons':
      return RibbonsBackground
    case 'waves':
      return WavesBackground
    case 'octograms':
      return OctogramsBackground
    case 'none':
      return null
    default:
      return RibbonsBackground
  }
})
</script>
