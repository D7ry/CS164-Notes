# Lexical Analysis

Written modern code is basically an **input string**

Goal of Lexical Analysis:
1. Partition input string into substrings
2. Classify them according to their role

Parser treats different types tokens differently.

A implementation of lexical analysis must do 2 things:
1. **Recognize** substrings corresponding to tokens
2. **Return** the **lexume** aka the value of the token
    - ("if", keyword) is a token-lexume tuple

The above 2 steps can be summarized as **tokenization**.
  
Uninteresting tokens that don't contribute to parsing are discarded.  
- whitespace, comments

**Lookahead** - looking ahead of the read position to decide where one token ends.
- `i` is a var, but `if` is a keyword. we don't know when to end `i` until we see `f`

## Tokenization
Token corresponds to sets of strings

- identifier: strings of letters or digits that *starts with a letter*
- integer: strings of digits
- keywords: things like `else`, `if`, `begin` etc....
- whitespace: sequence of `\n`, `\t` etc...
- open/close parenthesis: `(`, `)`

### Regular Languages
Regular languages is the most popular way to define tokens.  
Regular languages can be described using *regex*
- For each regex, there is a **finite autometa**[^f1] that recognizes the language

If `A` is a regular expressio,  `L(A)` is the language denoted by `A`

*Language*
Def: Let L be a set of strings. L is a language if for every string s in L, there exists a finite sequence of strings s1, s2, ..., sn such that s = s1s2...sn
- Alphabet = English Chars, Language = English Sentences
- Alphabet = ASCII, Language = C programs

#### Regex: Atomic Expressions
Atomic expressions consist of single characters, as building blocks for more complex regex.
Epislon: `ε`
- matches the empty string  

Single Character: `'c'`
- matches the string `c`

#### Regex: Compound Expressions
Concatenation: `AB` where `A` and `B` are regex
- L(AB) = {ab | a in L(A) **and** b in L(B)}
  - ('a'b') = {'ab'}

Union(`|`):
- L(A|B) = {s | s in L(A) **or** s in L(B)}
  - ('a'|'b') = {'a', 'b'}

Iteration(`*`):
- L(A*) = {ε, s | s in L(A)}
  - ('a'*) = {'', 'a', 'aa', 'aaa', ...}

#### Regex: Token identification
To identify...

Keyword:
`'else'| 'if'| 'begin'|`  

Integer(a string of non-empty digits):
digit = `'0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'`
integer = `digit digit*`
Note the integer must begin with a digit, otherwise the `*` will match the empty string.

Identifier:
letter = `'A'|'B'|.... |'z'`
identifier = `letter(letter|digit)*`
Note the identifier must begin with a letter, otherwise the `*` will match the empty string.  

Whitespace:
whitespace = `' '|'\t'|'\n'`
whitespaces* = `whitespace*`

#### Regex: Tokenization Algorithm

1. Select a set of tokens
2. Write regex for the lexemes of each token
3. Construct a regex that matches all lexemes for all tokens
4. Let the input be x<sub>1</sub>x<sub>2</sub>...x<sub>n</sub>
   1. For 1 <= i <= n, check if x<sub>i</sub> matches the regex
5. It must be that x<sub>i</sub> matches the regex for some token
6. Remove the matched substring(x<sub>i</sub>) from the input, and repeat step 4

Rule of **Maximal Munch** - if there are multiple tokens that match the same substring, choose the longest one to avoid ambiguities.

Rule of **first match** - if there are multiple tokens that match the same substring, choose the first one to avoid ambiguities.

## Error Handling
**Lexical Errors** - errors in the input string that are detected by the lexical analyzer

A regex rule matching all "bad" strings and put them in a special token called "error token" at the end of the token list:

R = R<sub>1</sub> | R<sub>2</sub> | ... | R<sub>n</sub> | error

The lexer tool picks only the **shortest** none-empty match.
Multiple, consecutive error tokens are merged into one.

[^f1]: Finite Autometa - a machine that accepts or rejects strings of symbols and only produces a result after it has read all of its input. It is a finite state machine that has no loops in the sense that there is a finite number of states and every state is reachable from every other state by a finite number of transitions. [Wikipedia](https://en.wikipedia.org/wiki/Finite-state_machine