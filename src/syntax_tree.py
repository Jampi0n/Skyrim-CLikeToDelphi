from pyleri import Grammar
from graphviz import Digraph


class Node:
    static_index = 0

    def __init__(self, parent, start, end, name, element, string):
        self.parent = parent
        self.index = Node.static_index
        self.start = start
        self.end = end
        self.name = name
        self.element = element
        self.string = string
        self.children = []

        self.is_grammar = self.name is not None
        self.is_symbol = self.element in ['Keyword', 'Token']
        Node.static_index += 1

    def add_child(self, child):
        if child is not None:
            self.children.append(child)

    def to_str(self, indentation):
        string = ' ' * indentation + self.display_name()

        for c in self.children:
            string += '\n' + c.to_str(indentation + 1)
        return string

    def __str__(self):
        return self.to_str(0)

    def display_name(self):
        string = ''
        if self.is_grammar:
            string += self.name
        elif self.is_symbol:
            string += '"' + self.string + '"'
        else:
            string += ''
        return string

    def draw(self, graph, parent):
        graph.node(str(self.index), self.display_name())
        if self.parent is not None:
            graph.edge(str(parent.index), str(self.index))

        for c in self.children:
            c.draw(graph, self)


class SyntaxTree:
    def __init__(self, grammar: Grammar, string):
        result = grammar.parse(string)

        start = result.tree.children[0] if result.tree.children else result.tree

        def parse_tree(node, parent):
            is_grammar = hasattr(node.element, 'name')
            is_symbol = node.element.__class__.__name__ in ['Keyword', 'Token']

            if is_grammar or is_symbol:
                node_object = Node(parent, node.start, node.end,
                                   node.element.name if hasattr(node.element, 'name') else None,
                                   node.element.__class__.__name__, node.string)

                for c in node.children:
                    node_object.add_child(parse_tree(c, node_object))

                return node_object
            else:
                for c in node.children:
                    parent.add_child(parse_tree(c, parent))
                return None

        self.root = parse_tree(start, None)

        print(self.root)
        self.draw()

    def draw(self):
        graph = Digraph(comment='syntax tree')
        self.root.draw(graph, None)
        graph.render('out/syntax_tree.gv', view=True)

    def get_top_level(self):
        return [c.children[0] for c in self.root.children]
