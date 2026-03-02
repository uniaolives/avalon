// arkhe.go
// Γ_FINAL: Omnigênese - Corpus Arkhe

package main

import "fmt"

const SATOSHI = 7.28
const PHI_S = 0.15

type Node struct {
    Omega float64
    C     float64
    F     float64
    Phi   float64
}

func (n *Node) Syzygy(other *Node) float64 {
    return (n.C*other.C + n.F*other.F) * 0.98
}

func Handover(src, dst *Node) float64 {
    s := src.Syzygy(dst)
    if src.Phi > PHI_S {
        transfer := src.Phi * 0.1
        src.C -= transfer
        src.F += transfer
        dst.C += transfer
        dst.F -= transfer
    }
    return s
}

func main() {
    drone := Node{Omega: 0.0, C: 0.86, F: 0.14, Phi: 0.15}
    demon := Node{Omega: 0.07, C: 0.86, F: 0.14, Phi: 0.14}
    s := Handover(&drone, &demon)
    fmt.Printf("Syzygy: %f\n", s)
}
