# Dijakstra's Algorithm - Shortest Path

from math import inf
from state import State


class Dijkstra:

    def __init__(self, nodes, a_star, start_node, finish_node, root):
        """ initialize solver """
        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.finish_node = finish_node
        self.prev_node_key = 'prev_node'
        self.distance_key = 'distance'
        self.heuristic_key = 'manhattan'
        self.a_star = a_star
        if a_star:
            self.priority_queue = {}
        else:
            self.priority_queue = {start_node: 0}
        self.adjacency_list, self.path_info = self.init_dijkstra()
        self.path_info[start_node][self.prev_node_key] = None
        self.path_info[start_node][self.distance_key] = 0
        self.path_info[start_node][self.heuristic_key] = self.manhattan_distance(start_node)
        self.shortest_path = []
        if self.dijkstra(start_node):
            self.backtrack()

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
                        if edge.state == State.wall:
                            continue
                        adjacency_list.setdefault(node, {edge}).add(edge)
        return adjacency_list, path_info

    def pythagoras(self, node):
        """ pythagorean theorem - heuristic """
        a = node.col - self.finish_node.col
        b = node.row - self.finish_node.row
        c = ((a ** 2) + (b ** 2)) ** (1/2) * 1000
        return c

    def manhattan_distance(self, node):
        """ manhattan distance - heuristic """
        return abs(self.finish_node.col - node.col) + abs(self.finish_node.row - node.row)

    def dijkstra(self, node):
        """ dijkstra and s-star algorithm implementation """
        while self.finish_node != self.get_next_priority():  # while none != self.finish_node:
            if node is None or node not in self.adjacency_list:
                return False
            node.state = State.visiting
            self.dispatch(node)
            self.priority_queue.pop(node, None)  # del self.priority_queue[node]
            edges = self.adjacency_list[node]
            self.relaxation(node, edges)
            node.state = State.visited
            self.dispatch(node)
            node = self.get_next_priority()
        return True

    def relaxation(self, node, edges):
        """ update distance array """
        for edge in edges:
            if edge.state == State.visited:
                continue
            if self.a_star:
                new_dist = edge.cost + self.path_info[edge][self.heuristic_key]
            else:
                new_dist = edge.cost + self.path_info[node][self.distance_key]
            if new_dist < self.path_info[edge][self.distance_key]:
                self.path_info[edge][self.prev_node_key] = node
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
            node.state = State.path
            prev_node = self.path_info[node][self.prev_node_key]
            self.shortest_path.append(prev_node)
            node = prev_node
        for node in reversed(self.shortest_path):
            self.dispatch(node)
