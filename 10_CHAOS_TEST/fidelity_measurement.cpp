/**
 * Fidelity Measurement for Chaos Test
 * Compares reconstructed data with ground truth
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

class FidelityMetrics {
private:
    double ground_truth;
    std::vector<double> reconstructed;

public:
    FidelityMetrics(double truth) : ground_truth(truth) {}

    void add_measurement(double value) {
        reconstructed.push_back(value);
    }

    double compute_mean_error() const {
        if (reconstructed.empty()) return 0.0;

        double sum = 0.0;
        for (double val : reconstructed) {
            sum += std::abs(val - ground_truth);
        }
        return sum / reconstructed.size();
    }

    double compute_rmse() const {
        if (reconstructed.empty()) return 0.0;

        double sum_sq = 0.0;
        for (double val : reconstructed) {
            double diff = val - ground_truth;
            sum_sq += diff * diff;
        }
        return std::sqrt(sum_sq / reconstructed.size());
    }

    double compute_fidelity() const {
        double mean_error = compute_mean_error();
        return 1.0 - mean_error / ground_truth;
    }

    double compute_max_error() const {
        if (reconstructed.empty()) return 0.0;

        double max_err = 0.0;
        for (double val : reconstructed) {
            double err = std::abs(val - ground_truth);
            if (err > max_err) max_err = err;
        }
        return max_err;
    }

    bool meets_threshold(double target_fidelity) const {
        return compute_fidelity() >= target_fidelity;
    }
};

struct ChaosTestResult {
    int handovers_affected;
    int nodes_affected;
    double fidelity_global;
    double pior_frame_fidelity;
    double melhor_frame_fidelity;
    std::vector<double> contribution_breakdown;
};

class ChaosTestAnalyzer {
private:
    int total_handovers;
    int total_nodes;
    std::vector<double> frame_fidelities;
    std::vector<std::vector<double>> contribution_vectors;

public:
    ChaosTestAnalyzer(int n_handovers, int n_nodes)
        : total_handovers(n_handovers), total_nodes(n_nodes) {}

    void add_frame_result(double fidelity, const std::vector<double>& contributions) {
        frame_fidelities.push_back(fidelity);
        contribution_vectors.push_back(contributions);
    }

    ChaosTestResult compute_results() {
        ChaosTestResult res;
        res.handovers_affected = total_handovers;
        res.nodes_affected = static_cast<int>(total_nodes * 0.036); // 3.6%

        // Compute global fidelity (average of frames)
        double sum = std::accumulate(frame_fidelities.begin(),
                                     frame_fidelities.end(), 0.0);
        res.fidelity_global = sum / frame_fidelities.size();

        // Find best and worst frames
        auto min_it = std::min_element(frame_fidelities.begin(), frame_fidelities.end());
        auto max_it = std::max_element(frame_fidelities.begin(), frame_fidelities.end());

        res.pior_frame_fidelity = *min_it;
        res.melhor_frame_fidelity = *max_it;

        // Average contributions across frames
        res.contribution_breakdown.resize(4, 0.0);
        for (const auto& contrib : contribution_vectors) {
            for (size_t i = 0; i < 4; ++i) {
                res.contribution_breakdown[i] += contrib[i];
            }
        }
        for (size_t i = 0; i < 4; ++i) {
            res.contribution_breakdown[i] /= contribution_vectors.size();
        }

        return res;
    }

    void print_results(const ChaosTestResult& res) {
        std::cout << "=" << std::string(58, '=') << "\n";
        std::cout << "CHAOS TEST RESULTS\n";
        std::cout << "=" << std::string(58, '=') << "\n";

        std::cout << "Handovers affected: " << res.handovers_affected << "\n";
        std::cout << "Nodes affected: " << res.nodes_affected << "\n";
        std::cout << "\nFidelity:\n";
        std::cout << "  Global: " << res.fidelity_global*100 << "%\n";
        std::cout << "  Pior frame: " << res.pior_frame_fidelity*100 << "%\n";
        std::cout << "  Melhor frame: " << res.melhor_frame_fidelity*100 << "%\n";
        std::cout << "\nContribution breakdown:\n";
        std::cout << "  Kalman filter: " << res.contribution_breakdown[0]*100 << "%\n";
        std::cout << "  ∇C continuity: " << res.contribution_breakdown[1]*100 << "%\n";
        std::cout << "  Phase alignment: " << res.contribution_breakdown[2]*100 << "%\n";
        std::cout << "  C+F=1 constraint: " << res.contribution_breakdown[3]*100 << "%\n";

        std::cout << "\nVeredict: "
                  << (res.fidelity_global >= 0.9978 ? "APROVADO" : "FALHOU") << "\n";
    }
};

int main() {
    // Simulate chaos test with 1000 handovers
    const int N_HANDOVERS = 1000;
    const int N_NODES = 1000000;

    ChaosTestAnalyzer analyzer(N_HANDOVERS, N_NODES);

    // Expected contributions from Arkhe chaos test
    const std::vector<double> CONTRIB_EXPECTED = {0.40, 0.20, 0.30, 0.10};

    // Simulate results
    for (int i = 0; i < N_HANDOVERS; ++i) {
        // Fidelity varies around 99.78%
        double fidelity = 0.9978 + (std::rand() % 100 - 50) * 0.00001;

        // Slight variations in contributions
        std::vector<double> contrib = CONTRIB_EXPECTED;
        for (size_t j = 0; j < contrib.size(); ++j) {
            contrib[j] += (std::rand() % 100 - 50) * 0.0001;
            if (contrib[j] < 0) contrib[j] = 0;
        }
        // Renormalize to sum 1
        double sum = 0.0;
        for (double c : contrib) sum += c;
        for (double& c : contrib) c /= sum;

        analyzer.add_frame_result(fidelity, contrib);
    }

    auto results = analyzer.compute_results();
    analyzer.print_results(results);

    return 0;
}
