use std::fs;

pub fn day1_part1(input: &str) -> u32 {
    input
        .lines()
        .map(|l| l.matches(char::is_numeric).collect())
        .map(|l: Vec<&str>| {
            format!("{}{}", l.first().unwrap(), l.last().unwrap())
                .parse::<u32>()
                .unwrap()
        })
        .sum()
}

pub fn day_1part2(input: &str) -> u32 {
    input
        .replace("one", "o1e")
        .replace("one", "o1e")
        .replace("two", "t2o")
        .replace("three", "t3e")
        .replace("four", "f4r")
        .replace("five", "f5e")
        .replace("six", "s6x")
        .replace("seven", "s7n")
        .replace("eight", "e8t")
        .replace("nine", "n9e")
        .lines()
        .map(|l| l.matches(char::is_numeric).collect())
        .map(|l: Vec<&str>| {
            format!("{}{}", l.first().unwrap(), l.last().unwrap())
                .parse::<u32>()
                .unwrap()
        })
        .sum()
}

fn main() {
    let input = fs::read_to_string("input/2023/day1.txt").unwrap();
    println!("Day 1, Part 1: {}", day1_part1(&input));
    println!("Day 1, Part 2: {}", day_1part2(&input));
}
