# Air Jordan Demand Forecasting - Slide Deck Outline

## Current Structure (8 slides)

### **Slide 1: Title**
- **What Drives Air Jordan Demand?**
- Subtitle: Understanding the levers behind sneaker sales
- Call to action: Press Space for next page

---

### **Slide 2: The Signal**
- **Title:** The Signal
- **Content:** Air Jordan sales follow predictable patterns—with surprises
- **Visual:** Overview plot (NA DTC segment)
- **Layout:** Two-column (text left, chart right)

---

### **Slide 3: Seasonal Patterns**
- **Title:** Seasonal Patterns
- **Content:** Weekly, monthly, and yearly cycles shape baseline demand
- **Sections:**
  - Yearly Seasonality (summer peaks, holiday surge)
  - Weekly Pattern (weekend traffic drives retail)
- **Layout:** Grid 2 columns
- **Note:** Currently just placeholders, needs actual charts

---

### **Slide 4: Events & Levers**
- **Title:** Events & Levers
- **Content:** Holidays and product drops create demand spikes
- **Visual:** Overview plot showing event markers
- **Key Points:**
  - Red dots = holidays (Black Friday, Christmas)
  - Green triangles = drop events
  - Clear correlation with demand spikes

---

### **Slide 5: How the Pieces Combine**
- **Title:** How the Pieces Combine
- **Content:** Multiplicative composition
- **Formula:** baseline × seasonality × events × promotions
- **Visual:** Components breakdown (9-panel grid)
- **Shows:**
  - Baseline (growing trend)
  - Weekly, yearly seasonality
  - Holiday, promo effects
  - Price elasticity
  - Hype (14d lead), Marketing (7d lead)
  - Traffic

---

### **Slide 6: Prophet Forecast**
- **Title:** Prophet Forecast
- **Content:** Model captures trend + seasonality + holiday effects
- **Metrics (OUTDATED - needs update):**
  - MAE: 19 units/day (WRONG - was from leaky benchmark)
  - MAPE: 76% (WRONG)
  - Coverage: 88% (WRONG)
- **Visual:** Prophet fit with confidence intervals
- **Layout:** Two-column (metrics left, chart right)

---

### **Slide 7: Inventory Reality**
- **Title:** Inventory Reality
- **Content:** Stockouts happen—especially during peaks
- **Visual:** Inventory analysis
- **Shows:**
  - On-hand inventory oscillation
  - Red X marks = stockouts
  - Weekly stockout frequency
- **Key Insight:** Stockouts increase over time as demand grows faster than replenishment

---

### **Slide 8: Call to Action**
- **Title:** Dive Deeper
- **Button:** "Open Interactive Dashboard →"
- **Subtext:** Explore components, run scenarios, compare regions
- **Purpose:** Transition to SPA

---

## **What's Missing / Needs Work:**

### **Critical Updates Needed:**
1. ✅ **Slide 6 metrics are wrong** - based on leaky benchmark
2. ❌ **No model comparison slide** - should show benchmark results
3. ❌ **No explanation of metrics** (MAE, MAPE, Coverage)
4. ❌ **No "journey" story** - the data leakage lesson
5. ❌ **Slide 3 placeholders** - needs actual seasonal charts

### **Content Gaps:**
- No explanation of synthetic data generation
- No segment comparison (NA vs EMEA vs APAC)
- No business recommendations
- No uncertainty quantification explanation

---

## **Proposed New Structure (12-14 slides)**

After we improve the models, add these slides:

### **New Slide A: "The Forecasting Challenge"** (after Slide 5)
- Why forecasting matters for inventory/planning
- The question: Which model works best?
- Preview: We tested 7 different approaches

### **New Slide B: "Model Benchmark"** (after Slide A)
- Table/chart comparing 7 models
- Metrics explained:
  - MAE = average error in shoes/day
  - MAPE = percentage error (scale-independent)
  - Coverage = do confidence intervals work?
- Winner: Prophet (27.76 MAE)

### **New Slide C: "The Data Leakage Lesson"** (after Slide B)
- Story: First results looked too good to be true
- Problem: XGBoost/LightGBM were "cheating" (peeking at future)
- Fix: Walk-forward validation
- Result: Accuracy dropped 50% → honest evaluation
- **Key Learning:** Proper validation is critical

### **New Slide D: "Improving the Forecast"** (after Slide C)
- Journey of improvement:
  - Step 1: Fixed data leakage (MAE: 27.76)
  - Step 2: Added exogenous features to Prophet (MAE: XX)
  - Step 3: Used actual lags for ML (MAE: XX)
  - Step 4: Shorter horizon (MAE: XX)
- Show progress chart

### **Updated Slide 6 → "Best Model: Prophet"**
- Correct metrics from final benchmark
- Why Prophet wins:
  - Designed for business time series
  - Handles seasonality/holidays natively
  - Best uncertainty quantification
  - Doesn't need lag features
- Visual: Prophet fit with intervals

### **New Slide E: "When to Use Which Model"** (optional)
- Prophet: Seasonal business data, need interpretability
- XGBoost/LightGBM: When you have rich features (price, promo, weather)
- ARIMA: Short-term, stable patterns
- Naive: Baseline comparison

---

## **Final Flow (After Improvements):**

1. **Title** - What Drives Air Jordan Demand?
2. **The Signal** - Sales patterns overview
3. **Seasonal Patterns** - Weekly/yearly cycles
4. **Events & Levers** - Holidays & drops
5. **How the Pieces Combine** - Multiplicative composition
6. **The Forecasting Challenge** 🆕 - Why we need models
7. **Model Benchmark** 🆕 - Comparing 7 approaches
8. **The Data Leakage Lesson** 🆕 - The validation story
9. **Improving the Forecast** 🆕 - Journey of improvement
10. **Best Model: Prophet** ✏️ (Updated) - Final results
11. **Inventory Reality** - Stockouts
12. **Dive Deeper** - Call to action

---

## **Next Steps:**

1. ✅ Implement Option 2 (actual lags for ML)
2. ✅ Re-run benchmark
3. ✅ Document improvement journey
4. ✏️ Update slides.md with new structure
5. 📊 Create comparison visualizations
6. 🎨 Add metric explanation graphics
7. 🚀 Build SPA dashboard

---

## **Notes:**

- Keep executive-friendly tone
- Show, don't tell (use visuals)
- Tell a story (problem → journey → solution)
- Emphasize the learning (data leakage lesson is valuable)
- Keep technical details optional/expandable
