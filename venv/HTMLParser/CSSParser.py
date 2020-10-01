
class Value(object):
    def __init__(self):
        self.name = ''
        self.value

class Declaration(object):
    def __init__(self):
        self.keyword = ''
        self.length = (None,None)      #units (PX,EM,...)
        self.ColorValue = (None,None,None,None) #rgba


class Selector(object):
    def __init__(self,tag_name,id,class_):
        self.tag_name = tag_name
        self.id = id
        self.class_ = class_


class Rule(object):
    def __init__(self,selectors,declarations):
        self.selectors = selectors
        self.declarations = declarations


class StyleSheet(object):
    def __init__(self):
        self.rules = []

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

    def parse_simple_selector(self):
        selector : Selector = Selector(None,None,None)

        while self.eof() == False:

            if self.next_char() == '#':
                self.consume_char()
                selector.id = self.parse_identifier()
            else :
                if self.next_char() == '.':
                    self.consume_char()
                    selector.class_ = self.parse_identifier()
                else:
                    if self.next_char() == '*':
                        self.consume_char()
                    else :
                        if valid_identifier_char(c):
                            selector.tag_name = self.parse_identifier()
                        else:
                            break

        return selector


    def specificity(self):
        selector : Selector = Selector(None,None,None)
     # to be continued

    def parse_rule(self):
        return  Rule(selectors = self.parse_selectors(),declarations = self.parse_declarations())

    def parse_selectors(self):
        selectors = []

        while True:
            selectors.append(self.parse_simple_selector())
            if self.next_char() == ',':
                self.consume_char()
                self.consume_whitespace()
            elif self.next_char() == '{':
                break;
            else:
                print("Unexpected character {} in selector list", c)
            selectors = selectors.sort(lambda a,b :self.compare(a,b))
            return selectors

    def compare(self,a,b):
        if self.specificity(a) > self.specificity(a):
            return a
        else:
            return b

        






