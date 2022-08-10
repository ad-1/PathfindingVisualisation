# Depth First Search

from get_adjacent_nodes import get_adj_list
from progress_state import progress_state
from state import State


class DFS:

    def __init__(self, nodes, recursive, start_node, finish_node, root, animate=False):
        """ initialise dfs solver """
        self.subscriber = root
        self.nodes = nodes
        self.adjacency_list = get_adj_list(nodes)
        self.path = []
        self.stack = [start_node]
        self.start_node = start_node
        self.finish_node = finish_node
        self.state_consts = [start_node, finish_node]
        if animate:
            self.render_delay = 0.01
        else:
            self.render_delay = 0
        self.recursive = recursive
        if recursive:
            if self.dfs_recursive(start_node):
                self.backtrack()
        else:
            if self.dfs(start_node):
                self.backtrack()

    def dfs(self, node):
        """ depth first search iterative solution """
        stack = [node]
        while node != self.finish_node:
            node = stack[-1]
            pop_from_stack = True
            progress_state(node, self.state_consts, State.VISITING, self.render_delay)
            self.path.append(node)
            for edge in self.adjacency_list[node]:
                if edge.state == State.VISITED or edge.state == State.VISITING or edge.state == State.START:
                    continue
                stack.append(edge)
                pop_from_stack = False
                break
            if pop_from_stack:
                progress_state(stack[-1], self.state_consts, State.VISITED, self.render_delay)
                stack.pop(-1)
            if not stack:
                return False
        self.path = [node for node in self.path if node.state != State.VISITED]
        return True

    def dfs_recursive(self, node):
        """ depth first search recursive algorithm """
        if node == self.finish_node:
            return True
        if node not in self.adjacency_list:
            return False
        progress_state(node, self.state_consts, State.VISITING, self.render_delay)
        edges = self.adjacency_list[node]
        for edge in edges:
            if edge.state == State.VISITED or edge.state == State.VISITING:
                continue
            if self.dfs_recursive(edge):
                self.path.append(edge)
                return True
            progress_state(node, self.state_consts, State.VISITED, self.render_delay)
        return False

    def backtrack(self):
        """ backtrack through path to finish node """
        if self.recursive:
            for node in reversed(self.path):
                progress_state(node, self.state_consts, State.PATH, self.render_delay)
        else:
            for node in self.path:
                progress_state(node, self.state_consts, State.PATH, self.render_delay)
