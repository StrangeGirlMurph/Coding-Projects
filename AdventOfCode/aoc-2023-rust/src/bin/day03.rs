use std::fs;

pub fn day3_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day3_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day3.txt").unwrap();
    println!("Day 3, Part 1: {}", day3_part1(&input));
    println!("Day 3, Part 2: {}", day3_part2(&input));
}
