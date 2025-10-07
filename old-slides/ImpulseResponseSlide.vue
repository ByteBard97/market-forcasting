<template>
  <SlideLayout>
    <h1>Step 4: Impulse Responses</h1>
    <p class="subtitle">The key to realistic causality</p>

    <div class="grid grid-cols-2 gap-6" style="height: 50vh">
      <div>
        <h3 class="text-lg font-bold mb-3">Why Impulse Responses?</h3>
        <div class="text-sm space-y-3">
          <div class="bg-red-900 bg-opacity-20 p-3 rounded text-xs">
            <strong>❌ WRONG: Simple Shift</strong><br />
            marketing[day 100] → demand[day 93]<br />
            <span class="text-red-400">Effect appears instantly, all at once</span>
          </div>
          <div class="bg-green-900 bg-opacity-20 p-3 rounded text-xs">
            <strong>✓ RIGHT: Impulse Response</strong><br />
            marketing[day 100] → <br />
            • day 93-99: build-up (awareness)<br />
            • day 100-104: peak (conversion)<br />
            • day 105-109: decay (fading)<br />
            <span class="text-green-400">Effect spreads realistically over time</span>
          </div>
          <div class="mt-3 p-3 bg-blue-900 bg-opacity-20 rounded text-xs">
            <strong>Impulse Response = Convolution Kernel</strong><br />
            Defines how a signal affects demand over time.<br />
            Like a transfer function in control systems.
          </div>
        </div>
      </div>
      <div class="glass-background flex items-center justify-center p-4">
        <video
          :src="`${base}/videos/ConvolutionAnimation.webm`"
          autoplay
          loop
          muted
          playsinline
          class="w-full h-full object-contain"
        ></video>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import { computed } from "vue";
import SlideLayout from "../components/SlideLayout.vue";

const base = computed(() => {
  const baseUrl = import.meta.env.BASE_URL || "/";
  return baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
});
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}

.glass-background {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(3px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
