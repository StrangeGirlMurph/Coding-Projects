use ndarray::{Array2, Zip};
use rayon::prelude::*;

pub fn plot(
    canvas: &mut Array2<u32>,
    boolean_mask: &Array2<bool>,
    alpha_mask: &Array2<f64>,
    color: u32,
    alpha: f64,
) {
    Zip::from(canvas)
        .and(alpha_mask)
        .and(boolean_mask)
        .into_par_iter()
        .filter(|(_, _, boolean)| **boolean)
        .for_each(|(canvas_pixel, alpha_pixel, _)| {
            *canvas_pixel = blend_colors(*canvas_pixel, color, *alpha_pixel * alpha);
        });
}

pub fn extract_rgb(color: u32) -> (u8, u8, u8) {
    let r = ((color >> 16) & 0xFF) as u8;
    let g = ((color >> 8) & 0xFF) as u8;
    let b = (color & 0xFF) as u8;
    (r, g, b)
}

pub fn blend_colors(old: u32, new: u32, alpha: f64) -> u32 {
    let (old_r, old_g, old_b) = extract_rgb(old);
    let (new_r, new_g, new_b) = extract_rgb(new);

    let new_r = (old_r as f64 * (1.0 - alpha) + alpha * new_r as f64).round() as u8;
    let new_g = (old_g as f64 * (1.0 - alpha) + alpha * new_g as f64).round() as u8;
    let new_b = (old_b as f64 * (1.0 - alpha) + alpha * new_b as f64).round() as u8;

    rgb(new_r, new_g, new_b)
}

pub fn rgb(r: u8, g: u8, b: u8) -> u32 {
    let (r, g, b) = (r as u32, g as u32, b as u32);
    (r << 16) | (g << 8) | b
}

pub fn grayscale(value: f64) -> u32 {
    let value = (value * 255.0) as u8;
    rgb(value, value, value)
}

use crate::MAX_SIZE;

pub fn load_image(path: &str) -> Array2<u32> {
    let mut img = image::open(path).expect("Failed to open image");
    println!("Image size: {}x{}", img.width(), img.height());

    let min = u32::min(img.height(), img.width());
    img = img.crop(img.width() % min / 2, img.height() % min / 2, min, min);

    if img.width() as usize > MAX_SIZE {
        img = img.resize(
            MAX_SIZE as u32,
            MAX_SIZE as u32,
            image::imageops::FilterType::Triangle,
        );
    }

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

    Array2::from_shape_vec((width, height), image).expect("Failed to create array from image...")
}

/// A pixel on the screen. The origin (0, 0) is at the top left.
#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub struct Pixel {
    pub x: usize,
    pub y: usize,
}

#[derive(Debug, Copy, Clone)]
pub struct Position {
    pub x: f64,
    pub y: f64,
}

impl Position {
    pub fn mul(self, mul: usize) -> Self {
        Position {
            x: self.x * mul as f64,
            y: self.y * mul as f64,
        }
    }
}
