from typing import Literal

key_lock = tuple[int, int, int, int, int]


def parse_key_lock(lines: list[str]) -> tuple[Literal['key', 'lock'], key_lock]:
    transposed = list(zip(*lines))
    item_type = 'key' if transposed[0][0] == '.' else 'lock'
    assert len(transposed) == 5 and len(transposed[0]) == 7
    return item_type, tuple(map(lambda a: a.count('#') - 1, transposed))


def parse_input(filename: str) -> tuple[list[key_lock], list[key_lock]]:
    keys: list[key_lock] = []
    locks: list[key_lock] = []
    with open(filename) as f:
        lock_lines = []
        for line in f:
            if line.strip():
                lock_lines.append(line.strip())
            else:
                item_type, value = parse_key_lock(lock_lines)
                if item_type == 'key':
                    keys.append(value)
                elif item_type == 'lock':
                    locks.append(value)
                lock_lines = []
    item_type, value = parse_key_lock(lock_lines)
    if item_type == 'key':
        keys.append(value)
    elif item_type == 'lock':
        locks.append(value)
    return keys, locks


def invert_key(key: key_lock) -> key_lock:
    t1, t2, t3, t4, t5 = key
    return 6 - t1, 6 - t2, 6 - t3, 6 - t4, 6 - t5


def key_fits(lock: key_lock, key: key_lock) -> bool:
    for lock_t, key_t in zip(lock, key):
        if lock_t + key_t >= 6:
            return False
    return True


def part1(filename: str) -> int:
    keys, locks = parse_input(filename)

    pairs = 0
    for lock in locks:
        for key in keys:
            if key_fits(lock, key):
                pairs += 1
    return pairs


def main():
    assert part1('sample.txt') == 3
    print('Part One:', part1('input.txt'))


if __name__ == "__main__":
    main()
