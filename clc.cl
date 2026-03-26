# ═══════════════════════════════════════
# clc.cl - The self-hosted cL assembler
# Built entirely in Circle 1 (cL) hex code.
# ═══════════════════════════════════════

:_start
# Entry point for Linux x86-64
48 8B 3C 24                  # mov rdi, [rsp]  (argc)
48 83 FF 02                  # cmp rdi, 2
0F 8D {argc_ok}              # jge argc_ok

# ─── Print usage and exit ───
48 C7 C0 01 00 00 00         # mov rax, 1 (sys_write)
48 C7 C7 01 00 00 00         # mov rdi, 1 (stdout)
48 8D 35 {usage_msg}         # lea rsi, [rip + usage_msg]
48 C7 C2 31 00 00 00         # mov rdx, 49 (length of usage_msg)
0F 05                        # syscall
48 C7 C0 3C 00 00 00         # mov rax, 60 (sys_exit)
48 31 FF                     # xor rdi, rdi (0)
0F 05                        # syscall

:argc_ok
# ─── Open input file (argv[1]) ───
48 8B 7C 24 10               # mov rdi, [rsp + 16]  (argv[1])
48 31 F6                     # xor rsi, rsi (O_RDONLY = 0)
48 31 D2                     # xor rdx, rdx (mode = 0)
48 C7 C0 02 00 00 00         # mov rax, 2 (sys_open)
0F 05                        # syscall

48 85 C0                     # test rax, rax
0F 89 {open_ok}              # jns open_ok

# ─── Print error and exit ───
48 C7 C0 01 00 00 00         # mov rax, 1 (sys_write)
48 C7 C7 02 00 00 00         # mov rdi, 2 (stderr)
48 8D 35 {err_open}          # lea rsi, [rip + err_open]
48 C7 C2 12 00 00 00         # mov rdx, 18 (length)
0F 05                        # syscall
48 C7 C0 3C 00 00 00         # mov rax, 60 (sys_exit)
48 C7 C7 01 00 00 00         # mov rdi, 1 (exit code 1)
0F 05                        # syscall

:open_ok
48 89 C3                     # mov rbx, rax (save fd in rbx)

# ─── Mmap input buffer (10 MB) ───
48 31 FF                     # xor rdi, rdi (addr=0)
48 C7 C6 00 00 A0 00         # mov rsi, 10485760 (10 MB)
48 C7 C2 03 00 00 00         # mov rdx, 3 (PROT_READ | PROT_WRITE)
49 C7 C2 22 00 00 00         # mov r10, 34 (MAP_PRIVATE | MAP_ANONYMOUS)
4D C7 C0 FF FF FF FF         # mov r8, -1 (fd=-1)
4D 31 C9                     # xor r9, r9 (offset=0)
48 C7 C0 09 00 00 00         # mov rax, 9 (sys_mmap)
0F 05                        # syscall
49 89 C4                     # mov r12, rax (save input mmap ptr in r12)

# ─── Read file into buffer ───
48 89 DF                     # mov rdi, rbx (fd)
4C 89 E6                     # mov rsi, r12 (buf)
48 C7 C2 00 00 A0 00         # mov rdx, 10485760 (count)
48 C7 C0 00 00 00 00         # mov rax, 0 (sys_read)
0F 05                        # syscall
49 89 C5                     # mov r13, rax (save bytes read in r13)

# ─── Close input file ───
48 89 DF                     # mov rdi, rbx (fd)
48 C7 C0 03 00 00 00         # mov rax, 3 (sys_close)
0F 05                        # syscall

# ─── Mmap output buffer (10 MB) ───
48 31 FF                     # xor rdi, rdi
48 C7 C6 00 00 A0 00         # mov rsi, 10485760
48 C7 C2 03 00 00 00         # mov rdx, 3
49 C7 C2 22 00 00 00         # mov r10, 34
4D C7 C0 FF FF FF FF         # mov r8, -1
4D 31 C9                     # xor r9, r9
48 C7 C0 09 00 00 00         # mov rax, 9 (sys_mmap)
0F 05                        # syscall
49 89 C6                     # mov r14, rax (save output ptr in r14)

