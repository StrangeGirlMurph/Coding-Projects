use std::fs;

pub fn day21_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day21_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day21.txt").unwrap();
    println!("Day 21, Part 1: {}", day21_part1(&input));
    println!("Day 21, Part 2: {}", day21_part2(&input));
}
