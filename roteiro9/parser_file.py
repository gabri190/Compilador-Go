import sys
import re 
from tokenizer import *
from node import *
from symboltable import *
from functable import *
from filter import  PrePro
class Parser:
    tokenizer = Tokenizer
    
    @staticmethod
    def parseProgram():
        tokens=Parser.tokenizer
        
        children = []
        while tokens.next.type != 'EOF':
            children.append(Parser.parseDeclaration())
        children_main = FuncCall("main", [])
        children.append(children_main)
        return BlockOp(None, children)
    
    @staticmethod
    def parseDeclaration():
        tokens = Parser.tokenizer
        result=NoOp(0,[])
        
        # while tokens.next.type=='NEWLINE':
        #     tokens.selectNext()
        
        if tokens.next.type != 'func':
            raise ValueError(f"Esperado 'func' como palavra-chave, recebido {tokens.next.type}")
        tokens.selectNext()        
        result=FuncDec(None,[])
        
        if tokens.next.type != 'IDENTIFIER':
            raise ValueError(f"Esperado 'IDENTIFIER' como palavra-chave, recebido {tokens.next.type}")
        func_name=IdentifierOp(tokens.next.value,[])
        tokens.selectNext()        
        
        if tokens.next.type!='LPAREN':
            raise ValueError(f"Esperado 'LPAREN' como palavra-chave, recebido {tokens.next.type}")
        tokens.selectNext()
        
        if tokens.next.type=='RPAREN':
            tokens.selectNext()
            if tokens.next.type!='type_value':
                raise ValueError(f'expected type but received {tokens.next.type}')
            func_type=tokens.next.value
            tokens.selectNext()
            block=Parser.parseBlock()
            
            var_name=VarDec(func_type,[func_name])
            result=FuncDec(None,[var_name,block])
        
        elif tokens.next.type=='IDENTIFIER':
            arg=IdentifierOp(tokens.next.value,[])
            tokens.selectNext()
            if tokens.next.type!='type_value':
                raise ValueError(f'expected type but received {tokens.next.type}')
            
            _type=tokens.next.value
            result.children.append(VarDec(_type,[arg]))
            tokens.selectNext()
            
            while tokens.next.type=='COMMA':
                tokens.selectNext()
                if tokens.next.type!='IDENTIFIER':
                    raise ValueError(f'expected IDENTIFIER but received {tokens.next.type}')
                arg=IdentifierOp(tokens.next.value,[])
                tokens.selectNext()
                
                if tokens.next.type!='type_value':
                    raise ValueError(f'expected type_value but received {tokens.next.type}')
                _type=tokens.next.value
                result.children.append(VarDec(_type,[arg]))
                tokens.selectNext()
            
            if tokens.next.type!='RPAREN':
                raise ValueError(f'expected RPAREN but received {tokens.next.type}')
            tokens.selectNext()
            
            if tokens.next.type!='type_value':
                raise ValueError(f'expected type_value but received {tokens.next.type}')
            func_type=tokens.next.value
            tokens.selectNext()
            block=Parser.parseBlock()
            
            result.children.append(block)
            
            var_name=VarDec(func_type,[func_name])
            result.children.insert(0,var_name)
        else:
            raise ValueError(f'expected either RPAREN or IDENTIFIER but received {tokens.next.type}')
        
        if tokens.next.type not in ('NEWLINE' ,'EOF') :
            raise ValueError(f'expected either NEWLINE but received {tokens.next.type}')
        tokens.selectNext()
        return result
    @staticmethod
    def parseBlock():
        tokens=Parser.tokenizer
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
    def parseAssignment():
        tokens=Parser.tokenizer
        args = []
        if tokens.next.type == 'IDENTIFIER':
            identi = IdentifierOp(tokens.next.value, [])
            tokens.selectNext()  
            
            if tokens.next.type == 'ASSIGN':
                tokens.selectNext()  
                result = AssignmentOp(None, [identi, Parser.parseBoolExpression()])
                if tokens.next.type == 'IDENTIFIER' or tokens.next.type == 'COMMA' or tokens.next.type == 'RPAREN':
                    raise SyntaxError("Erro: Assigment")
                return result
            elif tokens.next.type == 'LPAREN':
                tokens.selectNext()  
                
                if tokens.next.type != 'RPAREN':
                    arg = Parser.parseBoolExpression()
                    args.append(arg)
                    while tokens.next.type == 'COMMA':
                        tokens.selectNext()  
                        arg = Parser.parseBoolExpression()
                        args.append(arg)
                    
                    if tokens.next.type != 'RPAREN':
                        raise SyntaxError(f"Esperado {tokens.next.type}")
                    tokens.selectNext()  
                    return FuncCall(identi.value, args)
                    # else:
                    #     raise SyntaxError("Erro: fecha funccall")
                
                elif tokens.next.type == 'RPAREN':
                    tokens.selectNext()  
                    return FuncCall(identi.value, [])
                else:
                    raise SyntaxError(f"Esperado {tokens.next.type}")
            else:
                raise SyntaxError(f"Esperado {tokens.next.type}")
                    
            
    @staticmethod                
    def parseStatement():
        tokens = Parser.tokenizer
        result = NoOp(0,[])

        if tokens.next.type == 'IDENTIFIER':
            result = Parser.parseAssignment()
            # tokens.selectNext()

        elif tokens.next.type == 'Println':
            tokens.selectNext()
            if tokens.next.type != 'LPAREN':
                raise ValueError("erro LPAREN")
            tokens.selectNext()
            expression = Parser.parseBoolExpression()
            if tokens.next.type != 'RPAREN':
                raise ValueError(f"Esperado {tokens.next.type} após PRINT statement")
            tokens.selectNext()
            result= PrintOp("Println", [expression])

        elif tokens.next.type == 'if':
            tokens.selectNext()
            cond=Parser.parseBoolExpression()
            blk=Parser.parseBlock()
            if tokens.next.type=='else':
                tokens.selectNext()
                result= IfOp("else",[cond,blk,Parser.parseBlock()])
            else:
                result= IfOp("if",[cond,blk])
        elif tokens.next.type=='for':
            tokens.selectNext()
            assign=Parser.parseAssignment()
            if tokens.next.type!='ENDC':
                raise ValueError(f"erro endc {tokens.next.type}")
            tokens.selectNext()
            expression=Parser.parseBoolExpression()
            if tokens.next.type!='ENDC':
                raise ValueError(f"erro endc {tokens.next.type}")
            tokens.selectNext()
            result= ForOp("value",[assign,expression,
                                Parser.parseAssignment(),
                                Parser.parseBlock()])     

        elif tokens.next.type=='var':
            tokens.selectNext()
            if tokens.next.type!="IDENTIFIER":
                raise ValueError(f"erro iden, {tokens.next.type}")
            identificador=IdentifierOp(tokens.next.value,[])

            tokens.selectNext()
            
            if tokens.next.type !='type_value':
                raise ValueError(f"erro type, {tokens.next.type}")
            type_val=tokens.next.value

            tokens.selectNext()
            
            if tokens.next.type=='ASSIGN':

                tokens.selectNext()
                result= VarDec(type_val,[identificador,Parser.parseBoolExpression()])
            else:
                result= VarDec(type_val,[identificador])   
        
        elif tokens.next.type=='return':
            tokens.selectNext()
            expression=Parser.parseBoolExpression()
            result=ReturnOp('Retornar',[expression])

        # elif tokens.next.type in ('NEWLINE', 'EOF'):
        #     result = NoOp(None, None)

        # else:
        #     raise SyntaxError("Erro: Token não reconhecido")

        if tokens.next.type not in ('NEWLINE','EOF') :
            raise ValueError(f'expected NEWLINE but received {tokens.next.type}')
        tokens.selectNext()
        # print(tokens.next.type)

        return result

        
                
        
    @staticmethod
    def parseFactor():
        tokens=Parser.tokenizer
        if tokens.next.type == 'INT':
            result = tokens.next.value
            tokens.selectNext()  
            res = IntVal(result, [])
            return res
        
        elif tokens.next.type == 'STRING':
            result = tokens.next.value
            tokens.selectNext()  
            string = StrVal(result, [])
            return string
        
        elif tokens.next.type == 'IDENTIFIER':
            # args = []
            identifier = tokens.next.value
            identifier_node=IdentifierOp(identifier,[])
            tokens.selectNext()
            
            if tokens.next.type == 'LPAREN':
                res=FuncCall(identifier_node.value,[])
                tokens.selectNext()
                
                if tokens.next.type!='RPAREN':
                    arg=Parser.parseBoolExpression()
                    res.children.append(arg)
                    while tokens.next.type=='COMMA':
                        tokens.selectNext()
                        arg=Parser.parseBoolExpression()
                        res.children.append(arg)
                    
                    if tokens.next.type=='RPAREN':
                        tokens.selectNext()
                        result=res
                else:
                    tokens.selectNext()
                    result=res    
            else:
                result = identifier_node
            
            return result
    
        
        elif tokens.next.type == 'PLUS':
            tokens.selectNext()  
            return UnOp("+", [Parser.parseFactor()])
        
        elif tokens.next.type == 'MINUS':
            tokens.selectNext()  
            return UnOp("-", [Parser.parseFactor()])
        
        elif tokens.next.type == 'NOT':
            tokens.selectNext()  
            return UnOp("!", [Parser.parseFactor()])
        
        
        elif tokens.next.type == 'Scanln':
            tokens.selectNext()
            if tokens.next.type != 'LPAREN':
                raise ValueError(f"erro Lparen {tokens.next.type}")
            tokens.selectNext()
            if tokens.next.type != 'RPAREN':
                raise ValueError(f"Esperado {tokens.next.type} apos PRINT factor")
            tokens.selectNext()
            return ScanfOp("Scanln",[])
        
        elif tokens.next.type == 'LPAREN':
            tokens.selectNext()
            result = Parser.parseBoolExpression()
            if tokens.next.type != 'RPAREN':
                raise ValueError("Esperado fechamento de parênteses")
            tokens.selectNext()
            return result
        
        else:
            raise SyntaxError("Erro: Caractere inválido")
            
        
        
    @staticmethod
    def parseExpression():
        tokens=Parser.tokenizer
        result = Parser.parseTerm()
        #print(result.value)
        while tokens.next.type == 'PLUS' or tokens.next.type == 'MINUS' or tokens.next.type == 'CONCAT':
            op = Parser.tokenizer.next
            if op.type == 'PLUS':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseTerm()])
            elif op.type == 'MINUS':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseTerm()])

            elif op.type == 'CONCAT':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseTerm()])
                   
        return result
    
    
    @staticmethod
    def parseTerm():
        tokens=Parser.tokenizer
        result = Parser.parseFactor()
        #print(result)
        while tokens.next.type == 'MULTI' or tokens.next.type == 'DIV':
            op = Parser.tokenizer.next
            
            if op.type == 'MULTI':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseFactor()])
            elif op.type == 'DIV':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseFactor()])
                   
        return result
    @staticmethod
    def parseBoolExpression():
        tokens=Parser.tokenizer
        result = Parser.parseBoolTerm()
        #print(result)
        while tokens.next.type == 'OR':
            op = Parser.tokenizer.next
            tokens.selectNext()  
            result = BinOp(op.value, [result, Parser.parseBoolTerm()])
                   
        return result
    @staticmethod
    def parseBoolTerm():
        tokens=Parser.tokenizer
        result = Parser.parseRelExpression()
        #print(result)
        while tokens.next.type == 'AND':
            op = Parser.tokenizer.next
            tokens.selectNext()  
            result = BinOp(op.value, [result, Parser.parseRelExpression()])
                   
        return result
    
    @staticmethod
    def parseRelExpression():
        tokens=Parser.tokenizer
        result = Parser.parseExpression()
        #print(result)
        while tokens.next.type == 'EQUAL' or tokens.next.type == 'GREATER' or tokens.next.type == 'LESS':
            op = Parser.tokenizer.next
            
            if op.type == 'EQUAL':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseExpression()])
            elif op.type == 'GREATER':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseExpression()])
            elif op.type == 'LESS':
                tokens.selectNext()  
                result = BinOp(op.value, [result, Parser.parseExpression()])
                   
        return result
    @staticmethod
    def run(code):
        pre_processo = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(pre_processo)
        Parser.tokenizer.selectNext()
        result = Parser.parseProgram()
        if Parser.tokenizer.next.type != 'EOF':
            raise SyntaxError("EOF esperado, mas não encontrado")
        return result