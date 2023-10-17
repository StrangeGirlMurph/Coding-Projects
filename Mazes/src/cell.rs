use nannou::prelude::*;

use crate::MAZE_DIM;

#[derive(Clone, Copy)]
pub struct Cell {
    /// 128
    /// 64
    /// 32
    /// 16  - visited
    /// 8   - top border
    /// 4   - right border
    /// 2   - bottom border
    /// 1   - left border
    pub data: u8,
}

impl Cell {
    pub fn new() -> Self {
        Cell { data: 0 }
    }

    pub fn random() -> Self {
        Cell {
            data: random_range(0, 16),
        }
    }

    pub fn is_visited(&self) -> bool {
        self.data & 16 != 0
    }

    pub fn toggle_visited(&mut self) {
        if self.is_visited() {
            self.data &= !16;
        } else {
            self.data |= 16;
        }
    }

    pub fn get_borders(&self) -> Vec<Border> {
        vec![Border::Top, Border::Right, Border::Bottom, Border::Left]
            .into_iter()
            .filter(|border| self.has_border(*border))
            .collect::<Vec<Border>>()
    }

    pub fn has_border(&self, border: Border) -> bool {
        self.data & border.bit_representation() != 0
    }

    pub fn add_border(&mut self, border: Border) {
        self.data |= border.bit_representation();
    }

    pub fn get_possibile_directions(&self) -> Vec<Direction> {
        vec![
            Direction::Up,
            Direction::Right,
            Direction::Down,
            Direction::Left,
        ]
        .into_iter()
        .filter(|direction| !self.has_border(direction.border()))
        .collect::<Vec<Direction>>()
    }
}

#[derive(Clone, Copy, Debug)]
pub enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    pub fn index_step(&self) -> isize {
        match self {
            Direction::Up => -1 * MAZE_DIM as isize,
            Direction::Right => 1,
            Direction::Down => MAZE_DIM as isize,
            Direction::Left => -1,
        }
    }

    pub fn border(&self) -> Border {
        match self {
            Direction::Up => Border::Top,
            Direction::Right => Border::Right,
            Direction::Down => Border::Bottom,
            Direction::Left => Border::Left,
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub enum Border {
    Top,
    Right,
    Bottom,
    Left,
}

impl Border {
    pub fn bit_representation(&self) -> u8 {
        match self {
            Border::Top => 8,
            Border::Right => 4,
            Border::Bottom => 2,
            Border::Left => 1,
        }
    }

    pub fn direction(&self) -> Direction {
        match self {
            Border::Top => Direction::Up,
            Border::Right => Direction::Right,
            Border::Bottom => Direction::Down,
            Border::Left => Direction::Left,
        }
    }
}
