#ifndef GPT_ARKHE_H
#define GPT_ARKHE_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* Arkhe GPT Constants */
#define VOCAB_SIZE 256
#define MAX_SEQ_LEN 16
#define N_EMB 32
#define N_HEAD 4
#define HEAD_SIZE (N_EMB / N_HEAD)

typedef struct {
    float* data;
    float* grad;
    float* m; /* Adam first moment */
    float* v; /* Adam second moment */
    int size;
} Parameter;

typedef struct {
    Parameter wte[VOCAB_SIZE]; /* Token embeddings */
    Parameter wpe[MAX_SEQ_LEN]; /* Positional embeddings */
    /* Simplified: Single layer with attention and output projection */
    Parameter qkv_w;
    Parameter proj_w;
    Parameter head_w; /* Language head */
} GPTModel;

/* Function Declarations */
void init_parameter(Parameter* p, int size);
void free_parameter(Parameter* p);
void gpt_init(GPTModel* model);
void gpt_free(GPTModel* model);

float gpt_forward(GPTModel* model, int* tokens, int len, float* logits);
void gpt_backward(GPTModel* model, int* tokens, int len, float* logits, int* targets);
void gpt_update(GPTModel* model, float learning_rate, int step);

#endif /* GPT_ARKHE_H */
