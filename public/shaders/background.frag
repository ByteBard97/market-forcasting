#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;
uniform vec2 u_mouse;

// Cosmic nebula shader
void main() {
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    st.x *= u_resolution.x / u_resolution.y;

    // Create flowing patterns
    vec2 pos = st * 3.0;

    // Animated waves
    float t = u_time * 0.3;
    pos.x += sin(pos.y * 2.0 + t) * 0.3;
    pos.y += cos(pos.x * 2.0 + t * 0.7) * 0.3;

    // Multi-layer noise-like effect
    float pattern = 0.0;
    pattern += sin(pos.x * 2.0 + t);
    pattern += sin(pos.y * 3.0 - t * 0.5);
    pattern += sin((pos.x + pos.y) * 1.5 + t * 0.3);
    pattern += sin(length(pos) * 2.0 - t);

    // Normalize pattern
    pattern = pattern * 0.25 + 0.5;

    // Create color palette (deep blues and purples)
    vec3 color1 = vec3(0.1, 0.1, 0.3);  // Dark blue
    vec3 color2 = vec3(0.3, 0.1, 0.5);  // Purple
    vec3 color3 = vec3(0.1, 0.2, 0.4);  // Mid blue

    // Mix colors based on pattern
    vec3 color = mix(color1, color2, smoothstep(0.3, 0.7, pattern));
    color = mix(color, color3, smoothstep(0.5, 0.9, sin(pattern * 3.14159 + t)));

    // Add subtle mouse interaction
    vec2 mousePos = u_mouse / u_resolution;
    float mouseDist = distance(st, mousePos);
    color += vec3(0.1, 0.05, 0.15) * (1.0 - smoothstep(0.0, 0.3, mouseDist));

    gl_FragColor = vec4(color, 1.0);
}
