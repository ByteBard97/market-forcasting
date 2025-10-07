# Executive Slide Deck: Forecasting Air Jordan Demand
## A Journey Through Modern Time Series Prediction

**Target Audience:** Shoe executive (landlord)
**Goal:** Demonstrate the power of vibe coding + teach modern time series forecasting
**Tech Stack:** Vue 3 + Slidev + Vanta.js backgrounds + Manim animations + ECharts/D3 interactivity

---

## Narrative Arc

This deck tells a story in 5 acts:
1. **The Challenge** - Why this matters for shoe business
2. **Building Realistic Data** - Component-by-component synthetic data generation
3. **How Components Combine** - Multiplicative composition
4. **Classical Forecasting: Prophet** - Facebook's time series workhorse
5. **Modern Approaches** - Neural networks (TimeGPT) & gradient boosting

---

## Act 1: The Challenge (3 slides)

### Slide 1: Title Slide
**Component:** `TitleSlide.vue`
**Background:** Vanta Waves (or Perlin Noise for elegance)
**Content:**
- Title: "Forecasting Air Jordan Demand"
- Subtitle: "A Journey Through Modern Time Series Prediction"
- Footer: "Built with Vibe Coding"

**Visual:**
- Animated title fade-in
- Subtle particle effects in background
- Clean typography (Tympanus-inspired fonts)

---

### Slide 2: The Business Challenge
**Component:** `BusinessChallengeSlide.vue` (NEW)
**Background:** Vanta Net or Data Sphere
**Content:**
- **Problem:** Shoe companies need to predict demand to:
  - Avoid stockouts (lost sales during hype drops)
  - Minimize overstock (capital tied up, markdowns)
  - Optimize production & distribution
- **Stakes:**
  - Stockout = missed revenue + brand damage
  - Overstock = margin erosion + storage costs
- **Example:** Air Jordan release day - how many pairs per store?

**Visual Options:**
1. **Animated infographic** (JS):
   - Three columns: "Too Little" (empty shelves) | "Just Right" (full shelves, happy customers) | "Too Much" (discount bins)
   - Use GSAP for smooth transitions
2. **Manim animation:**
   - Show demand curve vs inventory levels
   - Highlight stockout periods (red zones)
   - Show cost of mismatch

**Preferred:** Interactive JS with hover states showing costs

---

