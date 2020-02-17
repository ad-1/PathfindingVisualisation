# Graph in Tkinter for Pathfinding Visualisation
import shutil

import requests
import tkinter as tk
import random
import time
from ttkthemes import themed_tk as theme
from tkinter import ttk as tkk
from PIL import ImageTk, Image
from node import Node
from algorithms.breadth_first_search import BFS
from algorithms.depth_fist_search import DFS
from algorithms.dijkstra import Dijkstra
from helpers.progress_state import progress_state
from state import State
from math import inf


class Graph:

    def __init__(self):
        """ Init graphical user interface for pathfinding """

        self.algorithms = ['Breadth First Search', 'Depth First Search', 'Dijkstra', 'A*']
        self.solve_mode = 0
        self.draw_modes = [1, 2, 3]
        self.draw_mode = 1
        self.is_solving = False
        self.last_rendered_node = None
        self.start_node = None
        self.finish_node = None
        self.root = theme.ThemedTk()
        self.menu_frame = tkk.Frame(self.root)
        self.graph_width = 1220
        self.graph_height = 850
        self.canvas = tk.Canvas(self.root, height=self.graph_height + 50, width=self.graph_width, bg='#333333')
        self.node_size = 20
        self.n_cols = None
        self.n_rows = None
        self.nodes = None
        self.flat_nodes = None
        self.shapes = []
        self.wall_frequency = 0.05
        self.render_delay = 0
        self.config_root()
        self.config_menu()
        self.config_canvas()
        self.root.mainloop()

    def config_root(self):
        """ configure tkinter root object """
        self.root.title('Pathfinding Visualisation')
        self.root.resizable(False, False)
        self.root.grid_propagate(True)
        self.root.get_themes()
        self.root.set_theme('radiance')
        self.root.config(background='#424242')
        self.root.bind('<Key>', self.key_press_event)

    def config_canvas(self):
        """ pack canvas on root and bind mouse event methods """
        self.canvas.bind('<Configure>', self.config_nodes)
        self.canvas.bind('<Button-1>', self.node_operation)
        self.canvas.bind('<B1-Motion>', self.node_operation)
        self.canvas.grid(row=0, column=1)

    def clean_canvas(self):
        """ delete all shapes from canvas"""
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.shapes = []

    def config_nodes(self, event=None):
        """ configure all nodes on the graph """
        if self.is_solving:
            return
        self.clean_canvas()
        self.reset_stored_nodes()
        self.n_cols = int(self.graph_width // self.node_size)
        self.n_rows = int(self.graph_height // self.node_size)
        self.nodes = [[None for _ in range(0, self.n_cols)] for _ in range(0, self.n_rows)]
        idx = 0
        for i, row in enumerate(self.nodes):
            y1 = i * self.node_size
            y2 = y1 + self.node_size
            for j, col in enumerate(row):
                x1 = j * self.node_size
                x2 = x1 + self.node_size
                node = Node(x1, y1, x2, y2, i, j, idx, self)
                progress_state(node, [], State.normal, self.render_delay)
                self.nodes[i][j] = node
                idx += 1
        self.flat_nodes = [node for row in self.nodes for node in row]

    def reset_stored_nodes(self):
        self.start_node = None
        self.finish_node = None
        self.last_rendered_node = None

    def clear_graph(self):
        """ reset node back to initial state """
        if self.is_solving:
            return
        self.reset_stored_nodes()
        for node in self.flat_nodes:
            progress_state(node, [], State.normal, self.render_delay)

    def clear_walls(self):
        """ clear all walls from graph """
        if self.is_solving:
            return
        for node in self.flat_nodes:
            if node.state == State.wall:
                progress_state(node, [], State.normal, self.render_delay)

    def clear_path(self):
        """ clear any nodes in last iteration """
        if self.is_solving:
            return
        for node in self.flat_nodes:
            if node.state == State.visited or \
                    node.state == State.visiting or \
                    node.state == State.queue or \
                    node.state == State.path:
                progress_state(node, [], State.normal, self.render_delay)

    def display_logo(self):
        """ display images for selected algorithms """
        url = 'https://fbcd.co/images/products/f004c91f1144880ca9a6bc83f3ae61f4_resize.jpg'
        file_name = 'images/logo.png'
        response = requests.get(url, stream=True)
        with open(file_name, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response
        img = ImageTk.PhotoImage(Image.open(file_name).resize((200, 100), Image.ANTIALIAS))
        image_label = tk.Label(self.menu_frame, image=img)
        image_label.img = img

    def config_menu(self):
        """ menu - user configurable settings for visualisation"""
        self.menu_frame.grid()
        menu_width, padx, pady = 18, 10, 5
        self.display_logo()
        current_algo = tk.StringVar()
        current_algo.set(self.algorithms[self.solve_mode])
        algorithms_menu = tk.OptionMenu(self.menu_frame, current_algo, *self.algorithms, command=self.algorithm_change)
        algorithms_menu.config(width=menu_width)
        node_size_label = tk.Label(self.menu_frame, text='Node Size', anchor='w')
        node_size_scaler = tk.Scale(self.menu_frame,
                                    from_=20,
                                    to=60,
                                    orient=tk.HORIZONTAL,
                                    command=self.change_node_size,
                                    resolution=2)
        tkk.Button(self.menu_frame, text='Clear Graph', command=self.clear_graph)
        tkk.Button(self.menu_frame, text='Clear Wall', command=self.clear_walls)
        tkk.Button(self.menu_frame, text='Clear Path', command=self.clear_path)
        tkk.Button(self.menu_frame, text='Generate Random Maze', command=self.random_maze)
        wall_frequency_label = tk.Label(self.menu_frame, text='Wall Frequency', anchor='w')
        wall_frequency_scaler = tk.Scale(self.menu_frame,
                                         from_=0.05,
                                         to=0.5,
                                         orient=tk.HORIZONTAL,
                                         command=self.change_wall_frequency,
                                         resolution=0.01)
        rb = tk.IntVar()
        rb.set(self.draw_mode)
        rb_start = tk.Radiobutton(self.menu_frame,
                                  text='Place Start Node',
                                  variable=rb,
                                  value=self.draw_modes[0],
                                  command=lambda: self.change_draw_mode(rb.get()))
        tk.Radiobutton(self.menu_frame,
                       text='Place Finish Node',
                       variable=rb,
                       value=self.draw_modes[1],
                       command=lambda: self.change_draw_mode(rb.get()))
        tk.Radiobutton(self.menu_frame,
                       text='Draw Weighted Node',
                       variable=rb,
                       value=self.draw_modes[2],
                       command=lambda: self.change_draw_mode(rb.get()))
        visualise_button = tkk.Button(self.menu_frame, text='Visualise', command=self.validate_graph)
        for r, child in enumerate(self.menu_frame.winfo_children()):
            if child == node_size_label or child == wall_frequency_label:
                child.grid_configure(row=r, column=0, sticky='ew', pady=(10, 0), padx=padx)
            elif child == node_size_scaler or child == wall_frequency_scaler:
                child.grid_configure(row=r, column=0, sticky='ew', pady=(0, 10), padx=padx)
            elif isinstance(child, tk.Radiobutton):
                if child == rb_start:
                    child.grid_configure(row=r, column=0, sticky='ew', pady=(12, 0), padx=padx)
                else:
                    child.grid_configure(row=r, column=0, sticky='ew', pady=0, padx=padx)
            elif child == visualise_button:
                child.grid_configure(row=r, column=0, sticky='ew', pady=15, padx=padx)
            else:
                child.grid_configure(row=r, column=0, sticky='ew', pady=pady, padx=padx)

    def algorithm_change(self, *args):
        """ change solve mode """
        self.solve_mode = self.algorithms.index(args[0])

    def random_maze(self):
        """ generate a random maze """
        if self.is_solving:
            return
        for node in self.flat_nodes:
            if random.uniform(0, 1) < self.wall_frequency:
                progress_state(node, [self.start_node, self.finish_node], State.wall, self.render_delay)
            else:
                progress_state(node, [self.start_node, self.finish_node], State.normal, self.render_delay)

    def change_wall_frequency(self, val):
        """ change probability a wall will appear for random maze """
        self.wall_frequency = float(val)

    def change_node_size(self, val):
        """ change graph size """
        self.node_size = float(val)
        self.config_nodes()

    def change_draw_mode(self, val):
        """ 1 for start node, 2 for finish node, 3 for weighted nodes """
        self.draw_mode = val

    def key_press_event(self, event):
        """1 change drawing mode """
        kp = repr(event.keysym)
        if kp == '\'1\'':
            self.draw_mode = 1
        elif kp == '\'2\'':
            self.draw_mode = 2
        elif kp == '\'3\'':
            self.draw_mode = 3
        elif kp == '\'p\'':
            self.clear_path()
        elif kp == '\'c\'':
            self.clear_graph()
        elif kp == '\'m\'':
            self.random_maze()
        elif kp == '\'n\'':
            self.clear_walls()
        elif kp == '\'space\'':
            self.validate_graph()

    def render_node(self, node, render_time):
        """ draw node on canvas """
        shape = self.canvas.create_rectangle(node.x1, node.y1, node.x2, node.y2, fill=node.state.value)
        self.shapes.append(shape)
        self.last_rendered_node = node
        if render_time != 0:
            self.root.update()
            time.sleep(render_time)

    def validate_operation(self, event):
        """ prevent against overlapping events """
        if self.is_solving or self.last_rendered_node is not None and \
                self.last_rendered_node.x1 <= event.x <= self.last_rendered_node.x2 and \
                self.last_rendered_node.y1 <= event.y <= self.last_rendered_node.y2:
            return False
        return True

    def node_operation(self, event):
        """ node operations on canvas given mouse event """
        if not self.validate_operation(event):
            return
        for node in self.flat_nodes:
            if node.x1 <= event.x <= node.x2 and node.y1 <= event.y <= node.y2:
                if self.draw_mode == 1:
                    self.update_start(node)
                elif self.draw_mode == 2:
                    self.update_finish(node)
                elif self.draw_mode == 3:
                    self.update_wall(node)
                return

    def update_start(self, node):
        """ update starting node """
        if self.start_node is not None:
            progress_state(self.start_node, [self.finish_node], State.normal, self.render_delay)
        progress_state(node, [self.finish_node], State.start, self.render_delay)
        self.start_node = node

    def update_finish(self, node):
        """ update finishing node """
        if self.finish_node is not None:
            progress_state(self.finish_node, [self.start_node], State.normal, self.render_delay)
        progress_state(node, [self.start_node], State.finish, self.render_delay)
        self.finish_node = node

    @staticmethod
    def update_wall(node):
        """ update node as wall or not """
        if node.state != State.start and node.state != State.finish:
            node.state = (State.wall, 0) if node.state != State.wall else (State.normal, 0)
            node.cost = inf if node.cost == 1 else inf

    def validate_graph(self):
        """ validate the graph is ready to be solved """
        if self.start_node is not None and self.finish_node is not None:
            self.visualise_pathfinding()

    def visualise_pathfinding(self):
        """ solve using selected algorithm """
        self.clear_path()
        self.is_solving = True
        if self.solve_mode == 0:
            BFS(self.nodes, self.start_node, self.finish_node, self)
        elif self.solve_mode == 1:
            DFS(self.nodes, self.start_node, self.finish_node, self)
        elif self.solve_mode == 2 or self.solve_mode == 3:
            a_star = True if self.solve_mode == 3 else False
            Dijkstra(self.nodes, a_star, self.start_node, self.finish_node, self)
        self.is_solving = False
