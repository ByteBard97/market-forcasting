import { defineAppSetup } from "@slidev/types";

// Import slide components from slides/ folder
import TitleSlide from "../slides/TitleSlide.vue";
import SyntheticDataSlide from "../slides/SyntheticDataSlide.vue";
import BaselineSlide from "../slides/BaselineSlide.vue";
import WeeklySeasonalitySlide from "../slides/WeeklySeasonalitySlide.vue";
import YearlySeasonalitySlide from "../slides/YearlySeasonalitySlide.vue";
import ImpulseResponseSlide from "../slides/ImpulseResponseSlide.vue";
import MarketingEffectSlide from "../slides/MarketingEffectSlide.vue";
import SeasonalPatternsSlide from "../slides/SeasonalPatternsSlide.vue";
import TimelineSlide from "../slides/TimelineSlide.vue";
import ComponentsStackSlide from "../slides/ComponentsStackSlide.vue";
import PredictionsSlide from "../slides/PredictionsSlide.vue";
import ModelComparisonSlide from "../slides/ModelComparisonSlide.vue";
import FirstResultsSlide from "../slides/FirstResultsSlide.vue";
import DataLeakageSlide from "../slides/DataLeakageSlide.vue";
import AfterFixingSlide from "../slides/AfterFixingSlide.vue";
import RealisticScenarioSlide from "../slides/RealisticScenarioSlide.vue";
import FinalResultsSlide from "../slides/FinalResultsSlide.vue";
import EnhancedRealismSlide from "../slides/EnhancedRealismSlide.vue";
import ProphetForecastSlide from "../slides/ProphetForecastSlide.vue";
import InventoryRealitySlide from "../slides/InventoryRealitySlide.vue";
import WhatWeLearnedSlide from "../slides/WhatWeLearnedSlide.vue";
import DiveDeeperSlide from "../slides/DiveDeeperSlide.vue";

// Import component library from components/ folder
import SlideLayout from "../components/SlideLayout.vue";
import TwoColumnSlide from "../components/TwoColumnSlide.vue";
import DataSphereBackground from "../components/DataSphereBackground.vue";
import MorphingDotsBackground from "../components/MorphingDotsBackground.vue";
import PerlinNoiseBackground from "../components/PerlinNoiseBackground.vue";
import SurfaceLinesBackground from "../components/SurfaceLinesBackground.vue";
import DistortedCubeBackground from "../components/DistortedCubeBackground.vue";
import TentacleBackground from "../components/TentacleBackground.vue";
import AnimatedBackground from "../components/AnimatedBackground.vue";
import DemandOverviewChart from "../components/DemandOverviewChart.vue";
import ComponentsChart from "../components/ComponentsChart.vue";
import ModelComparisonChart from "../components/ModelComparisonChart.vue";
import ForecastCone from "../components/ForecastCone.vue";
import AnimatedTimeline from "../components/AnimatedTimeline.vue";
import ComponentsStack from "../components/ComponentsStack.vue";
import ModelBars from "../components/ModelBars.vue";
import ModelPredictions from "../components/ModelPredictions.vue";

export default defineAppSetup(({ app }) => {
  // Register slide components from slides/ folder
  app.component("TitleSlide", TitleSlide);
  app.component("SyntheticDataSlide", SyntheticDataSlide);
  app.component("BaselineSlide", BaselineSlide);
  app.component("WeeklySeasonalitySlide", WeeklySeasonalitySlide);
  app.component("YearlySeasonalitySlide", YearlySeasonalitySlide);
  app.component("ImpulseResponseSlide", ImpulseResponseSlide);
  app.component("MarketingEffectSlide", MarketingEffectSlide);
  app.component("SeasonalPatternsSlide", SeasonalPatternsSlide);
  app.component("TimelineSlide", TimelineSlide);
  app.component("ComponentsStackSlide", ComponentsStackSlide);
  app.component("PredictionsSlide", PredictionsSlide);
  app.component("ModelComparisonSlide", ModelComparisonSlide);
  app.component("FirstResultsSlide", FirstResultsSlide);
  app.component("DataLeakageSlide", DataLeakageSlide);
  app.component("AfterFixingSlide", AfterFixingSlide);
  app.component("RealisticScenarioSlide", RealisticScenarioSlide);
  app.component("FinalResultsSlide", FinalResultsSlide);
  app.component("EnhancedRealismSlide", EnhancedRealismSlide);
  app.component("ProphetForecastSlide", ProphetForecastSlide);
  app.component("InventoryRealitySlide", InventoryRealitySlide);
  app.component("WhatWeLearnedSlide", WhatWeLearnedSlide);
  app.component("DiveDeeperSlide", DiveDeeperSlide);

  // Register supporting components from components/ folder
  app.component("SlideLayout", SlideLayout);
  app.component("TwoColumnSlide", TwoColumnSlide);

  // Register chart components
  app.component("DemandOverviewChart", DemandOverviewChart);
  app.component("ComponentsChart", ComponentsChart);
  app.component("ModelComparisonChart", ModelComparisonChart);
  app.component("ForecastCone", ForecastCone);
  app.component("AnimatedTimeline", AnimatedTimeline);
  app.component("ComponentsStack", ComponentsStack);
  app.component("ModelBars", ModelBars);
  app.component("ModelPredictions", ModelPredictions);

  // Register background components
  app.component("DataSphereBackground", DataSphereBackground);
  app.component("MorphingDotsBackground", MorphingDotsBackground);
  app.component("PerlinNoiseBackground", PerlinNoiseBackground);
  app.component("SurfaceLinesBackground", SurfaceLinesBackground);
  app.component("DistortedCubeBackground", DistortedCubeBackground);
  app.component("TentacleBackground", TentacleBackground);
  app.component("AnimatedBackground", AnimatedBackground);
});
