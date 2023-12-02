use std::fs;

pub fn day17_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day17_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day17.txt").unwrap();
    println!("Day 17, Part 1: {}", day17_part1(&input));
    println!("Day 17, Part 2: {}", day17_part2(&input));
}
