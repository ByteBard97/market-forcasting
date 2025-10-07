<template>
  <div class="particles-container">
    <Particles
      id="tsparticles"
      :particlesInit="particlesInit"
      :options="options"
    />
  </div>
</template>

<script setup>
import Particles from "@tsparticles/vue3";
import { loadSlim } from "@tsparticles/slim";

// Initialize tsParticles engine
const particlesInit = async (engine) => {
  await loadSlim(engine);
};

// Will be called when particles container is created
const onParticlesLoaded = async (container) => {
  console.log('Particles container loaded', container);
};

// tsParticles configuration - subtle network effect
const options = {
  background: {
    color: {
      value: 'transparent',
    },
  },
  fpsLimit: 60,
  interactivity: {
    events: {
      onHover: {
        enable: true,
        mode: 'grab',
      },
      onClick: {
        enable: true,
        mode: 'push',
      },
    },
    modes: {
      grab: {
        distance: 140,
        links: {
          opacity: 0.8,
        },
      },
      push: {
        quantity: 4,
      },
    },
  },
  particles: {
    color: {
      value: '#ffffff',
    },
    links: {
      color: '#ffffff',
      distance: 150,
      enable: true,
      opacity: 0.3,
      width: 1,
    },
    move: {
      direction: 'none',
      enable: true,
      outModes: {
        default: 'bounce',
      },
      random: false,
      speed: 1,
      straight: false,
    },
    number: {
      density: {
        enable: true,
        area: 800,
      },
      value: 60,
    },
    opacity: {
      value: 0.5,
    },
    shape: {
      type: 'circle',
    },
    size: {
      value: { min: 1, max: 3 },
    },
  },
  detectRetina: true,
};
</script>

<style scoped>
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}
</style>
