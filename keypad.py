import tkinter as tk


class Keypad(tk.Frame):

    def __init__(self, parent, keynames=None, columns=1, spacing_color='blue', **kwargs):
        super().__init__(parent, **kwargs)
        self.keynames = keynames if keynames else []
        self.columns = columns
        self.spacing_color = spacing_color
        self.buttons = []
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        for i in range(len(self.keynames) // columns + 1):
            self.grid_rowconfigure(i, weight=1)
        for i in range(columns):
            self.grid_columnconfigure(i, weight=1)

        row = 0
        col = 0
        for keyname in self.keynames:
            button = tk.Button(self, text=keyname, foreground='red')
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.buttons.append(button)

            col += 1
            if col >= columns:
                col = 0
                row += 1

        self.configure(background=self.spacing_color)

    def bind(self, sequence=None, func=None, add=None):
        """Bind an event handler to an event sequence."""
        for button in self.buttons:
            button.bind(sequence, func, add)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for button in self.buttons:
            button[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        return self.buttons[0][key]


def handle_press(event):
    button = event.widget

    button.configure(background='lightgrey')

    button.after(200, lambda: button.configure(background='SystemButtonFace'))

    print(f"Button {button['text']} pressed")


if __name__ == '__main__':
    keys = list('789456123 0.')  # = ['7','8','9',...]

    root = tk.Tk()
    root.title("Keypad Demo")
    keypad = Keypad(root, keynames=keys, columns=3, spacing_color='light blue')
    keypad.pack(expand=True, fill=tk.BOTH)

    keypad.bind("<Button>", handle_press)
    keypad['font'] = ('Monospace', 16)

    root.mainloop()
