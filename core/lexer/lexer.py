import re
from typing import List, Tuple

# Token types
TOKEN_TYPES = {
    'KEYWORD': r'\b(int|float|boolean|string|void|break|continue|if|else|while|for|return)\b',
    'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
    'NUMBER': r'\b\d+(\.\d+)?\b',
    'STRING': r'".*?"',
    'OPERATOR': r'\+\+|--|==|!=|<=|>=|[+\-*/=<>]',
    'PUNCTUATION': r'[(),{};,]',
    'WHITESPACE': r'\s+',
    'COMMENT': r'//.*|/\*.*?\*/'
}

# Combined regex for tokenizing
TOKEN_REGEX = re.compile(
    f"(?P<KEYWORD>{TOKEN_TYPES['KEYWORD']})|"
    f"(?P<IDENTIFIER>{TOKEN_TYPES['IDENTIFIER']})|"
    f"(?P<NUMBER>{TOKEN_TYPES['NUMBER']})|"
    f"(?P<STRING>{TOKEN_TYPES['STRING']})|"
    f"(?P<OPERATOR>{TOKEN_TYPES['OPERATOR']})|"
    f"(?P<PUNCTUATION>{TOKEN_TYPES['PUNCTUATION']})|"
    f"(?P<WHITESPACE>{TOKEN_TYPES['WHITESPACE']})|"
    f"(?P<COMMENT>{TOKEN_TYPES['COMMENT']})",
    re.DOTALL
)

class Token:
    def __init__(self, type_: str, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, Line: {self.line}, Column: {self.column})"

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        self.line = 1
        self.column = 1
    
    def tokenize(self) -> List[Token]:
        position = 0
        while position < len(self.source_code):
            match = TOKEN_REGEX.match(self.source_code, position)

            if not match:
                # Generate a placeholder "hole" for invalid tokens
                print(f"Warning: Invalid token at Line {self.line}, Column {self.column}")
                self.tokens.append(Token("ERROR", "<?>", self.line, self.column))
                position += 1  # Move forward to prevent infinite loops
                self.column += 1
                continue
            
            token_type = match.lastgroup
            value = match.group(token_type)
            
            if token_type == 'WHITESPACE':
                newlines = value.count('\n')
                if newlines:
                    self.line += newlines
                    self.column = 1
                else:
                    self.column += len(value)
            elif token_type == 'COMMENT':
                newlines = value.count('\n')
                self.line += newlines
                self.column = 1 if newlines else self.column + len(value)
            else:
                self.tokens.append(Token(token_type, value, self.line, self.column))
                self.column += len(value)
            
            position += len(value)
        
        return self.tokens

# Example usage:
if __name__ == "__main__":
    code = """
    int x = 10;
    string name = "nitesh";
    if (x > y) {
        return "Hello";
    }
    print("hello ",nitesh);
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token.type)
