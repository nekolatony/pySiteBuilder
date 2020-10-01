from html.parser import HTMLParser

class Node(object):
    def __init__(self,type = None,children = None,attributes = None):
        self.parent = None
        self.type = type
        if children is None :
            self.children = []
        else:
            self.children = children

class Parser(HTMLParser):
  # method to append the start tag to the list start_tags.
  def handle_starttag(self, tag, attrs):
    print("Encountered a start tag:", tag)
    global  nodes
    if tag == 'body':
        nodes.clear()

    node = Node(type = tag,children=None,attributes= None)
    nodes.append(node)
    global start_tags
    start_tags.append(tag)

    # method to append the end tag to the list end_tags.
  def handle_endtag(self, tag):
    print("Encountered an end tag:", tag)
    global end_tags
    global nodes
    end_tags.append(tag)
    if tag == start_tags[len(start_tags)-1]:
        i = 0
        start_tags.pop(len(start_tags)-1)
        for i in range(len(nodes)-1,0,-1):
            if tag == nodes[i].type:
                break
            if tag != 'html':
                node = nodes.pop(i)
                print("child :" + node.type)
                nodes[i - 1].children.append(node)
                print("child :" + node.type + " parent :" + nodes[i - 1].type)

  # method to append the data between the tags to the list all_data.
  def handle_data(self, data):
    global all_data
    all_data.append(data)

  # method to append the comment to the list comments.
  def handle_comment(self, data):
    global comments
    comments.append(data)

def handle_heirachy(start_tags,end_tag,nodes):

    for i in range(len(start_tags)):
        if start_tags[i] == end_tag[i]:
            break


    return 1

def print_DOM_tree(space, tree):
    print( space + tree.type + "")
    for i in range(len(tree.children)):
        print_DOM_tree(space + "____", tree.children[i])


html1 = """<html><title>Desserts</title><body><p>
            I am a fan of frozen yoghurt.</p><
            /body><!--My first webpage--></html>"""

html2 = """<!doctype html>

                <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <meta name = "description" content = "The HTML5 Herald">
                    <meta name = "author" content = "SitePoint">
                    <link rel = "stylesheet" href = "css/styles.css?v=1.0">

                    <title>The HTML5 Herald</title>
                </head>

                <body>
                    <h1>This site is created in python</h1>
                    
                    <img src="  """ + r"""file:///C:\Users\nekol\Documents\PycharmProjects\webSite-generator\venv\Site\python.png" alt="python" width="100" height="100"></img>
                    
                    <h2>Author: Tony Nekola</h2>
                   
                </body>
                </html>"""

nodes = []
start_tags = []
end_tags = []
all_data = []
comments = []
# Creating an instance of our class.
parser = Parser()
# Poviding the input.
parser.feed(html2)

# print("start tags:", start_tags)
# print("end tags:", end_tags)
# print("data:", all_data)
# print("comments", comments)
#
print_DOM_tree(" ", nodes[0])


