# Contributing to Forge

Forge is a self-hosting systems language combining assembly power with Python-like syntax and formal safety. We welcome contributions from the community.

## Reporting Bugs

- **Search existing issues** before filing a duplicate.
- Use a clear, descriptive title and include the Forge version (`forge --version` or commit hash).
- Provide a **minimal reproduction**: source file, compiler flags, expected vs. actual output.
- Label the issue with `bug` and, if applicable, the affected stage (`stage0`, `stage1`).

## Submitting Changes

1. **Fork** the repository on GitHub.
2. **Create a feature branch** from `main`: `git checkout -b feat/my-change`.
3. **Commit** small, focused changes with descriptive messages (imperative mood, e.g. "Add constant folding to Stage 1").
4. **Push** and open a **Pull Request** against `main`.
   - Reference any related issues in the PR body.
   - Ensure the PR title follows conventional commits: `type(scope): description`.
5. A maintainer will review your PR. Address feedback with additional commits — avoid force-pushing during review.

## Code Style

- **Indentation**: 4 spaces (no tabs).
- **Naming**: `snake_case` for functions, variables, and types.
- **Stage 0** (bootstrapping compiler): written in **C99**.
- **Stage 1** (self-hosted compiler): written in **Forge-Sub**, a safe subset of Forge.
- No trailing whitespace. Files must end with a single newline.

## Compiler Requirements

All code merged into Forge must:

- Compile with **zero warnings** (treat warnings as errors).
- Contain **zero instances of undefined behavior** — Stage 0 must pass `-Wall -Wextra -Wpedantic -Werror` with Clang or GCC; Stage 1 must pass the Forge-Sub safety checker.
- Use `const` correctness, avoid implicit casts, and prefer bounded operations.

## Testing

Before submitting, verify the three core test programs still pass:

```sh
cd forge/stage0 && make
./forge ../../examples/exit.forge   # exit code 0
./forge ../../examples/hello.forge  # prints "hello, world"
./forge ../../examples/fib.forge    # prints Fibonacci sequence correctly
```

If any test fails, your change is not ready for review. Add new test cases under `examples/` for new features.

## Building

```sh
cd forge/stage0 && make
```

The Makefile uses C99 and must remain dependency-free beyond a host C99 compiler (Clang or GCC). Stage 1 builds itself via the Stage 0 compiler — see `forge/stage1/Makefile`.

## Distributed Development Model

Forge development follows a **100 subagents participation model**: the project is designed so that hundreds of independent agents (human or automated) can contribute concurrently without central coordination. Each agent:

- Works in its own fork or feature branch.
- Self-validates changes against the core test suite.
- Submits small, atomic PRs that pass CI.
- Participates in asynchronous review rounds.

This model scales contributions horizontally and minimises merge conflicts through strict separation of concerns — the compiler pipeline, standard library, and examples are independently modifiable.
