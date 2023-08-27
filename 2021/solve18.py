"""Day 18: Snailfish - https://adventofcode.com/2021/day/18

Part 1: 3216
Part 2: 4643
"""

from typing import TypeAlias

import argparse
import dataclasses
import math
import pathlib
import functools

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)

SnailFish: TypeAlias = list['SnailFish'] | int


@dataclasses.dataclass
class Extra:
    left: int
    right: int


def parse(datafile: str) -> list[SnailFish]:
    with open(datafile) as f:
        return [eval(line.strip()) for line in f]


def split(sfn: SnailFish) -> tuple[bool, SnailFish]:
    if type(sfn) is int:
        if sfn >= 10:
            return True, [math.floor(sfn / 2), math.ceil(sfn / 2)]
        return False, sfn
    [left, right] = sfn
    did_split, left = split(left)
    if did_split:
        return True, [left, right]
    did_split, right = split(right)
    return did_split, [left, right]


def addleft(sfn: SnailFish, value: int) -> SnailFish:
    if type(sfn) is int:
        return sfn + value
    left, right = sfn
    return [left, addleft(right, value)]


def addright(sfn: SnailFish, value: int) -> SnailFish:
    if type(sfn) is int:
        return sfn + value
    left, right = sfn
    return [addright(left, value), right]


def explode(sfn: SnailFish, depth: int) -> tuple[bool, Extra, SnailFish]:
    if type(sfn) is int:
        return False, None, sfn
    if depth > 4:
        left, right = sfn
        assert type(left) is int
        assert type(right) is int
        return True, Extra(left, right), 0
    left, right = sfn
    did_left_explode, extra, left = explode(left, depth + 1)
    if did_left_explode:
        return True, Extra(extra.left, 0), [left, addright(right, extra.right)]
    did_right_explode, extra, right = explode(right, depth + 1)
    if did_right_explode:
        return True, Extra(0, extra.right), [addleft(left, extra.left), right]
    return False, None, [left, right]


def fullexplode(sfn: SnailFish) -> tuple[bool, SnailFish]:
    did_explode, _, sfn = explode(sfn, depth=1)
    return did_explode, sfn


def normalize(sfn: SnailFish) -> SnailFish:
    while True:
        did_explode, sfn = fullexplode(sfn)
        if did_explode:
            continue
        did_split, sfn = split(sfn)
        if did_split:
            continue
        return sfn


def add(a: SnailFish, b: SnailFish) -> SnailFish:
    return normalize([a, b])


def magnitude(sfn: SnailFish) -> int:
    if type(sfn) is int:
        return sfn
    left, right = sfn
    return 3 * magnitude(left) + 2 * magnitude(right)


def max_magnitude(nums: list[SnailFish]) -> int:
    return max(magnitude(add(a, b)) for a in nums for b in nums if a is not b)


def main(args):
    nums = parse(args.datafile)
    part1 = magnitude(functools.reduce(add, nums))
    part2 = max_magnitude(nums)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
