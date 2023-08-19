"""Solution to https://adventofcode.com/2021/day/3 - Binary Diagnostic.

Part 1: 3912944
Part 2: 4996233
"""

from typing import Iterable, Callable, TypeAlias

import argparse
import pathlib

parser = argparse.ArgumentParser(prog='Binary Diagnostic')
parser.add_argument('datafile', type=pathlib.Path)

Bit: TypeAlias = str
BitSlice: TypeAlias = Iterable[Bit]
BitChooser: TypeAlias = Callable[[BitSlice], Bit]


def most(bits: BitSlice) -> Bit:
    bits = [int(bit) for bit in bits]
    return '1' if sum(bits) * 2 >= len(bits) else '0'


def least(bits: BitSlice) -> Bit:
    bits = [int(bit) for bit in bits]
    return '0' if sum(bits) * 2 >= len(bits) else '1'


def slice(lines: list[str], index: int) -> BitSlice:
    return [line[index] for line in lines]


def simple(lines: list[str], chooser: BitChooser) -> str:
    LEN = len(lines[0])
    return ''.join(chooser(slice(lines, idx)) for idx in range(LEN))


def hard(lines: list[str], chooser: BitChooser, index=0) -> str:
    if len(lines) == 1:
        [result] = lines
        return result
    sliced: BitSlice = slice(lines, index)
    golden: Bit = chooser(sliced)
    filtered = [line for line, bit in zip(lines, sliced) if bit == golden]
    return hard(filtered, chooser, index + 1)


def main(args):
    with open(args.datafile) as datafile:
        lines = [line.strip() for line in datafile]

    gamma: str = simple(lines, most)
    epsilon: str = simple(lines, least)
    power = int(gamma, base=2) * int(epsilon, base=2)
    print(f'Part 1: {power}')

    oxygen: str = hard(lines, most)
    carbon: str = hard(lines, least)
    life_support = int(oxygen, base=2) * int(carbon, base=2)
    print(f'Part 2: {life_support}')


if __name__ == '__main__':
    main(args=parser.parse_args())
