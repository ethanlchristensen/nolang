
from .astvisitor import ASTVisitor
from ..parser.expressions import *
from ..parser.statements import *
from ..lexer.token import Tokens

from ..util import py_type_to_nl
from ..util import stringify

from io import FileIO

class ASTPrinter(ASTVisitor):
    """
    ASTPrinter generates graphviz output of abstract syntax tree.
    """
    def __init__(self, out: FileIO):
        self.out = out

    def explore(self, program: list[Statement]):
        self.node_counter = 0
        self.out.write('digraph {')
        prog_node = self._make_node('<prog>')

        prev_node = prog_node
        for stmt in program:
            stmt_node = self._make_node('<stmt>')
            self._make_edge(prev_node, stmt_node)
            self._make_edge(stmt_node, stmt.visit(self))
            prev_node = stmt_node

        self.out.write('}\n')

    def visit_vardecl(self, stmt: VarDeclaration):
        vardecl_node = self._make_node('<var_decl>')
        self._make_edge(vardecl_node, self._make_node(r'\"no\"'))
        self._make_edge(vardecl_node, self._make_node(f'\\"{stmt.id}\\"'))

        if stmt.has_initializer():
            self._make_edge(vardecl_node, self._make_node(r'\"=\"'))
            self._make_edge(vardecl_node, stmt.init.visit(self))

        return vardecl_node

    def _create_body(self, body: Body):
        body_node = self._make_node('<body>')
        indent_node = self._make_node('INDENT')
        self._make_edge(body_node, indent_node)

        prev_node = body_node
        for stmt in body.stmts:
            stmt_node = self._make_node('<stmt>')
            self._make_edge(prev_node, stmt_node)
            self._make_edge(stmt_node, stmt.visit(self))
            prev_node = stmt_node

        dedent_node = self._make_node('DEDENT')
        self._make_edge(body_node, dedent_node)
        return body_node

    def visit_ifstmt(self, stmt: IfStatement):
        if_node = self._make_node('<if_stmt>')

        self._make_edge(if_node, self._make_node(r'\"if\"'))
        self._make_edge(if_node, stmt.cond.visit(self))
        self._make_edge(if_node, self._make_node('NEWLINE'))
        self._make_edge(if_node, self._create_body(stmt.if_body))

        for (cond, body) in stmt.erm_bodies:
            self._make_edge(if_node, self._make_node(r'\"erm\"'))
            self._make_edge(if_node, cond.visit(self))
            self._make_edge(if_node, self._make_node('NEWLINE'))
            self._make_edge(if_node, self._create_body(body))

        if stmt.has_hermph():
            self._make_edge(if_node, self._make_node(r'\"hermph\"'))
            self._make_edge(if_node, self._make_node('NEWLINE'))
            self._make_edge(if_node, self._create_body(stmt.hermph_body))

        return if_node

    def visit_whileloop(self, stmt: WhileStatement):
        if_node = self._make_node('<while_loop>')

        self._make_edge(if_node, self._make_node(r'\"while\"'))
        self._make_edge(if_node, stmt.cond.visit(self))
        self._make_edge(if_node, self._make_node('NEWLINE'))
        self._make_edge(if_node, self._create_body(stmt.while_body))

        if stmt.has_hermph():
            self._make_edge(if_node, self._make_node(r'\"hermph\"'))
            self._make_edge(if_node, self._make_node('NEWLINE'))
            self._make_edge(if_node, self._create_body(stmt.hermph_body))

        return if_node

    def visit_exprstmt(self, stmt: ExprStatement):
        expr_node = self._make_node('<expr_stmt>')
        self._make_edge(expr_node, stmt.expr.visit(self))
        return expr_node

    def visit_return(self, stmt: ReturnStatement):
        return_node = self._make_node('<return_stmt>')
        self._make_edge(return_node, self._make_node(r'\"pay\"'))

        if stmt.has_value():
            self._make_edge(return_node, stmt.value.visit(self))

        return return_node

    def visit_assign(self, expr: AssignExpression):
        assign_node = self._make_node('<assign_expr>')
        self._make_edge(assign_node, self._make_node(f'\\"{expr.id}\\"'))
        self._make_edge(assign_node, self._make_node(r'\"=\"'))
        self._make_edge(assign_node, expr.assign.visit(self))
        return assign_node

    def visit_call(self, expr: CallExpression):
        call_node = self._make_node('<call_expr>')
        self._make_edge(call_node, expr.callee.visit(self))
        self._make_edge(call_node, self._make_node(r'\"(\"'))

        if len(expr.args) > 0:
            self._make_edge(call_node, expr.args[0].visit(self))
            for i in range(1, len(expr.args)):
                self._make_edge(call_node, self._make_node(r'\",\"'))
                self._make_edge(call_node, expr.args[i].visit(self))

        self._make_edge(call_node, self._make_node(r'\")\"'))
        return call_node

    def visit_binexpr(self, expr: BinaryExpression):
        expr_node = self._make_node(self._binexpr_name(expr))
        self._make_edge(expr_node, expr.left.visit(self))
        self._make_edge(expr_node, self._make_node(f'\\"{expr.op}\\"'))
        self._make_edge(expr_node, expr.right.visit(self))
        return expr_node

    def visit_unexpr(self, expr: UnaryExpression):
        expr_node = self._make_node(self._unexpr_name(expr))
        self._make_edge(expr_node, self._make_node(f'\\"{expr.op}\\"'))
        self._make_edge(expr_node, expr.operand.visit(self))
        return expr_node

    def visit_literal(self, expr: Literal):
        val = stringify(expr.value())
        typ = py_type_to_nl(type(expr.value()))

        # Make escape sequences literal
        val = val.replace('\\', '\\\\')
        val = val.replace('\n', r'\\n')
        val = val.replace('\r', r'\\n')
        val = val.replace('\t', r'\\t')
        val = val.replace('\a', r'\\a')
        val = val.replace('\v', r'\\v')
        val = val.replace('\b', r'\\b')

        return self._make_node(f'\\"{val}\\" ({typ})')

    def visit_identifier(self, expr: Identifier):
        return self._make_node(f'\\"{expr.name()}\\"')

    ### Util ###

    def _make_node(self, label: str) -> int:
        self.node_counter += 1
        self.out.write(f'{self.node_counter} [label="{label}"];')
        return self.node_counter

    def _make_edge(self, parent: int, child: int) -> None:
        self.out.write(f'{parent} -> {child};')

    def _binexpr_name(self, expr: BinaryExpression):
        match expr.op.type_id:
            case Tokens.OR: return '<or_expr>'
            case Tokens.AND: return '<and_expr>'
            case Tokens.EQUAL: return '<eq_expr>'
            case Tokens.NEQUAL: return '<eq_expr>'
            case Tokens.LESS_THAN: return '<rel_expr>'
            case Tokens.GREATER_THAN: return '<rel_expr>'
            case Tokens.LESS_THAN_EQ: return '<rel_expr>'
            case Tokens.GREATER_THAN_EQ: return '<rel_expr>'
            case Tokens.PLUS: return '<add_expr>'
            case Tokens.MINUS: return '<add_expr>'
            case Tokens.STAR: return '<mul_expr>'
            case Tokens.SLASH: return '<mul_expr>'
            case Tokens.PERCENT: return '<mul_expr>'
            case Tokens.EXP: return '<exp_expr>'
            case _: raise Exception(f'Unknown expression: {expr}')

    def _unexpr_name(self, expr: UnaryExpression):
        match expr.op.type_id:
            case Tokens.NOT: return '<not_expr>'
            case Tokens.MINUS: return '<sign_expr>'
            case Tokens.PLUS: return '<sign_expr>'
            case _: raise Exception(f'Unknown expression: {expr}')
