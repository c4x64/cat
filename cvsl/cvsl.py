import sys
import re

class CVSLCompiler:
    def __init__(self):
        self.vars = {}
        self.output = []
        self.label_count = 0
        self.stack = [] # (type, end_label, start_label_if_while)

    def gen_label(self, name):
        self.label_count += 1
        return f"_{name}_{self.label_count}"

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

            # 3. Control Flow: if/while
            if line.startswith("if ") or line.startswith("while "):
                is_while = line.startswith("while ")
                m = re.match(r'(if|while)\s+(v\d+|\w+)\s*(==|!=|<|>)\s*(v\d+|\w+|[0-9x]+):', line)
                if m:
                    _, v1, op, v2 = m.groups()
                    v1 = self.vars.get(v1, v1.replace("v", "R"))
                    v2 = self.vars.get(v2, v2.replace("v", "R"))
                    
                    start_lab = ""
                    if is_while:
                        start_lab = self.gen_label("while_start")
                        self.output.append(f"{start_lab}:")
                    
                    self.output.append(f"CMP {v1}, {v2}")
                    true_lab = self.gen_label("true")
                    end_lab = self.gen_label("end")
                    
                    if op == "==": self.output.append(f"JZ {true_lab}")
                    elif op == "!=": self.output.append(f"JNZ {true_lab}")
                    elif op == "<":  self.output.append(f"JL {true_lab}")
                    elif op == ">":  self.output.append(f"JG {true_lab}")
                    
                    self.output.append(f"JMP {end_lab}")
                    self.output.append(f"{true_lab}:")
                    self.stack.append(("while" if is_while else "if", end_lab, start_lab))
                continue

            if line == "endif" or line == "endwhile":
                type, end_lab, start_lab = self.stack.pop()
                if type == "while":
                    self.output.append(f"JMP {start_lab}")
                self.output.append(f"{end_lab}:")
                continue

            # 4. Instruction translation
            # Replace named variables with R-registers
            for var_name, reg_name in self.vars.items():
                line = re.sub(rf'\b{var_name}\b', reg_name, line)
            
            # Translate v0-v255 to R0-R255
            line = re.sub(r'\bv(\d+)\b', r'R\1', line)
            
            # Instruction refinement: mov R0, 10 -> movi R0, 10
            parts = re.split(r'[,\s]+', line)
            mnemonic = parts[0].upper()
            if mnemonic == "MOV" and len(parts) > 2:
                if re.match(r'^-?\d+$', parts[2]) or parts[2].startswith("0x"):
                    line = line.replace(parts[0], "MOVI")
            
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
