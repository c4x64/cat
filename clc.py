import sys, os, struct

def parse_string(line):
    s = line.split('"')[1]
    b = bytearray()
    i = 0
    while i < len(s):
        if s[i] == '\\' and i+1 < len(s):
            if s[i+1] == 'n': b.append(10)
            elif s[i+1] == 't': b.append(9)
            elif s[i+1] == 'r': b.append(13)
            elif s[i+1] == '\\': b.append(92)
            elif s[i+1] == 'x':
                b.append(int(s[i+2:i+4], 16))
                i += 2
            i += 2
        else:
            b.extend(s[i].encode('utf-8'))
            i += 1
    return b

def assemble(inf, outf):
    with open(inf, 'r') as f: lines = f.readlines()
    
    labels = {}; offset = 0
    for l in lines:
        l = l.split('#')[0].strip()
        if not l: continue
        if l.startswith(':'): labels[l[1:]] = offset
        elif l.startswith('"'): offset += len(parse_string(l))
        else:
            for t in l.split(): offset += 4 if t.startswith('{') else 1
            
    out = bytearray(); offset = 0x400078
    for l in lines:
        l = l.split('#')[0].strip()
        if not l or l.startswith(':'): continue
        if l.startswith('"'):
            db = parse_string(l)
            out.extend(db); offset += len(db)
        else:
            for t in l.split():
                if t.startswith('{'):
                    lbl = t[1:-1]
                    if lbl not in labels: raise Exception(f"Undefined: {lbl}")
                    target = labels[lbl] + 0x400078
                    out.extend(struct.pack('<i', target - (offset + 4)))
                    offset += 4
                else:
                    out.append(int(t, 16))
                    offset += 1
                    
    with open(outf, 'wb') as f:
        sz = len(out) + 0x78
        ep = labels.get('_start', 0) + 0x400078
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
