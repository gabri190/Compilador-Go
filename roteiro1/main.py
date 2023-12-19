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
        else:
            raise ValueError("Unknown character encountered")
        self.next = new_token
        return new_token

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.next = self.tokenizer.next

    def parseExpression(self):
        if self.next.type == 'INT':
            result = self.next.value
            self.next = self.tokenizer.selectNext()
            while self.next.type in ('PLUS', 'MINUS'):
                operator = self.next.type
                self.next = self.tokenizer.selectNext()
                if self.next.type == 'INT':
                    num = self.next.value
                    if operator == 'MINUS':
                        result -= num
                    else:
                        result += num
                    self.next = self.tokenizer.selectNext()
                else:
                    raise ValueError("ValueError exception thrown")
            if self.next.type == 'EOF':
                return result
            else:
                raise ValueError("ValueError exception thrown")
        else:
            raise ValueError("ValueError exception thrown")

    def run(self, code):
        tokenizer = Tokenizer(code)
        self.tokenizer = tokenizer
        self.next = self.tokenizer.next
        result = self.parseExpression()
        if self.next.type == 'EOF':
            return result
        else:
            raise ValueError("ValueError exception thrown")

entry = argv[1]
parser = Parser(Tokenizer(entry))
result = parser.run(entry)
print(result)