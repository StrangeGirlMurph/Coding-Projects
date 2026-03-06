use std::env;
use std::io;
use std::io::Write;

pub fn get_inputs() -> (usize, usize) {
    let args: Vec<String> = env::args().skip(1).collect();

    if args.len() == 0 {
        print!(
            "Do you want to configure your own grid (instead of using the default 1000x1000 grid)? (Y/n) "
        );
        let _ = io::stdout().flush();

        let mut answer = String::new();
        io::stdin()
            .read_line(&mut answer)
            .expect("Failed to read line");

        if answer.trim().to_lowercase() == "n" {
            return (1000, 1000);
        }

        let mut w = String::new();
        let mut h = String::new();

        print!("What width should the grid have? (in cells) ");
        let _ = io::stdout().flush();

        io::stdin().read_line(&mut w).expect("Failed to read line");

        print!("What height should the grid have? (in cells) ");
        let _ = io::stdout().flush();

        io::stdin().read_line(&mut h).expect("Failed to read line");

        let w: usize = w.trim().parse().expect("Please enter a valid number...");
        let h: usize = h.trim().parse().expect("Please enter a valid number...");

        return (w, h);
    } else if args.len() == 2 {
        let w: usize = args[0]
            .trim()
            .parse()
            .expect("That's not a valid number...");
        let h: usize = args[1]
            .trim()
            .parse()
            .expect("That's not a valid number...");

        return (w, h);
    } else {
        println!("{:?}", args);
        panic!(
            "Either add two arguments for the width and height of the grid in cells or no argument. I can't interpret what you gave me."
        )
    }
}
