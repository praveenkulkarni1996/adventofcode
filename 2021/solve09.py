"""Solution - Smoke Basin

Link: https://adventofcode.com/2021/day/9 
Part 1: 577
Part 2: 1069200
"""

from typing import TypeAlias, Iterator

import argparse
import itertools
import pathlib

parser = argparse.ArgumentParser(prog='Smoke Basin')
parser.add_argument('datafile', type=pathlib.Path)


def parse(datafile: str) -> list[list[int]]:

    def extract(intstring: str) -> list[int]:
        return [int(digit) for digit in list(intstring.strip())]

    with open(datafile) as f:
        return [extract(line) for line in f]


Pos: TypeAlias = tuple[int, int]


def minimas(grid: list[list[int]]) -> Iterator[Pos]:
    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    def is_minima(row: int, col: int) -> bool:
        value = grid[row][col]
        nbrs = ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        for nrow, ncol in nbrs:
            if 0 <= nrow < HEIGHT and 0 <= ncol < WIDTH:
                if grid[nrow][ncol] <= value:
                    return False
        return True

    for row, rowlist in enumerate(grid):
        for col, value in enumerate(rowlist):
            if is_minima(row, col):
                yield (row, col)


def basin(grid: list[list[int]], src: Pos) -> int:
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    seen: set[Pos] = {src}

    def dfs(row: int, col: int):
        nbrs = ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        for nrow, ncol in nbrs:
            if not (0 <= nrow < HEIGHT):
                continue
            if not (0 <= ncol < WIDTH):
                continue
            if (nrow, ncol) in seen:
                continue
            if grid[row][col] <= grid[nrow][ncol] < 9:
                seen.add((nrow, ncol))
                dfs(nrow, ncol)

    dfs(*src)
    return len(seen)


def main(args):
    heightmap = parse(args.datafile)
    lowests = list(minimas(heightmap))
    risk = sum(heightmap[row][col] + 1 for row, col in lowests)
    print(f'Part 1: {risk}')

    scores = [basin(heightmap, pos) for pos in lowests]
    (a, b, c) = sorted(scores, reverse=True)[:3]
    print(f'Part 2: {a * b * c}')


if __name__ == '__main__':
    main(args=parser.parse_args())
