import enum


class Cardinal(enum.Enum):
    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    SOUTH_EAST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    NORTH_WEST = 7


def next_coord(x: int, y: int, cardinal: Cardinal) -> tuple[int, int]:
    match cardinal:
        case Cardinal.NORTH:
            return x, y - 1
        case Cardinal.NORTH_EAST:
            return x + 1, y - 1
        case Cardinal.EAST:
            return x + 1, y
        case Cardinal.SOUTH_EAST:
            return x + 1, y + 1
        case Cardinal.SOUTH:
            return x, y + 1
        case Cardinal.SOUTH_WEST:
            return x - 1, y + 1
        case Cardinal.WEST:
            return x - 1, y
        case Cardinal.NORTH_WEST:
            return x - 1, y - 1
        case _:
            raise ValueError(f"Unknown cardinal {cardinal.value}")


def find_word(matrix: list[list[str]], x: int, y: int, word: str, cardinal: Cardinal) -> bool:
    if matrix[y][x] != word[0]:
        return False

    if len(word) == 1:
        return True  # found last letter

    next_x, next_y = next_coord(x, y, cardinal)

    # detect edge
    if next_x < 0 or next_x >= len(matrix[y]):
        return False
    if next_y < 0 or next_y >= len(matrix):
        return False
    return find_word(matrix, next_x, next_y, word[1:], cardinal)


def find_all_words(matrix: list[list[str]], x: int, y: int, word: str) -> int:
    count = 0
    for c in Cardinal:
        if find_word(matrix, x, y, word, c):
            count += 1
    return count


def part1(filename: str, search_string: str = 'XMAS') -> int:
    print(f"Part 1: {filename}")
    with open(filename) as f:
        matrix = [[c for c in line.strip()] for line in f]

    count = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            count += find_all_words(matrix, x, y, search_string)
    return count


def find_xmas_around(matrix: list[list[str]], x: int, y: int) -> bool:
    if not find_word(matrix, x - 1, y - 1, 'MAS', Cardinal.SOUTH_EAST) \
            and not find_word(matrix, x - 1, y - 1, 'SAM', Cardinal.SOUTH_EAST):
        return False
    if not find_word(matrix, x + 1, y - 1, 'MAS', Cardinal.SOUTH_WEST) \
            and not find_word(matrix, x + 1, y - 1, 'SAM', Cardinal.SOUTH_WEST):
        return False
    return True


def part2(filename: str) -> int:
    print(f"Part 2: {filename}")
    with open(filename) as f:
        matrix = [[c for c in line.strip()] for line in f]

    count = 0
    for y in range(1, len(matrix) - 1):
        for x in range(1, len(matrix[y]) - 1):
            if matrix[y][x] == "A":
                if find_xmas_around(matrix, x, y):
                    count += 1
    return count


def main():
    assert find_all_words([['X', 'M']], 0, 0, 'XM') == 1
    assert find_all_words([['M', 'X']], 1, 0, 'XM') == 1
    assert find_all_words([
        ['A', 'X'],
        ['B', 'M']
    ], 1, 0, 'XM') == 1
    assert find_all_words([
        ['A', 'X'],
        ['M', 'B']
    ], 1, 0, 'XM') == 1
    assert find_all_words([
        ['A', 'M'],
        ['X', 'B']
    ], 0, 1, 'XM') == 1
    assert find_all_words([
        ['A', 'M'],
        ['X', 'M']
    ], 0, 1, 'XM') == 2
    assert part1('sample.txt') == 18
    print(part1('input.txt'))
    assert find_xmas_around([
        ['M', '.', 'M'],
        ['.', 'A', '.'],
        ['S', '.', 'S'],
    ], 1, 1)
    assert find_xmas_around([
        ['S', '.', 'S'],
        ['.', 'A', '.'],
        ['M', '.', 'M'],
    ], 1, 1)
    assert find_xmas_around([
        ['M', '.', 'S'],
        ['.', 'A', '.'],
        ['M', '.', 'S'],
    ], 1, 1)
    assert find_xmas_around([
        ['S', '.', 'M'],
        ['.', 'A', '.'],
        ['S', '.', 'M'],
    ], 1, 1)
    assert part2('sample.txt') == 9
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
