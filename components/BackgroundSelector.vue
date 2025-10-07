<template>
  <div
    class="background-selector"
    :class="{ visible: isVisible }"
    @mouseenter="handleMenuEnter"
    @mouseleave="handleMenuLeave"
  >
    <button
      v-for="bg in backgrounds"
      :key="bg.type"
      :class="{ active: currentBackground === bg.type }"
      @click="selectBackground(bg.type)"
      class="bg-btn"
    >
      {{ bg.label }}
      <span class="bg-desc">{{ bg.description }}</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useSlideBackground } from "../composables/useSlideBackground";

const { currentBackground, setBackground } = useSlideBackground();
const isVisible = ref(false);
let hideTimeout = null;
let showTimeout = null;
let mouseInBottomArea = false;
let mouseInMenu = false;
let visibleSince = null;

const handleMouseMove = (e) => {
  // Debug: log mouse position
  //console.log("Mouse moved:", e.clientX, e.clientY);

  // Find the slide container - try multiple selectors for Slidev
  const slideContainer =
    document.querySelector(".slidev-slide-content") ||
    document.querySelector(".slidev-layout") ||
    document.querySelector("#slide-content") ||
    document.querySelector(".slidev-page");

  if (!slideContainer) {
    console.log("ERROR: Could not find slide container");
    return;
  }

  const slideRect = slideContainer.getBoundingClientRect();

  // Log the slide dimensions once in a while
  if (Math.random() < 0.01) {
    // Log 1% of the time to avoid spam
    console.log("Slide bounds:", {
      top: slideRect.top,
      bottom: slideRect.bottom,
      left: slideRect.left,
      right: slideRect.right,
      height: slideRect.height,
      width: slideRect.width,
    });
  }

  // Check if mouse is within the slide bounds
  const mouseInSlide =
    e.clientX >= slideRect.left &&
    e.clientX <= slideRect.right &&
    e.clientY >= slideRect.top &&
    e.clientY <= slideRect.bottom;

  if (!mouseInSlide) {
    // Mouse is outside slide entirely
    if (mouseInBottomArea) {
      console.log("Mouse left slide area");
      mouseInBottomArea = false;
      if (showTimeout) clearTimeout(showTimeout);
      if (!mouseInMenu) {
        scheduleHide();
      }
    }
    return;
  }

  // Calculate if mouse is in the bottom 1/8 of the slide
  const slideHeight = slideRect.height;
  const bottomEighthStart = slideRect.bottom - slideHeight * 0.125;

  const inBottomEighth = e.clientY >= bottomEighthStart;

  // Log when we're close to the threshold
  const distanceFromThreshold = Math.abs(e.clientY - bottomEighthStart);
  if (distanceFromThreshold < 50) {
    console.log("Near threshold:", {
      mouseY: e.clientY,
      threshold: bottomEighthStart,
      inBottomEighth,
      slideBottom: slideRect.bottom,
      distance: distanceFromThreshold,
    });
  }

  if (inBottomEighth && !mouseInBottomArea) {
    // Just entered bottom 1/8
    console.log("ENTERED bottom 1/8 of slide!", {
      mouseY: e.clientY,
      threshold: bottomEighthStart,
      slideBottom: slideRect.bottom,
    });

    mouseInBottomArea = true;
    if (hideTimeout) clearTimeout(hideTimeout);

    showTimeout = setTimeout(() => {
      if (mouseInBottomArea) {
        console.log("SHOWING MENU - setting isVisible to true");
        isVisible.value = true;
        visibleSince = Date.now();

        // Verify it actually changed
        setTimeout(() => {
          console.log("Menu visibility check:", isVisible.value);
        }, 100);
      }
    }, 100);
  } else if (!inBottomEighth && mouseInBottomArea) {
    // Just left bottom 1/8
    console.log("LEFT bottom 1/8 of slide");
    mouseInBottomArea = false;
    if (showTimeout) clearTimeout(showTimeout);

    if (!mouseInMenu) {
      scheduleHide();
    }
  }
};

const scheduleHide = () => {
  if (hideTimeout) clearTimeout(hideTimeout);

  // Calculate how long the menu has been visible
  const visibleDuration = visibleSince ? Date.now() - visibleSince : 0;
  const minVisibleTime = 1000; // Minimum 1 second visible

  // If already visible for 1+ seconds, hide after 1 second
  // Otherwise, wait until we've been visible for at least 1 second total
  const delayBeforeHide = Math.max(1000, minVisibleTime - visibleDuration);

  hideTimeout = setTimeout(() => {
    if (!mouseInMenu && !mouseInBottomArea) {
      isVisible.value = false;
      visibleSince = null;
    }
  }, delayBeforeHide);
};

const handleMenuEnter = () => {
  mouseInMenu = true;
  if (hideTimeout) clearTimeout(hideTimeout);
  if (showTimeout) clearTimeout(showTimeout);
  if (!isVisible.value) {
    isVisible.value = true;
    visibleSince = Date.now();
  }
};

const handleMenuLeave = () => {
  mouseInMenu = false;
  // If mouse is not in bottom area either, schedule hide
  if (!mouseInBottomArea) {
    scheduleHide();
  }
};

onMounted(() => {
  console.log("BackgroundSelector mounted, adding mousemove listener");
  console.log("handleMouseMove type:", typeof handleMouseMove);
  console.log("handleMouseMove:", handleMouseMove);

  document.addEventListener("mousemove", handleMouseMove);

  console.log("Component is alive, window height:", window.innerHeight);
});

onUnmounted(() => {
  console.log("BackgroundSelector unmounted");
  document.removeEventListener("mousemove", handleMouseMove);
  if (hideTimeout) clearTimeout(hideTimeout);
  if (showTimeout) clearTimeout(showTimeout);
});

const backgrounds = [
  { type: "datasphere", label: "Data Sphere", description: "Connected dots" },
  { type: "morphing", label: "Morphing", description: "Morphing dots" },
  { type: "perlin", label: "Perlin Noise", description: "Morphing shape" },
  {
    type: "surfacelines",
    label: "Surface Lines",
    description: "Flowing lines",
  },
  {
    type: "distortedcube",
    label: "Distorted Cube",
    description: "Wireframe cube",
  },
  { type: "tentacle", label: "Tentacle", description: "Organic lines" },
  { type: "none", label: "None", description: "No background" },
];

function selectBackground(type) {
  setBackground(type);
}
</script>

<style scoped>
.background-selector {
  position: fixed;
  bottom: 0; /* Anchor to bottom of viewport */
  left: 50%;
  transform: translateX(-50%) translateY(100%); /* Hide below viewport */
  z-index: 10000;
  display: flex;
  gap: 4px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px 12px 0 0;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-bottom: none;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.5);
  pointer-events: auto;
}

.background-selector.visible {
  transform: translateX(-50%) translateY(0); /* Slide up into view */
}

.bg-btn {
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.bg-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.bg-btn.active {
  background: rgba(100, 150, 255, 0.4);
  border-color: rgba(100, 150, 255, 0.6);
}

.bg-desc {
  font-size: 7px;
  opacity: 0.6;
}
</style>
