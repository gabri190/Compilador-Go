import re
class PrePro:
    @staticmethod
    def filter(source):
        source = re.sub(r'\/\/[^\n]*', '', source) 
        source = re.sub(r'\/\*.*?\*\/', '', source, flags=re.DOTALL)  

        lines = source.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        
        filtered_source = '\n'.join(non_empty_lines)

        return filtered_source.strip()