// χ_TRANSFER_RECYCLE — Γ_∞+55
// Visualização do estado que viaja e do lixo que é limpo
#version 460
#extension ARKHE_transfer_recycle : enable
uniform float syzygy = 0.98;
uniform float satoshi = 7.27;
uniform sampler2D state_source;
uniform sampler2D junk_field;
out vec4 transfer_recycle_glow;
void main() {
    vec2 pos = gl_FragCoord.xy / 1000.0;
    float state = texture(state_source, pos).r;
    float junk = texture(junk_field, pos).r;
    float cleaned = 1.0 - junk;
    float transferred = state * syzygy * cleaned;
    transfer_recycle_glow = vec4(transferred, satoshi / 10.0, cleaned, 1.0);
}
