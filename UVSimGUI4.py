# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:44:23 2024

@author: Jakob, Jarek, Ben, Michael
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter.scrolledtext import ScrolledText
import os

# Import the UVSim class from UVSIM.py
from UVSIMM4 import UVSim, get_program

CONFIG_FILE = "config.txt" #this file contains UVU's colors for the main start up

class UVSimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("UVSim GUI")
        self.uvsim = UVSim()  # creating an instance of UVSim
        self.program = []     # variable to hold the loaded program
        
        # Load color scheme from configuration file
        self.primary_color, self.off_color = self.load_color_scheme()
        
        self.create_widgets()

    def load_color_scheme(self):
        """Load color scheme from the configuration file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                lines = file.readlines()
                primary_color = lines[0].split('=')[1].strip()
                off_color = lines[1].split('=')[1].strip()
        else:
            # the default UVU colors
            primary_color = '#4C721D'
            off_color = '#FFFFFF'
        return primary_color, off_color

    def save_color_scheme(self):
        """Save color scheme to the configuration file."""
        with open(CONFIG_FILE, 'w') as file:
            file.write(f"primary_color = {self.primary_color}\n")
            file.write(f"off_color = {self.off_color}\n")

    def create_widgets(self):
        # configuring the GUI colors
        self.master.configure(bg=self.primary_color)
        
        # Display output
        self.output_text = ScrolledText(self.master, width=60, height=10, bg=self.off_color)
        self.output_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # New area added to edit the loaded program
        self.program_text = ScrolledText(self.master, width=60, height=10, bg=self.off_color)
        self.program_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Load Program button
        self.load_button = tk.Button(self.master, text="Load Program", command=self.load_program, bg=self.off_color)
        self.load_button.grid(row=2, column=0, padx=10, pady=5)

        # Run button
        self.run_button = tk.Button(self.master, text="Run", command=self.run_program, bg=self.off_color)
        self.run_button.grid(row=2, column=1, padx=10, pady=5)

        # Reset button
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_program, bg=self.off_color)
        self.reset_button.grid(row=2, column=2, padx=10, pady=5)

        # Save Program button
        self.save_button = tk.Button(self.master, text="Save Program", command=self.save_program, bg=self.off_color)
        self.save_button.grid(row=3, column=0, padx=10, pady=5)

        # Change Color Scheme button
        self.color_button = tk.Button(self.master, text="Change Color Scheme", command=self.change_color_scheme, bg=self.off_color)
        self.color_button.grid(row=3, column=1, padx=10, pady=5)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit, bg=self.off_color)
        self.quit_button.grid(row=3, column=2, padx=10, pady=5)

        # Menu for editing actions
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=lambda: self.program_text.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.program_text.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.program_text.event_generate("<<Paste>>"))
        self.edit_menu.add_command(label="Add Line", command=self.add_line)
        self.edit_menu.add_command(label="Delete Line", command=self.delete_line)

    def load_program(self):
        """Load Program button callback function."""
        try:
            program_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if program_file:
                self.program = get_program(program_file)
                self.uvsim.load_program(self.program)
                self.program_text.delete(1.0, tk.END)
                for line in self.program:
                    self.program_text.insert(tk.END, line + '\n')
                self.output_text.insert(tk.END, f"Program loaded successfully: {program_file}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading program: {str(e)}")

    def save_program(self):
        """Save Program button callback function."""
        try:
            program_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if program_file:
                # Get the edited program from the text area
                self.program = self.program_text.get(1.0, tk.END).strip().split('\n')
                if len(self.program) > 100:
                    messagebox.showerror("Error", "Program exceeds the maximum of 100 instructions.")
                    return
                with open(program_file, 'w') as file:
                    for line in self.program:
                        file.write(line + '\n')
                self.output_text.insert(tk.END, f"Program saved successfully: {program_file}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving program: {str(e)}")

    def run_program(self):
        """Run button callback function."""
        try:
            # Get the edited program from the text area
            self.program = self.program_text.get(1.0, tk.END).strip().split('\n')
            if len(self.program) > 100:
                messagebox.showerror("Error", "Program exceeds the maximum of 100 instructions.")
                return
            self.uvsim.load_program(self.program)
            self.output_text.insert(tk.END, "Starting program execution...\n")

            while self.uvsim.running:
                instruction = self.uvsim.fetch()
                if instruction[1:3] == '10':  # Handle READ opcode
                    self.handle_read(instruction)
                else:
                    self.uvsim.decode_execute(instruction)

            self.output_text.insert(tk.END, f"Accumulator = {self.uvsim.accumulator}\n")
            self.output_text.insert(tk.END, "Program execution completed.\n")

        except Exception as e:
            messagebox.showerror("Error", f"Error running program: {str(e)}")

    def handle_read(self, instruction):
        """Handle READ opcode."""
        operand = int(instruction[3:5])  # Get the operand from instruction
        value = simpledialog.askinteger("Input", "Enter an integer:")
        if value is not None:
            if value < -9999 or value > 9999:
                messagebox.showerror("Error", "Input must be between -9999 and 9999.")
            else:
                self.uvsim.memory[operand] = f'+{str(value).zfill(4)}'
                self.output_text.insert(tk.END, f"Input added: {value}\n")
        else:
            messagebox.showwarning("Warning", "No input provided.")

    def reset_program(self):
        """Reset button callback function."""
        self.uvsim = UVSim()  # Reset the UVSim instance
        self.program = []     # Reset the loaded program
        self.output_text.delete(1.0, tk.END)  # Clear all the output text
        self.program_text.delete(1.0, tk.END)  # Clear the program text
        self.output_text.insert(tk.END, "Program reset.\n")

    def change_color_scheme(self):
        """Change Color Scheme button callback function."""
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        off_color = colorchooser.askcolor(title="Choose Off Color")[1]
        if primary_color and off_color:
            self.primary_color = primary_color
            self.off_color = off_color
            self.save_color_scheme()
            self.apply_color_scheme()

    def apply_color_scheme(self):
        """Apply the selected color scheme."""
        self.master.configure(bg=self.primary_color)
        self.output_text.configure(bg=self.off_color)
        self.program_text.configure(bg=self.off_color)
        self.load_button.configure(bg=self.off_color)
        self.run_button.configure(bg=self.off_color)
        self.reset_button.configure(bg=self.off_color)
        self.save_button.configure(bg=self.off_color)
        self.color_button.configure(bg=self.off_color)
        self.quit_button.configure(bg=self.off_color)

    def add_line(self):
        """Add a new line to the program."""
        self.program_text.insert(tk.END, "+0000\n")

    def delete_line(self):
        """Delete the current line from the program."""
        try:
            current_index = self.program_text.index(tk.INSERT).split('.')[0]
            self.program_text.delete(f"{current_index}.0", f"{current_index}.end")
        except tk.TclError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()
