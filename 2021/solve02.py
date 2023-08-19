"""Solution to https://adventofcode.com/2021/day/2 - Dive!

Part 1: 2187380
Part 2: 2086357770
"""

from typing import Literal, TypeAlias

import argparse
import collections
import functools
import pathlib

parser = argparse.ArgumentParser(prog='Dive!')
parser.add_argument('datafile', type=pathlib.Path)

Opcode: TypeAlias = Literal['forward', 'down', 'up']

Cmd = collections.namedtuple('Cmd', ['opcode', 'value'])
Pos = collections.namedtuple('Pos', ['shift', 'depth'])
Pos3 = collections.namedtuple('Pos3', ['shift', 'depth', 'aim'])


def parse(line: str) -> Cmd:
    (opcode, valuestr) = line.strip().split()
    return Cmd(opcode=opcode, value=int(valuestr))


def apply(pos: Pos, cmd: Cmd) -> Pos:
    match cmd.opcode:
        case 'forward':
            return Pos(shift=pos.shift + cmd.value, depth=pos.depth)
        case 'down':
            return Pos(shift=pos.shift, depth=pos.depth + cmd.value)
        case 'up':
            return Pos(shift=pos.shift, depth=pos.depth - cmd.value)


def apply3(p: Pos3, cmd: Cmd) -> Pos3:
    match cmd.opcode:
        case 'forward':
            move = cmd.value
            fall = p.aim * cmd.value
            return Pos3(shift=p.shift + move, depth=p.depth + fall, aim=p.aim)
        case 'down':
            return Pos3(shift=p.shift, depth=p.depth, aim=p.aim + cmd.value)
        case 'up':
            return Pos3(shift=p.shift, depth=p.depth, aim=p.aim - cmd.value)


def main(args):
    with open(args.datafile) as datafile:
        commands = [parse(line) for line in datafile]
    part1: Pos = functools.reduce(apply, commands, Pos(0, 0))
    print("Part 1: {ans}".format(ans=part1.shift * part1.depth))

    part2: Pos3 = functools.reduce(apply3, commands, Pos3(0, 0, 0))
    print("Part 2: {ans}".format(ans=part2.shift * part2.depth))


if __name__ == '__main__':
    main(args=parser.parse_args())