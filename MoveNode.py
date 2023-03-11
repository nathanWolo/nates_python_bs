class MoveNode():

    def __init__(self, move, parent, value, depth=0):
        self.move = move
        self.parent = parent
        self.children = []
        self.depth = depth
        self.value = value
    def add_child(self, child):
        child.depth = self.depth + 1
        self.children.append(child)

    def get_parents(self, node):
        parents = []
        parents = self.get_parents_helper(node, parents)
        return parents

    def get_parents_helper(self, node, parents):
        if node.parent != None:
            parents.append(node.parent)
            self.get_parents_helper(node.parent, parents)
        return parents