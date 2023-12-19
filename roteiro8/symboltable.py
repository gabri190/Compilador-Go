class SymbolTable:
    def __init__(self):
        self.dic_var = {}
        self.shift = 4

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError(f"Erro: variável não existente {var}")

    def setter(self, var, val, _type):
        if var in self.dic_var and self.dic_var[var][1] != _type:
            raise ValueError(f"Erro: Tipo de variável '{var}' não compatível.")
        pos=self.dic_var[var][2]
        self.dic_var[var] = (val, _type,pos)

    def create(self, var, val, _type=None):
        if var in self.dic_var:
            raise ValueError(f"Variável '{var}' já existe.")
        else:
            self.dic_var[var] = (val, _type, self.shift)
            self.shift += 4

    def pos(self, var):
        return self.dic_var[var][2]