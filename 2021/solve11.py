"""Solution - Dumbo Octopus

Link: https://adventofcode.com/2021/day/11 
Part 1: 1773
Part 2: 494
"""
from typing import TypeAlias

import copy
import argparse
import collections
import itertools
import pathlib

parser = argparse.ArgumentParser(prog='Dumbo Octopus')
parser.add_argument('datafile', type=pathlib.Path)

Grid: TypeAlias = list[list[int]]
GRID_LENGTH = 10


def add(g: Grid) -> Grid:
    return [[value + 1 for value in row] for row in g]


def neighbours(row: int, col: int) -> list[tuple[int, int]]:
    nbrs = [
        (row - 1, col - 1),
        (row, col - 1),
        (row + 1, col - 1),
        (row - 1, col),
        (row + 1, col),
        (row - 1, col + 1),
        (row, col + 1),
        (row + 1, col + 1),
    ]
    return [(nrow, ncol) for nrow, ncol in nbrs
            if 0 <= nrow < GRID_LENGTH and 0 <= ncol < GRID_LENGTH]


def flash(g: Grid) -> int:
    f = [[False for _ in row] for row in g]
    q = collections.deque([])

    def flash(row: int, col: int):
        for nrow, ncol in neighbours(row, col):
            g[nrow][ncol] += 1
            if g[nrow][ncol] > 9 and not f[nrow][ncol]:
                f[nrow][ncol] = True
                q.append((nrow, ncol))

    for row, rowvalues in enumerate(g):
        for col, _ in enumerate(rowvalues):
            g[row][col] += 1

    for row, rowvalues in enumerate(g):
        for col, value in enumerate(rowvalues):
            if g[row][col] > 9:
                f[row][col] = True
                q.append((row, col))

    while q:
        row, col = q.popleft()
        flash(row, col)

    for row, rowvalues in enumerate(g):
        for col, _ in enumerate(rowvalues):
            g[row][col] = 0 if f[row][col] else g[row][col]

    return sum(did_flash for row in f for did_flash in row)


def parse(datafile: str) -> Grid:
    with open(datafile) as f:
        return [[int(digit) for digit in intstring.strip()] for intstring in f]


def flashes_100_epochs(g: Grid) -> int:
    return sum(flash(g) for _ in range(100))


def all_flash_epoch(g: Grid) -> int:
    for epoch in itertools.count(1):
        if flash(g) == GRID_LENGTH * GRID_LENGTH:
            return epoch


def main(args):
    grid = parse(args.datafile)
    part1: int = flashes_100_epochs(copy.deepcopy(grid))
    part2: int = all_flash_epoch(grid)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
