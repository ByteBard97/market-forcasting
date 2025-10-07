<template>
  <SlideLayout background="dots">
    <h1>The Data Leakage Problem</h1>
    <p class="subtitle">The Mistake: ML models were "peeking at the future"</p>

    <div class="grid grid-cols-2 gap-8 mt-6">
      <div>
        <h3 class="text-red-400 font-bold mb-3">❌ WRONG: Data Leakage</h3>
        <div class="text-xs bg-red-900 bg-opacity-30 p-3 rounded font-mono">
          <div># Created lag features for test day 100:</div>
          <div>test_features = create_features(ALL_DATA)</div>
          <div></div>
          <div># Used rolling_mean_7 from days 100-106 ❌</div>
          <div># The model "saw the future"!</div>
          <div>predictions = model.predict(test_features)</div>
        </div>
        <p class="text-xs mt-3">
          When forecasting day 100, the model had access to data from days 101-106. This is
          <strong>impossible in production!</strong>
        </p>
      </div>
      <div>
        <h3 class="text-green-400 font-bold mb-3">✅ RIGHT: Walk-Forward</h3>
        <div class="text-xs bg-green-900 bg-opacity-30 p-3 rounded font-mono">
          <div># Walk-forward validation:</div>
          <div>for each_test_day:</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;# Only use past data</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;features = create_features(PAST_DATA_ONLY)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;prediction = model.predict(features)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;add_actual_to_history() # Realistic!</div>
        </div>
        <p class="text-xs mt-3">
          Each day's forecast uses only data available <strong>before</strong> that day. This mirrors
          production reality.
        </p>
      </div>
    </div>

    <div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-sm">
      <strong>Key Learning:</strong> Proper validation is critical for time series. Always use walk-forward!
    </div>
  </SlideLayout>
</template>

<script setup>
import SlideLayout from "../components/SlideLayout.vue";
</script>

<style scoped>
.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}
</style>
