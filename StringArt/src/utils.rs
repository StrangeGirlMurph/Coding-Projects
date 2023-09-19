pub fn plot(canvas: &mut Vec<Vec<u32>>, pixel: &Pixel, color: u32, alpha: f64) {
    if pixel.x < canvas[0].len() && pixel.y < canvas.len() {
        let old_color = &mut canvas[pixel.y][pixel.x];
        *old_color = blend_colors(*old_color, color, alpha);
    }
}

pub fn extract_rgb(color: u32) -> (u8, u8, u8) {
    let r = ((color >> 16) & 0xFF) as u8;
    let g = ((color >> 8) & 0xFF) as u8;
    let b = (color & 0xFF) as u8;
    (r, g, b)
}

fn blend_colors(old: u32, new: u32, alpha: f64) -> u32 {
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

/// A pixel on the screen. The origin (0, 0) is at the top left.
#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub struct Pixel {
    pub x: usize,
    pub y: usize,
}
