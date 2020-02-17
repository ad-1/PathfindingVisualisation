# Breadth First Search - Shortest Path

from adj_list import get_adj_list
from state import State


class BFS:

    def __init__(self, nodes, start_node, finish_node, root):
        """ initialise bredth first search solver """
        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.finish_node = finish_node
        self.adjacency_list = get_adj_list(nodes)
        self.prev = {start_node: None}
        self.shortest_path = []
        self.queue = [start_node]
        self.bfs_recursive(start_node, finish_node)
        self.backtrack(finish_node)

    def dispatch(self, node):
        """ dispatch node info """
        self.subscriber.render_node(node)

    def bfs(self):
        pass

    def bfs_recursive(self, s, e):
        """ find shortest path to e from s """
        s.state = State.visiting
        self.dispatch(s)
        if s == e:
            return
        for edge in self.adjacency_list[s]:
            if not edge.state == State.visited and edge not in self.queue:
                self.queue.append(edge)
                edge.state = State.queue
                self.dispatch(edge)
                self.prev[edge] = self.queue[0]
        s.state = State.visited
        self.dispatch(s)
        self.queue.pop(0)
        if not self.queue:
            return
        self.bfs_recursive(self.queue[0], e)

    def backtrack(self, node):
        """ build shortest path """
        if node == self.start_node:
            self.visualise_path()
            return
        prev_node = self.prev[node]
        prev_node.state = State.path
        self.shortest_path.append(prev_node)
        self.backtrack(prev_node)

    def visualise_path(self):
        """ dispatch visual updates """
        for node in reversed(self.shortest_path):
            self.dispatch(node)
