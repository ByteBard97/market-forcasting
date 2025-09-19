# Vue + Node.js Implementation Plan

## Based on Questionnaire Responses

This document outlines the Vue/Node.js approach, optimized for sub-minute processing with good progress feedback.

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         Vue 3 Frontend (Vite)           │
│  - Drag & drop file upload              │
│  - Real-time progress bars              │
│  - Interactive charts & sliders         │
└────────────────┬────────────────────────┘
                 │ WebSocket/HTTP
┌────────────────▼────────────────────────┐
│      Node.js + Express Backend          │
│  - File parsing & validation            │
│  - Model orchestration                  │
│  - Progress streaming via SSE/WS        │
└────────────────┬────────────────────────┘
                 │ Child Process
┌────────────────▼────────────────────────┐
│    Python ML Worker (Optional)          │
│  - Heavy ML models (Prophet, XGBoost)   │
│  - Falls back to JS if not needed       │
└─────────────────────────────────────────┘
```

## Decision Tree Based on Questionnaire

### Scenario A: Basic Forecasting (Likely Path)
**If Cody answers:**
- Models: Naive seasonal, Exponential smoothing, basic ARIMA
- Data size: < 500 series, monthly data
- No complex ML needed

**Implementation:**
```javascript
// Pure JavaScript - no Python needed!
// backend/models/forecasting.js
import { ARIMA } from 'arima';
import { HoltWinters } from 'holtwinters-js';
import SimpleStatistics from 'simple-statistics';

export class ForecastEngine {
  async runAllModels(data, config) {
    const results = await Promise.all([
      this.runNaiveSeasonal(data),
      this.runHoltWinters(data),
      this.runARIMA(data, config.arimaParams),
      this.runExponentialSmoothing(data)
    ]);

    return this.compareModels(results);
  }
}
```

### Scenario B: Advanced ML (If Requested)
**If Cody answers:**
- Models: Prophet, XGBoost, Neural Networks
- Need for complex seasonality
- High accuracy requirements

**Implementation:**
```javascript
// backend/workers/pythonBridge.js
import { spawn } from 'child_process';
import { EventEmitter } from 'events';

export class PythonMLBridge extends EventEmitter {
  constructor() {
    super();
    this.python = spawn('python', ['ml_server.py']);
  }

  async runProphet(data, params) {
    return this.callPython('prophet', { data, params });
  }

  async runXGBoost(data, params) {
    return this.callPython('xgboost', { data, params });
  }
}
```

## Frontend Implementation

### 1. File Upload & Parsing
```vue
<!-- components/DataUploader.vue -->
<template>
  <div class="uploader"
       @drop.prevent="handleDrop"
       @dragover.prevent>
    <div v-if="!file">
      <CloudUploadIcon />
      <p>Drop CSV or Excel file here</p>
    </div>
    <div v-else>
      <FileIcon />
      <p>{{ file.name }} ({{ formatSize(file.size) }})</p>
      <ProgressBar :value="uploadProgress" />
    </div>
  </div>
</template>

<script setup>
import * as XLSX from 'xlsx';
import Papa from 'papaparse';

async function parseFile(file) {
  const ext = file.name.split('.').pop().toLowerCase();

  if (ext === 'csv') {
    return new Promise((resolve) => {
      Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        complete: (results) => resolve(results.data)
      });
    });
  } else if (['xlsx', 'xls'].includes(ext)) {
    const buffer = await file.arrayBuffer();
    const workbook = XLSX.read(buffer);
    const worksheet = workbook.Sheets[workbook.SheetNames[0]];
    return XLSX.utils.sheet_to_json(worksheet);
  }
}
</script>
```

### 2. Model Configuration UI
```vue
<!-- components/ModelConfigurator.vue -->
<template>
  <div class="model-config">
    <h3>Select Forecasting Models</h3>

    <div class="model-grid">
      <ModelCard
        v-for="model in availableModels"
        :key="model.id"
        :model="model"
        v-model:selected="selectedModels[model.id]"
        v-model:params="modelParams[model.id]"
      />
    </div>

    <div class="performance-estimate">
      <ClockIcon />
      <p>Estimated time: {{ estimatedTime }}s with {{ selectedCount }} models</p>
    </div>
  </div>
