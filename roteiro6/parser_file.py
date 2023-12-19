import os
from node import *
from tokenizer import *
from filter import PrePro
from symboltable import SymbolTable

class Parser:
    tokenizer:Tokenizer
    
    @staticmethod
    def parseFactor():
        tokens=Parser.tokenizer
        if tokens.next.type == 'INT':
            result = IntVal(tokens.next.value, [])
            tokens.selectNext()
            return result
        elif tokens.next.type in ('PLUS', 'MINUS','NOT'):
            operator = tokens.next.type
            tokens.selectNext()
            factor = Parser.parseFactor()
            if operator == 'PLUS':
                return UnOp('+', [factor])
            elif operator == 'MINUS':
                return UnOp('-', [factor])
            elif operator=='NOT':
                return UnOp('!',[factor])
        elif tokens.next.type == 'LPAREN':
            tokens.selectNext()
            result = Parser.boolexpression()
            if tokens.next.type != 'RPAREN':
                raise ValueError("Esperado fechamento de parênteses")
            tokens.selectNext()
            return result
        elif tokens.next.type == 'Scanln':
            tokens.selectNext()
            if tokens.next.type == 'LPAREN':
                tokens.selectNext()
                if tokens.next.type != 'RPAREN':
                    raise ValueError("Esperado ) apos PRINT factor")
                tokens.selectNext()
            return ScanfOp("Scanln",[])
        elif tokens.next.type == 'IDENTIFIER':
            result = IdentifierOp(tokens.next.value, [])
            tokens.selectNext()
            return result
        else:
            raise ValueError("ValueError exception thrown")
    @staticmethod
    def boolexpression():
        tokens=Parser.tokenizer
        result=Parser.boolTerm()
        while tokens.next.type in ('OR'):
            operator=tokens.next.type
            tokens.selectNext()
            bterm=Parser.boolTerm()
            if operator =='OR':
                result=BinOp('|',[result,bterm])
        return result

    @staticmethod
    def boolTerm():
        tokens=Parser.tokenizer
        result=Parser.relExpression()
        while tokens.next.type in ('AND'):
            operator=tokens.next.type
            tokens.selectNext()
            rexpression=Parser.relExpression()
            if operator =='AND':
                result=BinOp('&',[result,rexpression])
        return result
    
    @staticmethod
    def relExpression():
        tokens=Parser.tokenizer
        result = Parser.parseExpression()
        while tokens.next.type in ('EQUAL', 'GREATER','LESS'):
            operator = tokens.next.type
            tokens.selectNext()
            expression = Parser.parseExpression()
            if operator == 'EQUAL':
                result = BinOp('=', [result, expression])
            elif operator=='GREATER':
                result = BinOp('>', [result, expression])
            elif operator=='LESS':
                result=BinOp('<', [result, expression])
        return result


    @staticmethod
    def parseTerm():
        tokens=Parser.tokenizer
        result = Parser.parseFactor()
        while tokens.next.type in ('MULTI', 'DIV'):
            operator = tokens.next.type
            tokens.selectNext()
            factor = Parser.parseFactor()
            if operator == 'MULTI':
                result = BinOp('*', [result, factor])
            else:
                result = BinOp('/', [result, factor])
        return result

    @staticmethod
    def parseExpression():
        tokens=Parser.tokenizer
        result = Parser.parseTerm()

        while tokens.next.type in ('PLUS', 'MINUS'):
            operator = tokens.next.type
            tokens.selectNext()
            term = Parser.parseTerm()
            if operator == 'PLUS':
                result = BinOp('+', [result, term])
            else:
                result = BinOp('-', [result, term])
        return result

    @staticmethod
    def parseAssignment():
        tokens = Parser.tokenizer
        if tokens.next.type == 'IDENTIFIER':
            identifier = IdentifierOp(tokens.next.value, [])
            tokens.selectNext()
            if tokens.next.type != 'ASSIGN':
                raise ValueError('erro assign')
            tokens.selectNext()
            expression = Parser.boolexpression()
        return AssignmentOp("=", [identifier, expression])
        
    @staticmethod
    def parseBlock():
        tokens = Parser.tokenizer
        statements=[]
        if tokens.next.type != 'OPENK':
            raise ValueError(f"erro openk {tokens.next.type}")
        tokens.selectNext()
        
        if tokens.next.type != 'NEWLINE':
            raise ValueError(f"erro newline {tokens.next.type}")
        tokens.selectNext()
        
        while tokens.next.type != 'CLOSEK':
            statement = Parser.parseStatement()
            statements.append(statement)
           
        tokens.selectNext()
        
        return BlockOp(None, statements)

        
    @staticmethod
    def parseProgram():
        tokens=Parser.tokenizer
        statements = []
        while tokens.next.type != 'EOF':
            statements.append(Parser.parseStatement())
        # tokens.selectNext()
        return BlockOp("Block", statements)

    @staticmethod
    def parseStatement():
        tokens=Parser.tokenizer
        statment=NoOp(0,[])
        
        if tokens.next.type == 'IDENTIFIER':
            identifier = IdentifierOp(tokens.next.value, [])
            tokens.selectNext()
            if tokens.next.type != 'ASSIGN':
                raise ValueError('erro assign')
            tokens.selectNext()
            expression = Parser.boolexpression()
            statment= AssignmentOp("=", [identifier, expression])
        
        elif tokens.next.type == 'Println':
            tokens.selectNext()
            if tokens.next.type != 'LPAREN':
                raise ValueError("erro LPAREN")
            tokens.selectNext()
            expression = Parser.boolexpression()
            if tokens.next.type != 'RPAREN':
                raise ValueError("Esperado ) após PRINT statement")
            tokens.selectNext()
            statment= PrintOp("Println", [expression])
        
        elif tokens.next.type == 'if':
            tokens.selectNext()
            cond=Parser.boolexpression()
            blk=Parser.parseBlock()
            if tokens.next.type=='else':
                tokens.selectNext()
                statment= IfOp("else",[cond,blk,Parser.parseBlock()])
            else:
                statment= IfOp("if",[cond,blk])
            
        elif tokens.next.type=='for':
            tokens.selectNext()
            assign=Parser.parseAssignment()
            if tokens.next.type=='ENDC':
                tokens.selectNext()
                expression=Parser.boolexpression()
                if tokens.next.type=='ENDC':
                    tokens.selectNext()
            statment= ForOp("value",[assign,expression,
                                    Parser.parseAssignment(),
                                    Parser.parseBlock()])     

        if tokens.next.type != "NEWLINE":
            raise ValueError(f"erro newline,{tokens.next.type}")
        tokens.selectNext()
        return statment
        
    @staticmethod
    def run(code):
        filtered_code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(filtered_code)
        root = Parser.parseProgram()
        table = SymbolTable()
        result = root.evaluate(table)
        return result