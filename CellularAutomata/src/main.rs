use crate::game_of_life::game_of_life_step;
use crate::grid::Grid;
mod game_of_life;
mod grid;
mod helpers;

use bevy::input::common_conditions::input_toggle_active;
use bevy::prelude::*;
use bevy::window::{Monitor, WindowResolution};
use helpers::get_inputs;

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
        .insert_resource(Time::<Fixed>::from_seconds(0.2))
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(bevy::prelude::Window {
                title: "Cellular Automata".into(),
                visible: false,
                resizable: false,
                resolution: WindowResolution::new(1000.0, 1000.0).with_scale_factor_override(1.0),
                //position: WindowPosition::At(IVec2::new(0, 0)),
                ..default()
            }),
            ..default()
        }))
        .add_systems(Startup, setup)
        .add_systems(
            FixedUpdate,
            loooop.run_if(input_toggle_active(true, KeyCode::Space)),
        )
        .run();
}

fn setup(
    mut commands: Commands,
    monitor: Single<&Monitor>,
    mut window: Single<&mut bevy::prelude::Window>,
    mut win: ResMut<Window>,
    mut grid: ResMut<Grid>,
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

    commands.spawn(Camera2d);
}

fn loooop(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<ColorMaterial>>,
    mut grid: ResMut<Grid>,
    mut stats: ResMut<Stats>,
    window: Res<Window>,
    cells: Query<Entity, With<CellMarker>>,
) {
    for entity in &cells {
        commands.entity(entity).despawn();
    }

    let color = Color::hsl(0.0, 0.0, 1.0);
    let mesh = meshes.add(Rectangle::new(grid.size, grid.size));
    let material = materials.add(color);

    stats.step += 1;
    let mut dead_cells = 0;

    game_of_life_step(&mut grid);
    for (i, cell) in grid.iter().enumerate() {
        let alive = cell;
        if !alive {
            dead_cells += 1;
            continue;
        }

        let (x, y) = grid.index_to_xy(i);
        let x = x as f32 * grid.size - window.width as f32 / 2.0;
        let y = y as f32 * grid.size - window.height as f32 / 2.0;

        commands.spawn((
            Mesh2d(mesh.clone()),
            MeshMaterial2d(material.clone()),
            Transform::from_xyz(x + grid.size / 2.0, y + grid.size / 2.0, 0.0),
            CellMarker,
        ));
    }

    stats.dead_cells = dead_cells;
    stats.alive_cells = grid.width * grid.height - dead_cells
}

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

#[derive(Component)]
struct CellMarker;
