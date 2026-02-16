#ifndef GPT_ARKHE_H
#define GPT_ARKHE_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

/* Arkhe GPT Machine-Level Constants */
#define VOCAB_SIZE 256
#define MAX_SEQ_LEN 16
#define N_EMB 32
#define N_LAYER 2
#define N_HEAD 4

typedef struct {
    float* data;
    float* grad;
    float* m;
    float* v;
    int size;
} Parameter;

typedef struct {
    /* Weights: The Nodes (Γ) */
    Parameter wte;      /* Token embedding table [VOCAB_SIZE, N_EMB] */
    Parameter wpe;      /* Position embedding table [MAX_SEQ_LEN, N_EMB] */
    Parameter ln_f_g;   /* Final Layer Norm [N_EMB] */
    Parameter lm_head;  /* Language model head [VOCAB_SIZE, N_EMB] */

    /* Simplified: Single block parameters for demo */
    Parameter attn_qkv; /* Attention QKV [3 * N_EMB, N_EMB] */
    Parameter attn_proj;/* Attention Proj [N_EMB, N_EMB] */
} GPT;

typedef struct {
    int vocab_size;
    int char_to_token[256];
    char token_to_char[256];
} Tokenizer;

/* Core Functions */
void gpt_init(GPT* model);
void gpt_free(GPT* model);
float gpt_forward(GPT* model, int* tokens, int len, float* logits);
void gpt_backward(GPT* model, float* logits, int* targets, int len);
void gpt_update(GPT* model, float lr, int step);

/* Tokenizer */
void tokenizer_init(Tokenizer* tok);
void encode(Tokenizer* tok, const char* text, int* tokens, int* len);

/* RNG: xorshift + Box-Muller (Bloco 845) */
float rand_uniform();
float rand_gauss();

#endif
