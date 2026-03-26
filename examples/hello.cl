# ═══════════════════════════════════════
# hello.cl - Hello World in cL
# This IS machine code. Every byte shown.
# ═══════════════════════════════════════

# Entry point
:_start

# ─── sys_write(1, msg, 15) ───
48 C7 C0 01 00 00 00         # mov rax, 1 (sys_write)
48 C7 C7 01 00 00 00         # mov rdi, 1 (stdout)
48 8D 35 {msg}               # lea rsi, [rip + msg]
48 C7 C2 0F 00 00 00         # mov rdx, 15 (length)
0F 05                        # syscall

# ─── sys_exit(0) ───
48 C7 C0 3C 00 00 00         # mov rax, 60 (sys_exit)
48 31 FF                     # xor rdi, rdi (exit code 0)
0F 05                        # syscall

# ─── Data ───
:msg
"Hello from cL!\n"
