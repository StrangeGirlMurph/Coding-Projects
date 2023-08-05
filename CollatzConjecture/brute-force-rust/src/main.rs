use rayon::prelude::*;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let max = 100_000_000;

    let steps = (1..=max).into_par_iter().map(exec).sum::<usize>();

    println!("Total steps: {}", steps);
    println!("Took: {:?}", start.elapsed());
}

#[inline]
fn exec(mut n: usize) -> usize {
    let mut steps = 0;

    while n != 1 {
        if (n & 1) == 0 {
            n /= 2;
            steps += 1;
        } else {
            n = ((n * 3) + 1) / 2;
            steps += 2;
        }
    }

    steps
}
