<template>
  <canvas ref="canvas" class="tentacle-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const canvas = ref(null)
let renderer, scene, camera, sphere
let animationId

onMounted(() => {
  const width = window.innerWidth
  const height = window.innerHeight

  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true
  })
  renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1)
  renderer.setSize(width, height)
  renderer.setClearColor(0x191919)

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000)
  camera.position.set(0, 0, 280)

  sphere = new THREE.Group()
  scene.add(sphere)

  const mat1 = new THREE.LineBasicMaterial({ color: 0x4a4a4a })
  const mat2 = new THREE.LineBasicMaterial({ color: 0x3F51B5 })

  const radius = 100
  const lines = 50
  const dots = 50

  for (let i = 0; i < lines; i++) {
    const geometry = new THREE.BufferGeometry()
    const positions = new Float32Array(dots * 3)

    const line = new THREE.Line(geometry, (Math.random() > 0.2) ? mat1 : mat2)
    line.userData.speed = Math.random() * 300 + 250
    line.userData.wave = Math.random()
    line.userData.radius = Math.floor(radius + (Math.random() - 0.5) * (radius * 0.2))

    for (let j = 0; j < dots; j++) {
      const x = ((j / dots) * line.userData.radius * 2) - line.userData.radius
      positions[j * 3] = x
      positions[j * 3 + 1] = 0
      positions[j * 3 + 2] = 0
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))

    line.rotation.x = Math.random() * Math.PI
    line.rotation.y = Math.random() * Math.PI
    line.rotation.z = Math.random() * Math.PI

    sphere.add(line)
  }

  function updateDots(a) {
    for (let i = 0; i < lines; i++) {
      const line = sphere.children[i]
      const geometry = line.geometry
      const positionAttribute = geometry.attributes.position

      for (let j = 0; j < dots; j++) {
        const x = positionAttribute.array[j * 3]
        const ratio = 1 - ((line.userData.radius - Math.abs(x)) / line.userData.radius)
        const y = Math.sin(a / line.userData.speed + j * 0.15) * 12 * ratio
        positionAttribute.array[j * 3 + 1] = y
      }

      positionAttribute.needsUpdate = true
    }
  }

  function render(a) {
    updateDots(a)
    sphere.rotation.y = (a * 0.0001)
    sphere.rotation.x = (-a * 0.0001)
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
.tentacle-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
