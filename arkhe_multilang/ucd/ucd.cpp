// ucd.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

struct UCDResult {
    double C;
    double F;
    bool conservation;
    std::string topology;
    std::string scaling;
    double optimization;
};

class UCD {
private:
    std::vector<std::vector<double>> data;
    double C, F;

    double pearson(const std::vector<double>& x, const std::vector<double>& y) {
        size_t n = x.size();
        double sumX = std::accumulate(x.begin(), x.end(), 0.0);
        double sumY = std::accumulate(y.begin(), y.end(), 0.0);
        double meanX = sumX / n;
        double meanY = sumY / n;
        double num = 0.0, denX = 0.0, denY = 0.0;
        for (size_t i = 0; i < n; ++i) {
            double dx = x[i] - meanX;
            double dy = y[i] - meanY;
            num += dx * dy;
            denX += dx * dx;
            denY += dy * dy;
        }
        return (denX == 0.0 || denY == 0.0) ? 1.0 : num / std::sqrt(denX * denY);
    }

public:
    UCD(const std::vector<std::vector<double>>& input) : data(input), C(0.0), F(0.0) {}

    UCDResult analyze() {
        size_t n = data.size();
        if (n > 1) {
            double sumCorr = 0.0;
            for (size_t i = 0; i < n; ++i) {
                for (size_t j = 0; j < n; ++j) {
                    double corr = pearson(data[i], data[j]);
                    sumCorr += std::abs(corr);
                }
            }
            C = sumCorr / (n * n);
        } else {
            C = 0.5;
        }
        F = 1.0 - C;
        bool cons = std::abs(C + F - 1.0) < 1e-10;
        return {C, F, cons, (C>0.8)?"toroidal":"other", (C>0.7)?"self-similar":"linear", F*0.5};
    }
};

int main() {
    std::vector<std::vector<double>> data = {{1,2,3,4}, {2,3,4,5}, {5,6,7,8}};
    UCD ucd(data);
    auto res = ucd.analyze();
    std::cout << "C: " << res.C << "\nF: " << res.F << "\nConservation: " << res.conservation << "\n";
    return 0;
}
