<template>
  <canvas ref="canvas" class="data-sphere-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'

const canvas = ref(null)
let renderer, scene, camera, galaxy, wrap, segments
let mouse = new THREE.Vector2(-100, -100)
let raycaster, dotsGeometry, segmentsGeom
let attributePositions, attributeSizes
let animationId
let mouseMoveHandler, resizeHandler
let rotationSpeedY = 0.001
let rotationSpeedX = 0.0004

const colors = [
  new THREE.Color(0xac1122),
  new THREE.Color(0x96789f),
  new THREE.Color(0x535353)
]

// Register cleanup BEFORE async operations
onUnmounted(() => {
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
  }
  if (dotsGeometry) {
    dotsGeometry.dispose()
  }
  if (segmentsGeom) {
    segmentsGeom.dispose()
  }
})

onMounted(async () => {
  const width = window.innerWidth
  const height = window.innerHeight

  // Setup renderer
  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true
  })
  renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1)
  renderer.setSize(width, height)
  renderer.setClearColor(0x000000, 0)

  // Setup scene
  scene = new THREE.Scene()

  // Setup raycaster
  raycaster = new THREE.Raycaster()
  raycaster.params.Points.threshold = 6

  // Setup camera
  camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 2000)
  camera.position.set(0, 0, 350)

  galaxy = new THREE.Group()
  scene.add(galaxy)

  // Load texture
  const loader = new THREE.TextureLoader()
  const dotTexture = await new Promise((resolve) => {
    loader.load('/dotTexture.png', resolve)
  })

  // Create dots
  const dotsAmount = 3000
  dotsGeometry = new THREE.BufferGeometry()
  const positions = new Float32Array(dotsAmount * 3)
  const sizes = new Float32Array(dotsAmount)
  const colorsAttribute = new Float32Array(dotsAmount * 3)
  const vertices = []

  for (let i = 0; i < dotsAmount; i++) {
    const vector = new THREE.Vector3()

    vector.color = Math.floor(Math.random() * colors.length)
    vector.theta = Math.random() * Math.PI * 2
    vector.phi = (1 - Math.sqrt(Math.random())) * Math.PI / 2 * (Math.random() > 0.5 ? 1 : -1)

    vector.x = Math.cos(vector.theta) * Math.cos(vector.phi)
    vector.y = Math.sin(vector.phi)
    vector.z = Math.sin(vector.theta) * Math.cos(vector.phi)
    vector.multiplyScalar(120 + (Math.random() - 0.5) * 5)
    vector.scaleX = 5

    // Store original normalized position for pulsation
    vector.nx = vector.x
    vector.ny = vector.y
    vector.nz = vector.z
    const length = Math.sqrt(vector.nx * vector.nx + vector.ny * vector.ny + vector.nz * vector.nz)
    vector.nx /= length
    vector.ny /= length
    vector.nz /= length

    if (Math.random() > 0.5) {
      moveDot(vector, i, positions)
    }

    vertices.push(vector)
    vector.toArray(positions, i * 3)
    colors[vector.color].toArray(colorsAttribute, i * 3)
    sizes[i] = 5
  }

  function moveDot(vector, index, positions) {
    const tempVector = vector.clone()
    tempVector.multiplyScalar((Math.random() - 0.5) * 0.2 + 1)
    gsap.to(vector, {
      duration: Math.random() * 3 + 3,
      x: tempVector.x,
      y: tempVector.y,
      z: tempVector.z,
      yoyo: true,
      repeat: -1,
      delay: -Math.random() * 3,
      ease: 'none',
      onUpdate: () => {
        positions[index * 3] = vector.x
        positions[index * 3 + 1] = vector.y
        positions[index * 3 + 2] = vector.z
      }
    })
  }

  attributePositions = new THREE.BufferAttribute(positions, 3)
  dotsGeometry.setAttribute('position', attributePositions)
  attributeSizes = new THREE.BufferAttribute(sizes, 1)
  dotsGeometry.setAttribute('size', attributeSizes)
  const attributeColors = new THREE.BufferAttribute(colorsAttribute, 3)
  dotsGeometry.setAttribute('color', attributeColors)

  const shaderMaterial = new THREE.ShaderMaterial({
    uniforms: {
      pointTexture: { value: dotTexture }
    },
    vertexShader: `
      attribute float size;
      attribute vec3 color;
      varying vec3 vColor;
      void main() {
        vColor = color;
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = size * (350.0 / -mvPosition.z);
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

  wrap = new THREE.Points(dotsGeometry, shaderMaterial)
  scene.add(wrap)

  // Create segments
  segmentsGeom = new THREE.BufferGeometry()
  const segmentPositions = []
  const segmentColors = []
  const segmentIndices = [] // Store pairs of vertex indices

  for (let i = vertices.length - 1; i >= 0; i--) {
    const vector = vertices[i]
    for (let j = vertices.length - 1; j >= 0; j--) {
      if (i !== j && vector.distanceTo(vertices[j]) < 12) {
        segmentPositions.push(vector.x, vector.y, vector.z)
        segmentPositions.push(vertices[j].x, vertices[j].y, vertices[j].z)
        const col = colors[vector.color]
        segmentColors.push(col.r, col.g, col.b)
        segmentColors.push(col.r, col.g, col.b)
        // Store which vertices this segment connects
        segmentIndices.push([i, j])
      }
    }
  }

  segmentsGeom.setAttribute('position', new THREE.Float32BufferAttribute(segmentPositions, 3))
  segmentsGeom.setAttribute('color', new THREE.Float32BufferAttribute(segmentColors, 3))
  segmentsGeom.segmentIndices = segmentIndices

  const segmentsMat = new THREE.LineBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.3,
    vertexColors: true
  })

  segments = new THREE.LineSegments(segmentsGeom, segmentsMat)
  galaxy.add(segments)

  // Store vertices for raycasting
  dotsGeometry.vertices = vertices

  // Animation loop
  let hovered = []
  let prevHovered = []
  let pulseTime = 0

  function render() {
    pulseTime += 0.02
    const pulseScale = 1 + Math.sin(pulseTime) * 0.05

    // Update vertex positions for pulsation
    for (let i = 0; i < vertices.length; i++) {
      const vertex = vertices[i]
      const baseX = vertex.nx * 120
      const baseY = vertex.ny * 120
      const baseZ = vertex.nz * 120

      vertex.x = baseX * pulseScale
      vertex.y = baseY * pulseScale
      vertex.z = baseZ * pulseScale

      attributePositions.array[i * 3] = vertex.x
      attributePositions.array[i * 3 + 1] = vertex.y
      attributePositions.array[i * 3 + 2] = vertex.z
    }

    // Update segment positions to match pulsating dots
    const segmentPositions = segmentsGeom.attributes.position
    for (let i = 0; i < segmentsGeom.segmentIndices.length; i++) {
      const [idx1, idx2] = segmentsGeom.segmentIndices[i]
      const v1 = vertices[idx1]
      const v2 = vertices[idx2]

      segmentPositions.array[i * 6] = v1.x
      segmentPositions.array[i * 6 + 1] = v1.y
      segmentPositions.array[i * 6 + 2] = v1.z
      segmentPositions.array[i * 6 + 3] = v2.x
      segmentPositions.array[i * 6 + 4] = v2.y
      segmentPositions.array[i * 6 + 5] = v2.z
    }
    segmentPositions.needsUpdate = true

    raycaster.setFromCamera(mouse, camera)
    const intersections = raycaster.intersectObjects([wrap])
    hovered = []

    if (intersections.length) {
      for (let i = 0; i < intersections.length; i++) {
        const index = intersections[i].index
        hovered.push(index)
        if (prevHovered.indexOf(index) === -1) {
          onDotHover(index)
        }
      }
    }

    for (let i = 0; i < prevHovered.length; i++) {
      if (hovered.indexOf(prevHovered[i]) === -1) {
        mouseOut(prevHovered[i])
      }
    }

    prevHovered = hovered.slice(0)
    attributeSizes.needsUpdate = true
    attributePositions.needsUpdate = true

    // Random walk for rotation speeds
    rotationSpeedY += (Math.random() - 0.5) * 0.00005
    rotationSpeedX += (Math.random() - 0.5) * 0.00002

    // Clamp speeds to reasonable ranges
    rotationSpeedY = Math.max(-0.003, Math.min(0.003, rotationSpeedY))
    rotationSpeedX = Math.max(-0.002, Math.min(0.002, rotationSpeedX))

    galaxy.rotation.y += rotationSpeedY
    galaxy.rotation.x += rotationSpeedX

    renderer.render(scene, camera)
    animationId = requestAnimationFrame(render)
  }

  function onDotHover(index) {
    const vertex = vertices[index]
    if (vertex.tl) vertex.tl.kill()
    vertex.tl = gsap.to(vertex, {
      duration: 1,
      scaleX: 10,
      ease: 'elastic.out(2, 0.2)',
      onUpdate: () => {
        attributeSizes.array[index] = vertex.scaleX
      }
    })
  }

  function mouseOut(index) {
    const vertex = vertices[index]
    if (vertex.tl) vertex.tl.kill()
    vertex.tl = gsap.to(vertex, {
      duration: 0.4,
      scaleX: 5,
      ease: 'power2.out',
      onUpdate: () => {
        attributeSizes.array[index] = vertex.scaleX
      }
    })
  }

  function onMouseMove(e) {
    const canvasBounding = canvas.value.getBoundingClientRect()
    mouse.x = ((e.clientX - canvasBounding.left) / width) * 2 - 1
    mouse.y = -((e.clientY - canvasBounding.top) / height) * 2 + 1
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

  render()
})
</script>

<style scoped>
.data-sphere-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
