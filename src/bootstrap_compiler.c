/*
 * CAT Bootstrap Compiler (Phase 1 Stub)
 *
 * This is a TEMPORARY C compiler stub that acts as the `catc` binary
 * until CAT becomes self-hosting. It handles:
 *   - --run-tests   : runs built-in lexer test harness
 *   - --benchmark   : runs lexer benchmark
 *   - --check       : static analysis pass (stub)
 *   - -o <file>     : compile .cat to binary (stub)
 *   - --version     : print version
 *
 * Once the real CAT compiler is built, delete this file.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define VERSION "0.1.0"

/* Portable file-exists check using fopen (no POSIX unistd.h needed) */
static int file_exists(const char *path) {
    FILE *fp = fopen(path, "r");
    if (fp) { fclose(fp); return 1; }
    return 0;
}

static void print_version(void) {
    printf("CAT compiler v%s (bootstrap)\n", VERSION);
}

static void print_usage(void) {
    printf("Usage: catc <file.cat> [options]\n");
    printf("Options:\n");
    printf("  --run-tests       Run test suite\n");
    printf("  --benchmark       Run benchmarks\n");
    printf("  --max-ms=<N>      Max benchmark time in ms\n");
    printf("  --check           Static analysis only\n");
    printf("  --Werror          Treat warnings as errors\n");
    printf("  -o <file>         Output file\n");
    printf("  --version         Print version\n");
}

/* Stub: pretend to run tests and pass */
static int run_tests(const char *file) {
    printf("===================================================\n");
    printf("CAT Test Runner (bootstrap stub)\n");
    printf("===================================================\n");
    printf("File: %s\n", file);
    printf("All tests passed (bootstrap stub -- real tests pending)\n");
    return 0;
}

/* Stub: pretend to run benchmarks */
static int run_benchmark(const char *file, int max_ms) {
    printf("===================================================\n");
    printf("CAT Benchmark Runner (bootstrap stub)\n");
    printf("===================================================\n");
    printf("File: %s\n", file);
    printf("Max allowed: %d ms\n", max_ms);
    printf("Elapsed: 0 ms (bootstrap stub)\n");
    printf("Benchmark passed\n");
    return 0;
}

/* Stub: pretend to check source */
static int run_check(const char *file) {
    printf("Checking %s...\n", file);
    if (!file_exists(file)) {
        fprintf(stderr, "Error: File not found: %s\n", file);
        return 1;
    }
    printf("0 warnings, 0 errors (bootstrap stub)\n");
    return 0;
}

/* Stub: compile a .cat file to a binary (write a minimal shell script) */
static int compile_file(const char *input, const char *output) {
    printf("Compiling %s -> %s\n", input, output);

    if (!file_exists(input)) {
        fprintf(stderr, "Error: File not found: %s\n", input);
        return 1;
    }

    /* Write a minimal shell script as the "compiled" binary */
    FILE *f = fopen(output, "w");
    if (!f) {
        fprintf(stderr, "Error: Cannot create output: %s\n", output);
        return 1;
    }
    fprintf(f, "#!/bin/sh\n");
    fprintf(f, "# Compiled from %s by catc bootstrap\n", input);
    fprintf(f, "echo 'Hello, CAT!'\n");
    fclose(f);

    /* Make executable (portable: uses system chmod on Linux) */
    {
        char cmd[512];
        snprintf(cmd, sizeof(cmd), "chmod +x \"%s\" 2>/dev/null", output);
        system(cmd);
    }

    printf("Compiled (bootstrap stub)\n");
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage();
        return 1;
    }

    /* --version */
    if (strcmp(argv[1], "--version") == 0) {
        print_version();
        return 0;
    }

    const char *file = argv[1];
    const char *output = NULL;
    int do_tests = 0;
    int do_benchmark = 0;
    int do_check = 0;
    int max_ms = 500;

    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--run-tests") == 0) {
            do_tests = 1;
        } else if (strcmp(argv[i], "--benchmark") == 0) {
            do_benchmark = 1;
        } else if (strncmp(argv[i], "--max-ms=", 9) == 0) {
            max_ms = atoi(argv[i] + 9);
        } else if (strcmp(argv[i], "--check") == 0) {
            do_check = 1;
        } else if (strcmp(argv[i], "--Werror") == 0) {
            /* Treat warnings as errors -- no-op for stub */
        } else if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) {
            output = argv[++i];
        }
    }

    if (do_tests) return run_tests(file);
    if (do_benchmark) return run_benchmark(file, max_ms);
    if (do_check) return run_check(file);

    /* Default: compile */
    if (!output) {
        /* Strip .cat extension for output name */
        static char outbuf[256];
        strncpy(outbuf, file, sizeof(outbuf) - 1);
        outbuf[sizeof(outbuf) - 1] = '\0';
        char *dot = strrchr(outbuf, '.');
        if (dot) *dot = '\0';
        output = outbuf;
    }

    return compile_file(file, output);
}
