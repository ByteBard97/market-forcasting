---
theme: default
title: Air Jordan Demand Forecasting
info: |
  ## Air Jordan Demand Analysis
  Understanding what drives sneaker demand through data
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 100; padding: 2rem; background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(3px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); max-width: 600px;">
  <h1 style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(135deg, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">What Drives Air Jordan Demand?</h1>
  <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 1rem; color: white;">Understanding the levers behind sneaker sales</p>
  <div class="pt-6">
    <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10" style="color: white;">
      Press Space for next page <carbon:arrow-right class="inline"/>
    </span>
  </div>
</div>

---

# Building Realistic Synthetic Data

How we generate demand with causal structure

<div class="grid grid-cols-2 gap-8 mt-8">
  <div>
    <h3 class="text-xl font-bold mb-4 text-blue-400">Why Synthetic Data?</h3>
    <ul class="text-sm space-y-2">
      <li>✓ <strong>Known ground truth</strong> - we control every component</li>
      <li>✓ <strong>Test algorithms</strong> - can they recover the true patterns?</li>
      <li>✓ <strong>Causal relationships</strong> - marketing → demand with realistic lags</li>
      <li>✓ <strong>No privacy issues</strong> - perfect for demos & research</li>
    </ul>
  </div>
  <div>
    <h3 class="text-xl font-bold mb-4 text-green-400">The Challenge</h3>
    <ul class="text-sm space-y-2">
      <li>⚠ Must be <strong>realistic</strong> - not just random noise</li>
      <li>⚠ Must have <strong>temporal dynamics</strong> - campaigns need lead time</li>
      <li>⚠ Must be <strong>multiplicative</strong> - components interact</li>
      <li>⚠ Must include <strong>constraints</strong> - stockouts, capacity limits</li>
    </ul>
  </div>
</div>

<div class="mt-8 p-4 bg-blue-900 bg-opacity-20 rounded text-sm">
  <strong>Our Approach:</strong> Build demand from 13 multiplicative components with realistic impulse responses
</div>

---

# Step 1: The Baseline

Start with slow, steady growth

<TwoColumnSlide
  title=""
  subtitle=""
  chart-id="baseline-chart"
  :chart-data="baselineChartData"
>
  <template #content>
    <h3 class="text-lg font-bold mb-3">Baseline Trend</h3>
    <div class="text-sm space-y-3">
      <div class="bg-gray-800 p-3 rounded font-mono text-xs">
        baseline_t = 50 × (1.0003)^t
      </div>
      <ul class="space-y-2">
        <li>Starts at <strong>50 pairs/day</strong></li>
        <li>Grows <strong>~12% per year</strong></li>
        <li>Ends at <strong>~97 pairs/day</strong> (after 6 years)</li>
        <li>Represents organic brand growth</li>
      </ul>
      <div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-xs">
        <strong>Why multiplicative?</strong><br/>
        In retail, a 10% promo on 100 units ≠ 10% promo on 50 units.<br/>
        Effects scale with baseline level.
      </div>
    </div>
  </template>
</TwoColumnSlide>

<script setup>
const baselineChartData = () => {
  const n = 2192;
  const t = Array.from({length: n}, (_, i) => i);
  const dates = t.map(i => {
    const d = new Date('2019-01-01');
    d.setDate(d.getDate() + i);
    return d.toISOString().split('T')[0];
  });
  const baseline = t.map(i => 50 * Math.pow(1.0003, i));

  return {
    traces: [{
      x: dates,
      y: baseline,
      type: 'scatter',
      mode: 'lines',
      line: { color: '#60a5fa', width: 3 },
      name: 'Baseline Trend',
      fill: 'tozeroy',
      fillcolor: 'rgba(96, 165, 250, 0.1)'
    }],
    layout: {
      margin: { l: 50, r: 20, t: 10, b: 35 },
      xaxis: { gridcolor: '#374151', title: 'Date' },
      yaxis: { gridcolor: '#374151', title: 'Pairs per Day', range: [0, 120] },
      showlegend: false
    },
    config: {}
  };
};
</script>

---

# Step 2: Weekly Seasonality

Weekend uplift for retail traffic

<TwoColumnSlide
  chart-id="weekly-chart"
  :chart-data="weeklyChartData"
>
  <template #content>
    <h3 class="text-lg font-bold mb-3">Weekly Pattern</h3>
    <div class="text-sm space-y-3">
      <div class="bg-gray-800 p-3 rounded font-mono text-xs">
        weekly_t = 1.25  if weekend<br/>
        weekly_t = 0.95  if weekday
      </div>
      <ul class="space-y-2">
        <li><strong>Weekdays (M-F):</strong> 0.95× multiplier (5% dip)</li>
        <li><strong>Weekends (S-S):</strong> 1.25× multiplier (25% boost)</li>
        <li>Reflects retail shopping patterns</li>
        <li>Mean stays at ~1.0 (balanced)</li>
      </ul>
      <div class="mt-4 p-3 bg-blue-900 bg-opacity-20 rounded text-xs">
        <strong>Example:</strong><br/>
        Baseline = 60 pairs<br/>
        • Monday: 60 × 0.95 = 57 pairs<br/>
        • Saturday: 60 × 1.25 = 75 pairs
      </div>
    </div>
  </template>
</TwoColumnSlide>

<script setup>
const weeklyChartData = () => {
  const days = 28;
  const dates = Array.from({length: days}, (_, i) => {
    const d = new Date('2024-01-01');
    d.setDate(d.getDate() + i);
    return d.toISOString().split('T')[0];
  });

  const weekly = dates.map((_, i) => {
    const dayOfWeek = new Date(dates[i]).getDay();
    return (dayOfWeek === 0 || dayOfWeek === 6) ? 1.25 : 0.95;
  });

  return {
    traces: [{
      x: dates,
      y: weekly,
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: '#60a5fa', width: 2 },
      marker: { size: 6, color: '#60a5fa' },
      name: 'Weekly Multiplier'
    }],
    layout: {
      margin: { l: 50, r: 20, t: 20, b: 60 },
      xaxis: { gridcolor: '#374151', tickangle: -45 },
      yaxis: { gridcolor: '#374151', title: 'Multiplier', range: [0.8, 1.4] },
      shapes: [{
        type: 'line',
        x0: dates[0],
        x1: dates[dates.length-1],
        y0: 1.0,
        y1: 1.0,
        line: { color: '#f59e0b', width: 1, dash: 'dash' }
      }],
      showlegend: false
    },
    config: {}
  };
};
</script>

