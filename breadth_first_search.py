# Dijakstra's Algorithm - Shortest Path

class BFS:

    def __init__(self, nodes, start_node, fin_node, root):
        self.subscriber = root
        self.nodes = nodes
        self.start_node = start_node
        self.adjacency_list = self.get_adj_list()
        self.prev = {start_node: None}
        self.shortest_path = []
        self.queue = [start_node]
        self.bfs(start_node, fin_node)
        self.backtrack(fin_node)

    def dispatch(self, node):
        """ dispatch node info """

        self.subscriber.update_root(node)

    def get_adj_list(self):
        """ create graph adjacency list and distance array """

        adjacency_list = {}
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                for c in node.connections:
                    if 0 <= c[0] < len(self.nodes) and 0 <= c[1] < len(self.nodes[0]):
                        edge = self.nodes[c[0]][c[1]]
                        if edge.is_wall:
                            continue
                        adjacency_list.setdefault(node, [edge]).append(edge)
        return adjacency_list

    def bfs(self, s, e):

        s.visiting = True
        self.dispatch(s)

        if s == e:
            return

        for edge in self.adjacency_list[s]:
            if not edge.visited and edge not in self.queue:
                self.queue.append(edge)
                self.prev[edge] = self.queue[0]
                edge.in_queue = True
                self.dispatch(edge)

        s.visiting = False
        s.visited = True
        s.in_queue = False
        self.dispatch(s)

        self.queue.pop(0)

        if not self.queue:
            return

        self.bfs(self.queue[0], e)

    def backtrack(self, node):
        if node == self.start_node:
            self.visualise_path()
            return
        prev_node = self.prev[node]
        prev_node.in_path = True
        self.shortest_path.append(prev_node)
        self.backtrack(prev_node)

    def visualise_path(self):
        for node in reversed(self.shortest_path):
            self.dispatch(node)
