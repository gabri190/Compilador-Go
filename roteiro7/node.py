type_value=["int","string"]

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
        # Avaliando os nós filhos uma única vez e armazenando os resultados
        left_result = self.children[0].evaluate(table)
        right_result = self.children[1].evaluate(table)

        left_value, left_type = left_result[0], left_result[1]
        right_value, right_type = right_result[0], right_result[1]
        

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
        elif self.value in ['|', '&']:
            if left_type != type_value[0] or right_type != type_value[0]:
                raise ValueError("Erro: operações lógicas requerem inteiros")
            if self.value == '|':
                return (int(left_value or right_value), type_value[0])
            elif self.value == '&':
                return (int(left_value and right_value), type_value[0])

       # Operações de Comparação
        elif self.value in ['>', '<', '=']:
            if left_type != right_type:
                raise ValueError("Erro: tipos diferentes na comparação")
            if left_type not in type_value:
                raise ValueError(f"Erro: tipo '{left_type}' não suportado para comparação")
            if self.value == '>':
                return (int(left_value > right_value), type_value[0])
            elif self.value == '<':
                return (int(left_value < right_value), type_value[0])
            elif self.value == '=':
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
        self.value = value
        self.children = children

    def evaluate(self, table):
        result = self.children[1].evaluate(table)
        left_value = self.children[0].value
        right_value, _type = result[0], result[1]

        # Se o valor à direita for de Scanln e o tipo à esquerda for string, lançar um erro
        if isinstance(self.children[1], ScanfOp) and table.getter(left_value)[1] == "string":
            raise ValueError("Erro: Scanln() só pode ser usado com variáveis do tipo int.")

        return table.setter(left_value, right_value, _type)



class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        left_value=self.children[0].evaluate(table)[0]
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
            node.evaluate(table)

class ScanfOp(Node):
    def __init__(self, value, children, expected_type=None):
        self.value = value
        self.children = children
        self.expected_type = expected_type

    def evaluate(self, table):
        if self.expected_type and self.expected_type != "int":
            raise ValueError("Erro: Scanln() só pode ser usado com variáveis do tipo int.")
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
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        var_name = self.children[0].value
        
        if len(self.children) > 1:
            result = self.children[1].evaluate(table)
            val, _type = result[0], result[1]
            if _type != self.value:
                raise TypeError(f"Erro: tentando inicializar a variável '{var_name}' do tipo '{self.value}' com um valor do tipo '{_type}'")
            table.setter(var_name, val, _type)
        else:
            table.create(var_name, None, self.value)  # Modificamos esta linha para criar a variável sem um valor inicial.
