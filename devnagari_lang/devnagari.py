#!/usr/bin/env python3

import sys
import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

def run_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source = file.read()
        run(source, file_path)
    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
        sys.exit(1)

def run_repl():
    print("देवनागरी प्रोग्रामिंग भाषा REPL (Interactive Shell)")
    print("Type 'exit' or press Ctrl+D to exit")
    print()
    
    while True:
        try:
            line = input(">>> ")
            if line.lower() == "exit":
                break
            if line.strip():
                run(line, "REPL")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            continue
        except Exception as e:
            print(f"Error: {str(e)}")

def run(source, source_name="<script>"):
    try:
        # Create lexer and generate tokens
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        
        # Create parser and parse tokens into an AST
        parser = Parser(tokens)
        statements = parser.parse()
        
        # Create interpreter and evaluate the AST
        interpreter = Interpreter()
        interpreter.interpret(statements)
    except Exception as e:
        print(f"Error in {source_name}: {str(e)}")
        if not source_name == "REPL":
            sys.exit(1)

def print_usage():
    print("Usage: devnagari [script]")
    print()
    print("If no script is provided, starts an interactive REPL")
    print("Options:")
    print("  script    Path to a Devanagari language script file")

def main():
    args = sys.argv[1:]
    
    if len(args) > 1:
        print("Error: Too many arguments")
        print_usage()
        sys.exit(1)
    
    if len(args) == 1:
        if args[0] in ['-h', '--help']:
            print_usage()
            sys.exit(0)
        run_file(args[0])
    else:
        run_repl()

if __name__ == "__main__":
    main() 