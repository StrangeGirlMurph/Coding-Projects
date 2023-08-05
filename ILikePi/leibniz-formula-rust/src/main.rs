use indicatif::ProgressIterator;

// Leibniz formula for π
// https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80

fn main() {
    let digits = 10;
    let iterations = 10000000u32;

    let mut pi: u128 = 0;
    let base = 10u128.pow(digits);
    for i in (0..iterations).progress() {
        if i & 1 == 1 {
            pi = pi - 4 * base / (2 * i + 1) as u128;
        } else {
            pi = pi + 4 * base / (2 * i + 1) as u128;
        }
    }
    println!("{}", pi);
}
