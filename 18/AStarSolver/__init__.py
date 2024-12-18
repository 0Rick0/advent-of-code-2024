import typing
from dataclasses import dataclass
from functools import cached_property
from math import hypot


@dataclass
class Node:
    x: int
    y: int

    def weight(self, other: "Node") -> float:
        return hypot(other.x - self.x, other.y - self.y)

    @property
    def north(self):
        return Node(self.x, self.y - 1)

    @property
    def east(self):
        return Node(self.x + 1, self.y)

    @property
    def south(self):
        return Node(self.x, self.y + 1)

    @property
    def west(self):
        return Node(self.x - 1, self.y)

    def __hash__(self):
        return hash((self.x, self.y))


class Maze:
    endnode: Node
    startnode: Node
    maze: list[list[str]]

    def __init__(self, maze: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> None:
        self.maze = maze
        self.startnode = Node(*start)
        self.endnode = Node(*end)

    def node_valid(self, node: Node) -> bool:
        if node.x > self.endnode.x or node.y > self.endnode.y:
            return False
        if node.x < self.startnode.x or node.y < self.startnode.y:
            return False
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

    @cached_property
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
    def __init__(self):
        self.path = []
        self.known = dict()
        self.endnode = None

    def check_node(self, basenode: AStarNode, node: Node):
        if not node:
            return
        newlist = [node, *basenode.nodes]
        newstar = AStarNode(newlist, self.endnode)

        if node in self.known:
            # found shorter route
            # For part 2, <= is required, but for the full map this creates way to much work
            # if newstar.total_weight <= self.known[node].total_weight:
            if newstar.total_weight < self.known[node].total_weight:
                # print('found shorter route')
                self.path.append(newstar)
                self.known[node] = newstar
        else:
            self.path.append(newstar)
            self.known[node] = newstar

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

            for forward_node in [
                first_curnode.north,
                first_curnode.east,
                first_curnode.south,
                first_curnode.west,
            ]:
                if maze.node_valid(forward_node):
                    self.check_node(curnode, forward_node)
