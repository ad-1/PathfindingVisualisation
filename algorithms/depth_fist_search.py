# Depth First Search

from adj_list import get_adj_list
from state import State


class DFS:

    def __init__(self, nodes, start_node, finish_node, root):
        """ initialize solver """
        self.subscriber = root
        self.nodes = nodes
        self.adjacency_list = get_adj_list(nodes)
        self.visited = []
        self.path = []
        self.finish_node = finish_node
        if self.dfs_recursive(start_node):
            self.backtrack()

    def dispatch(self, node):
        """ dispatch node info """
        self.subscriber.render_node(node)

    def dfs_recursive(self, node):
        """ depth first search algorithm """
        if node == self.finish_node:
            return True
        if not node.visited:
            node.state = State.visited
            self.visited.append(node)
            self.dispatch(node)
            edges = self.adjacency_list[node]
            for edge in edges:
                if self.dfs_recursive(edge):
                    self.path.append(edge)
                    return True
        return False

    def backtrack(self):
        """ backtrack through path to finish node """
        for node in reversed(self.path):
            node.state = State.path
            self.dispatch(node)