</template>

<script setup>
const availableModels = [
  {
    id: 'naive_seasonal',
    name: 'Naive Seasonal',
    speed: 'instant',
    accuracy: 'baseline',
    params: { periods: 12 }
  },
  {
    id: 'holtwinters',
    name: 'Holt-Winters',
    speed: 'fast',
    accuracy: 'good',
    params: { seasonal: 'multiplicative', periods: 12 }
  },
  {
    id: 'arima',
    name: 'Auto-ARIMA',
    speed: 'medium',
    accuracy: 'very good',
    params: { max_p: 3, max_q: 3, seasonal: true }
  },
  {
    id: 'prophet',
    name: 'Prophet',
    speed: 'slower',
    accuracy: 'excellent',
    params: { yearly_seasonality: true, weekly_seasonality: false },
    requiresPython: true
  }
];

const estimatedTime = computed(() => {
  const times = {
    instant: 0.1,
    fast: 2,
    medium: 10,
    slower: 20
  };

  return Object.entries(selectedModels.value)
    .filter(([_, selected]) => selected)
    .reduce((sum, [modelId]) => {
      const model = availableModels.find(m => m.id === modelId);
      return sum + times[model.speed] * (seriesCount.value / 100);
    }, 0).toFixed(1);
});
</script>
```

### 3. Progress Tracking
```vue
<!-- components/ForecastProgress.vue -->
<template>
  <div class="forecast-progress" v-if="isRunning">
    <h3>Running Forecasts...</h3>

    <div v-for="model in runningModels" :key="model.id" class="model-progress">
      <div class="model-header">
        <span>{{ model.name }}</span>
        <span class="time">{{ model.elapsed }}s</span>
      </div>

      <ProgressBar
        :value="model.progress"
        :status="model.status"
        :label="model.currentSeries"
      />

      <div class="sub-tasks" v-if="model.subTasks">
        <div v-for="task in model.subTasks" :key="task.id">
          <CheckIcon v-if="task.done" />
          <SpinnerIcon v-else-if="task.active" />
          <CircleIcon v-else />
          <span>{{ task.name }}</span>
        </div>
      </div>
    </div>

    <div class="overall-progress">
      <ProgressBar :value="overallProgress" variant="primary" />
      <p>{{ completedModels }} of {{ totalModels }} models complete</p>
    </div>
  </div>
</template>

<script setup>
import { useEventSource } from '@vueuse/core';

// Server-Sent Events for real-time progress
const { data } = useEventSource('/api/forecast-progress');

watch(data, (update) => {
  const progress = JSON.parse(update);
  updateModelProgress(progress);
});
</script>
```

### 4. Results Visualization
```vue
<!-- components/ForecastResults.vue -->
<template>
  <div class="results">
    <!-- Model Comparison Chart -->
    <div class="chart-container">
      <PlotlyChart :data="chartData" :layout="chartLayout" />
    </div>

    <!-- Model Leaderboard -->
    <div class="leaderboard">
      <h3>Model Performance</h3>
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>MAPE</th>
            <th>RMSE</th>
            <th>Coverage</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="model in sortedModels" :key="model.id"
              :class="{ best: model.rank === 1 }">
            <td>{{ model.name }}</td>
            <td>{{ model.mape.toFixed(2) }}%</td>
            <td>${{ model.rmse.toLocaleString() }}</td>
            <td>{{ model.coverage.toFixed(1) }}%</td>
            <td>{{ model.time }}s</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Scenario Sliders -->
    <div class="scenarios">
      <h3>What-If Scenarios</h3>
      <SliderInput
        v-model="scenario.promoUplift"
        label="Promotion Impact"
        :min="-20" :max="50" :step="5"
        suffix="%"
        @update="recalculateForecast"
      />
      <SliderInput
        v-model="scenario.priceChange"
        label="Price Change"
        :min="-30" :max="30" :step="1"
        suffix="%"
        @update="recalculateForecast"
      />
    </div>
  </div>
</template>
```

## Backend Implementation

### 1. Main Server (Node.js)
```javascript
// server.js
import express from 'express';
import multer from 'multer';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { ForecastOrchestrator } from './orchestrator.js';

const app = express();
const server = createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

