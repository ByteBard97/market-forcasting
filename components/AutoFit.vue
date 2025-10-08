<template>
  <!-- The outer box defines the available space -->
  <div
    class="af-box"
    :style="{
      padding: typeof padding === 'number' ? padding + 'px' : padding,
    }"
    ref="boxEl"
  >
    <!-- Visible scaled content -->
    <div class="af-content" ref="contentEl" :style="contentStyle">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount,
  watch,
  nextTick,
} from "vue";

type Mode = "contain" | "cover";

const props = withDefaults(
  defineProps<{
    /** Only shrink, never upscale (recommended for slides) */
    shrinkOnly?: boolean;
    /** Allow upscaling up to this factor if shrinkOnly=false */
    maxScale?: number;
    /** Minimum scale; prevents over-shrinking tiny fragments */
    minScale?: number;
    /** contain = fit inside; cover = fill and crop (rarely used for text) */
    mode?: Mode;
    /** Optional padding inside the fit box, e.g., '12px' */
    padding?: string | number;
    /** Debounce ms for ResizeObserver */
    debounce?: number;
  }>(),
  {
    shrinkOnly: true,
    maxScale: 1.25,
    minScale: 0.5,
    mode: "contain",
    padding: "0px",
    debounce: 16,
  }
);

const boxEl = ref<HTMLElement | null>(null);
const contentEl = ref<HTMLElement | null>(null);
const scale = ref(1);

const contentStyle = computed(() => ({
  transform: `scale(${scale.value})`,
  transformOrigin: "top left",
}));

let ro: ResizeObserver | null = null;
let mo: MutationObserver | null = null;
let rafId: number | null = null;
let tId: number | null = null;

function scheduleMeasure() {
  if (rafId) cancelAnimationFrame(rafId);
  rafId = requestAnimationFrame(measure);
}

function measure() {
  if (!boxEl.value || !contentEl.value) return;

  // Temporarily remove transform to get natural size
  const oldTransform = contentEl.value.style.transform;
  contentEl.value.style.transform = 'none';

  const box = boxEl.value.getBoundingClientRect();
  const nat = contentEl.value.getBoundingClientRect();

  // Restore transform
  contentEl.value.style.transform = oldTransform;

  // natural content size (unscaled)
  const natW = nat.width || 1;
  const natH = nat.height || 1;

  // available size inside the box
  const availW = box.width || 1;
  const availH = box.height || 1;

  let s: number;
  if (props.mode === "cover") {
    s = Math.max(availW / natW, availH / natH);
  } else {
    // contain
    s = Math.min(availW / natW, availH / natH);
  }

  if (props.shrinkOnly) s = Math.min(1, s);
  s = Math.max(props.minScale, Math.min(s, props.maxScale));

  scale.value = s;
}

onMounted(async () => {
  await nextTick();

  const debounced = () => {
    if (tId) clearTimeout(tId);
    tId = window.setTimeout(scheduleMeasure, props.debounce);
  };

  ro = new ResizeObserver(debounced);
  if (boxEl.value) ro.observe(boxEl.value);
  if (contentEl.value) ro.observe(contentEl.value);

  // If slot content changes (text numbers, etc.), re-measure
  mo = new MutationObserver(debounced);
  if (contentEl.value)
    mo.observe(contentEl.value, {
      childList: true,
      subtree: true,
      characterData: true,
    });

  scheduleMeasure();
});

onBeforeUnmount(() => {
  if (ro) ro.disconnect();
  if (mo) mo.disconnect();
  if (rafId) cancelAnimationFrame(rafId);
  if (tId) clearTimeout(tId);
});
</script>

<style scoped>
.af-box {
  width: 100%;
  height: 100%;
  overflow: hidden; /* never show scrollbars */
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  position: relative;
}

/* The actually visible content; scaled via transform */
.af-content {
  transform-origin: top left;
  width: fit-content;
  height: fit-content;
}
</style>
