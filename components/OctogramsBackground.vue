<template>
  <canvas ref="canvas" class="octograms-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let gl = null
let program = null
let animationId = null
let startTime = Date.now()

const vertexShaderSource = `
  attribute vec2 position;
  void main() {
    gl_Position = vec4(position, 0.0, 1.0);
  }
`

const fragmentShaderSource = `
  precision highp float;
  uniform vec2 iResolution;
  uniform float iTime;

  float gTime = 0.;
  const float REPEAT = 5.0;

  mat2 rot(float a) {
    float c = cos(a), s = sin(a);
    return mat2(c,s,-s,c);
  }

  float sdBox( vec3 p, vec3 b ) {
    vec3 q = abs(p) - b;
    return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
  }

  float box(vec3 pos, float scale) {
    pos *= scale;
    float base = sdBox(pos, vec3(.4,.4,.1)) /1.5;
    pos.xy *= 5.;
    pos.y -= 3.5;
    pos.xy *= rot(.75);
    float result = -base;
    return result;
  }

  float box_set(vec3 pos, float iTime) {
    vec3 pos_origin = pos;
    pos = pos_origin;
    pos.y += sin(gTime * 0.4) * 2.5;
    pos.xy *= rot(.8);
    float box1 = box(pos,2. - abs(sin(gTime * 0.4)) * 1.5);
    pos = pos_origin;
    pos.y -=sin(gTime * 0.4) * 2.5;
    pos.xy *= rot(.8);
    float box2 = box(pos,2. - abs(sin(gTime * 0.4)) * 1.5);
    pos = pos_origin;
    pos.x +=sin(gTime * 0.4) * 2.5;
    pos.xy *= rot(.8);
    float box3 = box(pos,2. - abs(sin(gTime * 0.4)) * 1.5);
    pos = pos_origin;
    pos.x -=sin(gTime * 0.4) * 2.5;
    pos.xy *= rot(.8);
    float box4 = box(pos,2. - abs(sin(gTime * 0.4)) * 1.5);
    pos = pos_origin;
    pos.xy *= rot(.8);
    float box5 = box(pos,.5) * 6.;
    pos = pos_origin;
    float box6 = box(pos,.5) * 6.;
    float result = max(max(max(max(max(box1,box2),box3),box4),box5),box6);
    return result;
  }

  float map(vec3 pos, float iTime) {
    vec3 pos_origin = pos;
    float box_set1 = box_set(pos, iTime);
    return box_set1;
  }

  void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    vec2 p = (fragCoord.xy * 2. - iResolution.xy) / min(iResolution.x, iResolution.y);
    vec3 ro = vec3(0., -0.2 ,iTime * 4.);
    vec3 ray = normalize(vec3(p, 1.5));
    ray.xy = ray.xy * rot(sin(iTime * .03) * 5.);
    ray.yz = ray.yz * rot(sin(iTime * .05) * .2);
    float t = 0.1;
    vec3 col = vec3(0.);
    float ac = 0.0;

    for (int i = 0; i < 99; i++){
      vec3 pos = ro + ray * t;
      pos = mod(pos-2., 4.) -2.;
      gTime = iTime - float(i) * 0.01;

      float d = map(pos, iTime);

      d = max(abs(d), 0.01);
      ac += exp(-d*23.);

      t += d* 0.55;
    }

    col = vec3(ac * 0.02);
    col += vec3(0.,0.2 * abs(sin(iTime)),0.5 + sin(iTime) * 0.2);

    gl_FragColor = vec4(col, 1.0 - t * (0.02 + 0.02 * sin(iTime)));
  }
`

function createShader(gl, type, source) {
  const shader = gl.createShader(type)
  gl.shaderSource(shader, source)
  gl.compileShader(shader)

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error('Shader compilation error:', gl.getShaderInfoLog(shader))
    gl.deleteShader(shader)
    return null
  }

  return shader
}

function createProgram(gl, vertexShader, fragmentShader) {
  const program = gl.createProgram()
  gl.attachShader(program, vertexShader)
  gl.attachShader(program, fragmentShader)
  gl.linkProgram(program)

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error('Program linking error:', gl.getProgramInfoLog(program))
    return null
  }

  return program
}

onMounted(() => {
  gl = canvas.value.getContext('webgl')

  if (!gl) {
    console.error('WebGL not supported')
    return
  }

  canvas.value.width = window.innerWidth
  canvas.value.height = window.innerHeight

  const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource)
  const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource)
  program = createProgram(gl, vertexShader, fragmentShader)

  const positionBuffer = gl.createBuffer()
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer)
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1,
    1, -1,
    -1, 1,
    1, 1
  ]), gl.STATIC_DRAW)

  const positionLocation = gl.getAttribLocation(program, 'position')
  gl.enableVertexAttribArray(positionLocation)
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0)

  const iResolutionLocation = gl.getUniformLocation(program, 'iResolution')
  const iTimeLocation = gl.getUniformLocation(program, 'iTime')

  function render() {
    const currentTime = (Date.now() - startTime) / 1000

    gl.viewport(0, 0, canvas.value.width, canvas.value.height)
    gl.useProgram(program)

    gl.uniform2f(iResolutionLocation, canvas.value.width, canvas.value.height)
    gl.uniform1f(iTimeLocation, currentTime)

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4)

    animationId = requestAnimationFrame(render)
  }

  render()

  const handleResize = () => {
    canvas.value.width = window.innerWidth
    canvas.value.height = window.innerHeight
  }

  window.addEventListener('resize', handleResize)

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.octograms-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
