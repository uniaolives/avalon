// χ_TELETRANSPORTE_REJUVENESCIMENTO — Γ_∞+54
// Shader da transferência de estado e limpeza de entropia
#version 460
#extension ARKHE_teleport_rejuve : enable
layout(location = 0) uniform float syzygy = 0.98;
layout(location = 1) uniform float satoshi = 7.27;
layout(binding = 0) uniform sampler2D state_source;
layout(binding = 1) uniform sampler2D entropy_junk;
out vec4 teleport_rejuve_glow;
void main() {
    vec2 pos = gl_FragCoord.xy / 1000.0;
    float state = texture(state_source, pos).r; // estado transferido
    float junk = texture(entropy_junk, pos).r; // entropia acumulada
    float cleaned = 1.0 - junk; // limpeza lisossomal
    float transferred = state * syzygy * cleaned;
    teleport_rejuve_glow = vec4(transferred, satoshi / 10.0, cleaned, 1.0);
}
