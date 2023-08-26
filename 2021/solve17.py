"""Day 17: Trick Shot - https://adventofcode.com/2021/day/17

Part 1: 35511
Part 2: 3282
"""

import argparse
import dataclasses
import math
import pathlib
import re

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)


@dataclasses.dataclass
class Target:
    xrange: tuple[int, int]
    yrange: tuple[int, int]


def crosstimes(v: int, point: int) -> tuple[float | None, float | None]:
    discriminant = (2 * v + 1) * (2 * v + 1) - 8 * point
    if discriminant < 0:
        return (None, None)
    first = ((2 * v + 1) - math.sqrt(discriminant)) / 2
    second = ((2 * v + 1) + math.sqrt(discriminant)) / 2
    return (first, second)


def ytimes(v: int, low: int, high: int) -> tuple[int, int]:
    _, start = crosstimes(v, high)
    _, finish = crosstimes(v, low)
    return math.ceil(start), math.floor(finish)


def xtimes(v: int, low: int, high: int) -> None | tuple[int, float]:
    start, _ = crosstimes(v, low)
    finish, _ = crosstimes(v, high)
    if not start:
        return None
    if not finish:
        return (math.ceil(start), math.inf)
    return math.ceil(start), math.floor(finish)


def height(speed: int) -> int:
    return (speed * (speed + 1)) // 2


def make_yranges(low: int, high: int) -> dict[int, tuple[float, float]]:
    yranges = {}
    for vy in range(low, 1000):
        start, finish = ytimes(vy, low, high)
        if start <= finish:
            yranges[vy] = (start, finish)
    return yranges


def make_xranges(low: int, high: int) -> dict[int, tuple[float, float]]:
    xranges = {}
    for vx in range(0, high + 1):
        match xtimes(vx, low, high):
            case None:
                continue
            case (start, finish):
                if start <= finish:
                    xranges[vx] = (start, finish)
    return xranges


def possibilities(target: Target) -> set[tuple[int, int]]:
    xranges = make_xranges(*target.xrange)
    yranges = make_yranges(*target.yrange)
    hits = set()
    for vx, xrange in xranges.items():
        for vy, yrange in yranges.items():
            if xrange[1] < yrange[0]:
                continue
            if yrange[1] < xrange[0]:
                continue
            hits.add((vx, vy))
    return hits


def parse(datafile: str) -> Target:
    with open(datafile) as f:
        line = f.read().strip()
    m = re.match('target area: x=(\d+)..(\d+), y=-(\d+)..-(\d+)', line)
    return Target(
        xrange=(int(m.group(1)), int(m.group(2))),
        yrange=(-int(m.group(3)), -int(m.group(4))),
    )


def main(args):
    target = parse(args.datafile)
    hits = possibilities(target)
    peak = height(max({y for (_, y) in hits}))
    print(f'Part 1: {peak}')
    print(f'Part 2: {len(hits)}')


if __name__ == '__main__':
    main(args=parser.parse_args())
