from pprint import pprint
from typing import Generator


def parse_input(filename: str) -> list[list[int]]:
    data = []
    with open(filename) as f:
        for line in f:
            data.append(list(map(int, line.strip())))
    return data


def next_coords(x: int, y: int, max_x: int, max_y) -> Generator[tuple[int, int], None, None]:
    if x > 0:
        yield x - 1, y
    if y > 0:
        yield x, y - 1
    if x < max_x - 1:
        yield x + 1, y
    if y < (max_y - 1):
        yield x, y + 1


def print_route(route: list[tuple[int, int]], max_x: int, max_y: int) -> None:
    trail_map: list[list[str]] = [
        ['.' for _ in range(max_x)]
        for _ in range(max_y)
    ]

    for idx, (x, y) in enumerate(route):
        trail_map[y][x] = str(idx)

    pprint(route)
    print('\n'.join(''.join(line) for line in trail_map))


def walk_trail(trail_map: list[list[int]], x: int, y: int) -> list[list[tuple[int, int]]]:
    current_value = trail_map[y][x]
    if current_value == 9:
        return [[(x, y)]]
    next_value = current_value + 1
    routes = []
    for next_x, next_y in next_coords(x, y, len(trail_map[0]), len(trail_map)):
        if trail_map[next_y][next_x] == next_value:
            for route in walk_trail(trail_map, next_x, next_y):
                routes.append([(x, y)] + route)
    return routes


def get_trails_in_map(filename):
    data = parse_input(filename)
    trails = []
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value == 0:
                trails.append(walk_trail(data, x, y))
    return trails


def part1(filename: str) -> int:
    trails = get_trails_in_map(filename)

    total_ends_per_trail = 0
    for trail in trails:
        unique_ends = {route[-1] for route in trail}
        total_ends_per_trail += len(unique_ends)
    return total_ends_per_trail


def part2(filename: str) -> int:
    trails = get_trails_in_map(filename)
    return sum(len(trail) for trail in trails)


def main():
    assert part1("sample1.txt") == 1, part1("sample1.txt")
    assert part1("sample2.txt") == 36, part1("sample2.txt")
    print(part1("input.txt"))
    assert part2("sample2.txt") == 81, part1("sample2.txt")
    print(part2("input.txt"))


if __name__ == '__main__':
    main()
