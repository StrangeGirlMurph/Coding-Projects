use rand::prelude::*;

fn main() {
    let end = 1000;
    let mut pi: f64;
    let mut rng = rand::thread_rng();
    let mut coprime_count = 1;

    println!("Let's get this party started!");

    for i in 1.. {
        if are_coprime(rng.gen_range(1..end), rng.gen_range(1..end)) {
            coprime_count += 1;
        }

        pi = (6.0 / (coprime_count as f64 / i as f64)).sqrt();
        println!("{} \t  {}", pi, i);
    }
}

fn are_coprime(mut a: i32, mut b: i32) -> bool {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a == 1
}
