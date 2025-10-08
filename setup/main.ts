import { defineAppSetup } from "@slidev/types";

// Import slide components from slides/ folder
import TitleSlide from "../slides/TitleSlide.vue";
import BusinessChallengeSlide from "../slides/BusinessChallengeSlide.vue";
import DataProblemSlide from "../slides/DataProblemSlide.vue";
import WaveAdditionSlide from "../slides/WaveAdditionSlide.vue";
import BaselineSlide from "../slides/BaselineSlide.vue";
import WeeklySeasonalitySlide from "../slides/WeeklySeasonalitySlide.vue";
import YearlySeasonalitySlide from "../slides/YearlySeasonalitySlide.vue";
import HolidayEffectsSlide from "../slides/HolidayEffectsSlide.vue";
import DropEventsSlide from "../slides/DropEventsSlide.vue";
import PriceElasticitySlide from "../slides/PriceElasticitySlide.vue";
import MarketingEffectSlide from "../slides/MarketingEffectSlide.vue";
import AdditiveCompositionSlide from "../slides/AdditiveCompositionSlide.vue";
import ComponentsStackSlide from "../slides/ComponentsStackSlide.vue";
import ProphetIntroSlide from "../slides/ProphetIntroSlide.vue";
import ProphetForecastSlide from "../slides/ProphetForecastSlide.vue";
import ModelComparisonSlide from "../slides/ModelComparisonSlide.vue";
import InventoryRealitySlide from "../slides/InventoryRealitySlide.vue";
import HowToUseSlide from "../slides/HowToUseSlide.vue";
import DiveDeeperSlide from "../slides/DiveDeeperSlide.vue";

// Import component library from components/ folder
import SlideLayout from "../components/SlideLayout.vue";
import TwoColumnSlide from "../components/TwoColumnSlide.vue";
import AutoScaleContainer from "../components/AutoScaleContainer.vue";
import AutoFit from "../components/AutoFit.vue";
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
import MetricCell from "../components/MetricCell.vue";
import CellStack from "../components/CellStack.vue";

export default defineAppSetup(({ app }) => {
  // Register slide components from slides/ folder
  app.component("TitleSlide", TitleSlide);
  app.component("BusinessChallengeSlide", BusinessChallengeSlide);
  app.component("DataProblemSlide", DataProblemSlide);
  app.component("WaveAdditionSlide", WaveAdditionSlide);
  app.component("BaselineSlide", BaselineSlide);
  app.component("WeeklySeasonalitySlide", WeeklySeasonalitySlide);
  app.component("YearlySeasonalitySlide", YearlySeasonalitySlide);
  app.component("HolidayEffectsSlide", HolidayEffectsSlide);
  app.component("DropEventsSlide", DropEventsSlide);
  app.component("PriceElasticitySlide", PriceElasticitySlide);
  app.component("MarketingEffectSlide", MarketingEffectSlide);
  app.component("AdditiveCompositionSlide", AdditiveCompositionSlide);
  app.component("ComponentsStackSlide", ComponentsStackSlide);
  app.component("ProphetIntroSlide", ProphetIntroSlide);
  app.component("ProphetForecastSlide", ProphetForecastSlide);
  app.component("ModelComparisonSlide", ModelComparisonSlide);
  app.component("InventoryRealitySlide", InventoryRealitySlide);
  app.component("HowToUseSlide", HowToUseSlide);
  app.component("DiveDeeperSlide", DiveDeeperSlide);

  // Register supporting components from components/ folder
  app.component("SlideLayout", SlideLayout);
  app.component("TwoColumnSlide", TwoColumnSlide);
  app.component("AutoScaleContainer", AutoScaleContainer);
  app.component("AutoFit", AutoFit);

  // Register chart components
  app.component("DemandOverviewChart", DemandOverviewChart);
  app.component("ComponentsChart", ComponentsChart);
  app.component("ModelComparisonChart", ModelComparisonChart);
  app.component("ForecastCone", ForecastCone);
  app.component("AnimatedTimeline", AnimatedTimeline);
  app.component("ComponentsStack", ComponentsStack);
  app.component("ModelBars", ModelBars);
  app.component("ModelPredictions", ModelPredictions);
  app.component("MetricCell", MetricCell);
  app.component("CellStack", CellStack);

  // Register background components
  app.component("DataSphereBackground", DataSphereBackground);
  app.component("MorphingDotsBackground", MorphingDotsBackground);
  app.component("PerlinNoiseBackground", PerlinNoiseBackground);
  app.component("SurfaceLinesBackground", SurfaceLinesBackground);
  app.component("DistortedCubeBackground", DistortedCubeBackground);
  app.component("TentacleBackground", TentacleBackground);
  app.component("AnimatedBackground", AnimatedBackground);
});
