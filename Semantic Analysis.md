# Semantic Analysis

Parsing can catch some errors, but not all of them. For examlpe: 
```
all used variables must have been declared
```
The above rule is not context-free, meaning the parser cannot enforce it.

**Semantic Analysis** performs many checks that can't be done by the parser, for example:

- All identifiers must be declared
- Types must be enforced
- Inheritance relationship
- Classes can be defined only once
- Reserved identifiers are not used
- ...(depends on the language)


**Scope** is the region of the program where an identifier is visible.

**Symbol Table** is a data structure that tracks the current bindings of identifiers.

Most-Closely-nested rule: the most recently declared identifier is the one that is in scope.

MCNR doesn't work for some semantics: 
example: class definition. 
Solution: Do multiple passes over the program.


## Type Checking