# Dijakstra's Algorithm - Shortest Path

from math import inf
from state import State
from progress_state import progress_state


class Dijkstra:

    def __init__(self, nodes, a_star, start_node, finish_node, root, animate=False):
        """ initialize solver """
        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.finish_node = finish_node
        self.state_consts = [start_node, finish_node]
        self.prev_node_key = 'prev_node'
        self.distance_key = 'distance'
        self.heuristic_key = 'manhattan'
        self.a_star = a_star
        self.priority_queue = {start_node: 0}
        self.adjacency_list, self.path_info = self.init_dijkstra()
        self.path_info[start_node][self.prev_node_key] = None
        self.path_info[start_node][self.distance_key] = 0
        self.path_info[start_node][self.heuristic_key] = self.manhattan_distance(start_node)
        self.shortest_path = []
        if animate:
            self.render_delay = 0.01
        else:
            self.render_delay = 0
        if self.dijkstra(start_node):
            self.backtrack()
            self.visualise_path()

    def dispatch(self, node):
        """ dispatch node info """
        self.subscriber.render_node(node)

    def init_dijkstra(self):
        """ create graph adjacency list and distance array """
        adjacency_list = {}
        path_info = {}
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                path_info[node] = {self.prev_node_key: None, self.distance_key: inf, self.heuristic_key: self.manhattan_distance(node)}
                for c in node.connections:
                    if 0 <= c[0] < len(self.nodes) and 0 <= c[1] < len(self.nodes[0]):
                        edge = self.nodes[c[0]][c[1]]
                        if edge.state == State.WALL:
                            continue
                        adjacency_list.setdefault(node, {edge}).add(edge)
        return adjacency_list, path_info

    def pythagoras(self, node):
        """ euclidean distance - A* heuristic """
        a = node.col - self.finish_node.col
        b = node.row - self.finish_node.row
        c = ((a ** 2) + (b ** 2)) ** (1/2) * 1000
        return c

    def manhattan_distance(self, node):
        """ manhattan distance - A* heuristic """
        return abs(self.finish_node.col - node.col) + abs(self.finish_node.row - node.row)

    def dijkstra(self, node):
        """ dijkstra and a* algorithm implementation """
        while self.finish_node != self.get_next_priority():
            if node is None or node not in self.adjacency_list:
                return False
            progress_state(node, self.state_consts, State.VISITING, self.render_delay)
            self.priority_queue.pop(node, None)
            edges = self.adjacency_list[node]
            self.relaxation(node, edges)
            progress_state(node, self.state_consts, State.VISITED, self.render_delay)
            node = self.get_next_priority()
        return True

    def relaxation(self, node, edges):
        """ update distance array """
        for edge in edges:
            if edge.state == State.VISITED:
                continue
            if self.a_star:
                new_dist = edge.weight + self.path_info[edge][self.heuristic_key]
            else:
                new_dist = edge.weight + self.path_info[node][self.distance_key]
            if new_dist < self.path_info[edge][self.distance_key]:
                self.path_info[edge][self.prev_node_key] = node
                if self.a_star:
                    self.path_info[edge][self.heuristic_key] = new_dist
                else:
                    self.path_info[edge][self.distance_key] = new_dist
                self.priority_queue[edge] = new_dist

    def get_next_priority(self):
        """ get next priority node based on minimum distance in queue """
        if not self.priority_queue:
            return
        return min(self.priority_queue, key=self.priority_queue.get)

    def backtrack(self):
        """ backtrack through path info to find shortest path to finish node """
        node = self.finish_node
        while node != self.start_node:
            prev_node = self.path_info[node][self.prev_node_key]
            self.shortest_path.append(prev_node)
            node = prev_node

    def visualise_path(self):
        for node in reversed(self.shortest_path):
            progress_state(node, self.state_consts, State.PATH, self.render_delay)