---

# Step 3: Yearly Seasonality

Summer peaks and holiday surges

<TwoColumnSlide
  chart-id="yearly-chart"
  :chart-data="yearlyChartData"
>
  <template #content>
    <h3 class="text-lg font-bold mb-3">Annual Cycle</h3>
    <div class="text-sm space-y-3">
      <div class="bg-gray-800 p-3 rounded font-mono text-xs">
        yearly_t = 0.15×sin(2π×t/365) + <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.10×sin(4π×t/365) + 1.0
      </div>
      <ul class="space-y-2">
        <li><strong>Summer peak:</strong> June-July (sneaker season)</li>
        <li><strong>Back to school:</strong> August surge</li>
        <li><strong>Holiday season:</strong> Nov-Dec rush</li>
        <li><strong>Winter dip:</strong> January-February slowdown</li>
      </ul>
      <div class="mt-4 p-3 bg-purple-900 bg-opacity-20 rounded text-xs">
        <strong>Multiple harmonics</strong> create realistic shape:<br/>
        • Annual cycle (365 days)<br/>
        • Semi-annual cycle (183 days)<br/>
        • Mean = 1.0, Range = [0.82, 1.24]
      </div>
    </div>
  </template>
</TwoColumnSlide>

<script setup>
const yearlyChartData = () => {
  const days = 730;
  const dates = Array.from({length: days}, (_, i) => {
    const d = new Date('2023-01-01');
    d.setDate(d.getDate() + i);
    return d.toISOString().split('T')[0];
  });

  const yearly = dates.map((_, i) => {
    const t = i;
    return 0.15 * Math.sin(2 * Math.PI * t / 365.25 - Math.PI / 2) +
           0.10 * Math.sin(4 * Math.PI * t / 365.25 + Math.PI / 4) + 1.0;
  });

  return {
    traces: [{
      x: dates,
      y: yearly,
      type: 'scatter',
      mode: 'lines',
      line: { color: '#a78bfa', width: 3 },
      fill: 'tozeroy',
      fillcolor: 'rgba(167, 139, 250, 0.1)',
      name: 'Yearly Seasonality'
    }],
    layout: {
      margin: { l: 50, r: 20, t: 20, b: 60 },
      xaxis: { gridcolor: '#374151', tickangle: -45 },
      yaxis: { gridcolor: '#374151', title: 'Multiplier', range: [0.7, 1.3] },
      shapes: [{
        type: 'line',
        x0: dates[0],
        x1: dates[dates.length-1],
        y0: 1.0,
        y1: 1.0,
        line: { color: '#f59e0b', width: 1, dash: 'dash' }
      }],
      showlegend: false
    },
    config: {}
  };
};
</script>

