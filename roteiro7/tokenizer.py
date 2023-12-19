reserved = ['Println',"for", "if", "else", "Scanln","var"]
# PRINTLN = reserved
type_values=["string","int"]

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
        word=''
        
       #Espacos
        while self.position < len(self.source) and (self.source[self.position]==" " or self.source[self.position]=='\t'):
            self.position += 1
        
        #EOF
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return self.next
        
        #Digitos
        num = ''
        if self.source[self.position].isdigit():
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token('INT', int(num))
        #String
        elif self.source[self.position] == '"':
            self.position+=1
            while self.position<len(self.source) and (self.source[self.position] != '"'):
                num+=self.source[self.position]
                self.position+=1
            self.position+=1
            self.next = Token("STRING", num)
        #Identificador ou println
        elif self.source[self.position].isalpha():
            while self.position < len(self.source) and (self.source[self.position].isalpha() or 
                                                        self.source[self.position].isdigit() or 
                                                        self.source[self.position]=="_"):
                word += self.source[self.position]
                self.position += 1

            if word in reserved:
                self.next = Token(word, word)
            elif word in type_values:
                self.next=Token('type_value',word)
            else: 
                self.next = Token("IDENTIFIER", word)
       
        elif self.source[self.position] == '-':
            self.next = Token('MINUS', '-')
            self.position += 1
        elif self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            self.position += 1
        elif self.source[self.position] == '*':
            self.next = Token('MULTI', '*')
            self.position += 1
        elif self.source[self.position] == '/':
            self.next = Token('DIV', '/')
            self.position += 1
        elif(self.source[self.position] == '('):
            self.next = Token('LPAREN', '(')
            self.position += 1
        elif(self.source[self.position] == ')'):
            self.next = Token('RPAREN', ')')
            self.position += 1
        #diference between assign and equal
        elif self.source[self.position] == '=':
            # self.position+=1
            if self.source[self.position+1]=='=':
                self.next = Token("EQUAL", "==")
                self.position+=2
            else:
                self.next = Token("ASSIGN", "=")
                self.position+=1
            
        
        elif self.source[self.position] == '\n':
            self.next = Token("NEWLINE", "\n")
            self.position+=1
        elif self.source[self.position] == '|':
            self.next = Token("OR", "||")

            self.position+=2
        elif self.source[self.position] == '&':
            self.next = Token("AND", "&&")
            self.position+=2
        elif self.source[self.position] == '!':
            self.next = Token("NOT", "!")
            self.position+=1
        elif self.source[self.position] == '>':
            self.next = Token("GREATER", ">")
            self.position+=1
        elif self.source[self.position] == '<':
            self.next = Token("LESS", "<")
            self.position+=1
        elif self.source[self.position] == ';':
            self.next = Token("ENDC", ";")
            self.position+=1
        elif self.source[self.position] == '{':
            self.next = Token("OPENK", "{")
            self.position+=1
        elif self.source[self.position] == '}':
            self.next = Token("CLOSEK", "}")
            self.position+=1
        elif self.source[self.position] == '.':
            self.next = Token("CONCAT", ".")
            self.position+=1
        else:
            raise ValueError(f"Unknown character encountered {self.source[self.position]}")
        
        return self.next