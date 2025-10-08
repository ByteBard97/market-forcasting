<template>
  <SlideLayout>
    <div class="slide-header">
      <h1>How to Use Prophet for Your Business</h1>
      <p class="subtitle">Practical steps to start forecasting with your own data</p>
    </div>

    <div class="slide-body">
      <NumberedCell number="1" title="Gather Your Data">
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
      </NumberedCell>

      <NumberedCell number="2" title="Install Prophet">
        <p>Two options:</p>
        <div class="option">
          <strong>🐍 Python (recommended)</strong>
          <pre>pip install prophet pandas</pre>
        </div>
        <div class="option">
          <strong>📈 R</strong>
          <pre>install.packages('prophet')</pre>
        </div>
      </NumberedCell>

      <NumberedCell number="3" title="Run the Forecast">
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
      </NumberedCell>

      <NumberedCell number="4" title="Use the Forecast">
        <ul>
          <li>📦 <strong>Order inventory</strong> based on yhat (predicted demand)</li>
          <li>📊 <strong>Check uncertainty</strong> - look at yhat_lower and yhat_upper</li>
          <li>🔄 <strong>Update weekly</strong> - retrain as new data comes in</li>
          <li>⚠️ <strong>Trust but verify</strong> - compare predictions to actual sales</li>
        </ul>
        <div class="tip-box">
          💡 <strong>Pro tip:</strong> Add your promotions and drops as "holidays" in Prophet for better accuracy
        </div>
      </NumberedCell>
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from '../components/SlideLayout.vue'
import NumberedCell from '../components/NumberedCell.vue'
</script>

<style scoped>
.slide-header {
  flex: 0 0 auto;
  margin-bottom: 1rem;
}

.slide-header h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.5rem;
  line-height: 1.2;
}

.subtitle {
  font-size: 0.85rem;
  opacity: 0.9;
  margin: 0;
  line-height: 1.2;
}

.slide-body {
  flex: 1 1 0;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1rem;
  overflow: hidden;
}

/* Style content inside NumberedCell slots - use larger base sizes that will zoom down */
.slide-body :deep(p) {
  margin: 0 0 0.75rem 0;
  font-size: 0.95rem;
  line-height: 1.4;
}

.slide-body :deep(ul) {
  margin: 0;
  padding-left: 1.25rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.slide-body :deep(li) {
  margin-bottom: 0.4rem;
}

.slide-body :deep(.example-box),
.slide-body :deep(.option),
.slide-body :deep(.tip-box) {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.375rem;
  padding: 0.625rem;
  margin-top: 0.625rem;
  font-size: 0.875rem;
}

.slide-body :deep(.example-box pre),
.slide-body :deep(.option pre),
.slide-body :deep(.code-example) {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 0.375rem;
  padding: 0.5rem;
  font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
  font-size: 0.8rem;
  overflow-x: auto;
  overflow-y: auto;
  margin-top: 0.375rem;
  line-height: 1.4;
  max-height: 100%;
}

.slide-body :deep(.code-example) {
  margin: 0;
  padding: 0.625rem;
}

.slide-body :deep(.option) {
  margin-bottom: 0.5rem;
}

.slide-body :deep(.option strong) {
  display: block;
  margin-bottom: 0.375rem;
}

.slide-body :deep(.tip-box) {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}
</style>
