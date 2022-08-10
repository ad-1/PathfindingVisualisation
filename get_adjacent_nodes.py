# Get graph adjacency list

from state import State


def get_adj_list(nodes):
    """
    return graph adjacency list (from DFS)
    :param nodes is 2d list of nodes
    """
    adjl = {}
    for i, row in enumerate(nodes):
        for j, node in enumerate(row):
            for c in node.connections:
                if 0 <= c[0] < len(nodes) and 0 <= c[1] < len(nodes[0]):
                    edge = nodes[c[0]][c[1]]
                    if edge.state == State.WALL:
                        continue
                    adjl.setdefault(node, [edge]).append(edge)
    return adjl
