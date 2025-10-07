<template>
  <canvas ref="canvas" class="cube-lines-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let gl = null
let program = null
let animationId = null
let startTime = Date.now()
let mouseX = 0
let mouseY = 0

const vertexShaderSource = `
  attribute vec2 position;
  void main() {
    gl_Position = vec4(position, 0.0, 1.0);
  }
`

// Simplified version of the cube_lines shader - focusing on the core visual effect
const fragmentShaderSource = `
  #extension GL_OES_standard_derivatives : enable
  precision highp float;
  uniform vec2 iResolution;
  uniform float iTime;
  uniform vec2 iMouse;

  #define FDIST 0.7
  #define PI 3.1415926
  #define BOXDIMS vec3(0.75, 0.75, 1.25)
  #define IOR 1.33
  #define ROTATION_SPEED 0.8999

  mat3 rotx(float a){float s = sin(a);float c = cos(a);return mat3(vec3(1.0, 0.0, 0.0), vec3(0.0, c, s), vec3(0.0, -s, c));}
  mat3 roty(float a){float s = sin(a);float c = cos(a);return mat3(vec3(c, 0.0, s), vec3(0.0, 1.0, 0.0), vec3(-s, 0.0, c));}
  mat3 rotz(float a){float s = sin(a);float c = cos(a);return mat3(vec3(c, s, 0.0), vec3(-s, c, 0.0), vec3(0.0, 0.0, 1.0 ));}

  vec3 fcos1(vec3 x) {
      #ifdef GL_OES_standard_derivatives
      vec3 w = vec3(fwidth(x.x), fwidth(x.y), fwidth(x.z));
      float lw = length(w);
      if(lw < 0.0001) {
        vec3 tc = vec3(0.0);
        for(int i=0;i<8;i++)
          tc += cos(x + x * float(i-4) * (0.01 * 400.0 / iResolution.y));
        return tc / 8.0;
      }
      return cos(x) * smoothstep(3.14 * 2.0, 0.0, w);
      #else
      return cos(x);
      #endif
  }

  vec3 getColor(vec3 p) {
      p = abs(p);
      p *= 1.25;
      p = 0.5 * p / dot(p, p);

      float t = 0.13 * length(p);
      vec3 col = vec3(0.3, 0.4, 0.5);
      col += 0.12 * fcos1(6.28318 * t * 1.0 + vec3(0.0, 0.8, 1.1));
      col += 0.11 * fcos1(6.28318 * t * 3.1 + vec3(0.3, 0.4, 0.1));
      col += 0.10 * fcos1(6.28318 * t * 5.1 + vec3(0.1, 0.7, 1.1));
      col += 0.10 * fcos1(6.28318 * t * 17.1 + vec3(0.2, 0.6, 0.7));
      col += 0.10 * fcos1(6.28318 * t * 31.1 + vec3(0.1, 0.6, 0.7));
      col += 0.10 * fcos1(6.28318 * t * 65.1 + vec3(0.0, 0.5, 0.8));
      col += 0.10 * fcos1(6.28318 * t * 115.1 + vec3(0.1, 0.4, 0.7));
      col += 0.10 * fcos1(6.28318 * t * 265.1 + vec3(1.1, 1.4, 2.7));
      return clamp(col, 0.0, 1.0);
  }

  float box(in vec3 ro, in vec3 rd, in vec3 r, out vec3 nn, bool entering) {
      rd += 0.0001 * (1.0 - abs(sign(rd)));
      vec3 dr = 1.0 / rd;
      vec3 n = ro * dr;
      vec3 k = r * abs(dr);

      vec3 pin = -k - n;
      vec3 pout = k - n;
      float tin = max(pin.x, max(pin.y, pin.z));
      float tout = min(pout.x, min(pout.y, pout.z));
      if (tin > tout) return -1.0;

      if (entering) {
          nn = -sign(rd) * step(pin.zxy, pin.xyz) * step(pin.yzx, pin.xyz);
      } else {
          nn = sign(rd) * step(pout.xyz, pout.zxy) * step(pout.xyz, pout.yzx);
      }
      return entering ? tin : tout;
  }

  vec3 bgcol(in vec3 rd) {
      return mix(vec3(0.01), vec3(0.336, 0.458, 0.668), 1.0 - pow(abs(rd.z+0.25), 1.3));
  }

  void main() {
      vec2 fragCoord = gl_FragCoord.xy;
      float mouseY = 1.0 * 0.5 * PI;
      float mouseX = -2.0*PI - 0.25*(iTime*ROTATION_SPEED + 53.0);

      vec3 eye = 4.0 * vec3(cos(mouseX) * cos(mouseY), sin(mouseX) * cos(mouseY), sin(mouseY));
      vec3 w = normalize(-eye);
      vec3 up = vec3(0.0, 0.0, 1.0);
      vec3 u = normalize(cross(w, up));
      vec3 v = cross(u, w);

      vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.x;
      vec3 rd = normalize(w * FDIST + uv.x * u + uv.y * v);

      vec3 ni;
      float t = box(eye, rd, BOXDIMS, ni, true);
      vec3 ro = eye + t * rd;

      vec3 col = vec3(0.0);

      if (t > 0.0) {
          vec3 pos = ro;
          vec3 surfaceColor = getColor(pos);

          float R0 = (IOR - 1.0) / (IOR + 1.0);
          R0 *= R0;

          vec3 nr = ni;
          vec3 rdr = reflect(rd, nr);
          vec3 reflcol = bgcol(rdr);

          float fresnel = R0 + (1.0 - R0) * pow(1.0 - dot(-rd, nr), 5.0);
          col = mix(surfaceColor * 0.8, reflcol, pow(fresnel, 1.5));
      } else {
          col = bgcol(rd);
      }

      gl_FragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
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

  // Enable derivatives extension for fwidth support
  gl.getExtension('OES_standard_derivatives')

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
  const iMouseLocation = gl.getUniformLocation(program, 'iMouse')

  function render() {
    const currentTime = (Date.now() - startTime) / 1000

    gl.viewport(0, 0, canvas.value.width, canvas.value.height)
    gl.useProgram(program)

    gl.uniform2f(iResolutionLocation, canvas.value.width, canvas.value.height)
    gl.uniform1f(iTimeLocation, currentTime)
    gl.uniform2f(iMouseLocation, mouseX, mouseY)

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4)

    animationId = requestAnimationFrame(render)
  }

  render()

  const handleResize = () => {
    canvas.value.width = window.innerWidth
    canvas.value.height = window.innerHeight
  }

  const handleMouseMove = (e) => {
    mouseX = e.clientX
    mouseY = e.clientY
  }

  window.addEventListener('resize', handleResize)
  window.addEventListener('mousemove', handleMouseMove)

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('mousemove', handleMouseMove)
  })
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.cube-lines-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
