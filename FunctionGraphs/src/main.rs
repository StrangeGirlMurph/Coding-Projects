use bevy::prelude::*;
use bevy_polyline::prelude::*;
use std::ops::RangeInclusive;
use rayon::prelude::*;

fn main() {
    App::new()
        .insert_resource(ClearColor(Color::WHITE))
        .add_plugins(DefaultPlugins)
        .add_plugin(PolylinePlugin)
        .add_startup_system(setup)
        .run();
}

fn setup(
    mut commands: Commands,
    mut polyline_materials: ResMut<Assets<PolylineMaterial>>,
    mut polylines: ResMut<Assets<Polyline>>,
) {
    // Enter the function to plot here:
    fn f(x: f32) -> f32 {
        x.sin()
    }

    // Enter the range to plot here:
    let range = FloatRange {
        start: -8.0,
        end: 8.0,
        step: 0.1,
    };

    let plot_material = polyline_materials.add(PolylineMaterial {
        width: 3.0,
        color: Color::LIME_GREEN,
        ..default()
    });

    for (a, b) in range.zip(range.skip(1)) {
        commands.spawn(PolylineBundle {
            polyline: polylines.add(Polyline {
                vertices: vec![Vec3::new(a, f(a), 0.0), Vec3::new(b, f(b), 0.0)],
            }),
            material: plot_material.clone(),
            ..default()
        });
    }

    let axis_material = polyline_materials.add(PolylineMaterial {
        width: 2.5,
        color: Color::BLACK,
        ..default()
    });

    // Axis
    commands.spawn(PolylineBundle {
        polyline: polylines.add(Polyline {
            vertices: vec![
                Vec3::new(range.start, 0.0, 0.0),
                Vec3::new(range.end, 0.0, 0.0),
            ],
        }),
        material: axis_material.clone(),
        ..default()
    });

    commands.spawn(PolylineBundle {
        polyline: polylines.add(Polyline {
            vertices: vec![Vec3::new(0.0, -10.0, 0.0), Vec3::new(0.0, 10.0, 0.0)],
        }),
        material: axis_material.clone(),
        ..default()
    });

    // Grid
    let grid_material = polyline_materials.add(PolylineMaterial {
        width: 1.0,
        color: Color::GRAY,
        ..default()
    });

    let grid_material_light = polyline_materials.add(PolylineMaterial {
        width: 0.5,
        color: Color::GRAY,
        ..default()
    });

    let grid_range_x = RangeInclusive::new(range.start.floor() as i32, range.end.ceil() as i32);
    let grid_range_y = RangeInclusive::new(-10, 10);

    for x in grid_range_x.clone() {
        commands.spawn(PolylineBundle {
            polyline: polylines.add(Polyline {
                vertices: vec![
                    Vec3::new(x as f32, *grid_range_y.start() as f32, 0.0),
                    Vec3::new(x as f32, *grid_range_y.end() as f32, 0.0),
                ],
            }),
            material: grid_material.clone(),
            ..default()
        });
        commands.spawn(PolylineBundle {
            polyline: polylines.add(Polyline {
                vertices: vec![
                    Vec3::new(x as f32 + 0.5, *grid_range_y.start() as f32, 0.0),
                    Vec3::new(x as f32 + 0.5, *grid_range_y.end() as f32, 0.0),
                ],
            }),
            material: grid_material_light.clone(),
            ..default()
        });
    }

    for y in grid_range_y {
        commands.spawn(PolylineBundle {
            polyline: polylines.add(Polyline {
                vertices: vec![
                    Vec3::new(*grid_range_x.start() as f32, y as f32, 0.0),
                    Vec3::new(*grid_range_x.end() as f32, y as f32, 0.0),
                ],
            }),
            material: grid_material.clone(),
            ..default()
        });
        commands.spawn(PolylineBundle {
            polyline: polylines.add(Polyline {
                vertices: vec![
                    Vec3::new(*grid_range_x.start() as f32, y as f32 + 0.5, 0.0),
                    Vec3::new(*grid_range_x.end() as f32, y as f32 + 0.5, 0.0),
                ],
            }),
            material: grid_material_light.clone(),
            ..default()
        });
    }

    // Camera
    commands.spawn(Camera3dBundle {
        transform: Transform::from_xyz(0.0, 0.0, 10.0).looking_at(Vec3::ZERO, Vec3::Y),
        camera: Camera { ..default() },
        ..default()
    });
}

#[derive(Copy, Clone)]
struct FloatRange {
    start: f32,
    end: f32,
    step: f32,
}

impl Iterator for FloatRange {
    type Item = f32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.start < self.end {
            let current = self.start;
            self.start += self.step;
            Some(current)
        } else {
            None
        }
    }
}
