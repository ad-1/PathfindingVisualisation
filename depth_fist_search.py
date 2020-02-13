# Depth First Search


class DFS:

    def __init__(self, nodes, start_node, fin_node, root):
        """ initialize solver """

        self.subscriber = root
        self.nodes = nodes
        self.adjacency_list = self.get_adj_list()
        self.visited = []
        self.path = []
        self.fin_node = fin_node
        self.dfs(start_node)
        self.backtrack()

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

    def dfs(self, node):
        """ depth first search algorithm """

        if node == self.fin_node:
            return True
        if not node.visited:
            node.visited = True
            self.visited.append(node)
            self.dispatch(node)
            edges = self.adjacency_list[node]
            for edge in edges:
                if self.dfs(edge):
                    self.path.append(edge)
                    return True

        return False

    def backtrack(self):
        """ backtrack through path to finish node """

        for node in reversed(self.path):
            node.in_path = True
            self.dispatch(node)
