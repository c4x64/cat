import sys
import struct
import os

def parse_string(line, line_num):
    if not line.endswith('"') or len(line) < 2:
        print(f'ERROR: Unterminated string literal at line {line_num}', file=sys.stderr)
        sys.exit(1)
    content = line[1:len(line)-1]
    res = []
    i = 0
    while i < len(content):
        c = content[i]
        if c == '\\':
            if i + 1 >= len(content):
                print(f'ERROR: Invalid escape sequence "\\" in string at line {line_num}', file=sys.stderr)
                sys.exit(1)
            nxt = content[i+1]
            if nxt == 'n':
                res.append(0x0A)
                i = i + 2
            elif nxt == 't':
                res.append(0x09)
                i = i + 2
            elif nxt == 'r':
                res.append(0x0D)
                i = i + 2
            elif nxt == '\\':
                res.append(0x5C)
                i = i + 2
            elif nxt == '"':
                res.append(0x22)
                i = i + 2
            elif nxt == '0':
                res.append(0x00)
                i = i + 2
            elif nxt == 'x':
                if i + 3 >= len(content):
                    print(f'ERROR: Invalid escape sequence "\\x" in string at line {line_num}', file=sys.stderr)
                    sys.exit(1)
                hx = content[i+2:i+4]
                try:
                    res.append(int(hx, 16))
                except ValueError:
                    print(f'ERROR: Invalid escape sequence "\\x{hx}" in string at line {line_num}', file=sys.stderr)
                    sys.exit(1)
                i = i + 4
            else:
                print(f'ERROR: Invalid escape sequence "\\{nxt}" in string at line {line_num}', file=sys.stderr)
                sys.exit(1)
        else:
            res.extend(c.encode('utf-8'))
            i = i + 1
    return res

def main():
    if len(sys.argv) < 2:
        print("cL Assembler v1.0.0\nUsage: python clc.py <input.cl> [-o <output>]\n\ncL is raw machine code with labels.\nIt is the foundation of the CAT language ecosystem.")
        sys.exit(0)
    input_file = sys.argv[1]
    output_file = "a.out"
    if len(sys.argv) >= 4 and sys.argv[2] == "-o":
        output_file = sys.argv[3]
    if not os.path.exists(input_file):
        print(f'ERROR: Input file "{input_file}" not found', file=sys.stderr)
        sys.exit(1)
        
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    offset: int = 0
    labels = {}
    label_lines = {}
    
    # Pass 1: Scan
    for line_idx, raw_line in enumerate(lines):
        line_num = line_idx + 1
        line = raw_line.split('#', 1)[0].strip()
        if not line: continue
        
        if line.startswith(':'):
            name = line[1:].strip()
            if not name:
                print(f'ERROR: Empty label name at line {line_num}', file=sys.stderr)
                sys.exit(1)
            if name in labels:
                print(f'ERROR: Duplicate label "{name}" at line {line_num} (first defined at line {label_lines[name]})', file=sys.stderr)
                sys.exit(1)
            labels[name] = offset
            label_lines[name] = line_num
        elif line.startswith('"'):
            offset = offset + len(parse_string(line, line_num))  # type: ignore
        else:
            for token in line.split():
                if token.startswith('{'):
                    if not token.endswith('}'):
                        print(f'ERROR: Invalid reference "{token}" at line {line_num}', file=sys.stderr)
                        sys.exit(1)
                    offset = offset + 4  # type: ignore
                else:
                    try:
                        int(token, 16)
                        offset = offset + 1  # type: ignore
                    except ValueError:
                        print(f'ERROR: Invalid hex byte "{token}" at line {line_num}', file=sys.stderr)
                        sys.exit(1)
                        
    # Pass 2: Emit
    code = bytearray()
    for line_idx, raw_line in enumerate(lines):
        line_num = line_idx + 1
        line = raw_line.split('#', 1)[0].strip()
        if not line: continue
        if line.startswith(':'): continue
        if line.startswith('"'):
            code.extend(parse_string(line, line_num))
        else:
            for token in line.split():
                if token.startswith('{'):
                    name = token[1:len(token)-1]
                    if name not in labels:
                        print(f'ERROR: Undefined label "{name}" referenced at line {line_num}', file=sys.stderr)
                        sys.exit(1)
                    target = labels.get(name, 0) + 0x400078  # type: ignore
                    current = len(code) + 0x400078
                    code.extend(struct.pack('<i', target - (current + 4)))
                else:
                    code.append(int(token, 16))
                    
    # Write ELF
    entry = labels.get('_start', 0) + 0x400078  # type: ignore
    fsize = 0x78 + len(code)  # type: ignore
    
    ehdr = (
        b'\x7fELF' +
        b'\x02\x01\x01\x00' + b'\x00' * 8 +
        b'\x02\x00\x3E\x00' +
        b'\x01\x00\x00\x00' +
        struct.pack('<Q', entry) +
        struct.pack('<Q', 64) +
        struct.pack('<Q', 0) +
        struct.pack('<I', 0) + 
        struct.pack('<HHHHHH', 64, 56, 1, 0, 0, 0)
    )
    
    phdr = (
        struct.pack('<LL', 1, 5) +
        struct.pack('<Q', 0) +
        struct.pack('<Q', 0x400000) +
        struct.pack('<Q', 0x400000) +
        struct.pack('<Q', fsize) +
        struct.pack('<Q', fsize) +
        struct.pack('<Q', 4096)
    )
    
    with open(output_file, 'wb') as f:
        f.write(ehdr)
        f.write(phdr)
        f.write(code)
    os.chmod(output_file, 0o755)

if __name__ == '__main__':
    main()
