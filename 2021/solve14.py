"""Solution - Extended Polymerization

Link: https://adventofcode.com/2021/day/14
Part 1: 2899
Part 2: 3528317079545
"""

from collections.abc import Mapping

import copy
import argparse
import dataclasses
import collections
import itertools
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)

RuleBook = Mapping[str, str]


@dataclasses.dataclass
class Polymer:
    chars: Mapping[str, int]
    pairs: Mapping[str, int]


def analyse(polymer: str) -> Polymer:
    chars = collections.Counter(polymer)
    pairs = collections.Counter(a + b for a, b in itertools.pairwise(polymer))
    return Polymer(chars, pairs)


def rule(equation: str) -> tuple[str, str]:
    return equation.split(' -> ')


def rulebook(contents: str) -> RuleBook:
    return dict(rule(equation) for equation in contents.split('\n'))


def parse(datafile: str) -> tuple[Polymer, RuleBook]:
    with open(datafile) as f:
        polymer, rules = f.read().split('\n\n')
    return analyse(polymer), rulebook(rules)


def polymerize(polymer: Polymer, book: RuleBook) -> Polymer:
    new: Polymer = copy.deepcopy(polymer)
    for reactant, product in book.items():
        items = polymer.pairs[reactant]
        new.chars[product] += items
        new.pairs[reactant[0] + product] += items
        new.pairs[product + reactant[1]] += items
        new.pairs[reactant] -= items
    return new


def simulate(epochs: int, polymer: Polymer, book: RuleBook) -> Polymer:
    for _ in range(epochs):
        polymer = polymerize(polymer, book)
    return polymer


def gap(polymer: Polymer) -> int:
    frequencies = polymer.chars.values()
    return max(frequencies) - min(frequencies)


def solve(polymer: Polymer, book: RuleBook, epochs: int) -> int:
    return gap(simulate(epochs, polymer, book))


def main(args):
    polymer, rulebook = parse(args.datafile)
    part1 = solve(polymer, rulebook, 10)
    part2 = solve(polymer, rulebook, 40)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
