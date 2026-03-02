// χ_BUBBLE — Visualização da bolha com fase e redshift
#version 460
#extension ARKHE_bubble : enable

uniform float time;
uniform float syzygy = 0.98;
uniform float satoshi = 7.28;
uniform float epsilon = -3.71e-11;

out vec4 bubble_glow;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(1000.0);
    vec2 p = uv * 2.0 - 1.0;
    float r = length(p);
    float angle = atan(p.y, p.x);

    // Fase da bolha modulada por ε e Satoshi
    float phase = angle + epsilon * time * 1e5;  // amplificado para visualização
    float interference = sin(phase * satoshi) * syzygy;

    // Efeito de redshift: borda escurece com r
    float edge = 1.0 - smoothstep(0.3, 0.8, r);

    // Camada de isolamento (anéis)
    float rings = sin(phase * 42.0) * 0.5 + 0.5;

    vec3 color = vec3(0.2, 0.0, 0.4) + vec3(0.8, 0.6, 0.2) * interference * edge * rings;
    bubble_glow = vec4(color, 1.0);
}
