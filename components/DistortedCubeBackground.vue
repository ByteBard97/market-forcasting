<template>
  <canvas ref="canvas" class="distorted-cube-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'
import { createNoise3D } from 'simplex-noise'

const canvas = ref(null)
let renderer, scene, camera, cube, geometry
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
  renderer.setClearColor(0x0F1617)

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
  camera.position.set(0, 0, 100)

  geometry = new THREE.BoxGeometry(49, 49, 49, 7, 7, 7)

  // Create checkerboard pattern
  const groups = geometry.groups
  for (let i = 0; i < groups.length; i++) {
    const group = groups[i]
    const start = group.start
    const count = group.count

    for (let j = start; j < start + count; j += 3) {
      const index = geometry.index.array[j]
      const x = geometry.attributes.position.array[index * 3]
      const y = geometry.attributes.position.array[index * 3 + 1]
      const z = geometry.attributes.position.array[index * 3 + 2]

      const cx = Math.floor((x + 24.5) / 7)
      const cy = Math.floor((y + 24.5) / 7)
      const cz = Math.floor((z + 24.5) / 7)

      group.materialIndex = (cx + cy + cz) % 2
    }
  }

  // Store original positions
  const positionAttribute = geometry.attributes.position
  const originalPositions = new Float32Array(positionAttribute.array.length)
  for (let i = 0; i < positionAttribute.array.length; i++) {
    originalPositions[i] = positionAttribute.array[i]
  }
  geometry.userData.originalPositions = originalPositions

  const materials = [
    new THREE.MeshBasicMaterial({
      color: 0x000000,
      transparent: true,
      opacity: 0
    }),
    new THREE.MeshBasicMaterial({
      color: 0x13756a,
      side: THREE.DoubleSide,
      wireframe: true
    })
  ]

  cube = new THREE.Mesh(geometry, materials)
  scene.add(cube)

  gsap.to(cube.rotation, {
    duration: 80,
    y: Math.PI * 2,
    x: Math.PI * 2,
    ease: 'none',
    repeat: -1
  })

  function render(a) {
    const positionAttribute = geometry.attributes.position
    const originalPositions = geometry.userData.originalPositions

    for (let i = 0; i < positionAttribute.count; i++) {
      const x = originalPositions[i * 3]
      const y = originalPositions[i * 3 + 1]
      const z = originalPositions[i * 3 + 2]

      const ratio = noise((x * 0.01), (y * 0.01) + (a * 0.0005), (z * 0.01))
      const scale = 1 + (ratio * 0.1)

      positionAttribute.array[i * 3] = x * scale
      positionAttribute.array[i * 3 + 1] = y * scale
      positionAttribute.array[i * 3 + 2] = z * scale
    }

    positionAttribute.needsUpdate = true
    renderer.render(scene, camera)
    animationId = requestAnimationFrame(render)
  }

  function onResize() {
    const newWidth = window.innerWidth
    const newHeight = window.innerHeight
    camera.aspect = newWidth / newHeight
    camera.updateProjectionMatrix()
    renderer.setSize(newWidth, newHeight)
  }

  window.addEventListener('resize', onResize)

  render(0)

  onUnmounted(() => {
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
.distorted-cube-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
