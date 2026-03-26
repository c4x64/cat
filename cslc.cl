
:_start
# skip argv loop, open argv[1]
48 8B 3C 24 # mov rdi, [rsp]
48 83 FF 02 # cmp rdi, 2
0F 8D {argc_ok}

48 C7 C0 3C 00 00 00 # exit
48 31 FF
0F 05

:argc_ok
48 8B 7C 24 10 # mov rdi, argv[1]
48 31 F6
48 31 D2
48 C7 C0 02 00 00 00
0F 05
48 89 C3 # fd

48 31 FF
48 C7 C6 00 00 A0 00
48 C7 C2 03 00 00 00
49 C7 C2 22 00 00 00
4D C7 C0 FF FF FF FF
4D 31 C9
48 C7 C0 09 00 00 00
0F 05
49 89 C4 # r12 = in ptr

48 89 DF
4C 89 E6
48 C7 C2 00 00 A0 00
48 C7 C0 00 00 00 00
0F 05
49 89 C5 # r13 = in len

48 89 DF
48 C7 C0 03 00 00 00
0F 05

48 31 FF
48 C7 C6 00 00 A0 00
48 C7 C2 03 00 00 00
49 C7 C2 22 00 00 00
4D C7 C0 FF FF FF FF
4D 31 C9
48 C7 C0 09 00 00 00
0F 05
49 89 C6 # r14 = out ptr

4C 89 E3 # rbx = in pos
4C 8D 2C 2B # rbp = in end

:main_loop
48 39 EB # cmp rbx, rbp
0F 8D {done}

E8 {read_word} # rax = hash, r15 = ptr, r9 = len
48 85 C0
0F 84 {main_loop}

# check colon
41 8A 17 # mov dl, [r15]
80 FA 3A # cmp dl, ':'
0F 85 {not_cl_label}
E8 {emit_word}
E8 {emit_nl}
E9 {main_loop}

:not_cl_label
80 FA 22 # '"'
0F 85 {not_cl_str}
E8 {emit_word}
E8 {emit_nl}
E9 {main_loop}

:not_cl_str
80 FA 23 # '#'
0F 85 {not_cl_cmt}
E8 {skip_line}
E9 {main_loop}

:not_cl_cmt
# Evaluate Mnemonic in rax
# cmp eax, 'mov'
3D 6D 6F 76 00
0F 84 {h_mov}
# 'add'
3D 61 64 64 00
0F 84 {h_add}
# 'sub'
3D 73 75 62 00
0F 84 {h_sub}
# 'cmp'
3D 63 6D 70 00
0F 84 {h_cmp}
# 'lea'
3D 6C 65 61 00
0F 84 {h_lea}
# 'push'
3D 70 75 73 68
0F 84 {h_push}
# 'pop'
3D 70 6F 70 00
0F 84 {h_pop}
# 'call'
3D 63 61 6C 6C
0F 84 {h_call}
# 'ret'
3D 72 65 74 00
0F 84 {h_ret}
# 'dec'
3D 64 65 63 00
0F 84 {h_dec}
# 'inc'
3D 69 6E 63 00
0F 84 {h_inc}
# 'jmp'
3D 6A 6D 70 00
0F 84 {h_jmp}
# 'je'
3D 6A 65 00 00
0F 84 {h_je}
# 'syscall'
48 B9 73 79 73 63 61 6C 6C 00
48 39 C8
0F 84 {h_syscall}

# Unknown, just skip line for now
E8 {skip_line}
E9 {main_loop}

:h_mov
# Read op1
E8 {read_op}  # rax=type, rbx=reg, rcx=imm/offset, r15=str
50
53
51
# Read op2
E8 {read_op}
41 89 C4 # r12d = op2.type
41 89 DB # r11d = op2.reg
41 89 CD # r13d = op2.imm
59 # rcx = op1.imm
5A # rbx = op1.reg
58 # rax = op1.type

# if op1.type == REG (0) and op2.type == IMM (1): mov reg, imm
48 83 F8 00
0F 85 {mov_not_ri}
41 83 FC 01
0F 85 {mov_not_ri}
# emit 48 C7 C0+reg imm32
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 C7 00 00 00
E8 {eb}
48 8D 7B C0
E8 {eb}
48 89 CF
E8 {eb32}
E8 {emit_nl}
E9 {main_loop}

