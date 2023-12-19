from sys import argv
import re
import argparse
from node import *
from tokenizer import *

class PrePro:
    @staticmethod
    def filter(code):
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        code = re.sub(r"//.*?$", "", code, flags=re.MULTILINE)
        return code

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.next = self.tokenizer.next
    
    def parseFactor(self):
        if self.next.type == 'INT':
            result = IntVal(self.next.value,[])
            self.next = self.tokenizer.selectNext()
            return result
        elif self.next.type in ('PLUS', 'MINUS'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            factor = self.parseFactor()
            if operator == 'PLUS':
                return UnOp('+',[factor])
            else:
                return UnOp('-', [factor])
        elif self.next.type == 'LPAREN':
            self.next = self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.next.type != 'RPAREN':
                raise ValueError("Esperado fechamento de parênteses")
            self.next = self.tokenizer.selectNext()
            return result    
            
        elif self.next.type=='IDENTIFIER':
            result=IdentifierOp(self.next.value,[])
            self.next=self.tokenizer.selectNext()
            return result
        else:
            raise ValueError("ValueError exception thrown")
    def parseTerm(self):
        result = self.parseFactor()
        while self.next.type in ('MULTI', 'DIV'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            factor = self.parseFactor()
            if operator == 'MULTI':
                result = BinOp( '*',[result,factor])
            else:
                result = BinOp('/',[result,factor])
        return result
    
    def parseExpression(self):
        result = self.parseTerm()

        while self.next.type in ('PLUS', 'MINUS'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            term = self.parseTerm()
            if operator == 'PLUS':
                result = BinOp('+',[result,term])
            else:
                result = BinOp('-', [result,term])
        return result
    
    def parseBlock(self):
        parse_list = []
        while self.next.type!='EOF':
            parse_list.append(self.parseStatement())
        
        # self.next=self.tokenizer.selectNext()    
        return BlockOp("Block", parse_list)
    
    def parseStatement(self):
        
        if self.next.type == 'IDENTIFIER':
            identifier = IdentifierOp(self.next.value,[])
            self.next = self.tokenizer.selectNext()
            if self.next.type != 'ASSIGN':
                raise ValueError('erro assign')
            self.next = self.tokenizer.selectNext()
            expression = self.parseExpression()
            return AssignmentOp("=",[identifier,expression])
                        
        elif self.next.type == 'Println':
            self.next = self.tokenizer.selectNext()  
            if self.next.type == 'LPAREN':
                self.next = self.tokenizer.selectNext()  
                expression = self.parseExpression()
                if self.next.type != 'RPAREN':
                    raise ValueError("Esperado fechamento de parênteses após expressão do PRINT")
                self.next = self.tokenizer.selectNext()  
            return PrintOp("Println", [expression])

        elif self.next.type=="NEWLINE" or self.next.type=="EOF" :
            return NoOp(0,[])
        else:
            raise ValueError('erro newline| parseStatement')
        
    def run(self):
        resultado = self.parseBlock()
        if self.next.type != "EOF":
            raise NameError('Erro: final da operação não encontrado')
        return resultado
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analisador de Expressões Matemáticas')
    parser.add_argument('arquivo_go', help='arquivo.go')
    args = parser.parse_args()
    table=SymbolTable()

    with open(args.arquivo_go, 'r') as file:
        code=file.read()    
        filtered_code = PrePro.filter(code)  
        tokenizer = Tokenizer(filtered_code)
        parser = Parser(tokenizer)
        root = parser.run()  

        result = root.Evaluate(table)