from core.interpreter.symbol_table import SymbolTable
from core.lexer.lexer import Lexer
from core.parser.parser import Parser


if __name__ == "__main__":
    code = """
    int a = 40;
    a++;
    if(i < 10) {
        a += i;    
        }
    

    """



    lexer = Lexer(code)
    tokens = lexer.tokenize()

    print("Tokens:", tokens)

    parser = Parser(tokens)

    parse = parser.parse_program()
    print("parser: ..................................... ")

    for i in parse:
        print(i)



    