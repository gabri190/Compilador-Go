
reserved = ['Println',"for", "if", "else", "Scanln","var","func","return"]
# PRINTLN = reserved
type_values=["string","int"]
class Token:
    def __init__(self, token_type: str, token_value):
        self.type = token_type
        self.value = token_value

class Tokenizer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        
    
    
    def selectNext(self):
        #print((self.source))
        
        if self.position < len(self.source):
            next_token = self.source[self.position]
        
            #print(next_token)
            
            if next_token == '\n':
                self.next = Token('NEWLINE', '\n')
                self.position += 1
                
            elif next_token.isspace():
                self.position += 1
                self.selectNext()
                
            elif next_token == ",":
                self.next = Token('COMMA', ',') 
                self.position += 1 
                
            elif next_token.isalpha() or next_token == "_":
                identifier = ""
                while self.position < len(self.source) and (next_token.isalnum() or next_token == "_"):
                    identifier += next_token
                    self.position += 1
                    if self.position < len(self.source):
                        next_token = self.source[self.position]
                if identifier in reserved:
                    self.next=Token(identifier,identifier)
                
                elif identifier in type_values:
                    self.next=Token('type_value',identifier)
                else:
                    self.next = Token('IDENTIFIER', identifier)
                    
            elif next_token == '"':
                identifier = next_token
                self.position += 1
                next_token = self.source[self.position]

                while self.position < len(self.source) and next_token != '"':
                    identifier += next_token
                    self.position += 1
                    next_token = self.source[self.position]

                if next_token == '"':
                    identifier += next_token
                    self.position += 1
                    identifier = identifier.strip('"')
                    self.next = Token('STRING', identifier)
                else:
                    raise SyntaxError("String mal formada: aspa dupla de fechamento faltando")

            elif next_token.isdigit():
                value = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                self.next = Token('INT', int(value))
                
            elif next_token == "*":
                self.next = Token('MULTI', '*')
                self.position += 1

            elif next_token == "/":
                self.next = Token('DIV', '/') 
                self.position += 1

            elif next_token == "+":
                self.next = Token('PLUS', '+')
                self.position += 1

            elif next_token == "-":
                self.next = Token('MINUS', '-') 
                self.position += 1
                
            elif next_token == "(":
                self.next = Token('LPAREN', '(') 
                self.position += 1
            
            elif next_token == ")":
                self.next = Token('RPAREN', ')') 
                self.position += 1
                
            elif next_token == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token('EQUAL', '==')
                    self.position += 2
                else:
                    self.next = Token('ASSIGN', '=') 
                    self.position += 1
                
            elif next_token == ">":
                self.next = Token('GREATER', '>') 
                self.position += 1
                
            elif next_token == "<":
                self.next = Token('LESS', '<') 
                self.position += 1
                
            elif next_token == "|":
                self.next = Token('OR', '||') 
                self.position += 2
                
            elif next_token == "&":
                self.next = Token('AND', '&&') 
                self.position += 2
                
            elif next_token == "!":
                self.next = Token('NOT', '!') 
                self.position += 1
                
            elif next_token == "{":
                self.next = Token('OPENK', '{')
                self.position += 1
            
        
            elif next_token == "}":
                self.next = Token('CLOSEK', '}') 
                self.position += 1 
                
            elif next_token == ";":
                self.next = Token('ENDC', ';') 
                self.position += 1
            
            elif next_token == ".":
                self.next = Token('CONCAT', '.') 
                self.position += 1
                
     
            
            else:
                raise SyntaxError("Erro: Caractere inválido")

        else:
            self.next = Token('EOF', 'EOF')
            