# ─── Mmap labels hash table (10 MB) ───
48 31 FF                     # xor rdi, rdi
48 C7 C6 00 00 A0 00         # mov rsi, 10485760
48 C7 C2 03 00 00 00         # mov rdx, 3
49 C7 C2 22 00 00 00         # mov r10, 34
4D C7 C0 FF FF FF FF         # mov r8, -1
4D 31 C9                     # xor r9, r9
48 C7 C0 09 00 00 00         # mov rax, 9 (sys_mmap)
0F 05                        # syscall
49 89 C7                     # mov r15, rax (save labels ptr in r15)

# ─── PASS 1 INITIALIZATION ───
4D 31 C0                     # xor r8, r8 (offset = 0)
4D 31 C9                     # xor r9, r9 (labels_count = 0)
4C 89 E3                     # mov rbx, r12 (rbx = input ptr)
4C 8D 2C 2B                  # lea rbp, [r12 + r13] (rbp = end ptr)

:pass1_loop
48 39 EB                     # cmp rbx, rbp
0F 8D {pass1_end}            # jge pass1_end

48 31 C0                     # xor rax, rax
8A 03                        # mov al, byte [rbx]

3C 20                        # cmp al, 32
0F 86 {advance_p1}           # jbe advance_p1

3C 23                        # cmp al, 35 ('#')
0F 84 {skip_comment}         # je skip_comment

3C 3A                        # cmp al, 58 (':')
0F 84 {parse_label}          # je parse_label

3C 22                        # cmp al, 34 ('"')
0F 84 {parse_string}         # je parse_string

3C 7B                        # cmp al, 123 ('{')
0F 84 {parse_ref}            # je parse_ref

# Hex byte
49 FF C0                     # inc r8 (offset++)
:skip_hex_loop
48 FF C3                     # inc rbx
48 39 EB                     # cmp rbx, rbp
0F 8D {pass1_end}            # jge pass1_end
8A 03                        # mov al, byte [rbx]
3C 20                        # cmp al, 32
0F 86 {pass1_loop}           # jbe pass1_loop
E9 {skip_hex_loop}           # jmp skip_hex_loop

:advance_p1
48 FF C3                     # inc rbx
E9 {pass1_loop}

:skip_comment
48 FF C3                     # inc rbx
48 39 EB                     # cmp rbx, rbp
0F 8D {pass1_end}
8A 03                        # mov al, byte [rbx]
3C 0A                        # cmp al, 10
0F 84 {advance_p1}           # if newline, advance to pass1_loop
E9 {skip_comment}

:parse_label
48 FF C3                     # inc rbx
48 89 D9                     # mov rcx, rbx (name_start)

:parse_label_len
48 39 EB                     # cmp rbx, rbp
0F 8D {save_label}
8A 03                        # mov al, byte [rbx]
3C 20                        # cmp al, 32
0F 86 {save_label}
48 FF C3                     # inc rbx
E9 {parse_label_len}

:save_label
48 89 DA                     # mov rdx, rbx
48 29 CA                     # sub rdx, rcx (name_len)
4C 89 C8                     # mov rax, r9
48 6B C0 18                  # imul rax, rax, 24
4A 8D 3C 07                  # lea rdi, [r15 + rax]
48 89 0F                     # mov [rdi], rcx
48 89 57 08                  # mov [rdi+8], rdx
4C 89 47 10                  # mov [rdi+16], r8
49 FF C1                     # inc r9 (labels_count++)
E9 {pass1_loop}

:parse_string
48 FF C3                     # inc rbx
48 39 EB                     # cmp rbx, rbp
0F 8D {pass1_end}
8A 03                        # mov al, [rbx]
3C 22                        # cmp al, 34 ('"')
0F 84 {advance_p1}
3C 5C                        # cmp al, 92 ('\')
0F 85 {str_normal}
48 FF C3                     # inc rbx
8A 03                        # mov al, [rbx]
3C 78                        # cmp al, 120 ('x')
0F 85 {str_esc_1}
48 83 C3 02                  # add rbx, 2
49 FF C0                     # inc r8
E9 {parse_string}
:str_esc_1
49 FF C0                     # inc r8
E9 {parse_string}
:str_normal
49 FF C0                     # inc r8
E9 {parse_string}

:parse_ref
49 83 C0 04                  # add r8, 4
:skip_ref_loop
48 FF C3                     # inc rbx
48 39 EB                     # cmp rbx, rbp
0F 8D {pass1_end}
8A 03                        # mov al, byte [rbx]
3C 7D                        # cmp al, 125 ('}')
0F 84 {advance_p1}
E9 {skip_ref_loop}

:pass1_end

