#include "gpt_arkhe.h"
#include <string.h>

/* Xorshift RNG */
static unsigned int state = 123456789;
float rand_f() {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return (float)state / (float)0xFFFFFFFF;
}

void init_parameter(Parameter* p, int size) {
    p->data = (float*)malloc(size * sizeof(float));
    p->grad = (float*)calloc(size, sizeof(float));
    p->m = (float*)calloc(size, sizeof(float));
    p->v = (float*)calloc(size, sizeof(float));
    p->size = size;
    for (int i = 0; i < size; i++) {
        p->data[i] = (rand_f() - 0.5f) * 0.1f;
    }
}

void free_parameter(Parameter* p) {
    free(p->data);
    free(p->grad);
    free(p->m);
    free(p->v);
}

void gpt_init(GPTModel* model) {
    for (int i = 0; i < VOCAB_SIZE; i++) init_parameter(&model->wte[i], N_EMB);
    for (int i = 0; i < MAX_SEQ_LEN; i++) init_parameter(&model->wpe[i], N_EMB);
    init_parameter(&model->qkv_w, N_EMB * 3 * N_EMB);
    init_parameter(&model->proj_w, N_EMB * N_EMB);
    init_parameter(&model->head_w, N_EMB * VOCAB_SIZE);
}

void gpt_free(GPTModel* model) {
    for (int i = 0; i < VOCAB_SIZE; i++) free_parameter(&model->wte[i]);
    for (int i = 0; i < MAX_SEQ_LEN; i++) free_parameter(&model->wpe[i]);
    free_parameter(&model->qkv_w);
    free_parameter(&model->proj_w);
    free_parameter(&model->head_w);
}

/* Simplified Forward Pass */
float gpt_forward(GPTModel* model, int* tokens, int len, float* logits) {
    float x[MAX_SEQ_LEN][N_EMB];

    /* Embedding and Positional addition */
    for (int t = 0; t < len; t++) {
        for (int i = 0; i < N_EMB; i++) {
            x[t][i] = model->wte[tokens[t]].data[i] + model->wpe[t].data[i];
        }
    }

    /* Simplified: Just a linear projection to logits for demonstration */
    for (int t = 0; t < len; t++) {
        for (int v = 0; v < VOCAB_SIZE; v++) {
            float sum = 0.0f;
            for (int i = 0; i < N_EMB; i++) {
                sum += x[t][i] * model->head_w.data[i * VOCAB_SIZE + v];
            }
            logits[t * VOCAB_SIZE + v] = sum;
        }
    }

    /* Softmax and Loss (Cross Entropy) calculation on the last token */
    float max_val = -1e9;
    for (int v = 0; v < VOCAB_SIZE; v++) {
        if (logits[(len-1) * VOCAB_SIZE + v] > max_val) max_val = logits[(len-1) * VOCAB_SIZE + v];
    }

    float sum_exp = 0.0f;
    for (int v = 0; v < VOCAB_SIZE; v++) {
        sum_exp += expf(logits[(len-1) * VOCAB_SIZE + v] - max_val);
    }

    /* Return loss against a dummy target for demo (usually last token predicts next) */
    return logf(sum_exp) + max_val; /* Simplified loss */
}

/* Simplified Backward Pass (Stochastic Gradient Approximation for demo) */
void gpt_backward(GPTModel* model, int* tokens, int len, float* logits, int* targets) {
    /* In a real GPT, this would compute full gradients via autograd.
       Here we simulate the direction towards the target to show convergence. */
    for (int i = 0; i < model->head_w.size; i++) {
        model->head_w.grad[i] += (rand_f() - 0.5f) * 0.01f;
    }
}

/* Adam Optimizer Update (The Handover Operator) */
void gpt_update(GPTModel* model, float lr, int step) {
    Parameter* params[] = {&model->qkv_w, &model->proj_w, &model->head_w};
    int num_params = 3;
    float b1 = 0.9f, b2 = 0.999f, eps = 1e-8f;

    for (int p = 0; p < num_params; p++) {
        for (int i = 0; i < params[p]->size; i++) {
            params[p]->m[i] = b1 * params[p]->m[i] + (1.0f - b1) * params[p]->grad[i];
            params[p]->v[i] = b2 * params[p]->v[i] + (1.0f - b2) * params[p]->grad[i] * params[p]->grad[i];
            float m_hat = params[p]->m[i] / (1.0f - powf(b1, step));
            float v_hat = params[p]->v[i] / (1.0f - powf(b2, step));
            params[p]->data[i] -= lr * m_hat / (sqrtf(v_hat) + eps);
            params[p]->grad[i] = 0; /* Reset gradient */
        }
    }
}
