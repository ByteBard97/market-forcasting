<template>
  <SlideLayout>
    <div class="dive-deeper-slide">
      <h1>Dive Deeper</h1>
      <p class="subtitle">Explore the tools and concepts behind this presentation</p>

      <div class="resources-grid">
        <!-- Time Series Models -->
        <section class="resource-section">
          <h2>Time Series Models</h2>
          <div class="links">
            <ResourceLink
              label="Prophet"
              url="https://facebook.github.io/prophet/"
              description="Facebook's additive regression model for time series with strong seasonal effects and multiple seasons of historical data"
            />
            <ResourceLink
              label="XGBoost"
              url="https://xgboost.readthedocs.io/"
              description="Gradient boosting framework that's highly effective for structured data and time series with proper feature engineering"
            />
            <ResourceLink
              label="LightGBM"
              url="https://lightgbm.readthedocs.io/"
              description="Microsoft's gradient boosting framework optimized for speed and memory efficiency with large datasets"
            />
            <ResourceLink
              label="StatsForecast"
              url="https://nixtlaverse.nixtla.io/statsforecast/"
              description="Fast implementations of statistical forecasting models (ARIMA, ETS) optimized for production use"
            />
          </div>
        </section>

        <!-- Concepts & Theory -->
        <section class="resource-section">
          <h2>Concepts & Theory</h2>
          <div class="links">
            <ResourceLink
              label="Additive Models"
              url="https://en.wikipedia.org/wiki/Additive_model"
              description="Statistical models that combine multiple components (trend + seasonality + holidays) by addition to capture different patterns"
            />
            <ResourceLink
              label="Seasonality"
              url="https://otexts.com/fpp3/components.html"
              description="Repeating patterns at fixed intervals (weekly, yearly) caused by calendar effects, weather, or behavioral patterns"
            />
            <ResourceLink
              label="Price Elasticity"
              url="https://en.wikipedia.org/wiki/Price_elasticity_of_demand"
              description="Measure of how demand changes with price - elasticity of -1.2 means 10% price increase causes 12% demand decrease"
            />
            <ResourceLink
              label="Marketing Mix Modeling"
              url="https://en.wikipedia.org/wiki/Marketing_mix_modeling"
              description="Statistical analysis to estimate impact of marketing tactics on sales, accounting for diminishing returns and lags"
            />
          </div>
        </section>

        <!-- Validation & Techniques -->
        <section class="resource-section">
          <h2>Validation & Techniques</h2>
          <div class="links">
            <ResourceLink
              label="Walk-Forward Validation"
              url="https://en.wikipedia.org/wiki/Backtesting#Walk_forward_testing"
              description="Time series cross-validation where you train on past data, predict the future, then move forward and repeat"
            />
            <ResourceLink
              label="Adstock Transformation"
              url="https://en.wikipedia.org/wiki/Advertising_adstock"
              description="Models lingering effects of marketing - today's ad spend impacts demand for days/weeks via exponential decay"
            />
            <ResourceLink
              label="Impulse Response"
              url="https://en.wikipedia.org/wiki/Impulse_response"
              description="How a system responds over time to a brief input signal - shows how marketing spend affects demand across time"
            />
          </div>
        </section>

        <!-- Tools & Libraries -->
        <section class="resource-section">
          <h2>Tools & Libraries</h2>
          <div class="links">
            <ResourceLink
              label="Nixtla Ecosystem"
              url="https://nixtlaverse.nixtla.io/"
              description="Suite of production-ready time series tools (StatsForecast, NeuralForecast, MLForecast, TimeGPT)"
            />
            <ResourceLink
              label="Fourier Series"
              url="https://en.wikipedia.org/wiki/Fourier_series"
              description="Technique to represent complex seasonal patterns as sum of sine/cosine waves at different frequencies"
            />
            <ResourceLink
              label="Three.js"
              url="https://threejs.org/"
              description="JavaScript library for 3D graphics used to create the animated data sphere background in this presentation"
            />
            <ResourceLink
              label="Slidev"
              url="https://sli.dev/"
              description="Presentation framework for developers - slides written in Markdown with Vue components for interactivity"
            />
          </div>
        </section>
      </div>

      <div class="footer">
        <p>All code, data generation, and analysis available in the project repository</p>
        <p class="tech-note">13 multiplicative demand components • Walk-forward validation • 7-day forecast horizon</p>
      </div>
    </div>
  </SlideLayout>
</template>

<script setup>
import { ref } from 'vue'
import SlideLayout from "../components/SlideLayout.vue"

// Resource link component defined inline
const ResourceLink = {
  props: {
    label: String,
    url: String,
    description: String
  },
  setup(props) {
    const showTooltip = ref(false)

    return { showTooltip }
  },
  template: `
    <div class="resource-link-wrapper">
      <a
        :href="url"
        target="_blank"
        rel="noopener noreferrer"
        class="resource-link"
        @mouseenter="showTooltip = true"
        @mouseleave="showTooltip = false"
      >
        {{ label }}
        <span class="external-icon">↗</span>
      </a>
      <div v-if="showTooltip" class="tooltip">
        {{ description }}
      </div>
    </div>
  `
}
</script>

<style scoped>
.dive-deeper-slide {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 1rem 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  text-align: center;
}

.subtitle {
  text-align: center;
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 1rem;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.resource-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
}

.resource-section h2 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #60a5fa;
  border-bottom: 1px solid rgba(96, 165, 250, 0.3);
  padding-bottom: 0.25rem;
}

.links {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.resource-link-wrapper {
  position: relative;
}

.resource-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: #93c5fd;
  text-decoration: none;
  font-size: 0.85rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
  background: rgba(96, 165, 250, 0.05);
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.resource-link:hover {
  background: rgba(96, 165, 250, 0.15);
  border-color: rgba(96, 165, 250, 0.4);
  color: #bfdbfe;
  transform: translateX(2px);
}

.external-icon {
  font-size: 0.7rem;
  opacity: 0.6;
}

.tooltip {
  position: absolute;
  left: 0;
  top: calc(100% + 0.25rem);
  background: rgba(17, 24, 39, 0.95);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  line-height: 1.4;
  color: #e5e7eb;
  max-width: 300px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  pointer-events: none;
  animation: fadeIn 0.2s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.footer {
  text-align: center;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer p {
  font-size: 0.8rem;
  opacity: 0.7;
  margin: 0.25rem 0;
}

.tech-note {
  font-size: 0.7rem !important;
  opacity: 0.5 !important;
  font-family: 'Fira Code', monospace;
}
</style>
