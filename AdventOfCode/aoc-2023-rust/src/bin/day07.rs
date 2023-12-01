use std::fs;

pub fn day7_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day7_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day1.txt").unwrap();
    println!("Day 7, Part 1: {}", day7_part1(&input));
    println!("Day 7, Part 2: {}", day7_part2(&input));
}
