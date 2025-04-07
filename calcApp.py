# Import necessary modules
import tkinter as tk  # Base tkinter module for GUI
from logging import disable
from tkinter import ttk  # Themed widget set
from zoneinfo import available_timezones

from ttkthemes import ThemedTk  # Enables custom themes for the app

# Function to handle button clicks
def handle_button_click(clicked_button_text):
    current_text = result_var.get()  # Get current input/display

    if clicked_button_text == "=":  # If equals button is pressed
        try:
            # Replace symbols for division and multiplication with Python equivalents
            expression = current_text.replace("÷", "/").replace("x", "*")
            result = eval(expression)  # Evaluate the expression safely

            # Fix floating-point rounding issues by rounding to 10 decimal places
            result = round(result, 10)

            # Display as integer if the result is a whole number
            if result == int(result):
                result = int(result)

            result_var.set(result)  # Display the result
        except Exception as e:
            result_var.set("Error")  # Show error for invalid input
            # Store history entries
            history = []

            # History display (read-only Text Widget)
            history_text = tk.Text(root, height=6, state="disabled", font=("Helvetica", 12))
            history_text.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

            # Add to history if successful
            history.append(f"{expression} = {result}")

            # Update history display
            history_text.config(state="normal")
            history_text.delete("1.0", tk.end)
            for line in reversed(history[-10:]):
                history_text.insert(tk.END, line + "\n")
            history_text.config(state="disabled")

    elif clicked_button_text == "C":  # Clear the input
        result_var.set("")
    elif clicked_button_text == "%":  # Percentage calculation
        try:
            current_number = float(current_text)
            result_var.set(current_number / 100)  # Divide by 100
        except ValueError:
            result_var.set("Error")
    elif clicked_button_text == "±":  # Toggle positive/negative
        try:
            current_number = float(current_text)
            result_var.set(-current_number)  # Multiply by -1
        except ValueError:
            result_var.set("Error")
    else:
        # Append clicked button text to the current input
        result_var.set(current_text + clicked_button_text)


# Function to handle keypress events from the keyboard
def handle_keypress(event):
    key = event.char
    if key.isdigit() or key in "+-*/.":  # Accept numbers and math symbols
        handle_button_click(key)
    elif key == "\r":  # Enter key
        handle_button_click("=")
    elif key == "\b":  # Backspace key
        current_text = result_var.get()
        if len(current_text) > 0:
            result_var.set(current_text[:-1])  # Remove last character

# Create the main calculator window with a theme
root = ThemedTk(theme="arc")
available_themes = sorted(root.get_themes()) # Get available themes
def change_theme(event = None):
    selected = theme_var.get()
    root.set_theme(selected)
root.title("Calculator")
theme_var = tk.StringVar(value="arc")  # Default theme
theme_dropdown = ttk.Combobox(root, textvariable=theme_var, values=available_themes, state="readonly")
theme_dropdown.bind("<<ComboboxSelected>>", change_theme)
theme_dropdown.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

# Create a StringVar to store and update the display text
result_var = tk.StringVar()

# Entry widget to show input/output (large font, right-aligned)
result_entry = ttk.Entry(root, textvariable=result_var,
                         font=("Helvetica", 24), justify="right")
result_entry.grid(row=2, column=0, columnspan=4, sticky="nsew")

# Define button layout: (label, row, column[, columnspan])
buttons = [
    ("C", 3, 0), ("±", 3, 1), ("%", 3, 2), ("÷", 3, 3),
    ("7", 4, 0), ("8", 4, 1), ("9", 4, 2), ("x", 4, 3),
    ("4", 5, 0), ("5", 5, 1), ("6", 5, 2), ("-", 5, 3),
    ("1", 6, 0), ("2", 6, 1), ("3", 6, 2), ("+", 6, 3),
    ("0", 7, 0, 2), (".", 7, 2), ("=", 7, 3)
]

# Set style for buttons
style = ttk.Style(root)
style.theme_use('clam')  # Use a modern theme
style.configure("TButton", font=("Helvetica", 16), width=10, height=4)

# Create and place each button on the grid
for button_info in buttons:
    button_text, row, col = button_info[:3]
    colspan = button_info[3] if len(button_info) > 3 else 1
    button = ttk.Button(
        root,
        text=button_text,
        command=lambda text=button_text: handle_button_click(text),
        style="TButton"
    )
    button.grid(row=row, column=col, columnspan=colspan,
                sticky="nsew", ipadx=10, ipady=4, padx=5, pady=5)

# Make rows and columns stretch evenly when resizing
for i in range(8):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Set fixed window size with 9:16 ratio
width = 500
height = 700
root.geometry(f"{width}x{height}")

# Prevent window from being resizable
root.resizable(False, False)

# Enable keyboard interaction
root.bind("<Return>", lambda event: handle_button_click("="))
root.bind("<Key>", handle_keypress)

# Start the application loop
root.mainloop()
