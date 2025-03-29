from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def run(source):
    # Create lexer and generate tokens
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    # Debug: Print tokens
    print("Tokens:", [str(token) for token in tokens])
    
    # Create parser and parse tokens into an AST
    parser = Parser(tokens)
    statements = parser.parse()
    
    # Create interpreter and evaluate the AST
    interpreter = Interpreter()
    interpreter.interpret(statements)

# Example program demonstrating various features
program = """
// Variable declarations
वैरिएबल x = 10;
वैरिएबल y = 20;

// Function definition
फंक्शन add(a, b) {
    वापस a + b;
}

// If statement
अगर x > 5 {
    छाप "x is greater than 5";
} अन्यथा {
    छाप "x is less than or equal to 5";
}

// While loop
वैरिएबल count = 0;
जबतक count < 3 {
    छाप "Count: " + count;
    count = count + 1;
}

// For loop
केलिए (वैरिएबल i = 0; i < 3; i = i + 1) {
    छाप "Loop iteration: " + i;
}

// Function call
वैरिएबल result = add(x, y);
छाप "Sum of " + x + " and " + y + " is: " + result;

// Complex expression
वैरिएबल z = (x + y) * 2;
छाप "Complex calculation result: " + z;
"""

def main():
    print("Welcome to Devanagari Programming Language!")
    print("Running example program:\n")
    run(program)

if __name__ == "__main__":
    main() 