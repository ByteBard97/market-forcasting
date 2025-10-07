// composables/useInverseSlidevTransform.ts
import { ref, onMounted, onUnmounted, readonly } from "vue";

export function useInverseSlidevTransform() {
  const inverseTransform = ref("");
  let observer: ResizeObserver | null = null;

  onMounted(() => {
    // Try multiple selectors for the slide container
    const slideContainer =
      document.getElementById("slide-container") ||
      document.querySelector(".slidev-slide-content") ||
      document.querySelector("#slideshow");

    if (!slideContainer) {
      console.error("Slidev slide container not found.");
      return;
    }

    const updateTransform = () => {
      const computedStyle = window.getComputedStyle(slideContainer);
      const transformValue = computedStyle.transform;

      if (transformValue && transformValue !== "none") {
        try {
          // Create a DOMMatrix from the computed style string
          const matrix = new DOMMatrix(transformValue);
          // Invert the matrix
          matrix.invertSelf();
          // Update the reactive ref with the CSS string representation
          inverseTransform.value = matrix.toString();
        } catch (e) {
          console.error("Failed to parse or invert transform matrix:", e);
          // Fallback: try to extract scale manually
          const match = transformValue.match(/matrix\(([\d.-]+)/);
          if (match) {
            const scale = parseFloat(match[1]);
            const inverseScale = 1 / scale;
            inverseTransform.value = `scale(${inverseScale})`;
          }
        }
      } else {
        inverseTransform.value = "";
      }
    };

    // Use ResizeObserver to update when container changes
    observer = new ResizeObserver(updateTransform);
    observer.observe(slideContainer);

    // Initial update
    updateTransform();

    // Also update on window resize
    window.addEventListener("resize", updateTransform);
  });

  onUnmounted(() => {
    if (observer) {
      observer.disconnect();
    }
    window.removeEventListener("resize", updateTransform);
  });

  return {
    inverseTransform: readonly(inverseTransform),
  };
}
