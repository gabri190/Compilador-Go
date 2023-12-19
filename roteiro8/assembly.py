class Assembly:
    @staticmethod
    def startText():
        with open('teste1.asm', 'w', encoding='utf-8') as f:
            for line in open('start.txt', encoding='utf-8'):
                f.write(line)
    
    @staticmethod
    def writeText(text):
        with open("teste1.asm", "a", encoding='utf-8') as f:
            if not text.endswith("\n"): 
                text += "\n"  
            f.write(text)
            
    @staticmethod
    def endText():
        with open('teste1.asm', 'a', encoding='utf-8') as f:
            for line in open('end.txt', encoding='utf-8'):
                f.write(line)