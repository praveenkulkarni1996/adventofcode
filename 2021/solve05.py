"""Solution to https://adventofcode.com/2021/day/5 - Hydrothermal Venture

Part 1: 6666
Part 2: 19081
"""

from typing import TypeAlias, Iterable, Literal

import argparse
import collections
import itertools
import pathlib

parser = argparse.ArgumentParser(prog='Hydrothermal Venture')
parser.add_argument('datafile', type=pathlib.Path)

Pair: TypeAlias = tuple[int, int]
TwoPair: TypeAlias = tuple[Pair, Pair]


def parse(datafile: pathlib.Path) -> list[TwoPair]:

    def pair(csv: str) -> Pair:
        x, y = csv.split(',')
        return (int(x), int(y))

    def extract(line: str) -> TwoPair:
        left, right = line.strip().split(' -> ')
        return pair(left), pair(right)

    with open(datafile) as f:
        return [extract(line) for line in f]


def dist(a: Pair, b: Pair) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def signum(x: int) -> Literal[-1, 0, 1]:
    if x > 0: return 1
    if x < 0: return -1
    return 0


def points(a: Pair, b: Pair) -> Iterable[Pair]:
    diff0 = signum(b[0] - a[0])
    diff1 = signum(b[1] - a[1])
    length = dist(a, b)
    return ((a[0] + x * diff0, a[1] + x * diff1) for x in range(length + 1))


def is_parallel(a: Pair, b: Pair) -> bool:
    return a[0] == b[0] or a[1] == b[1]


def only_parallels(ventdefs: list[TwoPair]) -> list[TwoPair]:
    return [v for v in ventdefs if is_parallel(*v)]


def count_dangerous(vent_defs: list[TwoPair]) -> int:
    vents = itertools.chain.from_iterable(points(*v) for v in vent_defs)
    return len([v for v in collections.Counter(vents).values() if v > 1])


def main(args):
    vent_defs: Iterable[TwoPair] = parse(datafile=args.datafile)
    ans1 = count_dangerous(only_parallels(vent_defs))
    print(f'Part 1: {ans1}')
    ans2 = count_dangerous(vent_defs)
    print(f'Part 2: {ans2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
