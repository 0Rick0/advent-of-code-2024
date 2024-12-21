from itertools import permutations


class KeyPad:
    keys: list[list[str]]
    position: tuple[int, int]
    illegal_positions: list[tuple[int, int]]

    def __init__(self, keys: list[list[str]]) -> None:
        self.illegal_positions = []
        self.keys = keys
        for y, row in enumerate(self.keys):
            for x, c in enumerate(row):
                if c == 'A':
                    self.position = (x, y)
                if c is None:
                    self.illegal_positions.append((x, y))

    def move_to(self, destination: tuple[int, int]) -> list[str]:
        dx = destination[0] - self.position[0]
        dy = destination[1] - self.position[1]
        mx = (['<'] if dx < 0 else ['>']) * abs(dx)
        my = (['^'] if dy < 0 else ['v']) * abs(dy)
        self.position = destination
        return sorted(mx + my) + ['A']

    def distance_to(self, other: tuple[int, int]) -> int:
        dx = other[0] - self.position[0]
        dy = other[1] - self.position[1]
        return abs(dx) + abs(dy)

    def find_key(self, value: str) -> tuple[int, int]:
        for y, row in enumerate(self.keys):
            for x, c in enumerate(row):
                if c == value:
                    return x, y
        raise ValueError(f'Unknown key: {value}')


def split_list(data: list[str], split: str) -> list[list[str]]:
    if split not in data:
        return [data]
    output: list[list[str]] = []
    remainder = data
    while remainder:
        idx = remainder.index('A')
        output.append(remainder[:idx])
        remainder = remainder[idx + 1:]
    return output


def find_shortest_moves(start_position: tuple[int, int], moves: list[tuple[int, int, str]]) -> list[
    tuple[int, int, str]]:
    if not moves:
        return []
    shortest_moves: list[tuple[int, int, str]] | None = None
    shortest_distance: int = int(1e9)

    for permutation in permutations(moves):
        current_x, current_y = start_position
        total_distance = 0
        for x, y, _ in permutation:
            distance = abs(current_x - x) + abs(current_y - y)
            total_distance += distance
            current_x, current_y = x, y
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_moves = list(permutation)
    if not shortest_moves:
        raise ValueError('No valid moves')
    return shortest_moves


class RobotStack:
    key_pads: list[KeyPad]

    def __init__(self, key_pads: list[KeyPad]) -> None:
        self.key_pads = key_pads

    def move_to(self, value: list[str]) -> list[str]:
        moves = value
        for pad in self.key_pads:
            new_moves = []
            for split in split_list(moves, 'A'):
                for dest_x, dest_y, move in find_shortest_moves(
                        pad.position,
                        [(*pad.find_key(move), move) for move in split],
                ):
                    new_moves += pad.move_to((dest_x, dest_y))
                new_moves += pad.move_to(pad.find_key('A'))
            moves = new_moves
        return moves


def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return list(map(str.strip, f.readlines()))


door_key_pad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A'],
]
direction_key_pad = [
    [None, '^', 'A'],
    ['<', 'v', '>']
]


def part1(filename: str) -> int:
    codes = parse_input(filename)
    score = 0
    for code in codes:
        robot_stack = RobotStack([
            KeyPad(door_key_pad),
            KeyPad(direction_key_pad),
            KeyPad(direction_key_pad),
            # KeyPad(direction_key_pad),
        ])
        moves = robot_stack.move_to([*code])
        print(f'{code}: {"".join(moves)} {len(moves)}')
        score += len(moves) * int(''.join(char for char in code if char.isdigit()))
    print(score)
    return score


def main():
    assert part1("sample.txt") == 126384
    print("Part One:", part1("input.txt"))


if __name__ == '__main__':
    main()
