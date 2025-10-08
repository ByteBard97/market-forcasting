<template>
  <div class="metric-cell" :class="`align-${align}`">
    <div class="single-line">
      <span class="label">{{ line1 }}</span>
      <span class="value">{{ line2 }}</span>
      <span class="subtext">{{ line3 }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  line1: { type: String, required: true },
  line2: { type: String, required: true },
  line3: { type: String, required: true },
  align: {
    type: String,
    default: 'center',
    validator: (val) => ['left', 'center', 'right'].includes(val)
  }
})
</script>

<style scoped>
.metric-cell {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.6rem 0.7rem;

  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap: 0.4rem;

  height: 100%;
  min-height: 0;
  overflow: hidden; /* Hide overflow while we calculate */
}

.single-line {
  white-space: nowrap;
  overflow: hidden;
  line-height: 1.1;
  font-size: 4cqh; /* Scale based on container height */
}

.label {
  opacity: 0.7;
  font-weight: 400;
}

.value {
  font-weight: 700;
  margin: 0 0.3em;
}

.subtext {
  opacity: 0.6;
  font-weight: 400;
}

/* Alignment classes */
.align-left .single-line {
  text-align: left;
}

.align-center .single-line {
  text-align: center;
}

.align-right .single-line {
  text-align: right;
}
</style>
