use bevy::prelude::*;
use rayon::prelude::*;

pub const BASE: usize = 8;

pub const NEIGHBORS_IN_2D: [(isize, isize); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
];

#[derive(Resource, Clone)]
pub struct Grid {
    pub raw: Vec<u8>,
    /// In cells
    pub width: usize,
    /// In cells
    pub height: usize,
    /// In pixels
    pub size: f32,
}

impl Grid {
    pub fn new(width: usize, height: usize) -> Grid {
        Grid {
            raw: (0..(width * height).div_ceil(8))
                .map(|_| rand::random::<u8>())
                .collect(),
            width,
            height,
            size: 0.0,
        }
    }

    pub fn iter(&self) -> impl Iterator<Item = bool> {
        self.raw
            .iter()
            .flat_map(|el| Self::bits_to_bool_iter(el))
            .take(self.width * self.height)
    }

    pub fn par_iter(&self) -> impl IndexedParallelIterator<Item = bool> {
        (0..self.width * self.height).into_par_iter().map(move |i| {
            let block_index = i / BASE;
            let index_in_block = i % 8;
            let block = self.raw[block_index];
            (block >> (7 - index_in_block)) & 1 == 1
        })
    }

    pub fn par_iter_bits(&self) -> impl IndexedParallelIterator<Item = &u8> {
        self.raw.par_iter()
    }

    pub fn index_to_xy(&self, i: usize) -> (usize, usize) {
        (i % self.width, i / self.width)
    }

    pub fn set(&mut self, i: usize, alive: bool) {
        let block_index = i / BASE;
        let block = self.raw[block_index];
        let index_in_block = i % 8; // from left
        let bit_at_position = 1 << (7 - index_in_block);
        let current = (block & bit_at_position) != 0;
        if !current && alive {
            self.raw[block_index] |= bit_at_position;
        } else if current && !alive {
            self.raw[block_index] ^= bit_at_position;
        }
    }

    pub fn get(&self, x: usize, y: usize) -> bool {
        let index_in_chain = y * self.width + x;
        let block = self.raw[index_in_chain / BASE];
        let index_in_block = index_in_chain % 8;
        (block >> (7 - index_in_block)) & 1 == 1
    }

    pub fn bits_to_bool_iter(el: &u8) -> impl Iterator<Item = bool> {
        (0..=7).rev().map(move |n| (el & (1 << n)) != 0)
    }

    pub fn bits_to_bools(el: &u8) -> Vec<bool> {
        (0..=7).rev().map(|n| (el & (1 << n)) != 0).collect()
    }

    pub fn bools_to_bits(bools: Vec<bool>) -> u8 {
        let mut bits = 0;
        for i in bools
            .iter()
            .enumerate()
            .filter_map(|(i, el)| if *el { Some(i) } else { None })
        {
            bits |= 1 << (7 - i)
        }

        bits
    }

    pub fn bool_iter_to_bits(bools: impl Iterator<Item = bool>) -> u8 {
        let mut bits = 0;
        for i in bools
            .enumerate()
            .filter_map(|(i, el)| if el { Some(i) } else { None })
        {
            bits |= 1 << (7 - i)
        }

        bits
    }
}
