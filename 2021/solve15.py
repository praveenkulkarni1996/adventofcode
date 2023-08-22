"""Solution - Chiton

Link: https://adventofcode.com/2021/day/15
Part 1: 613
Part 2: 2899
"""

import argparse
import heapq
import math
import pathlib
import pprint

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)


def parse(datafile: str) -> list[list[int]]:
    with open(datafile) as f:
        return [[int(digit) for digit in line.strip()] for line in f]


def neighbours(grid: list[list[int]], row: int, col: int):
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    nbrs = [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]
    return [(nrow, ncol) for nrow, ncol in nbrs
            if 0 <= nrow < HEIGHT and 0 <= ncol < WIDTH]


def dijkstra(grid: list[list[int]]) -> int:
    best = [[math.inf for _ in row] for row in grid]
    queue = [(0, (0, 0))]
    best[0][0] = 0
    while queue:
        value, (row, col) = heapq.heappop(queue)
        if value > best[row][col]:
            continue
        for nrow, ncol in neighbours(grid, row, col):
            if best[nrow][ncol] > best[row][col] + grid[nrow][ncol]:
                best[nrow][ncol] = best[row][col] + grid[nrow][ncol]
                heapq.heappush(queue, (best[nrow][ncol], (nrow, ncol)))
    return best[-1][-1]


def expand(grid: list[list[int]]):
    return [[(item + a + b - 1) % 9 + 1 for a in range(5) for item in row]
            for b in range(5) for row in grid]


def main(args):
    grid = parse(args.datafile)
    part1 = dijkstra(grid)
    part2 = dijkstra(expand(grid))
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
