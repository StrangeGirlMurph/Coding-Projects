use crate::grid::{BASE, Grid, NEIGHBORS_IN_2D};
use rayon::prelude::*;

pub fn game_of_life_step(grid: &mut Grid) {
    grid.raw = grid
        .par_iter_bits()
        .enumerate()
        .map(|(i, bits)| {
            let bools = Grid::bits_to_bools(bits);

            let new_bools = bools
                .par_iter()
                .enumerate()
                .map(|(j, alive)| {
                    let (x, y) = grid.index_to_xy(i * BASE + j);

                    let alive_neighbors = NEIGHBORS_IN_2D
                        .iter()
                        .map(|(x_off, y_off)| {
                            let (mut x, mut y) = (x as isize - x_off, y as isize - y_off);

                            if x == -1 {
                                x = grid.width as isize - 1
                            } else if x as usize == grid.width {
                                x = 0
                            }

                            if y == -1 {
                                y = grid.height as isize - 1
                            } else if y as usize == grid.height {
                                y = 0
                            }

                            if grid.get(x as usize, y as usize) {
                                1
                            } else {
                                0
                            }
                        })
                        .sum::<usize>();

                    if *alive {
                        alive_neighbors == 2 || alive_neighbors == 3
                    } else {
                        alive_neighbors == 3
                    }
                })
                .collect::<Vec<bool>>();

            Grid::bools_to_bits(new_bools)
        })
        .collect::<Vec<u8>>();
}
