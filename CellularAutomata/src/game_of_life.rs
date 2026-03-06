use crate::grid::{Grid, NEIGHBORS_IN_2D};

pub fn game_of_life_step(grid: &mut Grid) {
    let mut new_grid = grid.clone();
    for (i, cell) in grid.iter().enumerate() {
        let alive = cell;
        let (x, y) = grid.index_to_xy(i);

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

        let new = if alive {
            alive_neighbors == 2 || alive_neighbors == 3
        } else {
            alive_neighbors == 3
        };

        new_grid.set(i, new);
    }
    grid.raw = new_grid.raw;
}
