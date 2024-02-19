import math
import ast
import tkinter as tk


class Calculate(tk.Tk):

    @staticmethod
    def calculate(expression):
        try:
            expression = expression.replace('exp', 'math.exp')
            expression = expression.replace('log10', 'math.log10')
            expression = expression.replace('log2', 'math.log2')
            expression = expression.replace('ln', 'math.log')
            expression = expression.replace('sqrt', 'math.sqrt')
            expression = expression.replace('mod', '%')

            # Parse the expression into an Abstract Syntax Tree (AST)
            node = ast.parse(expression, mode='eval')

            # Use the `compile` function to create a code object from the AST
            code = compile(node, '<string>', 'eval')

            # Use the `eval` function to evaluate the code object in a safe environment
            result = eval(code, {'math': math})

            return str(result)
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def square_root(x):
        """Calculate the square root of a number."""
        return math.sqrt(x)

    @staticmethod
    def exp(x):
        """Calculate the exponential of a number."""
        return math.exp(x)

    @staticmethod
    def log10(x):
        """Calculate the base-10 logarithm of a number."""
        return math.log10(x)

    @staticmethod
    def log2(x):
        """Calculate the base-2 logarithm of a number."""
        return math.log2(x)

    @staticmethod
    def ln(x):
        """Calculate the natural logarithm of a number."""
        return math.log(x)

    @staticmethod
    def sqrt(x):
        """Calculate the square root of a number."""
        return math.sqrt(x)

    @staticmethod
    def mod(x, y):
        """Calculate the modulus of two numbers."""
        return x % y
