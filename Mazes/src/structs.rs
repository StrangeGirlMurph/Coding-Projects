use nannou::prelude::*;

use crate::MAZE_DIM;

pub struct Maze {
    pub cells: [[Cell; MAZE_DIM]; MAZE_DIM],
}

impl Maze {
    pub fn new_borderless() -> Self {
        Maze {
            cells: [[Cell::new(); MAZE_DIM]; MAZE_DIM],
        }
    }

    pub fn new_with_borders() -> Self {
        Maze {
            cells: [[Cell::full(); MAZE_DIM]; MAZE_DIM],
        }
    }

    pub fn new_random() -> Self {
        Maze {
            cells: [[Cell::random(); MAZE_DIM]; MAZE_DIM],
        }
    }

    pub fn read_cell(&self, position: &CellPosition) -> Option<&Cell> {
        match position.is_out_of_bounds() {
            true => None,
            false => Some(&self.cells[position.y as usize][position.x as usize]),
        }
    }

    pub fn read_cell_by_xy(&self, position: &(usize, usize)) -> Option<&Cell> {
        self.read_cell(&CellPosition {
            x: position.0 as isize,
            y: position.1 as isize,
        })
    }

    pub fn cell(&mut self, position: &CellPosition) -> Option<&mut Cell> {
        match position.is_out_of_bounds() {
            true => None,
            false => Some(&mut self.cells[position.y as usize][position.x as usize]),
        }
    }

    pub fn cell_by_xy(&mut self, position: &(usize, usize)) -> Option<&mut Cell> {
        self.cell(&CellPosition {
            x: position.0 as isize,
            y: position.1 as isize,
        })
    }

    pub fn cell_in_direction(
        &mut self,
        position: &CellPosition,
        direction: &Direction,
    ) -> Option<&mut Cell> {
        self.cell(&position.move_in_direction(&direction))
    }
}

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

    pub fn full() -> Self {
        Cell {
            data: 8 | 4 | 2 | 1,
        }
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
            .filter(|border| self.has_border(border))
            .collect::<Vec<Border>>()
    }

    pub fn has_border(&self, border: &Border) -> bool {
        self.data & border.bit_representation() != 0
    }

    pub fn add_border(&mut self, border: &Border) {
        self.data |= border.bit_representation();
    }

    pub fn remove_border(&mut self, border: &Border) {
        self.data &= !border.bit_representation();
    }

    pub fn get_possibile_directions(&self) -> Vec<Direction> {
        vec![
            Direction::Up,
            Direction::Right,
            Direction::Down,
            Direction::Left,
        ]
        .into_iter()
        .filter(|direction| !self.has_border(&direction.border()))
        .collect::<Vec<Direction>>()
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    pub fn border(&self) -> Border {
        match self {
            Direction::Up => Border::Top,
            Direction::Right => Border::Right,
            Direction::Down => Border::Bottom,
            Direction::Left => Border::Left,
        }
    }

    pub fn all() -> Vec<Direction> {
        vec![
            Direction::Up,
            Direction::Right,
            Direction::Down,
            Direction::Left,
        ]
    }

    pub fn reverse(&self) -> Direction {
        match self {
            Direction::Up => Direction::Down,
            Direction::Right => Direction::Left,
            Direction::Down => Direction::Up,
            Direction::Left => Direction::Right,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
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

    pub fn all() -> Vec<Border> {
        vec![Border::Top, Border::Right, Border::Bottom, Border::Left]
    }
}

/// The position of a cell in the maze. The top left cell is (0, 0).
#[derive(Clone, Copy, Debug)]
pub struct CellPosition {
    pub x: isize,
    pub y: isize,
}

impl CellPosition {
    pub fn move_in_direction(&self, direction: &Direction) -> CellPosition {
        match direction {
            Direction::Up => CellPosition {
                x: self.x,
                y: self.y - 1,
            },
            Direction::Right => CellPosition {
                x: self.x + 1,
                y: self.y,
            },
            Direction::Down => CellPosition {
                x: self.x,
                y: self.y + 1,
            },
            Direction::Left => CellPosition {
                x: self.x - 1,
                y: self.y,
            },
        }
    }

    pub fn is_out_of_bounds(&self) -> bool {
        self.x < 0 || self.x >= MAZE_DIM as isize || self.y < 0 || self.y >= MAZE_DIM as isize
    }
}
