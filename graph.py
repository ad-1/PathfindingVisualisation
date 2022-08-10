import shutil
import requests
import tkinter as tk
import random
import time
from tkinter import messagebox
from ttkthemes import themed_tk as theme
from tkinter import ttk as tkk
from PIL import ImageTk, Image
from node import Node
from algorithms.breadth_first_search import BFS
from algorithms.depth_fist_search import DFS
from algorithms.dijkstra import Dijkstra
from progress_state import progress_state
from state import State
from math import inf


class Graph:

    def __init__(self):
        """ Init graphical user interface for pathfinding """

        self.algorithms = ['Breadth First Search', 'BFS Recursive', 'Depth First Search', 'DFS Recursive', 'Dijkstra', 'A*']
        self.solve_mode = 0
        self.draw_modes = [1, 2, 3, 4]
        self.draw_mode = 1
        self.is_solving, self.solved = False, False
        self.start_node, self.finish_node, self.last_rendered_node = None, None, None
        self.root = theme.ThemedTk()
        self.menu_frame = tkk.Frame(self.root)
        self.graph_width, self.graph_height = 1220, 850
        self.canvas = tk.Canvas(self.root, height=self.graph_height + 50, width=self.graph_width, bg='#333333')
        self.node_size = 20
        self.weight = 10
        self.n_cols, self.n_rows = None, None
        self.nodes, self.flat_nodes = None, None
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

    def config_nodes(self, event=None):
        """ configure all nodes on the graph """
        if self.is_solving:
            return
        self.clean_canvas()
        self.reset_local_nodes()
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
                progress_state(node, [], State.NORMAL, self.render_delay)
                self.nodes[i][j] = node
                idx += 1
        self.flat_nodes = [node for row in self.nodes for node in row]

    def config_menu(self):
        """ menu - user configurable settings for visualisation"""
        self.menu_frame.grid(row=0, column=0, sticky='n')
        menu_width = 18
        self.tkk_label(self.menu_frame, ['Start Program'])
        self.tkk_btn(self.menu_frame, [('Visualise', self.validate_graph)], True)
        # self.display_logo()
        self.tkk_label(self.menu_frame, ['Select Algorithm'])
        current_algo = tk.StringVar()
        current_algo.set(self.algorithms[self.solve_mode])
        algorithms_menu = tkk.OptionMenu(self.menu_frame, current_algo, self.algorithms[0], *self.algorithms, command=self.algorithm_change)
        algorithms_menu.config(width=menu_width)
        self.tkk_label(self.menu_frame, ['Node Size'])
        self.tkk_scaler(20, 60, self.change_node_size)
        self.tkk_label(self.menu_frame, ['Wall Frequency'])
        self.tkk_scaler(0.05, 0.5, self.change_wall_frequency)
        self.tkk_btn(self.menu_frame, [('Generate Random Maze', self.random_maze),
                                       ('Clear Graph', self.clear_graph),
                                       ('Clear Wall', self.clear_walls_and_weights),
                                       ('Clear Path', self.clear_path)], True)
        rb = tk.IntVar()
        rb.set(self.draw_mode)
        self.tkk_rbtn([('Place Start Node', rb), ('Place Finish Node', rb), ('Draw Wall Node', rb), ('Draw Weighted Node', rb)])
        self.tkk_label(self.menu_frame, ['Node Weight'])
        callback = self.menu_frame.register(self.only_numeric_input)
        tkk.Entry(self.menu_frame, validate="key", validatecommand=(callback, "%P")).insert(0, str(self.weight))
        self.tkk_label(self.menu_frame, ['Graph Legend'])
        state_keys = [(state.name, state.value) for state in State]
        self.tkk_btn(self.menu_frame, state_keys, False)
        for r, child in enumerate(self.menu_frame.winfo_children()):
            pad = 0 if isinstance(child, tk.Button) else 5
            child.grid_configure(row=r, column=0, sticky='ew', padx=pad, pady=pad)

    def clean_canvas(self):
        """ delete all shapes from canvas"""
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.shapes = []

    def reset_local_nodes(self):
        """ reset start, finish and last rendered nodes to None """
        self.start_node, self.finish_node, self.last_rendered_node = None, None, None

    def clear_graph(self):
        """ reset node back to initial state """
        if self.is_solving:
            return
        self.solved = False
        self.reset_local_nodes()
        for node in self.flat_nodes:
            progress_state(node, [], State.NORMAL, self.render_delay)

    def clear_walls_and_weights(self):
        """ clear all walls and weights from graph """
        if self.is_solving:
            return
        self.solved = False
        for node in self.flat_nodes:
            if node.state == State.WALL or node.state == State.WEIGHT:
                progress_state(node, [], State.NORMAL, self.render_delay)

    def clear_path(self):
        """ clear any nodes in last iteration """
        if self.is_solving:
            return
        self.solved = False
        for node in self.flat_nodes:
            if 1 < node.weight < inf:
                self.render_weight(node, random_weight=False, current_weight=True)
            elif node.state == State.VISITED or \
                    node.state == State.VISITING or \
                    node.state == State.QUEUE or \
                    node.state == State.PATH:
                progress_state(node, [], State.NORMAL, self.render_delay)

    def display_logo(self):
        """ display images for selected algorithms """
        url = 'https://fbcd.co/images/products/f004c91f1144880ca9a6bc83f3ae61f4_resize.jpg'
        file_name = 'images/logo.png'
        try:
            response = requests.get(url, stream=True)
        except requests.ConnectionError:
            return
        with open(file_name, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response
        img = ImageTk.PhotoImage(Image.open(file_name).resize((200, 100), Image.ANTIALIAS))
        image_label = tk.Label(self.menu_frame, image=img)
        image_label.img = img

    def only_numeric_input(self, i):
        try:
            if i == '':
                self.weight = inf
            else:
                self.weight = int(i)
            return True
        except Exception as e:
            tk.messagebox.showerror('Weight Error', 'Please enter a positive integer for node weights or leave blank for wall')
            print(e)
            return False

    @staticmethod
    def tkk_btn(parent, btns, is_tkk):
        """ create buttons given list of text and commands """
        for text, cmd in btns:
            if is_tkk:
                tkk.Button(parent, text=text, command=cmd)
            else:
                tk.Button(parent, text=text, highlightbackground=cmd, height=2, state='disabled')

    @staticmethod
    def tkk_label(parent, text):
        """ create labels from list of text """
        for t in text:
            tkk.Label(parent, text=t, anchor='e')

    def tkk_rbtn(self, rbtns):
        """ create radio buttons given text, mode and cmd """
        for i, (text, var) in enumerate(rbtns):
            tkk.Radiobutton(self.menu_frame,
                            text=text,
                            variable=var,
                            value=i + 1,
                            command=lambda: self.change_draw_mode(var.get()))

    def tkk_scaler(self, from_, to_, cmd):
        """ create themed scaler """
        tkk.Scale(self.menu_frame,
                  from_=from_,
                  to=to_,
                  orient=tk.HORIZONTAL,
                  command=cmd)

    def algorithm_change(self, *args):
        """ change solve mode """
        self.solve_mode = self.algorithms.index(args[0])

    def random_maze(self):
        """ generate a random maze """
        if self.is_solving:
            return
        for node in self.flat_nodes:
            if random.uniform(0, 1) < self.wall_frequency:
                if random.uniform(0, 1) < 0.5:
                    progress_state(node, [self.start_node, self.finish_node], State.WALL, self.render_delay)
                else:
                    self.render_weight(node, random_weight=True, current_weight=False)
                    # self.render_node(node, render_time=0)
            else:
                progress_state(node, [self.start_node, self.finish_node], State.NORMAL, self.render_delay)

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
        elif kp == '\'4\'':
            self.draw_mode = 4
        elif kp == '\'p\'':
            self.clear_path()
        elif kp == '\'c\'':
            self.clear_graph()
        elif kp == '\'m\'':
            self.random_maze()
        elif kp == '\'n\'':
            self.clear_walls_and_weights()
        elif kp == '\'v\'':
            self.validate_graph(True)

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
                    self.update_start_node(node)
                elif self.draw_mode == 2:
                    self.update_finish_node(node)
                elif self.draw_mode == 3:
                    self.update_wall_node(node)
                elif self.draw_mode == 4:
                    self.update_weight_node(node)
                return

    def update_start_node(self, node):
        """ update starting node """
        if self.start_node is not None:
            progress_state(self.start_node, [self.finish_node], State.NORMAL, self.render_delay)
        progress_state(node, [self.finish_node], State.START, self.render_delay)
        self.start_node = node
        if self.solved:
            self.validate_graph(animate=False)

    def update_finish_node(self, node):
        """ update finishing node """
        if self.finish_node is not None:
            progress_state(self.finish_node, [self.start_node], State.NORMAL, self.render_delay)
        progress_state(node, [self.start_node], State.FINISH, self.render_delay)
        self.finish_node = node
        if self.solved:
            self.validate_graph(animate=False)

    def update_wall_node(self, node):
        """ update node as wall or not """
        if node.state == State.WALL:
            progress_state(node, [self.start_node, self.finish_node], State.NORMAL, self.render_delay)
        elif node.state == State.NORMAL or node.state == State.WEIGHT:
            progress_state(node, [self.start_node, self.finish_node], State.WALL, self.render_delay)

    def update_weight_node(self, node):
        """ update node as weighted or not """
        if node.state == State.WEIGHT:
            progress_state(node, [self.start_node, self.finish_node], State.NORMAL, self.render_delay)
        elif node.state == State.NORMAL or node.state == State.WALL:
            self.render_weight(node, random_weight=False, current_weight=False)

    def render_weight(self, node, random_weight, current_weight):
        if random_weight:
            w = random.randrange(50)
        elif current_weight:
            w = node.weight
        else:
            w = self.weight
        progress_state(node, [self.start_node, self.finish_node], State.WEIGHT, self.render_delay, weight=w)
        self.canvas.create_text(node.x1 + (self.node_size / 2), node.y1 + (self.node_size / 2), fill="#333333", font="Times 11 bold",
                                text=node.weight)

    def validate_graph(self, animate=True):
        """ validate the graph is ready to be solved """
        if self.start_node is None or self.finish_node is None:
            return
        max_recursive_node_size = 35
        if (self.solve_mode == 1 or self.solve_mode == 3) and self.node_size < max_recursive_node_size:
            messagebox.showwarning('Recursion Info', 'Unable to run Recursive function '
                                                     'on node sizes less than {} due to Python recursion limit.'
                                                     ' Please increase node size and try again.'.format(max_recursive_node_size))
            return
        self.visualise_pathfinding(animate)

    def visualise_pathfinding(self, animate):
        """ solve using selected algorithm """
        self.clear_path()
        self.is_solving = True
        if self.solve_mode == 0 or self.solve_mode == 1:
            bfs_recursive = True if self.solve_mode == 1 else False
            BFS(self.nodes, bfs_recursive, self.start_node, self.finish_node, self, animate)
        elif self.solve_mode == 2 or self.solve_mode == 3:
            dfs_recursive = True if self.solve_mode == 3 else False
            DFS(self.nodes, dfs_recursive, self.start_node, self.finish_node, self, animate)
        elif self.solve_mode == 4 or self.solve_mode == 5:
            a_star = True if self.solve_mode == 5 else False
            Dijkstra(self.nodes, a_star, self.start_node, self.finish_node, self, animate)
        self.is_solving = False
        self.solved = True
