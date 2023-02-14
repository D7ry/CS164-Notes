# Top-down Parsing

Top-down parsing is very inefficient, but we'll begin from here.

Construction order: top->down; left->right.

Example: csonsider the grammar:
```
E-> T+ E|T
T->(E)|int|int*T
```

Given the token stream: `int * int`

we begin with the top-level non-terminal `E`, and try the rules for `E` in order.

```
void match-A() {
    choose an A-production A->X1X2...Xn
    for (i = 1 to n) {
        if (Xi is a terminal) {
            if (Xi matches the next token) {
                consume the next token
            } else {
                back-track(no match founded)
            }
        } else {
            match-Xi()
        }
    }
}
```

This is egregiously inefficient, because we have to try every possible derivation of the string, and we have to try every possible derivation of every sub-string.  

Problem: left-recursive grammar leads to infinite recursion. Example: `E->E|T`