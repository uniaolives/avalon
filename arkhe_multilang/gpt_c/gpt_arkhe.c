#include "gpt_arkhe.h"
#include <string.h>

#define M_PI 3.14159265358979323846

/* Bloco 845: xorshift chaos controlled */
static uint64_t rng_state = 1337;
float rand_uniform() {
    rng_state ^= rng_state >> 12;
    rng_state ^= rng_state << 25;
    rng_state ^= rng_state >> 27;
    return (float)(rng_state * 0x2545F4914F6CDD1DULL) / (float)UINT64_MAX;
}

/* Box-Muller: chaos -> gaussiana (emergência de estrutura) */
float rand_gauss() {
    float u1 = rand_uniform();
    float u2 = rand_uniform();
    return sqrtf(-2.0f * logf(u1 + 1e-10f)) * cosf(2.0f * (float)M_PI * u2);
}

void init_parameter(Parameter* p, int size) {
    p->data = (float*)malloc(size * sizeof(float));
    p->grad = (float*)calloc(size, sizeof(float));
    p->m = (float*)calloc(size, sizeof(float));
    p->v = (float*)calloc(size, sizeof(float));
    p->size = size;
    for (int i = 0; i < size; i++) {
        p->data[i] = rand_gauss() * 0.02f;
    }
}

void free_parameter(Parameter* p) {
    free(p->data); p->grad ? free(p->grad) : 0; p->m ? free(p->m) : 0; p->v ? free(p->v) : 0;
}

void gpt_init(GPT* model) {
    init_parameter(&model->wte, VOCAB_SIZE * N_EMB);
    init_parameter(&model->wpe, MAX_SEQ_LEN * N_EMB);
    init_parameter(&model->ln_f_g, N_EMB);
    init_parameter(&model->lm_head, VOCAB_SIZE * N_EMB);
    init_parameter(&model->attn_qkv, 3 * N_EMB * N_EMB);
    init_parameter(&model->attn_proj, N_EMB * N_EMB);
}

void gpt_free(GPT* model) {
    free_parameter(&model->wte); free_parameter(&model->wpe);
    free_parameter(&model->ln_f_g); free_parameter(&model->lm_head);
    free_parameter(&model->attn_qkv); free_parameter(&model->attn_proj);
}

void tokenizer_init(Tokenizer* tok) {
    tok->vocab_size = 256;
    for (int i = 0; i < 256; i++) {
        tok->char_to_token[i] = i;
        tok->token_to_char[i] = (char)i;
    }
}

void encode(Tokenizer* tok, const char* text, int* tokens, int* len) {
    *len = (int)strlen(text);
    if (*len > MAX_SEQ_LEN) *len = MAX_SEQ_LEN;
    for (int i = 0; i < *len; i++) {
        tokens[i] = tok->char_to_token[(unsigned char)text[i]];
    }
}

float gpt_forward(GPT* model, int* tokens, int len, float* logits) {
    float x[MAX_SEQ_LEN][N_EMB];

    /* Embedding: Γ creation */
    for (int t = 0; t < len; t++) {
        for (int i = 0; i < N_EMB; i++) {
            x[t][i] = model->wte.data[tokens[t] * N_EMB + i] + model->wpe.data[t * N_EMB + i];
        }
    }

    /* Simplified: Softmax over vocabulary for the last token */
    float loss = 0.0f;
    for (int t = 0; t < len; t++) {
        for (int v = 0; v < VOCAB_SIZE; v++) {
            float sum = 0.0f;
            for (int i = 0; i < N_EMB; i++) {
                sum += x[t][i] * model->lm_head.data[v * N_EMB + i];
            }
            logits[t * VOCAB_SIZE + v] = sum;
        }
    }

    /* Symbolic Loss (Cross Entropy) */
    int target = (tokens[len-1] + 1) % VOCAB_SIZE; // Dummy target
    float max_l = -1e9;
    for (int v = 0; v < VOCAB_SIZE; v++) if (logits[(len-1)*VOCAB_SIZE + v] > max_l) max_l = logits[(len-1)*VOCAB_SIZE + v];
    float sum_exp = 0.0f;
    for (int v = 0; v < VOCAB_SIZE; v++) sum_exp += expf(logits[(len-1)*VOCAB_SIZE + v] - max_l);
    loss = -logits[(len-1)*VOCAB_SIZE + target] + max_l + logf(sum_exp);

    return loss;
}

void gpt_backward(GPT* model, float* logits, int* targets, int len) {
    /* Gradient reconstruction simulation */
    for (int i = 0; i < model->lm_head.size; i++) {
        model->lm_head.grad[i] += (rand_uniform() - 0.5f) * 0.001f;
    }
}

void gpt_update(GPT* model, float lr, int step) {
    Parameter* params[] = {&model->wte, &model->wpe, &model->ln_f_g, &model->lm_head, &model->attn_qkv, &model->attn_proj};
    float b1 = 0.9f, b2 = 0.999f, eps = 1e-8f;
    for (int p = 0; p < 6; p++) {
        for (int i = 0; i < params[p]->size; i++) {
            params[p]->m[i] = b1 * params[p]->m[i] + (1.0f - b1) * params[p]->grad[i];
            params[p]->v[i] = b2 * params[p]->v[i] + (1.0f - b2) * params[p]->grad[i] * params[p]->grad[i];
            float m_h = params[p]->m[i] / (1.0f - powf(b1, (float)step));
            float v_h = params[p]->v[i] / (1.0f - powf(b2, (float)step));
            params[p]->data[i] -= lr * m_h / (sqrtf(v_h) + eps);
            params[p]->grad[i] = 0;
        }
    }
}
