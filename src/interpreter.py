from src.parser import Binary, Grouping, Literal, Unary, Variable, Assign, Call, Stmt, Expression, Var, Function, If, While, For, Block, Print
from src.lexer import TokenType

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise Exception(f"Undefined variable '{name}'.")

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise Exception(f"Undefined variable '{name}'.")

    def assign_at(self, distance, name, value):
        self.ancestor(distance).values[name] = value

    def get_at(self, distance, name):
        return self.ancestor(distance).values.get(name)

    def ancestor(self, distance):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}

        # Add native functions
        self.globals.define("छाप", self.print_function)

    def print_function(self, args):
        print(*[self.stringify(arg) for arg in args])
        return None

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except Exception as e:
            print(f"Runtime error: {str(e)}")
            return None

    def execute(self, stmt):
        return stmt.accept(self)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.PLUS:
            # Handle string concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            self.check_number_operands(expr.operator, left, right)
            return float(left) + float(right)
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.MULTIPLY:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.DIVIDE:
            self.check_number_operands(expr.operator, left, right)
            if float(right) == 0:
                raise Exception("Division by zero")
            return float(left) / float(right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        return None

    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not callable(callee):
            raise Exception("Can only call functions.")
        if len(arguments) != len(expr.arguments):
            raise Exception(f"Expected {len(expr.arguments)} arguments but got {len(arguments)}.")
        return callee(arguments)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        return None

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name.lexeme)

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name.lexeme, value)
        return value

    def visit_expression_stmt(self, stmt):
        return self.evaluate(stmt.expression)

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_function_stmt(self, stmt):
        function = Function(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            return self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            return self.execute(stmt.else_branch)
        return None

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_for_stmt(self, stmt):
        if stmt.initializer is not None:
            self.execute(stmt.initializer)
        while stmt.condition is None or self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
            if stmt.increment is not None:
                self.evaluate(stmt.increment)
        return None

    def visit_block_stmt(self, stmt):
        try:
            previous = self.environment
            self.environment = Environment(previous)
            for statement in stmt.statements:
                self.execute(statement)
        finally:
            self.environment = previous
        return None

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def look_up_variable(self, name, expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name)
        return self.globals.get(name)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, (int, float)):
            return
        raise Exception(f"Operand must be a number for operator {operator.lexeme}")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise Exception(f"Operands must be numbers for operator {operator.lexeme}")

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def stringify(self, obj):
        if obj is None:
            return "निल"
        if isinstance(obj, bool):
            return "सत्य" if obj else "असत्य"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)

class Function:
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def __call__(self, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        
        try:
            interpreter = Interpreter()
            interpreter.environment = environment
            for statement in self.declaration.body.statements:
                interpreter.execute(statement)
        except Return as return_value:
            return return_value.value
        return None

class Return(Exception):
    def __init__(self, value):
        self.value = value 