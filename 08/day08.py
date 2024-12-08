from dataclasses import dataclass
from itertools import groupby, combinations


@dataclass
class Antenna:
    x: int
    y: int
    frequency: str


def parse_input(filename: str) -> tuple[int, int, list[Antenna]]:
    antennas = []
    max_x = 0
    max_y = 0
    with open(filename) as f:
        for y, line in enumerate(f):
            max_y = max(max_y, y)
            for x, c in enumerate(line.strip()):
                max_x = max(max_x, x)
                if c != '.':
                    antennas.append(Antenna(x, y, c))
    return max_x, max_y, antennas


def get_antinodes(a1: Antenna, a2: Antenna) -> list[tuple[int, int]]:
    if a1.x > a2.x or a1.y > a2.y:
        a1, a2 = a2, a1
    dx = a2.x - a1.x
    dy = a2.y - a1.y

    anti1_x = a1.x - dx
    anti1_y = a1.y - dy
    anti2_x = a2.x + dx
    anti2_y = a2.y + dy
    return [(anti1_x, anti1_y), (anti2_x, anti2_y)]


def get_all_antinodes(a1: Antenna, a2: Antenna, max_x: int, max_y: int) -> list[tuple[int, int]]:
    if a1.x > a2.x or a1.y > a2.y:
        a1, a2 = a2, a1
    dx = a2.x - a1.x
    dy = a2.y - a1.y
    antinodes = []
    # Starting at the current node, as there's also an antinode there
    current_x = a1.x
    current_y = a1.y
    while current_x >= 0 and current_y >= 0:
        antinodes.append((current_x, current_y))
        current_x -= dx
        current_y -= dy
    current_x = a2.x
    current_y = a2.y
    while current_x <= max_x and current_y <= max_y:
        antinodes.append((current_x, current_y))
        current_x += dx
        current_y += dy

    return antinodes


def in_bounds(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x <= max_x and 0 <= y <= max_y


def part1(filename: str) -> int:
    max_x, max_y, antennas = parse_input(filename)
    antennas_by_frequency = groupby(sorted(antennas, key=lambda a: a.frequency), lambda a: a.frequency)
    antinodes = set()
    for frequency, frequency_antennas in antennas_by_frequency:
        for a1, a2 in combinations(frequency_antennas, 2):
            new_antinodes = get_antinodes(a1, a2)
            antinodes.update(new_antinodes)

    filtered_antinodes = {antinode for antinode in antinodes
                          if in_bounds(*antinode, max_x, max_y)}
    return len(filtered_antinodes)


def part2(filename: str) -> int:
    max_x, max_y, antennas = parse_input(filename)
    antennas_by_frequency = groupby(sorted(antennas, key=lambda a: a.frequency), lambda a: a.frequency)
    antinodes = set()
    for frequency, frequency_antennas in antennas_by_frequency:
        for a1, a2 in combinations(frequency_antennas, 2):
            new_antinodes = get_all_antinodes(a1, a2, max_x, max_y)
            antinodes.update(new_antinodes)

    filtered_antinodes = {antinode for antinode in antinodes
                          if in_bounds(*antinode, max_x, max_y)}
    return len(filtered_antinodes)


def main():
    assert get_antinodes(Antenna(4, 3, 'a'), Antenna(5, 5, 'a')) == [(3, 1), (6, 7)],\
        get_antinodes(Antenna(4, 3, 'a'), Antenna(5, 5, 'a'))
    assert part1('sample.txt') == 14
    print(part1('input.txt'))

    assert part2('sample.txt') == 34
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
