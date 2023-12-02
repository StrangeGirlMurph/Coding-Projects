use std::fs;

pub fn day15_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day15_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day15.txt").unwrap();
    println!("Day 15, Part 1: {}", day15_part1(&input));
    println!("Day 15, Part 2: {}", day15_part2(&input));
}
