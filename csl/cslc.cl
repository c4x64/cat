:_start
48 8B 3C 24               # argc
48 83 FF 02               # cmp argc, 2
0F 8D {argc_ok}
48 C7 C0 3C 00 00 00      # sys_exit
48 31 FF                  # exit 1
0F 05
:argc_ok
48 8B 7C 24 10            # argv[1]
48 31 F6                  # O_RDONLY
48 31 D2                  # mode
48 C7 C0 02 00 00 00      # sys_open
0F 05
48 89 C3                  # rbx = fd
48 31 FF                  # addr
48 C7 C6 00 00 A0 00      # 10MB
48 C7 C2 03 00 00 00      # PROT_RW
49 C7 C2 22 00 00 00      # MAP_PRIV
4D C7 C0 FF FF FF FF      # fd=-1
4D 31 C9                  # offset
48 C7 C0 09 00 00 00      # sys_mmap
0F 05
49 89 C4                  # r12 = input ptr
48 89 DF                  # fd
4C 89 E6                  # buf
48 C7 C2 00 00 A0 00      # len
48 C7 C0 00 00 00 00      # sys_read
0F 05
49 89 C5                  # r13 = input bytes length
48 89 DF
48 C7 C0 03 00 00 00      # sys_close
0F 05
48 31 FF
48 C7 C6 00 00 A0 00
48 C7 C2 03 00 00 00
49 C7 C2 22 00 00 00
4D C7 C0 FF FF FF FF
4D 31 C9
48 C7 C0 09 00 00 00      # sys_mmap
0F 05
49 89 C6                  # r14 = output ptr
4C 89 E3                  # rbx = curr input ptr
4C 8D 2C 2B               # rbp = input end ptr
:main_loop
48 39 EB                  # cmp rbx, rbp
0F 8D {finish}            # jge finish
E8 {read_word}
48 85 C0                  # test rax, rax
0F 84 {main_loop}         # if empty or ws, skip
4C 89 DF                  # r15 = word_ptr
41 8A 17                  # mov dl, [r15]
80 FA 3A                  # cmp dl, ':'
0F 85 {not_cl_label}
E8 {emit_word}            # call emit_word
E8 {emit_nl}
E9 {main_loop}
:not_cl_label
80 FA 22                  # cmp dl, '"'
0F 85 {not_cl_str}
E8 {emit_word}
E8 {emit_nl}
E9 {main_loop}
:not_cl_str
80 FA 23                  # cmp dl, '#'
0F 85 {not_cl_cmt}
E8 {skip_line}
E9 {main_loop}
:not_cl_cmt
3D 6D 6F 76 00            # cmp eax, 'mov'
0F 84 {h_mov}
3D 61 64 64 00            # cmp eax, 'add'
0F 84 {h_add}
3D 73 75 62 00            # cmp eax, 'sub'
0F 84 {h_sub}
3D 63 6D 70 00            # cmp eax, 'cmp'
0F 84 {h_cmp}
3D 6C 65 61 00            # cmp eax, 'lea'
0F 84 {h_lea}
3D 70 75 73 68            # cmp eax, 'push'
0F 84 {h_push}
3D 70 6F 70 00            # cmp eax, 'pop'
0F 84 {h_pop}
3D 63 61 6C 6C            # cmp eax, 'call'
0F 84 {h_call}
3D 72 65 74 00            # cmp eax, 'ret'
0F 84 {h_ret}
3D 64 65 63 00            # cmp eax, 'dec'
0F 84 {h_dec}
3D 69 6E 63 00            # cmp eax, 'inc'
0F 84 {h_inc}
3D 6A 6D 70 00            # cmp eax, 'jmp'
0F 84 {h_jmp}
3D 6A 65 00 00            # cmp eax, 'je'
0F 84 {h_je}
48 B9 73 79 73 63 61 6C 6C 00 # mov rcx, 'syscall'
48 39 C8                  # cmp rax, rcx
0F 84 {h_syscall}
E8 {skip_line}
E9 {main_loop}
:h_mov
E8 {read_op}
50
53
51
E8 {read_op}
41 89 C4
41 89 DB
41 89 CD
59
5A
58
48 83 F8 00
0F 85 {mov_not_ri}
41 83 FC 01
0F 85 {mov_not_ri}
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
E8 {read_op}
41 89 DB
5B
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
41 89 CD
5B
58
48 C7 C7 48 00 00 00
E8 {eb}
48 C7 C7 81 00 00 00
E8 {eb}
48 8D 7B F8
E8 {eb}
4D 89 EF
E8 {eb32}
E8 {emit_nl}
E9 {main_loop}
:h_push
E8 {read_op}
48 8D 7B 50
E8 {eb}
E8 {emit_nl}
E9 {main_loop}
:h_pop
E8 {read_op}
48 8D 7B 58
E8 {eb}
E8 {emit_nl}
E9 {main_loop}
:h_dec
E8 {read_op}
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
48 C7 C7 E9 00 00 00
E8 {eb}
4C 89 F6
4C 89 CF
4C 89 CA
F3 A4
4C 89 F1
4C 89 FE
E8 {emit_nl}
E9 {main_loop}
:h_je
E8 {read_op}
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
53
E8 {read_op}
5B
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
4C 89 DF
:rw_loop
4D 39 ED
0F 8E {rw_end}
41 8A 13
80 FA 20
0F 86 {rw_end}
80 FA 2C
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
3D 72 61 78 00
0F 84 {op_rax}
3D 72 64 69 00
0F 84 {op_rdi}
3D 72 64 78 00
0F 84 {op_rdx}
3D 72 73 69 00
0F 84 {op_rsi}
3D 72 62 78 00
0F 84 {op_rbx}
3D 72 63 78 00
0F 84 {op_rcx}
41 8A 0F
80 F9 30
0F 8C {op_chk_lbl}
80 F9 39
0F 8F {op_chk_lbl}
48 31 C9
48 31 D2
49 89 FE
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
48 C7 C0 01 00 00 00
C3
:op_chk_lbl
80 F9 7B
0F 85 {op_end}
48 C7 C0 04 00 00 00
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
48 0F C8
48 89 C7
E8 {eb}
C1 E8 08
48 89 C7
E8 {eb}
C1 E8 08
48 89 C7
E8 {eb}
C1 E8 08
48 89 C7
E8 {eb}
C3
:emit_nl
41 C6 06 0A
49 FF C6
C3
:finish
48 83 3C 24 04
0F 8C {use_def}
48 8B 7C 24 20
E9 {do_opn}
:use_def
48 8D 3D {_out_name}
:do_opn
48 C7 C6 41 02 00 00
48 C7 C2 ED 01 00 00
48 C7 C0 02 00 00 00
0F 05
48 89 C3
48 89 DF
4C 89 F6
4C 89 F2
4C 29 C2
48 C7 C0 01 00 00 00
0F 05
48 C7 C0 3C 00 00 00
48 31 FF
0F 05
:_out_name
"a.cl\0"
