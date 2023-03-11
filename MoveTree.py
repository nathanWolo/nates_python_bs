class MoveTree():

    def __init__(self, root_move, depth):
        self.root_move = root_move
        self.depth = depth
        
    def get_leaves(self):
        leaves = []
        leaves = self.get_leaves_helper(self.root_move, leaves)
        return leaves

    def get_leaves_helper(self, node, leaves):
        if len(node.children) == 0:
            leaves.append(node)
        else:
            for child in node.children:
                self.get_leaves_helper(child, leaves)
        return leaves