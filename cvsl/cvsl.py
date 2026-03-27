import sys
import re

class CVSLCompiler:
    def __init__(self):
        self.vars = {}
        self.output = []

    def compile(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # 1. Variable mapping: var x = v10
            var_match = re.match(r'var\s+(\w+)\s*=\s*v(\d+)', line)
            if var_match:
                self.vars[var_match.group(1)] = f"R{var_match.group(2)}"
                continue
            
            # 2. Function start
            if line.startswith("func "):
                name = line.split()[1].rstrip(":")
                self.output.append(f"{name}:")
                continue
            
            if line == "endfunc":
                continue

            # 3. Instruction translation
            # Replace named variables with R-registers
            for var_name, reg_name in self.vars.items():
                line = re.sub(rf'\b{var_name}\b', reg_name, line)
            
            # Translate v0-v255 to R0-R255
            line = re.sub(r'\bv(\d+)\b', r'R\1', line)
            
            # 4. Instruction refinement: mov R0, 10 -> movi R0, 10
            parts = re.split(r'[,\s]+', line)
            mnemonic = parts[0].upper()
            if mnemonic == "MOV" and len(parts) > 2:
                if re.match(r'^-?\d+$', parts[2]) or parts[2].startswith("0x"):
                    line = line.replace(parts[0], "MOVI")
            
            # Map logical mnemonics if they differ
            # e.g. 'and' in cVSL -> 'AND' in CatArch (already matches)
            # but 'shl v0, v1, 2' -> 'SHLI R0, R1, 2'
            if mnemonic in ["SHL", "SHR", "AND", "OR", "XOR"] and len(parts) > 3:
                 if re.match(r'^-?\d+$', parts[3]) or parts[3].startswith("0x"):
                     line = line.replace(mnemonic, mnemonic + "I")

            self.output.append(line)
        
        return "\n".join(self.output)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cvsl.py input.cvsl output.casm")
        sys.exit(1)
    
    compiler = CVSLCompiler()
    result = compiler.compile(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(result)
    print(f"Compiled {sys.argv[1]} to {sys.argv[2]}")
