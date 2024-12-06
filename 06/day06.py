import enum
from dataclasses import dataclass

try:
    # https://pypi.org/project/tqdm/
    from tqdm import tqdm
except ImportError:
    def tqdm(iterator):
        return iterator

class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def get_next_direction(self) -> "Direction":
        new_value = (self.value + 1) % 4
        return Direction(new_value)


@dataclass
class Point:
    x: int
    y: int


    def get_next(self, direction: Direction) -> "Point":
        match direction:
            case Direction.NORTH:
                return Point(self.x, self.y - 1)
            case Direction.EAST:
                return Point(self.x + 1, self.y)
            case Direction.SOUTH:
                return Point(self.x, self.y + 1)
            case Direction.WEST:
                return Point(self.x - 1, self.y)
            case _:
                raise ValueError("Invalid direction")

    def is_in_bounds(self, max_x: int, max_y: int) -> bool:
        if self.x < 0 or self.y < 0:
            return False
        if self.x > max_x or self.y > max_y:
            return False
        return True

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


def parse_file(filename: str) -> tuple[dict[Point, str], tuple[int, int]]:
    entities: dict[Point, str] = {}
    max_y = 0
    max_x = 0
    with open(filename) as f:
        for y, line in enumerate(f):
            max_y = max(max_y, y)
            for x, character in enumerate(line.strip()):
                max_x = max(max_x, x)
                if character in '#^':
                    entities[Point(x, y)] = character
    return entities, (max_x, max_y)


def parse_input(filename):
    entities, (max_x, max_y) = parse_file(filename)
    guard = None
    for index, value in entities.items():
        if value == '^':
            if guard is not None:
                raise ValueError('Multiple guards')
            guard = index
    del entities[guard]
    objects = list(entities.keys())
    return guard, max_x, max_y, objects


def guard_move(objects: list[Point], position: Point, direction: Direction) -> tuple[Point, Direction]:
    next_point = position.get_next(direction)
    new_direction = direction
    while next_point in objects:
        new_direction = new_direction.get_next_direction()
        next_point = position.get_next(new_direction)
    return next_point, new_direction


def get_all_possible_positions(initial_guard: Point, max_x: int, max_y: int, objects: list[Point]) -> set[
    tuple[Point, Direction]]:
    direction = Direction.NORTH
    guard = initial_guard
    all_known_positions = set()
    while guard.is_in_bounds(max_x, max_y):
        # print(f'Guard is at {guard} facing {direction}')
        if (guard, direction) in all_known_positions:
            raise ValueError('Guard is looping')
        all_known_positions.add((guard, direction))
        guard, direction = guard_move(objects, guard, direction)
        # print(f'Next position is {guard}')
    return all_known_positions


def part1(filename: str) -> int:
    guard, max_x, max_y, objects = parse_input(filename)

    all_possible_positions = get_all_possible_positions(guard, max_x, max_y, objects)
    return len(set(v[0] for v in all_possible_positions))


def part2(filename: str) -> int:
    guard, max_x, max_y, objects = parse_input(filename)

    all_known_positions = get_all_possible_positions(guard, max_x, max_y, objects)
    all_known_points = set(position[0] for position in all_known_positions)

    loops = set()
    for point in tqdm(all_known_points):
        try:
            # optimization idea: start at the position just before the obstacle.
            # The loop will only deviate from the base route from the obstacle onwards, so the rest of the route doesn't matter.
            # Unfortunate the previous position and direction are not available right now.
            # They also can't be calculated as the guard might turn twice in one move
            get_all_possible_positions(guard, max_x, max_y, [*objects, point])
        except ValueError:
            loops.add(point)

    return len(loops)


def main():
    assert part1('sample.txt') == 41, print(part1('sample.txt'))
    print(part1('input.txt'))
    # #.
    # ^#
    # *.  * is expected
    assert guard_move([
        Point(0, 0),
        Point(1, 1),
    ], Point(0, 1), Direction.NORTH) == (Point(0, 2), Direction.SOUTH)
    assert part2('sample.txt') == 6, print(part2('sample.txt'))
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
