<template>
  <div class="gradient-background"></div>
</template>

<script setup>
// Pure CSS - no JavaScript needed!
</script>

<style scoped>
.gradient-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(
    -45deg,
    #1a1a2e,
    #16213e,
    #0f3460,
    #533483
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
