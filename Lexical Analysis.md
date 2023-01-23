# Lexical Analysis

Written modern code is basically an **input string**

Goal of Lexical Analysis:
1. Partition input string into substrings
2. Classify them according to their role

Parser treats different types tokens differently.

## Token
Token corresponds to sets of strings

- identifier: strings of letters or digits that *starts with a letter*
- integer: strings of digits
- keywords: things like `else`, `if`, `begin` etc....
- whitespace: sequence of ` `, `\n`, `\t` etc...
- open/close parenthesis: `(`, `)`

