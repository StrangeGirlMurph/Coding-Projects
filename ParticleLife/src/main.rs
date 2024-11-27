use bevy::{prelude::*, sprite::Mesh2dHandle, window::close_on_esc};
use rand::prelude::*;

const WINDOW_RESOLUTION: (f32, f32) = (1000.0, 1000.0);

fn main() {
    App::new()
        .insert_resource(Settings::default())
        .insert_resource(ClearColor(Color::Hsla {
            hue: 360.,
            saturation: 0.,
            lightness: 0.1,
            alpha: 1.,
        }))
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Particle Life".into(),
                resolution: WINDOW_RESOLUTION.into(),
                ..default()
            }),
            ..default()
        }))
        .add_systems(Startup, (setup, generate_particles))
        .add_systems(Update, close_on_esc)
        .add_systems(Update, move_particles)
        .run();
}

fn move_particles(
    settings: Res<Settings>,
    time: Res<Time>,
    mut particles: Query<(&mut Particle, &mut Transform)>,
) {
    let particles_lookup = particles
        .iter()
        .map(|(particle, transform)| (particle.clone(), transform.clone()))
        .collect::<Vec<(Particle, Transform)>>();

    let dt = time.delta_seconds();

    for (mut particle, mut transform) in &mut particles {
        let acceleration = particles_lookup
            .iter()
            .map(|(other_particle, other_transform)| {
                let distance = (transform.translation - other_transform.translation).length();
                let magnitude_force = magnitude_force_function(
                    distance / settings.maximum_radius,
                    settings.attraction_matrix[particle.color][other_particle.color],
                );
                let force = (transform.translation - other_transform.translation).normalize()
                    * magnitude_force;
                force
            })
            .sum::<Vec3>()
            * settings.maximum_radius;

        particle.velocity = (1.0f32 / 2.0).powf(dt / settings.friction_half_time)
            * particle.velocity
            + acceleration * dt;
        transform.translation = transform.translation + particle.velocity * dt;
    }
}

fn generate_particles(
    settings: Res<Settings>,
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<ColorMaterial>>,
) {
    let mut rng = rand::thread_rng();
    let half_resolution_x = WINDOW_RESOLUTION.0 / 2.0;
    let half_resolution_y = WINDOW_RESOLUTION.1 / 2.0;
    let particles: Vec<Particle> = (0..settings.num_particles)
        .map(|_| Particle {
            velocity: Vec3::ZERO,
            color: rng.gen_range(0..settings.num_colors),
        })
        .collect();

    let mesh = Mesh2dHandle(meshes.add(Circle::new(3.0)));

    for particle in particles.into_iter() {
        let material = materials.add(Color::hsla(
            360.0 / settings.num_colors as f32 * particle.color as f32,
            0.8,
            0.5,
            1.0,
        ));
        commands.spawn((
            ColorMesh2dBundle {
                material: material,
                mesh: mesh.clone(),
                transform: Transform::from_translation(Vec3::new(
                    rng.gen_range(-half_resolution_x..=half_resolution_x),
                    rng.gen_range(-half_resolution_y..=half_resolution_y),
                    0.0,
                )),
                ..Default::default()
            },
            particle,
        ));
    }
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2dBundle::default());
}

#[derive(Component, Clone, Copy, Debug)]
struct Particle {
    velocity: Vec3,
    /// 0 <= x < num_colors
    color: usize,
}

#[derive(Resource)]
struct Settings {
    num_particles: usize,
    num_colors: usize,
    attraction_matrix: Vec<Vec<f32>>,
    maximum_radius: f32,
    friction_half_time: f32,
}

impl Default for Settings {
    fn default() -> Self {
        let num_colors = 4;

        Settings {
            num_particles: 10,
            num_colors: num_colors,
            attraction_matrix: vec![vec![0.0; num_colors]; num_colors],
            maximum_radius: 10.0,
            friction_half_time: 0.1,
        }
    }
}

fn magnitude_force_function(distance: f32, attraction_factor: f32) -> f32 {
    let normal_distance = 0.3;

    if distance < normal_distance {
        distance / normal_distance - 1.0
    } else if normal_distance < distance && distance < 1.0 {
        attraction_factor
            * (1.0 - (2.0 * distance - 1.0 - normal_distance).abs() / (1.0 - normal_distance))
    } else {
        0.0
    }
}
