from enum import Enum, auto

class TokenType(Enum):
    # Keywords in Devanagari
    FUNCTION = auto()      # फंक्शन
    RETURN = auto()        # वापस
    IF = auto()            # अगर
    ELSE = auto()          # अन्यथा
    WHILE = auto()         # जबतक
    TRUE = auto()          # सत्य
    FALSE = auto()         # असत्य
    VAR = auto()           # वैरिएबल
    CONST = auto()         # स्थिर
    FOR = auto()           # केलिए
    BREAK = auto()         # तोड़
    CONTINUE = auto()      # जारी
    PRINT = auto()         # छाप
    STRING = auto()        # स्ट्रिंग
    ARRAY = auto()         # सरणी
    
    # Other tokens
    IDENTIFIER = auto()
    NUMBER = auto()
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    EQUALS = auto()        # =
    BANG = auto()          # !
    BANG_EQUAL = auto()    # !=
    EQUAL_EQUAL = auto()   # ==
    GREATER = auto()       # >
    GREATER_EQUAL = auto() # >=
    LESS = auto()          # <
    LESS_EQUAL = auto()    # <=
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    SEMICOLON = auto()     # ;
    COMMA = auto()         # ,
    DOT = auto()           # .
    COLON = auto()         # :
    EOF = auto()

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type}: {self.lexeme}"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        
        # Devanagari keywords mapping
        self.keywords = {
            'फंक्शन': TokenType.FUNCTION,
            'वापस': TokenType.RETURN,
            'अगर': TokenType.IF,
            'अन्यथा': TokenType.ELSE,
            'जबतक': TokenType.WHILE,
            'सत्य': TokenType.TRUE,
            'असत्य': TokenType.FALSE,
            'वैरिएबल': TokenType.VAR,
            'स्थिर': TokenType.CONST,
            'केलिए': TokenType.FOR,
            'तोड़': TokenType.BREAK,
            'जारी': TokenType.CONTINUE,
            'छाप': TokenType.PRINT,
            'स्ट्रिंग': TokenType.STRING,
            'सरणी': TokenType.ARRAY
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        
        if c.isspace():
            if c == '\n':
                self.line += 1
            return

        if c == '/':
            if self.match('/'):
                # A comment goes until the end of the line.
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
                return
            else:
                self.add_token(TokenType.DIVIDE)
                return

        if c.isdigit():
            self.number()
            return

        if c.isalpha() or ord(c) > 127:  # Support for Devanagari characters
            self.identifier()
            return

        if c == '"':
            self.string()
            return

        if c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '*':
            self.add_token(TokenType.MULTIPLY)
        elif c == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUALS)
        elif c == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == '<':
            if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == '(':
            self.add_token(TokenType.LPAREN)
        elif c == ')':
            self.add_token(TokenType.RPAREN)
        elif c == '{':
            self.add_token(TokenType.LBRACE)
        elif c == '}':
            self.add_token(TokenType.RBRACE)
        elif c == '[':
            self.add_token(TokenType.LBRACKET)
        elif c == ']':
            self.add_token(TokenType.RBRACKET)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == ':':
            self.add_token(TokenType.COLON)
        else:
            print(f"Unexpected character '{c}' at line {self.line}")
            return

    def identifier(self):
        while not self.is_at_end() and (self.peek().isalnum() or ord(self.peek()) > 127 or self.peek() == '_'):
            self.advance()

        text = self.source[self.start:self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        if type == TokenType.TRUE:
            self.add_token(type, True)
        elif type == TokenType.FALSE:
            self.add_token(type, False)
        else:
            self.add_token(type)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        # Look for decimal point
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()  # consume the "."
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            print(f"Unterminated string at line {self.line}")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source)

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line)) 