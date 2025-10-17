<script setup>
import { ref, onMounted } from "vue";
import { gsap } from "gsap";

// Refs
const svg = ref();
const kernel = ref();
const windowBox = ref();
const dot = ref();

onMounted(() => {
  const tl = gsap.timeline({ repeat: -1, defaults: { ease: "power2.inOut" } });

  // Slide kernel across
  tl.fromTo(kernel.value, { x: 50 }, { x: 700, duration: 6 });

  // Move highlight window with it
  tl.fromTo(windowBox.value, { x: 40 }, { x: 690, duration: 6 }, "<");

  // Move dot along bottom curve
  tl.fromTo(dot.value, { x: 50, y: 180 }, { x: 700, y: 180, duration: 6 }, "<");

  // Fade in labels
  tl.from(".label", { opacity: 0, y: 10, stagger: 0.3, duration: 0.6 }, 0.2);
});
</script>

<template>
  <svg ref="svg" viewBox="0 0 800 240" class="w-full h-auto">
    <!-- Signal -->
    <polyline
      points="0,120 50,120 100,80 200,80 200,120 800,120"
      stroke="#60a5fa"
      stroke-width="2"
      fill="none"
    />

    <!-- Output -->
    <path
      d="M0,180 C150,140 250,200 400,150 550,210 700,140 800,180"
      stroke="#a78bfa"
      stroke-width="2"
      fill="none"
      opacity="0.8"
    />

    <!-- Sliding window -->
    <rect
      ref="windowBox"
      x="40"
      y="50"
      width="100"
      height="80"
      fill="rgba(255,223,128,0.05)"
      stroke="#fbbf24"
      stroke-width="1.5"
    />

    <!-- Impulse kernel bars -->
    <g ref="kernel" transform="translate(50,50)">
      <rect
        v-for="i in 10"
        :key="i"
        :x="i * 8"
        :y="80 - Math.abs(Math.sin(i / 2)) * 60"
        width="6"
        :height="Math.abs(Math.sin(i / 2)) * 60 + 5"
        fill="#22c55e"
        opacity="0.8"
      />
    </g>

    <!-- Moving dot on output -->
    <circle
      ref="dot"
      cx="50"
      cy="180"
      r="5"
      fill="#a78bfa"
      stroke="white"
      stroke-width="1"
    />

    <!-- Labels -->
    <text x="20" y="30" class="label" fill="#22c55e" font-size="14">
      Impulse Kernel
    </text>
    <text x="20" y="105" class="label" fill="#60a5fa" font-size="14">
      Signal
    </text>
    <text x="20" y="205" class="label" fill="#a78bfa" font-size="14">
      Output
    </text>
  </svg>
</template>

<style scoped>
svg {
  overflow: visible;
}
</style>
