"""Solution to https://adventofcode.com/2021/day/4 - Giant Squid

Part 1: 41668
Part 2: 10478
"""

from typing import TypeAlias

import argparse
import functools
import pathlib

import more_itertools

parser = argparse.ArgumentParser(prog='Giant Squid')
parser.add_argument('datafile', type=pathlib.Path)

Quince: TypeAlias = tuple[int, int, int, int, int]
Board: TypeAlias = list[Quince]


def finish(order: list[int], q: Quince) -> int:
    return max(order.index(value) for value in q)


def finish_any(order: list[int], board: Board) -> int:
    return min(finish(order, q) for q in board)


def score(order: list[int], board: Board) -> int:
    values = {num for q in board for num in q}
    index = finish_any(order, board)
    pending = set(order[index + 1:])
    return sum(pending & values) * order[index]


def parse(datafile: pathlib.Path) -> tuple[list[int], list[Board]]:

    def extract_ints(line: str) -> list[int]:
        modified = line.replace(',', ' ')
        return [int(s) for s in modified.split()]

    def to_board(batch: list[Quince]) -> Board:
        return list(batch) + list(more_itertools.transpose(batch))

    with open(datafile) as f:
        order, *rows = [ints for line in f if (ints := extract_ints(line))]
    boards = [to_board(batch) for batch in more_itertools.batched(rows, 5)]
    return order, boards


def main(args):
    order, boards = parse(datafile=args.datafile)
    time_to_win = functools.partial(finish_any, order)
    winner = min(boards, key=time_to_win)
    loser = max(boards, key=time_to_win)
    print("Part 1: {ans}".format(ans=score(order, winner)))
    print("Part 2: {ans}".format(ans=score(order, loser)))


if __name__ == '__main__':
    main(args=parser.parse_args())
