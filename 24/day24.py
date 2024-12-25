import re
from dataclasses import dataclass

import z4

re_gate = re.compile(r'(\w{3}) (XOR|OR|AND) (\w{3}) -> (\w{3})')


@dataclass
class InitialState:
    wires: list[tuple[str, int]]
    gates: list[tuple[str, str, str, str]]


def parse_input(filename: str) -> InitialState:
    wires: list[tuple[str, int]] = []
    gates: list[tuple[str, str, str, str]] = []
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            wire, value = line.strip().split(': ')
            wires.append((wire, int(value)))
        for line in f:
            wire1, gate, wire2, wire_out = re_gate.match(line.strip()).groups()
            gates.append((wire1, gate, wire2, wire_out))
    return InitialState(wires, gates)


def part1(filename: str) -> int:
    state = parse_input(filename)
    wires: dict[str, z4.Bool] = {}
    solver = z4.Solver()
    for name, value in state.wires:
        b = z4.Bool(name)
        wires[name] = b
        solver.add(b == bool(value))

    for wire1, gate, wire2, wireout in state.gates:
        if wire1 not in wires:
            b1 = z4.Bool(wire1)
            wires[wire1] = b1
        else:
            b1 = wires[wire1]
        if wire2 not in wires:
            b2 = z4.Bool(wire2)
            wires[wire2] = b2
        else:
            b2 = wires[wire2]
        if wireout not in wires:
            b3 = z4.Bool(wireout)
            wires[wireout] = b3
        else:
            b3 = wires[wireout]
            # raise ValueError(f'{wireout} is already defined')
        if gate == 'XOR':
            solver.add(b3 == z4.Xor(b1, b2))
        elif gate == 'OR':
            solver.add(b3 == z4.Or(b1, b2))
        elif gate == 'AND':
            solver.add(b3 == z4.And(b1, b2))
        else:
            raise ValueError(f'Unknown gate: {gate}')
    assert solver.check() == z4.sat
    model = solver.model()
    parts = {}
    for name, z4v in wires.items():
        if name.startswith('z'):
            parts[name] = bool(model[z4v])
    out = 0
    for key in sorted(parts.keys())[::-1]:
        out <<= 1
        out |= parts[key]
    return out


def main():
    assert part1('sample.txt') == 4
    assert part1('sample2.txt') == 2024
    print('Part One:', part1('input.txt'))


if __name__ == '__main__':
    main()
