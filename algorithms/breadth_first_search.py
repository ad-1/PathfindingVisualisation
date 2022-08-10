# Breadth First Search - Shortest Path

from get_adjacent_nodes import get_adj_list
from progress_state import progress_state
from state import State


class BFS:

    def __init__(self, nodes, recursive, start_node, finish_node, root, animate=False):
        """ initialise bredth first search solver """
        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.finish_node = finish_node
        self.state_consts = [start_node, finish_node]
        self.adjacency_list = get_adj_list(nodes)
        self.prev = {}
        self.path = []
        self.queue = [start_node]
        if animate:
            self.render_delay = 0.01
        else:
            self.render_delay = 0
        if recursive:
            self.bfs_recursive(start_node)
        else:
            self.bfs()
        self.backtrack(finish_node)
        self.visualise_path()

    def bfs(self):
        """ breadth first search iterative """
        node = self.queue[-1]
        while node != self.finish_node and node in self.adjacency_list:
            progress_state(node, self.state_consts, State.VISITING, self.render_delay)
            for edge in self.adjacency_list[node]:
                if edge.state == State.VISITED or edge.state == State.QUEUE:
                    continue
                self.prev[edge] = node
                self.queue.append(edge)
                progress_state(edge, self.state_consts, State.QUEUE, self.render_delay)
            self.queue.pop(0)
            progress_state(node, self.state_consts, State.VISITED, self.render_delay)
            if not self.queue:
                break
            node = self.queue[0]

    def bfs_recursive(self, node):
        """ breadth first search recursive - find shortest path """
        if node == self.finish_node or node not in self.adjacency_list:
            return
        progress_state(node, self.state_consts, State.VISITING, self.render_delay)
        for edge in self.adjacency_list[node]:
            if edge.state == State.VISITED or edge in self.queue:
                continue
            self.queue.append(edge)
            progress_state(edge, self.state_consts, State.QUEUE, self.render_delay)
            self.prev[edge] = self.queue[0]
        progress_state(node, self.state_consts, State.VISITED, self.render_delay)
        self.queue.pop(0)
        if not self.queue:
            return
        self.bfs_recursive(self.queue[0])

    def backtrack(self, node):
        """ build shortest path """
        if node == self.start_node or node not in self.prev:
            return
        prev_node = self.prev[node]
        self.path.append(prev_node)
        self.backtrack(prev_node)

    def visualise_path(self):
        for node in reversed(self.path):
            progress_state(node, self.state_consts, State.PATH, self.render_delay)
