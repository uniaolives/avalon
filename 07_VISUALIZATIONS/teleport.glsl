// χ_TELEPORT — Γ_∞+53
// Visualização da transferência de estado

#version 460
#extension ARKHE_teleport : enable

uniform float syzygy = 0.98;
uniform float satoshi = 7.27;
uniform sampler2D source_state;
uniform sampler2D destination_reconstruction;

out vec4 teleport_glow;

void main() {
    vec2 pos = gl_FragCoord.xy / 1000.0;
    float src = texture(source_state, pos).r;
    float dst = texture(destination_reconstruction, pos).r;
    float fidelity = 1.0 - abs(src - dst);
    teleport_glow = vec4(fidelity, satoshi/10.0, syzygy, 1.0);
}
