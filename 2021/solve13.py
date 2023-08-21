"""Solution - Transparent Origami

Link: https://adventofcode.com/2021/day/13
Part 1: 724
Part 2: CPJBERUL
"""

import argparse
import collections
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)

Dot = collections.namedtuple('Dot', ['x', 'y'])
Fold = collections.namedtuple('Fold', ['var', 'value'])


def read_dot(csv: str) -> Dot:
    [x, y] = [int(num) for num in csv.strip().split(',')]
    return Dot(x=x, y=y)


def read_fold(instruction: str) -> Fold:
    _, linegraph = instruction.rsplit(' ', maxsplit=1)
    variable, valuestr = linegraph.split('=')
    return Fold(variable, int(valuestr))


def parse(datafile: str) -> tuple[list[Dot], list[Fold]]:
    with open(datafile) as f:
        pointfile, foldfile = f.read().split('\n\n')
    dots = [read_dot(line) for line in pointfile.split('\n')]
    folds = [read_fold(line) for line in foldfile.split('\n')]
    return dots, folds


def mirror(spot: int, glass: int) -> int:
    return spot if spot < glass else 2 * glass - spot


def dotfold(dot: Dot, fold: Fold) -> Dot:
    if fold.var == 'x':
        return Dot(x=mirror(dot.x, fold.value), y=dot.y)
    if fold.var == 'y':
        return Dot(x=dot.x, y=mirror(dot.y, fold.value))
    raise ValueError('incorrect folding.')


def singlefold(dots: set[Dot], fold: Fold) -> set[Dot]:
    return {dotfold(dot, fold) for dot in dots}


def multifolds(dots: set[Dot], folds: list[Fold]) -> set[Dot]:
    for fold in folds:
        dots = singlefold(dots, fold)
    return dots


def draw(dots: set[Dot]):
    width = max(dot.x for dot in dots)
    height = max(dot.y for dot in dots)
    screen = [[' ' for _ in range(width + 1)] for _ in range(height + 1)]
    for dot in dots:
        screen[dot.y][dot.x] = '#'
    return '\n'.join((''.join(char for char in row)) for row in screen)


def main(args):
    dots, folds = parse(args.datafile)
    part1 = len(singlefold(dots, folds[0]))
    part2 = draw(multifolds(dots, folds))
    print(f'Part 1: {part1}')
    print(f'Part 2: \n{part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
