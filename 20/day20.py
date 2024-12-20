from typing import Generator


def parse_file(filename: str) -> list[list[str]]:
    maze: list[list[str]] = []
    with open(filename) as f:
        for line in f:
            maze.append([*line.strip()])
    return maze


def point_in_diamond(radius) -> Generator[tuple[int, int], None, None]:
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if abs(0 - x) + abs(0 - y) <= radius:
                yield x, y


def find_in_maze(maze: list[list[str]], to_find: str) -> tuple[int, int]:
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == to_find:
                return x, y
    raise ValueError(f'Could not find {to_find} in maze')


def next_nodes(current_x: int, current_y: int, offset: int) -> Generator[tuple[int, int], None, None]:
    yield current_x + offset, current_y
    yield current_x, current_y + offset
    yield current_x, current_y - offset
    yield current_x - offset, current_y


def point_is_valid(next_x: int, next_y: int, maze: list[list[str]]) -> bool:
    if next_x < 0 or next_y < 0:
        return False
    if next_x >= len(maze[0]) or next_y >= len(maze):
        return False
    if maze[next_y][next_x] == '#':
        return False
    return True


def next_valid_nodes(maze: list[list[str]], current_x: int, current_y: int, offset: int = 1) -> Generator[
    tuple[int, int], None, None]:
    for next_x, next_y in next_nodes(current_x, current_y, offset):
        if point_is_valid(next_x, next_y, maze):
            yield next_x, next_y


def next_valid_nodes_diamond(maze: list[list[str]], current_x: int, current_y: int, radius: int = 1) \
        -> Generator[tuple[int, int], None, None]:
    for point in point_in_diamond(radius):
        if point_is_valid(current_x + point[0], current_y + point[1], maze):
            yield current_x + point[0], current_y + point[1]


def get_first_valid_path(maze: list[list[str]]) -> list[tuple[int, int]]:
    start = find_in_maze(maze, 'S')
    end = find_in_maze(maze, 'E')
    path = [start]
    while path[-1] != end:
        next_nodes_in_path = [node for node in next_valid_nodes(maze, *path[-1]) if node not in path]
        if len(next_nodes_in_path) > 1:
            raise ValueError(f'Found {len(next_nodes_in_path)} valid paths')
        path.append(next_nodes_in_path.pop())
    return path


def find_shortcuts(maze: list[list[str]], path: list[tuple[int, int]]) -> Generator[int, None, None]:
    for idx, node in enumerate(path):
        for shortcut in next_valid_nodes(maze, *node, 2):
            if shortcut in path:
                idx_path = path.index(shortcut)
                savings = idx_path - idx - 2
                if savings > 0:
                    yield savings


def find_long_shortcuts(maze: list[list[str]], path: list[tuple[int, int]]) -> Generator[int, None, None]:
    for idx, node in enumerate(path):
        for shortcut in next_valid_nodes_diamond(maze, *node, 20):
            dx = abs(shortcut[0] - node[0])
            dy = abs(shortcut[1] - node[1])
            if dx + dy > 20:
                continue
            if shortcut in path:
                idx_path = path.index(shortcut)
                savings = idx_path - idx - dx - dy
                if savings > 0:
                    yield savings


def print_maze(maze_data: list[list[str]]) -> None:
    print('\n'.join(''.join(line) for line in maze_data))


def part1(filename: str) -> list[int]:
    maze_data = parse_file(filename)
    # maze = AStarSolver.Maze(maze_data)
    path = get_first_valid_path(maze_data)
    shortcuts = list(find_shortcuts(maze_data, path))

    return shortcuts


def part2(filename: str) -> list[int]:
    maze_data = parse_file(filename)
    # maze = AStarSolver.Maze(maze_data)
    path = get_first_valid_path(maze_data)
    shortcuts = list(find_long_shortcuts(maze_data, path))

    return shortcuts


part_1_sample_shortcuts = [
    *[2 for _ in range(14)],
    *[4 for _ in range(14)],
    *[6 for _ in range(2)],
    *[8 for _ in range(4)],
    *[10 for _ in range(2)],
    *[12 for _ in range(3)],
    20,
    36,
    38,
    40,
    64,
]

part_2_sample_shortcuts = [
    *[50 for _ in range(32)],
    *[52 for _ in range(31)],
    *[54 for _ in range(29)],
    *[56 for _ in range(39)],
    *[58 for _ in range(25)],
    *[60 for _ in range(23)],
    *[62 for _ in range(20)],
    *[64 for _ in range(19)],
    *[66 for _ in range(12)],
    *[68 for _ in range(14)],
    *[70 for _ in range(12)],
    *[72 for _ in range(22)],
    *[74 for _ in range(4)],
    *[76 for _ in range(3)],
]


def main():
    assert sorted(part1('sample.txt')) == sorted(part_1_sample_shortcuts), sorted(part1('sample.txt'))
    print('Part 1: ', sum(1 for shortcut in part1('input.txt') if shortcut >= 100))
    part_2_shortcuts = sorted([shortcut for shortcut in part2('sample.txt') if shortcut >= 50])
    for value in set(part_2_shortcuts):
        print(f'Part 2: {value} -> {part_2_shortcuts.count(value)}')
    assert sorted(part_2_shortcuts) == sorted(part_2_sample_shortcuts), sorted(part_2_shortcuts)
    print('Part 2: ', sum(1 for shortcut in part2('input.txt') if shortcut >= 100))


if __name__ == '__main__':
    main()
