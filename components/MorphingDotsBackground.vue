<template>
  <canvas ref="canvas" class="morphing-dots-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'

const canvas = ref(null)
let mouseMoveHandler, resizeHandler
let isVisible = ref(true)
let intersectionObserver = null

// Register cleanup BEFORE async operations
onUnmounted(() => {
  // Kill all GSAP animations
  gsap.killTweensOf('*')

  if (intersectionObserver) {
    intersectionObserver.disconnect()
  }
  if (mouseMoveHandler) {
    window.removeEventListener('mousemove', mouseMoveHandler)
  }
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    renderer.dispose()
    renderer.forceContextLoss()
  }
  if (scene) {
    scene.clear()
  }
  if (canvas.value) {
    canvas.value.width = 0
    canvas.value.height = 0
  }
})
let renderer, scene, camera, dots
let mouse = new THREE.Vector2(0.8, 0.5)
let animationId, attributePositions

onMounted(async () => {
  // Wait for DOM to be fully ready
  await new Promise(resolve => setTimeout(resolve, 100))

  if (!canvas.value) {
    console.warn('MorphingDots canvas not available')
    return
  }

  const width = window.innerWidth
  const height = window.innerHeight

  // Validate dimensions
  if (width <= 0 || height <= 0) {
    console.warn('Invalid viewport dimensions for MorphingDots')
    return
  }

  // Setup renderer
  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true
  })
  renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1)
  renderer.setSize(width, height)
  renderer.setClearColor(0x59c384)

  // Setup scene
  scene = new THREE.Scene()

  // Setup camera
  camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 2000)
  camera.position.set(0, 0, 80)

  // Load texture with proper base URL
  const baseUrl = import.meta.env.BASE_URL || '/'
  const texturePath = `${baseUrl.endsWith('/') ? baseUrl : baseUrl + '/'}dotTexture.png`
  console.log('Loading MorphingDots texture from:', texturePath)

  const loader = new THREE.TextureLoader()
  const dotTexture = await new Promise((resolve, reject) => {
    loader.load(
      texturePath,
      resolve,
      undefined,
      (error) => {
        console.error('Failed to load MorphingDots texture:', error)
        reject(error)
      }
    )
  }).catch(err => {
    console.error('MorphingDots texture load failed')
    return null
  })

  if (!dotTexture) {
    console.warn('MorphingDots texture not loaded, aborting initialization')
    return
  }

  // Create sphere geometry
  const radius = 50
  const sphereGeom = new THREE.IcosahedronGeometry(radius, 5)
  const bufferDotsGeom = new THREE.BufferGeometry()
  const positions = new Float32Array(sphereGeom.attributes.position.array.length)
  const vertices = []

  for (let i = 0; i < sphereGeom.attributes.position.array.length / 3; i++) {
    const x = sphereGeom.attributes.position.array[i * 3]
    const y = sphereGeom.attributes.position.array[i * 3 + 1]
    const z = sphereGeom.attributes.position.array[i * 3 + 2]
    const vector = new THREE.Vector3(x, y, z)
    vertices.push(vector)
    animateDot(i, vector, radius, positions)
    vector.toArray(positions, i * 3)
  }

  function animateDot(index, vector, radius, positions) {
    gsap.to(vector, {
      duration: 4,
      x: 0,
      z: 0,
      ease: 'back.out',
      delay: Math.abs(vector.y / radius) * 2,
      repeat: -1,
      yoyo: true,
      yoyoEase: 'back.out',
      onUpdate: () => {
        positions[index * 3] = vector.x
        positions[index * 3 + 2] = vector.z
      }
    })
  }

  attributePositions = new THREE.BufferAttribute(positions, 3)
  bufferDotsGeom.setAttribute('position', attributePositions)

  const shaderMaterial = new THREE.ShaderMaterial({
    uniforms: {
      pointTexture: { value: dotTexture }
    },
    vertexShader: `
      uniform float size;
      varying vec3 vColor;
      void main() {
        vColor = vec3(1.0);
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = 5.0 * (350.0 / -mvPosition.z);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      uniform sampler2D pointTexture;
      void main() {
        vec4 textureColor = texture2D(pointTexture, gl_PointCoord);
        if (textureColor.a < 0.3) discard;
        vec4 color = vec4(vColor.xyz, 1.0) * textureColor;
        gl_FragColor = color;
      }
    `,
    transparent: true
  })

  dots = new THREE.Points(bufferDotsGeom, shaderMaterial)
  scene.add(dots)

  // Animation loop
  function render() {
    if (!isVisible.value) {
      // Don't continue the loop if not visible
      return
    }
    attributePositions.needsUpdate = true
    renderer.render(scene, camera)
    animationId = requestAnimationFrame(render)
  }

  function onMouseMove(e) {
    mouse.x = (e.clientX / window.innerWidth) - 0.5
    mouse.y = (e.clientY / window.innerHeight) - 0.5
    gsap.to(dots.rotation, {
      duration: 4,
      x: mouse.y * Math.PI * 0.5,
      z: mouse.x * Math.PI * 0.2,
      ease: 'power1.out'
    })
  }

  function onResize() {
    const newWidth = window.innerWidth
    const newHeight = window.innerHeight
    camera.aspect = newWidth / newHeight
    camera.updateProjectionMatrix()
    renderer.setSize(newWidth, newHeight)
  }

  mouseMoveHandler = onMouseMove
  resizeHandler = onResize

  window.addEventListener('mousemove', mouseMoveHandler)
  window.addEventListener('resize', resizeHandler)

  // Set up intersection observer to detect visibility
  intersectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const wasVisible = isVisible.value
      isVisible.value = entry.isIntersecting

      // Start animation when becoming visible
      if (!wasVisible && entry.isIntersecting) {
        render()
      }
    })
  }, { threshold: 0.1 })

  if (canvas.value) {
    intersectionObserver.observe(canvas.value)
  }

  // Start initial render only if visible
  const rect = canvas.value.getBoundingClientRect()
  const inViewport = rect.top < window.innerHeight && rect.bottom > 0
  if (inViewport) {
    render()
  }
})
</script>

<style scoped>
.morphing-dots-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
