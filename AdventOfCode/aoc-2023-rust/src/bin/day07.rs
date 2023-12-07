use std::fs;

use itertools::Itertools;
use rayon::slice::ParallelSliceMut;

const CARDS: [char; 13] = [
    'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2',
];

#[derive(Debug)]
struct Hand {
    cards: [char; 5],
    bid: usize,
}

impl Hand {
    fn get_type(&self) -> Type {
        let mut counts = [0; 13];
        CARDS.iter().enumerate().for_each(|(i, c)| {
            counts[i] = self.cards.iter().filter(|&x| x == c).count();
        });

        if counts.contains(&5) {
            Type::FiveOfAKind
        } else if counts.contains(&4) {
            Type::FourOfAKind
        } else if counts.contains(&3) && counts.contains(&2) {
            Type::FullHouse
        } else if counts.contains(&3) {
            Type::ThreeOfAKind
        } else if counts.iter().filter(|&x| x == &2).count() == 2 {
            Type::TwoPairs
        } else if counts.iter().filter(|&x| x == &2).count() == 1 {
            Type::OnePair
        } else {
            Type::HighCard
        }
    }
}

#[derive(PartialEq, PartialOrd, Debug)]
enum Type {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPairs,
    OnePair,
    HighCard,
}

pub fn day7_part1(input: &str) -> usize {
    let mut hands: Vec<Hand> = input
        .lines()
        .map(|l| {
            let (hand, bid) = l.split_once(" ").unwrap();
            Hand {
                cards: match hand.chars().collect_vec()[..] {
                    [a, b, c, d, e] => [a, b, c, d, e],
                    _ => panic!("Unexpected length of Vec"),
                },
                bid: bid.parse().unwrap(),
            }
        })
        .collect_vec();

    hands.par_sort_by(|a, b| {
        let a_type = a.get_type();
        let b_type = b.get_type();

        if a_type != b_type {
            b_type.partial_cmp(&a_type).unwrap()
        } else {
            let mut i = 0;
            while a.cards[i] == b.cards[i] {
                i += 1;
            }

            let a_index = CARDS.iter().position(|&x| x == a.cards[i]).unwrap();
            let b_index = CARDS.iter().position(|&x| x == b.cards[i]).unwrap();

            b_index.partial_cmp(&a_index).unwrap()
        }
    });

    hands
        .iter()
        .enumerate()
        .map(|(i, hand)| (i + 1) * hand.bid)
        .sum()
}

impl Hand {
    fn get_type_with_joker(&self) -> Type {
        let mut counts = [0; 13];
        CARDS.iter().enumerate().for_each(|(i, c)| {
            counts[i] = self.cards.iter().filter(|&x| x == c).count();
        });

        let counts_iter_with_joker = counts
            .iter()
            .enumerate()
            .map(|(i, c)| if i == 3 { counts[3] } else { c + counts[3] })
            .collect_vec();

        if counts.contains(&5) || counts_iter_with_joker.contains(&5) {
            Type::FiveOfAKind
        } else if counts.contains(&4) || counts_iter_with_joker.contains(&4) {
            Type::FourOfAKind
        } else if counts.contains(&3) && counts.contains(&2)
            || counts.iter().filter(|&x| x == &2).count() == 2 && counts[3] == 1
        {
            Type::FullHouse
        } else if counts.contains(&3) || counts_iter_with_joker.contains(&3) {
            Type::ThreeOfAKind
        } else if counts.iter().filter(|&x| x == &2).count() == 2
            || counts.contains(&2) && counts_iter_with_joker.contains(&2) && counts[3] != 0
        {
            Type::TwoPairs
        } else if counts.contains(&2) || counts_iter_with_joker.contains(&2) {
            Type::OnePair
        } else {
            Type::HighCard
        }
    }
}

pub fn day7_part2(input: &str) -> usize {
    let mut hands: Vec<Hand> = input
        .lines()
        .map(|l| {
            let (hand, bid) = l.split_once(" ").unwrap();
            Hand {
                cards: match hand.chars().collect_vec()[..] {
                    [a, b, c, d, e] => [a, b, c, d, e],
                    _ => panic!("Unexpected length of Vec"),
                },
                bid: bid.parse().unwrap(),
            }
        })
        .collect_vec();

    hands.par_sort_by(|a, b| {
        let a_type = a.get_type_with_joker();
        let b_type = b.get_type_with_joker();

        if a_type != b_type {
            b_type.partial_cmp(&a_type).unwrap()
        } else {
            let mut i = 0;
            while a.cards[i] == b.cards[i] {
                i += 1;
            }

            if a.cards[i] == 'J' {
                std::cmp::Ordering::Less
            } else if b.cards[i] == 'J' {
                std::cmp::Ordering::Greater
            } else {
                let a_index = CARDS.iter().position(|&x| x == a.cards[i]).unwrap();
                let b_index = CARDS.iter().position(|&x| x == b.cards[i]).unwrap();

                b_index.partial_cmp(&a_index).unwrap()
            }
        }
    });

    hands
        .iter()
        .enumerate()
        .map(|(i, hand)| (i + 1) * hand.bid)
        .sum()
}

fn main() {
    let input = fs::read_to_string("input/2023/day7.txt").unwrap();
    println!("Day 7, Part 1: {}", day7_part1(&input));
    println!("Day 7, Part 2: {}", day7_part2(&input));
}
