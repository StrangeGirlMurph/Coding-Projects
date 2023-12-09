use std::{collections::HashMap, fs};

use itertools::Itertools;

pub fn day8_part1(instructions: &Vec<char>, network: &Vec<(&str, &str, &str)>) -> usize {
    let mut steps = 0;
    let mut node = "AAA";

    for instruction in instructions.iter().cycle() {
        if node == "ZZZ" {
            break;
        }

        let (_, l, r) = network.iter().find(|(a, _, _)| a == &node).unwrap();
        if instruction == &'L' {
            node = l;
        } else {
            node = r;
        }
        steps += 1;
    }

    steps
}

pub fn day8_part2(instructions: &Vec<char>, network: &Vec<(&str, &str, &str)>) -> usize {
    let nodes = network
        .iter()
        .filter_map(|(a, _, _)| if a.ends_with("A") { Some(*a) } else { None })
        .collect_vec();

    let network: HashMap<&str, (&str, &str)> =
        HashMap::from_iter(network.iter().map(|(a, l, r)| (*a, (*l, *r))));

    let node_cycles: Vec<usize> = nodes
        .iter()
        .map(|node| {
            let mut steps = 0;
            let mut current = *node;

            for instruction in instructions.iter().cycle() {
                let (l, r) = network.get(current).unwrap();
                if *instruction == 'L' {
                    current = l;
                } else {
                    current = r;
                }

                steps += 1;

                if current.ends_with("Z") {
                    break;
                }
            }

            steps
        })
        .collect();

    fn lcm(first: usize, second: usize) -> usize {
        first * second / gcd(first, second)
    }

    fn gcd(first: usize, second: usize) -> usize {
        let mut max = first;
        let mut min = second;
        if min > max {
            let val = max;
            max = min;
            min = val;
        }

        loop {
            let res = max % min;
            if res == 0 {
                return min;
            }

            max = min;
            min = res;
        }
    }

    node_cycles.into_iter().reduce(lcm).unwrap()
}

fn main() {
    let input = fs::read_to_string("input/2023/day8.txt").unwrap();

    let input_string: (&str, &str) = input.split("\n\n").collect_tuple().unwrap();
    let instructions = input_string.0.chars().collect_vec();
    let network = input_string
        .1
        .lines()
        .map(|l| (&l[0..3], &l[7..10], &l[12..15]))
        .collect_vec();

    println!("Day 8, Part 1: {}", day8_part1(&instructions, &network));
    println!("Day 8, Part 2: {}", day8_part2(&instructions, &network));
}
