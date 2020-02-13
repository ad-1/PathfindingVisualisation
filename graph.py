# Graph in Tkinter for Graph Traversal

import tkinter as tk
from node import Node
from dijkstra import Dijkstra
from depth_fist_search import DFS
from breadth_first_search import BFS
from math import inf
import time
import random


class Graph:

    def __init__(self, px_width, px_height, px_cell_width):
        """
            initialize graph GUI

            solver modes:
            0 = dijkstra
            1 = depth first search
        """

        self.cell_width = px_cell_width
        self.n_cols = px_width // px_cell_width
        self.n_rows = px_height // px_cell_width
        self.root = tk.Tk()
        self.config_root()
        self.canvas = tk.Canvas(self.root, height=px_height, width=px_width, bg='#ffffff')
        self.random_maze = True
        self.nodes = [[None for _ in range(0, px_width, self.cell_width)] for _ in range(0, px_height, self.cell_width)]
        self.start_node = None
        self.finish_node = None
        self.is_solving = False
        self.last_rendered_node = None
        self.draw_mode = 0
        self.solve_mode = 'b'
        self.config_canvas()
        self.root.mainloop()

    def config_root(self):
        """ configure the canvas root """

        self.root.title('Graph Traversal')
        self.root.resizable(False, False)
        self.root.bind('<Key>', self.key_press_event)

    def config_canvas(self):
        """ pack canvas on root and bind mouse event methods """

        self.canvas.pack(fill=tk.BOTH, expand=False)
        self.canvas.bind('<Configure>', self.config_nodes)
        self.canvas.bind('<Button-1>', self.node_op)
        self.canvas.bind('<B1-Motion>', self.node_op)
        # self.canvas.bind('<ButtonRelease-1>', self.node_op)

    def config_nodes(self, event=None):
        """ configure all nodes on the graph """

        idx = 0

        for i, row in enumerate(self.nodes):
            y1 = i * self.cell_width
            y2 = y1 + self.cell_width
            for j, col in enumerate(row):
                x1 = j * self.cell_width
                x2 = x1 + self.cell_width
                node = Node(x1, y1, x2, y2, i, j, idx)
                self.nodes[i][j] = node
                if self.random_maze and random.uniform(0, 1) > 0.7:
                    node.is_wall = True
                self.render_node(node)
                idx += 1

    def render_node(self, node):
        """ draw node on canvas """

        color = '#ffffff'
        if node.is_wall:
            color = '#333333'
        elif node.is_start:
            color = '#00ff00'
        elif node.is_finish:
            color = '#ff0000'
        elif node.in_path:
            color = '#ffff00'
        elif node.in_queue:
            color = '#E2B8FF'
        elif node.visited:
            color = '#add8e6'
        elif node.visiting:
            color = '#ffff00'
        self.canvas.create_rectangle(node.x1, node.y1, node.x2, node.y2, fill=color)
        self.last_rendered_node = node

    def key_press_event(self, event):
        """
            change drawing mode
            0: choose start node
            1: choose finishing node
            2: draw walls
        """

        kp = repr(event.keysym)
        if kp == '\'1\'':
            self.draw_mode = 1
        elif kp == '\'2\'':
            self.draw_mode = 2
        elif kp == '\'3\'':
            self.draw_mode = 3
        elif kp == '\'space\'':
            self.validate_graph()
        elif kp == '\'k\'':
            self.solve_mode = 'k'
        elif kp == '\'d\'':
            self.solve_mode = 'd'
        elif kp == '\'b\'':
            self.solve_mode = 'b'
        elif kp == '\'r\'':
            self.reconfig_canvas()

    def node_op(self, event):
        """ node operations on canvas given mouse event """

        if self.is_solving:
            return

        if self.last_rendered_node is not None and \
                self.last_rendered_node.x1 <= event.x <= self.last_rendered_node.x2 and \
                self.last_rendered_node.y1 <= event.y <= self.last_rendered_node.y2:
            return

        for row in self.nodes:
            for node in row:
                if node.x1 <= event.x <= node.x2 and node.y1 <= event.y <= node.y2:
                    if self.draw_mode == 1:
                        self.update_start_node(node)
                        return
                    elif self.draw_mode == 2:
                        self.update_finish_node(node)
                        return
                    elif self.draw_mode == 3:
                        self.update_wall(node)
                        return

    def update_start_node(self, new_start_node):
        """ update the source node used in algorithm """

        if new_start_node.is_finish or new_start_node.is_wall:
            return

        if self.start_node is not None:
            osr, osc = self.start_node.row, self.start_node.col
            old_start_node = self.nodes[osr][osc]
            old_start_node.is_start = False
            self.render_node(old_start_node)
        new_start_node.is_start = True
        self.start_node = new_start_node
        self.render_node(new_start_node)

    def update_finish_node(self, new_fin_node):
        """ update the destination node used in algorithm """

        if new_fin_node.is_start or new_fin_node.is_wall:
            return

        if self.finish_node is not None:
            ofr, ofc = self.finish_node.row, self.finish_node.col
            old_fin_node = self.nodes[ofr][ofc]
            old_fin_node.is_finish = False
            self.render_node(old_fin_node)
        new_fin_node.is_finish = True
        self.finish_node = new_fin_node
        self.render_node(new_fin_node)

    def update_wall(self, node):
        """ update node as wall or not """

        if not node.is_start and not node.is_finish:
            node.is_wall = False if node.is_wall else True
            node.cost = inf if node.is_wall else 1
            self.render_node(node)

    def validate_graph(self):
        """ validate the graph is ready to be solved """

        if self.start_node is not None and self.finish_node is not None:
            self.solve()

    def solve(self):
        """ solve using dijkstra's algorithm """

        self.is_solving = True
        if self.solve_mode == 'k':
            Dijkstra(self.nodes, self.start_node, self.finish_node, self)
        elif self.solve_mode == 'd':
            DFS(self.nodes, self.start_node, self.finish_node, self)
        elif self.solve_mode == 'b':
            BFS(self.nodes, self.start_node, self.finish_node, self)
        self.is_solving = False

    def update_root(self, node):
        """ update root to display visiting node """
        self.render_node(node)
        self.root.update()
        if node.in_path:
            time.sleep(0.15)
        else:
            time.sleep(0.01)

    def reconfig_canvas(self):
        """ refresh gui """

        if not self.is_solving:
            self.config_nodes()


# Program Driver
if __name__ == '__main__':
    game = Graph(px_width=1000, px_height=600, px_cell_width=20)
