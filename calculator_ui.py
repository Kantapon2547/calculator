import tkinter as tk
from keypad import Keypad
from calculate import Calculate


class CalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.display = None
        self.history_display = None
        self.state = 'init'
        self.history = []

        self.init_components()

    def init_components(self):
        """Create components and layout the UI."""
        self.display = self.make_display()
        self.history_display = self.make_history_display()
        self.history_display.config(height=10, width=50)
        keypad = self.make_keypad()
        operators = self.make_operator_pad()

        self.history_display.pack(side=tk.TOP, expand=True, fill=tk.X)
        self.display.pack(side=tk.TOP, expand=True, fill=tk.X)
        keypad.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        operators.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def make_display(self) -> tk.Entry:
        """Create a display for text."""
        display = tk.Entry(self, justify='right', state='disabled', font=('Arial', 14))
        return display

    def make_history_display(self) -> tk.Text:
        """Create a display for history."""
        history_display = tk.Text(self, state='disabled', font=('Arial', 12))
        return history_display

    def make_keypad(self) -> Keypad:
        """Create a keypad containing buttons for the numeric keys."""
        keypad = Keypad(self, keynames=list('789456123 0.'), columns=3, spacing_color='light blue')
        keypad.bind("<Button>", self.handle_keypress)
        return keypad

    def make_operator_pad(self):
        """Create a frame containing buttons for the operator keys."""
        frame = tk.Frame(self)

        operators = ['DEL', 'CLR', '+', '-', '*', '/', '^', '=', '(', ')']
        functions = ['exp', 'ln', 'log10', 'log2', 'sqrt', 'mod']
        all_operators = operators + functions

        for i, operator in enumerate(all_operators):
            if operator in operators:
                button = tk.Button(frame, text=operator, command=lambda o=operator: self.update_display(o))
            else:
                button = tk.Button(frame, text=operator,
                                   command=lambda o=operator: self.update_display_function(o))
            button.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="nsew")

        for i in range(4):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        return frame

    def handle_function_select(self, event):
        """Handle selection of a mathematical function from the combobox."""
        function = event.widget.get()
        self.update_display_function(function)

    def handle_keypress(self, event):
        """Handle button press events."""
        button = event.widget
        value = button['text']
        self.update_display(value)

    def update_display(self, value):
        """Update the display field."""
        current_text = self.display.get()
        self.display.config(state='normal')
        if value == '=':
            try:
                result = Calculate.calculate(current_text)  # Calculate the result
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.history_display.config(state='normal')
                self.history_display.insert(tk.END, f"{current_text} = {result}\n{'-' * 50}\n")
                self.history_display.config(state='disabled')
                self.history.append((current_text, result))
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error: " + str(e))
        elif value == '^':
            self.display.insert(tk.END, '**2')
        elif value == 'DEL':
            if len(current_text) > 0:
                self.display.delete(len(current_text) - 1)
        elif value == 'CLR':
            self.display.delete(0, tk.END)
            self.history_display.config(state='normal')
            self.history_display.delete(1.0, tk.END)  # Clear the history display
            self.history_display.config(state='disabled')
            self.history.clear()  # Clear the history list
        elif value == '(':
            self.display.insert(tk.END, '(')
        elif value == ')':
            self.display.insert(tk.END, ')')
        elif value == 'exp':
            self.display.insert(tk.END, 'exp(')
        elif value == 'ln':
            self.display.insert(tk.END, 'ln(')
        elif value == 'log10':
            self.display.insert(tk.END, 'log10(')
        elif value == 'log2':
            self.display.insert(tk.END, 'log2(')
        elif value == 'mod':
            self.display.insert(tk.END, 'mod(')
        elif value == 'sqrt':
            self.display.insert(tk.END, 'sqrt(')
        else:
            self.display.insert(tk.END, value)
        self.display.config(state='disabled')

    def update_display_function(self, function):
        """Update the display field with a selected mathematical function."""
        current_text = self.display.get()
        self.display.config(state='normal')

        if not current_text:
            return  # Exit early if current_text is empty

        if function == 'exp':
            last_number = current_text.split()[-1]
            if last_number.isdigit():
                result = Calculate.exp(float(last_number))
                self.history.append(('exp', current_text, str(result)))
            else:
                self.display.insert(tk.END, function)
                return
        elif function == 'log10':
            last_number = current_text.split()[-1]
            if last_number.isdigit():
                result = Calculate.log10(float(last_number))
                self.history.append(('log10', current_text, str(result)))
            else:
                self.display.insert(tk.END, function)
                return
        elif function == 'log2':
            last_number = current_text.split()[-1]
            if last_number.isdigit():
                result = Calculate.log2(float(last_number))
                self.history.append(('log2', current_text, str(result)))
            else:
                self.display.insert(tk.END, function)
                return
        elif function == 'ln':
            last_number = current_text.split()[-1]
            if last_number.isdigit():
                result = Calculate.ln(float(last_number))
                self.history.append(('ln', current_text, str(result)))
            else:
                self.display.insert(tk.END, function)
                return
        elif function == 'sqrt':
            last_number = current_text.split()[-1]
            if last_number.isdigit():
                result = Calculate.sqrt(float(last_number))
                self.history.append(('sqrt', current_text, str(result)))
            else:
                self.display.insert(tk.END, function)
                return
        elif function == 'mod':
            last_number = current_text.split()[-1]
            if last_number.isdigit():
                second_last_number = current_text.split()[-2]
                result = Calculate.mod(float(second_last_number), float(last_number))
                self.history.append(('mod', current_text, str(result)))
            else:
                self.display.insert(tk.END, function)
                return
        else:
            self.display.insert(tk.END, function)
            return

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, str(result))
        self.display.config(state='disabled')

    def run(self):
        """Starts the app and waits for events."""
        self.mainloop()


if __name__ == "__main__":
    app = CalculatorUI()
    app.run()
