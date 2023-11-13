"""Solution - Dirac Dice.

Link: https://adventofcode.com/2021/day/21 
Part 1: 513936
Part 2: 105619718613031
"""

import argparse
import collections
import dataclasses
import functools
import itertools
import pathlib

import more_itertools

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)

UNIVERSE_ROLLS = collections.Counter([
    a + b + c 
    for a in range(1, 4)
    for b in range(1, 4)
    for c in range(1, 4)
])


@functools.cache
def count(score: int, pos: int, otherscore: int, otherpos: int) -> int:
    assert 0 <= score < 21
    if otherscore >= 21:
        return (0, 1)
    total_p1 = 0
    total_p2 = 0
    for steps, universe in UNIVERSE_ROLLS.items():
        new_pos = ((pos + steps - 1) % 10) + 1
        new_score = score + new_pos
        p2wins, p1wins = count(otherscore, otherpos, new_score, new_pos)
        total_p1 += universe * p1wins
        total_p2 += universe * p2wins
    return total_p1, total_p2


def parse(datafile: str):
    with open(datafile) as f:
        return tuple([int(line.split(':')[-1].strip()) for line in f])
        

def take(n: int, iterable) -> list:
    """Return first n items of the iterable as a list."""
    return list(itertools.islice(iterable, n))


@dataclasses.dataclass
class Player:
    score: int
    position: int 

def move(player: Player, steps: int):
    player.position = ((player.position + steps - 1) % 10) + 1
    player.score += player.position


def is_winner(player: Player) -> bool:
    return player.score >= 1000

def throw(rolls3 : list[tuple[int, int]]) -> int:
    steps = [roll[-1] for roll in rolls3]
    throws = max(roll[0] for roll in rolls3)
    return (sum(steps), throws)

def simulate(a: Player, b: Player) -> int:
    dice = enumerate(itertools.count(1), start=1)
    dice3 = more_itertools.chunked(dice, 3)
    for curr, opponent in itertools.cycle(((a, b), (b, a))):
        if not is_winner(curr):
            steps, throws = throw(next(dice3))
            move(player=curr, steps=steps)
            if is_winner(curr):
                return throws * opponent.score


def main(args):
    pos1, pos2 = parse(args.datafile)
    p1 = Player(score=0, position=pos1)
    p2 = Player(score=0, position=pos2)
    part1 = simulate(p1, p2)
    print(f'Part 1: {part1}')
    part2 = max(count(score=0, pos=pos1, otherscore=0, otherpos=pos2))
    print(f'Part 2: {part2}')



if __name__ == '__main__':
    main(args=parser.parse_args())
