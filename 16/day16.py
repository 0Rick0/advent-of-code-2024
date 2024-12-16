import copy
from timeit import timeit

import AStarSolver


def parse_file(filename: str) -> list[list[str]]:
    maze: list[list[str]] = []
    with open(filename) as f:
        for line in f:
            maze.append([*line.strip()])
    return maze


def part1(filename: str) -> int:
    maze = parse_file(filename)
    maze_ = AStarSolver.Maze(maze)
    path = AStarSolver.AStarSolver().solve_maze(maze_)
    path.reverse()
    # new_maze = copy.copy(maze)
    # for node in path:
    #     new_maze[node.y][node.x] = 'O'
    # print('\n'.join(''.join(line) for line in new_maze))
    return sum(map(lambda a: a[0].weight(a[1]), zip(path, path[1:])))


def part2(filename: str) -> int:
    maze = parse_file(filename)
    maze_ = AStarSolver.Maze(maze)
    all_solutions = AStarSolver.AStarSolver().solve_all_maze_solutions(maze_)
    all_coords: set[tuple[int, int]] = set()
    for solution in all_solutions:
        for node in solution:
            all_coords.add((node.x, node.y))
    new_maze = copy.copy(maze)
    for (x, y) in all_coords:
        new_maze[y][x] = 'O'
    print('\n'.join(''.join(line) for line in new_maze))
    return len(all_coords)


def main():
    time = timeit(lambda: part1('sample1.txt'), number=10)
    print(f'Part 1: {time}')
    assert part1('sample1.txt') == 7036, part1('sample1.txt')
    assert part1('sample2.txt') == 11048
    print('Part 1: ', part1('input.txt'))
    # assert part2('sample1.txt') == 45
    # assert part2('sample2.txt') == 64
    # print('Part 2: ', part2('input.txt'))


if __name__ == '__main__':
    main()
