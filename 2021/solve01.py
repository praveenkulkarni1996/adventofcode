"""Solution to https://adventofcode.com/2021/day/1 - Sonar Sweep.

Part 1: 1715
Part 2: 1739
"""

import argparse
import itertools
import pathlib

parser = argparse.ArgumentParser(prog='Sonar Sweep')
parser.add_argument('datafile', type=pathlib.Path)


def triplewise(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') --> ABC BCD CDE DEF EFG
    pairwise = itertools.pairwise
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def main(args):
    with open(args.datafile) as datafile:
        depths = [int(line) for line in datafile]
    part1: int = sum(next > prev for prev, next in itertools.pairwise(depths))
    depths3 = [a + b + c for a, b, c in triplewise(depths)]
    part2: int = sum(next > prev for prev, next in itertools.pairwise(depths3))
    print(part1)
    print(part2)


if __name__ == '__main__':
    main(args=parser.parse_args())
