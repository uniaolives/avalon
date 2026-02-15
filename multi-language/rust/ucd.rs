// multi-language/rust/ucd.rs
struct UCD {
    data: Vec<Vec<f64>>,
}

impl UCD {
    fn new(data: Vec<Vec<f64>>) -> Self {
        UCD { data }
    }

    fn pearson(&self, x: &[f64], y: &[f64]) -> f64 {
        let n = x.len() as f64;
        let mx = x.iter().sum::<f64>() / n;
        let my = y.iter().sum::<f64>() / n;
        let mut num = 0.0;
        let mut dx2 = 0.0;
        let mut dy2 = 0.0;
        for i in 0..x.len() {
            let dx = x[i] - mx;
            let dy = y[i] - my;
            num += dx * dy;
            dx2 += dx * dx;
            dy2 += dy * dy;
        }
        if dx2 * dy2 == 0.0 { 0.0 } else { num / (dx2 * dy2).sqrt() }
    }

    fn analyze(&self) -> (f64, f64) {
        let n = self.data.len();
        if n > 1 {
            let mut sum_corr = 0.0;
            let mut count = 0;
            for i in 0..n {
                for j in i+1..n {
                    sum_corr += self.pearson(&self.data[i], &self.data[j]).abs();
                    count += 1;
                }
            }
            let c = if count > 0 { sum_corr / count as f64 } else { 1.0 };
            (c, 1.0 - c)
        } else {
            (0.5, 0.5)
        }
    }
}

fn main() {
    let data = vec![
        vec![1.0, 2.0, 3.0, 4.0],
        vec![2.0, 3.0, 4.0, 5.0],
        vec![5.0, 6.0, 7.0, 8.0],
    ];
    let ucd = UCD::new(data);
    let (c, f) = ucd.analyze();
    println!("C: {}, F: {}", c, f);
}
