from pyleri import Grammar
from graphviz import Digraph
from typing import *
import json


class Node:
    static_id = 0
    node_map = {}

    def __init__(self, parent, start, end, name, element, string):
        self.parent = parent
        self.id = Node.static_id
        self.start = start
        self.end = end
        self.name = name
        self.element = element
        self.string = string
        self.children: List[Node] = []
        self.index = 0

        self.is_grammar = self.name is not None
        self.is_symbol = self.element in ['Keyword', 'Token']
        Node.static_id += 1

    def allow_children(self):
        return True

    def add_child(self, child):
        if child is not None:
            child.index = len(self.children)
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
        graph.node(str(self.id), self.display_name())
        if self.parent is not None:
            graph.edge(str(parent.id), str(self.id))

        for c in self.children:
            c.draw(graph, self)

    def translated(self):
        return self.string

    def write(self, int_state, block):
        token_translation = {
            '!': ' Not ',
            '!=': ' <> ',
            '&&': ' And ',
            '||': ' Or ',
            '%': ' mod ',
            '+': ' + ',
            '-': ' - ',
            '*': ' * ',
            '/': ' / ',
            '<': ' < ',
            '>': ' > ',
            '==': ' = '
        }
        string = self.translated()
        if string in token_translation:
            string = token_translation[string]
        block.append(string)

    def index_of_type(self, class_type, index=0):
        counter = 0
        i = 0
        for c in self.children:
            if isinstance(c, class_type):
                if class_type == index:
                    return i
                counter += 1
            i += 1

        return -1

    def child_of_type(self, class_type, index=0):
        index = self.index_of_type(class_type, index)
        if index != -1:
            return self.children[index]
        return None

    def children_of_type(self, class_type):
        array = []
        for c in self.children:
            if isinstance(c, class_type):
                array.append(c)
        return array

    def get_index(self):
        return self.index


class Leaf(Node):
    def allow_children(self):
        return False


class SyntaxTree:
    def __init__(self, grammar: Grammar, string):
        result = grammar.parse(string)
        if not result.is_valid:
            assert False, result.as_str() + '\n' + string[result.pos - 30:result.pos + 30]

        start = result.tree.children[0] if result.tree.children else result.tree

        def parse_tree(node, parent, current):
            is_grammar = hasattr(node.element, 'name')
            is_symbol = node.element.__class__.__name__ in ['Keyword', 'Token']

            is_real_grammar = is_grammar

            if is_grammar:
                name = node.element.name
            elif node.element.__class__.__name__ == 'This':
                name = current.name
                is_grammar = True
            elif is_symbol:
                name = node.string
            else:
                name = node.element.__class__.__name__

            if parent is not None:
                if parent.name == 'EXPRESSION':
                    if node.element.__class__.__name__ == 'Optional':
                        is_grammar = True
                        if hasattr(node.children[0].element, 'name') and node.children[0].element.name == 'COMMENT':
                            name = 'CMT'
                        else:
                            name = 'ARGUMENT_LIST'

            if is_grammar or is_symbol:
                node_class = Node.node_map[name] if is_grammar else Node

                node_object = node_class(parent, node.start, node.end, name, node.element.__class__.__name__,
                                         node.string)

                if is_real_grammar:
                    current = node_object

                if node_object.allow_children():
                    for c in node.children:
                        node_object.add_child(parse_tree(c, node_object, current))

                return node_object
            else:
                for c in node.children:
                    parent.add_child(parse_tree(c, parent, current))
                return None

        self.root = parse_tree(start, None, None)
        # print(json.dumps(view_parse_tree(result), indent=2))
        self.draw()

    def draw(self):
        graph = Digraph(comment='syntax tree')
        self.root.draw(graph, None)
        graph.render('out/syntax_tree.gv', view=False)

    def get_top_level(self):
        return [c.children[0] for c in self.root.children]


# Returns properties of a node object as a dictionary:
def node_props(node, children):
    return {
        'start': node.start,
        'end': node.end,
        'name': node.element.name if hasattr(node.element, 'name') else None,
        'element': node.element.__class__.__name__,
        'string': node.string,
        'children': children}


# Recursive method to get the children of a node object:
def get_children(children):
    return [node_props(c, get_children(c.children)) for c in children]


# View the parse tree:
def view_parse_tree(res):
    start = res.tree.children[0] \
        if res.tree.children else res.tree
    return node_props(start, get_children(start.children))
