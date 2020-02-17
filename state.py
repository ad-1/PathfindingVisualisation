from enum import Enum


class State(Enum):
    """ different states a node may be in """
    normal = '#f6f4f2'
    start = '#71DE5F'
    finish = '#F15353'
    weighted = '#fcb6b6'
    wall = '#434343'
    queue = '#ebbfff'
    visiting = '#fc03c6'
    visited = '#83fce0'
    path = '#f2fc83'
