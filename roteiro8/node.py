type_value=["int","string"]
from assembly import Assembly 
class Node:
    i=0
    def __init__(self):
        self.value = None
        self.children = []
        self.id = self.newId()

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i
    
    def evaluate(self, table):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        self.children[1].evaluate(table)
        Assembly().writeText("\tPUSH EAX")

        self.children[0].evaluate(table)
        Assembly().writeText("\tPOP EBX")

        # Operações Aritméticas
        if self.value in ['+', '-', '*', '/']:
            print("entrei")
            if self.value == '+':
                print("+")
                Assembly().writeText("\tADD EAX, EBX")
            elif self.value == '-':
                print("-")
                Assembly().writeText("\tSUB EAX, EBX")
            elif self.value == '*':
                print("*")
                Assembly().writeText("\tIMUL EBX")
            elif self.value == '/':
                print("/")
                Assembly().writeText("\tIDIV EBX")
       
        elif self.value in ['|', '&']:
            if self.value == '|':
                Assembly().writeText("\tOR EAX, EBX")
            elif self.value == '&':
                Assembly().writeText("\tAND EAX, EBX")
        
        # Operações de Comparação
        elif self.value in ['>', '<', '=']:
            if self.value == '>':
                Assembly().writeText("\tCMP EAX, EBX")
                Assembly().writeText("\tCALL binop_jg")
            elif self.value == '<':
                Assembly().writeText("\tCMP EAX, EBX")
                Assembly().writeText("\tCALL binop_jl")
            elif self.value == '=':
                Assembly().writeText("\tCMP EAX, EBX")
                Assembly().writeText("\tCALL binop_je")
        
        else:
            raise ValueError(f"Operador desconhecido: {self.value}")

        return None

        
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        left_value=self.children[0].evaluate(table)[0]
        
        if self.value == '+':
            return (left_value,type_value[0])
        elif self.value == '-':
            return (-left_value,type_value[0])
        elif self.value=='!':
            return (not left_value,type_value[0])

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        Assembly.writeText(f"\tMOV EAX, {self.value}\t\t")
        return None
class StrVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        return (self.value,type_value[1])
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
        left_value = self.children[0].value
        self.children[1].evaluate(table)


        identifier=table.getter(left_value)
        sp=identifier[2]
        Assembly.writeText(f"\tMOV [EBP-{sp}], EAX\t")



class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        self.children[0].evaluate(table)
        Assembly.writeText("\tPUSH EAX")
        Assembly.writeText("\tPUSH formatout")
        Assembly.writeText("\tCALL printf")
        Assembly.writeText("\tADD ESP, 8\n")

class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        var_info = table.getter(self.value)
        # pos=table.pos(self.value)
        var_offset = var_info[2]  
        Assembly().writeText(f"\tMOV EAX, [EBP-{var_offset}]\t") 

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
        print("scan")
        Assembly.writeText("\tPUSH scanint")
        Assembly.writeText("\tPUSH formatin")
        Assembly.writeText("\tcall scanf")
        Assembly.writeText("\tADD ESP, 8")
        Assembly.writeText("\tMOV EAX, DWORD [scanint]")    
        return (int(input()), type_value[0])


class ForOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = self.newId()
        
    def evaluate(self, table):
        self.children[0].evaluate(table)
        Assembly.writeText(f"\nLOOP_{self.id}:\t\t")
        self.children[1].evaluate(table)
        Assembly.writeText("\tCMP EAX, False")
        Assembly.writeText(f"\tJE EXIT_{self.id}")
        self.children[3].evaluate(table)
        self.children[2].evaluate(table)
        Assembly.writeText(f"\tJMP LOOP_{self.id}")
        Assembly.writeText(f"\nEXIT_{self.id}:\n")

class IfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = self.newId()
        
    def evaluate(self, table):
        Assembly.writeText("IF_{}:".format(self.id))
        self.children[0].evaluate(table)
        Assembly.writeText("\tCMP EAX, False")
        if len(self.children)>2:  
            Assembly.writeText("\tJE ELSE_{}".format(self.id))
            self.children[1].evaluate(table)
            Assembly.writeText("\tJMP EXIT_{}".format(self.id))
            Assembly.writeText("\tELSE_{}:".format(self.id))
            self.children[2].evaluate(table)
            Assembly.writeText("EXIT_{}:".format(self.id))
            
        else:                              
            Assembly.writeText("\tJE EXIT_{}".format(self.id))
            self.children[1].evaluate(table)
            Assembly.writeText("\tJMP EXIT_{}".format(self.id))
            Assembly.writeText("EXIT_{}:".format(self.id))
            
class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        print("jfneo")
        var_name = self.children[0].value
        
        Assembly.writeText("\tPUSH DWORD 0\t")
        table.create(var_name, None, self.value) 