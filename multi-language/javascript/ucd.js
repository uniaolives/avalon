// multi-language/javascript/ucd.js
function verifyConservation(C, F, tol = 1e-10) {
    return Math.abs(C + F - 1.0) < tol;
}

class UCD {
    constructor(data) {
        this.data = data;
        this.C = 0.5;
        this.F = 0.5;
    }

    analyze() {
        if (this.data.length > 1) {
            let sumCorr = 0;
            let count = 0;
            for (let i = 0; i < this.data.length; i++) {
                for (let j = i + 1; j < this.data.length; j++) {
                    sumCorr += Math.abs(this._pearson(this.data[i], this.data[j]));
                    count++;
                }
            }
            this.C = count > 0 ? sumCorr / count : 1.0;
        }
        this.F = 1.0 - this.C;
        return { C: this.C, F: this.F, conservation: verifyConservation(this.C, this.F) };
    }

    _pearson(x, y) {
        let n = x.length;
        let mx = x.reduce((a, b) => a + b) / n;
        let my = y.reduce((a, b) => a + b) / n;
        let num = 0, dx2 = 0, dy2 = 0;
        for (let i = 0; i < n; i++) {
            let dx = x[i] - mx;
            let dy = y[i] - my;
            num += dx * dy;
            dx2 += dx * dx;
            dy2 += dy * dy;
        }
        return dx2 * dy2 === 0 ? 0 : num / Math.sqrt(dx2 * dy2);
    }
}

const data = [[1,2,3,4], [2,3,4,5], [5,6,7,8]];
const ucd = new UCD(data);
console.log(ucd.analyze());
