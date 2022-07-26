import enum
import sys
import unicodedata


class Lexer:
    def __init__(self, input):
        self.source = input
        self.cur_char = ''
        self.cur_pos = -1
        self.next_char()

    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        if self.cur_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos + 1]

    @staticmethod
    def abort(message):
        sys.exit("Lexing error: " + message)

    def skip_whitespace(self):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r' or self.cur_char == '\n':
            self.next_char()

    def skip_comment(self):
        if self.cur_char == '/':
            if self.peek() == '/':
                while self.cur_char != '\n':
                    self.next_char()
                self.next_char()
                self.skip_comment()
            if self.peek() == '*':
                while self.cur_char != '*' or self.peek() != '/':
                    self.next_char()
                self.next_char()
                self.next_char()
                self.skip_comment()

    def get_token(self):
        self.skip_whitespace()
        self.skip_comment()
        token = None
        match self.cur_char:
            case '+':
                token = Token(self.cur_char, TokenType.PLUS)
            case '-':
                token = Token(self.cur_char, TokenType.MINUS)
            case '*':
                token = Token(self.cur_char, TokenType.ASTERISK)
            case '/':
                token = Token(self.cur_char, TokenType.SLASH)
            case '=':
                if self.peek() == '=':
                    last_char = self.cur_char
                    self.next_char()
                    token = Token(last_char + self.cur_char, TokenType.EQEQ)
                else:
                    token = Token(self.cur_char, TokenType.EQ)
            case '>':
                if self.peek() == '=':
                    last_char = self.cur_char
                    self.next_char()
                    token = Token(last_char + self.cur_char, TokenType.GTEQ)
                else:
                    token = Token(self.cur_char, TokenType.GT)
            case '<':
                if self.peek() == '=':
                    last_char = self.cur_char
                    self.next_char()
                    token = Token(last_char + self.cur_char, TokenType.LTEQ)
                else:
                    token = Token(self.cur_char, TokenType.LT)
            case '!':
                if self.peek() == '=':
                    last_char = self.cur_char
                    self.next_char()
                    token = Token(last_char + self.cur_char, TokenType.NOTEQ)
                else:
                    self.abort("Expected !=, got !" + self.peek())
            case '\"':
                self.next_char()
                start_pos = self.cur_pos
                while self.cur_char != '\"':
                    self.next_char()
                token_text = self.source[start_pos:self.cur_pos]
                token = Token(token_text, TokenType.STRING)
            case '{':
                token = Token(self.cur_char, TokenType.LEFTBRACE)
            case '}':
                token = Token(self.cur_char, TokenType.RIGHTBRACE)
            case '(':
                token = Token(self.cur_char, TokenType.LEFTPARENTHESIS)
            case ')':
                token = Token(self.cur_char, TokenType.RIGHTPARENTHESIS)
            case '[':
                token = Token(self.cur_char, TokenType.LEFTBRACKET)
            case ']':
                token = Token(self.cur_char, TokenType.RIGHTBRACKET)
            case ',':
                token = Token(self.cur_char, TokenType.COMMA)
            case '\0':
                token = Token(self.cur_char, TokenType.EOF)
            case _:
                if self.cur_char.isdigit():
                    start_pos = self.cur_pos
                    while self.peek().isdigit():
                        self.next_char()
                    if self.peek() == '.':
                        self.next_char()
                        if not self.peek().isdigit():
                            self.abort("Digit expected, received " + self.peek() + " (" + unicodedata.name(self.peek()) + ")")
                        while self.peek().isdigit():
                            self.next_char()
                    token_text = self.source[start_pos:self.cur_pos + 1]
                    token = Token(token_text, TokenType.NUMBER)
                elif self.cur_char.isalpha():
                    start_pos = self.cur_pos
                    while self.peek().isalnum():
                        self.next_char()
                    token_text = self.source[start_pos:self.cur_pos + 1]
                    keyword = Token.check_if_keyword(token_text)
                    if keyword is None:
                        token = Token(token_text, TokenType.IDENT)
                    else:
                        token = Token(token_text, keyword)
                else:
                    self.abort("Unknown token: " + self.cur_char + " (" + unicodedata.name(self.cur_char) + ")")
        self.next_char()
        return token


class Token:
    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind

    @staticmethod
    def check_if_keyword(token_text):
        for token_kind in TokenType:
            if token_kind.name.lower() == token_text and 100 <= token_kind.value < 200:
                return token_kind
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    LEFTBRACE = 4
    RIGHTBRACE = 5
    LEFTPARENTHESIS = 6
    RIGHTPARENTHESIS = 7
    LEFTBRACKET = 8
    RIGHTBRACKET = 9
    COMMA = 10
    # Keywords
    PRINT = 101
    INPUT = 102
    LET = 103
    IF = 104
    FOR = 105
    WHILE = 106
    REPEAT = 107
    LOOP = 108
    BREAK = 109
    CONTINUE = 110
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
