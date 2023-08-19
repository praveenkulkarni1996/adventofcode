"""Solution - Seven Segment Search

Link: https://adventofcode.com/2021/day/8 
Part 1: 330
Part 2: 1010472
"""

from typing import TypeAlias

import argparse
import itertools
import pathlib

parser = argparse.ArgumentParser(prog='Seven Segment Search')
parser.add_argument('datafile', type=pathlib.Path)

Tokens: TypeAlias = list[str]
TokensIO: TypeAlias = tuple[Tokens, Tokens]

SEVEN_SEGMENT = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

ALL_DISPLAYS = set(SEVEN_SEGMENT.keys())


def parse(datafile: str) -> list[TokensIO]:

    def extract(line: str):
        inputs, outputs = line.strip().split('|')
        inputs = [token.strip() for token in inputs.split(' ') if token]
        outputs = [token.strip() for token in outputs.split(' ') if token]
        return (inputs, outputs)

    with open(datafile) as f:
        return [extract(line) for line in f]


def normalize(display: str) -> str:
    return ''.join(sorted(display))


def brute(intokens: Tokens):
    for miswire in itertools.permutations('abcdefg'):
        table = str.maketrans('abcdefg', ''.join(miswire))
        deciphered = {normalize(tok.translate(table)) for tok in intokens}
        if deciphered == ALL_DISPLAYS:
            return table
    raise AssertionError("could not brute force discover")


def solve(intokens: Tokens, outtokens: Tokens):
    table = brute(intokens)

    def integerize(tok: str) -> int:
        return SEVEN_SEGMENT[normalize(tok.translate(table))]

    return tuple(integerize(tok) for tok in outtokens)


def main(args):
    io_tokens = parse(args.datafile)
    results = [solve(intokens, outtokens) for intokens, outtokens in io_tokens]
    part1 = len([v for tup in results for v in tup if v in {1, 4, 7, 8}])
    part2 = sum(1000 * a + 100 * b + 10 * c + d for (a, b, c, d) in results)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == '__main__':
    main(args=parser.parse_args())
