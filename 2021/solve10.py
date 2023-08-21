"""Solution - Syntax Scoring

Link: https://adventofcode.com/2021/day/10 
Part 1: 318099
Part 2: 2389738699
"""

import argparse
import pathlib
import statistics

parser = argparse.ArgumentParser(prog='Syntax Scoring')
parser.add_argument('datafile', type=pathlib.Path)


def parse(datafile: str) -> list[list[int]]:
    with open(datafile) as f:
        return [line.strip() for line in f]


MATCHING = {
    ')': '(',
    '}': '{',
    '>': '<',
    ']': '[',
}


def analyse(line: str) -> tuple[str, str | list[str]]:
    stack = []
    for token in line:
        if token in MATCHING:
            if not stack or stack.pop() != MATCHING[token]:
                return ('syntax error', token)
        else:
            stack.append(token)
    return ('autocomplete', stack)


SYNTAX_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}


def autoscore(tokens: list[str]) -> int:
    tokens = ''.join(reversed(tokens))
    tokens = tokens.replace('(', '1')
    tokens = tokens.replace('[', '2')
    tokens = tokens.replace('{', '3')
    tokens = tokens.replace('<', '4')
    return int(tokens, base=5)


def main(args):
    lines = parse(args.datafile)
    statuses = [analyse(line) for line in lines]
    part1: int = sum([
        SYNTAX_SCORES[tok] for status, tok in statuses
        if status == 'syntax error'
    ])
    part2: int = statistics.median([
        autoscore(tokens) for status, tokens in statuses
        if status == 'autocomplete'
    ])
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main(args=parser.parse_args())
