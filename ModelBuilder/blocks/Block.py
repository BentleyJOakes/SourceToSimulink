

class Block:

    def __init__(self, node):
        self.children = []
        self.kind = node.get('kind')
        self.parent = None
        self.vertex = None
        self.symbol_table = {}

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

        self.collect_childrens_symbol_table()


    def collect_childrens_symbol_table(self):
        print("Symbol_table before: " + str(self.symbol_table))
        for child in self.children:
            print("Symbol_table child: " + str(child.symbol_table))
            self.symbol_table.update(child.symbol_table)
        print("Symbol_table after: " + str(self.symbol_table))

    def store_in_symbol_table(self, name, value):
        self.symbol_table[name] = value
