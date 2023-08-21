"""Solution - Passage Pathing

Link: https://adventofcode.com/2021/day/12
Part 1: 3495
Part 2: 94849
"""

from typing import TypeAlias

import argparse
import collections
import pathlib

parser = argparse.ArgumentParser(prog='Passage Pathing')
parser.add_argument('datafile', type=pathlib.Path)

Graph: TypeAlias = dict[str, list[str]]


def parse(datafile: str) -> Graph:
    with open(datafile) as f:
        edges = [line.strip().split('-') for line in f if line]
    g = collections.defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    return dict(g)


def count(cur, seen: set[str], g: Graph) -> int:
    if cur == 'end':
        return 1
    return sum(
        count(nbr, seen | {nbr}, g) for nbr in g[cur]
        if nbr.isupper() or nbr not in seen)


def count2(cur, seen: set[str], g: Graph) -> int:
    if cur == 'end':
        return 1
    repeat_now = sum(
        count(nbr, seen, g) for nbr in g[cur]
        if nbr.islower() and nbr in seen and nbr != 'start')
    repeat_later = sum(
        count2(nbr, seen | {nbr}, g) for nbr in g[cur]
        if nbr.isupper() or nbr not in seen)
    return repeat_now + repeat_later


def main(args):
    g = parse(args.datafile)
    part1 = count('start', {'start'}, g)
    print(f'Part 1: {part1}')
    part2 = count2('start', {'start'}, g)
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
