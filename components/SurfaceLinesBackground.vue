<template>
  <canvas ref="canvas" class="surface-lines-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'
import { createNoise3D } from 'simplex-noise'

const canvas = ref(null)
let renderer, scene, camera, sphere
let mouse = new THREE.Vector2(0.8, 0.5)
let animationId
const noise = createNoise3D()

onMounted(() => {
  const width = window.innerWidth
  const height = window.innerHeight

  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true
  })
  renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1)
  renderer.setSize(width, height)
  renderer.setClearColor(0x000000, 0)

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000)
  camera.position.set(0, 0, 350)

  sphere = new THREE.Group()
  scene.add(sphere)

  const material = new THREE.LineBasicMaterial({ color: 0xfe0e55 })
  const linesAmount = 18
  const radius = 100
  const verticesAmount = 50

  for (let j = 0; j < linesAmount; j++) {
    const geometry = new THREE.BufferGeometry()
    const positions = new Float32Array((verticesAmount + 1) * 3)
    const originalPositions = new Float32Array((verticesAmount + 1) * 3)

    geometry.userData = { y: (j / linesAmount) * radius * 2 }

    for (let i = 0; i <= verticesAmount; i++) {
      const x = Math.cos(i / verticesAmount * Math.PI * 2)
      const z = Math.sin(i / verticesAmount * Math.PI * 2)
      positions[i * 3] = x
      positions[i * 3 + 1] = 0
      positions[i * 3 + 2] = z
      originalPositions[i * 3] = x
      originalPositions[i * 3 + 1] = 0
      originalPositions[i * 3 + 2] = z
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geometry.userData.originalPositions = originalPositions
    geometry.userData.verticesAmount = verticesAmount

    const line = new THREE.Line(geometry, material)
    sphere.add(line)
  }

  function updateVertices(a) {
    for (let j = 0; j < sphere.children.length; j++) {
      const line = sphere.children[j]
      const geometry = line.geometry
      const positionAttribute = geometry.attributes.position
      const originalPositions = geometry.userData.originalPositions

      geometry.userData.y += 0.3
      if (geometry.userData.y > radius * 2) {
        geometry.userData.y = 0
      }

      const radiusHeight = Math.sqrt(geometry.userData.y * (2 * radius - geometry.userData.y))

      for (let i = 0; i <= geometry.userData.verticesAmount; i++) {
        const x = originalPositions[i * 3]
        const z = originalPositions[i * 3 + 2]

        const ratio = noise(x * 0.009, z * 0.009 + a * 0.0006, geometry.userData.y * 0.009) * 15

        positionAttribute.array[i * 3] = x * (radiusHeight + ratio)
        positionAttribute.array[i * 3 + 1] = geometry.userData.y - radius
        positionAttribute.array[i * 3 + 2] = z * (radiusHeight + ratio)
      }

      positionAttribute.needsUpdate = true
    }
  }

  function render(a) {
    updateVertices(a)
    renderer.render(scene, camera)
    animationId = requestAnimationFrame(render)
  }

  function onMouseMove(e) {
    mouse.y = e.clientY / window.innerHeight
    gsap.to(sphere.rotation, {
      duration: 2,
      x: mouse.y * 1,
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
.surface-lines-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
