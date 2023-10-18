use nannou::{
    prelude::*,
    rand::{self, seq::SliceRandom},
};
use structs::{Border, CellPosition, Direction, Maze};
pub mod structs;

const MAZE_DIM: usize = 100;
const WINDOW_DIM: u32 = 1000;
const PADDING: u32 = 10;

const CELL_SIZE: f32 = (WINDOW_DIM - PADDING * 2) as f32 / MAZE_DIM as f32;

fn main() {
    nannou::app(model)
        /* .loop_mode(LoopMode::Rate {
            update_interval: Duration::from_millis(1000), // currently not working
        }) */
        .update(update)
        .simple_window(view)
        .size(WINDOW_DIM, WINDOW_DIM)
        .run();
}

struct Model {
    maze: Maze,
}

fn model(_app: &App) -> Model {
    let mut maze = Maze::new_with_borders();
    let start = CellPosition { x: 0, y: 0 };
    let end = CellPosition {
        x: MAZE_DIM as isize - 1,
        y: MAZE_DIM as isize - 1,
    };

    let mut stack = vec![start];
    maze.cell(&start).unwrap().toggle_visited();

    while stack.len() != 0 {
        let position = stack.pop().unwrap();

        let directions = Direction::all()
            .into_iter()
            .filter(|direction| {
                let target = maze.read_cell(&position.move_in_direction(direction));
                match target.is_some() {
                    true => !target.unwrap().is_visited(),
                    false => false,
                }
            })
            .collect::<Vec<Direction>>();

        if !directions.is_empty() {
            let direction = directions.choose(&mut rand::thread_rng()).unwrap();

            maze.cell_in_direction(&position, direction)
                .unwrap()
                .toggle_visited();

            stack.push(position);
            stack.push(position.move_in_direction(direction));
            maze.cell(&position)
                .unwrap()
                .remove_border(&direction.border());
            maze.cell(&position.move_in_direction(direction))
                .unwrap()
                .remove_border(&direction.reverse().border());
        }
    }

    maze.cell(&start).unwrap().remove_border(&Border::Top);
    maze.cell(&end).unwrap().remove_border(&Border::Bottom);

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
    let half_cell_size = CELL_SIZE / 2.0;
    let half_window_size = (WINDOW_DIM / 2) as f32;

    for x in 0..MAZE_DIM {
        for y in 0..MAZE_DIM {
            let cell = model.maze.read_cell_by_xy(&(x, y));

            let x = x as f32 * CELL_SIZE + PADDING as f32 - half_window_size + half_cell_size;
            let y =
                -1.0 * y as f32 * CELL_SIZE - PADDING as f32 + half_window_size - half_cell_size;

            for border in cell.unwrap().get_borders() {
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
    }

    draw.to_frame(app, &frame).unwrap();
}
