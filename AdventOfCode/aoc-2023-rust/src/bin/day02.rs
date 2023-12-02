use std::{collections::HashMap, fs};

pub fn day2_part1(input: &str) -> usize {
    let bag = HashMap::<&str, usize>::from([("red", 12), ("green", 13), ("blue", 14)]);

    let data: Vec<(usize, Vec<Vec<(usize, &str)>>)> = input
        .lines()
        .map(|game| {
            let split = game.split(": ").collect::<Vec<&str>>();

            (
                split[0][5..].parse::<usize>().unwrap(),
                split[1]
                    .split("; ")
                    .map(|round| {
                        round
                            .split(", ")
                            .map(|cubes| {
                                let split = cubes.split(" ").collect::<Vec<&str>>();
                                (split[0].parse::<usize>().unwrap(), split[1])
                            })
                            .collect()
                    })
                    .collect(),
            )
        })
        .collect();

    data.iter()
        .filter(|e| {
            e.1.iter()
                .filter(|r| r.iter().filter(|c| c.0 > *bag.get(c.1).unwrap()).count() > 0)
                .count()
                == 0
        })
        .map(|e| e.0)
        .sum()
}

pub fn day2_part2(input: &str) -> usize {
    let data: Vec<Vec<Vec<(usize, &str)>>> = input
        .lines()
        .map(|game| {
            game.split(": ").collect::<Vec<&str>>()[1]
                .split("; ")
                .map(|round| {
                    round
                        .split(", ")
                        .map(|cubes| {
                            let split = cubes.split(" ").collect::<Vec<&str>>();
                            (split[0].parse::<usize>().unwrap(), split[1])
                        })
                        .collect()
                })
                .collect()
        })
        .collect();

    data.iter()
        .map(|e| {
            let mut red = 1;
            let mut green = 1;
            let mut blue = 1;

            for round in e {
                for cube in round {
                    match cube.1 {
                        "red" => red = red.max(cube.0),
                        "green" => green = green.max(cube.0),
                        "blue" => blue = blue.max(cube.0),
                        _ => (),
                    }
                }
            }

            red * green * blue
        })
        .sum()
}

fn main() {
    let input = fs::read_to_string("input/2023/day2.txt").unwrap();
    println!("Day 2, Part 1: {}", day2_part1(&input));
    println!("Day 2, Part 2: {}", day2_part2(&input));
}