### Slide 3: The Data Problem
**Component:** `DataProblemSlide.vue` (NEW)
**Background:** Vanta Fog
**Content:**
- **Challenge:** Real shoe sales data is:
  - Proprietary (Nike won't share!)
  - Messy (returns, cancellations, system glitches)
  - Incomplete (missing competitor data, weather, social signals)
- **Solution:** Build synthetic data that behaves realistically
- **Why synthetic?**
  - Control ground truth (we know what drives demand)
  - Test forecasting methods fairly
  - Demonstrate concepts without legal issues

**Visual Options:**
1. **Split screen comparison:**
   - Left: "Real Data" - chaotic, messy chart with question marks
   - Right: "Synthetic Data" - clean, labeled components
2. **Animated transformation:**
   - Start with messy real data
   - Apply "synthesis process"
   - End with clean multi-component data

**Preferred:** Animated transformation (GSAP)

---

## Act 2: Building Realistic Synthetic Data (13 slides)

### Slide 4: Baseline Growth
**Component:** `BaselineSlide.vue` (EXISTS - enhance)
**Background:** Perlin Noise
**Content:**
- **What:** Slow upward trend (brand growing over time)
- **Math:** `baseline_t = 50 + 25 * (t / T)` (linear growth from 50 → 75 pairs/day)
- **Why:** Air Jordans gaining popularity 2019-2024

**Visual:**
- Line chart showing smooth upward trend
- Animate line drawing from left to right
- Add subtle glow effect on the line
- Show equation overlaid

**Enhancement:** Add animated equation that highlights variables

---

### Slide 5: Weekly Seasonality
**Component:** `WeeklySeasonalitySlide.vue` (EXISTS - enhance)
**Background:** Vanta Waves
**Content:**
- **What:** Weekend uplift for retail shopping
- **Pattern:**
  - Monday-Friday: 0.95× (5% dip)
  - Saturday-Sunday: 1.25× (25% boost)
- **Why:** People shop for sneakers on weekends
- **Mean:** ~1.0 (balanced)

**Visual:**
- Repeating wave pattern showing weekly cycles
- 7-day segments clearly marked
- Color code weekdays (blue) vs weekends (gold)
- **Manim option:** Show wave equation building up

**Enhancement:** Interactive hover showing actual day-of-week multipliers

---

### Slide 6: Yearly Seasonality
**Component:** `YearlySeasonalitySlide.vue` (EXISTS - enhance)
**Background:** Data Sphere
**Content:**
- **What:** Annual patterns tied to calendar
- **Peaks:**
  - Back to school (August-September): +20%
  - Holiday season (November-December): +30%
- **Troughs:**
  - Post-holiday (January-February): -15%
  - Summer lull (June-July): -10%

**Visual:**
- 12-month sine wave with labeled peaks/troughs
- Overlay icons: backpack (school), gift (holidays), sun (summer)
- Animate full year cycle
- Show multiple years stacked

**Enhancement:** Add circular "clock" visualization showing seasonal cycle

---

### Slide 7: Holiday Effects
**Component:** `HolidayEffectSlide.vue` (NEW)
**Background:** Vanta Clouds
**Content:**
- **What:** Specific date-based demand spikes
- **Major holidays:**
  - Black Friday: 2.5× (150% boost)
  - Cyber Monday: 2.0× (100% boost)
  - Christmas week: 1.8× (80% boost)
  - Memorial Day: 1.3× (30% boost)
- **Duration:** 1-3 days per event

**Visual Options:**
1. **Timeline with spikes:**
   - Horizontal timeline (6 years)
   - Vertical bars for each holiday
   - Height = multiplier strength
   - Color code by holiday type
2. **Manim animation:**
   - Show baseline + weekly/yearly
   - Add holiday "impulses" that shoot up
   - Watch them decay back to trend

**Preferred:** Interactive timeline (click holiday to see details)

---

### Slide 8: Drop Events
**Component:** `DropEventsSlide.vue` (NEW)
**Background:** Distorted Cube
**Content:**
- **What:** New product releases create hype spikes
- **Examples:**
  - Air Jordan 1 Retro "Chicago" (2.0× for 2 weeks)
  - Air Jordan 11 "Concord" (2.5× for 1 week)
  - Limited collabs (3.0× for 3 days)
- **Pattern:** Sharp spike, gradual decay
- **Frequency:** 6-10 drops per year

**Visual Options:**
1. **Event markers on timeline:**
   - Green triangles for drop dates
   - Demand curve shows spike + decay
   - Hover shows sneaker image + name
2. **Manim animation:**
   - Show exponential decay curve
   - Formula: `drop_t = exp(-0.15 * days_since)`
   - Visualize multiple overlapping drops

**Preferred:** Interactive timeline with sneaker images

---

### Slide 9: Promotional Windows
**Component:** `PromoSlide.vue` (NEW)
**Background:** Vanta Net
**Content:**
- **What:** Planned discount periods drive volume
- **Examples:**
  - Summer sale: 20% off → 1.4× demand
  - End-of-season clearance: 30% off → 1.7× demand
  - Friends & Family: 15% off → 1.3× demand
- **Duration:** 1-2 weeks
- **Frequency:** 12-15 promos per year

**Visual:**
- Calendar heat map showing promo windows (colored blocks)
- Demand multiplier shown as height/intensity
- Animate promos lighting up over time

**Enhancement:** Show discount % → demand multiplier relationship (curve)

---

### Slide 10: Price Elasticity
**Component:** `PriceElasticitySlide.vue` (NEW)
**Background:** Morphing Dots
**Content:**
- **What:** Price changes affect demand
- **Formula:** `price_mult = (price / list_price) ^ β`
- **Elasticity:** β = -1.2 (elastic: 10% price cut → 12% demand increase)
- **Range:** $140 - $210 (±20% from $180 MSRP)

**Visual Options:**
1. **Curve showing price vs demand:**
   - X-axis: Price ($)
   - Y-axis: Demand multiplier
   - Show tangent line illustrating elasticity
2. **Interactive slider:**
   - Drag price slider
   - Watch demand bar adjust in real-time
3. **Manim animation:**
   - Animate along the elasticity curve
   - Show "inelastic" vs "elastic" regions

**Preferred:** Interactive slider (most engaging for executive)

---

### Slide 11: Hype Signal (with Convolution!)
**Component:** `HypeSignalSlide.vue` (NEW)
**Background:** Vanta Fog
**Content:**
- **What:** Social media buzz predicts future demand
- **Sources:** Instagram mentions, Google Trends, resale prices
- **Lead time:** 14 days (hype builds before purchase)
- **Convolution:** Impulse response spreads hype over time
- **Formula:** `demand_t = Σ hype_{t-k} × IR_k`

**Visual - THE STAR SLIDE:**
1. **Manim convolution animation** (transparent background):
   - Top: Raw hype signal (spiky)
   - Middle: Impulse response kernel sliding across
   - Bottom: Convolved output (smoothed demand effect)
   - Show the sliding window + multiplication + sum
2. **After animation:**
   - Show 3-panel comparison:
     - Raw hype (green line)
     - Impulse response (gaussian curve)
     - Resulting demand (blue line, lagged)

**Technical:**
- Use the `/videos/ConvolutionAnimation.webm` we already created
- Add pause/replay controls
- Show equation below video

**This is the money slide** - convolution is hard to understand, visualization makes it click!

---

### Slide 12: Marketing Effect (with Convolution!)
**Component:** `MarketingEffectSlide.vue` (EXISTS - enhance with convolution)
**Background:** Surface Lines
**Content:**
- **What:** Ad spend drives demand with delay
- **Channels:** Facebook ads, Instagram sponsored posts, TV commercials
- **Lead time:** 7 days (shorter than hype, more immediate)
- **Budget:** $50K - $200K per week
- **ROI:** 1.2× - 1.8× demand multiplier

**Visual - SECOND CONVOLUTION SLIDE:**
- Same convolution animation structure as hype
- Different impulse response (faster decay, 7-day kernel)
- Color code differently (marketing = purple vs hype = green)
- Side-by-side comparison showing 7-day vs 14-day lag

**Enhancement:**
- Interactive: let user adjust ad spend, see demand response
- Show cost per incremental unit sold

---

### Slide 13: Traffic Signal
**Component:** `TrafficSlide.vue` (NEW)
**Background:** Tentacle
**Content:**
- **What:** Foot traffic (stores) + web sessions (online)
- **Relationship:** Contemporaneous (traffic = sales, same day)
- **Range:** 500 - 2000 visitors/day
- **Correlation:** 0.85 with demand

**Visual:**
- Dual Y-axis chart:
  - Left axis: Traffic (orange line)
  - Right axis: Demand (blue line)
  - Show tight correlation
- Animate both lines drawing together
- Highlight correlation coefficient

**Enhancement:** Scatter plot showing traffic vs demand (strong linear fit)

---

### Slide 14: Competitor Events
**Component:** `CompetitorEventsSlide.vue` (NEW)
**Background:** Vanta Birds
**Content:**
- **What:** When Adidas/New Balance drops hot sneakers, we lose sales
- **Impact:** -10% to -30% during competitor launch week
- **Examples:**
  - Yeezy drop: -25% for 1 week
  - New Balance 990v6: -15% for 5 days
- **Frequency:** 6-8 events per year

**Visual:**
- Timeline showing:
  - Our demand (blue line, baseline)
  - Competitor events (red down-arrows)
  - Demand dips (shaded red zones)
- Show competitor logos at event times

**Enhancement:** Animate "market share battle" with flowing particles

---

### Slide 15: Weather Effects
**Component:** `WeatherEffectsSlide.vue` (NEW)
**Background:** Vanta Clouds (fitting!)
**Content:**
- **What:** Weather affects foot traffic (online less affected)
- **Impact:**
  - Rain/snow: -10% (people stay home)
  - Extreme heat: -5% (mall avoidance)
  - Nice weather: +5% (shopping trips)
- **Variance:** 5-15% swing

**Visual Options:**
1. **Weather icons + demand curve:**
   - Overlay weather icons (☀️ 🌧️ ❄️) on timeline
   - Color-code demand: gray (rain), yellow (sun)
2. **Manim animation:**
   - Show baseline demand
   - Add weather "noise" layer
   - Show final wiggle

**Preferred:** Weather icons on timeline (intuitive for executive)

---

### Slide 16: Viral Moments
**Component:** `ViralMomentsSlide.vue` (NEW)
**Background:** Perlin Noise (morphing)
**Content:**
- **What:** Unexpected social media events cause demand explosions
- **Examples:**
  - Celebrity spotted in Jordans: +150% for 1 week
  - TikTok trend: +200% for 2 weeks
  - Meme goes viral: +80% for 3 days
- **Unpredictable:** Random timing, massive impact

**Visual:**
- Timeline with "lightning bolt" viral events
- Show demand erupting (volcano visualization?)
- Each event has unique trajectory (fast spike, slow decay)

**Enhancement:**
- Animate viral spread (particle explosion)
- Show social media engagement metric (hearts, retweets)

---

## Act 3: How The Pieces Combine (2 slides)

### Slide 17: Multiplicative Composition
**Component:** `MultiplicativeCompositionSlide.vue` (NEW)
**Background:** Vanta Net
**Content:**
- **Formula:**
```
demand_t = baseline_t
         × weekly_t
         × yearly_t
         × holiday_t
         × drop_t
         × promo_t
         × price_mult_t
         × hype_t
         × marketing_t
         × traffic_t
         × competitor_t
         × weather_t
         × viral_t
         × noise_t
```
- **Why multiplicative?** Components interact (weekend + holiday = 1.25 × 1.8 = 2.25×)
- **Alternative:** Additive models don't capture interactions

**Visual:**
1. **Animated equation build-up:**
   - Start with baseline
   - Multiply by weekly (show wave appear)
   - Multiply by yearly (wave gets seasonal)
   - Continue adding components one-by-one
   - Each step shows partial result
2. **Manim animation:**
   - Show operators (×) appearing
   - Highlight each component
   - Build final curve layer by layer

**Preferred:** Manim animation (mathematical elegance)

---

### Slide 18: All Components Stacked
**Component:** `ComponentsStackSlide.vue` (EXISTS - enhance)
**Background:** Data Sphere
**Content:**
- **Visual:** Stacked area chart showing all 13 components
- **Layers (bottom to top):**
  1. Baseline (gray)
  2. Weekly (blue)
  3. Yearly (orange)
  4. Holidays (red spikes)
  5. Drops (green spikes)
  6. Promos (purple bands)
  7. Price (pink variance)
  8. Hype (light green)
  9. Marketing (light purple)
  10. Traffic (yellow)
  11. Competitors (red dips)
  12. Weather (light gray)
  13. Viral (lightning yellow)
  14. Noise (transparency)

**Enhancement:**
- Interactive: toggle components on/off
- Show final demand line on top
- Highlight any component to see its contribution
- Play "build-up" animation

---

## Act 4: Classical Forecasting - Prophet (6 slides)

### Slide 19: What is Prophet?
**Component:** `WhatIsProphetSlide.vue` (NEW)
**Background:** Vanta Waves
**Content:**
- **Origin:** Developed by Facebook (Meta) in 2017
- **Purpose:** Business time series forecasting at scale
- **Use cases:** Daily active users, revenue, inventory
- **Why "Prophet"?** Predicts the future (tongue-in-cheek)
- **Open source:** Python & R libraries

**Visual:**
- Facebook/Meta logo
- Prophet logo (if available)
- Timeline: 2017 → 2025 (adoption curve)
- Quote: "We want the forecast to be interpretable and easy to use"

**Enhancement:** Show Prophet's GitHub stars over time (popularity)

---

### Slide 20: Prophet's Three Components
**Component:** `ProphetComponentsSlide.vue` (NEW)
**Background:** Morphing Dots
**Content:**
- **Prophet decomposes time series into:**
  1. **Trend (g(t)):** Long-term growth (linear or logistic)
  2. **Seasonality (s(t)):** Periodic patterns (Fourier series)
  3. **Holidays (h(t)):** Irregular events (one-time spikes)
  4. **Error (ε):** Residual noise

- **Formula:** `y(t) = g(t) + s(t) + h(t) + ε_t`

- **Perfect match for our data!** We built the data the same way

**Visual:**
1. **Three-panel decomposition:**
   - Top: Trend (smooth line)
   - Middle: Seasonality (repeating waves)
   - Bottom: Holidays (spikes)
   - Final: All combined
2. **Manim animation:**
   - Show components adding together (literally, with + signs)
   - Build final curve

**Preferred:** Manim animation showing additive composition

---

### Slide 21: How Prophet Learns - Fourier Features
**Component:** `ProphetFourierSlide.vue` (NEW)
**Background:** Surface Lines
**Content:**
- **Challenge:** How to represent seasonality mathematically?
- **Solution:** Fourier series (sum of sine/cosine waves)
- **Formula:**
```
s(t) = Σ [aₙ cos(2πnt/P) + bₙ sin(2πnt/P)]
```
- **Intuition:** Any periodic pattern = sum of simple waves
- **Prophet learns:** Coefficients (aₙ, bₙ) from data

**Visual - TECHNICAL DEEP DIVE:**
1. **Manim animation (★ MONEY SLIDE):**
   - Start with flat line
   - Add 1st harmonic (annual sine wave)
   - Add 2nd harmonic (6-month cycle)
   - Add 3rd harmonic (4-month cycle)
   - Continue adding harmonics
   - Show how sum approximates complex seasonal pattern
   - Overlay: actual Air Jordan yearly seasonality

2. **Interactive demo:**
   - Sliders for each harmonic amplitude
   - User can adjust to see effect
   - Show equation updating

**This explains the "magic" - great for technical executive**

---

### Slide 22: How Prophet Learns - Changepoints
**Component:** `ProphetChangepointsSlide.vue` (NEW)
**Background:** Distorted Cube
**Content:**
- **Challenge:** Trends change over time (not always linear)
- **Solution:** Piecewise linear trends with automatic changepoint detection
- **Example:** Air Jordan demand growth rate increases in 2023 (TikTok effect)
- **Prophet automatically finds:** Where trend shifts
- **Regularization:** Penalizes too many changepoints (avoid overfitting)

**Visual:**
1. **Demand curve with changepoints marked:**
   - Show 6-year trend
   - Mark changepoints (vertical dashed lines)
   - Show slope change at each point
2. **Manim animation:**
   - Draw piecewise linear trend
   - Show how slope changes at changepoints
   - Contrast with single linear fit (poor) vs piecewise (good)

**Enhancement:** Interactive: drag changepoints, see fit improve/degrade

---

### Slide 23: Prophet's Forecast
**Component:** `ProphetForecastSlide.vue` (EXISTS - enhance)
**Background:** Vanta Fog
**Content:**
- **What:** Prophet predicts future demand with uncertainty
- **Output:**
  - Point forecast (yhat): Most likely value
  - Uncertainty intervals: 80% and 95% confidence bands
- **Horizon:** 90 days ahead (3 months)

**Visual:**
- Line chart:
  - Historical data (blue dots)
  - Prophet forecast (blue line)
  - 80% interval (dark blue band)
  - 95% interval (light blue band)
- Animate forecast "unrolling" into future

**Enhancement:**
- Show multiple scenarios (optimistic/pessimistic)
- Highlight: "80% of time, actual demand falls in dark blue band"

---

### Slide 24: Why Prophet Works Here
**Component:** `WhyProphetWorksSlide.vue` (NEW)
**Background:** Perlin Noise
**Content:**
- **Advantages for shoe demand:**
  1. ✅ **Handles seasonality natively** (Fourier series)
  2. ✅ **Holiday effects built-in** (no feature engineering)
  3. ✅ **Uncertainty quantification** (confidence intervals)
  4. ✅ **Interpretable components** (can explain to execs)
  5. ✅ **No lag features needed** (unlike ML models)
  6. ✅ **Robust to missing data** (doesn't crash)

- **When Prophet struggles:**
  - Complex interactions between features (ML better)
  - Non-seasonal, noisy data (ARIMA might win)
  - Very short history (not enough data to learn)

**Visual:**
- Checkmark list (animated)
- Comparison table: Prophet vs XGBoost vs ARIMA
- Show "sweet spot" diagram (when to use what)

---

### Slide 25: Model Comparison
**Component:** `ModelComparisonSlide.vue` (EXISTS - enhance)
**Background:** Vanta Net
**Content:**
- **Models tested:**
  1. Prophet: MAE 27.76 ⭐ **WINNER**
  2. Seasonal Naive: MAE 31.84
  3. ARIMA: MAE 29.45
  4. XGBoost (fixed): MAE 32.19
  5. LightGBM (fixed): MAE 33.67
  6. Naive (baseline): MAE 35.12
  7. Linear Regression: MAE 34.89

- **Metrics explained:**
  - MAE = Mean Absolute Error (avg error in shoes/day)
  - Lower is better

**Visual:**
- Horizontal bar chart (MAE on X-axis, models on Y-axis)
- Prophet bar highlighted (gold)
- Animate bars growing from left
- Show "error reduction vs naive" percentage

**Enhancement:** Click model to see its forecast plot

---

## Act 5: Reality & Results (3 slides)

### Slide 26: Inventory Constraints
**Component:** `InventoryRealitySlide.vue` (EXISTS)
**Background:** Vanta Clouds
**Content:** (keep existing - already good)

---

### Slide 27: The Data Leakage Lesson
**Component:** `DataLeakageSlide.vue` (EXISTS - enhance)
**Background:** Distorted Cube
**Content:**
- **Story:** First benchmark results looked incredible!
  - XGBoost: MAE 12.34 (too good to be true)
  - LightGBM: MAE 13.67 (also suspicious)
- **Problem:** Models were "peeking at the future"
  - Using lag features computed on full dataset
  - Validation not respecting time order
- **Fix:** Walk-forward validation + proper lag calculation
- **Result:** Accuracy dropped 50% → **honest evaluation**
- **Lesson:** Always validate like production (no future info!)

**Visual:**
- Split screen:
  - Left: "Data Leakage" (model peeking over wall at future)
  - Right: "Proper Validation" (model only sees past)
- Animate before/after results

**Enhancement:** Show diagram of walk-forward splits vs wrong approach

---

### Slide 28: Call to Action
**Component:** `DiveDeeperSlide.vue` (EXISTS)
**Background:** Vanta Waves
**Content:** (keep existing)

---

## Act 6: Modern Approaches (Extension - 4-6 slides)

### Slide 29: Beyond Classical Methods
**Component:** `BeyondClassicalSlide.vue` (NEW)
**Background:** Vanta Birds
**Content:**
- **Classical methods (Prophet, ARIMA):** Hand-crafted features, statistical models
- **Modern approaches:** Neural networks learn patterns automatically
- **When to go modern:**
  - Very long sequences (years of daily data)
  - Complex multivariate interactions
  - Need to model non-linear relationships
- **Trade-offs:**
  - (+) Can capture subtle patterns
  - (−) Less interpretable ("black box")
  - (−) Need more data & compute
  - (−) Harder to debug

**Visual:**
- Timeline: Statistical methods (1970s) → ML (2000s) → Deep Learning (2010s) → Foundation models (2020s)
- Show "complexity vs interpretability" curve

---

### Slide 30: Neural Networks for Time Series
**Component:** `NeuralTimeSeriesSlide.vue` (NEW)
**Background:** Vanta Net
**Content:**
- **Key architectures:**
  1. **RNN/LSTM:** Recurrent networks (memory of past)
  2. **CNN:** 1D convolutions (local patterns)
  3. **Transformers:** Attention mechanism (global context)
  4. **N-BEATS:** Pure architecture for forecasting
  5. **TimeGPT:** Foundation model (pre-trained on millions of series)

- **How they work:**
  - Input: Historical sequence (e.g., last 90 days)
  - Output: Future sequence (e.g., next 30 days)
  - Learn: Patterns, seasonality, trends automatically

**Visual:**
1. **Neural network diagram:**
   - Show input layer (time series)
   - Hidden layers (abstract)
   - Output layer (forecast)
   - Animate data flowing through
2. **Manim animation:**
   - Show LSTM "memory cell" remembering patterns
   - Show attention mechanism "focusing" on relevant history

**Preferred:** Interactive network diagram (hover shows activations)

---

### Slide 31: TimeGPT - Foundation Model for Time Series
**Component:** `TimeGPTSlide.vue` (NEW)
**Background:** Perlin Noise
**Content:**
- **What:** Pre-trained transformer model (like GPT, but for time series)
- **Training:** 100+ million time series from diverse domains
- **Zero-shot forecasting:** Works on new series without fine-tuning
- **API-based:** Nixtla provides cloud service
- **Performance:** Often beats classical + custom ML

**Key innovation:** Transfer learning for time series
- GPT learned language from billions of documents
- TimeGPT learned "temporal patterns" from millions of series
- Can generalize to shoe demand (never seen before!)

**Visual:**
1. **Show TimeGPT architecture:**
   - Transformer blocks
   - Pre-training data sources (weather, sales, traffic, etc.)
   - Fine-tuning on Air Jordan data
2. **Comparison chart:**
   - Prophet: MAE 27.76
   - TimeGPT: MAE ~25-30 (estimated)
   - Show training time difference (Prophet: 5 sec, TimeGPT: pre-trained)

**Enhancement:** Live API demo (if feasible)

---

### Slide 32: Gradient Boosting for Time Series
**Component:** `GradientBoostingTimeSeriesSlide.vue` (NEW)
**Background:** Surface Lines
**Content:**
- **Models:** XGBoost, LightGBM, CatBoost
- **How they work:**
  - Ensemble of decision trees
  - Each tree corrects errors of previous trees
  - Final prediction = weighted sum of all trees

- **For time series:**
  - Need engineered features: lags, rolling stats, date features
  - Don't handle seasonality natively (vs Prophet)
  - Excel at complex interactions (price × promo × weather)

- **Our results:**
  - XGBoost (with proper lags): MAE 32.19
  - Worse than Prophet (27.76)
  - Why? Prophet designed for this problem

- **When boosting wins:**
  - Rich exogenous features (price, promotions, weather)
  - Cross-sectional data (forecasting 1000s of SKUs)
  - Non-seasonal patterns

**Visual:**
1. **Decision tree diagram:**
   - Show tree splitting on features
   - Animate boosting process (tree 1 → tree 2 → tree 3)
2. **Feature importance chart:**
   - Show which features XGBoost learned were important
   - lag_7, lag_14, holiday, promo, etc.

**Enhancement:** Interactive tree explorer (click to see splits)

---

### Slide 33: The Modern Toolkit - When to Use What
**Component:** `ModernToolkitSlide.vue` (NEW)
**Background:** Vanta Fog
**Content:**
- **Decision framework:**

```
                             START
                               |
                    Is data seasonal/cyclical?
                         /            \
                       YES             NO
                        |               |
                   Use Prophet      Use ARIMA
                        |          or Boosting
                        |
            Do you have rich features?
                  /         \
                YES          NO
                 |            |
          Try XGBoost    Stick with
          + Prophet      Prophet
                 |            |
                 |            |
        Is data very long (years)?
                 |
               YES
                 |
        Try TimeGPT / N-BEATS
```

- **Rules of thumb:**
  - Prophet: 1 year+ data, clear seasonality, need interpretability
  - XGBoost: Rich features, non-seasonal, cross-sectional
  - TimeGPT: Long series, want SOTA, OK with black box
  - ARIMA: Short-term, stable, simple

**Visual:**
- Flowchart (interactive, can click through)
- Each node links to example use case

---

### Slide 34: What We Built Today
**Component:** `WhatWeBuiltSlide.vue` (NEW)
**Background:** Vanta Waves
**Content:**
- **Recap:**
  1. ✅ Synthetic Air Jordan demand (13 components)
  2. ✅ Convolution animations (hype + marketing lag)
  3. ✅ Prophet forecasting (27.76 MAE)
  4. ✅ Model comparison (7 algorithms)
  5. ✅ Data leakage lesson (validation matters!)
  6. ✅ Modern approaches (TimeGPT, boosting)

- **Vibe coding in action:**
  - Python (data generation)
  - Manim (mathematical animations)
  - Vue 3 + Slidev (interactive slides)
  - Vanta.js (WebGL backgrounds)
  - ECharts (interactive charts)

- **Key takeaway:** Modern forecasting = classical stats + ML + deep learning

**Visual:**
- Grid of slide thumbnails (mosaic)
- Highlight key visuals (convolution, Fourier, changepoints)
- Show tech stack logos

---

## Visual Asset Requirements

### Manim Animations Needed:
1. ✅ **Convolution** (already have `/videos/ConvolutionAnimation.webm`)
2. **Fourier series build-up** (slide 21) - PRIORITY
3. **Multiplicative composition** (slide 17)
4. **Additive Prophet components** (slide 20)
5. **Changepoints** (slide 22)
6. **LSTM memory cell** (slide 30) - optional
7. **Attention mechanism** (slide 30) - optional

### JavaScript Interactions Needed:
1. **Price elasticity slider** (slide 10) - PRIORITY
2. **Component toggle** (slide 18) - PRIORITY
3. **Model comparison drill-down** (slide 25)
4. **Walk-forward validation diagram** (slide 27)
5. **Decision tree explorer** (slide 32) - optional

### Chart Types Needed:
- Line charts: All component slides
- Area charts: Stacked components (slide 18)
- Bar charts: Model comparison (slide 25)
- Scatter plots: Price elasticity (slide 10), Traffic correlation (slide 13)
- Timeline: Holidays, drops, competitors
- Heatmaps: Promo calendar (slide 9)

---

## Technical Implementation Notes

### Background Assignment Strategy:
- **Vanta Waves:** Title, smooth flows (Prophet intro)
- **Vanta Net:** Data connections, networks
- **Vanta Clouds:** Weather, soft topics
- **Vanta Fog:** Uncertainty, forecasting
- **Vanta Birds:** Competition, market dynamics
- **Perlin Noise:** Mathematical elegance (Fourier, formulas)
- **Data Sphere:** Components overview
- **Morphing Dots:** Transitions
- **Surface Lines:** Marketing, signals
- **Distorted Cube:** Disruption, problems
- **Tentacle:** Traffic, organic flow

### Component Reuse:
- `TwoColumnSlide.vue` for text + chart layouts
- `AnimatedTimeline.vue` for temporal events
- Chart components from ComponentsStack can be extracted

### Animation Timing:
- Keep under 10 seconds per animation
- Add pause/replay controls for Manim videos
- Use GSAP for JS animations (smooth, controllable)

---

## Next Steps

1. **Create missing slide components** (slides 2-3, 7-16, 19-28, 29-34)
2. **Build Manim animations:**
   - Fourier series (PRIORITY)
   - Multiplicative composition
   - Prophet components
3. **Implement interactive features:**
   - Price slider
   - Component toggles
   - Model drill-downs
4. **Update slides.md** with new structure
5. **Test flow & pacing** (aim for 20-30 min presentation)
6. **Add speaker notes** for each slide
7. **Polish typography** (Tympanus fonts)
8. **Test on production build** (GitHub Pages)

---

## Estimated Timeline

- **Phase 1:** Core synthetic data slides (4-16) - 4 hours
- **Phase 2:** Prophet explanation slides (19-25) - 3 hours
- **Phase 3:** Manim animations - 4 hours
- **Phase 4:** Interactive features - 3 hours
- **Phase 5:** Modern approaches extension (29-34) - 3 hours
- **Phase 6:** Polish & testing - 2 hours

**Total:** ~19 hours of focused work

---

## Success Metrics

- ✅ Landlord says "I learned something new about forecasting"
- ✅ Landlord asks technical questions (engagement)
- ✅ Smooth presentation (no bugs, fast loads)
- ✅ Visual "wow" moments (convolution, Fourier, backgrounds)
- ✅ Clear narrative arc (problem → solution → modern future)
