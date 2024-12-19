from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import List, Generator

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x):
        return x


class Color(Enum):
    WHITE = 0
    BLUE = 1
    BLACK = 2
    RED = 3
    GREEN = 4

    def to_string(self) -> str:
        match self:
            case Color.WHITE:
                return "w"
            case Color.BLUE:
                return "u"
            case Color.BLACK:
                return "b"
            case Color.RED:
                return "r"
            case Color.GREEN:
                return "g"

    @staticmethod
    def from_str(color):
        match color:
            case 'w':
                return Color.WHITE
            case 'u':
                return Color.BLUE
            case 'b':
                return Color.BLACK
            case 'r':
                return Color.RED
            case 'g':
                return Color.GREEN
            case _:
                raise ValueError(f'Unknown color {color}')


@dataclass
class Game:
    towels: List[list[Color]]
    designs: list[list[Color]]


def parse_input(filename: str) -> Game:
    towels = []
    designs = []
    with open(filename) as f:
        for towel in f.readline().strip().split(','):
            towels.append(list(map(Color.from_str, towel.strip())))
        for line in f:
            if not line.strip():
                continue
            designs.append(list(map(Color.from_str, line.strip())))
    return Game(towels, designs)


def make_pattern(pattern: list[Color], towels: list[list[Color]]) -> Generator[list[list[Color]], None, None]:
    if len(pattern) == 0:
        yield []
        return
    for towel in towels:
        if pattern[:len(towel)] == towel:
            for make_next in make_pattern(pattern[len(towel):], towels):
                if make_next is not None:
                    yield [towel, *make_next]


@cache
def count_possible_patterns(pattern: tuple[Color], towels: tuple[tuple[Color]]) -> int:
    if len(pattern) == 0:
        return 1
    total = 0
    for towel in towels:
        if pattern[:len(towel)] == towel:
            total += count_possible_patterns(pattern[len(towel):], towels)
    return total


def part1(filename: str) -> int:
    game = parse_input(filename)
    can_make = 0
    for pattern in game.designs:
        try:
            next(make_pattern(pattern, game.towels))
            can_make += 1
        except StopIteration:
            pass
    return can_make


def part2(filename: str) -> int:
    game = parse_input(filename)
    can_make = 0
    count_possible_patterns.cache_clear()
    for pattern in tqdm(game.designs):
        can_make += count_possible_patterns(tuple(pattern), tuple(map(tuple, game.towels)))
    return can_make


def main():
    assert part1("sample.txt") == 6, part1("sample.txt")
    print(part1("input.txt"))
    assert part2("sample.txt") == 16, part2("sample.txt")
    print(part2("input.txt"))


if __name__ == '__main__':
    main()
