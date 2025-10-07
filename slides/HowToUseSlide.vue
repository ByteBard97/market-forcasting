<template>
  <SlideLayout>
    <h1>How to Use Prophet for Your Business</h1>
    <p class="subtitle">Practical steps to start forecasting with your own data</p>

    <div class="steps-container">
      <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>Gather Your Data</h3>
          <p>You need at minimum:</p>
          <ul>
            <li>📅 <strong>Date</strong> - Daily sales dates</li>
            <li>📊 <strong>Sales volume</strong> - Pairs sold per day</li>
            <li>🎯 <strong>1+ year of history</strong> - More is better</li>
          </ul>
          <div class="example-box">
            <strong>Example CSV:</strong>
            <pre>date,pairs_sold
2023-01-01,45
2023-01-02,52
2023-01-03,48</pre>
          </div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>Install Prophet</h3>
          <p>Two options:</p>
          <div class="option">
            <strong>🐍 Python (recommended)</strong>
            <pre>pip install prophet pandas</pre>
          </div>
          <div class="option">
            <strong>📈 R</strong>
            <pre>install.packages('prophet')</pre>
          </div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>Run the Forecast</h3>
          <pre class="code-example">import pandas as pd
from prophet import Prophet

# Load your data
df = pd.read_csv('shoe_sales.csv')
df.columns = ['ds', 'y']  # Prophet needs these names

# Create and fit model
model = Prophet()
model.fit(df)

# Forecast next 90 days
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

# Plot results
model.plot(forecast)</pre>
        </div>
      </div>

      <div class="step-card">
        <div class="step-number">4</div>
        <div class="step-content">
          <h3>Use the Forecast</h3>
          <ul>
            <li>📦 <strong>Order inventory</strong> based on yhat (predicted demand)</li>
            <li>📊 <strong>Check uncertainty</strong> - look at yhat_lower and yhat_upper</li>
            <li>🔄 <strong>Update weekly</strong> - retrain as new data comes in</li>
            <li>⚠️ <strong>Trust but verify</strong> - compare predictions to actual sales</li>
          </ul>
          <div class="tip-box">
            💡 <strong>Pro tip:</strong> Add your promotions and drops as "holidays" in Prophet for better accuracy
          </div>
        </div>
      </div>
    </div>

    <div class="resources">
      <h3>Resources to Get Started</h3>
      <div class="resource-links">
        <div class="resource">📚 <a href="https://facebook.github.io/prophet/" target="_blank">Prophet Documentation</a></div>
        <div class="resource">🎓 <a href="https://facebook.github.io/prophet/docs/quick_start.html" target="_blank">Quick Start Guide</a></div>
        <div class="resource">💬 Ask me questions - I built this demo with Claude Code!</div>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
</script>

<style scoped>
.subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 1.5rem;
}

.steps-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.step-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.25rem;
  display: flex;
  gap: 1rem;
}

.step-number {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: #fff;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #fff;
}

.step-content p {
  font-size: 0.85rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.step-content ul {
  font-size: 0.8rem;
  opacity: 0.9;
  margin-left: 1rem;
  line-height: 1.6;
}

.example-box, .option, .tip-box {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  padding: 0.75rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
}

.example-box pre, .option pre, .code-example {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  padding: 0.5rem;
  font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
  font-size: 0.7rem;
  overflow-x: auto;
  margin-top: 0.25rem;
  line-height: 1.4;
}

.code-example {
  margin-top: 0.5rem;
  padding: 0.75rem;
}

.option {
  margin-bottom: 0.5rem;
}

.option strong {
  display: block;
  margin-bottom: 0.25rem;
}

.tip-box {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.resources {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.resources h3 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
}

.resource-links {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.resource {
  font-size: 0.85rem;
}

.resource a {
  color: #3b82f6;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.resource a:hover {
  border-bottom-color: #3b82f6;
}
</style>
