
def progress_state(node, constants, state, render_delay):
    """ change state of node based on algorithm progress """
    if node not in constants:
        node.state = (state, render_delay)
