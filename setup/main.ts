import { defineAppSetup } from '@slidev/types'
import DataSphereBackground from '../components/DataSphereBackground.vue'
import MorphingDotsBackground from '../components/MorphingDotsBackground.vue'
import PerlinNoiseBackground from '../components/PerlinNoiseBackground.vue'
import SurfaceLinesBackground from '../components/SurfaceLinesBackground.vue'
import DistortedCubeBackground from '../components/DistortedCubeBackground.vue'
import TentacleBackground from '../components/TentacleBackground.vue'
import AnimatedBackground from '../components/AnimatedBackground.vue'
import DemandOverviewChart from '../components/DemandOverviewChart.vue'
import ComponentsChart from '../components/ComponentsChart.vue'
import ModelComparisonChart from '../components/ModelComparisonChart.vue'
import ForecastCone from '../components/ForecastCone.vue'
import AnimatedTimeline from '../components/AnimatedTimeline.vue'
import ComponentsStack from '../components/ComponentsStack.vue'
import ModelBars from '../components/ModelBars.vue'
import ModelPredictions from '../components/ModelPredictions.vue'
import BackgroundSelector from '../components/BackgroundSelector.vue'

export default defineAppSetup(({ app }) => {
  // Register background components
  app.component('DataSphereBackground', DataSphereBackground)
  app.component('MorphingDotsBackground', MorphingDotsBackground)
  app.component('PerlinNoiseBackground', PerlinNoiseBackground)
  app.component('SurfaceLinesBackground', SurfaceLinesBackground)
  app.component('DistortedCubeBackground', DistortedCubeBackground)
  app.component('TentacleBackground', TentacleBackground)
  app.component('AnimatedBackground', AnimatedBackground)
  app.component('BackgroundSelector', BackgroundSelector)

  // Register chart components
  app.component('DemandOverviewChart', DemandOverviewChart)
  app.component('ComponentsChart', ComponentsChart)
  app.component('ModelComparisonChart', ModelComparisonChart)
  app.component('ForecastCone', ForecastCone)
  app.component('AnimatedTimeline', AnimatedTimeline)
  app.component('ComponentsStack', ComponentsStack)
  app.component('ModelBars', ModelBars)
  app.component('ModelPredictions', ModelPredictions)
})
