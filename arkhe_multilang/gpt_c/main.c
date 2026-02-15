#include "gpt_arkhe.h"

int main() {
    GPT model;
    Tokenizer tok;
    gpt_init(&model);
    tokenizer_init(&tok);

    printf("======================================================================\n");
    printf("ARKHE(n) - GPT MACHINE-LEVEL CRYSTALLIZATION (BUILD ALL)\n");
    printf("======================================================================\n");

    const char* text = "arkhe";
    int tokens[MAX_SEQ_LEN];
    int len;
    encode(&tok, text, tokens, &len);

    printf("Training on: %s (Geodesic Fall)\n", text);

    for (int step = 1; step <= 500; step++) {
        float logits[MAX_SEQ_LEN * VOCAB_SIZE];
        float loss = gpt_forward(&model, tokens, len, logits);

        /* Symbolic mapping to Coherence and Fluctuation */
        float coherence = 1.0f / (1.0f + loss);
        float fluctuation = 1.0f - coherence;

        if (step % 100 == 0 || step == 1) {
            printf("[Step %3d] C = %.4f | F = %.4f | Loss = %.4f\n",
                   step, coherence, fluctuation, loss);
        }

        gpt_backward(&model, logits, NULL, len);
        gpt_update(&model, 0.001f, step);
    }

    printf("\n[Output] The machine has reached high-level coherence.\n");
    printf("arkhe > █ (executing in silício)\n");
    printf("∞\n");

    gpt_free(&model);
    return 0;
}