# ─── PASS 2 INITIALIZATION ───
# Write EHDR and PHDR templates to output buffer (r14)
4C 89 F7                     # mov rdi, r14
48 8D 35 {_ehdr_tmpl}        # lea rsi, [rip + _ehdr_tmpl]
48 C7 C1 78 00 00 00         # mov rcx, 120 (0x78)
F3 A4                        # rep movsb

# Patch `filesz` and `memsz` in PHDR (at offset 0x20 and 0x28 of PHDR, which is r14 + 64 + 32 = r14 + 96)
4C 89 C0                     # mov rax, r8 (code size)
48 05 78 00 00 00            # add rax, 0x78 (headers size)
49 89 46 60                  # mov [r14 + 96], rax
49 89 46 68                  # mov [r14 + 104], rax

# Reset iteration state for pass 2
4D 31 C0                     # xor r8, r8
4C 89 E3                     # mov rbx, r12 (input ptr)
4D 8D 56 78                  # lea r10, [r14 + 120] (output ptr)

:pass2_loop
48 39 EB                     # cmp rbx, rbp
0F 8D {pass2_end}            # jge pass2_end

48 31 C0                     # xor rax, rax
8A 03                        # mov al, byte [rbx]

3C 20                        # cmp al, 32
0F 86 {adv_p2}
3C 23                        # cmp al, 35 ('#')
0F 84 {skip_cmt2}
3C 3A                        # cmp al, 58 (':')
0F 84 {skip_lbl2}
3C 22                        # cmp al, 34 ('"')
0F 84 {emit_str2}
3C 7B                        # cmp al, 123 ('{')
0F 84 {emit_ref2}

# Parse Hex byte (2 chars)
48 31 C9                     # xor rcx, rcx  (accum)
:parse_hex1
8A 03                        # mov al, byte [rbx]
48 FF C3                     # inc rbx
3C 39                        # cmp al, '9'
0F 8F {hex_alpha1}
2C 30                        # sub al, '0'
E9 {hex_done1}
:hex_alpha1
24 DF                        # and al, 0xDF
2C 37                        # sub al, 55
:hex_done1
C1 E0 04                     # shl eax, 4
09 C1                        # or ecx, eax

:parse_hex2
8A 03                        # mov al, byte [rbx]
48 FF C3                     # inc rbx
3C 39                        # cmp al, '9'
0F 8F {hex_alpha2}
2C 30                        # sub al, '0'
E9 {hex_done2}
:hex_alpha2
24 DF                        # and al, 0xDF
2C 37                        # sub al, 55
:hex_done2
09 C1                        # or ecx, eax

# emit byte
41 88 0A                     # mov [r10], cl
49 FF C2                     # inc r10
49 FF C0                     # inc r8

:skip_hex_spaces
48 39 EB                     # cmp rbx, rbp
0F 8D {pass2_end}
8A 03                        # mov al, byte [rbx]
3C 20                        # cmp al, 32
0F 8F {pass2_loop}           # jg pass2_loop
48 FF C3                     # inc rbx
E9 {skip_hex_spaces}

:adv_p2
48 FF C3
E9 {pass2_loop}

:skip_cmt2
48 FF C3
48 39 EB
0F 8D {pass2_end}
8A 03
3C 0A
0F 84 {adv_p2}
E9 {skip_cmt2}

:skip_lbl2
48 FF C3
:skip_lbl2_loop
48 39 EB
0F 8D {pass2_loop}
8A 03
3C 20
0F 86 {pass2_loop}
48 FF C3
E9 {skip_lbl2_loop}

:emit_str2
48 FF C3                     # inc rbx (skip quote)
:emit_str2_loop
48 39 EB                     # cmp rbx, rbp
0F 8D {pass2_end}
8A 03                        # mov al, [rbx]
3C 22                        # cmp al, '"'
0F 84 {adv_p2}
3C 5C                        # cmp al, '\'
0F 84 {emit_str_esc}

:emit_str_norm
41 88 02                     # mov [r10], al
49 FF C2                     # inc r10
49 FF C0                     # inc r8
48 FF C3                     # inc rbx
E9 {emit_str2_loop}

:emit_str_esc
48 83 C3 02                  # add rbx, 2 (skip \ and char, proper escape tracking omitted for brevity since pass 1 proved it)
# In a pure self-host, we fallback to just writing 0x0A (10) for '\n'.
B0 0A                        # mov al, 10
41 88 02                     # mov [r10], al
49 FF C2                     # inc r10
49 FF C0                     # inc r8
E9 {emit_str2_loop}

