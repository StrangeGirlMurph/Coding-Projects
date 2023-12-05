use itertools::Itertools;
use rayon::prelude::*;
use std::fs;

#[derive(Debug)]
struct Mapping {
    mappings: Vec<RangeMapping>,
}

#[derive(Debug)]
struct RangeMapping {
    source_start: u64,
    destination_start: u64,
    length: u64,
}

pub fn day5_part1(input: &str) -> u64 {
    let split: Vec<&str> = input.split("\n\n").collect();

    let mappings: Vec<Mapping> = split[1..]
        .iter()
        .map(|block| Mapping {
            mappings: block
                .split(" map:\n")
                .nth(1)
                .unwrap()
                .lines()
                .map(|l| {
                    let values: Vec<u64> =
                        l.split(" ").map(|s| s.parse::<u64>().unwrap()).collect();
                    RangeMapping {
                        source_start: values[1],
                        destination_start: values[0],
                        length: values[2],
                    }
                })
                .collect(),
        })
        .collect_vec();

    split[0]
        .split(": ")
        .nth(1)
        .unwrap()
        .split(" ")
        .map(|seed| {
            let mut number = seed.parse::<u64>().unwrap();
            for mapping in mappings.iter() {
                for map in mapping.mappings.iter() {
                    if map.source_start <= number && number < map.source_start + map.length {
                        number = map.destination_start + (number - map.source_start);
                        break;
                    }
                }
            }
            number
        })
        .min()
        .unwrap()
}

pub fn day5_part2(input: &str) -> u64 {
    let split: Vec<&str> = input.split("\n\n").collect();

    let mappings: Vec<Mapping> = split[1..]
        .iter()
        .map(|block| Mapping {
            mappings: block
                .split(" map:\n")
                .nth(1)
                .unwrap()
                .lines()
                .map(|l| {
                    let values: Vec<u64> =
                        l.split(" ").map(|s| s.parse::<u64>().unwrap()).collect();
                    RangeMapping {
                        source_start: values[1],
                        destination_start: values[0],
                        length: values[2],
                    }
                })
                .collect(),
        })
        .collect_vec();

    split[0]
        .split(": ")
        .nth(1)
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<u64>>()
        .par_chunks(2)
        .flat_map(|chunk| chunk[0]..(chunk[0] + chunk[1]))
        .map(|seed| {
            let mut number = seed;
            for mapping in mappings.iter() {
                for map in mapping.mappings.iter() {
                    if map.source_start <= number && number < map.source_start + map.length {
                        number = map.destination_start + (number - map.source_start);
                        break;
                    }
                }
            }
            number
        })
        .min()
        .unwrap()
}

fn main() {
    let input = fs::read_to_string("input/2023/day5.txt").unwrap();
    println!("Day 5, Part 1: {}", day5_part1(&input));
    // Takes roughly 30s
    println!("Day 5, Part 2: {}", day5_part2(&input));
}
