pub fn day6_part1() -> usize {
    [(53, 313), (89, 1090), (76, 1214), (98, 1201)]
        .iter()
        .map(|race| {
            let mut num = 0;
            for t in 0..=race.0 {
                if race.1 < (race.0 - t) * t {
                    num += 1;
                }
            }
            num
        })
        .product()
}

pub fn day6_part2() -> usize {
    let time = 53897698;
    let distance: u64 = 313109012141201;

    let mut num = 0;
    for t in 0..=time {
        if distance < (time - t) * t {
            num += 1;
        }
    }
    num
}

fn main() {
    println!("Day 6, Part 1: {}", day6_part1());
    println!("Day 6, Part 2: {}", day6_part2());
}
