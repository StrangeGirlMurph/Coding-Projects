use cell::{Border, Cell, Direction};
use nannou::{
    prelude::*,
    rand::{self, seq::SliceRandom},
};
pub mod cell;

const MAZE_DIM: usize = 100;
const WINDOW_DIM: u32 = 1000;
const PADDING: u32 = 10;

const CELL_SIZE: f32 = (WINDOW_DIM - PADDING * 2) as f32 / MAZE_DIM as f32;

fn main() {
    nannou::app(model)
        .update(update)
        .simple_window(view)
        .size(WINDOW_DIM, WINDOW_DIM)
        .run();
}

struct Model {
    maze: [Cell; MAZE_DIM * MAZE_DIM],
}

fn model(_app: &App) -> Model {
    let mut maze = [Cell::new(); MAZE_DIM * MAZE_DIM];

    // Generate maze
    for i in 0..MAZE_DIM {
        maze[i].add_border(Border::Top);
        maze[i * MAZE_DIM + MAZE_DIM - 1].add_border(Border::Right);
        maze[MAZE_DIM * MAZE_DIM - MAZE_DIM + i].add_border(Border::Bottom);
        maze[i * MAZE_DIM].add_border(Border::Left);
    }

    let mut stack = vec![0];
    maze[0].toggle_visited();
    while stack.len() > 0 {
        let position = stack.last().unwrap().clone();

        let directions = maze[position].get_possibile_directions();
        let dir = directions
            .into_iter()
            .filter(|dir| !maze[(position as isize + dir.index_step()) as usize].is_visited())
            .collect::<Vec<Direction>>();
        let dir = dir.choose(&mut rand::thread_rng());

        if dir.is_some() {
            let dir = dir.unwrap();
            let next = (position as isize + dir.index_step()) as usize;

            maze[next].toggle_visited();
            stack.push(next);
            let options = maze[position].get_possibile_directions();
            for option in options {
                if !stack.contains(&((position as isize + option.index_step()) as usize)) {
                    maze[position].add_border(option.border());
                }
            }
        } else {
            stack.pop();
        }
    }

    Model { maze }
}

fn update(_app: &App, _model: &mut Model, _update: Update) {}

fn view(app: &App, model: &Model, frame: Frame) {
    let background_color = hsl(0.0, 0.0, 0.02);
    let line_color = hsl(0.0, 0.0, 0.4);
    let weight = 2.0.min(CELL_SIZE * 0.1);

    let draw = app.draw();
    draw.background().color(background_color);

    // Draw the maze
    for (i, cell) in model.maze.iter().enumerate() {
        let half_cell_size = CELL_SIZE / 2.0;
        let half_window_size = (WINDOW_DIM / 2) as f32;

        let x =
            (i % MAZE_DIM) as f32 * CELL_SIZE + PADDING as f32 - half_window_size + half_cell_size;
        let y = -1.0 * (i / MAZE_DIM) as f32 * CELL_SIZE - PADDING as f32 + half_window_size
            - half_cell_size;

        for border in cell.get_borders() {
            match border {
                Border::Top => {
                    draw.line()
                        .start(pt2(x - half_cell_size, y + half_cell_size))
                        .end(pt2(x + half_cell_size, y + half_cell_size))
                        .color(line_color)
                        .weight(weight);
                }
                Border::Right => {
                    draw.line()
                        .start(pt2(x + half_cell_size, y + half_cell_size))
                        .end(pt2(x + half_cell_size, y - half_cell_size))
                        .color(line_color)
                        .weight(weight);
                }
                Border::Bottom => {
                    draw.line()
                        .start(pt2(x + half_cell_size, y - half_cell_size))
                        .end(pt2(x - half_cell_size, y - half_cell_size))
                        .color(line_color)
                        .weight(weight);
                }
                Border::Left => {
                    draw.line()
                        .start(pt2(x - half_cell_size, y - half_cell_size))
                        .end(pt2(x - half_cell_size, y + half_cell_size))
                        .color(line_color)
                        .weight(weight);
                }
            }
        }
    }

    draw.to_frame(app, &frame).unwrap();
}
