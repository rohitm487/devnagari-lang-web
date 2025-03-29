from src.lexer import TokenType, Token

class Expr:
    def accept(self, visitor):
        pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

class Stmt:
    def accept(self, visitor):
        pass

class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

class Function(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)

class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class For(Stmt):
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_stmt(self)

class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class Return(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            decl = self.declaration()
            if decl is not None:  # Only add non-None statements
                statements.append(decl)
        return statements

    def declaration(self):
        try:
            if self.match(TokenType.VAR, TokenType.CONST):
                return self.var_declaration()
            if self.match(TokenType.FUNCTION):
                return self.function_declaration()
            return self.statement()
        except Exception as e:
            print(f"Parse error: {str(e)}")
            self.synchronize()
            return None

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUALS):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def function_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect function name.")
        self.consume(TokenType.LPAREN, "Expect '(' after function name.")
        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RPAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LBRACE, "Expect '{' before function body.")
        body = self.block()
        return Function(name, parameters, body)

    def statement(self):
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LBRACE):
            return Block(self.block())
        return self.expression_statement()

    def if_statement(self):
        condition = self.expression()
        self.consume(TokenType.LBRACE, "Expect '{' after if condition.")
        then_branch = self.block()
        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LBRACE, "Expect '{' after else.")
            else_branch = self.block()
        return If(condition, then_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        self.consume(TokenType.LBRACE, "Expect '{' after while condition.")
        body = self.block()
        return While(condition, body)

    def for_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match(TokenType.VAR):
            initializer = self.var_declaration()
        elif not self.match(TokenType.SEMICOLON):
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RPAREN):
            increment = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after for clauses.")

        self.consume(TokenType.LBRACE, "Expect '{' after for clauses.")
        body = self.block()

        # Desugar for loop into while loop
        if increment is not None:
            body.statements.append(Expression(increment))

        if condition is None:
            condition = Literal(True)

        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def block(self):
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            decl = self.declaration()
            if decl is not None:
                statements.append(decl)
        self.consume(TokenType.RBRACE, "Expect '}' after block.")
        return Block(statements)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.EQUALS):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                        TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NUMBER):
            return Literal(float(self.previous().literal))
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Grouping(expr)
        self.error(self.peek(), "Expect expression.")
        return None

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise Exception(f"{message} Got {self.peek()}")

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in [
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.CONST,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.RETURN
            ]:
                return

            self.advance()

    def error(self, token, message):
        print(f"Parse error at line {token.line}: {message}")
        raise Exception(message)

    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RPAREN, "Expect ')' after arguments.")
        return Call(callee, paren, arguments)

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None 