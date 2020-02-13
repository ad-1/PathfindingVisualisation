# Node object


class Node:
    """ Node in a graph """

    def __init__(self, x1, y1, x2, y2, row, col, idx):
        """ initialize node with graph positional info """

        self.id = 'node_' + str(idx)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.row = row
        self.col = col
        self.idx = idx
        self.is_start = False
        self.is_finish = False
        self.is_wall = False
        self.visited = False
        self.visiting = False
        self.in_path = False
        self.cost = 1
        self.connections = [(self.row - 1, self.col), (self.row, self.col + 1), (self.row + 1, self.col), (self.row, self.col - 1)]
