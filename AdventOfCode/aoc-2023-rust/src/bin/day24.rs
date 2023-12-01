use std::fs;

pub fn day24_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day24_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day1.txt").unwrap();
    println!("Day 24, Part 1: {}", day24_part1(&input));
    println!("Day 24, Part 2: {}", day24_part2(&input));
}
