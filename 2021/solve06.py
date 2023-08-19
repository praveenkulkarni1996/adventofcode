"""Solution to https://adventofcode.com/2021/day/6 - Lanternfish.

Part 1: 351188
Part 2: 1595779846729
"""

import argparse
import collections
import pathlib

parser = argparse.ArgumentParser(prog='Lanternfish')
parser.add_argument('datafile', type=pathlib.Path)


def parse(datafile: pathlib.Path) -> tuple[int]:
    with open(datafile) as f:
        return [int(num) for num in f.read().split(',')]


def tomorrow(fishes: collections.deque):
    fishes.rotate(-1)
    fishes[6] += fishes[8]


def simulate(timers: tuple[int], days: int) -> int:
    fishes = collections.deque([0, 0, 0, 0, 0, 0, 0, 0, 0])
    for timer in timers:
        fishes[timer] += 1
    for _ in range(days):
        tomorrow(fishes)
    return sum(fishes)


def main(args):
    timers = parse(args.datafile)
    print("Part 1: {ans}".format(ans=simulate(timers, 80)))
    print("Part 2: {ans}".format(ans=simulate(timers, 256)))


if __name__ == '__main__':
    main(args=parser.parse_args())