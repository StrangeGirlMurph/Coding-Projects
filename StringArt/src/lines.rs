use crate::utils::{plot, Pixel};

fn ipart(x: f64) -> usize {
    x.floor() as usize
}

fn fpart(x: f64) -> f64 {
    x - x.floor()
}

fn rfpart(x: f64) -> f64 {
    1.0 - fpart(x)
}

pub fn draw_line(
    canvas: &mut Vec<Vec<u32>>,
    start: Pixel,
    end: Pixel,
    color: u32,
    alpha: f64,
) -> Vec<Pixel> {
    let x0 = start.x;
    let y0 = start.y;
    let x1 = end.x;
    let y1 = end.y;
    let steep = y0.abs_diff(y1) > x0.abs_diff(x1);

    let (mut x0, mut y0, mut x1, mut y1) = if steep {
        (y0, x0, y1, x1)
    } else {
        (x0, y0, x1, y1)
    };

    if x0 > x1 {
        std::mem::swap(&mut x0, &mut x1);
        std::mem::swap(&mut y0, &mut y1);
    }

    let dx = x1 as i32 - x0 as i32;
    let dy = y1 as i32 - y0 as i32;

    let gradient = if dx == 0 { 1.0 } else { dy as f64 / dx as f64 };

    let xend = x0;
    let yend = y0 as f64 + gradient * (xend as f64 - x0 as f64);
    let xgap = rfpart(x0 as f64 + 0.5);
    let xpxl1 = xend;
    let ypxl1 = ipart(yend);

    let mut touched: Vec<Pixel> = Vec::new();

    if steep {
        plot(
            canvas,
            &Pixel { x: ypxl1, y: xpxl1 },
            color,
            rfpart(yend) * xgap * alpha,
        );
        plot(
            canvas,
            &Pixel {
                x: ypxl1 + 1,
                y: xpxl1,
            },
            color,
            fpart(yend) * xgap * alpha,
        );
        touched.push(Pixel { x: ypxl1, y: xpxl1 });
        touched.push(Pixel {
            x: ypxl1 + 1,
            y: xpxl1,
        });
    } else {
        plot(
            canvas,
            &Pixel { x: xpxl1, y: ypxl1 },
            color,
            rfpart(yend) * xgap * alpha,
        );
        plot(
            canvas,
            &Pixel {
                x: xpxl1,
                y: ypxl1 + 1,
            },
            color,
            fpart(yend) * xgap * alpha,
        );
        touched.push(Pixel { x: xpxl1, y: ypxl1 });
        touched.push(Pixel {
            x: xpxl1,
            y: ypxl1 + 1,
        });
    }

    let mut intery = yend + gradient;

    let xend = x1;
    let yend = y1 as f64 + gradient * (xend as f64 - x1 as f64);
    let xgap = fpart(x1 as f64 + 0.5);
    let xpxl2 = xend;
    let ypxl2 = ipart(yend);

    if steep {
        plot(
            canvas,
            &Pixel { x: ypxl2, y: xpxl2 },
            color,
            rfpart(yend) * xgap * alpha,
        );
        plot(
            canvas,
            &Pixel {
                x: ypxl2 + 1,
                y: xpxl2,
            },
            color,
            fpart(yend) * xgap * alpha,
        );
        touched.push(Pixel { x: ypxl2, y: xpxl2 });
        touched.push(Pixel {
            x: ypxl2 + 1,
            y: xpxl2,
        });
    } else {
        plot(
            canvas,
            &Pixel { x: xpxl2, y: ypxl2 },
            color,
            rfpart(yend) * xgap * alpha,
        );
        plot(
            canvas,
            &Pixel {
                x: xpxl2,
                y: ypxl2 + 1,
            },
            color,
            fpart(yend) * xgap * alpha,
        );
        touched.push(Pixel { x: xpxl2, y: ypxl2 });
        touched.push(Pixel {
            x: xpxl2,
            y: ypxl2 + 1,
        });
    }

    if steep {
        for x in xpxl1 + 1..xpxl2 {
            plot(
                canvas,
                &Pixel {
                    x: ipart(intery),
                    y: x,
                },
                color,
                rfpart(intery) * alpha,
            );
            plot(
                canvas,
                &Pixel {
                    x: ipart(intery) + 1,
                    y: x,
                },
                color,
                fpart(intery) * alpha,
            );
            touched.push(Pixel {
                x: ipart(intery),
                y: x,
            });
            touched.push(Pixel {
                x: ipart(intery) + 1,
                y: x,
            });
            intery += gradient;
        }
    } else {
        for x in xpxl1 + 1..xpxl2 {
            plot(
                canvas,
                &Pixel {
                    x,
                    y: ipart(intery),
                },
                color,
                rfpart(intery) * alpha,
            );
            plot(
                canvas,
                &Pixel {
                    x,
                    y: ipart(intery) + 1,
                },
                color,
                fpart(intery) * alpha,
            );
            touched.push(Pixel {
                x,
                y: ipart(intery),
            });
            touched.push(Pixel {
                x,
                y: ipart(intery) + 1,
            });
            intery += gradient;
        }
    }

    touched
}
