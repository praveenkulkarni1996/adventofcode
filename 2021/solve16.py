"""Solution - Packet Decoder

Link: https://adventofcode.com/2021/day/16
Part 1: 1038
Part 2: 246761930504
"""

import argparse
import collections
import dataclasses
import enum
import math
import operator
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)


class Opcode(enum.Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    VALUE = 4
    GREATER = 5
    LESSER = 6
    EQUAL = 7


@dataclasses.dataclass(frozen=True)
class Header:
    version: int
    typeid: Opcode


@dataclasses.dataclass(frozen=True)
class Literal:
    header: Header
    value: int


@dataclasses.dataclass(frozen=True)
class Operation:
    header: Header
    subpackets: list['Packet']


Packet = Literal | Operation


def bitstring(datafile: str) -> str:
    with open(datafile) as f:
        hexstring = f.read().strip()
    required_chars = len(hexstring) * 4
    binary = bin(int(hexstring, base=16))[2:]
    return binary.zfill(required_chars)


def multipop(bs: collections.deque, nbits: int) -> str:
    return ''.join([bs.popleft() for _ in range(nbits)])


def integer(bs: collections.deque, nbits: int) -> int:
    return int(multipop(bs, nbits), base=2)


def litvalue(bs: collections.deque) -> int:
    value = 0
    while True:
        more = integer(bs, 1)
        value = (value << 4) | integer(bs, 4)
        if not more: break
    return value


def allpackets(bs: collections.deque) -> list[Packet]:
    packets = []
    while bs:
        packets.append(packet(bs))
    return packets


def packet(bs: collections.deque) -> Packet:
    header = Header(
        version=integer(bs, 3),
        typeid=Opcode(integer(bs, 3)),
    )
    if header.typeid == Opcode.VALUE:
        return Literal(header=header, value=litvalue(bs))
    if integer(bs, 1) == 0:
        subbits = integer(bs, 15)
        prefix = collections.deque(multipop(bs, subbits))
        return Operation(header=header, subpackets=allpackets(prefix))
    else:
        numpackets = integer(bs, 11)
        subpackets = [packet(bs) for _ in range(numpackets)]
        return Operation(header=header, subpackets=subpackets)


def sumversion(p: Packet) -> int:
    match p:
        case Literal(header, value):
            return header.version
        case Operation(header, subpackets):
            return header.version + sum(sumversion(sp) for sp in subpackets)
    raise ValueError


def solve(p: Packet) -> int:
    match p:
        case Literal(_, value):
            return value
        case Operation(header, subpackets):
            values = (solve(sp) for sp in subpackets)
            match header.typeid:
                case Opcode.SUM:
                    return sum(values)
                case Opcode.PRODUCT:
                    return math.prod(values)
                case Opcode.MAX:
                    return max(values)
                case Opcode.MIN:
                    return min(values)
                case Opcode.GREATER:
                    return operator.gt(*values)
                case Opcode.LESSER:
                    return operator.lt(*values)
                case Opcode.EQUAL:
                    return operator.eq(*values)
    raise ValueError


def main(args):
    bs = bitstring(args.datafile)
    bs = collections.deque(list(bs))
    p = packet(bs)
    print('Part 1:', sumversion(p))
    print('Part 2:', solve(p))


if __name__ == '__main__':
    main(args=parser.parse_args())
