import sys
def solve(expr):
    termos = expr.replace(" ","").split("+")
    lista_ints = []
    if ("+" or "-") not in expr:
            return sys.stderr.write("erro")
    else:
        for termo in termos:
            if '-' in termo:
                sublist = termo.split('-')
                resultado = int(sublist[0]) - sum(map(int, sublist[1:]))
                lista_ints.append(resultado)
            else:
                lista_ints.append(int(termo))
            
        return sum(lista_ints)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python nome_do_arquivo.py '<expressao>'")
        sys.exit(1)
    expression=sys.argv[1]
    resultado = solve(expression)

    print(resultado)
    