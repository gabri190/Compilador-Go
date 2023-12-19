class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, table):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        if self.value == '+':
            return self.children[0].Evaluate(table) + self.children[1].Evaluate(table)
        elif self.value == '-':
            return self.children[0].Evaluate(table) - self.children[1].Evaluate(table)
        elif self.value == '*':
            return self.children[0].Evaluate(table) * self.children[1].Evaluate(table)
        elif self.value == '/':
            return self.children[0].Evaluate(table) // self.children[1].Evaluate(table)

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        if self.value == '+':
            return self.children[0].Evaluate(table)
        elif self.value == '-':
            return -self.children[0].Evaluate(table)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        pass

class AssignmentOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return table.setter(self.children[0].value, self.children[1].Evaluate(table))

class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        print(self.children[0].Evaluate(table))

class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return table.getter(self.value)

class BlockOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        for node in self.children:
            node.Evaluate(table)

class SymbolTable:
    def __init__(self):
        self.dic_var = {}

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError("Erro: variável não exitablee")

    def setter(self, var, val):
        self.dic_var[var] = val