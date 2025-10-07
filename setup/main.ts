import { defineAppSetup } from '@slidev/types'
import GradientBackground from '../components/GradientBackground.vue'
import ParticlesBackground from '../components/ParticlesBackground.vue'
import ShaderBackground from '../components/ShaderBackground.vue'
import DemandOverviewChart from '../components/DemandOverviewChart.vue'
import ComponentsChart from '../components/ComponentsChart.vue'
import ModelComparisonChart from '../components/ModelComparisonChart.vue'
import ForecastCone from '../components/ForecastCone.vue'
import AnimatedTimeline from '../components/AnimatedTimeline.vue'
import ComponentsStack from '../components/ComponentsStack.vue'
import ModelBars from '../components/ModelBars.vue'

export default defineAppSetup(({ app }) => {
  app.component('GradientBackground', GradientBackground)
  app.component('ParticlesBackground', ParticlesBackground)
  app.component('ShaderBackground', ShaderBackground)
  app.component('DemandOverviewChart', DemandOverviewChart)
  app.component('ComponentsChart', ComponentsChart)
  app.component('ModelComparisonChart', ModelComparisonChart)
  app.component('ForecastCone', ForecastCone)
  app.component('AnimatedTimeline', AnimatedTimeline)
  app.component('ComponentsStack', ComponentsStack)
  app.component('ModelBars', ModelBars)
})
