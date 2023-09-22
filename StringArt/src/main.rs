pub mod lines;
pub mod utils;

use lines::calculate_line;
use minifb::{Key, ScaleMode, Window, WindowOptions};
use ndarray::{concatenate, s, Array1, Array2, Axis, Order, Zip};
use rayon::prelude::*;
use utils::{blend_colors, extract_rgb, grayscale, load_image, plot, Position};

const NODES: usize = 480; // number of nodes (must be divisible by 4) (and pls don't make it divisible by 3 okay byeee)
const MAX_SIZE: usize = 400; // maximum height and width of the image
const MIN_SIZE: usize = 300; // minimum height and width of the image
const ALPHA: f64 = 0.08; // alpha value for the lines

fn main() {
    // Load image
    let image = load_image("resources/road.jpg");
    let size = image.dim().0;

    // Drawing
    let mut window = Window::new(
        "String Art - Press ESC to exit",
        2 * size,
        size,
        WindowOptions {
            resize: true,
            scale_mode: ScaleMode::Center,
            ..WindowOptions::default()
        },
    )
    .expect("Unable to create window :(");

    // Limit to max ~60 fps update rate
    //window.limit_update_rate(Some(std::time::Duration::from_micros(16600)));

    // Computation
    let mut nodes: [Position; NODES] = [Position { x: 0.0, y: 0.0 }; NODES];
    for (i, val) in Array1::<f64>::linspace(0.0, 1.0, NODES / 4 + 1)
        .slice(s![0..-1i32])
        .iter()
        .enumerate()
    {
        nodes[i * 4] = Position { x: *val, y: 0.0 };
        nodes[i * 4 + 1] = Position { x: 1.0, y: *val };
        nodes[i * 4 + 2] = Position {
            x: 1.0 - *val,
            y: 1.0,
        };
        nodes[i * 4 + 3] = Position {
            x: 0.0,
            y: 1.0 - *val,
        };
    }

    let mut canvas: Array2<u32> = Array2::from_elem((size, size), grayscale(0.0));
    let color = grayscale(1.0);

    let mut previous = 0;
    let mut current = 0;

    while window.is_open() && !window.is_key_down(Key::Escape) && !window.is_key_down(Key::Q) {
        let distance_map = distance_map(&image, &canvas);

        let mut best: (usize, f64, Array2<bool>, Array2<f64>) = (
            0,
            f64::INFINITY,
            Array2::default((0, 0)),
            Array2::default((0, 0)),
        );

        for (index, node) in nodes.iter().enumerate() {
            if index == current
                || index == previous
                || (nodes[current].x == node.x
                    && nodes[current].x % 1.0 == 0.0
                    && node.x % 1.0 == 0.0)
                || (nodes[current].y == node.y
                    && nodes[current].y % 1.0 == 0.0
                    && node.y % 1.0 == 0.0)
            {
                continue;
            }

            let (alpha_mask, boolean_mask) =
                calculate_line(&canvas.raw_dim(), nodes[current].mul(size), node.mul(size));
            let diff = calculate_distance(
                &distance_map,
                &image,
                &canvas,
                &boolean_mask,
                &alpha_mask,
                color,
                ALPHA,
            );
            //println!("{} -> {} | {}", current, index, diff);

            if diff < best.1 {
                best = (index, diff, boolean_mask, alpha_mask);
            }
        }

        //println!("{} {}", nodes[current].x, nodes[current].y);
        previous = current;
        current = best.0;
        plot(&mut canvas, &best.2, &best.3, color, ALPHA);

        let concatenated = concatenate(Axis(1), &[image.view(), canvas.view()]).unwrap();
        let concatenated = concatenated
            .to_shape(((2 * size * size), Order::RowMajor))
            .unwrap()
            .to_vec();

        window
            .update_with_buffer(&concatenated, 2 * size, size)
            .unwrap();
    }
}

fn calculate_distance(
    distance_map: &Array2<usize>,
    image: &Array2<u32>,
    canvas: &Array2<u32>,
    boolean_mask: &Array2<bool>,
    alpha_mask: &Array2<f64>,
    color: u32,
    alpha: f64,
) -> f64 {
    Zip::from(distance_map)
        .and(boolean_mask)
        .into_par_iter()
        .filter(|(_, boolean)| !**boolean)
        .map(|(distance, _)| *distance as f64)
        .sum::<f64>()
        + Zip::from(image)
            .and(canvas)
            .and(alpha_mask)
            .and(boolean_mask)
            .into_par_iter()
            .filter(|(_, _, _, boolean)| **boolean)
            .map(|(image_pixel, canvas_pixel, alpha_pixel, _)| {
                let reference = *image_pixel;
                let new = blend_colors(*canvas_pixel, color, *alpha_pixel * alpha);
                let (r0, g0, b0) = extract_rgb(reference);
                let (r1, g1, b1) = extract_rgb(new);
                (r0.abs_diff(r1) as f64).powf(1.0)
                    + (g0.abs_diff(g1) as f64).powf(1.0)
                    + (b0.abs_diff(b1) as f64).powf(1.0)
            })
            .sum::<f64>()
}

fn distance_map(image: &Array2<u32>, canvas: &Array2<u32>) -> Array2<usize> {
    Zip::from(image)
        .and(canvas)
        .map_collect(|image_pixel, canvas_pixel| {
            let (r0, g0, b0) = extract_rgb(*image_pixel);
            let (r1, g1, b1) = extract_rgb(*canvas_pixel);
            (r0.abs_diff(r1) as usize) + (g0.abs_diff(g1) as usize) + (b0.abs_diff(b1) as usize)
        })
}
