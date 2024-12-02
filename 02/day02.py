import operator


def parse_input(filename: str) -> list[list[int]]:
    with open(filename) as f:
        return [list(map(int, line.split())) for line in f.readlines()]

def report_is_safe(report: list[int]) -> bool:
    op = operator.gt if report[0] >= report[1] else operator.lt
    for a, b in zip(report, report[1:]):
        if not op(a, b):
            # print(f"not safe {a} {op.__name__} {b}")
            return False
        if abs(a - b) > 3:
            # print(f"not safe {a} +- {b} > 3")
            return False
    # print(f"safe {report}")
    return True

def part1(filename: str) -> int:
    return sum(1 for _ in filter(report_is_safe, parse_input(filename)))


def mutate_report(report: list[int]) -> list[list[int]]:
    new_reports = []
    for i in range(len(report)):
        new_report = list(report)
        del new_report[i]
        new_reports.append(new_report)
    return new_reports


def part2(filename: str) -> int:
    # This solution is not really optimized
    # But the dataset is small enough that it doesn't matter
    # To optimize this, a similar operator check can be done as report_is_safe around the index of the first unsafe value
    # That way only 3 values have to be considered for removal
    result = 0
    for report in parse_input(filename):
        if report_is_safe(report):
            result += 1
            continue
        for mutated_report in mutate_report(report):
            if report_is_safe(mutated_report):
                result += 1
                break
    return result

def main():
    assert report_is_safe([1, 2])
    assert report_is_safe([2, 1])
    assert not report_is_safe([2, 1, 2])
    assert not report_is_safe([1, 10])
    assert not report_is_safe([1, 1])
    assert not report_is_safe([1, 2, 2])
    assert part1('sample.txt') == 2
    print(part1('input.txt'))

    assert part2('sample.txt') == 4
    print(part2('input.txt'))

if __name__ == '__main__':
    main()
