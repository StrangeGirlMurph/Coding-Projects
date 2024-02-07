use std::fs;

use itertools::Itertools;
use rayon::vec;

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Direction {
    North,
    South,
    East,
    West,
}

impl Direction {
    fn move_to_index(&self, index: (usize, usize)) -> (usize, usize) {
        match self {
            Direction::North => (index.0, index.1 - 1),
            Direction::South => (index.0, index.1 + 1),
            Direction::East => (index.0 + 1, index.1),
            Direction::West => (index.0 - 1, index.1),
        }
    }

    fn opposite(&self) -> Direction {
        match self {
            Direction::North => Direction::South,
            Direction::South => Direction::North,
            Direction::East => Direction::West,
            Direction::West => Direction::East,
        }
    }
}

fn char_to_directions(c: char) -> [Direction; 2] {
    match c {
        '|' => [Direction::North, Direction::South],
        '-' => [Direction::West, Direction::East],
        'L' => [Direction::North, Direction::East],
        'J' => [Direction::North, Direction::West],
        '7' => [Direction::West, Direction::South],
        'F' => [Direction::South, Direction::East],
        _ => panic!("Unknown direction: {}", c),
    }
}

pub fn day10_part1(input: &str) -> usize {
    let grid = input.lines().map(|l| l.chars().collect_vec()).collect_vec();

    let start_y = grid.iter().position(|l| l.contains(&'S')).unwrap();
    let start_x = grid[start_y].iter().position(|c| *c == 'S').unwrap();

    let mut current_position = (start_x, start_y);
    let mut current_direction: Direction = Direction::North;

    for direction in [
        Direction::North,
        Direction::South,
        Direction::East,
        Direction::West,
    ]
    .into_iter()
    {
        let (x, y) = direction.move_to_index(current_position);
        if char_to_directions(grid[y][x])
            .map(|d| d.opposite())
            .contains(&direction)
        {
            current_direction = direction;
            break;
        }
    }

    let mut len = 0;
    loop {
        current_position = current_direction.move_to_index(current_position);
        len += 1;
        if current_position == (start_x, start_y) {
            break;
        }
        current_direction = char_to_directions(grid[current_position.1][current_position.0])
            .into_iter()
            .find(|d| *d != current_direction.opposite())
            .unwrap();
    }

    len / 2
}

// WIP
pub fn day10_part2(input: &str) -> usize {
    let mut grid = input.lines().map(|l| l.chars().collect_vec()).collect_vec();

    let start_y = grid.iter().position(|l| l.contains(&'S')).unwrap();
    let start_x = grid[start_y].iter().position(|c| *c == 'S').unwrap();

    let mut current_position = (start_x, start_y);
    let mut current_direction: Direction = Direction::North;

    for direction in [
        Direction::North,
        Direction::South,
        Direction::East,
        Direction::West,
    ]
    .into_iter()
    {
        let (x, y) = direction.move_to_index(current_position);
        if char_to_directions(grid[y][x])
            .map(|d| d.opposite())
            .contains(&direction)
        {
            current_direction = direction;
            break;
        }
    }

    let mut pipe = vec![current_position];
    loop {
        let next_position = current_direction.move_to_index(current_position);
        if next_position == (start_x, start_y) {
            break;
        }

        current_position = next_position;
        pipe.push(current_position);
        current_direction = char_to_directions(grid[current_position.1][current_position.0])
            .into_iter()
            .find(|d| *d != current_direction.opposite())
            .unwrap();
    }

    grid = grid
        .iter()
        .enumerate()
        .map(|(y, l)| {
            l.iter()
                .enumerate()
                .map(|(x, c)| if pipe.contains(&(x, y)) { *c } else { '.' })
                .collect_vec()
        })
        .collect_vec();

    let mut shortest_pipe = vec![(start_x, start_y)];

    let mut count = 0;

    for y in 0..grid.len() {
        let mut inside = false;
        for x in 0..grid[y].len() {
            if ['-', 'J', 'L'].contains(&grid[y][x]) {
                inside = !inside;
            } else if grid[y][x] == '.' && inside {
                count += 1;
            }
        }
    }

    count
}

fn main() {
    let input = fs::read_to_string("input/2023/day10.txt").unwrap();
    println!("Day 10, Part 1: {}", day10_part1(&input));
    println!("Day 10, Part 2: {}", day10_part2(&input));
}
