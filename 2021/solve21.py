"""Solution - Dirac Dice.

Link: https://adventofcode.com/2021/day/21 
Part 1: 513936
Part 2: ???
"""

import argparse
import dataclasses
import itertools
import pathlib

import more_itertools

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)


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
    answer = simulate(p1, p2)
    print(f'Part 1: {answer}')


if __name__ == '__main__':
    main(args=parser.parse_args())
