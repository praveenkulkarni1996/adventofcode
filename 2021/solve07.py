"""Solution - The Treachery of Whales

Link: https://adventofcode.com/2021/day/7 
Part 1: 344605
Part 2: 93699985
"""

from typing import TypeAlias, Callable

import argparse
import functools
import pathlib

parser = argparse.ArgumentParser(prog='Sonar Sweep')
parser.add_argument('datafile', type=pathlib.Path)

BurnFn: TypeAlias = Callable[[int], int]


def parse(datafile) -> list[int]:
    with open(datafile) as f:
        return [int(num) for num in f.read().strip().split(',')]


def linear(start: int, stop: int) -> int:
    return abs(start - stop)


def quadratic(start: int, stop: int) -> int:
    diff = abs(start - stop)
    return (diff * (diff + 1)) // 2


def charge(burn: BurnFn, spots: list[int], guess: int) -> int:
    return sum(burn(spot, guess) for spot in spots)


def main(args):
    spots: list[int] = sorted(parse(args.datafile))
    # If it's linear rate of burning fuel, then the answer will always occur
    # at one of the spots.
    cheapest: int = min(charge(linear, spots, guess) for guess in spots)
    print(f"Part 1: {cheapest}")

    # For quadratic rates of burning fuel, the answer can occur anywhere in
    # range of the spots.
    guesses = range(min(spots), max(spots) + 1)
    cheapest = min(charge(quadratic, spots, guess) for guess in guesses)
    print(f"Part 2: {cheapest}")


if __name__ == '__main__':
    main(args=parser.parse_args())
