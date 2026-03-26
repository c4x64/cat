# ═══════════════════════════════════════
# add.cl - Add two numbers, exit with sum
# ═══════════════════════════════════════

:_start

# Load values
48 C7 C0 05 00 00 00         # mov rax, 5
48 C7 C3 03 00 00 00         # mov rbx, 3

# Add them
48 01 D8                     # add rax, rbx

# Exit with result (rax = 8)
48 89 C7                     # mov rdi, rax (exit code = sum)
48 C7 C0 3C 00 00 00         # mov rax, 60 (sys_exit)
0F 05                        # syscall

# Test: echo $? should print 8
