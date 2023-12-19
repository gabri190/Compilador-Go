from sys import argv
import sys
import re
from abc import ABC, abstractmethod
import argparse


class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = self.selectNext()
    def selectNext(self):
        num = ''
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position += 1
        if self.position >= len(self.source):
            new_token = Token("EOF", "")
        elif self.source[self.position].isdigit():
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            new_token = Token('INT', int(num))
        elif self.source[self.position] == '-':
            new_token = Token('MINUS', '-')
            self.position += 1
        elif self.source[self.position] == '+':
            new_token = Token('PLUS', '+')
            self.position += 1
        elif self.source[self.position] == '*':
            new_token = Token('MULTI', '*')
            self.position += 1
        elif self.source[self.position] == '/':
            new_token = Token('DIV', '/')
            self.position += 1
        elif(self.source[self.position] == '('):
            new_token = Token('LPAREN', '(')
            self.position += 1
        elif(self.source[self.position] == ')'):
            new_token = Token('RPAREN', ')')
            self.position += 1
        else:
            raise ValueError("Unknown character encountered")
        self.next = new_token
        return new_token

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.next = self.tokenizer.next

    def parseFactor(self):
        if self.next.type == 'INT':
            result = IntVal(self.next.value)
            self.next = self.tokenizer.selectNext()
            return result
        elif self.next.type in ('PLUS', 'MINUS'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            factor = self.parseFactor()
            if operator == 'PLUS':
                return factor
            else:
                return UnOp('-', factor)
        elif self.next.type == 'LPAREN':
            self.next = self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.next.type == 'RPAREN':
                self.next = self.tokenizer.selectNext()
                return result
            else:
                raise ValueError("Esperado fechamento de parênteses")
        else:
            raise ValueError("ValueError exception thrown")

    def parseTerm(self):
        result = self.parseFactor()
        while self.next.type in ('MULTI', 'DIV'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            factor = self.parseFactor()
            if operator == 'MULTI':
                result = BinOp(result, '*', factor)
            else:
                result = BinOp(result, '/', factor)
        return result

    def parseExpression(self):
        result = self.parseTerm()
        while self.next.type in ('PLUS', 'MINUS'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            term = self.parseTerm()
            if operator == 'PLUS':
                result = BinOp(result, '+', term)
            else:
                result = BinOp(result, '-', term)
        return result

    def run(self):
        result = self.parseExpression()
        if self.next.type == 'EOF':
            return result
        else:
            raise ValueError("ValueError exception thrown")

# class PrePro:
#     def filter(code):
#         return re.sub(r"\/\*(.*?)\*\/", "", code)
class PrePro:
    @staticmethod
    def filter(code):
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        code = re.sub(r"//.*?$", "", code, flags=re.MULTILINE)
        return code

class Node(ABC):
    def __init__(self):
        self.value = None
        self.children = []

    @abstractmethod
    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def Evaluate(self):
        if self.operator == '+':
            return self.left.Evaluate() + self.right.Evaluate()
        elif self.operator == '-':
            return self.left.Evaluate() - self.right.Evaluate()
        elif self.operator == '*':
            return self.left.Evaluate() * self.right.Evaluate()
        elif self.operator == '/':
            return self.left.Evaluate() // self.right.Evaluate()
        else:
            raise ValueError("Operador inválido")

class UnOp(Node):
    def __init__(self, operator, operand):
        super().__init__()
        self.operator = operator
        self.operand = operand

    def Evaluate(self):
        if self.operator == '-':
            return -self.operand.Evaluate()
        else:
            raise ValueError("Operador unário inválido")

class IntVal(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        return None  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analisador de Expressões Matemáticas')
    parser.add_argument('arquivo_go', help='arquivo.go')
    args = parser.parse_args()
    with open(args.arquivo_go, 'r') as file:
            for line in file:
                filtered_code = PrePro.filter(line.strip())  
                tokenizer = Tokenizer(filtered_code)
                parser = Parser(tokenizer)
                root = parser.run()  
                result = root.Evaluate()
                print(result)
    