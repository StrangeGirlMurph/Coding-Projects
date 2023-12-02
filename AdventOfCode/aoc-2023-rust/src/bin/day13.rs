use std::fs;

pub fn day13_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day13_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day13.txt").unwrap();
    println!("Day 13, Part 1: {}", day13_part1(&input));
    println!("Day 13, Part 2: {}", day13_part2(&input));
}
