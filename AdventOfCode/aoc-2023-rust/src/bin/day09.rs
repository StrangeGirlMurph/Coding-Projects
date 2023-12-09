use std::fs;

pub fn day9_part1(input: &str) -> isize {
    let histories = input
        .lines()
        .map(|l| {
            l.split_whitespace()
                .map(|w| w.parse::<isize>().unwrap())
                .collect::<Vec<isize>>()
        })
        .collect::<Vec<Vec<isize>>>();

    fn extrapolate(history: Vec<isize>) -> isize {
        if history.iter().all(|e| *e == 0isize) {
            return 0;
        } else {
            return extrapolate(
                history
                    .iter()
                    .cloned()
                    .zip(history.iter().cloned().skip(1))
                    .map(|(x, y)| y - x)
                    .collect(),
            ) + history.last().unwrap();
        }
    }

    histories.into_iter().map(|h| extrapolate(h)).sum()
}

pub fn day9_part2(input: &str) -> isize {
    let histories = input
        .lines()
        .map(|l| {
            l.split_whitespace()
                .map(|w| w.parse::<isize>().unwrap())
                .collect::<Vec<isize>>()
        })
        .collect::<Vec<Vec<isize>>>();

    fn extrapolate_backwards(history: Vec<isize>) -> isize {
        if history.iter().all(|e| *e == 0isize) {
            return 0;
        } else {
            return history.first().unwrap()
                - extrapolate_backwards(
                    history
                        .iter()
                        .cloned()
                        .zip(history.iter().cloned().skip(1))
                        .map(|(x, y)| y - x)
                        .collect(),
                );
        }
    }

    histories
        .into_iter()
        .map(|h| extrapolate_backwards(h))
        .sum()
}

fn main() {
    let input = fs::read_to_string("input/2023/day9.txt").unwrap();
    println!("Day 9, Part 1: {}", day9_part1(&input));
    println!("Day 9, Part 2: {}", day9_part2(&input));
}
