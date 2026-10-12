import tkinter as tk  # Importing the Tkinter library for GUI
from tkinter.font import Font  # Importing the Font class for custom fonts


class Stack:
    def __init__(self):
        self.items = []  # Initialize an empty list to use as the stack

    def push(self, item):
        self.items.append(item)  # Add an item to the top of the stack

    def peek(self):
        if self.isempty():
            return None  # Return None if the stack is empty
        return self.items[-1]  # Return the top item of the stack without removing it

    def pop(self):
        if self.isempty():
            return None  # Return None if the stack is empty
        return self.items.pop()  # Remove and return the top item of the stack

    def length(self):
        return len(self.items)  # Return the number of items in the stack

    def isempty(self):
        return len(self.items) == 0  # Return True if the stack is empty, otherwise False

    def display(self):
        if self.isempty():
            return  # If the stack is empty, do nothing
        temps = Stack()  # Temporary stack to hold items for display
        while not self.isempty():
            x = self.peek()
            print("~", x)  # Print the top item of the stack
            temps.push(x)  # Push the item to the temporary stack
            self.pop()  # Remove the item from the original stack
        while not temps.isempty():
            x = temps.peek()
            self.push(x)  # Push the item back to the original stack
            temps.pop()  # Remove the item from the temporary stack

    def isOperand(self, ch):
        return ch.isdigit()  # Check if the character is a digit (operand)

    def notGreater(self, i):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3, '>': 0, '<': 0, '>=': 0, '<=': 0, '==': 0,
                      '!=': 0, '&&': -1, '||': -1}  # Define operator precedence
        if self.peek() == '(':
            return False  # '(' has the lowest precedence
        a = precedence[i]
        b = precedence[self.peek()]
        return a <= b  # Compare precedence of current operator and stack top operator

    def infixToPostfix(self, exp):
        if len(exp) > 256:
            raise ValueError("Expression exceeds 256 characters")  # Limit the expression length

        output = ""
        i = 0
        parentheses_stack = []  # Stack to keep track of parentheses

        while i < len(exp):
            if exp[i].isdigit():
                num = ""
                while i < len(exp) and exp[i].isdigit():
                    num += exp[i]
                    i += 1
                output += num + " "  # Add operand to output
            else:
                if exp[i] == '-' and (i == 0 or exp[i - 1] in "+-*/%^><=()"):
                    raise ValueError("Negative numbers are not allowed")  # Negative numbers not allowed
                if exp[i:i + 2] in ('>=', '<=', '==', '!=', '&&', '||'):
                    item = exp[i:i + 2]
                    i += 2
                else:
                    item = exp[i]
                    i += 1

                if self.isOperand(item):
                    output += item + " "
                elif item == '(':
                    self.push(item)  # Push '(' to stack
                    parentheses_stack.append('(')  # Track open parenthesis
                elif item == ')':
                    if not parentheses_stack:
                        raise ValueError("Mismatched parentheses")
                    parentheses_stack.pop()
                    while not self.isempty() and self.peek() != '(':
                        output += self.pop() + " "
                    if not self.isempty() and self.peek() != '(':
                        return -1
                    else:
                        self.pop()  # Pop '(' from stack
                else:
                    if not output.strip() or output.strip()[-1] in '+-*/%^><=()':
                        raise ValueError("Missing operand")
                    while not self.isempty() and self.notGreater(item):
                        output += self.pop() + " "
                    self.push(item)  # Push operator to stack
                i += 0  # no additional increment needed

        if parentheses_stack:
            raise ValueError("Mismatched parentheses")

        while not self.isempty():
            output += self.pop() + " "  # Pop all remaining operators

        return output.strip()  # Return the postfix expression

    def evaluatePostfix(self, exp):
        for item in exp.split():
            if item.isdigit():
                self.push(int(item))  # Push operand to stack
            else:
                val1 = self.pop()
                val2 = self.pop()
                if item == '+':
                    self.push(val2 + val1)  # Perform addition
                elif item == '-':
                    self.push(val2 - val1)  # Perform subtraction
                elif item == '*':
                    self.push(val2 * val1)  # Perform multiplication
                elif item == '/':
                    if val1 == 0:
                        raise ZeroDivisionError("Division by zero")
                    self.push(val2 / val1)  # Perform division
                elif item == '%':
                    self.push(val2 % val1)  # Perform modulus
                elif item == '^':
                    self.push(val2 ** val1)  # Perform exponentiation
                elif item == '>':
                    self.push(val2 > val1)  # Greater than comparison
                elif item == '<':
                    self.push(val2 < val1)  # Less than comparison
                elif item == '>=':
                    self.push(val2 >= val1)  # Greater than or equal to comparison
                elif item == '<=':
                    self.push(val2 <= val1)  # Less than or equal to comparison
                elif item == '==':
                    self.push(val2 == val1)  # Equal to comparison
                elif item == '!=':
                    self.push(val2 != val1)  # Not equal to comparison
                elif item == '&&':
                    self.push(val2 and val1)  # Logical AND
                elif item == '||':
                    self.push(val2 or val1)  # Logical OR
                else:
                    raise ValueError(f"Invalid operation")
        return self.pop()  # Return the final result


def convert_expression():
    expression = entry.get()  # Get the input expression from the GUI entry widget
    s = Stack()
    try:
        postfix = s.infixToPostfix(expression)  # Convert infix to postfix
        if postfix != -1:
            output_label.config(text=f"Postfix: {postfix}")  # Display postfix expression
            try:
                result = s.evaluatePostfix(postfix)  # Evaluate the postfix expression
                result_label.config(text=f"Result: {int(result)}")  # Display the result
                error_label.config(text="")  # Clear any previous error message
            except ZeroDivisionError as zde:
                error_label.config(text=f"Error: {zde}")  # Handle division by zero
            except ValueError as ve:
                error_label.config(text=f"Error: {ve}")  # Handle other value errors
            except Exception as e:
                error_label.config(text=f"Error: {e}")  # Handle any other exceptions
        else:
            error_label.config(text="Error: Invalid expression")  # Handle invalid expressions
    except ValueError as ve:
        error_label.config(text=f"Error: {ve}")  # Handle invalid expressions


# main window setup
root = tk.Tk()
root.title("Infix to Postfix Converter")

# Font
font_style = Font(family="Noir Pro", size=15)

# Create and pack the GUI widgets
entry_label = tk.Label(root, text="Enter Infix Expression", font=font_style)
entry_label.pack(pady=30)
entry = tk.Entry(root, width=50, font=font_style)
entry.pack(pady=20)
convert_button = tk.Button(root, text="Convert", command=convert_expression, font=font_style)
convert_button.pack(pady=15)
output_label = tk.Label(root, text="Postfix:", font=font_style)
output_label.pack(pady=10)
result_label = tk.Label(root, text="Expression evaluated value:", font=font_style)
result_label.pack(pady=10)

# Error label for displaying error messages
error_label = tk.Label(root, text="", font=font_style, fg="red")
error_label.pack(pady=10)

# Start the main loop
root.mainloop()