:mov_not_ri
# if op1.type == REG and op2.type == REG: mov reg, reg -> 48 89 D8 (modrm dst=op1, src=op2)
# modrm = 0xC0 | (src<<3) | dst = 0xC0 | (r11d<<3) | ebx
41 83 FC 00
0F 85 {mov_not_rr}
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 89 00 00 00
E8 {eb}
45 89 DA
41 C1 E2 03
4C 09 D3
48 8D 7B C0
E8 {eb}
E8 {emit_nl}
E9 {main_loop}

:mov_not_rr
E8 {emit_nl}
E9 {main_loop}

:h_add
E8 {read_op}
50
53
# add reg, reg -> 48 01 D8 (modrm dst=op1, src=op2)
E8 {read_op}
41 89 DB # src = op2.reg
5B # dst = op1.reg
58
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 01 00 00 00
E8 {eb}
45 89 DA
41 C1 E2 03
4C 09 D3
48 8D 7B C0
E8 {eb}
E8 {emit_nl}
E9 {main_loop}

:h_sub
E8 {emit_nl}
E9 {main_loop}

:h_cmp
E8 {read_op}
50
53
E8 {read_op}
41 89 CD # op2.imm
5B # op1.reg
58 # op1.type
# cmp reg, imm32 -> 48 81 F8+reg imm32
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 81 00 00 00
E8 {eb}
48 8D 7B F8
E8 {eb}
4D 89 EF # rdi = r13
E8 {eb32}
E8 {emit_nl}
E9 {main_loop}

:h_push
E8 {read_op}
# push reg -> 50+reg
48 8D 7B 50
E8 {eb}
E8 {emit_nl}
E9 {main_loop}

:h_pop
E8 {read_op}
# pop reg -> 58+reg
48 8D 7B 58
E8 {eb}
E8 {emit_nl}
E9 {main_loop}

:h_dec
E8 {read_op}
# dec reg -> 48 FF C8+reg
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 FF 00 00 00
E8 {eb}
48 8D 7B C8
E8 {eb}
E8 {emit_nl}
E9 {main_loop}

:h_inc
E8 {emit_nl}
E9 {main_loop}

:h_jmp
E8 {read_op}
# jmp {label} -> E9 {label}
48 C7 C7 E9 00 00 00
E8 {eb}
# op returns label str in r15, len=r9. We just copy the string natively.
4C 89 F6 # rsi = r15
4C 89 CF # rdi = r14
4C 89 CA # rcx = r9
F3 A4
4C 89 F1
4C 89 FE
E8 {emit_nl}
E9 {main_loop}

:h_je
E8 {read_op}
# je {label} -> 0F 84 {label}
48 C7 C7 0F 00 00 00
E8 {eb}
48 C7 C7 84 00 00 00
E8 {eb}
4C 89 F6
4C 89 CF
4C 89 CA
F3 A4
4C 89 F1
4C 89 FE
E8 {emit_nl}
E9 {main_loop}

:h_lea
E8 {read_op}
53 # op1.reg
E8 {read_op}
5B # dst = op1.reg
# lea reg, {label} -> 48 8D modrm(cros=00, src=dst, rm=101) + {label}
# modrm = 0x05 | (dst<<3)
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 8D 00 00 00
E8 {eb}
48 C1 E3 03
48 8D 7B 05
E8 {eb}
4C 89 F6
4C 89 CF
4C 89 CA
F3 A4
4C 89 F1
4C 89 FE
E8 {emit_nl}
E9 {main_loop}

:h_call
E8 {read_op}
# call {label} -> E8 {label}
48 C7 C7 E8 00 00 00
E8 {eb}
4C 89 F6
4C 89 CF
4C 89 CA
F3 A4
4C 89 F1
4C 89 FE
E8 {emit_nl}
E9 {main_loop}

:h_ret
48 C7 C7 C3 00 00 00
E8 {eb}
E8 {emit_nl}
E9 {main_loop}

:h_syscall
48 C7 C7 0F 00 00 00
E8 {eb}
48 C7 C7 05 00 00 00
E8 {eb}
E8 {emit_nl}
E9 {main_loop}


