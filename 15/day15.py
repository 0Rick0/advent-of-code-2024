from dataclasses import dataclass
from typing import List


@dataclass
class WarehouseObject:
    x: int
    y: int
    width: int

    def get_gps(self) -> int:
        return self.x + self.y * 100

    def get_next_coords(self, direction: str) -> tuple[int, int]:
        match direction:
            case "<":
                return self.x - 1, self.y
            case ">":
                return self.x + 1, self.y
            case "V" | 'v':
                return self.x, self.y + 1
            case "^":
                return self.x, self.y - 1
            case _:
                raise ValueError(f"Invalid direction {direction}")


@dataclass
class Robot(WarehouseObject):
    pass


@dataclass
class Box(WarehouseObject):
    pass


@dataclass
class Wall(WarehouseObject):
    pass


@dataclass
class Warehouse:
    walls: List[Wall]
    boxes: List[Box]
    robots: List[Robot]
    moves: list[str]
    move_index: int = 0

    def get_object_at(self, x: int, y: int) -> WarehouseObject | None:
        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return wall
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        for robot in self.robots:
            if robot.x == x and robot.y == y:
                return robot
        return None

    def can_move_one(self, warehouse_object: WarehouseObject, direction: str) -> bool:
        next_x, next_y = warehouse_object.get_next_coords(direction)
        object_in_way = self.get_object_at(next_x, next_y)
        if object_in_way:
            if isinstance(object_in_way, Wall):
                return False
            return self.can_move_one(object_in_way, direction)
        else:
            return True

    def do_move_one(self, warehouse_object: WarehouseObject, direction: str):
        next_x, next_y = warehouse_object.get_next_coords(direction)
        object_in_way = self.get_object_at(next_x, next_y)
        if object_in_way:
            if isinstance(object_in_way, Wall):
                raise ValueError('Not expected, wall in way')
            self.do_move_one(object_in_way, direction)
        warehouse_object.x = next_x
        warehouse_object.y = next_y

    def do_move(self):
        move = self.moves[self.move_index]
        self.move_index += 1

        for robot in self.robots:
            if self.can_move_one(robot, move):
                self.do_move_one(robot, move)

    def stringify_field(self) -> str:
        width = max(*[wall.x for wall in self.walls]) + 1
        height = max(*[wall.y for wall in self.walls]) + 1
        fields = [['.'] * width for _ in range(height)]
        for wall in self.walls:
            fields[wall.y][wall.x] = '#'
        for box in self.boxes:
            fields[box.y][box.x] = 'O'
        for robot in self.robots:
            fields[robot.y][robot.x] = '@'
        return '\n'.join(''.join(field) for field in fields)


def parse_input(filename: str, object_width: int) -> Warehouse:
    walls = []
    boxes = []
    robots = []
    moves = []
    with open(filename) as f:
        for y, line in enumerate(f):
            if not line.strip():
                break  # blank line, now continuing with moves
            for x, c in enumerate(line.strip()):
                if c == "#":
                    walls.append(Wall(x * object_width, y, object_width))
                elif c == "O":
                    boxes.append(Box(x * object_width, y, object_width))
                elif c == '@':
                    robots.append(Robot(x * object_width, y, 1))
                elif c == '.':
                    continue
                else:
                    print(f'Unknown character {c!r}')
        for line in f:
            moves.extend(line.strip())
    return Warehouse(walls, boxes, robots, moves)


def part1(filename: str) -> int:
    warehouse = parse_input(filename, 1)
    assert len(warehouse.robots) == 1
    while warehouse.move_index < len(warehouse.moves):
        warehouse.do_move()

    print(warehouse.stringify_field())

    return sum(box.get_gps() for box in warehouse.boxes)


def main():
    assert part1('sample1.txt') == 2028
    assert part1('sample2.txt') == 10092
    print(part1('input.txt'))


if __name__ == '__main__':
    main()
