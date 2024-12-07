import math
import operator
from dataclasses import dataclass
from typing import Generator

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable):
        return iterable

operators = [
    operator.add,
    operator.mul,
]


# https://stackoverflow.com/a/12838701
# Interestingly enough, this isn't (significantly) faster the int/str implementation
# I've left it in here anyway, but I've used my original implementation
def concat(x: int, y: int) -> int:
    if y != 0:
        a = math.floor(math.log10(y))
    else:
        a = -1
    return int(x * 10 ** (1 + a) + y)


operators2 = [
    operator.add,
    operator.mul,
    # concat,
    lambda a, b: int(str(a) + str(b)),
]


@dataclass
class Record:
    expected: int
    values: list[int]


def parse_input(filename: str) -> list[Record]:
    records = []
    with open(filename) as inp:
        for line in inp:
            expected, values = line.strip().split(':')
            values = values.strip().split(' ')
            records.append(Record(int(expected), list(map(int, values))))

    return records


def get_possible_values(values: list[int], ops) -> Generator[int, None, None]:
    if len(values) < 2:
        yield values[0]
        return
    a, b, *rest = values
    for op in ops:
        yield from get_possible_values([op(a, b), *rest], ops)


def part1(filename: str) -> int:
    records = parse_input(filename)
    valid_records = []
    for record in tqdm(records):
        for possible_value in get_possible_values(record.values, operators):
            if possible_value == record.expected:
                valid_records.append(record)
                break
    return sum(val.expected for val in valid_records)


def part2(filename: str) -> int:
    records = parse_input(filename)
    valid_records = []
    for record in tqdm(records):
        for possible_value in get_possible_values(record.values, operators2):
            if possible_value == record.expected:
                valid_records.append(record)
                break
    return sum(val.expected for val in valid_records)


def main():
    assert part1('sample.txt') == 3749, print(part1('sample.txt'))
    print(part1('input.txt'))
    assert part2('sample.txt') == 11387, print(part1('sample.txt'))
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
