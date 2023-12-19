class FuncTable:
    def __init__(self):
        self.table = {}

    def create(self,func_key):
        self.table[func_key]=None
        
    def getter(self, func_key):
        return self.table[func_key]
    
    def setter(self, func_key, func_value):
        self.table[func_key] = func_value