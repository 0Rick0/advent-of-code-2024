import AStarSolver


def parse_file(filename: str) -> list[tuple[int, int]]:
    data = []
    with open(filename) as f:
        for line in f:
            data.append(tuple(map(int, line.split(','))))
    return data


def get_first_valid_path(maze: AStarSolver.Maze) -> list[AStarSolver.Node]:
    return AStarSolver.AStarSolver().solve_maze(maze)


def path_is_valid(nodes: list[AStarSolver.Node], maze: AStarSolver.Maze) -> bool:
    for node in nodes:
        if not maze.node_valid(node):
            return False
    return True


def print_maze(maze_data: list[list[str]]) -> None:
    print('\n'.join(''.join(line) for line in maze_data))


def part1(filename: str, size: int, time: int) -> int:
    data = parse_file(filename)
    maze_data = [['.'] * size for _ in range(size)]
    for x, y in data[:time]:
        maze_data[y][x] = '#'
    start = (0, 0)
    end = (size - 1, size - 1)
    maze = AStarSolver.Maze(maze_data, start, end)
    path = get_first_valid_path(maze)
    return len(path) - 1


def part2(filename: str, size: int, time: int) -> tuple[int, int]:
    data = parse_file(filename)
    maze_data = [['.'] * size for _ in range(size)]
    for x, y in data[:time]:
        maze_data[y][x] = '#'

    start = (0, 0)
    end = (size - 1, size - 1)
    maze = AStarSolver.Maze(maze_data, start, end)
    last_known_path = get_first_valid_path(maze)
    remaining_data = data[time:]
    while True:
        next_x, next_y = remaining_data.pop(0)
        maze_data[next_y][next_x] = '#'
        # if not path_is_valid(last_known_path, maze):
        if any(node.x == next_x and node.y == next_y for node in last_known_path):
            print('Path broke, finding new path')
            try:
                last_known_path = get_first_valid_path(maze)
            except IndexError:
                print_maze(maze_data)
                return next_x, next_y


def main():
    assert part1('sample.txt', 7, 12) == 22, part1('sample.txt', 7, 12)
    print('Part 1: ', part1('input.txt', 71, 1024))
    assert part2('sample.txt', 7, 12) == (6, 1), part2('sample.txt', 7, 12)
    print('Part 2: ', part2('input.txt', 71, 1024))


if __name__ == '__main__':
    main()
