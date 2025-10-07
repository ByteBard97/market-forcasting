<template>
  <canvas ref="canvas" class="constellations-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let gl = null
let program = null
let animationId = null
let startTime = Date.now()
let mouseX = 0.5
let mouseY = 0.5

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
  uniform vec2 iMouse;

  #define S(a, b, t) smoothstep(a, b, t)
  #define NUM_LAYERS 4.0

  float N21(vec2 p) {
    vec3 a = fract(vec3(p.xyx) * vec3(213.897, 653.453, 253.098));
    a += dot(a, a.yzx + 79.76);
    return fract((a.x + a.y) * a.z);
  }

  vec2 GetPos(vec2 id, vec2 offs, float t) {
    float n = N21(id+offs);
    float n1 = fract(n*10.0);
    float n2 = fract(n*100.0);
    float a = t+n;
    return offs + vec2(sin(a*n1), cos(a*n2))*0.4;
  }

  float df_line(in vec2 a, in vec2 b, in vec2 p) {
    vec2 pa = p - a, ba = b - a;
    float h = clamp(dot(pa,ba) / dot(ba,ba), 0.0, 1.0);
    return length(pa - ba * h);
  }

  float line(vec2 a, vec2 b, vec2 uv) {
    float r1 = 0.04;
    float r2 = 0.01;

    float d = df_line(a, b, uv);
    float d2 = length(a-b);
    float fade = S(1.5, 0.5, d2);

    fade += S(0.05, 0.02, abs(d2-0.75));
    return S(r1, r2, d)*fade;
  }

  float NetLayer(vec2 st, float n, float t) {
    vec2 id = floor(st)+n;
    st = fract(st)-0.5;

    // Manually compute all 9 positions
    vec2 p0 = GetPos(id, vec2(-1.0,-1.0), t);
    vec2 p1 = GetPos(id, vec2(0.0,-1.0), t);
    vec2 p2 = GetPos(id, vec2(1.0,-1.0), t);
    vec2 p3 = GetPos(id, vec2(-1.0,0.0), t);
    vec2 p4 = GetPos(id, vec2(0.0,0.0), t);
    vec2 p5 = GetPos(id, vec2(1.0,0.0), t);
    vec2 p6 = GetPos(id, vec2(-1.0,1.0), t);
    vec2 p7 = GetPos(id, vec2(0.0,1.0), t);
    vec2 p8 = GetPos(id, vec2(1.0,1.0), t);

    float m = 0.0;
    float sparkle = 0.0;

    // Manually unroll loop for all connections
    m += line(p4, p0, st);
    m += line(p4, p1, st);
    m += line(p4, p2, st);
    m += line(p4, p3, st);
    m += line(p4, p5, st);
    m += line(p4, p6, st);
    m += line(p4, p7, st);
    m += line(p4, p8, st);

    // Sparkle for all points
    float d0 = length(st-p0);
    float s0 = (0.005/(d0*d0)) * S(1.0, 0.7, d0);
    float pulse0 = sin((fract(p0.x)+fract(p0.y)+t)*5.0)*0.4+0.6;
    s0 *= pow(pulse0, 20.0);
    sparkle += s0;

    float d1 = length(st-p1);
    float s1 = (0.005/(d1*d1)) * S(1.0, 0.7, d1);
    float pulse1 = sin((fract(p1.x)+fract(p1.y)+t)*5.0)*0.4+0.6;
    s1 *= pow(pulse1, 20.0);
    sparkle += s1;

    float d2 = length(st-p2);
    float s2 = (0.005/(d2*d2)) * S(1.0, 0.7, d2);
    float pulse2 = sin((fract(p2.x)+fract(p2.y)+t)*5.0)*0.4+0.6;
    s2 *= pow(pulse2, 20.0);
    sparkle += s2;

    float d3 = length(st-p3);
    float s3 = (0.005/(d3*d3)) * S(1.0, 0.7, d3);
    float pulse3 = sin((fract(p3.x)+fract(p3.y)+t)*5.0)*0.4+0.6;
    s3 *= pow(pulse3, 20.0);
    sparkle += s3;

    float d4 = length(st-p4);
    float s4 = (0.005/(d4*d4)) * S(1.0, 0.7, d4);
    float pulse4 = sin((fract(p4.x)+fract(p4.y)+t)*5.0)*0.4+0.6;
    s4 *= pow(pulse4, 20.0);
    sparkle += s4;

    float d5 = length(st-p5);
    float s5 = (0.005/(d5*d5)) * S(1.0, 0.7, d5);
    float pulse5 = sin((fract(p5.x)+fract(p5.y)+t)*5.0)*0.4+0.6;
    s5 *= pow(pulse5, 20.0);
    sparkle += s5;

    float d6 = length(st-p6);
    float s6 = (0.005/(d6*d6)) * S(1.0, 0.7, d6);
    float pulse6 = sin((fract(p6.x)+fract(p6.y)+t)*5.0)*0.4+0.6;
    s6 *= pow(pulse6, 20.0);
    sparkle += s6;

    float d7 = length(st-p7);
    float s7 = (0.005/(d7*d7)) * S(1.0, 0.7, d7);
    float pulse7 = sin((fract(p7.x)+fract(p7.y)+t)*5.0)*0.4+0.6;
    s7 *= pow(pulse7, 20.0);
    sparkle += s7;

    float d8 = length(st-p8);
    float s8 = (0.005/(d8*d8)) * S(1.0, 0.7, d8);
    float pulse8 = sin((fract(p8.x)+fract(p8.y)+t)*5.0)*0.4+0.6;
    s8 *= pow(pulse8, 20.0);
    sparkle += s8;

    // Additional connections
    m += line(p1, p3, st);
    m += line(p1, p5, st);
    m += line(p7, p5, st);
    m += line(p7, p3, st);

    float sPhase = (sin(t+n)+sin(t*0.1))*0.25+0.5;
    sPhase += pow(sin(t*0.1)*0.5+0.5, 50.0)*5.0;
    m += sparkle*sPhase;

    return m;
  }

  void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    vec2 uv = (fragCoord-iResolution.xy*0.5)/iResolution.y;
    vec2 M = iMouse.xy-0.5;

    float t = iTime*0.1;

    float s = sin(t);
    float c = cos(t);
    mat2 rot = mat2(c, -s, s, c);
    vec2 st = uv*rot;
    M *= rot*2.0;

    float m = 0.0;
    for(float i=0.0; i<1.0; i+=1.0/NUM_LAYERS) {
      float z = fract(t+i);
      float size = mix(15.0, 1.0, z);
      float fade = S(0.0, 0.6, z)*S(1.0, 0.8, z);

      m += fade * NetLayer(st*size-M*z, i, iTime);
    }

    float glow = -uv.y*0.5;

    vec3 baseCol = vec3(s, cos(t*0.4), -sin(t*0.24))*0.4+0.6;
    vec3 col = baseCol*m;
    col += baseCol*glow;

    col *= 1.0-dot(uv,uv);

    gl_FragColor = vec4(col, 1.0);
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
    mouseX = e.clientX / window.innerWidth
    mouseY = e.clientY / window.innerHeight
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
.constellations-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
