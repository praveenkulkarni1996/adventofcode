"""Day 25: Sea Cucumber - https://adventofcode.com/2021/day/25

Part 1: 534
Part 2: Requires the completion of all other problems. 
"""

import argparse
import copy
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)


def parse(datafile: str) -> list[list[str]]:
    with open(datafile) as f:
        return [list(line.strip()) for line in f]


def east(g: list[list[str]]):
    width = len(g[0])
    for rowvalues in g:
        for col, value in enumerate(rowvalues):
            nextcol = 0 if col + 1 == width else col + 1
            if value != '>':
                continue
            if rowvalues[nextcol] != '.':
                continue
            rowvalues[nextcol] = '>>'
            rowvalues[col] = '*'
    for row, rowvalues in enumerate(g):
        for col, value in enumerate(rowvalues):
            g[row][col] = '>' if g[row][col] == '>>' else g[row][col]
            g[row][col] = '.' if g[row][col] == '*' else g[row][col]


def south(g: list[list[str]]):
    height = len(g)
    width = len(g[0])
    for row in range(height):
        nextrow = 0 if row + 1 == height else row + 1
        for col in range(width):
            if g[row][col] != 'v':
                continue
            if g[nextrow][col] != '.':
                continue
            g[nextrow][col] = 'vv'
            g[row][col] = '*'
    for row, rowvalues in enumerate(g):
        for col, _ in enumerate(rowvalues):
            g[row][col] = 'v' if g[row][col] == 'vv' else g[row][col]
            g[row][col] = '.' if g[row][col] == '*' else g[row][col]


def step(g: list[list[str]]) -> bool:
    before = copy.deepcopy(g)
    east(g)
    south(g)
    return g != before


def stoppage(g: list[list[str]]) -> int:
    counts = 1
    while step(g):
        counts += 1
    return counts


def main(args):
    grid = parse(args.datafile)
    answer = stoppage(grid)
    print(f'Part 1: {answer}')


if __name__ == '__main__':
    main(args=parser.parse_args())
