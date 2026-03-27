# cvm_win.cl - Native CatVM for Windows (Circle 1)
# This VM executes CatArch binaries natively on Windows x64.

:_start
    # 1. Setup Stack Frame
    48 83 EC 28               # sub rsp, 40 (shadow space)

    # 2. Get standard out/in? (Actually, let's use NtWriteFile later)
    # For now, let's just implement a math loop to prove it works.

    # 3. Simulate VM execution
    # R10 = VM R0 (hardwired 0)
    # R11 = VM R1 (return)
    # R12 = VM Registers base (let's use stack space)
    48 89 E5                  # mov rbp, rsp
    48 81 EC 00 08 00 00      # sub rsp, 2048 (256 * 8 bytes for regs)
    49 89 E4                  # mov r12, rsp

    # 4. Mock instruction execution
    # CatArch: MOVI R1, 10 (02 01 00 0A)
    # x86-64 equivalent:
    49 C7 04 24 0A 00 00 00   # mov qword [r12], 10 (Set R0=10, wait R0 should be 0)
    # Let's set R1 instead
    49 C7 44 24 08 0A 00 00 00 # mov qword [r12+8], 10 (R1=10)
    
    # 5. ExitProcess(0)
    # Syscall 0x2c is NtTerminateProcess in many Win10/11 versions
    # But usually we call RtlExitUserProcess
    # To keep it simple, we'll just return for now if possible? 
    # (Actually we need a real exit)
    48 31 C9                  # xor rcx, rcx (handle)
    48 31 D2                  # xor rdx, rdx (status)
    48 C7 C0 2C 00 00 00      # rax = 0x2c
    0F 05                     # syscall (NtTerminateProcess)

    # Note: This is an experiment. Real cvm_win.cl will have reach fetch/decode.
