use std::fs;

pub fn day8_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day8_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day8.txt").unwrap();
    println!("Day 8, Part 1: {}", day8_part1(&input));
    println!("Day 8, Part 2: {}", day8_part2(&input));
}
