from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.ast.statementNodes import For_Statement_Node
from core.ast.declarationNodes import VarDeclarationNode
from core.ast.expressionNodes import IdentifierNode, BinaryOpNode, UnaryOpNode

def test_parse_for_statement_basic():
    code = "for(int i = 0; i < 10; i++) { a = a + i; }"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    node = parser.parse_for_statement()
    assert isinstance(node, For_Statement_Node)
    # Check initialization
    assert isinstance(node.init, VarDeclarationNode)
    assert node.init.name == "i"
    # Check condition
    assert isinstance(node.condition, BinaryOpNode)
    assert node.condition.op == "<"
    assert isinstance(node.condition.left, IdentifierNode)
    assert node.condition.left.name == "i"
    # Check increment
    assert isinstance(node.increment, UnaryOpNode)
    assert node.increment.operator == "++"
    assert isinstance(node.increment.operand, IdentifierNode)
    assert node.increment.operand.name == "i"
    # Check body
    assert isinstance(node.body, list)
    assert len(node.body) == 1
    # Check assignment in body
    assign = node.body[0]
    assert hasattr(assign, "name") and assign.name == "a"