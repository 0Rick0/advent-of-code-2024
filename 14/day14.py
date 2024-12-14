import math
import re
from dataclasses import dataclass
from enum import Enum
from typing import IO

try:
    from PIL import Image
except ImportError:
    print('Missing pillow, part 2 will not work')

RE_ROBOT = re.compile(r'p=(\d+,\d+) v=(-?\d+,-?\d+)')


class Quadrant(Enum):
    A = 1
    B = 2
    C = 3
    D = 4


@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def simulate(self, field_width: int, field_height: int):
        new_position_x = self.position[0] + self.velocity[0]
        new_position_y = self.position[1] + self.velocity[1]
        if new_position_x < 0:
            new_position_x += field_width
        if new_position_y < 0:
            new_position_y += field_height
        if new_position_x >= field_width:
            new_position_x -= field_width
        if new_position_y >= field_height:
            new_position_y -= field_height
        self.position = (new_position_x, new_position_y)

    def get_quadrant(self, x_cutoff: int, y_cutoff: int) -> Quadrant | None:
        if self.position[0] < x_cutoff and self.position[1] < y_cutoff:
            return Quadrant.A
        elif self.position[0] > x_cutoff and self.position[1] < y_cutoff:
            return Quadrant.B
        elif self.position[0] < x_cutoff and self.position[1] > y_cutoff:
            return Quadrant.C
        elif self.position[0] > x_cutoff and self.position[1] > y_cutoff:
            return Quadrant.D
        return None


def parse_input(filename) -> list[Robot]:
    robots = []
    with open(filename) as f:
        for line in f:
            match = RE_ROBOT.match(line)
            position, velocity = match.groups()
            x, y = map(int, position.split(','))
            vx, vy = map(int, velocity.split(','))
            robots.append(Robot((x, y), (vx, vy)))
    return robots


def draw_field(filename: str, robots: list[Robot], field_width: int, field_height: int):
    robots_per_coord: dict[tuple[int, int], int] = {}
    for robot in robots:
        if robot.position not in robots_per_coord:
            robots_per_coord[robot.position] = 0
        robots_per_coord[robot.position] += 1
    image = Image.new('1', (field_width, field_height), (0,))
    for (x, y) in robots_per_coord.keys():
        image.putpixel((x, y), (1,))
    image.save(filename)


def part1(filename: str, field_width: int, field_height: int) -> int:
    robots = parse_input(filename)
    for iteration in range(100):
        for robot in robots:
            robot.simulate(field_width, field_height)

    quadrants: dict[Quadrant, list[Robot]] = {
        Quadrant.A: [],
        Quadrant.B: [],
        Quadrant.C: [],
        Quadrant.D: [],
    }
    no_quadrant = []
    x_cutoff = math.ceil(field_width / 2) - 1
    y_cutoff = math.ceil(field_height / 2) - 1
    for robot in robots:
        quadrant = robot.get_quadrant(x_cutoff, y_cutoff)
        if quadrant is not None:
            quadrants[quadrant].append(robot)
        else:
            no_quadrant.append(robot)
    return (len(quadrants[Quadrant.A])
            * len(quadrants[Quadrant.B])
            * len(quadrants[Quadrant.C])
            * len(quadrants[Quadrant.D]))


def part2(filename: str, field_width: int, field_height: int) -> int:
    robots = parse_input(filename)
    for iteration in range(10_000):
        draw_field(f'output/{filename.split('.')[0]}-{iteration}.png', robots, field_width, field_height)
        for robot in robots:
            robot.simulate(field_width, field_height)


def test_robot():
    robot = Robot((3, 3), (2, 2))
    assert robot.get_quadrant(4, 4) == Quadrant.A
    assert robot.get_quadrant(3, 3) is None
    assert robot.get_quadrant(4, 3) is None

    robot.simulate(11, 7)
    assert robot.position == (5, 5)
    assert robot.get_quadrant(4, 4) == Quadrant.D
    robot.simulate(11, 7)
    assert robot.position == (7, 0)
    robot.simulate(11, 7)
    assert robot.position == (9, 2)

    robot = Robot((1, 1), (-2, -2))
    robot.simulate(11, 7)
    assert robot.position == (10, 6)

    robot = Robot((1, 3), (-2, -2))
    assert robot.get_quadrant(5, 3) is None


def main():
    test_robot()
    assert part1('sample.txt', 11, 7) == 12, print(part1('sample.txt', 11, 7))
    print(part1('input.txt', 101, 103))

    part2('input.txt', 101, 103)


if __name__ == '__main__':
    main()
