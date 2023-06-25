### PyParseExcel

This is a toy project written in Python that demonstrates how to implement a lexer, parser, and interpreter for Excel formulas. The main goal is just to provide a example of how to implement these fundamental components of a programming language interpreter without relying on third-party libraries.
Please note that this is not intended to be a production-ready implementation of an Excel interpreter. Instead, it only supports a small subset of the Excel formulas grammar. Additionally, some common features of interpreters, such as variable scope, semantic analysis, call stack, and procedure calls, have not been implemented.

Also the interpreter doesn't implement strictly the same behavior as the original excel formula resolver. Since I don't use excel very often and this is only intend as a study, is probably that some functions are implemented with different behavior

### Project Overview

The project is implemented in Python and consists of the following files:

- `lexer.py`: Defines the lexical analysis rules for the parser.
- `parser.py`: Defines the syntax analysis rules for the parser to assemple the AST.
- `interpreter.py`: Implements the interpreter that evaluates the AST.
- `main.py`: Provides a REPL (WIP) for users to input and evaluate Excel formulas and a cli interface to process csv files.

### Usage

- Using the REPL:

  > WIP

- Calling the API directly inside a script:

```python
from pyexcelparser import formula_resolver

formula_resolver("1 + COS(2 * PI())")
>>> 2
formula_resolver("SUM(A1:A2)", variable = {"A1":1, "A2":2})
>>> 3
```

- Loading a CSV file and evaluating all the formulas in cells:

```bash
$ cat test.csv
>>> 1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    1,2,3,=MAX(A1:C1),
    =SUM(A1:A10),=SUM(B1:B10),=SUM(C1:C10),=SUM(D1:D10)

$ python formula_resolver/main.py test.csv
>>> 1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    1,2,3,3,
    10,20,30,30,
```

### Limitations

This project is intended as a simple example and has some limitations:

- Only a subset of Excel functions are implemented
- The parser does not handle all possible input errors gracefully
- The interpreter does not handle all possible data types and formats

Not implemented:

- datetime types;
- auto converting data types
- reference to other sheets
- intersect operator

### TODO

- [x] parse and resolve csv file
- [ ] implement repl
- [x] use custom dict for variables
- [ ] better error handling in parser and log management
- [ ] return correct error types (e.g. #NAME?, #REF!, #NULL!, #N/A, #DIV0!, #NUM!)
- [ ] implemented some ref functions
- [x] parse all data types: FLOAT, INT, TEXT, LOGICAL
- [x] implement unary operators -, + and %
- [x] parse all variable formats: AB12, $AB12, AB$12, $AB$12
- [x] implement all binary / comparison operators
- [x] add common functions:
  - [x] AND, OR, XOR, IF, NOT
  - [x] ABS, COS, SIN, TAN, EXP, LOG, LOG10, PI
  - [x] CEIL, EXP, FLOOR, LOG, LOG10, MAX, MIN, ROUND, SUM
  - [x] COS, PI, SIN, TAN
- [x] add integrated tests
- [x] implement range operator
