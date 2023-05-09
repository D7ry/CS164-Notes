# Bottom-up Parsing/LR Parsing

Bottom-up parsing is more general than top-down, and just as efficient.

L - tokens are read from left to right
R - constructs the rightmost derivation

Advantage: 
1. LR parsing don't need grammar to be left-factored
2. LR parsing support left-recursive grammar

Example: consider the following grammar:

```
E -> E + (E) | int
```
The grammar isn't LL(1); it's left-recursive.

Core idea: reducing a string to the start symbol by inverting productions. Replace rhs with lhs non-terminals until the start symbol is reached.

example:
```
str <- input string of terminals
```
repeat:
```
Identify b in str such that A->b is a prouction
replace b by A in str
until str = S
```

The algorithm goes from bottom to top, from left to right.
However, looking at the reduction as a top-down process, it's a right-to-left derivation process.

**A LR parser traces the right-most derivation, but in reverse**

## Implemntation

consider the following state of a string being LR-parsed
`lhs > rhs`
`rhs` is a stack of terminals and non-terminals
`rhs` is a list of non-terminals that haven't been read yet.
if some consequtive combination of symbols in `lhs` can be reduced(more on this later) i.e. they belong to the right part of a production rule, reduce them.
Otherwise, keep going right, adding one terminal from rhs to lhs at a time.

To know when to reduce lhs or when to advance the arrow, we use a DFA.

The DFA is ran on the lhs stack to reach state `X`, with `tok` as the next token to be read.
if `X` has a transition `tok`, advance the arrow and change state.
if `X` has label `A->b on tok`, reduce `A->b`
else, error.

## Generating the DFA

**LR(1) item**  - a production rule with a dot in it, indicating the position of the next symbol to be read, and a lookahead terminal symbol.


e.g.: E-> E + (e) can be turned into E-> * E + (e) + any terminal symbol