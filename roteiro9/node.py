type_value=["int","string"]

from functable import *
from symboltable import *

ft = FuncTable()

class Node:
    def __init__(self, value, children):
        self.value = value 
        self.children = children
        

    def evaluate(self, table):
        pass
    
class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        # Avaliando os nós filhos uma única vez e armazenando os resultados
        left_result = self.children[0].evaluate(table)
        right_result = self.children[1].evaluate(table)

        left_value, left_type = left_result[0], left_result[1]
        right_value, right_type = right_result[0], right_result[1]
        
        # print(right_type,left_type)
        # Operações Aritméticas
        if self.value in ['+', '-', '*', '/']:
            if left_type != type_value[0] or right_type != type_value[0]:
                raise ValueError("Erro: operações aritméticas requerem inteiros")
            if self.value == '+':
                return (left_value + right_value, type_value[0])
            elif self.value == '-':
                return (left_value - right_value, type_value[0])
            elif self.value == '*':
                return (left_value * right_value, type_value[0])
            elif self.value == '/':
                return (left_value // right_value, type_value[0])  # Divisão inteira

        # Operações Lógicas
        elif self.value in ['||', '&&']:
            if left_type != type_value[0] or right_type != type_value[0]:
                raise ValueError("Erro: operações lógicas requerem inteiros")
            if self.value == '||':
                return (int(left_value or right_value), type_value[0])
            elif self.value == '&&':
                return (int(left_value and right_value), type_value[0])

       # Operações de Comparação
        elif self.value in ['>', '<', '==']:
            if left_type != right_type:
                raise ValueError("Erro: tipos diferentes na comparação")
            if left_type not in type_value:
                raise ValueError(f"Erro: tipo '{left_type}' não suportado para comparação")
            if self.value == '>':
                return (int(left_value > right_value), type_value[0])
            elif self.value == '<':
                return (int(left_value < right_value), type_value[0])
            elif self.value == '==':
                return (int(left_value == right_value), type_value[0])

        # Concatenação
        elif self.value == '.':
            return (f'{str(left_value)}{str(right_value)}', type_value[1])
        else:
            raise ValueError(f"Operador desconhecido: {self.value}")


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
        return (self.value,type_value[0])
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
        super().__init__(value, children)
        if len(children) != 2:
            raise ValueError("AssignmentOp precisa de exatamente dois filhos.")
        
    def evaluate(self, table):
        identifier = self.children[0].value
        value_to_assign = self.children[1].evaluate(table)

        # Verifica se o identificador é válido antes de atribuir
        if not isinstance(identifier, str):
            raise TypeError("O identificador da atribuição deve ser uma string.")

        table.setter(identifier, value_to_assign)

class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        left_value = self.children[0].evaluate(table)[0]
        print(left_value)


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
            if isinstance(node,ReturnOp):
                return node.evaluate(table)
            node.evaluate(table)
class ScanfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        
        return (int(input()), type_value[0])


class ForOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, table):
        self.children[0].evaluate(table)
        while(self.children[1].evaluate(table)[0]):
            self.children[3].evaluate(table)
            self.children[2].evaluate(table)

class IfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, table):
        if self.children[0].evaluate(table):
            self.children[1].evaluate(table)
        elif(len(self.children)>2):
            self.children[2].evaluate(table)
class VarDec(Node):
    TYPE_INT = "int"
    TYPE_STRING = "string"

    def evaluate(self, table):
        variable_name = self.children[0].value
        default_value = 0 if self.value == self.TYPE_INT else ""

        if len(self.children) == 1:
            # Declaração de variável sem inicialização
            table.create(variable_name, (default_value, self.value))
        else:
            # Declaração de variável com inicialização
            _type = self.children[1].evaluate(table)
            if self.value != _type[1]:
                raise SyntaxError("Tipo errado na atribuição.")
            table.create(variable_name, (_type[0], self.value))

class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, table):
        
        function_name = self.children[0]
        child=function_name.children[0].value

        ft.setter(child, (self,function_name.value))


class ReturnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        return self.children[0].evaluate(table)

class FuncCall(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children  

    def evaluate(self, table):
        func_obj = ft.getter(self.value)
        if len(func_obj[0].children) != len(self.children)+2:
            raise Exception("Number of arguments from function declaration and function call differ")
        local_st = SymbolTable()
       
        for i in range(len(self.children)):
            func_obj[0].children[i+1].evaluate(local_st)
            
            local_st.setter(func_obj[0].children[i+1].children[0].value,self.children[i].evaluate(table))
        
        result= func_obj[0].children[-1].evaluate(local_st)
                
        if result is not None:
            if func_obj[1]!=result[1]:
                raise SyntaxError('Tipo de função errado')
            else:
                return result    