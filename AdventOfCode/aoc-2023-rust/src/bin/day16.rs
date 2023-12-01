use std::fs;

pub fn day16_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day16_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day1.txt").unwrap();
    println!("Day 16, Part 1: {}", day16_part1(&input));
    println!("Day 16, Part 2: {}", day16_part2(&input));
}
