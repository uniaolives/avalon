// warp_bubble.cpp
#include <iostream>
#include <cmath>
#include <vector>

const double PI = 3.141592653589793;
const double EPSILON = -3.71e-11;
const double PHI_S = 0.15;
const double R_PLANCK = 1.616e-35;

class WarpBubble {
private:
    double radius;
    double phase_int;
    double phase_ext;
    double syzygy;
    bool stable;

public:
    WarpBubble(double r = 10.0) : radius(r), phase_int(PI), phase_ext(0.0),
                                  syzygy(0.98), stable(false) {}

    double energy_available() const {
        return std::abs(EPSILON) * PHI_S * std::pow(radius / R_PLANCK, 2);
    }

    bool check_isolation() {
        double delta = std::fmod(std::abs(phase_int - phase_ext), 2*PI);
        stable = std::abs(delta - PI) < 0.01;
        return stable;
    }

    double redshift(double nu_em) const {
        return 0.253 * nu_em;
    }

    double metric(double r, double sigma = 1.0) const {
        double f = (std::tanh(sigma * (r + radius)) -
                   std::tanh(sigma * (r - radius))) /
                   (2 * std::tanh(sigma * radius));
        return -syzygy * (1 - f * phase_int / PI);
    }

    // RK4 para integração de geodésicas
    std::vector<std::vector<double>> integrate_geodesic(
        double t_max, double dt,
        double r0, double v0, double theta0, double omega0) {

        std::vector<std::vector<double>> trajectory;
        double r = r0, v = v0, theta = theta0, omega = omega0;
        double t = 0.0;

        while (t < t_max) {
            trajectory.push_back({t, r, v, theta, omega});

            // RK4 para sistema 4D
            auto get_derivatives = [&](double _r, double _v, double _theta, double _omega) {
                double dr = _v;
                double dv = -metric(_r) * EPSILON * syzygy * _v*_v / (_r + 1e-12);
                double dtheta = _omega;
                double domega = -2 * _v * _omega / (_r + 1e-12);
                return std::vector<double>{dr, dv, dtheta, domega};
            };

            auto k1 = get_derivatives(r, v, theta, omega);
            auto k2 = get_derivatives(r + dt/2*k1[0], v + dt/2*k1[1], theta + dt/2*k1[2], omega + dt/2*k1[3]);
            auto k3 = get_derivatives(r + dt/2*k2[0], v + dt/2*k2[1], theta + dt/2*k2[2], omega + dt/2*k2[3]);
            auto k4 = get_derivatives(r + dt*k3[0], v + dt*k3[1], theta + dt*k3[2], omega + dt*k3[3]);

            r += dt/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]);
            v += dt/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]);
            theta += dt/6 * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2]);
            omega += dt/6 * (k1[3] + 2*k2[3] + 2*k3[3] + k4[3]);

            t += dt;
        }

        return trajectory;
    }
};

int main() {
    WarpBubble bubble(10.0);
    std::cout << "Energia disponível: " << bubble.energy_available() << " J" << std::endl;
    std::cout << "Isolamento ativo: " << bubble.check_isolation() << std::endl;
    auto traj = bubble.integrate_geodesic(50.0, 0.1, 1.0, 0.0, 0.0, 1.0);
    std::cout << "Trajetória calculada com " << traj.size() << " pontos" << std::endl;
    return 0;
}
