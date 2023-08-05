struct Particle {
    pos: f64,
    vel: f64,
    mass: f64,
}

const DIGITS: u32 = 9;

fn main() {
    let number_of_collisions: u64 = 0;

    let small = Particle {
        pos: 1.0,
        vel: 0.0,
        mass: 1.0,
    };

    let big = Particle {
        pos: 2.0,
        vel: -1.0,
        mass: 100.0_f64.powf((DIGITS - 1) as f64),
    };

    calculate(big, small, number_of_collisions);
}

fn calculate(mut big: Particle, mut small: Particle, mut number_of_collisions: u64) {
    while !(big.vel > small.vel && big.vel > 0.0 && small.vel >= 0.0) {
        if number_of_collisions % 2 == 0 {
            // Collision between particles
            small.pos = (small.pos - big.pos) / (big.vel - small.vel) * small.vel + small.pos;
            big.pos = small.pos;
            particle_collision(&mut big, &mut small);
            number_of_collisions += 1;
        } else {
            // Collision with wall
            small.pos = 0.0;
            big.pos = big.pos + big.vel * small.pos / -small.vel;
            wall_collision(&mut small);
            number_of_collisions += 1;
        }
        if number_of_collisions % 10u64.pow(DIGITS - 2) == 0 {
            println!("Update: {}", number_of_collisions);
        }
    }

    println!("Number of collisions: {}", number_of_collisions);
}

fn wall_collision(particle: &mut Particle) {
    particle.vel *= -1.0;
}

fn particle_collision(big: &mut Particle, small: &mut Particle) {
    let sum = big.mass + small.mass;
    let diff = big.mass - small.mass;
    let temp = big.vel;
    big.vel = (diff * big.vel + 2.0 * small.mass * small.vel) / sum;
    small.vel = (-diff * small.vel + 2.0 * big.mass * temp) / sum;
}
