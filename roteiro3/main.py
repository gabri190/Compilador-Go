from sys import argv

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
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.next = self.tokenizer.next

    def parseFactor(self):
        if self.next.type == 'INT':
            result = self.next.value
            self.next = self.tokenizer.selectNext()
            return result
        elif self.next.type in ('PLUS', 'MINUS'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            factor = self.parseFactor()
            if operator == 'PLUS':
                return factor
            else:
                return -factor
        elif self.next.type == 'LPAREN':
            self.next = self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.next.type == 'RPAREN':
                self.next = self.tokenizer.selectNext()
                return result
            else:
                raise ValueError("Esperado fechamento de parenteses")
        else:
            raise ValueError("ValueError exception thrown")

    def parseTerm(self):
        result = self.parseFactor()
        while self.next.type in ('MULTI', 'DIV'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            factor = self.parseFactor()
            if operator == 'MULTI':
                result *= factor
            else:
                result //= factor
        return result

    def parseExpression(self):
        result = self.parseTerm()
        while self.next.type in ('PLUS', 'MINUS'):
            operator = self.next.type
            self.next = self.tokenizer.selectNext()
            term = self.parseTerm()
            if operator == 'PLUS':
                result += term
            else:
                result -= term
        return result

    def run(self):
        result = self.parseExpression()
        if self.next.type == 'EOF':
            return result
        else:
            raise ValueError("ValueError exception thrown")

if __name__ == '__main__':
    code = argv[1]
    tokenizer = Tokenizer(code)
    parser = Parser(tokenizer)
    result = parser.run()
    print(result)