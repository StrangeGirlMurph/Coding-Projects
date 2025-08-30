use std::io::{self, Write};
use std::sync::{
    Arc,
    atomic::{AtomicUsize, Ordering},
};

use colored::{ColoredString, Colorize};
use hsv::hsv_to_rgb;
use rayon::prelude::*;

const ORDER: u8 = 8;
const BOARD_SIZE: usize = ORDER as usize * (ORDER as usize + 1) / 2;

fn main() {
    if ORDER < 8 {
        println!(
            "There are no solutions for this puzzle with an order less than 8. But fine, I'll check anyway. Just for you <3"
        );
    }

    println!("Finding puzzle solutions...");
    let solution_counter = Arc::new(AtomicUsize::new(0));
    println!("Number of solutions found:");
    let total_solutions = find_puzzle_solutions(Board::new(), solution_counter.clone());
    println!("In total there are {} solutions found.", total_solutions);
}

fn find_puzzle_solutions(board: Board, counter: Arc<AtomicUsize>) -> usize {
    if Piece::iter_all().all(|p| !board.has(p)) {
        // Found a solution if no pieces are left
        let count = counter.fetch_add(1, Ordering::Relaxed) + 1;
        if count % 100 == 0 {
            print!("\r{}", count);
            io::stdout().flush().unwrap();
        }
        //board.display();
        return 1;
    } else {
        let (x, y) = board
            .iter_coords()
            .find(|(x, y)| board.is_empty_at(*x, *y))
            .unwrap();

        //println!("Filling position ({}, {})", x, y);
        //board.display();

        let mut solutions: usize = 0;

        solutions += (2..=ORDER)
            .into_par_iter()
            .rev()
            .map(|id| Piece::from_id(id))
            .filter(|p| board.has(*p) && board.fits(x, y, *p))
            .map(|p| find_puzzle_solutions(board.place(x, y, p), counter.clone()))
            .sum::<usize>();

        // It holds: (x,y) empty =>
        // (<x,y) and (x,<y) must be filled
        // (x,>y) must be empty
        if board.has(Piece::from_id(1)) {
            if x.min(y) != 0 && x.max(y) != BOARD_SIZE - 1 {
                // The 1x1 piece cannot go on the edges
                if !(board.is_empty_at(x + 1, y) && board.is_filled_at(x - 1, y + 1)) {
                    /* The 1x1 piece cannot go into a corner created by two larger pieces like this:
                       o o o
                       o 1 -
                       x
                    */
                    if !(board.is_filled_at(x + 1, y)
                        && board.is_filled_at(x - 1, y + 1)
                        && board.is_filled_at(x + 1, y + 1))
                    {
                        /* The 1x1 piece cannot go into a slot where it would be isolated like this:
                           o o o
                           o 1 x
                           x   x
                        */
                        solutions += find_puzzle_solutions(
                            board.place(x, y, Piece::from_id(1)),
                            counter.clone(),
                        );
                    }
                }
            }
        }

        return solutions;
    }
}

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct Board {
    board: [Piece; BOARD_SIZE * BOARD_SIZE],
    pieces: [u8; ORDER as usize],
}

impl Board {
    fn new() -> Self {
        Self {
            board: [Piece { id: 0 }; BOARD_SIZE * BOARD_SIZE],
            pieces: std::array::from_fn(|i| (i + 1) as u8),
        }
    }

    fn has(&self, piece: Piece) -> bool {
        let id = piece.id as usize;
        self.pieces[id - 1] > 0
    }

    fn spend(&mut self, piece: Piece) {
        let id = piece.id as usize;
        self.pieces[id - 1] -= 1;
    }

    fn is_empty_at(&self, x: usize, y: usize) -> bool {
        self.get(x, y).is_empty()
    }

    fn is_filled_at(&self, x: usize, y: usize) -> bool {
        !self.is_empty_at(x, y)
    }

    fn get(&self, x: usize, y: usize) -> Piece {
        self.board[y * BOARD_SIZE + x]
    }

    fn set(&mut self, x: usize, y: usize, value: Piece) {
        self.board[y * BOARD_SIZE + x] = value;
    }

    fn fits(&self, x: usize, y: usize, piece: Piece) -> bool {
        let size = piece.size();
        if x + size as usize > BOARD_SIZE || y + size as usize > BOARD_SIZE {
            return false;
        }
        for dy in 0..size {
            for dx in 0..size {
                if !self.get(x + dx as usize, y + dy as usize).is_empty() {
                    return false;
                }
            }
        }
        true
    }

    fn place(&self, x: usize, y: usize, piece: Piece) -> Board {
        let mut new_board = self.clone();
        new_board.spend(piece);

        let size = piece.size();
        for dy in 0..size {
            for dx in 0..size {
                new_board.set(x + dx as usize, y + dy as usize, piece);
            }
        }
        new_board
    }

    fn iter_coords(&self) -> impl Iterator<Item = (usize, usize)> {
        (0..BOARD_SIZE * BOARD_SIZE).map(|i| (i % BOARD_SIZE, i / BOARD_SIZE))
    }

    fn display(&self) {
        if self.pieces.iter().sum::<u8>() != 0 {
            println!(
                "Pieces left: {}",
                self.pieces
                    .iter()
                    .enumerate()
                    .map(|(i, count)| format!("{}x{}: {}", i + 1, i + 1, count))
                    .filter(|s| !s.ends_with("0"))
                    .collect::<Vec<_>>()
                    .join(", ")
            );
        } else {
            println!("A solution!");
        }

        println!("┌{}─┐", "──".repeat(BOARD_SIZE));
        for y in 0..BOARD_SIZE {
            print!("│");
            for x in 0..BOARD_SIZE {
                let t = self.get(x, y);
                let colorized = if t.is_empty() {
                    " -".normal()
                } else {
                    t.colorize()
                };
                print!("{}", colorized);
            }
            println!(" │");
        }
        println!("└{}─┘", "──".repeat(BOARD_SIZE));
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Piece {
    id: u8,
}

impl Piece {
    fn from_id(id: u8) -> Self {
        Self { id }
    }

    fn iter_all() -> impl Iterator<Item = Piece> {
        (1..=ORDER).map(Piece::from_id)
    }

    fn size(&self) -> u8 {
        self.id
    }

    fn is_empty(&self) -> bool {
        self.id == 0
    }

    fn colorize(&self) -> ColoredString {
        let fill = format!(" {}", self.id);

        let fraction = (self.id - 1) as f64 / ORDER as f64;
        let hue = fraction * 360.0;
        let (r, g, b) = hsv_to_rgb(hue, 0.5, 1.0);

        fill.truecolor(r, g, b)
    }
}
