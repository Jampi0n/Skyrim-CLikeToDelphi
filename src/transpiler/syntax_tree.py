from pyleri import Grammar
from typing import *

try:
    from graphviz import Digraph
except ImportError:
    Digraph = None


class Node:
    """
    A node in the syntax tree.
    """

    # Unique identifier of the node. Used to draw the syntax tree.
    static_index = 0

    # Maps node names to node class types.
    node_map = {}

    def __init__(self, parent, start, end, name, element, string):
        """
        Creates a new node in the syntax tree.
        :param parent: Parent node.
        :param start: Start position in the code.
        :param end: End position in the code.
        :param name: If it is a grammar node, this is the name of the grammar object.
        :param element: What kind of node this is, e.g. Keyword, Token, Sequence, ...
        :param string: The code represented by this node.
        """
        self.parent = parent
        self.index = Node.static_index
        self.start = start
        self.end = end
        self.name = name
        self.element = element
        self.string = string
        self.children: List[Node] = []

        self.is_grammar = self.name is not None
        self.is_symbol = self.element in ['Keyword', 'Token']
        Node.static_index += 1

    def allow_children(self):
        return True

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

    def translated(self):
        return self.string

    def write(self, int_state, block):
        """
        Writes the transpiled code of this node to the block.
        Block specifies to which block the text is written.
        In some cases, other blocks need to be accessed via the Intermediate State object.
        :param int_state: Intermediate State object.
        :param block: Text Block of the Intermediate State object.
        :return:
        """
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


class Leaf(Node):
    def allow_children(self):
        return False


class SyntaxTree:
    def __init__(self, grammar: Grammar, string):
        result = grammar.parse(string)

        # The string must be valid.
        if not result.is_valid:
            assert False, 'The input code contains syntax errors:\n' \
                          + result.as_str() + '\nSurrounding code:\n' + string[result.pos - 30:result.pos + 30] + ''

        # Root node of the pyleri syntax tree.
        start = result.tree.children[0] if result.tree.children else result.tree

        def parse_tree(node, parent, current):
            """
            Parses the pyleri syntax tree starting at node and builds a custom syntax tree.
            :param node: The node of the pyleri syntax tree.
            :param parent: The parent node in the custom syntax tree.
            :param current: This parameter is used store the grammar object for the THIS element.
            :return:
            """

            is_grammar = hasattr(node.element, 'name')
            is_symbol = node.element.__class__.__name__ in ['Keyword', 'Token']

            is_real_grammar = is_grammar

            if is_grammar:
                name = node.element.name
            elif node.element.__class__.__name__ == 'This':
                # THIS refers to the current grammar object and is therefore a grammar object itself.
                name = current.name
                is_grammar = True
            elif is_symbol:
                # A symbol is a specific string.
                name = node.string
            else:
                name = node.element.__class__.__name__

            # Special case for EXPRESSION
            # The optional child of an EXPRESSION object is the ARGUMENT_LIST for function calls.
            if parent is not None:
                if parent.name == 'EXPRESSION':
                    if node.element.__class__.__name__ == 'Optional':
                        is_grammar = True
                        name = 'ARGUMENT_LIST'

            if is_grammar or is_symbol:  # Standard case.
                # Use correct class depending on name.
                node_class = Node.node_map[name] if is_grammar else Node

                # Create node object.
                node_object = node_class(parent, node.start, node.end, name, node.element.__class__.__name__,
                                         node.string)

                # Store current grammar object.
                if is_real_grammar:
                    current = node_object

                # If the node_object can have children, continue recursively.
                if node_object.allow_children():
                    for c in node.children:
                        node_object.add_child(parse_tree(c, node_object, current))

                return node_object
            else:  # The node is a temporary element like Sequence or Choice. In that case, no node object is created.
                for c in node.children:
                    parent.add_child(parse_tree(c, parent, current))
                return None

        # Create custom syntax tree.
        self.root = parse_tree(start, None, None)

    def draw(self):
        assert Digraph is not None, 'Module graphviz is required in order to draw the syntax tree.'
        graph = Digraph(comment='syntax tree')
        self.root.draw(graph, None)
        graph.render('out/syntax_tree.gv', view=False)

    def get_top_level(self):
        """
        Returns a list of top level elements.
        :return:
        """
        return [c.children[0] for c in self.root.children]
