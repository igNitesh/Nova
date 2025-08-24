# from core.lexer.lexer import Lexer
# from core.parser.parser import Parser
# from core.ast.expressionNodes import IntNode, BinaryOpNode, IdentifierNode

# def test_simple_addition():
#     code = "int x = 3 + 5;"
#     lexer = Lexer(code)
#     tokens = lexer.tokenize()
#     parser = Parser(tokens)
#     vardec = parser.parse_variable_declaration()
#     # Check the value node is a BinaryOpNode with IntNode children
#     assert isinstance(vardec.value, BinaryOpNode)
#     assert vardec.value.operator == '+'
#     assert isinstance(vardec.value.left, IntNode)
#     assert vardec.value.left.value == 3
#     assert isinstance(vardec.value.right, IntNode)
#     assert vardec.value.right.value == 5

# def test_variable_and_nested_expression():
#     code = "int a = 40;\nint y = a + 3 * 4;"
#     lexer = Lexer(code)
#     tokens = lexer.tokenize()
#     parser = Parser(tokens)
#     vardec_a = parser.parse_variable_declaration()
#     assert vardec_a.name == "a"
#     assert isinstance(vardec_a.value, IntNode)
#     assert vardec_a.value.value == 40

#     vardec_y = parser.parse_variable_declaration()
#     assert vardec_y.name == "y"
#     assert isinstance(vardec_y.value, BinaryOpNode)
#     assert vardec_y.value.operator == '+'
#     assert isinstance(vardec_y.value.left, IdentifierNode)
#     assert vardec_y.value.left.name == "a"
#     assert isinstance(vardec_y.value.right, BinaryOpNode)
#     assert vardec_y.value.right.operator == '*'
#     assert isinstance(vardec_y.value.right.left, IntNode)
#     assert vardec_y.value.right.left.value == 3
#     assert isinstance(vardec_y.value.right.right, IntNode)
#     assert vardec_y.value.right.right.value == 4