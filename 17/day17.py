from timeit import timeit
from transpiled import transpiled


class TelePc:
    reg_a: int
    reg_b: int
    reg_c: int
    ip: int

    data: list[int]

    opcodes: list

    stdout: list[int]

    def __init__(self):
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0
        self.ip = 0
        self.data = []
        self.opcodes = [
            self.instruction_adv,
            self.instruction_bxl,
            self.instruction_bst,
            self.instruction_jnz,
            self.instruction_bxc,
            self.instruction_out,
            self.instruction_bdv,
            self.instruction_cdv,
        ]
        self.stdout = []

    def opcode_name_at(self, ip: int):
        opcode = self.opcodes[self.data[ip]]
        return opcode.__name__.split('_')[1]

    def operand_value(self, ip: int):
        operand = self.data[ip + 1]
        match self.opcode_name_at(ip):
            case 'adv' | 'bst' | 'out' | 'bdv' | 'cdv':
                if 0 <= operand <= 3:
                    return f'CL{operand}'
                elif operand == 4:
                    return f'CRA'
                elif operand == 5:
                    return f'CRB'
                elif operand == 6:
                    return f'CRC'
                else:
                    return f'ERR'
            case 'bxl' | 'jnz' | 'bxc':
                return f'L{operand}'

    def __repr__(self):
        return f'<TelePc: IP: {self.ip}[{self.opcode_name_at(self.ip)}][{self.operand_value(self.ip)}] A: {self.reg_a} B: {self.reg_b} C: {self.reg_c}>'

    def load(self, data: list[int], reg_a: int, reg_b: int, reg_c: int) -> None:
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.ip = 0
        self.data = data

    def combo_operant_to_value(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                raise ValueError('Bad combo operant 7')
            case _:
                raise ValueError('Operant above 7')

    def tick(self):
        if self.ip >= len(self.data):
            raise ValueError('CPU Halt')

        opcode, operand = self.data[self.ip:self.ip + 2]
        self.opcodes[opcode](operand)

    def instruction_adv(self, operand: int):
        operand = self.combo_operant_to_value(operand)
        denominator = 2 ** operand
        numerator = self.reg_a
        self.reg_a = numerator // denominator
        self.ip += 2

    def instruction_bxl(self, operand: int):
        self.reg_b = self.reg_b ^ operand
        self.ip += 2

    def instruction_bst(self, operand: int):
        operand = self.combo_operant_to_value(operand)
        self.reg_b = operand % 8
        self.ip += 2

    def instruction_jnz(self, operand: int):
        if self.reg_a != 0:
            self.ip = operand
        else:
            self.ip += 2

    def instruction_bxc(self, operand: int):
        self.reg_b = self.reg_b ^ self.reg_c
        self.ip += 2

    def instruction_out(self, operand: int):
        operand = self.combo_operant_to_value(operand)
        self.stdout.append(operand % 8)
        self.ip += 2

    def instruction_bdv(self, operand: int):
        operand = self.combo_operant_to_value(operand)
        denominator = 2 ** operand
        numerator = self.reg_a
        self.reg_b = numerator // denominator
        self.ip += 2

    def instruction_cdv(self, operand: int):
        operand = self.combo_operant_to_value(operand)
        denominator = 2 ** operand
        numerator = self.reg_a
        self.reg_c = numerator // denominator
        self.ip += 2

    def reset(self, reg_a: int, reg_b: int, reg_c: int) -> None:
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.ip = 0
        self.stdout = []

    def dump(self):
        for i in range(0, len(self.data), 2):
            print(self.opcode_name_at(i) + ' ' + self.operand_value(i))

    def run_until_halt(self):
        try:
            while True:
                self.tick()
        except ValueError:
            pass


def test(reg_a, reg_b, reg_c, data: list[int]) -> TelePc:
    tpc = TelePc()
    tpc.load(data, reg_a, reg_b, reg_c)
    tpc.run_until_halt()
    return tpc


def tests():
    assert test(0, 0, 9, [2, 6]).reg_b == 1
    assert test(10, 0, 0, [5, 0, 5, 1, 5, 4]).stdout == [0, 1, 2]
    test_3 = test(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    assert test_3.stdout == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert test_3.reg_a == 0
    assert test(0, 29, 0, [1, 7]).reg_b == 26
    assert test(0, 2024, 43690, [4, 0]).reg_b == 44354
    assert test(10, 0, 0, [6, 1]).reg_b == 5
    assert test(10, 0, 0, [7, 1]).reg_c == 5

    pc_self = load_pc('sample2.txt')
    pc_self.reset(117440, 0, 0)
    pc_self.run_until_halt()
    assert pc_self.data == pc_self.stdout


def load_pc(filename):
    reg_a: int = -1
    reg_b: int = -1
    reg_c: int = -1
    program: list[int] = []
    with open(filename) as f:
        for line in f:
            if line.startswith('Register A:'):
                reg_a = int(line.split(':')[1].strip())
            elif line.startswith('Register B:'):
                reg_b = int(line.split(':')[1].strip())
            elif line.startswith('Register C:'):
                reg_c = int(line.split(':')[1].strip())
            elif line.startswith('Program:'):
                program.extend(map(int, line.split(':')[1].strip().split(',')))
    assert reg_a >= 0
    assert reg_b >= 0
    assert reg_c >= 0
    assert program != []
    assert all(i < 8 for i in program)
    pc = TelePc()
    pc.load(program, reg_a, reg_b, reg_c)
    return pc


def part1(filename: str) -> str:
    pc = load_pc(filename)
    pc.run_until_halt()
    return ','.join(map(str, pc.stdout))


def part2(filename: str) -> int:
    pc = load_pc(filename)
    pc.dump()
    reg_a = -1
    while pc.stdout != pc.data:
        reg_a += 1
        if reg_a % 100000 == 0:
            print(reg_a)
        pc.reset(reg_a, 0, 0)
        try:
            while True:
                if len(pc.stdout) > len(pc.data):
                    # print('Stdout to long')
                    break
                elif pc.stdout != pc.data[:len(pc.stdout)]:
                    # print(f'Stdout start diverges {pc.stdout} != {pc.data}')
                    break
                pc.tick()
        except ValueError:
            pass
    return reg_a


def part2b() -> int:
    i = 3264000000
    # Transpiled is the program rewritten in python
    while not transpiled(i):
        if i % 1_000_000 == 0:
            print(i)
        i += 1
    return i


def main():
    tests()
    assert part1('sample.txt') == '4,6,3,5,6,3,5,2,1,0'
    time_part1 = timeit(lambda: part1('sample.txt'), number=10)
    estimate_part2 = 117440 * time_part1
    print(estimate_part2)
    print(part1('input.txt'))
    assert part2('sample2.txt') == 117440
    # print(part2('input.txt'))
    print(part2b())


if __name__ == '__main__':
    main()
