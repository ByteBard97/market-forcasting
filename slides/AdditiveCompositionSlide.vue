<template>
  <SlideLayout>
    <h1>How the Components Add Together</h1>
    <p class="subtitle">Simple addition creates complex, realistic demand patterns</p>

    <div class="formula-box">
      <div class="formula">
        <span class="component">baseline</span>
        <span class="operator">+</span>
        <span class="component">weekly</span>
        <span class="operator">+</span>
        <span class="component">yearly</span>
        <span class="operator">+</span>
        <span class="component">holidays</span>
        <span class="operator">+</span>
        <span class="component">drops</span>
        <span class="operator">+</span>
        <span class="component">marketing</span>
        <span class="operator">+</span>
        <span class="component">...</span>
        <span class="operator">=</span>
        <span class="result">final demand</span>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-8 mt-8">
      <div>
        <h3 class="text-xl font-bold mb-4 text-blue-400">Why Addition?</h3>
        <ul class="text-sm space-y-2">
          <li>✓ <strong>Intuitive</strong> - Each component adds its effect</li>
          <li>✓ <strong>Independent</strong> - Components don't interact</li>
          <li>✓ <strong>Interpretable</strong> - Can see each contribution</li>
          <li>✓ <strong>Simple math</strong> - Easy to understand & explain</li>
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-bold mb-4 text-purple-400">The Result</h3>
        <ul class="text-sm space-y-2">
          <li>📈 <strong>Realistic</strong> - Matches real shoe demand patterns</li>
          <li>🎯 <strong>Predictable</strong> - Known ground truth for testing</li>
          <li>🔬 <strong>Testable</strong> - Can Prophet recover the components?</li>
          <li>📊 <strong>Complex</strong> - Simple parts → sophisticated whole</li>
        </ul>
      </div>
    </div>

    <div class="mt-8 p-4 bg-purple-900 bg-opacity-20 rounded text-center">
      <strong>Next:</strong> See how all components stack together visually
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.formula-box {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
}

.formula {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
}

.component {
  background: rgba(59, 130, 246, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  color: #60a5fa;
}

.operator {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 300;
}

.result {
  background: rgba(168, 85, 247, 0.3);
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  color: #a855f7;
  font-size: 1.2rem;
}
</style>