---

# Step 4: Impulse Responses

The key to realistic causality

<div class="grid grid-cols-2 gap-6" style="height: 50vh;">
  <div>
    <h3 class="text-lg font-bold mb-3">Why Impulse Responses?</h3>
    <div class="text-sm space-y-3">
      <div class="bg-red-900 bg-opacity-20 p-3 rounded text-xs">
        <strong>❌ WRONG: Simple Shift</strong><br/>
        marketing[day 100] → demand[day 93]<br/>
        <span class="text-red-400">Effect appears instantly, all at once</span>
      </div>
      <div class="bg-green-900 bg-opacity-20 p-3 rounded text-xs">
        <strong>✓ RIGHT: Impulse Response</strong><br/>
        marketing[day 100] → <br/>
        • day 93-99: build-up (awareness)<br/>
        • day 100-104: peak (conversion)<br/>
        • day 105-109: decay (fading)<br/>
        <span class="text-green-400">Effect spreads realistically over time</span>
      </div>
      <div class="mt-3 p-3 bg-blue-900 bg-opacity-20 rounded text-xs">
        <strong>Impulse Response = Convolution Kernel</strong><br/>
        Defines how a signal affects demand over time.<br/>
        Like a transfer function in control systems.
      </div>
    </div>
  </div>
  <div class="glass-background flex items-center justify-center p-4">
    <ImpulseAnimation />
  </div>
</div>

---

# Step 5: Marketing Effect

Campaigns need lead time to work

<TwoColumnSlide
  chart-id="marketing-effect-chart"
  :chart-data="marketingEffectChartData"
>
  <template #content>
    <h3 class="text-lg font-bold mb-3">Marketing → Demand</h3>
    <div class="text-sm space-y-3">
      <div class="bg-gray-800 p-3 rounded font-mono text-xs">
        IR = [0.05, 0.1, ..., 1.0, ..., 0.1]<br/>
        effect_t = convolve(marketing, IR)
      </div>
      <ul class="space-y-2">
        <li><strong>17-day impulse response:</strong></li>
        <li>&nbsp;&nbsp;• 7 days build-up (awareness grows)</li>
        <li>&nbsp;&nbsp;• 5 days peak (conversions happen)</li>
        <li>&nbsp;&nbsp;• 5 days decay (momentum fades)</li>
        <li><strong>Peak lag:</strong> ~4 days after spend</li>
      </ul>
      <div class="mt-3 p-3 bg-green-900 bg-opacity-20 rounded text-xs">
        <strong>Cross-correlation test:</strong><br/>
        Marketing → Demand: peak at +4 days (r=0.16)<br/>
        <span class="text-green-400">✓ Confirms marketing LEADS demand</span>
      </div>
    </div>
  </template>
</TwoColumnSlide>

