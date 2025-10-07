import { defineAppSetup } from "@slidev/types";

// Import slide components from slides/ folder
import TitleSlide from "../slides/TitleSlide.vue";
import SyntheticDataSlide from "../slides/SyntheticDataSlide.vue";
import BaselineSlide from "../slides/BaselineSlide.vue";
import WeeklySeasonalitySlide from "../slides/WeeklySeasonalitySlide.vue";
import TimelineSlide from "../slides/TimelineSlide.vue";
import ComponentsStackSlide from "../slides/ComponentsStackSlide.vue";
import ModelComparisonSlide from "../slides/ModelComparisonSlide.vue";
import FinalResultsSlide from "../slides/FinalResultsSlide.vue";

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
  app.component("TimelineSlide", TimelineSlide);
  app.component("ComponentsStackSlide", ComponentsStackSlide);
  app.component("ModelComparisonSlide", ModelComparisonSlide);
  app.component("FinalResultsSlide", FinalResultsSlide);

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
