# Depth First Search

from helpers.adj_list import get_adj_list
from helpers.progress_state import progress_state
from state import State


class DFS:

    def __init__(self, nodes, start_node, finish_node, root):
        """ initialize solver """
        self.subscriber = root
        self.nodes = nodes
        self.adjacency_list = get_adj_list(nodes)
        self.path = []
        self.start_node = start_node
        self.finish_node = finish_node
        self.state_consts = [start_node, finish_node]
        self.render_delay = 0.01
        if self.dfs_recursive(start_node):
            self.backtrack()

    def dfs_recursive(self, node):
        """ depth first search algorithm """
        if node == self.finish_node or node not in self.adjacency_list:
            return True
        if not node.state == State.visited:
            progress_state(node, self.state_consts, State.visited, self.render_delay)
            edges = self.adjacency_list[node]
            for edge in edges:
                if self.dfs_recursive(edge):
                    self.path.append(edge)
                    return True
        return False

    def backtrack(self):
        """ backtrack through path to finish node """
        for node in reversed(self.path):
            progress_state(node, self.state_consts, State.path, self.render_delay)
