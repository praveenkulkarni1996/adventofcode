"""Solution to https://adventofcode.com/2021/day/2 - Dive!

Part 1: 2187380
Part 2: 2086357770
"""

import argparse
import collections
import functools
import pathlib

parser = argparse.ArgumentParser(prog='Dive!')
parser.add_argument('datafile', type=pathlib.Path)

Pos = collections.namedtuple('Pos', ['shift', 'depth'])


def apply(pos: Pos, command: str) -> Pos:
    opcode: str = command[0]
    offset: int = int(command[1])
    match opcode:
        case 'forward':
            return Pos(shift=pos.shift + offset, depth=pos.depth)
        case 'down':
            return Pos(shift=pos.shift, depth=pos.depth + offset)
        case 'up':
            return Pos(shift=pos.shift, depth=pos.depth - offset)


Pos3 = collections.namedtuple('Pos3', ['shift', 'depth', 'aim'])


def apply3(p: Pos3, command: str) -> Pos3:
    opcode: str = command[0]
    offset: int = int(command[1])
    match opcode:
        case 'forward':
            diff = p.aim * offset
            return Pos3(shift=p.shift + offset,
                        depth=p.depth + diff,
                        aim=p.aim)
        case 'down':
            return Pos3(shift=p.shift, depth=p.depth, aim=p.aim + offset)
        case 'up':
            return Pos3(shift=p.shift, depth=p.depth, aim=p.aim - offset)


def main(args):
    with open(args.datafile) as datafile:
        fullcommands = [tuple(line.strip().split(' ')) for line in datafile]
    part1: Pos = functools.reduce(apply, fullcommands, Pos(0, 0))
    print("Part 1: {ans}".format(ans=part1.shift * part1.depth))
    part2: Pos3 = functools.reduce(apply3, fullcommands, Pos3(0, 0, 0))
    print("Part 2: {ans}".format(ans=part2.shift * part2.depth))


if __name__ == '__main__':
    main(args=parser.parse_args())