const orchestrator = new ForecastOrchestrator(io);

// File upload endpoint
app.post('/api/upload', upload.single('file'), async (req, res) => {
  const data = await parseFile(req.file);
  const validationResult = validateData(data);

  res.json({
    success: validationResult.valid,
    seriesCount: validationResult.seriesCount,
    timePoints: validationResult.timePoints,
    issues: validationResult.issues
  });
});

// Forecast endpoint with progress streaming
app.post('/api/forecast', async (req, res) => {
  const { data, models, config } = req.body;
  const jobId = generateJobId();

  // Start async processing
  orchestrator.startForecast(jobId, data, models, config);

  // Return immediately with job ID
  res.json({ jobId, estimatedTime: orchestrator.estimateTime(data, models) });
});

// Progress updates via Server-Sent Events
app.get('/api/forecast-progress/:jobId', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });

  const listener = (progress) => {
    res.write(`data: ${JSON.stringify(progress)}\n\n`);
  };

  orchestrator.on(`progress-${req.params.jobId}`, listener);

  req.on('close', () => {
    orchestrator.off(`progress-${req.params.jobId}`, listener);
  });
});
```

### 2. Forecast Orchestrator
```javascript
// orchestrator.js
import { EventEmitter } from 'events';
import pLimit from 'p-limit';
import { Worker } from 'worker_threads';

export class ForecastOrchestrator extends EventEmitter {
  constructor(io) {
    super();
    this.io = io;
    this.jobs = new Map();
    this.limit = pLimit(4); // Run 4 models in parallel
  }

  async startForecast(jobId, data, models, config) {
    const job = {
      id: jobId,
      status: 'running',
      models: models.map(m => ({ ...m, progress: 0 })),
      startTime: Date.now()
    };

    this.jobs.set(jobId, job);

    // Process each model
    const results = await Promise.all(
      models.map(model =>
        this.limit(() => this.runModel(jobId, model, data, config))
      )
    );

    // Compute comparison metrics
    const comparison = this.compareModels(results, data);

    job.status = 'complete';
    job.results = comparison;
    job.duration = (Date.now() - job.startTime) / 1000;

    this.emit(`complete-${jobId}`, comparison);
    return comparison;
  }

  async runModel(jobId, model, data, config) {
    const updateProgress = (progress) => {
      const job = this.jobs.get(jobId);
      const modelStatus = job.models.find(m => m.id === model.id);
      modelStatus.progress = progress;

      this.emit(`progress-${jobId}`, {
        jobId,
        modelId: model.id,
        progress,
        overall: this.calculateOverallProgress(job)
      });
    };

    // JavaScript models (fast path)
    if (model.type === 'javascript') {
      return this.runJSModel(model, data, config, updateProgress);
    }

    // Python models (slower but more powerful)
    if (model.type === 'python') {
      return this.runPythonModel(model, data, config, updateProgress);
    }
  }

  async runJSModel(model, data, config, onProgress) {
    // Run in worker thread for non-blocking
    return new Promise((resolve, reject) => {
      const worker = new Worker('./workers/jsModels.js', {
        workerData: { model, data, config }
      });

      worker.on('message', (msg) => {
        if (msg.type === 'progress') {
          onProgress(msg.value);
        } else if (msg.type === 'complete') {
          resolve(msg.result);
        }
      });

      worker.on('error', reject);
    });
  }
}
```

### 3. JavaScript Model Workers
```javascript
// workers/jsModels.js
import { parentPort, workerData } from 'worker_threads';
import ARIMA from 'arima';
import { HoltWinters } from 'holtwinters-js';

const { model, data, config } = workerData;

async function runARIMA(series, params) {
  const arima = new ARIMA({
    p: params.p || 2,
    d: params.d || 1,
    q: params.q || 2,
    P: params.P || 1,
    D: params.D || 1,
    Q: params.Q || 1,
    s: params.s || 12,
    verbose: false
  });

  const [train, test] = splitData(series, config.testSize);

  arima.train(train);
  const forecast = arima.predict(config.horizon);

  return {
    forecast,
    metrics: calculateMetrics(test, forecast),
    model: 'ARIMA'
  };
}

