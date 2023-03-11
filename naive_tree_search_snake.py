from MoveNode import MoveNode
from MoveTree import MoveTree
from snakebrain import get_safe_moves, simulate_next_move, get_move_value

def construct_tree(data, move, depth):
    root = MoveNode(move, None, get_move_value(data, data["you"], move))
    tree = MoveTree(root, depth)
    for _ in range(0, depth):
        add_layer(tree, data)
    return tree

def add_layer(tree, data):
    leaves = tree.get_leaves()
    sim_data = data
    #print("SIM DATA:", sim_data)
    you = {}
    for snake in sim_data["board"]["snakes"]:
        print("snakeid:", snake["id"], "youid:", data["you"]["id"])
        if snake["id"] == data["you"]["id"]:
            you = snake
    for leaf in leaves:
        sim_data = data
        parent_moves = leaf.get_parents(leaf)
        for parent in parent_moves:
            sim_data = apply_move_to_board(sim_data, you, parent.move)
        moves = get_safe_moves(sim_data, you)
        for move in moves:
            leaf.add_child(MoveNode(move, leaf, get_move_value(sim_data, you, move)))


def apply_move_to_board(data, snake, move):
    new_board = data
    new_board["board"]["snakes"][snake["id"]]["body"] = simulate_next_move(snake, move)
    new_board["board"]["snakes"][snake["id"]]["head"] = new_board["board"]["snakes"][snake["id"]]["body"][0]
    return new_board


def get_best_move(data, depth):
    moves = get_safe_moves(data, data["you"])
    best_move = moves[0]
    best_value = 0
    for move in moves:
        tree = construct_tree(data, move, depth)
        leaves = tree.get_leaves()
        for leaf in leaves:
            if leaf.value > best_value:
                best_value = leaf.value
                best_move = move
    return best_move