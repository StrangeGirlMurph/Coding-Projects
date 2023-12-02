use std::fs;

pub fn day23_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day23_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day23.txt").unwrap();
    println!("Day 23, Part 1: {}", day23_part1(&input));
    println!("Day 23, Part 2: {}", day23_part2(&input));
}
