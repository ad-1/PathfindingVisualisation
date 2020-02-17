# Breadth First Search - Shortest Path

from helpers.adj_list import get_adj_list
from helpers.progress_state import progress_state
from state import State


class BFS:

    def __init__(self, nodes, start_node, finish_node, root):
        """ initialise bredth first search solver """
        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.finish_node = finish_node
        self.state_consts = [start_node, finish_node]
        self.adjacency_list = get_adj_list(nodes)
        self.prev = {}
        self.queue = [start_node]
        self.render_delay = 0.001
        self.bfs_recursive(start_node, finish_node)
        self.backtrack(finish_node)

    def bfs(self):
        pass

    def bfs_recursive(self, s, e):
        """ find shortest path to e from s """
        if s == e or s not in self.adjacency_list:
            return
        progress_state(s, self.state_consts, State.visiting, self.render_delay)
        for edge in self.adjacency_list[s]:
            if edge.state == State.visited or edge in self.queue:
                continue
            self.queue.append(edge)
            progress_state(edge, self.state_consts, State.queue, self.render_delay)
            self.prev[edge] = self.queue[0]
        progress_state(s, self.state_consts, State.visited, self.render_delay)
        self.queue.pop(0)
        if not self.queue:
            return
        self.bfs_recursive(self.queue[0], e)

    def backtrack(self, node):
        """ build shortest path """
        if node == self.start_node or node not in self.prev:
            return
        prev_node = self.prev[node]
        progress_state(prev_node, self.state_consts, State.path, self.render_delay)
        self.backtrack(prev_node)