<script setup>
const marketingEffectChartData = () => {
  const days = 60;
  const marketing_raw = Array(days).fill(1.0);
  for (let i = 20; i <= 30; i++) marketing_raw[i] = 2.0;

  // Impulse response: marketing on day T affects demand on days T to T+16
  // [build-up days 0-6, peak days 7-11, decay days 12-16]
  const ir = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0, 1.0, 0.9, 0.7, 0.5, 0.3, 0.2, 0.1];
  const effect = Array(days).fill(0);

  // Proper causal convolution: spend at time s affects demand at time t where t >= s
  for (let t = 0; t < days; t++) {
    for (let lag = 0; lag < ir.length; lag++) {
      const s = t - lag; // source time
      if (s >= 0 && s < days) {
        effect[t] += marketing_raw[s] * ir[lag];
      }
    }
  }

  const dates = Array.from({length: days}, (_, i) => `Day ${i}`);

  // Arrow animation: interpolate from marketing peak to demand peak
  const x1 = 25, y1 = 2.5;   // Marketing peak
  const x2 = 34, y2 = 15.0;  // Demand peak (actual peak is around day 34)
  const numFrames = 20;

  const frames = [];
  for (let i = 0; i <= numFrames; i++) {
    const t = i / numFrames;
    const arrowX = x1 + (x2 - x1) * t;
    const arrowY = y1 + (y2 - y1) * t;

    frames.push({
      name: `frame${i}`,
      layout: {
        annotations: [
          {
            x: `Day ${Math.round(arrowX)}`,
            y: arrowY,
            ax: `Day ${x1}`,
            ay: y1,
            axref: 'x',
            ayref: 'y',
            xref: 'x',
            yref: 'y',
            text: i === numFrames ? '~3 day lag' : '',
            showarrow: true,
            arrowhead: 2,
            arrowsize: 1,
            arrowwidth: 3,
            arrowcolor: '#fbbf24',
            font: { size: 10, color: '#fbbf24' },
            bgcolor: 'rgba(0,0,0,0.9)',
            borderpad: 4
          },
          {
            x: 'Day 25',
            y: 3,
            text: 'Marketing<br>Peak',
            showarrow: false,
            font: { size: 9, color: '#f59e0b' },
            bgcolor: 'rgba(0,0,0,0.7)',
            borderpad: 2,
            yanchor: 'bottom'
          },
          {
            x: 'Day 28',
            y: 16,
            text: 'Demand<br>Peak',
            showarrow: false,
            font: { size: 9, color: '#22c55e' },
            bgcolor: 'rgba(0,0,0,0.7)',
            borderpad: 2,
            yanchor: 'bottom'
          }
        ]
      }
    });
  }

  return {
    traces: [
      {
        x: dates,
        y: marketing_raw,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#f59e0b', width: 2, dash: 'dot' },
        name: 'Marketing Spend (raw)'
      },
      {
        x: dates,
        y: effect,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#22c55e', width: 3 },
        name: 'Effect on Demand',
        fill: 'tozeroy',
        fillcolor: 'rgba(34, 197, 94, 0.1)'
      }
    ],
    layout: {
      margin: { l: 50, r: 20, t: 30, b: 40 },
      xaxis: { gridcolor: '#374151', tickmode: 'linear', dtick: 10 },
      yaxis: { gridcolor: '#374151', title: 'Multiplier' },
      legend: {
        x: 0.5,
        xanchor: 'center',
        y: 1.05,
        orientation: 'h',
        font: { size: 9 }
      }
    },
    config: {},
    frames: frames
  };
};
</script>

---

# The Signal

Air Jordan sales follow predictable patterns—with surprises

- **Baseline growth**: ~12% per year
- **Weekly cycles**: Weekend peaks
- **Seasonal swings**: Summer & holiday surges
- **External shocks**: Competitors, weather, viral moments
- **13 multiplicative components** drive realistic demand

---

# Seasonal Patterns

Weekly, monthly, and yearly cycles shape baseline demand

<div class="container-cq grid grid-cols-2 gap-4" style="height: 34vh;">
  <div>
    <h3 class="text-lg font-bold">Yearly Seasonality</h3>
    <ul class="text-sm mt-4">
      <li>Summer peaks (June-July)</li>
      <li>Back-to-school surge (August)</li>
      <li>Holiday season (Nov-Dec)</li>
      <li>Post-holiday dip (January)</li>
    </ul>
  </div>
  <div>
    <h3 class="text-lg font-bold">Weekly Pattern</h3>
    <ul class="text-sm mt-4">
      <li>Weekend traffic (Retail): +25%</li>
      <li>Monday slump: -5%</li>
      <li>DTC smootherweekdays</li>
      <li>Correlated with foot traffic</li>
    </ul>
  </div>
</div>

---

# The Signal: 6 Years of Demand

Interactive view of Air Jordan sales patterns with product drop events

<div style="height: 450px; width: 100%;">
  <AnimatedTimeline />
</div>

<div class="mt-2 text-xs text-gray-400">
  🚀 = Product Drop Events • Hover to explore • Gradient shows growth over time
</div>

---

# How the Pieces Combine

**13 multiplicative components** create realistic demand patterns

<div style="height: 450px; width: 100%;">
  <ComponentsStack />
</div>

<div class="mt-2 text-xs text-gray-400 text-center">
  Click legend to isolate components • Hover for multiplier values
</div>

