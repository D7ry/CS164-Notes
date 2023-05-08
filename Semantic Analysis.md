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

We use **rule of inference** to check types.
For example, if e<sub>1</sub> has type int and e<sub>2</sub> has type int, then e<sub>1</sub> + e<sub>2</sub> has type int.

For chocopy, inference rules are written as:
(e<sub>1</sub>:int ^ e<sub>2</sub>:int) => e<sub>1</sub> + e<sub>2</sub>:int

Conventional inference rules are written as:
$$\frac{rules}{conclusion}$$

**Type Checking** proves fact about e : T


### Static v. Dynamic Types

review
**Static Type** is the type of an expression that is known at compile time.
**Dynamic Type** is the type of an expression that is known at run time.

 **Soundness Theorem** - an object's dynamic type is always a subtype of its static type.

**Least Upper Bound(LUB)** - the closest common ancestor of 2 types in the inheritance hierarchy. LUB is useful when we look for the type of an expression that has multiple possible types e.g. concatenation of 2 lists.

