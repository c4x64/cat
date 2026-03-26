import sys, os, struct
from typing import Dict

def parse_string(line: str) -> bytearray:
    s: str = line.split('"')[1]
    b = bytearray()
    i: int = 0
    while i < len(s):
        if s[i] == '\\' and i+1 < len(s):
            if s[i+1] == 'n': b.append(10)
            elif s[i+1] == 't': b.append(9)
            elif s[i+1] == 'r': b.append(13)
            elif s[i+1] == '\\': b.append(92)
            elif s[i+1] == 'x':
                b.append(int(s[i+2:i+4], 16))  # type: ignore
                i = i + 2
            i = i + 2
        else:
            b.extend(s[i].encode('utf-8'))
            i = i + 1
    return b

def assemble(inf: str, outf: str) -> None:
    with open(inf, 'r', encoding='utf-8') as f: lines = f.readlines()
    
    labels: Dict[str, int] = {}
    offset: int = 0
    for l in lines:
        l = l.split('#')[0].strip()
        if not l: continue
        if l.startswith(':'): labels[l[1:]] = offset  # type: ignore
        elif l.startswith('"'): offset = offset + len(parse_string(l))  # type: ignore
        else:
            for t in l.split(): offset = offset + (4 if t.startswith('{') else 1)  # type: ignore
            
    out = bytearray()
    offset = 0x400078
    for l in lines:
        l = l.split('#')[0].strip()
        if not l or l.startswith(':'): continue
        if l.startswith('"'):
            db = parse_string(l)
            out.extend(db)
            offset = offset + len(db)  # type: ignore
        else:
            for t in l.split():
                if t.startswith('{'):
                    lbl = t[1:-1]  # type: ignore
                    if lbl not in labels: raise Exception(f"Undefined: {lbl}")
                    target = labels.get(lbl, 0) + 0x400078  # type: ignore
                    out.extend(struct.pack('<i', target - (offset + 4)))
                    offset = offset + 4  # type: ignore
                else:
                    out.append(int(t, 16))
                    offset = offset + 1  # type: ignore
                    
    with open(outf, 'wb') as f:
        sz: int = len(out) + 0x78
        ep: int = labels.get('_start', 0) + 0x400078  # type: ignore
        ehdr = (b'\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                b'\x02\x00\x3e\x00\x01\x00\x00\x00' + struct.pack('<q', ep) +
                b'\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                b'\x00\x00\x00\x00\x40\x00\x38\x00\x01\x00\x00\x00\x00\x00\x00\x00')
        phdr = (b'\x01\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                b'\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00' +
                struct.pack('<q', sz) + struct.pack('<q', sz) + b'\x00\x10\x00\x00\x00\x00\x00\x00')
        f.write(ehdr + phdr + out)
    os.chmod(outf, 0o755)

assemble(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 else "a.out")
