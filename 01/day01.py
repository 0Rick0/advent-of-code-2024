def parse_file(filename: str) -> list[tuple[int, int]]:
    result = []
    with open(filename) as f:
        for line in f:
            parts = [x for x in line.strip().split(' ') if x]
            if len(parts) != 2:
                print(f'Line: {line!r} not correct length')
                raise ValueError()
            result.append((int(parts[0]), int(parts[1])))
    return result


def part1(filename: str) -> int:
    sample = parse_file(filename)
    first = [i[0] for i in sample]
    second = [i[1] for i in sample]

    total_distance = 0

    for a, b in zip(sorted(first), sorted(second)):
        distance = abs(a - b)
        total_distance += distance

    return total_distance


def part2(filename: str) -> int:
    sample = parse_file(filename)
    first = [i[0] for i in sample]
    second = [i[1] for i in sample]
    return sum(i * second.count(i) for i in first)


if __name__ == '__main__':
    assert part1('sample.txt') == 11
    print(part1('input.txt'))
    assert part2('sample.txt') == 31
    print(part2('input.txt'))
