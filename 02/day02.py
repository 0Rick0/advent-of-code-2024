import operator


def parse_input(filename: str) -> list[list[int]]:
    with open(filename) as f:
        return [list(map(int, line.split())) for line in f.readlines()]

def report_is_safe(report: list[int]) -> tuple[int, bool]:
    op = operator.gt if report[0] >= report[1] else operator.lt
    for idx, (a, b) in enumerate(zip(report, report[1:])):
        if not op(a, b):
            # print(f"not safe {a} {op.__name__} {b}")
            return idx, False
        if abs(a - b) > 3:
            # print(f"not safe {a} +- {b} > 3")
            return idx, False
    # print(f"safe {report}")
    return -1, True

def part1(filename: str) -> int:
    return sum(1 for report in parse_input(filename) if report_is_safe(report)[1])


def mutate_report(report: list[int], idx) -> list[list[int]]:
    new_reports = []
    for i in range(max(idx - 1, 0), min(idx + 1, len(report)) + 1):
        new_report = list(report)
        del new_report[i]
        new_reports.append(new_report)
    return new_reports


def part2(filename: str) -> int:
    result = 0
    for report in parse_input(filename):
        idx, safe = report_is_safe(report)
        if safe:
            result += 1
            continue
        for mutated_report in mutate_report(report, idx):
            if report_is_safe(mutated_report)[1]:
                result += 1
                break
    return result

def main():
    assert report_is_safe([1, 2])[1]
    assert report_is_safe([2, 1])[1]
    assert not report_is_safe([2, 1, 2])[1]
    assert not report_is_safe([1, 10])[1]
    assert not report_is_safe([1, 1])[1]
    assert not report_is_safe([1, 2, 2])[1]
    assert part1('sample.txt') == 2
    print(part1('input.txt'))

    assert part2('sample.txt') == 4
    print(part2('input.txt'))

if __name__ == '__main__':
    main()