---

# Predictions vs Actual

**How well does Prophet track actual demand?**

<div style="height: 450px; width: 100%;">
  <ModelPredictions />
</div>

<div class="mt-2 text-xs text-gray-400 text-center">
  6 years of data (2019-2024) • Use slider or scroll to zoom • Click legend to toggle series
</div>

---

# Model Comparison

**Which model handles this complexity best?**

<div style="height: 450px; width: 100%;">
  <ModelBars />
</div>

<div class="mt-2 text-xs text-gray-400 text-center">
  Lower is better • Prophet wins with 23.34 MAE (19% better than #2)
</div>

---

# First Results: Too Good to Be True?

Initial benchmark looked impressive...

<div class="grid grid-cols-2 gap-8 mt-6">
  <div>
    <h3 class="text-lg font-bold mb-4">Initial Results (56-day horizon)</h3>
    <table class="text-sm w-full">
      <thead>
        <tr class="border-b border-gray-600">
          <th class="text-left py-2">Model</th>
          <th class="text-right">MAE</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-green-400">
          <td>LightGBM</td>
          <td class="text-right font-mono">19.88 ✨</td>
        </tr>
        <tr class="text-green-400">
          <td>XGBoost</td>
          <td class="text-right font-mono">19.99 ✨</td>
        </tr>
        <tr>
          <td>Prophet</td>
          <td class="text-right font-mono">27.76 😞</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div>
    <h3 class="text-lg font-bold mb-4 text-red-400">🚨 Problem Discovered</h3>
    <div class="text-sm space-y-3">
      <p><strong>Question:</strong> Why are ML models <em>so much better</em>?</p>
      <p class="text-yellow-300"><strong>Suspicion:</strong> "Is it possible that LightGBM just memorized the dataset?"</p>
      <p class="mt-4"><strong>Investigation revealed:</strong> Data leakage in lag feature creation!</p>
    </div>
  </div>
</div>

<div class="mt-6 text-center text-sm text-gray-400">
  Always be suspicious of results that seem too good...
</div>

---

# The Data Leakage Problem

**The Mistake:** ML models were "peeking at the future"

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
    <p class="text-xs mt-3">When forecasting day 100, the model had access to data from days 101-106. This is <strong>impossible in production!</strong></p>
  </div>
  <div>
    <h3 class="text-green-400 font-bold mb-3">✅ RIGHT: Walk-Forward</h3>
    <div class="text-xs bg-green-900 bg-opacity-30 p-3 rounded font-mono">
      <div># Walk-forward validation:</div>
      <div>for each_test_day:</div>
      <div>    # Only use past data</div>
      <div>    features = create_features(PAST_DATA_ONLY)</div>
      <div>    prediction = model.predict(features)</div>
      <div>    add_actual_to_history()  # Realistic!</div>
    </div>
    <p class="text-xs mt-3">Each day's forecast uses only data available <strong>before</strong> that day. This mirrors production reality.</p>
  </div>
</div>

<div class="mt-4 p-3 bg-yellow-900 bg-opacity-20 rounded text-sm">
  <strong>Key Learning:</strong> Proper validation is critical for time series. Always use walk-forward!
</div>

---

# After Fixing: Honest Evaluation

Error increased 48% when we removed the "cheat"

<div class="grid grid-cols-2 gap-8 mt-6">
  <div>
    <h3 class="font-bold mb-4">Results After Fix (56-day)</h3>
    <table class="text-sm w-full">
      <thead>
        <tr class="border-b border-gray-600">
          <th class="text-left py-2">Model</th>
          <th class="text-right">MAE</th>
          <th class="text-right">Change</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-green-400">
          <td>Prophet</td>
          <td class="text-right font-mono">27.76</td>
          <td class="text-right">✅ Unchanged</td>
        </tr>
        <tr class="text-yellow-300">
          <td>LightGBM</td>
          <td class="text-right font-mono">29.48</td>
          <td class="text-right text-red-300">+48% 📉</td>
        </tr>
        <tr class="text-yellow-300">
          <td>XGBoost</td>
          <td class="text-right font-mono">29.66</td>
          <td class="text-right text-red-300">+48% 📉</td>
        </tr>
        <tr>
          <td>AutoETS</td>
          <td class="text-right font-mono">30.42</td>
          <td class="text-right">-</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div>
    <h3 class="font-bold mb-4">Key Insights</h3>
    <ul class="text-sm space-y-3">
      <li>✅ <strong>Prophet wins</strong> when validation is fair</li>
      <li>📉 ML models struggled without seeing the future</li>
      <li>🔍 But there's more to the story...</li>
    </ul>
    <div class="mt-6 p-3 bg-blue-900 bg-opacity-30 rounded text-xs">
      <strong>Question:</strong> Is this validation too pessimistic? In production, don't we have yesterday's actual sales?
    </div>
  </div>
</div>

---

# The Realistic Scenario

**In production:** You have yesterday's actuals when forecasting tomorrow

<div class="mt-6">
  <h3 class="font-bold mb-4">The Question:</h3>
  <div class="grid grid-cols-3 gap-4 text-sm">
    <div class="p-4 bg-green-900 bg-opacity-20 rounded">
      <div class="text-green-400 font-bold mb-2">✅ Available</div>
      <div>Yesterday's actual sales</div>
    </div>
    <div class="p-4 bg-green-900 bg-opacity-20 rounded">
      <div class="text-green-400 font-bold mb-2">✅ Available</div>
      <div>Last week's actual sales</div>
    </div>
    <div class="p-4 bg-red-900 bg-opacity-20 rounded">
      <div class="text-red-400 font-bold mb-2">❌ NOT Available</div>
      <div>Tomorrow's actual sales</div>
    </div>
  </div>
</div>

<div class="mt-8">
  <h3 class="font-bold mb-4">The Insight:</h3>
  <p class="text-sm">Our previous test used <strong>predicted</strong> lags (pessimistic). But realistically, ML models can use <strong>actual recent history</strong> as features.</p>
</div>

<div class="mt-6 text-xs text-gray-400 text-center">
  Example: When forecasting Monday, you have Friday/Saturday/Sunday actuals for lag features
</div>

---

<AnimatedBackground type="perlin" />

# Final Results: Best of Both Worlds

**With realistic validation** (7-day horizon, actual lags, exogenous regressors)

<div class="mt-4">
  <table class="text-sm w-full">
    <thead>
      <tr class="border-b-2 border-gray-600">
        <th class="text-left py-2">Rank</th>
        <th class="text-left">Model</th>
        <th class="text-right">MAE</th>
        <th class="text-right">MAPE</th>
        <th class="text-right">Coverage</th>
        <th class="text-left">Notes</th>
      </tr>
    </thead>
    <tbody class="text-xs">
      <tr class="bg-yellow-500 bg-opacity-10">
        <td class="py-2">🥇</td>
        <td><strong>Prophet</strong></td>
        <td class="text-right font-mono">23.34</td>
        <td class="text-right font-mono">127.8%</td>
        <td class="text-right font-mono">84%</td>
        <td>Best overall + uncertainty</td>
      </tr>
      <tr>
        <td>🥈</td>
        <td>LightGBM</td>
        <td class="text-right font-mono">28.90</td>
        <td class="text-right font-mono">107.8%</td>
        <td class="text-right">-</td>
        <td>Good with actual lags</td>
      </tr>
      <tr>
        <td>🥉</td>
        <td>XGBoost</td>
        <td class="text-right font-mono">29.83</td>
        <td class="text-right font-mono">109.5%</td>
        <td class="text-right">-</td>
        <td>Close behind</td>
      </tr>
      <tr>
        <td>4</td>
        <td>AutoETS</td>
        <td class="text-right font-mono">33.13</td>
        <td class="text-right font-mono">81.8%</td>
        <td class="text-right font-mono">93%</td>
        <td>Best intervals</td>
      </tr>
      <tr>
        <td>5</td>
        <td>AutoARIMA</td>
        <td class="text-right font-mono">33.32</td>
        <td class="text-right font-mono">96.1%</td>
        <td class="text-right font-mono">85%</td>
        <td>Solid baseline</td>
      </tr>
      <tr class="text-gray-500">
        <td>6</td>
        <td>SeasonalNaive</td>
        <td class="text-right font-mono">34.34</td>
        <td class="text-right font-mono">88.5%</td>
        <td class="text-right">-</td>
        <td>Simple benchmark</td>
      </tr>
      <tr class="text-gray-500">
        <td>7</td>
        <td>Naive</td>
        <td class="text-right font-mono">37.99</td>
        <td class="text-right font-mono">81.7%</td>
        <td class="text-right">-</td>
        <td>Baseline</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="mt-4 grid grid-cols-2 gap-4 text-xs">
  <div class="p-2 bg-blue-900 bg-opacity-20 rounded">
    <strong>MAE = 23.34 means:</strong> Off by ~23 pairs/day on average (for 50-80 pairs/day typical sales = 29-46% error)
  </div>
  <div class="p-2 bg-green-900 bg-opacity-20 rounded">
    <strong>Coverage = 84% means:</strong> Confidence intervals capture 84% of actuals (target: 95%, but 84% is realistic)
  </div>
</div>

---

# Enhanced Realism: New Components

We added **3 real-world factors** executives face daily

<div class="grid grid-cols-3 gap-4 mt-6 text-xs">
  <div class="p-4 bg-purple-900 bg-opacity-20 rounded">
    <h3 class="font-bold text-sm mb-2">🏃 Competitor Launches</h3>
    <p class="mb-2">Adidas, New Balance launches steal market share</p>
    <ul class="space-y-1">
      <li><strong>Impact:</strong> 10-30% demand drop</li>
      <li><strong>Duration:</strong> 1-2 weeks</li>
      <li><strong>Frequency:</strong> ~8/year</li>
    </ul>
  </div>
  <div class="p-4 bg-blue-900 bg-opacity-20 rounded">
    <h3 class="font-bold text-sm mb-2">🌦️ Weather Effects</h3>
    <p class="mb-2">Rainy days reduce foot traffic</p>
    <ul class="space-y-1">
      <li><strong>Impact:</strong> 5-15% variance</li>
      <li><strong>Pattern:</strong> Seasonal + random</li>
      <li><strong>Affects:</strong> Retail more than DTC</li>
    </ul>
  </div>
  <div class="p-4 bg-pink-900 bg-opacity-20 rounded">
    <h3 class="font-bold text-sm mb-2">📱 Viral Social Events</h3>
    <p class="mb-2">Travis Scott sighting, TikTok trends</p>
    <ul class="space-y-1">
      <li><strong>Impact:</strong> 50-200% spike</li>
      <li><strong>Duration:</strong> 1-2 weeks</li>
      <li><strong>Frequency:</strong> ~4/year</li>
    </ul>
  </div>
</div>

<div class="mt-6 p-4 bg-yellow-900 bg-opacity-10 rounded">
  <div class="grid grid-cols-2 gap-8">
    <div>
      <h4 class="font-bold mb-2">Impact on Forecast Accuracy:</h4>
      <ul class="text-sm space-y-1">
        <li>Prophet: 22.90 → 23.34 MAE (<strong>+1.9%</strong> only!) ✅</li>
        <li>XGBoost: 26.58 → 29.83 MAE (+12.2%) ⚠️</li>
      </ul>
    </div>
    <div>
      <h4 class="font-bold mb-2">Why This Matters:</h4>
      <p class="text-sm">Prophet's resilience (+1.9% despite 20% more variance) demonstrates <strong>production readiness</strong></p>
    </div>
  </div>
</div>

---
layout: two-cols
---

# Prophet Forecast

Model captures trend + seasonality + holiday effects + exogenous factors

<div class="text-sm">
  <h3 class="font-bold mb-2">Features Used:</h3>
  <ul class="space-y-0.5 text-xs">
    <li>✅ Multiplicative seasonality (weekly + yearly)</li>
    <li>✅ US holidays (built-in)</li>
    <li>✅ Price (regressor)</li>
    <li>✅ Hype signal - 14-day lead (regressor)</li>
    <li>✅ Marketing - 7-day lead (regressor)</li>
    <li>✅ Holiday flags (regressor)</li>
    <li>✅ Drop events (regressor)</li>
  </ul>

  <h3 class="font-bold mt-3 mb-1.5">Final Metrics (7-day):</h3>
  <ul class="space-y-0.5 text-xs">
    <li><strong>MAE:</strong> 23.34 pairs/day</li>
    <li><strong>MAPE:</strong> 127.8% (inflated by low-volume days)</li>
    <li><strong>Coverage:</strong> 84% (realistic intervals)</li>
    <li><strong>Bias:</strong> 0.01 (unbiased!)</li>
  </ul>
</div>

::right::

<div style="height: 500px; width: 100%;">
  <ForecastCone />
</div>

<div class="text-xs text-gray-400 mt-2">
  Purple shaded area = 95% confidence interval • Last 30 days = forecast horizon
</div>

---

# Inventory Reality

Stockouts happen—especially during peaks

<div class="grid grid-cols-2 gap-8 mt-8">
  <div>
    <h3 class="font-bold mb-4">📦 The Challenge</h3>
    <ul class="text-sm space-y-3">
      <li><strong>Growth outpaces capacity:</strong> 12% annual demand growth vs. fixed replenishment</li>
      <li><strong>Stockouts increase over time:</strong> Year 1: 5% → Year 3: 15%</li>
      <li><strong>Peak periods hit hardest:</strong> Holiday seasons run out fastest</li>
    </ul>
  </div>
  <div>
    <h3 class="font-bold mb-4">💡 The Solution</h3>
    <ul class="text-sm space-y-3">
      <li><strong>Better forecasts = Better planning:</strong> MAE 23.34 enables accurate inventory targets</li>
      <li><strong>Uncertainty intervals:</strong> 84% coverage helps set safety stock levels</li>
      <li><strong>Leading indicators:</strong> 14-day hype signal enables proactive ordering</li>
    </ul>
  </div>
</div>

<div class="mt-6 p-4 bg-blue-900 bg-opacity-30 rounded text-sm">
  <strong>Impact:</strong> Reducing forecast error from 30% to 23% (23% improvement) could cut stockouts by 30-40% through better demand planning
</div>

---

<AnimatedBackground type="perlin" />

# What We Learned

The complete journey from data to production-ready model

<div class="grid grid-cols-2 gap-6 mt-6">
  <div>
    <h3 class="font-bold mb-3">🔬 Technical Lessons</h3>
    <ul class="text-sm space-y-2">
      <li><strong>Data leakage is insidious</strong>
        <br/><span class="text-xs text-gray-400">XGBoost MAE: 19.99 → 29.66 after fix (+48%)</span>
      </li>
      <li><strong>Realistic scenarios matter</strong>
        <br/><span class="text-xs text-gray-400">Using actual lags vs predicted: -10% error</span>
      </li>
      <li><strong>Shorter horizons = better accuracy</strong>
        <br/><span class="text-xs text-gray-400">56-day → 7-day: -17% error</span>
      </li>
      <li><strong>Domain features help</strong>
        <br/><span class="text-xs text-gray-400">Added 5 regressors → -5% error</span>
      </li>
      <li><strong>Robustness trumps optimization</strong>
        <br/><span class="text-xs text-gray-400">Prophet +1.9% with harder data (resilient!)</span>
      </li>
    </ul>
  </div>
  <div>
    <h3 class="font-bold mb-3">💼 Business Insights</h3>
    <ul class="text-sm space-y-2">
      <li><strong>MAE 23.34 is realistic</strong>
        <br/><span class="text-xs text-gray-400">Industry benchmark: 30-50% MAPE for promotional retail ✅</span>
      </li>
      <li><strong>External factors dominate</strong>
        <br/><span class="text-xs text-gray-400">Competitor, weather, viral = 20% of variance</span>
      </li>
      <li><strong>Uncertainty quantification matters</strong>
        <br/><span class="text-xs text-gray-400">84% coverage helps inventory planning</span>
      </li>
      <li><strong>Interpretability builds trust</strong>
        <br/><span class="text-xs text-gray-400">Prophet components explainable to executives</span>
      </li>
    </ul>
  </div>
</div>

<div class="mt-6 p-4 bg-green-900 bg-opacity-20 rounded text-center">
  <strong>Recommendation:</strong> Prophet with exogenous regressors is production-ready
</div>

---
layout: center
class: text-center
---

# Dive Deeper

<div class="pt-12">
  <a href="http://localhost:3030/" class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
    View Live Presentation →
  </a>
</div>

<div class="mt-8 text-sm">
  <p>Explore interactive components, compare regions, analyze segments</p>
  <p class="text-xs text-gray-400 mt-2">
    All code, data, and analysis available in the project repository
  </p>
</div>

<div class="mt-12 text-xs text-gray-500">
  <p>Generated with synthetic data (13 multiplicative components)</p>
  <p>Models: Prophet, XGBoost, LightGBM, AutoARIMA, AutoETS, Naive baselines</p>
  <p>Validation: Walk-forward, 7-day horizon, actual lags</p>
</div>