:read_word
48 31 C0
4D 31 C9
:rw_ws
4D 39 ED
0F 8E {rw_end}
41 8A 13
80 FA 20
0F 8F {rw_chars}
49 FF C3
E9 {rw_ws}
:rw_chars
4C 89 DF # r15 = start ptr
:rw_loop
4D 39 ED
0F 8E {rw_end}
41 8A 13
80 FA 20
0F 86 {rw_end}
80 FA 2C # comma
0F 84 {rw_comm}
49 83 F9 08
0F 8D {rw_skip}
51
81 E2 FF 00 00 00
C1 E1 03
48 D3 E2
48 09 D0
59
49 FF C1
:rw_skip
49 FF C3
E9 {rw_loop}
:rw_comm
49 FF C3
:rw_end
C3

:read_op
E8 {read_word}
# determine type from rax
# is it reg?
3D 72 61 78 00 # rax
0F 84 {op_rax}
3D 72 64 69 00 # rdi
0F 84 {op_rdi}
3D 72 64 78 00 # rdx
0F 84 {op_rdx}
3D 72 73 69 00 # rsi
0F 84 {op_rsi}
3D 72 62 78 00 # rbx
0F 84 {op_rbx}
3D 72 63 78 00 # rcx
0F 84 {op_rcx}

# is it IMM?
41 8A 0F # [r15]
80 F9 30
0F 8C {op_chk_lbl}
80 F9 39
0F 8F {op_chk_lbl}
# parse IMM loop
48 31 C9
48 31 D2
49 89 FE # r14 ptr
:op_imm_lp
41 8A 16
80 FA 30
0F 8C {op_imm_ret}
80 FA 39
0F 8F {op_imm_ret}
80 EA 30
48 6B C9 0A
48 01 D1
49 FF C6
E9 {op_imm_lp}
:op_imm_ret
48 C7 C0 01 00 00 00 # type=1
C3

:op_chk_lbl
80 F9 7B # '{'
0F 85 {op_end}
48 C7 C0 04 00 00 00 # type=4
C3

:op_end
48 31 C0
C3

:op_rax
48 31 C0
48 31 DB
C3
:op_rcx
48 31 C0
48 C7 C3 01 00 00 00
C3
:op_rdx
48 31 C0
48 C7 C3 02 00 00 00
C3
:op_rbx
48 31 C0
48 C7 C3 03 00 00 00
C3
:op_rsi
48 31 C0
48 C7 C3 06 00 00 00
C3
:op_rdi
48 31 C0
48 C7 C3 07 00 00 00
C3

:skip_line
4D 39 ED
0F 8E {skip_end}
41 8A 13
49 FF C3
80 FA 0A
0F 85 {skip_line}
:skip_end
C3

:emit_word
4C 89 F6
4C 89 CE
4C 89 CF
F3 A4
4C 89 F1
C3

:eb
48 89 FB
C1 EB 04
83 E3 0F
80 FB 09
0F 8F {h1}
80 C3 30
E9 {wh}
:h1
80 C3 37
:wh
41 88 1E
49 FF C6

48 89 FB
83 E3 0F
80 FB 09
0F 8F {h2}
80 C3 30
E9 {wl}
:h2
80 C3 37
:wl
41 88 1E
49 FF C6
41 C6 06 20
49 FF C6
C3

:eb32
48 89 F8
48 0F C8
50
48 89 C7
E8 {eb}
58
C1 E8 08
50
48 89 C7
E8 {eb}
58
C1 E8 08
50
48 89 C7
E8 {eb}
58
C1 E8 08
48 89 C7
E8 {eb}
C3

:emit_nl
41 C6 06 0A
49 FF C6
C3

:done
48 8D 3D {_out_name}
48 C7 C6 41 02 00 00
48 C7 C2 ED 01 00 00
48 C7 C0 02 00 00 00
0F 05
48 89 C3

48 89 DF
4C 89 F6
4C 89 F2
4C 2B 56 60 # len = r14 - base (wait base was output mapped)
# Let's fix length output:
4C 29 C2
48 C7 C0 01 00 00 00
0F 05

48 C7 C0 3C 00 00 00
48 31 FF
0F 05

:_out_name
"a.cl\n"
