# Dijakstra's Algorithm - Shortest Path

from math import inf


class Dijkstra:

    def __init__(self, nodes, start_node, fin_node, root):
        """ initialize solver """

        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.fin_node = fin_node
        self.prev_node_key = 'prev_node'
        self.distance_key = 'distance'
        self.adjacency_list, self.path_info = self.create_data_structs()
        self.priority_queue = {start_node: 0}
        self.path_info[start_node][self.prev_node_key] = None
        self.path_info[start_node][self.distance_key] = 0
        self.shortest_path = []

        if self.dijkstra(start_node):
            self.backtrack()

    def dispatch(self, node):
        """ dispatch node info """

        self.subscriber.update_root(node)

    def create_data_structs(self):
        """ create graph adjacency list and distance array """

        adjacency_list = {}
        path_info = {}
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                path_info[node] = {self.prev_node_key: None, self.distance_key: inf}
                for c in node.connections:
                    if 0 <= c[0] < len(self.nodes) and 0 <= c[1] < len(self.nodes[0]):
                        edge = self.nodes[c[0]][c[1]]
                        if edge.is_wall:
                            continue
                        adjacency_list.setdefault(node, {edge}).add(edge)
        return adjacency_list, path_info

    def dijkstra(self, current_node):
        """ dijkstra algorithm implementation """

        while current_node != self.fin_node:  # while any(x == inf for x in self.dist):
            if current_node is None or current_node not in self.adjacency_list:
                return False

            current_node.visiting = True
            self.dispatch(current_node)

            self.remove_priority(current_node)
            edges = self.adjacency_list[current_node]
            self.relaxation(current_node, edges)

            current_node.visited, current_node.visiting = True, False
            self.dispatch(current_node)

            current_node = self.get_next_priority()

        return True

    def relaxation(self, visiting, edges):
        """ update distance array """

        for c in edges:
            if c.visited:
                continue
            new_dist = self.path_info[visiting][self.distance_key] + c.cost
            if new_dist < self.path_info[c][self.distance_key]:
                self.path_info[c][self.prev_node_key] = visiting
                self.path_info[c][self.distance_key] = new_dist
                self.priority_queue[c] = new_dist

    def remove_priority(self, visited):
        """ remove visited node from queue """

        del self.priority_queue[visited]

    def get_next_priority(self):
        """ get next priority node based on minimum distance in queue """

        if not self.priority_queue:
            return

        return min(self.priority_queue, key=self.priority_queue.get)

    def backtrack(self):
        """ backtrack through path info to find shortest path to finish node """
        node = self.fin_node

        while node != self.start_node:
            node.in_path = True
            prev_node = self.path_info[node][self.prev_node_key]
            self.shortest_path.append(prev_node)
            node = prev_node

        for node in reversed(self.shortest_path):
            self.dispatch(node)

