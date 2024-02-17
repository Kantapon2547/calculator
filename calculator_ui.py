import tkinter as tk
from tkinter import ttk
from keypad import Keypad


class CalculatorUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.display = None
        self.state = 'init'
        self.history = []

        self.init_components()

    def init_components(self):
        """Create components and layout the UI."""
        self.display = self.make_display()
        keypad = self.make_keypad()
        operators = self.make_operator_pad()

        self.display.pack(side=tk.TOP, expand=True, fill=tk.X)
        keypad.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        operators.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def make_display(self) -> tk.Entry:
        """Create a display for text."""
        display = tk.Entry(self, justify='right', state='disabled', font=('Arial', 14), fg='white', bg='black')
        return display

    def make_keypad(self) -> Keypad:
        """Create a keypad containing buttons for the numeric keys."""
        keypad = Keypad(self, keynames=list('789456123 0.'), columns=3, spacing_color='light blue')
        keypad.bind("<Button>", self.handle_keypress)
        return keypad

    def make_operator_pad(self):
        """Create a frame containing buttons for the operator keys."""
        frame = tk.Frame(self)

        operators = ['DEL', 'CLR', '+', '-', '*', '/', '^', 'mod']
        functions = ['exp', 'ln', 'log10', 'log2', 'sqrt', '=']
        all_operators = operators + functions

        for i, operator in enumerate(all_operators):
            if operator in operators:
                button = tk.Button(frame, text=operator, command=lambda o=operator: self.update_display(o))
            else:
                button = tk.Button(frame, text=operator, command=lambda o=operator: self.update_display_with_function(o))
            button.grid(row=i//2, column=i % 2, padx=2, pady=2, sticky="nsew")

        for i in range(4):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        return frame

    def make_function_combobox(self) -> ttk.Combobox:
        """Create a combobox for selecting mathematical functions."""
        combobox = ttk.Combobox(self, values=['exp', 'ln', 'log10', 'log2', 'sqrt'])
        combobox.bind("<<ComboboxSelected>>", self.handle_function_select)
        return combobox

    def handle_function_select(self, event):
        """Handle selection of a mathematical function from the combobox."""
        function = event.widget.get()
        self.update_display_with_function(function)

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
                result = str(eval(current_text))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.history.append(current_text)
            except Exception as e:
                self.display.configure(bg='red')
                self.after(100, lambda: self.display.configure(
                    bg='black'))
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error: " + str(e))
        elif value == '^':
            self.display.insert(tk.END, '**2')
        elif value == 'DEL':
            if len(current_text) > 0:
                self.display.delete(len(current_text) - 1)
        elif value == 'CLR':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, value)
        self.display.config(state='disabled')

    def update_display_with_function(self, function):
        """Update the display field with a selected mathematical function."""
        current_text = self.display.get()
        self.display.config(state='normal')
        if current_text.endswith(('+', '-', '*', '/', '^', 'mod', 'exp', 'ln', 'log10', 'log2', 'sqrt')):
            self.display.insert(tk.END, function + '(')
        else:
            self.display.insert(tk.END, '*' + function + '(')
        self.display.config(state='disabled')

    def run(self):
        """Starts the app and waits for events."""
        self.mainloop()
