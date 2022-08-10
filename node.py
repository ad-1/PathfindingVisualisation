from state import State
from math import inf


class Node:
    def __init__(self, x1, y1, x2, y2, row, col, idx, root):
        """ initialize node with graph positional info """
        self.subscriber = root
        self.id = 'n_' + str(idx)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.row, self.col = row, col
        self.idx = idx
        self.weight = 1
        self._state = State.NORMAL
        self.connections = [(self.row - 1, self.col),
                            (self.row, self.col + 1),
                            (self.row + 1, self.col),
                            (self.row, self.col - 1)]

    def __repr__(self):
        return '<Node {}, State \'{}\'>'.format(self.idx, self.state.name)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        """ set state """
        state, render_delay, w = val
        self._state = state
        if state == State.WALL:
            self.weight = inf
        elif state != State.VISITED and state != State.VISITING and state != State.PATH and state != State.QUEUE:
            self.weight = w
        self.dispatch(self, render_delay)

    def dispatch(self, node, render_time):
        """ dispatch node info """
        self.subscriber.render_node(node, render_time)
