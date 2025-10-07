<template>
  <div class="slidev-layout default">
    <AnimatedBackground :type="bgType" />
    <slot />
  </div>
</template>

<script setup>
import AnimatedBackground from '../components/AnimatedBackground.vue'

const props = defineProps({
  bgType: {
    type: String,
    default: 'gradient'
  }
})
</script>

<style scoped>
.slidev-layout {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
