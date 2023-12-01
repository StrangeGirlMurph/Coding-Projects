use std::fs;

pub fn day9_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day9_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day1.txt").unwrap();
    println!("Day 9, Part 1: {}", day9_part1(&input));
    println!("Day 9, Part 2: {}", day9_part2(&input));
}
