# Code Generation

## Stack Machine

- Behaves just like a stack
- Top of the stack stored in a register
- Invariant(convention): after computing an expression, the stack is the same as before


## Code Generation Strategy in RISC-V

For each expression **e** we generate RISC-V code that:
- Computes the value of **e** in `a0`
- Preserves stack pointer and the contents of the stack, after generation.