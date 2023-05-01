### PyParseExcel

This is a toy project written in Python that demonstrates how to implement a lexer, parser, and interpreter for Excel formulas. The main goal is just to provide a example of how to implement these fundamental components of a programming language interpreter without relying on third-party libraries.

Please note that this is not intended to be a production-ready implementation of an Excel interpreter. Instead, it only supports a small subset of the Excel formulas grammar. Additionally, some common features, such as variable scope, semantic analysis, call stack, and procedure calls, have not been implemented.

### Project Overview

The project is implemented in Python and consists of the following files:

- `lexer.py`: Defines the lexical analysis rules for the parser.
- `parser.py`: Defines the syntax analysis rules for the parser.
- `interpreter.py`: Implements the interpreter for the parsed formulas.
- `main.py`: Provides a REPL (Read-Eval-Print Loop) for users to input and evaluate Excel formulas.

### Usage

Using the REPL:

Calling the API directly inside a script:

Loading a CSV file and evaluating all the formulas in cells:

### Limitations

This project is intended as a simple example and has some limitations:

- Only a subset of Excel functions are implemented
- The parser does not handle all possible input errors gracefully
- The interpreter does not handle all possible data types and formats
