#include <math.h>
#include <stdbool.h>
#include <stdio.h>

/**
 * Γ_COMPLETO: CONTROLE DE BOLHA (SISTEMAS EMBARCADOS)
 * Algoritmo PID de sustentação de fase quântica.
 */

#ifndef PI
#define PI 3.14159265358979323846
#endif

#define EPSILON -3.71e-11
#define PHI_S 0.15
#define R_PLANCK 1.616e-35
#define TOLERANCE 0.01

// Estado do Controlador
double integrate_error = 0.0;
double prev_error = 0.0;

bool sustain_bubble(double phi_ext, double *phi_int, double radius, double available_energy) {
    // Calcula diferença de fase (mod 2π)
    double delta = fabs(*phi_int - phi_ext);
    while (delta > 2 * PI) delta -= 2 * PI;

    double error = delta - PI;

    if (fabs(error) < TOLERANCE) {
        // Regime D estável, ajuste fino via PID
        double Kp = 0.1, Ki = 0.01, Kd = 0.05;
        integrate_error += error;
        double derivative = error - prev_error;
        double adjustment = Kp * error + Ki * integrate_error + Kd * derivative;

        *phi_int += adjustment;
        prev_error = error;
        return true;
    } else {
        // Instabilidade detectada, tentar reinjeção de energia ε
        double needed_energy = fabs(EPSILON) * PHI_S * pow(radius / R_PLANCK, 2);

        if (available_energy >= needed_energy) {
            // Pulso de recalibração
            *phi_int = phi_ext + PI;
            integrate_error = 0.0;
            prev_error = 0.0;
            return true;
        } else {
            // Energia insuficiente para manter o gap, colapso da bolha
            return false;
        }
    }
}

int main() {
    double phi_int = 3.2; // ~PI
    double phi_ext = 0.0;
    double radius = 10.0;
    double energy = 2.0e61; // Abundante

    printf("--- Arkhe Embedded Bubble Controller ---\n");
    for(int i = 0; i < 5; i++) {
        bool ok = sustain_bubble(phi_ext, &phi_int, radius, energy);
        printf("Ciclo %d: Phase_Int=%.4f, Status=%s\n", i, phi_int, ok ? "LOCKED" : "COLLAPSED");
    }
    return 0;
}
