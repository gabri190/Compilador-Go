import sys
from parser_file import Parser
from symboltable import SymbolTable

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)

    arquivo = sys.argv[1]
    try:
        with open(arquivo, 'r') as file:
            conteudo = file.read() + '\n'

        parser = Parser()
        arvore = parser.run(conteudo)
        table = SymbolTable()
        arvore.evaluate(table)

        # Descomente as linhas abaixo para depuração, se necessário
        # print("Conteúdo do arquivo:")
        # print(repr(conteudo))
        # print("Tabela de Funções:")
        # print(FT.table)

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo}")

if __name__ == "__main__":
    main()