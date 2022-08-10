from enum import Enum


class State(Enum):
    """ different states a node may be in """

    NORMAL = '#f6f4f2'
    START = '#71DE5F'
    FINISH = '#F15353'
    WEIGHT = '#eba173'
    WALL = '#434343'
    QUEUE = '#ebbfff'
    VISITING = '#fc03c6'
    VISITED = '#83fce0'
    PATH = '#f2fc83'
