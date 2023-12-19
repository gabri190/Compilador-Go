class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, table):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        if self.value == '+':
            return self.children[0].evaluate(table) + self.children[1].evaluate(table)
        elif self.value == '-':
            return self.children[0].evaluate(table) - self.children[1].evaluate(table)
        elif self.value == '*':
            return self.children[0].evaluate(table) * self.children[1].evaluate(table)
        elif self.value == '/':
            return self.children[0].evaluate(table) // self.children[1].evaluate(table)
        elif self.value=='|':
            return self.children[0].evaluate(table) or self.children[1].evaluate(table)
        elif self.value=='&':
            return self.children[0].evaluate(table) and self.children[1].evaluate(table)
        elif self.value=='>':
            return self.children[0].evaluate(table) > self.children[1].evaluate(table)
        elif self.value=='<':
            return self.children[0].evaluate(table) < self.children[1].evaluate(table)
        elif self.value=='=':
            return self.children[0].evaluate(table) == self.children[1].evaluate(table)
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        if self.value == '+':
            return self.children[0].evaluate(table)
        elif self.value == '-':
            return -self.children[0].evaluate(table)
        elif self.value=='!':
            return not self.children[0].evaluate(table)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        pass

class AssignmentOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        return table.setter(self.children[0].value, self.children[1].evaluate(table))

class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        print(self.children[0].evaluate(table))

class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        return table.getter(self.value)

class BlockOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        for node in self.children:
            node.evaluate(table)

class ScanfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, table):
        return int(input())

class ForOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, table):
        self.children[0].evaluate(table)
        while(self.children[1].evaluate(table)):
            self.children[3].evaluate(table)
            self.children[2].evaluate(table)

class IfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, table):
        if self.children[0].evaluate(table):
            self.children[1].evaluate(table)
        else:
            if(len(self.children)>2):
                self.children[2].evaluate(table)