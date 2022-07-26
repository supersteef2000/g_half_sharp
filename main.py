from lex import *


def main():
    input = "whileb while+"
    lexer = Lexer(input)

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()


main()
