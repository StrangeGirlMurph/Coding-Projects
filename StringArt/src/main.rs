pub mod lines;
pub mod utils;

use lines::draw_line;
use minifb::{Key, ScaleMode, Window, WindowOptions};
use rayon::prelude::*;
use utils::{extract_rgb, grayscale, rgb, Pixel};

const NODE_SPACING: usize = 8; // number of pixels between nodes
const ROUGH_HEIGHT: usize = 400; // roughly the height of the image

fn main() {
    // Load image
    let (image, width, height) = load_image("resources/road.jpg");

    // Drawing
    let mut window = Window::new(
        "String Art - Press ESC to exit",
        width as usize,
        height as usize,
        WindowOptions {
            resize: true,
            scale_mode: ScaleMode::Center,
            ..WindowOptions::default()
        },
    )
    .expect("Unable to create window :(");

    // Limit to max ~60 fps update rate
    window.limit_update_rate(Some(std::time::Duration::from_micros(16600)));

    // Computation
    let mut canvas: Vec<Vec<u32>> = vec![vec![grayscale(0.0); width]; height];

    let mut nodes: Vec<Pixel> = Vec::new();
    for x in [0, width] {
        for y in (0..=height).step_by(NODE_SPACING) {
            nodes.push(Pixel { x, y });
        }
    }
    for y in [0, height] {
        for x in (NODE_SPACING..=width - NODE_SPACING).step_by(NODE_SPACING) {
            nodes.push(Pixel { x, y });
        }
    }

    let mut previous = 0;
    let mut current = 0;

    while window.is_open() && !window.is_key_down(Key::Escape) && !window.is_key_down(Key::Q) {
        let mut best: (usize, f64, Vec<Vec<u32>>) = (0, f64::INFINITY, vec![vec![]]);
        for (index, node) in nodes.iter().enumerate() {
            if index == current
                || index == previous
                || (nodes[current].x == node.x
                    && nodes[current].x % width == 0
                    && node.x % width == 0)
                || (nodes[current].y == node.y
                    && nodes[current].y % height == 0
                    && node.y % height == 0)
            {
                continue;
            }

            let mut clone = canvas.clone();
            let touched = draw_line(&mut clone, nodes[current], *node, grayscale(1.0), 0.4);
            //for pixel in touched {}

            let diff = distance(&image, &flatten(&clone));
            if diff < best.1 {
                //println!("New best: {:?}", node);
                best = (index, diff, clone);
            }
        }

        //println!("{} - {}", best.1, distance(&image, &flatten(&canvas)));
        /* if best.1 >= distance(&image, &flatten(&canvas)) {
            break;
        } */

        previous = current;
        current = best.0;
        canvas = best.2;

        window
            .update_with_buffer(&flatten(&canvas), width as usize, height as usize)
            .unwrap();
    }
}

fn distance(v1: &Vec<u32>, v2: &Vec<u32>) -> f64 {
    (v1.par_iter()
        .zip(v2.par_iter())
        .map(|(&x, &y)| {
            let (r0, g0, b0) = extract_rgb(x);
            let (r1, g1, b1) = extract_rgb(y);
            r0.abs_diff(r1) as u64 + g0.abs_diff(g1) as u64 + b0.abs_diff(b1) as u64
        })
        .sum::<u64>() as f64)
        .sqrt()
}

fn flatten(vec: &Vec<Vec<u32>>) -> Vec<u32> {
    vec.clone().into_par_iter().flatten().collect()
}

fn load_image(path: &str) -> (Vec<u32>, usize, usize) {
    let mut img = image::open(path).expect("Failed to open image");
    println!("Image size: {}x{}", img.width(), img.height());
    img = img.resize(
        (ROUGH_HEIGHT + ROUGH_HEIGHT % NODE_SPACING) as u32,
        (ROUGH_HEIGHT + ROUGH_HEIGHT % NODE_SPACING) as u32,
        image::imageops::FilterType::Triangle,
    );
    img = img.crop(
        img.width() % NODE_SPACING as u32 / 2,
        img.height() % NODE_SPACING as u32 / 2,
        img.width() - img.width() % NODE_SPACING as u32,
        img.height() - img.height() % NODE_SPACING as u32,
    );

    let (width, height) = (img.width() as usize, img.height() as usize);
    let image: Vec<u32> = img
        .grayscale()
        .to_rgb8()
        .enumerate_pixels()
        .map(|(_, _, p)| rgb(p[0], p[1], p[2]))
        .collect();

    println!(
        "Image size after scaling and cropping: {}x{}",
        width, height
    );

    (image, width, height)
}
