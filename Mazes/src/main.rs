use nannou::prelude::*;
use rayon::prelude::*;

const MAZE_DIM: usize = 100;
const WINDOW_DIM: u32 = 1000;
const PADDING: u32 = 10;

const CELL_SIZE: f32 = (WINDOW_DIM - PADDING * 2) as f32 / MAZE_DIM as f32;

#[derive(Clone, Copy)]
struct Cell {
    pub data: u8,
}

impl Cell {
    fn new() -> Self {
        Cell { data: 0 }
    }

    fn random() -> Self {
        Cell {
            data: random_range(0, 16),
        }
    }

    fn borders((top, right, bottom, left): (bool, bool, bool, bool)) -> Self {
        let mut data = 0;
        if top {
            data |= 8;
        }
        if right {
            data |= 4;
        }
        if bottom {
            data |= 2;
        }
        if left {
            data |= 1;
        }

        Cell { data }
    }

    fn get_borders(&self) -> (bool, bool, bool, bool) {
        (
            self.data & 8 == 0,
            self.data & 4 == 0,
            self.data & 2 == 0,
            self.data & 1 == 0,
        )
    }

    fn set_borders(&mut self, (top, right, bottom, left): (bool, bool, bool, bool)) {
        self.data = 0;
        if top {
            self.data |= 8;
        }
        if right {
            self.data |= 4;
        }
        if bottom {
            self.data |= 2;
        }
        if left {
            self.data |= 1;
        }
    }
}

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
    let maze = [Cell::new(); MAZE_DIM * MAZE_DIM].map(|_| Cell::random());
    Model { maze }
}

fn update(_app: &App, _model: &mut Model, _update: Update) {}

fn view(app: &App, model: &Model, frame: Frame) {
    let background_color = hsl(0.0, 0.0, 0.02);
    let line_color = hsl(0.0, 0.0, 0.4);
    let weight = CELL_SIZE * 0.1;

    let draw = app.draw();
    draw.background().color(background_color);

    // Draw the maze
    for (i, cell) in model.maze.iter().enumerate() {
        let x = (i % MAZE_DIM) as f32 * CELL_SIZE + PADDING as f32 - (WINDOW_DIM / 2) as f32
            + CELL_SIZE / 2.0;
        let y = (i / MAZE_DIM) as f32 * CELL_SIZE + PADDING as f32 - (WINDOW_DIM / 2) as f32
            + CELL_SIZE / 2.0;

        let half = CELL_SIZE / 2.0;
        let (top, right, bottom, left) = cell.get_borders();

        if top {
            draw.line()
                .start(pt2(x - half, y + half))
                .end(pt2(x + half, y + half))
                .color(line_color)
                .weight(weight);
        }
        if right {
            draw.line()
                .start(pt2(x + half, y + half))
                .end(pt2(x + half, y - half))
                .color(line_color)
                .weight(weight);
        }
        if bottom {
            draw.line()
                .start(pt2(x + half, y - half))
                .end(pt2(x - half, y - half))
                .color(line_color)
                .weight(weight);
        }
        if left {
            draw.line()
                .start(pt2(x - half, y - half))
                .end(pt2(x - half, y + half))
                .color(line_color)
                .weight(weight);
        }
    }

    draw.to_frame(app, &frame).unwrap();
}
