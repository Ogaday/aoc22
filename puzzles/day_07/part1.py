from typing import Optional, List, Dict, Set, Tuple


class Node:
    def __init__(self, name: str, value: int = 0):
        self.name = name
        self.value = value
        self.parent: Node = None
        self._children: Dict[str, Node] = {}

    def __repr__(self):
        return f"Node(name={self.name}, value={self.value})"

    @property
    def children(self):
        return self._children

    def add_child(self, other: "Node"):
        other.parent = self
        self._children[other.name] = other

    def total_value(self):
        return self.value + sum(child.total_value() for child in self.children.values())


def build_graph(lines: List[str]) -> Tuple[Node, Set[Node]]:
    dirs = set()

    root = Node(name="/")
    current = root
    dirs.add(root)

    for row in lines:
        # Changedir
        if row.startswith("$ cd"):
            if row.endswith(".."):
                current = current.parent
            elif row.endswith(" /"):
                current = root
            else:
                current = current.children[row.split()[-1]]
        # ls
        elif row.startswith("$ ls"):
            # Deal with ls return values in later conditionals:
            pass
        else:
            value, name = row.split()
            value = 0 if value == "dir" else int(value)
            node = Node(name=name, value=value)
            current.add_child(node)
            if node.value == 0:
                dirs.add(node)
    return root, dirs


# n = Node(name="/")
# n
# n.add_child(Node('a', value=1))
# n.add_child(Node('b', value=2))
# n.children['a'].add_child(Node(name='c', value=3))
# n
# n.total_value()
# c.children['a'].parent
# n.children['a'].parent
# n.children['a'].children['c']
# n.children['a'].children['c'].parent
# n.children['a'].children['c'].parent.parent

if __name__ == "__main__":
    with open("inputs/day_07.txt") as f:
        data = [line.strip() for line in f.readlines()]

    root, dirs = build_graph(data)

    nodes_lt_100000 = [
        node for node in dirs if node.total_value() < 100000 and node.value == 0
    ]
    print(sum([node.total_value() for node in nodes_lt_100000]))
