class SymbolTable:
    def __init__(self):
        self.dic_var = {}

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError(f"Erro: variável não existente {var}")

    def setter(self, var, val, _type):
        # print(self.dic_var[var][0])
        # if _type != self.dic_var[var][0]:
        #     raise NameError(f"Erro: tipo errado")
        self.dic_var[var] = (val, _type)

    def create(self, var, val=None, _type=None):
        if var in self.dic_var:
            raise ValueError(f"Variável '{var}' já existe.")
        else:
            self.dic_var[var] = (val, _type)