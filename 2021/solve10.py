"""Solution - Syntax Scoring

Link: https://adventofcode.com/2021/day/10 
Part 1: ???
Part 2: ???
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


def syntax(line: str) -> int:
    SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
    stack = []
    for token in line:
        if token in MATCHING:
            if not stack or stack.pop() != MATCHING[token]:
                return SCORE[token]
        else:
            stack.append(token)
    return 0


def autocomplete(line: str) -> int:
    stack = []
    for token in line:
        if token in MATCHING:
            if not stack or stack.pop() != MATCHING[token]:
                return 0
        else:
            stack.append(token)
    SCORE = {'(': 1, '[': 2, '{': 3, '<': 4}
    ans = 0
    for token in reversed(stack):
        ans = (ans * 5) + SCORE[stack.pop()]
    return ans


def main(args):
    lines = parse(args.datafile)
    total = sum(syntax(line) for line in lines)
    autoscores = [score for line in lines if (score := autocomplete(line))]
    median = statistics.median(autoscores)
    print(median)


if __name__ == '__main__':
    main(args=parser.parse_args())
