<template>
  <SlideLayout background="sphere" no-padding>
    <div class="title-card">
      <h1 class="main-title">Forecasting Air Jordan Demand</h1>
      <p class="subtitle">
        A Journey Through Modern Time Series Prediction
      </p>
      <div class="pt-6">
        <span
          @click="$slidev.nav.next"
          class="px-2 py-1 rounded cursor-pointer"
          hover="bg-white bg-opacity-10"
          style="color: white"
        >
          Press Space for next page <carbon:arrow-right class="inline" />
        </span>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap");

.title-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 100;
  padding: 2.5rem 3rem;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.6);
  width: 600px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.main-title {
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
  font-size: 1.875rem !important;
  margin-bottom: 1rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.15 !important;
  max-width: 100%;
  background: linear-gradient(
    135deg,
    #ffffff 0%,
    #ffc9e0 20%,
    #ff85c0 40%,
    #e05a9d 60%,
    #c43d7f 80%,
    #a82060 100%
  );
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 4s ease-in-out infinite;
}

@keyframes shimmer {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.subtitle {
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
  font-size: 0.85rem;
  opacity: 0.85;
  margin-bottom: 1.5rem;
  color: #d1d5db;
  font-weight: 300;
  letter-spacing: 0.02em;
  line-height: 1.5;
  max-width: 90%;
}
</style>
