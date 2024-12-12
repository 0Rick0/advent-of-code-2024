from dataclasses import dataclass
from typing import Optional


@dataclass
class Region:
    fields: list["Field"]

    def __init__(self):
        self.fields = []

    def __hash__(self):
        return id(self)

    def area(self) -> int:
        return len(self.fields)

    def perimeter(self) -> int:
        return sum(4 - len(field.neighbours()) for field in self.fields)

    def calculate_price(self) -> int:
        return self.area() * self.perimeter()

    def calculate_bulk_price(self) -> int:
        return self.area() * self.no_faces()

    def no_faces(self) -> int:
        return sum([
            self.no_faces_direction((0, 1), (-1, 0), (1, 0)),
            self.no_faces_direction((0, -1), (-1, 0), (1, 0)),
            self.no_faces_direction((1, 0), (0, -1), (0, 1)),
            self.no_faces_direction((-1, 0), (0, -1), (0, 1)),
        ])

    def no_faces_direction(self,
                           break_direction: tuple[int, int],
                           negative_direction: tuple[int, int],
                           positive_direction: tuple[int, int]) -> int:
        faces: list[list[Field]] = []
        fields_already_in_face: set[Field] = set()
        for field in self.fields:
            if field in fields_already_in_face:
                continue
            face = field.faces_in_plane(break_direction, negative_direction, positive_direction)
            if len(face) == 0:
                # this field is not part of a plane
                continue
            faces.append(list(face))
            fields_already_in_face.update(face)
        return len(faces)


@dataclass
class Field:
    character: str
    x: int
    y: int
    region: Region = None

    def set_region(self, region: Region):
        if region is self.region:
            return
        if self.region:
            region = merge_regions(self.region, region)
        self.region = region
        self.register_self()

    def new_region(self):
        self.region = Region()
        self.register_self()

    def register_self(self):
        if self not in self.region.fields:
            self.region.fields.append(self)

    def faces_in_plane(self,
                       break_direction: tuple[int, int],
                       negative_direction: tuple[int, int],
                       positive_direction: tuple[int, int]) -> set["Field"]:
        faces = set()
        current = self
        while current and not current.neighbour_in_direction(*break_direction):
            faces.add(current)
            current = current.neighbour_in_direction(*negative_direction)
        current = self
        while current and not current.neighbour_in_direction(*break_direction):
            faces.add(current)
            current = current.neighbour_in_direction(*positive_direction)
        return faces

    def neighbour_in_direction(self, x: int, y: int) -> Optional["Field"]:
        for field in self.region.fields:
            if field.x == self.x + x and field.y == self.y + y:
                return field
        return None

    def neighbours(self) -> list["Field"]:
        neighbours: set["Field"] = set()
        for x in range(-1, 2, 2):
            neighbour = self.neighbour_in_direction(x, 0)
            if neighbour:
                neighbours.add(neighbour)
        for y in range(-1, 2, 2):
            neighbour = self.neighbour_in_direction(0, y)
            if neighbour:
                neighbours.add(neighbour)

        return list(neighbours)

    def __hash__(self):
        return id(self)


def merge_regions(region_a: Region, region_b: Region) -> Region:
    all_fields = region_a.fields + region_b.fields
    new_region = Region()
    new_region.fields = all_fields
    for field in all_fields:
        field.region = new_region
    return new_region


def parse_input(filename: str) -> list[list[Field]]:
    data = []
    with open(filename) as f:
        for y, line in enumerate(f):
            data_line = []
            data.append(data_line)
            for x, c in enumerate(line.strip()):
                data_line.append(Field(c, x, y))
    return data


def get_regions(filename) -> list[Region]:
    data = parse_input(filename)
    for y, line in enumerate(data):
        for x, field in enumerate(line):
            if x > 0:
                if line[x - 1].character == field.character:
                    field.set_region(line[x - 1].region)
            if y > 0:
                if data[y - 1][x].character == field.character:
                    field.set_region(data[y - 1][x].region)
            if field.region is None:
                field.new_region()
    regions = set()
    for line in data:
        for field in line:
            regions.add(field.region)
    return list(regions)


def part1(filename: str) -> int:
    regions = get_regions(filename)
    return sum(region.calculate_price() for region in regions)


def part2(filename: str) -> int:
    regions = get_regions(filename)
    return sum(region.calculate_bulk_price() for region in regions)


def main():
    assert part1('sample1.txt') == 140, part1('sample1.txt')
    assert part1('sample2.txt') == 772, part1('sample2.txt')
    assert part1('sample3.txt') == 1930, part1('sample3.txt')
    print('Part 1: ', part1('input.txt'))

    assert part2('sample1.txt') == 80, part2('sample1.txt')
    assert part2('sample2.txt') == 436, part2('sample2.txt')
    assert part2('sample3.txt') == 1206, part2('sample3.txt')
    assert part2('sample4.txt') == 236, part2('sample4.txt')
    assert part2('sample5.txt') == 368, part2('sample5.txt')
    print('Part 2: ', part2('input.txt'))


if __name__ == '__main__':
    main()
