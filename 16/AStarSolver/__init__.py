import copy
import typing
from dataclasses import dataclass
from enum import Enum
from math import hypot


class Cardinal(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def next(self) -> "Cardinal":
        return type(self)((self.value + 1) % 4)

    def previous(self) -> "Cardinal":
        new_value = self.value - 1
        if new_value < 0:
            return self.WEST
        return type(self)((self.value - 1))


@dataclass
class Node:
    x: int
    y: int
    direction: Cardinal | None

    def weight(self, other: "Node") -> float:
        if other.direction is None and self.x == other.x and self.y == other.y:
            return 0
        elif self.direction == other.direction:
            dist = abs(self.x - other.x) + abs(self.y - other.y)
            if dist != 1:
                raise ValueError(f'illegal move xy = {self.x}, {self.y} {dist}')
            return 1
        elif self.x == other.x and self.y == other.y:
            return 1000
        else:
            raise ValueError('Illegal move')

    @property
    def forward(self):
        match self.direction:
            case Cardinal.NORTH:
                return Node(self.x, self.y - 1, self.direction)
            case Cardinal.EAST:
                return Node(self.x + 1, self.y, self.direction)
            case Cardinal.SOUTH:
                return Node(self.x, self.y + 1, self.direction)
            case Cardinal.WEST:
                return Node(self.x - 1, self.y, self.direction)

    @property
    def rotate_clockwise(self):
        return Node(self.x, self.y, self.direction.next())

    @property
    def rotate_counterclockwise(self):
        return Node(self.x, self.y, self.direction.previous())

    def __hash__(self):
        return hash((self.x, self.y, self.direction))



class Maze:
    endnode: Node
    startnode: Node
    maze: list[list[str]]

    def __init__(self, maze: list[list[str]]) -> None:
        self.maze = maze
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 'S':
                    self.startnode = Node(x, y, Cardinal.EAST)
                elif cell == 'E':
                    self.endnode = Node(x, y, None)



    def node_valid(self, node: Node) -> bool:
        return self.maze[node.y][node.x] != '#'


def _dist_nodex(n1: Node, n2: Node):
    return hypot(n1.x - n2.x, n1.y - n2.y)


class AStarNode:
    dist = 0
    weight = 0
    nodes = []

    def __init__(self, nodes: typing.List[Node], endnode: Node):
        self.nodes = nodes
        for i in range(len(nodes) - 2):
            self.weight += nodes[i].weight(nodes[i + 1])
        self.dist = _dist_nodex(self.first_node, endnode)

    @property
    def total_weight(self):
        return self.weight + self.dist * 2

    @property
    def first_node(self):
        return self.nodes[0]

    def __lt__(self, other):
        if not isinstance(other, AStarNode):
            raise ValueError("Can't compare to %r" % other)
        return self.total_weight > other.total_weight  # hacked to get the correct order


class AStarSolver:
    path = []
    known = []
    endnode = None

    def check_node(self, basenode: AStarNode, node: Node):
        if not node:
            return
        newlist = copy.copy(basenode.nodes)
        newlist.insert(0, node)
        newstar = AStarNode(newlist, self.endnode)

        if node in self.known.keys():
            # found shorter route
            if newstar.total_weight < self.known[node].total_weight:
                # print('found shorter route')
                self.path.append(newstar)
                for nn in newstar.nodes:
                    self.known[nn] = newstar
        else:
            self.path.append(newstar)
            for nn in newlist:
                self.known[nn] = newstar

    def solve_maze(self, maze: Maze) -> typing.List[Node]:
        self.endnode = maze.endnode
        self.path = [AStarNode([maze.startnode], maze.endnode)]
        self.known = {maze.startnode: self.path[0]}

        while True:
            self.path.sort()
            curnode = self.path.pop()
            if curnode.dist == 0:
                return curnode.nodes
            first_curnode = curnode.first_node

            forward_node = first_curnode.forward
            if maze.node_valid(forward_node):
                self.check_node(curnode, forward_node)
            self.check_node(curnode, first_curnode.rotate_clockwise)
            self.check_node(curnode, first_curnode.rotate_counterclockwise)
