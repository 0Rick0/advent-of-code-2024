import math
import re
from dataclasses import dataclass

RE_BUTTON = re.compile(r"Button [AB]: X([+-]\d+), Y([+-]\d+)")
RE_PRIZE = re.compile(r"Prize: X=(\d+), Y=(\d+)")


@dataclass
class Machine:
    button_a_delta: tuple[int, int]
    button_b_delta: tuple[int, int]
    prize: tuple[int, int]


def parse_input(filename) -> list[Machine]:
    machines = []
    with open(filename) as f:
        while True:
            button_a = f.readline().strip()
            if not button_a:
                break
            button_b = f.readline().strip()
            prize = f.readline().strip()
            _ = f.readline().strip()
            button_a_coords = tuple(map(int, RE_BUTTON.match(button_a).groups()))
            button_b_coords = tuple(map(int, RE_BUTTON.match(button_b).groups()))
            prize_coords = tuple(map(int, RE_PRIZE.match(prize).groups()))
            assert len(button_a_coords) == 2
            assert len(button_b_coords) == 2
            assert len(prize_coords) == 2

            machines.append(Machine(button_a_coords, button_b_coords, prize_coords))

    return machines


def solution_prize(button_a: int, button_b: int) -> int:
    return button_a * 3 + button_b


def part1(filename) -> int:
    machines = parse_input(filename)

    machine_solutions = []
    # let's start with an easy solution
    for machine in machines:
        solutions = []
        for button_a in range(100):
            for button_b in range(100):
                delta_a_x = machine.button_a_delta[0] * button_a
                delta_a_y = machine.button_a_delta[1] * button_a
                delta_b_x = machine.button_b_delta[0] * button_b
                delta_b_y = machine.button_b_delta[1] * button_b
                x = delta_a_x + delta_b_x
                y = delta_a_y + delta_b_y
                if (x, y) == machine.prize:
                    solutions.append([button_a, button_b])
        if len(solutions) > 0:
            sorted_solutions = sorted(solutions, key=lambda solution: sum(solution))
            machine_solutions.append([machine, sorted_solutions[0]])
    return sum(solution_prize(*solution[1]) for solution in machine_solutions)


def distance_to_prize(prize_x, prize_y, button_a_x, button_a_y, button_b_x, button_b_y, no_a, no_b) -> float:
    # f(x, y) = sqrt((e - ax - cy)^2 + (f - bx - cy)^2)
    return math.sqrt(
        (prize_x - button_a_x * no_a - button_b_x * no_b) ** 2 +
        (prize_y - button_a_y * no_a - button_b_y * no_b) ** 2
    )


def part2(filename: str) -> int:
    machines = parse_input(filename)
    # for machine in machines:
    #     old_prize_x, old_prize_y = machine.prize
    #     machine.prize = (old_prize_x + 10000000000000, old_prize_y + 10000000000000)

    for machine in machines:
        no_a = 0
        no_b = 0
        lowest_delta = float("inf")
        while True:
            new_delta = distance_to_prize(*machine.prize, *machine.button_a_delta, *machine.button_b_delta, no_a, no_b)
            if new_delta < lowest_delta:
                lowest_delta = new_delta
                adding = int(new_delta / 10000)
                if distance_to_prize(*machine.prize, *machine.button_a_delta, *machine.button_b_delta, no_a + adding, no_b) > \
                    distance_to_prize(*machine.prize, *machine.button_a_delta, *machine.button_b_delta, no_a, no_b + adding):
                    no_a += adding
                else:
                    no_b += adding
            else:
                break
        print(f"current lowest {lowest_delta} at {no_a} {no_b}")




def main():
    assert part1('sample.txt') == 480, part1('sample.txt')
    print(part1('input.txt'))
    # I've made an attempt for part 2, but I haven't found a good solution yet
    # print(part2('sample.txt'))
    # print(part2('input.txt'))


if __name__ == '__main__':
    main()
