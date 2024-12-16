from pprint import pprint

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
    return sum(map(lambda a: a[0].weight(a[1]), zip(path, path[1:])))


def main():
    assert part1('sample1.txt') == 7036, part1('sample1.txt')
    assert part1('sample2.txt') == 11048
    print('Part 1: ', part1('input.txt'))


if __name__ == '__main__':
    main()
