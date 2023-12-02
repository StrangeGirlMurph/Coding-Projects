use std::fs;

pub fn day22_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day22_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day22.txt").unwrap();
    println!("Day 22, Part 1: {}", day22_part1(&input));
    println!("Day 22, Part 2: {}", day22_part2(&input));
}
