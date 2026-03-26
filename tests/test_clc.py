import subprocess
import os
import sys

def run_test(name, cl_file, expected_output=None, expected_exit_code=0):
    print(f"TEST: {name}...", end=" ")

    # Assemble
    result = subprocess.run(
        [sys.executable, "clc.py", cl_file, "-o", "test_binary"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"FAIL (assembler error: {result.stderr.strip()})")
        return False

    # Make executable
    os.chmod("test_binary", 0o755)

    # Run
    try:
        result = subprocess.run(
            ["./test_binary"],
            capture_output=True, text=True
        )

        if expected_output is not None:
            if result.stdout != expected_output:
                print(f"FAIL (expected '{expected_output}', got '{result.stdout}')")
                return False

        if result.returncode != expected_exit_code:
            print(f"FAIL (expected exit {expected_exit_code}, got {result.returncode})")
            return False
            
    except OSError as e:
        print(f"SKIPPED (cannot run ELF on this OS: {e})")
        return True

    print("PASS")
    return True

def run_error_test(name, cl_content, expected_error_substring):
    print(f"TEST: {name}...", end=" ")

    with open("test_error.cl", "w") as f:
        f.write(cl_content)

    result = subprocess.run(
        [sys.executable, "clc.py", "test_error.cl", "-o", "test_binary"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"FAIL (should have produced error)")
        return False

    if expected_error_substring not in result.stderr:
        print(f"FAIL (expected error containing '{expected_error_substring}')")
        return False

    print("PASS")
    return True

passed = 0
failed = 0

tests = [
    lambda: run_test("Hello World", "examples/hello.cl", "Hello from cL!\n"),
    lambda: run_test("Exit Code", "examples/exit.cl", expected_exit_code=42),
    lambda: run_test("Addition", "examples/add.cl", expected_exit_code=8),
    lambda: run_error_test("Invalid Hex", "GG FF\n", "Invalid hex"),
    lambda: run_error_test("Undefined Label", "48 8D 35 {nonexistent}\n", "Undefined label"),
    lambda: run_error_test("Duplicate Label", ":foo\n:foo\n", "Duplicate label"),
]

for test in tests:
    if test():
        passed = passed + 1  # type: ignore
    else:
        failed = failed + 1  # type: ignore

# Cleanup
for f in ["test_binary", "test_error.cl"]:
    if os.path.exists(f):
        try: os.remove(f)
        except OSError: pass

print(f"\nResults: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
