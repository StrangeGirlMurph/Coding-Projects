use regex::Regex;
use std::{collections::HashMap, fs, vec};

pub fn day3_part1(input: &str) -> usize {
    let is_symbol =
        |c: char| -> bool { ['#', '+', '-', '=', '*', '$', '%', '/', '&', '@'].contains(&c) };

    let re = Regex::new(r"\d+").unwrap();
    let line_width = 141;

    re.find_iter(input)
        .filter_map(|m| {
            let number = m.as_str().parse::<usize>().unwrap();

            let start = m.start();
            let end = m.end();
            let left;
            let right;
            let top;
            let top_pos;
            let bottom;
            let bottom_pos;

            if start % line_width == 0 {
                left = ' ';
                right = input.chars().nth(end).unwrap_or(' ');
                top_pos = start - line_width..=end - line_width;
                bottom_pos = start + line_width..=end + line_width;
            } else if (end + 1) % line_width == 0 {
                right = ' ';
                left = input.chars().nth(start - 1).unwrap_or(' ');
                top_pos = start - line_width - 1..=end - line_width - 1;
                bottom_pos = start + line_width - 1..=end + line_width - 1;
            } else {
                left = input.chars().nth(start - 1).unwrap_or(' ');
                right = input.chars().nth(end).unwrap_or(' ');
                top_pos = start - line_width - 1..=end - line_width;
                bottom_pos = start + line_width - 1..=end + line_width;
            }
            top = input.get(top_pos).unwrap_or("");
            bottom = input.get(bottom_pos).unwrap_or("");

            if is_symbol(left)
                || is_symbol(right)
                || top.contains(is_symbol)
                || bottom.contains(is_symbol)
            {
                Some(number)
            } else {
                None
            }
        })
        .sum()
}

pub fn day3_part2(input: &str) -> usize {
    let re = Regex::new(r"\d+").unwrap();
    let line_width = 141;

    let mut gears = HashMap::<usize, Vec<usize>>::new();

    re.find_iter(input).for_each(|m| {
        let number = m.as_str().parse::<usize>().unwrap();

        let start = m.start();
        let end = m.end();
        let left;
        let right;
        let top;
        let top_pos;
        let bottom;
        let bottom_pos;

        if start % line_width == 0 {
            left = ' ';
            right = input.chars().nth(end).unwrap_or(' ');
            top_pos = start - line_width..=end - line_width;
            bottom_pos = start + line_width..=end + line_width;
        } else if (end + 1) % line_width == 0 {
            right = ' ';
            left = input.chars().nth(start - 1).unwrap_or(' ');
            top_pos = start - line_width - 1..=end - line_width - 1;
            bottom_pos = start + line_width - 1..=end + line_width - 1;
        } else {
            left = input.chars().nth(start - 1).unwrap_or(' ');
            right = input.chars().nth(end).unwrap_or(' ');
            top_pos = start - line_width - 1..=end - line_width;
            bottom_pos = start + line_width - 1..=end + line_width;
        }
        top = input.get(top_pos.clone()).unwrap_or("");
        bottom = input.get(bottom_pos.clone()).unwrap_or("");

        if left == '*' {
            if gears.get(&(start - 1)).is_some() {
                gears.get_mut(&(start - 1)).unwrap().push(number);
            } else {
                gears.insert(start - 1, vec![number]);
            }
        };
        if right == '*' {
            if gears.get(&(end)).is_some() {
                gears.get_mut(&(end)).unwrap().push(number);
            } else {
                gears.insert(end, vec![number]);
            }
        };

        if top.contains(|c| c == '*') {
            if gears
                .get(&(top.find(|c| c == '*').unwrap() + top_pos.start()))
                .is_some()
            {
                gears
                    .get_mut(&(top.find(|c| c == '*').unwrap() + top_pos.start()))
                    .unwrap()
                    .push(number);
            } else {
                gears.insert(
                    top.find(|c| c == '*').unwrap() + top_pos.start(),
                    vec![number],
                );
            }
        };
        if bottom.contains(|c| c == '*') {
            if gears
                .get(&(bottom.find(|c| c == '*').unwrap() + bottom_pos.start()))
                .is_some()
            {
                gears
                    .get_mut(&(bottom.find(|c| c == '*').unwrap() + bottom_pos.start()))
                    .unwrap()
                    .push(number);
            } else {
                gears.insert(
                    bottom.find(|c| c == '*').unwrap() + bottom_pos.start(),
                    vec![number],
                );
            }
        };
    });

    gears
        .iter()
        .filter(|(_, v)| v.len() > 1)
        .map(|(_, v)| v.iter().product::<usize>())
        .sum()
}

fn main() {
    let input = fs::read_to_string("input/2023/day3.txt").unwrap();
    println!("Day 3, Part 1: {}", day3_part1(&input));
    println!("Day 3, Part 2: {}", day3_part2(&input));
}
