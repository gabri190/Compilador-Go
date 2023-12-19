class SymbolTable:
    def __init__(self):
        self.dic_var = {}

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError(f"Erro: variável não exitablee {var}")

    def setter(self, var, val):
        self.dic_var[var] = val