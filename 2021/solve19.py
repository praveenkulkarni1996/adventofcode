"""Day 19: Beacon Scanner - https://adventofcode.com/2021/day/19

Part 1: ???
Part 2: ???
"""

from typing import TypeAlias, Callable

import argparse
import pathlib
import collections
import itertools
import pprint
import sys

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=pathlib.Path)

Vec3: TypeAlias = tuple[int, int, int]
Scans: TypeAlias = list[Vec3]


def rotator(px, py, pz, sx, sy, sz):
    return lambda v: (sx * v[px], sy * v[py], sz * v[pz])


def build_rotations():
    rotations = []
    for (px, py, pz) in itertools.permutations([0, 1, 2]):
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                for sz in [-1, 1]:
                    rotations.append(rotator(px, py, pz, sx, sy, sz))
    return rotations


ROTATIONS = build_rotations()


def parse_single(single: str) -> list[Vec3]:
    lines = [line for line in single.split('\n') if line.count(',') == 2]
    return [tuple(int(num) for num in line.split(',')) for line in lines]


def parse(datafile: str):
    with open(datafile) as f:
        return [parse_single(single) for single in f.read().split('\n\n')]


def distance(a: Vec3, b: Vec3) -> int:
    ax, ay, az = a
    bx, by, bz = b
    return (ax - bx)**2 + (ay - by)**2 + (az - bz)**2


def distanceset(pt: Vec3, scans: Scans) -> dict[int, int]:
    return collections.Counter([distance(pt, o) for o in scans if o != pt])


def overlaps(a: Scans, b: Scans) -> None | dict[Vec3, Vec3]:
    adists = {pt: distanceset(pt, a) for pt in a}
    bdists = {pt: distanceset(pt, b) for pt in b}
    matches = {}
    for pointa in adists:
        for pointb in bdists:
            if sum((adists[pointa] & bdists[pointb]).values()) >= 11:
                matches[pointa] = pointb
    assert len(matches) == 0 or len(matches) >= 12
    return matches or None


def diff(a: Vec3, b: Vec3) -> Vec3:
    ax, ay, az = a
    bx, by, bz = b
    return (bx - ax, by - ay, bz - az)


def rotator_b2a(a: Vec3, b: Vec3) -> Callable[[Vec3], Vec3]:
    [b2a] = [r for r in ROTATIONS if r(b) == a]
    return b2a


def build_transformer(overlap: dict[Vec3, Vec3]):
    a1, a2 = list(overlap.keys())[:2]
    b1, b2 = overlap[a1], overlap[a2]
    adiff = diff(a1, a2)
    bdiff = diff(b1, b2)
    rotator = rotator_b2a(adiff, bdiff)

    def transformer(pointb: Vec3) -> Vec3:
        tx, ty, tz = rotator(diff(b1, pointb))
        ax, ay, az = a1
        return (ax + tx, ay + ty, az + tz)

    for apoint, bpoint in overlap.items():
        assert apoint == transformer(bpoint)

    return transformer


def invert(overlap: dict[Vec3, Vec3]) -> dict[Vec3, Vec3]:
    return {v: k for k, v in overlap.items()}


def main(args):
    scanners = parse(args.datafile)
    edges = collections.defaultdict(set)
    for a, b in itertools.combinations(range(len(scanners)), 2):
        if overlaps(scanners[a], scanners[b]):
            edges[a].add(b)
            edges[b].add(a)

    transforms = {
        0: lambda v: v  # only one
    }
    q = collections.deque([0])
    while q:
        cur = q.popleft()
        for nbr in edges[cur]:
            print(cur, nbr)
            if nbr not in transforms:
                overlap = overlaps(scanners[cur], scanners[nbr])
                nbr2cur = build_transformer(overlap)
                transforms[nbr] = lambda v: (transforms[cur](nbr2cur(v)))
                q.append(nbr)
    points = {
        transforms[index](point)
        for index, scanner in enumerate(scanners)
        for point in scanner
    }
    print(len(points))

    # edges.append(((a, b), build_transformer(overlap)))
    # pprint.pprint(sorted(edges))


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    main(args=parser.parse_args())
