use crate::game_of_life::game_of_life_step;
use crate::grid::Grid;
mod game_of_life;
mod grid;
mod helpers;

use bevy::asset::RenderAssetUsages;
use bevy::image::ImageSamplerDescriptor;
use bevy::input::common_conditions::input_toggle_active;
use bevy::prelude::*;
use bevy::render::render_resource::{Extent3d, TextureDimension, TextureFormat};
use bevy::window::{Monitor, WindowResolution};
use helpers::get_inputs;
use rayon::prelude::*;

fn main() {
    let (w, h) = get_inputs();

    App::new()
        .insert_resource(Grid::new(w, h))
        .insert_resource(Window {
            width: 0,
            height: 0,
        })
        .insert_resource(Stats {
            step: 0,
            alive_cells: 0,
            dead_cells: 0,
        })
        .insert_resource(Time::<Fixed>::from_seconds(0.15))
        .add_plugins((DefaultPlugins.set(WindowPlugin {
            primary_window: Some(bevy::prelude::Window {
                title: "Cellular Automata".into(),
                visible: false,
                resizable: false,
                resolution: WindowResolution::new(1000.0, 1000.0).with_scale_factor_override(1.0),
                //position: WindowPosition::At(IVec2::new(0, 0)),
                ..default()
            }),
            ..default()
        }),))
        .add_systems(Startup, setup)
        .add_systems(Update, toggle_pause)
        .add_systems(FixedUpdate, loooop)
        .run();
}

fn setup(
    mut commands: Commands,
    monitor: Single<&Monitor>,
    mut window: Single<&mut bevy::prelude::Window>,
    mut win: ResMut<Window>,
    mut grid: ResMut<Grid>,
    mut images: ResMut<Assets<Image>>,
) {
    let ratio = grid.width as f32 / grid.height as f32;
    let monitor_ratio = monitor.physical_width as f32 / monitor.physical_height as f32;
    let (width, height) = if ratio > monitor_ratio {
        let width = monitor.physical_width - 100;
        (width, (width as f32 / ratio) as u32)
    } else {
        let height = monitor.physical_height - 100;
        ((height as f32 * ratio) as u32, height)
    };
    window.resolution.set_scale_factor_override(Some(1.0));
    window.resolution.set_physical_resolution(width, height);
    window.visible = true;

    win.width = width;
    win.height = height;
    grid.size = width as f32 / grid.width as f32;

    let mut image = Image::new_fill(
        Extent3d {
            width: grid.width as u32,
            height: grid.height as u32,
            depth_or_array_layers: 1,
        },
        TextureDimension::D2,
        &[0, 0, 0, 255], // Default color (Black, full alpha)
        TextureFormat::Rgba8UnormSrgb,
        RenderAssetUsages::MAIN_WORLD | RenderAssetUsages::RENDER_WORLD,
    );

    image.sampler = bevy::image::ImageSampler::Descriptor(ImageSamplerDescriptor::nearest());

    let image_handle = images.add(image);
    commands.insert_resource(GridTexture(image_handle.clone()));

    commands.spawn((
        Sprite::from_image(image_handle),
        Transform::from_scale(Vec3::splat(grid.size)),
    ));

    commands.spawn(Camera2d);
}

fn loooop(
    mut images: ResMut<Assets<Image>>,
    mut grid: ResMut<Grid>,
    mut stats: ResMut<Stats>,
    grid_texture: Res<GridTexture>,
) {
    stats.step += 1;

    game_of_life_step(&mut grid);

    let image_data = images
        .get_mut(&grid_texture.0)
        .unwrap()
        .data
        .as_mut()
        .unwrap();

    for (i, cell_is_alive) in grid.iter().enumerate() {
        let pixel_index = i * 4;

        if cell_is_alive {
            // White for alive
            stats.alive_cells += 1;
            image_data[pixel_index] = 255; // R
            image_data[pixel_index + 1] = 255; // G
            image_data[pixel_index + 2] = 255; // B
        } else {
            // Black for dead
            image_data[pixel_index] = 0; // R
            image_data[pixel_index + 1] = 0; // G
            image_data[pixel_index + 2] = 0; // B
        }
        // Alpha remains 255
    }

    stats.dead_cells = grid.width * grid.height - stats.alive_cells;
}

fn toggle_pause(keys: Res<ButtonInput<KeyCode>>, mut time: ResMut<Time<Virtual>>) {
    if keys.just_pressed(KeyCode::Space) {
        if time.is_paused() {
            time.unpause();
        } else {
            time.pause();
        }
    }
}

#[derive(Resource)]
struct GridTexture(Handle<Image>);

#[derive(Resource)]
struct Window {
    width: u32,
    height: u32,
}

#[derive(Resource)]
struct Stats {
    step: usize,
    alive_cells: usize,
    dead_cells: usize,
}
