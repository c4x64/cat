# ═══════════════════════════════════════
# exit.cl - Minimal program. Just exits.
# ═══════════════════════════════════════

:_start

# sys_exit(42)
48 C7 C0 3C 00 00 00         # mov rax, 60 (sys_exit)
48 C7 C7 2A 00 00 00         # mov rdi, 42 (exit code)
0F 05                        # syscall
