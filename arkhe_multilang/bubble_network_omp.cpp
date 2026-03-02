// bubble_network_omp.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <utility>

#ifdef _OPENMP
#include <omp.h>
#endif

const double EARTH_RADIUS = 6371000.0;  // metros
const double PI = 3.141592653589793;

struct Bubble {
    int id;
    double x, y, z;
    double state[2];  // [real, imag]
    std::vector<int> entangled_with;

    Bubble(int i, double px, double py, double pz)
        : id(i), x(px), y(py), z(pz) {
        state[0] = 1.0;
        state[1] = 0.0;
    }
};

class BubbleNetwork {
private:
    std::vector<Bubble> bubbles;
    double satoshi;

public:
    BubbleNetwork(int n = 42) : satoshi(7.28) {
        // Distribuição uniforme na esfera
        for (int i = 0; i < n; i++) {
            double theta = 2 * PI * i / n;
            double phi = acos(1 - 2.0 * i / n);

            double x = EARTH_RADIUS * sin(phi) * cos(theta);
            double y = EARTH_RADIUS * sin(phi) * sin(theta);
            double z = EARTH_RADIUS * cos(phi);

            bubbles.emplace_back(i, x, y, z);
        }

        // Emaranhamento completo (mesh)
        for (int i = 0; i < n; i++) {
            for (int j = i+1; j < n; j++) {
                bubbles[i].entangled_with.push_back(j);
                bubbles[j].entangled_with.push_back(i);
            }
        }
    }

    double teleport_parallel(int source_idx, int dest_idx) {
        if (source_idx >= (int)bubbles.size() || dest_idx >= (int)bubbles.size())
            return 0.0;

        Bubble& src = bubbles[source_idx];
        Bubble& dest = bubbles[dest_idx];

        // Estado original
        double orig[2] = {src.state[0], src.state[1]};

        // Destrói original
        src.state[0] = src.state[1] = 0.0;

        // Ruído
        std::random_device rd;
        std::mt19937 gen(rd());
        std::normal_distribution<> noise(0.0, 0.0002);

        dest.state[0] = orig[0] + noise(gen);
        dest.state[1] = orig[1] + noise(gen);

        // Normalização
        double norm = sqrt(dest.state[0]*dest.state[0] + dest.state[1]*dest.state[1]);
        dest.state[0] /= norm;
        dest.state[1] /= norm;

        double fidelity = orig[0]*dest.state[0] + orig[1]*dest.state[1];

        satoshi += fidelity * 0.01;

        return fidelity;
    }

    double global_coherence() {
        double sum = 0.0;
        int count = 0;

        for (int i = 0; i < (int)bubbles.size(); i++) {
            for (int j = i+1; j < (int)bubbles.size(); j++) {
                // Simula syzygy entre bolhas
                double s = (bubbles[i].state[0] * bubbles[j].state[0] +
                           bubbles[i].state[1] * bubbles[j].state[1]) * 0.98;
                sum += s;
                count++;
            }
        }

        return sum / (count + 1e-12);
    }

    double get_satoshi() const { return satoshi; }
};

int main() {
    BubbleNetwork network(42);
    std::cout << "Coerência inicial: " << network.global_coherence() << std::endl;

    // Salto entre várias bolhas
    std::vector<std::pair<int,int>> jumps = {{0,21}, {5,27}, {13,38}, {22,41}};

    for (size_t i = 0; i < jumps.size(); i++) {
        double fid = network.teleport_parallel(jumps[i].first, jumps[i].second);
        std::cout << "Salto " << jumps[i].first << "→" << jumps[i].second
                  << ": fidelidade " << fid << std::endl;
    }

    std::cout << "Coerência final: " << network.global_coherence() << std::endl;
    std::cout << "Satoshi: " << network.get_satoshi() << std::endl;

    return 0;
}
