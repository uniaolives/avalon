// multi-language/cpp/ucd.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>

class UCD {
    std::vector<std::vector<double>> data;
public:
    UCD(std::vector<std::vector<double>> d) : data(d) {}

    double pearson(const std::vector<double>& x, const std::vector<double>& y) {
        size_t n = x.size();
        double sx = std::accumulate(x.begin(), x.end(), 0.0);
        double sy = std::accumulate(y.begin(), y.end(), 0.0);
        double mx = sx / n, my = sy / n;
        double num = 0, dx2 = 0, dy2 = 0;
        for (size_t i = 0; i < n; ++i) {
            double dx = x[i] - mx;
            double dy = y[i] - my;
            num += dx * dy;
            dx2 += dx * dx;
            dy2 += dy * dy;
        }
        return (dx2 * dy2 == 0) ? 0 : num / std::sqrt(dx2 * dy2);
    }

    std::pair<double, double> analyze() {
        size_t n = data.size();
        if (n > 1) {
            double sumCorr = 0;
            int count = 0;
            for (size_t i = 0; i < n; ++i) {
                for (size_t j = i + 1; j < n; ++j) {
                    sumCorr += std::abs(pearson(data[i], data[j]));
                    count++;
                }
            }
            double c = sumCorr / count;
            return {c, 1.0 - c};
        }
        return {0.5, 0.5};
    }
};

int main() {
    std::vector<std::vector<double>> data = {{1,2,3,4}, {2,3,4,5}, {5,6,7,8}};
    UCD ucd(data);
    auto res = ucd.analyze();
    std::cout << "C: " << res.first << ", F: " << res.second << std::endl;
    return 0;
}
