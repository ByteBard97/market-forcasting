<template>
  <div ref="container" class="chart-container">
    <svg
      v-if="dimensions.width > 0"
      :viewBox="`0 0 ${dimensions.width} ${dimensions.height}`"
      preserveAspectRatio="xMidYMid meet"
      class="chart-svg"
    >
      <!-- Grid -->
      <g class="grid">
        <line
          v-for="i in 5"
          :key="'h-' + i"
          :x1="margins.left"
          :y1="margins.top + i * gridStep.y"
          :x2="dimensions.width - margins.right"
          :y2="margins.top + i * gridStep.y"
          stroke="rgba(255,255,255,0.1)"
          stroke-dasharray="2,2"
        />
        <line
          v-for="i in 6"
          :key="'v-' + i"
          :x1="margins.left + i * gridStep.x"
          :y1="margins.top"
          :x2="margins.left + i * gridStep.x"
          :y2="dimensions.height - margins.bottom"
          stroke="rgba(255,255,255,0.2)"
          stroke-dasharray="4,4"
        />
      </g>

      <!-- Axes -->
      <line
        :x1="margins.left"
        :y1="dimensions.height - margins.bottom"
        :x2="dimensions.width - margins.right"
        :y2="dimensions.height - margins.bottom"
        stroke="#e5e7eb"
        stroke-width="2"
      />
      <line
        :x1="margins.left"
        :y1="margins.top"
        :x2="margins.left"
        :y2="dimensions.height - margins.bottom"
        stroke="#e5e7eb"
        stroke-width="2"
      />

      <!-- Axis labels -->
      <text
        :x="margins.left + plotWidth / 2"
        :y="dimensions.height - margins.bottom / 3"
        fill="#9ca3af"
        text-anchor="middle"
        :font-size="fontSize"
        class="axis-label"
      >
        Price →
      </text>
      <text
        :x="margins.left / 3"
        :y="margins.top + plotHeight / 2"
        fill="#9ca3af"
        text-anchor="middle"
        :font-size="fontSize"
        class="axis-label"
        :transform="`rotate(-90 ${margins.left / 3} ${margins.top + plotHeight / 2})`"
      >
        ← Demand
      </text>

      <!-- Curve + fill -->
      <path :d="curvePath" fill="url(#gradient)" opacity="0.15" />
      <path :d="curvePath" fill="none" stroke="#60a5fa" stroke-width="2.5" />

      <!-- Current point with spring physics - draggable -->
      <g
        class="current-point-group"
        @mousedown="startDrag"
        @touchstart="startDrag"
      >
        <circle
          :cx="displayPoint.x"
          :cy="displayPoint.y"
          :r="dotRadius"
          fill="#10b981"
          stroke="#fff"
          stroke-width="2"
          class="current-point"
          :class="{ dragging: isDragging }"
        />
        <text
          :x="displayPoint.x"
          :y="displayPoint.y - dotRadius * 2"
          fill="#10b981"
          text-anchor="middle"
          :font-size="labelFontSize"
          font-weight="bold"
          class="point-label"
        >
          ${{ currentPrice }}
        </text>
      </g>

      <defs>
        <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3" />
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
        </linearGradient>
      </defs>
    </svg>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  currentPrice: {
    type: Number,
    required: true
  },
  msrp: {
    type: Number,
    default: 180
  },
  elasticity: {
    type: Number,
    default: -1.2
  },
  priceMin: {
    type: Number,
    default: 140
  },
  priceMax: {
    type: Number,
    default: 210
  }
});

const container = ref(null);
const dimensions = ref({ width: 0, height: 0 });

// Margins as percentages of dimensions
const margins = computed(() => ({
  left: dimensions.value.width * 0.12,
  right: dimensions.value.width * 0.05,
  top: dimensions.value.height * 0.12,
  bottom: dimensions.value.height * 0.08
}));

const plotWidth = computed(() =>
  dimensions.value.width - margins.value.left - margins.value.right
);

const plotHeight = computed(() =>
  dimensions.value.height - margins.value.top - margins.value.bottom
);

const gridStep = computed(() => ({
  x: plotWidth.value / 6,
  y: plotHeight.value / 5
}));

// Responsive font sizes based on dimensions
const fontSize = computed(() => Math.max(10, Math.min(16, dimensions.value.width / 30)));
const labelFontSize = computed(() => Math.max(12, Math.min(18, dimensions.value.width / 25)));
const dotRadius = computed(() => Math.max(6, Math.min(10, dimensions.value.width / 50)));

