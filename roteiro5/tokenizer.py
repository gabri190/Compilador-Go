reserved = ['Println']
PRINTLN = reserved

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
        word=''
        
       #Espacos
        
        while self.position < len(self.source) and (self.source[self.position].isspace() or self.source[self.position]=="\n"):
            self.position += 1
        
        #EOF
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return self.next
        
            # if self.position >= len(self.source):
            #     self.next = Token("EOF", "")
            #     return self.next
        #Digitos
        if self.source[self.position].isdigit():
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token('INT', int(num))
        #Identificador ou println
        elif self.source[self.position].isalpha():
            word += self.source[self.position]
            self.position += 1
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position]=="_"):
                word += self.source[self.position]
                self.position += 1

            if word in reserved:
                self.next = Token(word, word)
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
        elif self.source[self.position] == '=':
            self.next = Token("ASSIGN", "=")
            self.position+=1
        elif self.source[self.position] == '\n':
            self.next = Token("NEWLINE", "\n")
            self.position+=1
        else:
            raise ValueError("Unknown character encountered")
        
        return self.next