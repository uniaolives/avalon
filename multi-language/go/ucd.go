// multi-language/go/ucd.go
package main

import (
	"fmt"
	"math"
)

type UCD struct {
	data [][]float64
}

func (u *UCD) pearson(x, y []float64) float64 {
	n := float64(len(x))
	var sx, sy float64
	for i := range x {
		sx += x[i]
		sy += y[i]
	}
	mx, my := sx/n, sy/n
	var num, dx2, dy2 float64
	for i := range x {
		dx, dy := x[i]-mx, y[i]-my
		num += dx * dy
		dx2 += dx * dx
		dy2 += dy * dy
	}
	if dx2*dy2 == 0 { return 0 }
	return num / math.Sqrt(dx2*dy2)
}

func (u *UCD) Analyze() (float64, float64) {
	n := len(u.data)
	if n > 1 {
		var sumCorr float64
		count := 0
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				sumCorr += math.Abs(u.pearson(u.data[i], u.data[j]))
				count++
			}
		}
		c := sumCorr / float64(count)
		return c, 1.0 - c
	}
	return 0.5, 0.5
}

func main() {
	data := [][]float64{{1, 2, 3, 4}, {2, 3, 4, 5}, {5, 6, 7, 8}}
	ucd := UCD{data: data}
	c, f := ucd.Analyze()
	fmt.Printf("C: %f, F: %f\n", c, f)
}
