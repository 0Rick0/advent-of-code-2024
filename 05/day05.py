class InputRule:
    def __init__(self, number: int, before: int):
        self.number = number
        self.before = before

    def __repr__(self) -> str:
        return f'InputRule[{self.number} before {self.before}]'


def parse_input(filename: str) -> tuple[list[InputRule], list[list[int]]]:
    rules = []
    updates = []
    with open(filename) as f:
        for line in f:
            if line.strip() == "":
                break  # end of rules, continue to updates
            number, before = line.strip().split('|')
            rules.append(InputRule(int(number), int(before)))

        for line in f:
            updates.append(list(map(int, line.strip().split(','))))

    return rules, updates


def find_applicable_rules(rules: list[InputRule], update: list[int]) -> list[InputRule]:
    return [rule for rule in rules if rule.number in update and rule.before in update]


def update_is_correct(update: list[int], rules: list[InputRule]) -> tuple[bool, int]:
    applicable_rules = find_applicable_rules(rules, update)
    for index, page in enumerate(update):
        for rule in applicable_rules:
            if rule.number == page:
                if rule.before in update[:index]:
                    return False, index

    return True, -1


def fix_update(update: list[int], rules: list[InputRule]) -> list[int]:
    applicable_rules = find_applicable_rules(rules, update)
    current_update = update[:]
    while True:
        is_correct, index = update_is_correct(current_update, applicable_rules)
        if is_correct:
            break
        # Move back once at index
        current_update[index - 1:index + 1] = current_update[index - 1:index + 1][::-1]

    return current_update


def part1(filename: str) -> int:
    rules, updates = parse_input(filename)
    result = 0
    for update in updates:
        if update_is_correct(update, rules)[0]:
            result += update[len(update) // 2]
    return result


def part2(filename: str) -> int:
    rules, updates = parse_input(filename)
    incorrect = []
    for update in updates:
        if not update_is_correct(update, rules)[0]:
            incorrect.append(update)

    result = 0
    for update in incorrect:
        fixed = fix_update(update, rules)
        result += fixed[len(fixed) // 2]
    return result


def main():
    assert part1('sample.txt') == 143
    print(part1('input.txt'))
    assert part2('sample.txt') == 123
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
