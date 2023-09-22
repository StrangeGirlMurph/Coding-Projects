use crate::utils::Position;
use ndarray::{Array2, Dim};

/// <https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm>
pub fn calculate_line(
    canvas_shape: &Dim<[usize; 2]>,
    start: Position,
    end: Position,
) -> (Array2<f64>, Array2<bool>) {
    let mut alpha_mask = Array2::<f64>::zeros(*canvas_shape);
    let mut boolean_mask = Array2::<bool>::from_elem(*canvas_shape, false);

    let mut add = |i: [usize; 2], alpha: f64| {
        if i[0] < canvas_shape[0] && i[1] < canvas_shape[1] {
            alpha_mask[[i[1], i[0]]] = alpha;
            boolean_mask[[i[1], i[0]]] = true;
        }
    };

    let mut x0 = start.x;
    let mut y0 = start.y;
    let mut x1 = end.x;
    let mut y1 = end.y;
    let steep = (y1 - y0).abs() > (x1 - x0).abs();

    if steep {
        (x0, y0, x1, y1) = (y0, x0, y1, x1);
    }

    if x0 > x1 {
        (x0, y0, x1, y1) = (x1, y1, x0, y0);
    }

    let dx = x1 - x0;
    let dy = y1 - y0;

    let gradient = if dx == 0.0 { 1.0 } else { dy / dx };

    let xend = x0.round() as usize;
    let yend = y0 + gradient * (xend as f64 - x0);
    let xgap = rfpart(x0 + 0.5);
    let xpxl1 = xend;
    let ypxl1 = ipart(yend);

    if steep {
        add([ypxl1, xpxl1], rfpart(yend) * xgap);
        add([ypxl1 + 1, xpxl1], fpart(yend) * xgap);
    } else {
        add([xpxl1, ypxl1], rfpart(yend) * xgap);
        add([xpxl1, ypxl1 + 1], fpart(yend) * xgap);
    }

    let mut intery = yend + gradient;

    let xend = x1.round() as usize;
    let yend = y1 + gradient * (xend as f64 - x1);
    let xgap = fpart(x1 + 0.5);
    let xpxl2 = xend;
    let ypxl2 = ipart(yend);

    if steep {
        add([ypxl2, xpxl2], rfpart(yend) * xgap);
        add([ypxl2 + 1, xpxl2], fpart(yend) * xgap);
    } else {
        add([xpxl2, ypxl2], rfpart(yend) * xgap);
        add([xpxl2, ypxl2 + 1], fpart(yend) * xgap);
    }

    if steep {
        for x in xpxl1 + 1..xpxl2 {
            add([ipart(intery), x], rfpart(intery));
            add([ipart(intery) + 1, x], fpart(intery));
            intery += gradient;
        }
    } else {
        for x in xpxl1 + 1..xpxl2 {
            add([x, ipart(intery)], rfpart(intery));
            add([x, ipart(intery) + 1], fpart(intery));
            intery += gradient;
        }
    }

    (alpha_mask, boolean_mask)
}

fn ipart(x: f64) -> usize {
    x.floor() as usize
}

fn fpart(x: f64) -> f64 {
    x - x.floor()
}

fn rfpart(x: f64) -> f64 {
    1.0 - fpart(x)
}
