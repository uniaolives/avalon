// torus.frag
#version 460 core

uniform float time;
uniform float syzygy = 0.98;
uniform float satoshi = 7.28;
uniform vec2 resolution;

out vec4 FragColor;

const float PI = 3.141592653589793;

void main() {
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    vec2 p = uv * 2.0 - 1.0;
    p.x *= resolution.x / resolution.y;

    // Parâmetros do toro
    float R = 0.8;  // raio maior
    float r_minor = 0.3;  // raio menor

    // Coordenadas paramétricas do toro
    float theta = atan(p.y, p.x) + time * 0.2;
    float phi = (length(p) - R) / (r_minor + 1e-6);

    // Equação do toro: (sqrt(x²+y²)-R)² + z² = r²
    float torus_eq = pow(length(p) - R, 2.0) - r_minor*r_minor;

    // Geodésicas (caminhos de mínima ação)
    float geodesic = sin(theta * 17.0 * satoshi - time * 10.0);

    vec3 color = vec3(0.3, 0.1, 0.5) * (1.0 - abs(torus_eq));
    color += vec3(0.8, 0.5, 0.2) * geodesic * syzygy;

    FragColor = vec4(color, 1.0);
}