async function runHoltWinters(series, params) {
  const hw = new HoltWinters({
    alpha: params.alpha || 0.5,
    beta: params.beta || 0.4,
    gamma: params.gamma || 0.6,
    period: params.period || 12,
    multiplicative: params.seasonal === 'multiplicative'
  });

  const forecast = hw.forecast(series, config.horizon);

  return {
    forecast,
    metrics: calculateMetrics(series.slice(-config.testSize), forecast),
    model: 'Holt-Winters'
  };
}

// Process each series
let processed = 0;
const results = [];

for (const series of data.series) {
  let result;

  switch (model.id) {
    case 'arima':
      result = await runARIMA(series, model.params);
      break;
    case 'holtwinters':
      result = await runHoltWinters(series, model.params);
      break;
    // ... other models
  }

  results.push(result);
  processed++;

  // Report progress
  parentPort.postMessage({
    type: 'progress',
    value: (processed / data.series.length) * 100
  });
}

// Send final results
parentPort.postMessage({
  type: 'complete',
  result: aggregateResults(results)
});
```

### 4. Optional Python Bridge
```javascript
// workers/pythonBridge.js
import { spawn } from 'child_process';
import { EventEmitter } from 'events';

export class PythonModelRunner extends EventEmitter {
  constructor() {
    super();
    this.pythonProcess = null;
    this.initPython();
  }

  initPython() {
    // Check if Python environment exists
    const pythonPath = process.env.PYTHON_PATH || 'python3';

    try {
      this.pythonProcess = spawn(pythonPath, [
        'ml_models/server.py'
      ]);

      this.pythonProcess.stdout.on('data', (data) => {
        const msg = JSON.parse(data.toString());
        this.emit(msg.type, msg.data);
      });

    } catch (error) {
      console.log('Python ML models not available, using JS fallback');
      this.pythonAvailable = false;
    }
  }

  async runModel(modelName, data, params) {
    if (!this.pythonAvailable) {
      throw new Error('Python models not available');
    }

    return new Promise((resolve) => {
      const requestId = generateId();

      this.once(`result-${requestId}`, resolve);

      this.pythonProcess.stdin.write(JSON.stringify({
        id: requestId,
        model: modelName,
        data,
        params
      }) + '\n');
    });
  }
}
```

## Deployment Options

### 1. Desktop App (Tauri)
```toml
# src-tauri/tauri.conf.json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "package": {
    "productName": "Market Forecaster",
    "version": "1.0.0"
  },
  "tauri": {
    "bundle": {
      "active": true,
      "icon": ["icons/icon.icns"],
      "identifier": "com.marketforecaster.app",
      "targets": "all"
    }
  }
}
```

### 2. Build Script
```bash
#!/bin/bash
# build.sh

# Install dependencies
npm install
cd backend && npm install

# Build frontend
npm run build

# Package with Tauri
npm run tauri build

# Or create Electron app
# npx electron-packager . MarketForecaster --platform=darwin --arch=x64
```

## Performance Optimizations

### 1. Caching Strategy
```javascript
// Use LRU cache for repeated calculations
import LRU from 'lru-cache';

const modelCache = new LRU({
  max: 500,
  ttl: 1000 * 60 * 60 // 1 hour
});

function getCacheKey(data, model, params) {
  return `${hashData(data)}-${model.id}-${JSON.stringify(params)}`;
}
```

### 2. Progressive Loading
```javascript
// Stream results as they complete
async function* streamForecasts(models, data) {
  for (const model of models) {
    const result = await runModel(model, data);
    yield { model: model.id, result };
  }
}
```

## Expected Performance

| Scenario | Data Size | Models | Expected Time |
|----------|-----------|---------|---------------|
| Small | 100 series × 60 points | ARIMA, HW, Naive | 5-10s |
| Medium | 300 series × 60 points | ARIMA, HW, Naive | 15-30s |
| Large | 500 series × 120 points | ARIMA, HW, Naive | 30-50s |
| With Python | 300 series × 60 points | + Prophet, XGBoost | 40-60s |

## User Experience Features

1. **Real-time Progress**: WebSocket updates every 100ms
2. **Partial Results**: Show completed models while others run
3. **Cancel Support**: Stop long-running jobs
4. **Export Queue**: Generate reports in background
5. **Auto-save**: Persist scenarios to localStorage