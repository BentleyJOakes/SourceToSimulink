

class Block:

    def __init__(self, node):
        self.children = []
        self.kind = node.get('kind')
        self.parent = None
        self.vertex = None

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parent = parent

    def add_to_model(self, h):
        for child in self.children:
            child.add_to_model(h)

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = self.kind

        self.vertex = vertex

        for child in self.children:
            h.add_edge(vertex, child.vertex)

