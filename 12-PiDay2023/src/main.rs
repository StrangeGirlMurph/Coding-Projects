use indicatif::ProgressIterator;

fn main() {
    let mut pi: u128 = 0;
    let digits = 1000000000000;

    for i in (0..1000000000u32).progress() {
        if i & 1 == 1 {
            pi = pi - 4 * digits / (2 * i + 1) as u128;
        } else {
            pi = pi + 4 * digits / (2 * i + 1) as u128;
        }
    }
    println!("{}", pi);
}
