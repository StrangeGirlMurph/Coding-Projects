# for generating the rust files

for i in range(2, 26):
    f = open(f"src/bin/day{i:02d}.rs", "w")
    f.write(f"""use std::fs;

pub fn day{i}_part1(input: &str) -> usize {{
    input.lines().count()
}}

pub fn day{i}_part2(input: &str) -> usize {{
    input.lines().count()
}}

fn main() {{
    let input = fs::read_to_string("input/2023/day{i}.txt").unwrap();
    println!("Day {i}, Part 1: {{}}", day{i}_part1(&input));
    println!("Day {i}, Part 2: {{}}", day{i}_part2(&input));
}}
""")
    f.close()