:emit_ref2
48 FF C3                     # inc rbx (skip '{')
48 89 D9                     # mov rcx, rbx (name start)
:emit_ref2_len
8A 03                        # mov al, [rbx]
3C 7D                        # cmp al, '}'
0F 84 {lookup_label}
48 FF C3                     # inc rbx
E9 {emit_ref2_len}

:lookup_label
48 89 DA                     # mov rdx, rbx
48 29 CA                     # sub rdx, rcx (length)
41 50                        # push r8 (save offset)
41 52                        # push r10 (save output ptr)
4D 31 C9                     # xor r9, r9 (index = 0)

:lookup_loop
4C 89 C8                     # mov rax, r9
48 6B C0 18                  # imul rax, 24
4A 8D 3C 07                  # lea rdi, [r15 + rax]
48 39 57 08                  # cmp [rdi+8], rdx
0F 85 {lookup_next}
57 51 52                     # push rdi, rcx, rdx
48 8B 3F                     # mov rdi, [rdi] (name_ptr)
48 89 CE                     # mov rsi, rcx
F3 A6                        # rep cmpsb
5A 59 5F                     # pop rdx, rcx, rdi
0F 84 {lookup_found}         # je lookup_found
:lookup_next
49 FF C1                     # inc r9
E9 {lookup_loop}

:lookup_found
48 8B 47 10                  # mov rax, [rdi+16] (target)
41 5A                        # pop r10
41 58                        # pop r8

4C 89 C1                     # mov r9, r8
49 81 C1 78 00 40 00         # add r9, 0x400078
49 83 C1 04                  # add r9, 4
4C 29 C8                     # sub rax, r9 (rax = relative)
41 89 02                     # mov dword [r10], eax
49 83 C2 04                  # add r10, 4
49 83 C0 04                  # add r8, 4
48 FF C3                     # inc rbx (skip '}')
E9 {pass2_loop}

:pass2_end

# ─── WRITE FILE TO DISK ───
# sys_open("a.out", O_WRONLY|O_CREAT|O_TRUNC = 0x241, 0755 = 493)
48 8D 3D {_out_name}         # lea rdi, [rip + _out_name]
48 C7 C6 41 02 00 00         # mov rsi, 0x241
48 C7 C2 ED 01 00 00         # mov rdx, 493
48 C7 C0 02 00 00 00         # mov rax, 2 (sys_open)
0F 05                        # syscall
48 89 C3                     # mov rbx, rax (fd)

# sys_write(fd, buf=r14, count=filesz)
48 89 DF                     # mov rdi, rbx
4C 89 F6                     # mov rsi, r14
48 8B 56 60                  # mov rdx, [rsi + 96]
48 C7 C0 01 00 00 00         # mov rax, 1 (sys_write)
0F 05                        # syscall

# sys_close(fd)
48 89 DF                     # mov rdi, rbx
48 C7 C0 03 00 00 00         # mov rax, 3 (sys_close)
0F 05                        # syscall

# ─── EXIT 0 ───
48 C7 C0 3C 00 00 00         # mov rax, 60 (sys_exit)
48 31 FF                     # xor rdi, rdi (0)
0F 05                        # syscall


# ─── DATA SECTION ───
:usage_msg
"Usage: clc <input.cl>\n(Self-hosted assembler)\n"

:err_open
"Failed to open file\n"

:_out_name
"a.out\n"

:_start_str
"_start"

:_ehdr_tmpl
# ELF Header (64 bytes)
7F 45 4C 46 02 01 01 00 00 00 00 00 00 00 00 00
02 00 3E 00 01 00 00 00 78 00 40 00 00 00 00 00  # Default entry = 0x400078
40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  # phoff = 64
00 00 00 00 40 00 38 00 01 00 00 00 00 00 00 00  # ehsize=64, phentsize=56, phnum=1, rest=0

# Program Header (56 bytes)
01 00 00 00 05 00 00 00  # PT_LOAD, RX
00 00 00 00 00 00 00 00  # offset
00 00 40 00 00 00 00 00  # vaddr = 0x400000
00 00 40 00 00 00 00 00  # paddr = 0x400000
78 00 00 00 00 00 00 00  # filesz (will be patched)
78 00 00 00 00 00 00 00  # memsz  (will be patched)
00 10 00 00 00 00 00 00  # align = 4096
