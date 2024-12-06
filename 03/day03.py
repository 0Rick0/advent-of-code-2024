import re

MUL_PATTERN = re.compile(r'mul\((\d+),(\d+)\)')
INSTRUCTION_PATTERN = re.compile(r'(do(?:n\'t)?|mul)\((?:(\d+),(\d+))?\)')


def get_instructions(inp: str) -> list[tuple[str, str, str]]:
    return INSTRUCTION_PATTERN.findall(inp)


def part1(filename: str) -> int:
    with open(filename) as f:
        muls = get_instructions(f.read())
    return sum(int(parts[1]) * int(parts[2]) for parts in muls if parts[0] == 'mul' and muls[1] and muls[2])


def part2(filename: str) -> int:
    with open(filename) as f:
        instructions = get_instructions(f.read())
    result = 0
    active = True
    for instruction in instructions:
        match instruction:
            case 'do', _, _:
                active = True
            case 'don\'t', _, _:
                active = False
            case 'mul', a, b:
                if active:
                    result += int(a) * int(b)
    return result


def main():
    assert part1('sample.txt') == 161
    print(part1('input.txt'))
    assert part2('sample2.txt') == 48
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