// Calculate demand for a given price
const demandAtPrice = (price) => Math.pow(price / props.msrp, props.elasticity);

// Convert price to x coordinate
const priceToX = (price) => {
  const t = (price - props.priceMin) / (props.priceMax - props.priceMin);
  return margins.value.left + t * plotWidth.value;
};

// Convert demand multiplier to y coordinate
const demandToY = (demandMultiplier) => {
  // Calculate min/max demand based on price range
  const minDemand = demandAtPrice(props.priceMax); // Higher price = lower demand
  const maxDemand = demandAtPrice(props.priceMin); // Lower price = higher demand

  const t = (demandMultiplier - minDemand) / (maxDemand - minDemand);
  return margins.value.top + plotHeight.value * (1 - t);
};

// Generate the curve path
const curvePath = computed(() => {
  if (dimensions.value.width === 0) return '';

  const numPoints = 50;
  const step = (props.priceMax - props.priceMin) / (numPoints - 1);

  const points = [];
  for (let i = 0; i < numPoints; i++) {
    const price = props.priceMin + i * step;
    const demand = demandAtPrice(price);
    const x = priceToX(price);
    const y = demandToY(demand);
    points.push(`${x},${y}`);
  }

  // Create filled path: start at bottom-left, draw curve, end at bottom-right, close
  const bottomY = dimensions.value.height - margins.value.bottom;
  const leftX = priceToX(props.priceMin);
  const rightX = priceToX(props.priceMax);

  return `M${leftX},${bottomY} L${points.join(' L')} L${rightX},${bottomY} Z`;
});

// Current point position (target)
const currentPoint = computed(() => ({
  x: priceToX(props.currentPrice),
  y: demandToY(demandAtPrice(props.currentPrice))
}));

// Physics simulation for the point
const springPoint = ref({ x: 0, y: 0 });
const velocity = ref({ x: 0, y: 0 });
const lastUpdateTime = ref(0);

// Dragging state
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });
const dragPosition = ref({ x: 0, y: 0 });

// Physics constants (F=MA style)
const MASS = 1.0;                 // Mass of the point
const SPRING_K = 0.3;             // Spring constant (stiffness)
const DAMPING_COEFFICIENT = 0.92; // Friction/damping (0-1, higher = less friction)
const VELOCITY_THRESHOLD = 0.01;  // When to stop animating
const SLIDER_VELOCITY_GAIN = 0.25; // How much slider motion affects the point

let animationFrameId = null;

const updateSpring = (timestamp) => {
  const target = currentPoint.value; // Anchor point on the curve
  const current = springPoint.value;
  const vel = velocity.value;

  // Calculate time delta (in seconds)
  const dt = lastUpdateTime.value ? Math.min((timestamp - lastUpdateTime.value) / 1000, 0.05) : 0.016;
  lastUpdateTime.value = timestamp;

  // If dragging, update position directly
  if (isDragging.value) {
    current.x = dragPosition.value.x;
    current.y = dragPosition.value.y;
    // Keep velocity at zero while dragging so it doesn't accumulate
    vel.x = 0;
    vel.y = 0;
    animationFrameId = requestAnimationFrame(updateSpring);
    return;
  }

  // Spring force: F = -k * x (Hooke's law) in 2D
  // The spring pulls toward the anchor point (currentPoint)
  const dx = target.x - current.x;
  const dy = target.y - current.y;
  const springForceX = SPRING_K * dx;
  const springForceY = SPRING_K * dy;

  // Damping force: F = -c * v
  const dampingForceX = -vel.x * (1 - DAMPING_COEFFICIENT);
  const dampingForceY = -vel.y * (1 - DAMPING_COEFFICIENT);

  // Total force
  const totalForceX = springForceX + dampingForceX;
  const totalForceY = springForceY + dampingForceY;

  // F = MA, so A = F/M
  const accelerationX = totalForceX / MASS;
  const accelerationY = totalForceY / MASS;

  // Update velocity: v = v + a*dt
  vel.x += accelerationX * dt * 60;
  vel.y += accelerationY * dt * 60;

  // Update position: x = x + v*dt
  current.x += vel.x * dt * 60;
  current.y += vel.y * dt * 60;

  // Check if we should keep animating
  const speed = Math.sqrt(vel.x * vel.x + vel.y * vel.y);
  const distance = Math.sqrt(dx * dx + dy * dy);

  if (speed > VELOCITY_THRESHOLD || distance > 0.5) {
    animationFrameId = requestAnimationFrame(updateSpring);
  } else {
    // Snap to target when close enough
    current.x = target.x;
    current.y = target.y;
    vel.x = 0;
    vel.y = 0;
    animationFrameId = null; // Clear frame ID when stopped
  }
};

