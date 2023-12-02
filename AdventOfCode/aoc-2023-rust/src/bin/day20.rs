use std::fs;

pub fn day20_part1(input: &str) -> usize {
    input.lines().count()
}

pub fn day20_part2(input: &str) -> usize {
    input.lines().count()
}

fn main() {
    let input = fs::read_to_string("input/2023/day20.txt").unwrap();
    println!("Day 20, Part 1: {}", day20_part1(&input));
    println!("Day 20, Part 2: {}", day20_part2(&input));
}
