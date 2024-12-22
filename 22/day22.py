try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x):
        return x


def get_next_secret_number(secret_number: int) -> int:
    secret_number = ((secret_number * 64) ^ secret_number) & 0xFFFFFF
    secret_number = ((secret_number // 32) ^ secret_number) & 0xFFFFFF
    secret_number = ((secret_number * 2048) ^ secret_number) & 0xFFFFFF
    return secret_number


valid_chain = [
    123,
    15887950,
    16495136,
    527345,
    704524,
    1553684,
    12683156,
    11100544,
    12249484,
    7753432,
    5908254,
]


def parse_file(filename: str) -> list[int]:
    with open(filename) as f:
        return list(map(int, f))


def part1(filename: str) -> int:
    initials = parse_file(filename)
    total = 0
    for number in initials:
        current = number
        for _ in range(2000):
            current = get_next_secret_number(current)
        total += current
    return total


def generate_possible_change_sets() -> list[list[int]]:
    possible_changes = []
    for a in range(-9, 10):
        for b in range(-9, 10):
            if a + b < -9 or a + b > 9:
                continue
            for c in range(-9, 10):
                if a + b + c < -9 or a + b + c > 9:
                    continue
                for d in range(-9, 10):
                    if a + b + c + d < -9 or a + b + c + d > 9:
                        continue
                    possible_changes.append([a, b, c, d])
    return possible_changes


def get_price(value: int) -> int:
    return value % 10

def find_list_in_list(to_search: list[int], fo_find: list[int]) -> int:
    start = 0
    while True:
        try:
            start = to_search.index(fo_find[0], start)
            if to_search[start:start + len(fo_find)] == fo_find:
                return start
            else:
                start += 1
        except ValueError:
            return -1

def part2(filename: str) -> int:
    initials = parse_file(filename)
    monkeys = []
    prices = []
    changes = []
    for monkey in initials:
        current = monkey
        values = [current]
        for _ in range(2000):
            current = get_next_secret_number(current)
            values.append(current)
        monkey_prices = list(map(get_price, values))
        prices.append(monkey_prices)
        changes_monkey = []
        for a, b in zip(monkey_prices, monkey_prices[1:]):
            changes_monkey.append(b - a)
        changes.append(changes_monkey)
        monkeys.append(values)
    possible_changes = generate_possible_change_sets()
    bananas_per_change = []
    for possible_change in tqdm(possible_changes):
        total_bananas = 0
        for idx, monkey in enumerate(changes):
            found_at = find_list_in_list(monkey, possible_change)
            if found_at == -1:
                continue
            price = prices[idx][found_at + len(possible_change)]
            total_bananas += price
        bananas_per_change.append(total_bananas)
    print(max(bananas_per_change))
    return max(bananas_per_change)


def main():
    for value, expected in zip(valid_chain, valid_chain[1:]):
        assert get_next_secret_number(value) == expected, (value, expected, get_next_secret_number(value))

    assert part1("sample.txt") == 37327623
    print('Part One:', part1("input.txt"))

    assert part2("sample2.txt") == 23
    # runtime: ~18 minutes
    print('Part 2:', part2("input.txt"))


if __name__ == '__main__':
    main()
