// ArkheCore.java
// Γ_FINAL: Omnigênese - Corpus Arkhe

public class ArkheCore {
    public static final double SATOSHI = 7.28;
    public static final double PHI_S = 0.15;

    public static class Node {
        double omega, C, F, phi;

        public Node(double omega, double C, double F, double phi) {
            this.omega = omega;
            this.C = C;
            this.F = F;
            this.phi = phi;
        }

        public double syzygy(Node other) {
            return (this.C * other.C + this.F * other.F) * 0.98;
        }
    }

    public static double handover(Node src, Node dst) {
        double s = src.syzygy(dst);
        if (src.phi > PHI_S) {
            double transfer = src.phi * 0.1;
            src.C -= transfer;
            src.F += transfer;
            dst.C += transfer;
            dst.F -= transfer;
        }
        return s;
    }

    public static void main(String[] args) {
        Node drone = new Node(0.0, 0.86, 0.14, 0.15);
        Node demon = new Node(0.07, 0.86, 0.14, 0.14);
        double s = handover(drone, demon);
        System.out.println("Syzygy: " + s);
    }
}
