from dataclasses import dataclass

from PIL.Image import composite


@dataclass
class Computer:
    name: str

    def __gt__(self, other):
        return self.name > other.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class Connection:
    computers: list[Computer]


@dataclass
class Network:
    computers: list[Computer]
    connections: list[Connection]

    def get_connected_to(self, computer: Computer) -> list[Computer]:
        connected_to = []
        for connection in self.connections:
            if computer in connection.computers:
                for connected_computer in connection.computers:
                    if connected_computer != computer:
                        connected_to.append(connected_computer)
        return connected_to


def parse_input(filename: str) -> list[tuple[str, str]]:
    output = []
    with open(filename) as f:
        for line in f:
            a, b = line.strip().split('-')
            output.append((a, b))
    return output


def build_map(connections: list[tuple[str, str]]):
    known_computers = []
    known_connections = []
    for a, b in connections:
        ca = Computer(a)
        cb = Computer(b)
        if ca not in known_computers:
            known_computers.append(ca)
        if cb not in known_computers:
            known_computers.append(cb)
        if a < b:
            known_connections.append(Connection([
                ca, cb
            ]))
        else:
            known_connections.append(Connection([
                cb, ca,
            ]))
    return Network(known_computers, known_connections)


def find_interconnect_trio_of(network: Network, computer: Computer) -> set[tuple[Computer, Computer, Computer]]:
    connected_to = network.get_connected_to(computer)
    potential = []
    for connected in connected_to:
        filtered = [second_connected for second_connected in network.get_connected_to(connected) if
                    second_connected in connected_to]
        if len(filtered) == 0:
            continue
        potential.append((connected, filtered))
    trios: set[tuple[Computer, Computer, Computer]] = set()
    for connected_computer, connections in potential:
        for second_connected in connections:
            trios.add(tuple(sorted([second_connected, connected_computer, computer])))
    return trios


def find_interconnect_of(network: Network, computer: Computer) -> set[tuple[Computer, ...]]:
    connected_to = network.get_connected_to(computer)
    potential = set()
    for connected in connected_to:
        filtered = [second_connected for second_connected in network.get_connected_to(connected) if
                    second_connected in connected_to]
        if len(filtered) == 0:
            continue
        potential.add(tuple(sorted([connected, computer, *filtered])))
    return potential



def part1(filename: str) -> int:
    network = build_map(parse_input(filename))
    trios: set[tuple[Computer, Computer, Computer]] = set()
    for computer in network.computers:
        if not computer.name.startswith('t'):
            continue
        trios.update(find_interconnect_trio_of(network, computer))
    print(len(trios))

    return len(trios)

def part2(filename: str) -> str:
    network = build_map(parse_input(filename))
    interconnects: set[tuple[*Computer]] = set()
    for computer in network.computers:
        # if not computer.name.startswith('t'):
        #     continue
        interconnects.update(find_interconnect_of(network, computer))
    valid_interconnects = []
    for interconnect in interconnects:
        for computer in interconnect:
            if len(network.get_connected_to(computer)) == len(interconnect) - 1:
                break
        else:
            valid_interconnects.append(interconnect)

    longest_valid_interconnect = max(valid_interconnects, key=len)
    return ','.join(sorted(map(lambda c: c.name, longest_valid_interconnect)))


def main():
    assert part1('sample.txt') == 7
    print('Part One:', part1('input.txt'))
    # assert part2('sample.txt') == 'co,de,ka,ta'
    # print('Part Two:', part2('input.txt'))


if __name__ == '__main__':
    main()
