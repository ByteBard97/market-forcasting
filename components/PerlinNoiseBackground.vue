<template>
  <canvas ref="canvas" class="perlin-noise-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'
import { createNoise3D } from 'simplex-noise'

const canvas = ref(null)
let renderer, scene, camera, shape, geometry
let mouse = new THREE.Vector2(0.8, 0.5)
let animationId
const noise = createNoise3D()

onMounted(() => {
  const width = window.innerWidth
  const height = window.innerHeight

  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true
  })
  renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1)
  renderer.setSize(width, height)
  renderer.setClearColor(0xA9E7DA)

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(100, width / height, 0.1, 10000)
  camera.position.set(120, 0, 300)

  const light = new THREE.HemisphereLight(0xffffff, 0x0C056D, 0.6)
  scene.add(light)

  const light2 = new THREE.DirectionalLight(0x590D82, 0.5)
  light2.position.set(200, 300, 400)
  scene.add(light2)

  const light3 = light2.clone()
  light3.position.set(-200, 300, 400)
  scene.add(light3)

  geometry = new THREE.IcosahedronGeometry(100, 64)  // More subdivisions for smoother blob

  // Store original positions
  const positionAttribute = geometry.attributes.position
  const originalPositions = new Float32Array(positionAttribute.array.length)
  for (let i = 0; i < positionAttribute.array.length; i++) {
    originalPositions[i] = positionAttribute.array[i]
  }
  geometry.userData.originalPositions = originalPositions

  const material = new THREE.MeshPhongMaterial({
    color: 0x23f660,
    emissive: 0x0B4F30,
    emissiveIntensity: 0.2,
    shininess: 90,
    specular: 0x33ff88
  })

  shape = new THREE.Mesh(geometry, material)
  scene.add(shape)

  function updateVertices(a) {
    const positionAttribute = geometry.attributes.position
    const originalPositions = geometry.userData.originalPositions

    for (let i = 0; i < positionAttribute.count; i++) {
      const x = originalPositions[i * 3]
      const y = originalPositions[i * 3 + 1]
      const z = originalPositions[i * 3 + 2]

      const perlin = noise(
        (x * 0.004) + (a * 0.0003),
        (y * 0.004) + (a * 0.0004),
        (z * 0.004) + (a * 0.0002)
      )

      // More dramatic deformation
      const ratio = ((perlin * 0.6 * (mouse.y + 0.3)) + 0.9)

      positionAttribute.array[i * 3] = x * ratio
      positionAttribute.array[i * 3 + 1] = y * ratio
      positionAttribute.array[i * 3 + 2] = z * ratio
    }

    positionAttribute.needsUpdate = true
  }

  function render(a) {
    updateVertices(a)
    shape.rotation.y = a * 0.0001
    shape.rotation.x = a * 0.00005
    renderer.render(scene, camera)
    animationId = requestAnimationFrame(render)
  }

  function onMouseMove(e) {
    gsap.to(mouse, {
      duration: 0.8,
      y: (e.clientY / height),
      x: (e.clientX / width),
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

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('resize', onResize)

  render(0)

  onUnmounted(() => {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('resize', onResize)
  })
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    renderer.dispose()
  }
})
</script>

<style scoped>
.perlin-noise-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