// Display point is either drag position or spring position
const displayPoint = computed(() => {
  if (isDragging.value) {
    return dragPosition.value;
  }
  return springPoint.value;
});

// Drag handlers
const startDrag = (event) => {
  event.preventDefault();
  isDragging.value = true;

  const svg = container.value.querySelector('svg');
  const pt = svg.createSVGPoint();

  const clientX = event.clientX || event.touches?.[0]?.clientX;
  const clientY = event.clientY || event.touches?.[0]?.clientY;

  pt.x = clientX;
  pt.y = clientY;
  const svgP = pt.matrixTransform(svg.getScreenCTM().inverse());

  dragOffset.value = {
    x: svgP.x - springPoint.value.x,
    y: svgP.y - springPoint.value.y
  };

  dragPosition.value = { ...springPoint.value };

  // Add global event listeners
  window.addEventListener('mousemove', handleDrag);
  window.addEventListener('mouseup', endDrag);
  window.addEventListener('touchmove', handleDrag);
  window.addEventListener('touchend', endDrag);

  // Start animation loop if not already running
  if (!animationFrameId) {
    animationFrameId = requestAnimationFrame(updateSpring);
  }
};

const handleDrag = (event) => {
  if (!isDragging.value) return;

  const svg = container.value.querySelector('svg');
  const pt = svg.createSVGPoint();

  const clientX = event.clientX || event.touches?.[0]?.clientX;
  const clientY = event.clientY || event.touches?.[0]?.clientY;

  pt.x = clientX;
  pt.y = clientY;
  const svgP = pt.matrixTransform(svg.getScreenCTM().inverse());

  dragPosition.value = {
    x: svgP.x - dragOffset.value.x,
    y: svgP.y - dragOffset.value.y
  };
};

const endDrag = () => {
  if (!isDragging.value) return;

  isDragging.value = false;

  // Calculate velocity based on drag release
  const dx = dragPosition.value.x - springPoint.value.x;
  const dy = dragPosition.value.y - springPoint.value.y;

  // Impart some velocity based on displacement
  velocity.value.x += dx * 0.1;
  velocity.value.y += dy * 0.1;

  // Update spring position to drag position
  springPoint.value = { ...dragPosition.value };

  // Remove global event listeners
  window.removeEventListener('mousemove', handleDrag);
  window.removeEventListener('mouseup', endDrag);
  window.removeEventListener('touchmove', handleDrag);
  window.removeEventListener('touchend', endDrag);

  // Continue animation
  if (!animationFrameId) {
    animationFrameId = requestAnimationFrame(updateSpring);
  }
};

// Watch for target anchor point changes
watch(currentPoint, (target) => {
  // If this is the first update, just snap to position
  if (springPoint.value.x === 0 && springPoint.value.y === 0) {
    springPoint.value = { ...target };
    return;
  }

  // When slider moves, the anchor point moves
  // The spring will naturally pull the point to the new anchor
  // Start animation if not running
  if (!animationFrameId) {
    animationFrameId = requestAnimationFrame(updateSpring);
  }
}, { immediate: true });

// Resize observer
let resizeObserver;

const updateDimensions = () => {
  if (container.value) {
    const rect = container.value.getBoundingClientRect();
    dimensions.value = {
      width: rect.width,
      height: rect.height
    };
  }
};

onMounted(() => {
  updateDimensions();

  resizeObserver = new ResizeObserver(() => {
    updateDimensions();
  });

  if (container.value) {
    resizeObserver.observe(container.value);
  }
});

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 0;
  position: relative;
}

.chart-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.3));
}

.chart-svg text {
  font-family: inherit;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.axis-label {
  font-family: inherit;
  letter-spacing: 0.05em;
}

.point-label {
  font-family: inherit;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.5);
}

.current-point {
  filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.5));
  cursor: grab;
  transition: filter 0.2s;
}

.current-point.dragging {
  cursor: grabbing;
  filter: drop-shadow(0 0 12px rgba(16, 185, 129, 0.8));
}

.current-point-group {
  cursor: grab;
}

.current-point-group:active {
  cursor: grabbing;
}
</style>
