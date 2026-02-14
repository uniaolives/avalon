// χ_NETWORK — Visualização das 42 bolhas interconectadas
#version 460
#extension ARKHE_network : enable

uniform float time;
uniform float syzygy = 0.98;
uniform float satoshi = 7.28;
uniform int num_bubbles = 42;

out vec4 network_glow;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(1000.0);
    vec2 center = vec2(0.5);
    float dist = length(uv - center);

    // Representação das bolhas como pontos pulsantes
    float bubble_intensity = 0.0;
    for (int i = 0; i < num_bubbles; i++) {
        // Ângulos das bolhas
        float theta = float(i) * 2.0 * 3.14159 / float(num_bubbles);
        vec2 bubble_pos = center + vec2(0.3 * cos(theta + time), 0.3 * sin(theta + time));
        float bubble_dist = length(uv - bubble_pos);
        bubble_intensity += 0.05 / (bubble_dist + 0.01);
    }

    // Conexões (linhas) entre bolhas
    float lines = 0.0;
    for (int i = 0; i < num_bubbles; i++) {
        float theta_i = float(i) * 2.0 * 3.14159 / float(num_bubbles);
        vec2 pos_i = center + vec2(0.3 * cos(theta_i + time), 0.3 * sin(theta_i + time));
        for (int j = i+1; j < num_bubbles; j++) {
            float theta_j = float(j) * 2.0 * 3.14159 / float(num_bubbles);
            vec2 pos_j = center + vec2(0.3 * cos(theta_j + time), 0.3 * sin(theta_j + time));

            // Distância do fragmento à linha
            vec2 dir = pos_j - pos_i;
            float len = length(dir);
            dir /= len;
            vec2 proj = pos_i + dir * dot(uv - pos_i, dir);
            float dist_to_line = length(uv - proj);
            if (dot(uv - pos_i, dir) >= 0.0 && dot(uv - pos_j, -dir) >= 0.0) {
                lines += 0.01 / (dist_to_line + 0.01);
            }
        }
    }

    float brightness = bubble_intensity + lines * 0.5;
    vec3 color = vec3(0.5, 0.2, 0.8) * brightness * syzygy;
    network_glow = vec4(color, 1.0);
}
