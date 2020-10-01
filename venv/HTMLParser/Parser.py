# from DOM_Tree import *
import string

tag_names = list(string.ascii_letters)
tag_names.extend(list(string.digits))

html = """<html>
    <body>
        <h1>Title</h1>
        <div id="main" class="test">
            <p>Hello <em>world</em>!</p>
        </div>
    </body>
</html>"""

html2 = """ <html lang="en">
                <head>


                </head>

                <body>
                    <h1>This site is created in python</h1>
                    <br>
                    <img src="  """ + r"""file:///C:\Users\nekol\Documents\PycharmProjects\webSite-generator\venv\Site\python.png" alt="python" width="100" height="100"></img>
                    <br>
                    <h2>Author: Tony Nekola</h2>
                    <br>
                </body>
                </html>"""

class Element_Data(object):
    def __init__(self,attributes):
        self.tag_name = None
        self.attributes = attributes
        self.type_ = None

class Node_type(object):
    def __init__(self,type = None,attributes = None):
        self.children = []
        self.Element = Element_Data(attributes)
        self.type_ = type

class Node(object):
    def __init__(self,type = None,children = None,attributes = None):
        self.parent = None
        self.node_type = Node_type(type,attributes)
        if children is None :
            self.children = []
        else:
            self.children = children
    def setParent(self,parent):
        self.parent = parent

def createNode(data):
    return Node(data)

def element(name,attributes,children):
    return Node(name,children,attributes)


class HTMLParser(object):
    def __init__(self, input=None):
        self.input = input
        self.position = 0

    def next_char(self):
        return self.input[self.position]

    def starts_with(self, str_):
        return self.input.startswith(str_, self.position)

    def eof(self):
        return self.position == len(self.input)

    def consume_char(self):
        curr_char = self.input[self.position]
        self.position = self.position + 1
        return curr_char

    def consume_while(self, F):
        result = str('')
        while self.eof() is False and F(self.next_char()):
            result = result + self.consume_char()
        return result

    def consume_whitespace(self):
        self.consume_while(lambda s: s == ' ')

    def isIN(self, c):
        if c in tag_names:
            return c
        else:
            return None

    def parse_tag_name(self):  # /arse a tag or attribute name.
        return self.consume_while(lambda c: c in tag_names)

    def parse_text(self):
        return self.consume_while(lambda c: c != '<')

    def parse_node(self):
        if self.next_char() == '<':
            return self.parse_element()
        else:
            self.parse_text()
            return

    def parse_attr_value(self):
        open_quote = self.consume_char()
        assert open_quote == '"' or open_quote == r'\'', 'HTMLParser.attr()\nnot an open quote'
        value = self.consume_while(lambda c: c != open_quote)
        assert open_quote == self.consume_char(), 'HTMLParser.attr()\nnot an close quote'
        return value

    def parse_attr(self):
        self.consume_whitespace()
        name = self.parse_tag_name()
        self.consume_whitespace()
        assert self.consume_char() == '=', 'HTMLParser.parse_attr()\nnot =\n'
        self.consume_whitespace()
        value = self.parse_attr_value()
        return {name: value}

    def parse_attributes(self):
        attributes = dict()

        self.consume_whitespace()
        while True:
            if self.next_char() == '>':
                break
            attr = self.parse_attr()
            for key in attr.keys():
                attributes[key] = attr[key]
        return attributes

    def parse_nodes(self):
        nodes = list()
        while True:
            self.consume_whitespace()
            if self.eof() or self.starts_with('</'):
                break;
            node = self.parse_node()
            if node != None:
                nodes.append(node)
        return nodes

    def parse_element(self):
        tag_name = ''
        attr = dict()
        assert self.consume_char() == '<', 'HTMLParser.parse_element() \nOpening tag not <'
        tag_name = self.parse_tag_name()
        attr = self.parse_attributes()
        assert self.consume_char() == '>', 'HTMLParser.parse_element()\nOpening tag not >'

        if tag_name == 'br':
            return Node(type=tag_name, attributes=None, children=None)
        children = self.parse_nodes()

        assert self.consume_char() == '<', 'HTMLParser.parse_element()\nClosing tag not <'
        assert self.consume_char() == '/', 'HTMLParser.parse_element()\nClosing tag not /'
        assert tag_name == self.parse_tag_name(), 'HTMLParser.parse_element()\nClosing tag - tag name is not the same'
        assert self.consume_char() == '>', 'HTMLParser.parse_element()\nClosing tag not >'

        return Node(type=tag_name, attributes=attr, children=children)


def parse(source):
    htmlparser_ = HTMLParser(input=source)
    nodes = list()
    nodes = htmlparser_.parse_nodes()
    if len(nodes) == 1:
        return nodes
    else:
        return Node(type='html', children=nodes, attributes=None)

def DOM_tree(space, tree):
    tree = tree[0]
    for i in range(len(tree.children) - 1, -1, -1):
        if type(tree.children[i]) == str:
            tree.children.pop(i)
    for i in range(len(tree.children)):
        print_DOM_tree(space + "____", tree.children[i])



def print_DOM_tree(space, tree):
    print("|" + space + tree.node_type.type_ + "")
    for i in range(len(tree.children)):
        print_DOM_tree(space + "____", tree.children[i])


def get_DOM_Tree(data):
    # with open(html_file_url, 'r') as file:
    #     # read a list of lines into data
    #     data = file.readlines()
    # print(data)

    html = ""
    for line in data:
        if html.find('<body>'):
            break
        html = html + line
    dom_tree = parse(html)
    return dom_tree[0]


# print(html)
# tree = parse(html)
# print_DOM_tree("", tree[0])