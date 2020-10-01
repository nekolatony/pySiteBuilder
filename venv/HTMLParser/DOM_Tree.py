
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











