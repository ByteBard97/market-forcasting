<template>
  <div id="particles-js" class="particles-container"></div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

let particlesInstance = null

onMounted(() => {
  // Load particles.js from CDN
  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js'
  script.onload = () => {
    // Initialize particles.js with the exact config from the working example
    if (window.particlesJS) {
      window.particlesJS('particles-js', {
        particles: {
          number: {
            value: 80,
            density: {
              enable: true,
              value_area: 800
            }
          },
          color: {
            value: '#ffffff'
          },
          shape: {
            type: 'circle'
          },
          opacity: {
            value: 0.5,
            random: false,
            anim: {
              enable: false
            }
          },
          size: {
            value: 3,
            random: true,
            anim: {
              enable: false
            }
          },
          line_linked: {
            enable: true,
            distance: 150,
            color: '#ffffff',
            opacity: 0.4,
            width: 1
          },
          move: {
            enable: true,
            speed: 2,
            direction: 'none',
            random: false,
            straight: false,
            out_mode: 'out',
            bounce: false,
            attract: {
              enable: false
            }
          }
        },
        interactivity: {
          detect_on: 'canvas',
          events: {
            onhover: {
              enable: true,
              mode: 'repulse'
            },
            onclick: {
              enable: true,
              mode: 'push'
            },
            resize: true
          },
          modes: {
            repulse: {
              distance: 100
            },
            push: {
              particles_nb: 4
            }
          }
        },
        retina_detect: true
      })
    }
  }
  document.head.appendChild(script)
})

onUnmounted(() => {
  // Clean up
  if (window.pJSDom && window.pJSDom.length > 0) {
    window.pJSDom[0].pJS.fn.vendors.destroypJS()
    window.pJSDom = []
  }
})
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
