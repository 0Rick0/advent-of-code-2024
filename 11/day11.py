import timeit
from functools import cache

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x):
        return x


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return list(map(int, f.readline().strip().split(' ')))


@cache
def stone_blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    stone_str_len = len(stone_str)
    if stone_str_len & 1 == 0:
        return list(map(int, [stone_str[:stone_str_len // 2], stone_str[stone_str_len // 2:]]))

    return [stone * 2024]


def blink(stones: list[int]) -> list[int]:
    out: list[int] = []
    for stone in stones:
        out.extend(stone_blink(stone))
    return out


def part1a(filename: str) -> int:
    clear_cache()
    data = parse_input(filename)
    for _ in range(25):
        data = blink(data)

    return len(data)


# The solution to part 2 was cache :sweat_smile:
@cache
def blink_depth(stone: int, depth: int) -> int:
    next_stones = stone_blink(stone)
    if depth == 1:
        return len(next_stones)
    else:
        return sum(blink_depth(next_stone, depth - 1) for next_stone in next_stones)


def part1b(filename: str) -> int:
    clear_cache()
    data = parse_input(filename)
    return sum(blink_depth(stone, 25) for stone in data)


def part2(filename: str) -> int:
    data = parse_input(filename)
    total_len = sum(blink_depth(stone, 75) for stone in data)
    return total_len


def clear_cache():
    stone_blink.cache_clear()
    blink_depth.cache_clear()


def main():
    assert blink([0, 1, 10, 99, 999]) == [1, 2024, 1, 0, 9, 9, 2021976], blink([0, 1, 10, 99, 999])
    assert blink([125, 17]) == [253000, 1, 7], blink([127, 17])
    assert blink([253000, 1, 7]) == [253, 0, 2024, 14168]
    assert part1a('sample2.txt') == 55312, part1a('sample2.txt')
    assert part1b('sample2.txt') == 55312, part1b('sample2.txt')
    time_part1a = timeit.timeit(lambda: part1a('sample2.txt'), number=100)
    print(f'Part 1a took {time_part1a} seconds on average')
    time_part1b = timeit.timeit(lambda: part1b('sample2.txt'), number=100)
    print(f'Part 1b took {time_part1b} seconds on average')
    print('Part 1: ', part1b('input.txt'))
    print('Part 2: ', part2('input.txt'))
    print(stone_blink.cache_info())
    print(blink_depth.cache_info())


if __name__ == '__main__':
    main()
