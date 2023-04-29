from parser import parser

from lexer import lexer


def main(expr):
    tokens = lexer(expr)
    ast = parser(iter(tokens))
    print(ast)


if __name__ == "__main__":
    test = "1 * (2 + 3)"
    main(test)
