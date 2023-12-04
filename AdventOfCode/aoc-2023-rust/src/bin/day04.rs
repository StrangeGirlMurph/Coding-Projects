use std::fs;

use regex::Regex;

pub fn day4_part1(input: &str) -> usize {
    let re = Regex::new(r"\d+").unwrap();

    input
        .lines()
        .map(|l| {
            let split: Vec<&str> = l.split(": ").nth(1).unwrap().split(" | ").collect();
            let winning_numbers = re
                .find_iter(split[0])
                .map(|m| m.as_str().parse().unwrap())
                .collect::<Vec<usize>>();
            let numbers = re
                .find_iter(split[1])
                .map(|m| m.as_str().parse().unwrap())
                .collect::<Vec<usize>>();

            let mut number_of_winners = 0;
            for number in numbers {
                if winning_numbers.contains(&number) {
                    number_of_winners += 1;
                }
            }

            if number_of_winners == 0 {
                0
            } else {
                2usize.pow(number_of_winners - 1)
            }
        })
        .sum()
}

pub fn day4_part2(input: &str) -> usize {
    let re = Regex::new(r"\d+").unwrap();

    let winners_per_game = input
        .lines()
        .map(|l| {
            let split: Vec<&str> = l.split(": ").nth(1).unwrap().split(" | ").collect();
            let winning_numbers = re
                .find_iter(split[0])
                .map(|m| m.as_str().parse().unwrap())
                .collect::<Vec<usize>>();
            let numbers = re
                .find_iter(split[1])
                .map(|m| m.as_str().parse().unwrap())
                .collect::<Vec<usize>>();

            let mut number_of_winners = 0;
            for number in numbers {
                if winning_numbers.contains(&number) {
                    number_of_winners += 1;
                }
            }

            number_of_winners
        })
        .collect::<Vec<usize>>();

    let mut copies: Vec<usize> = vec![1; winners_per_game.len()];
    for i in 0..copies.len() {
        for j in (i + 1)..=(i + winners_per_game[i]) {
            copies[j] += copies[i];
        }
    }

    copies.iter().sum()
}

fn main() {
    let input = fs::read_to_string("input/2023/day4.txt").unwrap();
    println!("Day 4, Part 1: {}", day4_part1(&input));
    println!("Day 4, Part 2: {}", day4_part2(&input));
}
