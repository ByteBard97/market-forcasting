<template>
  <div ref="cellContainer" class="numbered-cell">
    <div ref="cellInner" class="cell-inner">
      <div class="cell-header">
        <div class="number-circle">{{ number }}</div>
        <div class="title-area">
          <div class="cell-title">{{ title }}</div>
          <div v-if="subtitle" class="cell-subtitle">{{ subtitle }}</div>
        </div>
      </div>
      <div class="cell-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

defineProps({
  number: {
    type: [Number, String],
    required: true
  },
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
});

const cellContainer = ref(null);
const cellInner = ref(null);

let resizeObserver = null;

const fitContent = () => {
  if (!cellContainer.value || !cellInner.value) return;

  // Reset zoom first
  cellInner.value.style.zoom = '1';

  // Wait for layout to settle
  requestAnimationFrame(() => {
    const containerHeight = cellContainer.value.clientHeight;
    const contentHeight = cellInner.value.scrollHeight;

    if (contentHeight > containerHeight) {
      // Calculate zoom to fit with small buffer
      const zoom = Math.max(0.4, (containerHeight / contentHeight) * 0.95);
      cellInner.value.style.zoom = zoom;
    }
  });
};

onMounted(() => {
  // Initial fit
  setTimeout(fitContent, 100);

  // Watch for resize
  resizeObserver = new ResizeObserver(() => {
    fitContent();
  });

  if (cellContainer.value) {
    resizeObserver.observe(cellContainer.value);
  }
});

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>

<style scoped>
.numbered-cell {
  height: 100%;
  min-height: 0;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 0.75rem;
  overflow: hidden;
  position: relative;
}

.cell-inner {
  display: flex;
  flex-direction: column;
  width: 100%;
  transform-origin: top left;
}

.cell-header {
  flex-shrink: 0;
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.number-circle {
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
  color: white;
}

.title-area {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.cell-title {
  font-weight: 600;
  font-size: 0.85rem;
  line-height: 1.2;
  color: rgba(255, 255, 255, 0.95);
}

.cell-subtitle {
  font-size: 0.7rem;
  line-height: 1.2;
  color: rgba(255, 255, 255, 0.6);
}

.cell-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  font-size: 0.75rem;
  line-height: 1.3;
  color: rgba(255, 255, 255, 0.8);
}

/* Deep selector to style slotted content */
.cell-content :deep(ul) {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.cell-content :deep(li) {
  margin: 0;
}

.cell-content :deep(strong) {
  color: rgba(255, 255, 255, 0.95);
}
</style>
