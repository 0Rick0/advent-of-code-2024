import enum
from dataclasses import dataclass


class BlockType(enum.Enum):
    USED = 0
    FREE = 1


@dataclass
class Block:
    length: int
    type: BlockType
    id: int
    id_offset: int
    offset: int
    moved: bool = False


def parse_input(filename: str) -> list[Block]:
    blocks = []
    current = BlockType.USED
    offset = 0
    with open(filename) as f:
        for i, c in enumerate(f.read().strip()):
            block_size = int(c)
            blocks.append(Block(block_size, BlockType(i % 2), i // 2, 0, offset))
            offset += block_size
    return [block for block in blocks if block.length > 0]


def compact(blocks: list[Block]) -> list[Block]:
    _blocks: list[Block] = [*blocks]
    idx = 0
    while idx < len(_blocks):
        block: Block = _blocks[idx]
        if block.type == BlockType.USED:
            pass
        else:
            del _blocks[idx]
            last_block: Block = _blocks.pop()
            if last_block.type == BlockType.FREE:
                last_block = _blocks.pop()

            if last_block.length <= block.length:
                _blocks.insert(idx,
                               Block(last_block.length,
                                     last_block.type,
                                     last_block.id,
                                     last_block.id_offset,
                                     block.offset))
                if last_block.length < block.length:
                    _blocks.insert(idx + 1, Block(
                        block.length - last_block.length,
                        BlockType.FREE,
                        0,
                        0,
                        block.offset + last_block.length,
                    ))
            else:
                _blocks.insert(idx, Block(
                    block.length,
                    last_block.type,
                    last_block.id,
                    last_block.id_offset + block.length,
                    block.offset,
                ))
                _blocks.append(Block(
                    last_block.length - block.length,
                    last_block.type,
                    last_block.id,
                    last_block.id_offset,
                    last_block.offset,
                ))

        idx += 1
    return _blocks


def compact_v2(blocks: list[Block]) -> list[Block]:
    _blocks = [*blocks]
    idx = len(_blocks) - 1
    while idx > 0:
        block: Block = _blocks[idx]
        if block.type == BlockType.USED and block.moved is False:
            del _blocks[idx]
            for idx2 in range(0, min(idx, len(_blocks))):
                if _blocks[idx2].type == BlockType.FREE \
                        and _blocks[idx2].length >= block.length:
                    old_free = _blocks[idx2]
                    _blocks[idx2] = Block(
                        block.length,
                        block.type,
                        block.id,
                        block.id_offset,
                        old_free.offset,
                        True,
                    )
                    if old_free.length > block.length:
                        _blocks.insert(idx2 + 1, Block(
                            old_free.length - block.length,
                            BlockType.FREE,
                            0,
                            0,
                            old_free.offset + block.length,
                        ))
                        if idx2 < idx:
                            idx += 1

                    _blocks.insert(idx, Block(
                        block.length,
                        BlockType.FREE,
                        0,
                        0,
                        block.offset,
                    ))
                    break
            else:
                # Re-add if it wasn't moved
                _blocks.insert(idx, block)
        idx -= 1
    return _blocks


def print_blocks(blocks: list[Block]) -> str:
    out = []
    for block in blocks:
        if block.type == BlockType.USED:
            out.append(str(block.id) * block.length)
        else:
            out.append('.' * block.length)
    return ''.join(out)


def assert_offset(blocks: list[Block]) -> bool:
    offset = 0
    for idx, block in enumerate(blocks):
        assert block.offset == offset, f'Offset incorrect at {offset} blocks[{idx}]'
        offset += block.length


def part1(filename: str) -> int:
    blocks = parse_input(filename)
    compacted = compact(blocks)
    checksum = sum(
        sum(block.id * o for o in range(block.offset, block.offset + block.length))
        for block in compacted)
    return checksum


def part2(filename: str) -> int:
    blocks = parse_input(filename)
    compacted = compact_v2(blocks)
    assert_offset(compacted)
    checksum = sum(
        sum(block.id * o for o in range(block.offset, block.offset + block.length))
        for block in compacted if block.type == BlockType.USED)
    return checksum


def main():
    assert part1('sample.txt') == 1928, part1('sample.txt')
    print(part1('input.txt'))
    assert part2('sample.txt') == 2858, part2('sample.txt')
    print(part2('input.txt'))


if __name__ == '__main__':
    main()
