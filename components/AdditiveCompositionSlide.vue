<template>
  <SlideLayout>
    <div class="slide-header">
      <h1>How the Components Add Together</h1>
      <p class="subtitle">Simple addition creates complex, realistic demand patterns</p>
    </div>

    <div class="slide-body">
      <div class="formula-section">
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
          <span class="operator">=</span>
          <span class="result">demand</span>
        </div>
      </div>

      <div class="cards-section">
        <NumberedCell number="1" title="Why Addition?" subtitle="Simple and interpretable">
          <ul>
            <li><strong>Intuitive</strong> - Each component adds its effect</li>
            <li><strong>Independent</strong> - Components don't interact</li>
            <li><strong>Interpretable</strong> - See each contribution</li>
          </ul>
        </NumberedCell>

        <NumberedCell number="2" title="The Result" subtitle="Complex from simple parts">
          <ul>
            <li><strong>Realistic</strong> - Matches real patterns</li>
            <li><strong>Predictable</strong> - Known ground truth</li>
            <li><strong>Testable</strong> - Can Prophet recover components?</li>
          </ul>
        </NumberedCell>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
import NumberedCell from '../components/NumberedCell.vue'
</script>

<style scoped>
.slide-header {
  flex-shrink: 0;
  margin-bottom: 1rem;
}

.slide-header h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.5rem;
}

.subtitle {
  font-size: 0.85rem;
  opacity: 0.9;
  margin: 0;
}

.slide-body {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}

.formula-section {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.formula {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;
}

.component {
  background: rgba(59, 130, 246, 0.2);
  padding: 0.4rem 0.8rem;
  border-radius: 0.5rem;
  font-weight: 600;
  color: #60a5fa;
}

.operator {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 300;
}

.result {
  background: rgba(168, 85, 247, 0.3);
  padding: 0.4rem 1rem;
  border-radius: 0.5rem;
  font-weight: 700;
  color: #a855f7;
}

.cards-section {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  overflow: hidden;
}
</style>
