from parser_file import Parser
import sys
if __name__ == '__main__':
    arquivo_go = sys.argv[1] 
    with open(arquivo_go, 'r') as file:
        code = file.read()
        result = Parser.run(code)