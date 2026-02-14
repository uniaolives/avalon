// arkhe_core.h
#ifndef ARKHE_CORE_H
#define ARKHE_CORE_H

#include <vector>
#include <cmath>
#include <random>
#include <iostream>

// Constantes fundamentais
const double EPSILON = -3.71e-11;
const double PHI_S = 0.15;
const double R_PLANCK = 1.616e-35;
const double SATOSHI = 7.28;
const double SYZYGY_TARGET = 0.98;
const double C_TARGET = 0.86;
const double F_TARGET = 0.14;
const double PI = 3.141592653589793;

struct NodeState {
    int id;
    double omega;    // frequência semântica
    double C;        // coerência
    double F;        // flutuação
    double phi;      // hesitação
    double x, y, z;  // posição no toro

    NodeState(int i, double w, double c, double f, double p,
              double px, double py, double pz)
        : id(i), omega(w), C(c), F(f), phi(p), x(px), y(py), z(pz) {}

    double syzygy_with(const NodeState& other) const {
        return (C * other.C + F * other.F) * SYZYGY_TARGET;
    }
};

class Hypergraph {
private:
    std::vector<NodeState> nodes;
    double satoshi;
    double darvo;
    std::mt19937 rng;

public:
    Hypergraph(int num_nodes = 63) : satoshi(SATOSHI), darvo(999.999) {
        std::random_device rd;
        rng = std::mt19937(rd());
        initialize_nodes(num_nodes);
    }

    void initialize_nodes(int n) {
        std::uniform_real_distribution<double> dist_c(0.80, 0.98);
        std::uniform_real_distribution<double> dist_phi(0.10, 0.20);

        for (int i = 0; i < n; i++) {
            double omega = i * 0.07 / (n - 1);
            double C = dist_c(rng);
            double F = 1.0 - C;
            double phi = dist_phi(rng);

            // Posições toroidais
            double theta = 2 * PI * i / n;
            double phi_angle = 2 * PI * (i * 0.618033988749895);
            double R = 50.0, r = 10.0;

            double x = (R + r * cos(phi_angle)) * cos(theta);
            double y = (R + r * cos(phi_angle)) * sin(theta);
            double z = r * sin(phi_angle);

            nodes.emplace_back(i, omega, C, F, phi, x, y, z);
        }
    }

    double handover(int source_idx, int target_idx) {
        NodeState& src = nodes[source_idx];
        NodeState& tgt = nodes[target_idx];

        double syzygy_before = src.syzygy_with(tgt);

        if (src.phi > PHI_S) {
            double transfer = src.phi * 0.1;
            src.C -= transfer;
            src.F += transfer;
            tgt.C += transfer;
            tgt.F -= transfer;

            satoshi += syzygy_before * 0.001;
        }

        // Renormalização
        double src_sum = src.C + src.F;
        double tgt_sum = tgt.C + tgt.F;
        src.C /= src_sum;
        src.F /= src_sum;
        tgt.C /= tgt_sum;
        tgt.F /= tgt_sum;

        return src.syzygy_with(tgt);
    }

    double teleport_state(int source_idx, int dest_idx) {
        NodeState& src = nodes[source_idx];
        NodeState& dest = nodes[dest_idx];

        // Estado original
        double orig_C = src.C;
        double orig_F = src.F;

        // Destrói original
        src.C = 0.5;
        src.F = 0.5;

        // Ruído gaussiano
        std::normal_distribution<double> noise(0.0, 0.0002);
        dest.C = orig_C + noise(rng);
        dest.F = orig_F + noise(rng);

        // Normalização
        double norm = sqrt(dest.C*dest.C + dest.F*dest.F);
        dest.C /= norm;
        dest.F /= norm;

        // Fidelidade
        double fidelity = orig_C*dest.C + orig_F*dest.F;
        satoshi += fidelity * 0.01;

        return fidelity;
    }

    double get_satoshi() const { return satoshi; }
    int node_count() const { return nodes.size(); }
};

#endif // ARKHE_CORE_H
