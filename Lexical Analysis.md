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
- For each regex, there is a deterministic **finite autometa**[^f1] that recognizes the language
- the state machine drops any string not matching its regex; there exists an implicit "bad state" to which all other states can transition to reject a regex.

If `A` is a regular expressio,  `L(A)` is the language denoted by `A`

**Language**
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

# Finite Autometa
## NFA Vs. DFA
DFA - completely determined by input

NFA - NFAs can choose whether to make *epsilon moves*(moves that don't consume any input); NFAs also has one-deterministic transitions from one state to another.

NFA is much easier to implement than DFA, but DFA can simulate NFA.

## $\varepsilon$ -NFA to NFA
Somehow this part is not covered in the slides wtf lol; but it's explained nicely [here](https://www.geeksforgeeks.org/conversion-of-epsilon-nfa-to-nfa/)

pseud code:
```python
epsilon_moves = [...]
for epsilon_move in epsilon_moves:
  v1 = epsilon_move.src
  v2 = epsilon_move.dest
  for move in v2.moves:
    v1.add_move(move.input, move.dest)
  v1.remove(epsilon_move)
  if v1.is_start_state:
    v2.is_start_state = True
  if v2.is_final_state:
    v1.is_final_state = True
```

1. Consider the two vertexes having the epsilon move. Here in Fig.1 we have vertex v1 and vertex v2 having epsilon move from v1 to v2. 

2. Now find all the moves to any other vertex that start from vertex v2 (other than the epsilon move that is considering). After finding the moves, duplicate all the moves that start from vertex v2, with the same input to start from vertex v1 and remove the epsilon move from vertex v1 to vertex v2.

3. See that if the vertex v1 is a start state or not. If vertex v1 is a start state, then we will also make vertex v2 as a start state. If vertex v1 is not a start state, then there will not be any change. 

4. See that if the vertex v2 is a final state or not. If vertex v2 is a final state, then we will also make vertex v1 as a final state. If vertex v2 is not a final state, then there will not be any change. Repeat the steps(from step 1 to step 4) until all the epsilon moves are removed from the NFA.

## NFA to DFA

1. Start with NFA
2. Simulate all possible inputs, and record all possible states
3. For each input, group all possible NFA state outcomes into a single DFA state

pseudo-algorithm
```python
#nfaStateGroup is a subset of nfaStates
map<nfaStateGroup, map<action, nfaStateGroup>> dfaStateActionMap
list actions = [...]
def do(nfaStateGroup):
  if nfaStateGroup in dfaStateActionMap:
    return
  dfaStateActionMap[nfaStateGroup] = {}
  for nfaState in nfaStateGroup:
    for action in actions
     ...
        
do({{startState, [(epsilon, startState)]}})

```
[Full Algorithm](https://github.com/D7ry/CS164-Notes/blob/main/ezDFA.py)

## REGEX to NFA
more on [lecture slides](https://drive.google.com/file/d/15Cq6EwE17AmH7rxYtwfncWs2f6fVpOXh/view)


## DFA Implementation
DFA can be implemented by a 2D table, where the rows are the states and the columns are input symbols.  
For every transition, read transition and skip to another state per the table.
This implementation is efficient as a jump table.

*In some practices, NFA is eventually used instead of DFA for less space complexity.

## Limits of regular languages
A finite autometon that runs long enough must repeat states.
Therefore it can't remember # of times it has visited a particular state, hence for example, it can't recognize a string that contains same number of 0s and 1s.

[^f1]: Finite Autometa - a machine that accepts or rejects strings of symbols and only produces a result after it has read all of its input. It is a finite state machine that has no loops in the sense that there is a finite number of states and every state is reachable from every other state by a finite number of transitions. [Wikipedia](https://en.wikipedia.org/wiki/Finite-state_machine


